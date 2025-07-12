"""Call ChatGPT."""

import os
import re
from typing import Optional

from openai import OpenAI, OpenAIError

from cltk.morphology.morphosyntax import FORM_UD_MAP
from cltk.core.data_types import Doc, Language, Word
from cltk.core.exceptions import CLTKException, OpenAIInferenceError
from cltk.languages.utils import get_lang
from cltk.morphology.morphosyntax import MorphosyntacticFeatureBundle, from_ud
from cltk.utils.utils import load_env_file


class ChatGPT:
    def __init__(
        self,
        language: str,
        api_key: str,
        model: str = "gpt-4.1",
        temperature: float = 1.0,
    ):
        """Initialize the ChatGPT class and set up OpenAI connection."""
        self.api_key = api_key
        self.language: Language = get_lang(language)
        self.model: str = model
        self.temperature: float = temperature
        self.client: OpenAI = OpenAI(api_key=self.api_key)

    def generate(
        self,
        input_text: str,
        prompt_template: Optional[str] = None,
        print_raw_response: bool = False,
    ) -> Doc:
        """Call the OpenAI API and return the response text."""
        if not prompt_template:
            prompt = f"""Return part of speech tags (including full morphological information) about the following text in the {self.language.name} language.

Return each word with its part of speech tag on its own line. Use the Universal Dependencies format. For each line/word, use markup as follows: `**Ἐγὼ**  – PRON|Case=Nom|Gender=Masc|Number=Sing|Person=1`.

{input_text}
"""
        else:
            prompt = prompt_template.format(input_text=input_text)
        try:
            response = self.client.responses.create(
                model=self.model, input=prompt, temperature=self.temperature
            )
        except OpenAIError as openai_error:
            raise OpenAIInferenceError(f"An error from OpenAI occurred: {openai_error}")
        if print_raw_response:
            print("Raw response from OpenAI:", response.output_text)
        return self._post_process_response(
            response=response.output_text, input_text=input_text
        )

    def _post_process_response(
        self, response: str, input_text: Optional[str] = None
    ) -> Doc:
        """Post-process the response to format it correctly."""
        # Try to extract between --- markers, but fall back to extracting lines with ** if not found
        start_index = response.find("---")
        end_index = response.rfind("---")
        if start_index != -1 and end_index != -1:
            relevant_section = response[start_index + 3 : end_index].strip()
            lines = [
                line.strip() for line in relevant_section.split("\n") if line.strip()
            ]
            cleaned_response = "\n".join(lines)
        else:
            # Fallback: extract only lines starting with **
            lines = [
                line.strip()
                for line in response.split("\n")
                if line.strip().startswith("**")
            ]
            cleaned_response = "\n".join(lines)
        word_level_info: dict[str, str] = self._get_word_info(response=cleaned_response)
        doc: Doc = self._build_cltk_doc(
            word_info_dict=word_level_info, input_text=input_text
        )
        return doc

    def _get_word_info(
        self, response: str, print_raw_response: bool = False
    ) -> dict[str, str]:
        """Extract part of speech and morphological information from a word."""

        word_info: dict[str, str] = {}
        # Regex matches: **word** <spaces> – or - <spaces> info
        pattern = re.compile(r"^\*\*(.+?)\*\*\s*[–-]\s*(.+)$")
        for line in response.split("\n"):
            line = line.strip()
            match = pattern.match(line)
            if match:
                word = match.group(1).strip()
                info = match.group(2).strip()
                word_info[word] = info
        return word_info

    def _map_non_ud_feature(self, key: str, value: str) -> list[tuple[str, str]]:
        """Map non-UD features to closest UD equivalents, or return as custom."""
        # Map PartType
        if key == "PartType":
            if value == "Disc":
                return [("Polarity", "Pos")]
            if value == "Conj":
                return [("POS", "CCONJ")]
        # Add more mappings as needed for other features
        # If no mapping, return as custom (for user inspection)
        return [(key, value)]

    def _normalize_feature_value(self, key: str, value: str) -> list[str]:
        """Normalize only problematic forms for UD features, stripping commentary and mapping non-UD features."""
        # Remove commentary in parentheses or after a space
        value = re.sub(r"\s*\(.*?\)", "", value)
        value = value.split()[0]
        # Handle slashed values (e.g., 'Acc/Gen')
        if "/" in value:
            return value.split("/")
        # Specific rewrites
        if key == "Tense" and value == "Aor":
            return ["Past"]
        if key == "Tense" and value == "Plup":
            return ["Pqp"]
        if key == "Degree" and value == "Comp":
            return ["Cmp"]
        if key == "Aspect" and value == "Aor":
            return ["Perf"]
        if key == "Aspect" and value == "Pres":
            return []  # Ignore invalid aspect value
        if key == "Voice" and value == "Perf":
            return ["Act"]
        return [value]

    def _build_cltk_doc(
        self, word_info_dict: dict[str, str], input_text: Optional[str] = None
    ) -> Doc:

        doc = Doc(language=self.language.name)
        words: list[Word] = list()
        used_spans = []  # List of (start, stop) for already matched words

        def is_span_used(start, stop):
            for s, e in used_spans:
                if not (stop <= s or start >= e):
                    return True
            return False

        for idx, (word, info) in enumerate(word_info_dict.items()):
            pos_info = info.split("|")
            pos_tag = pos_info[0]
            morph_dict: dict[str, list[str]] = dict()
            custom_features: dict[str, list[str]] = dict()
            for feature in pos_info[1:]:
                if "=" not in feature:
                    continue  # Skip empty or malformed features
                key, value = feature.split("=")
                # Try to map non-UD features
                if key not in FORM_UD_MAP:
                    mapped = self._map_non_ud_feature(key, value)
                    for mapped_key, mapped_value in mapped:
                        if mapped_key in FORM_UD_MAP:
                            values = self._normalize_feature_value(mapped_key, mapped_value)
                            if values:
                                morph_dict[mapped_key] = values
                        else:
                            # Store as custom feature for user inspection
                            if mapped_key not in custom_features:
                                custom_features[mapped_key] = []
                            custom_features[mapped_key].append(mapped_value)
                else:
                    values = self._normalize_feature_value(key, value)
                    if values:
                        morph_dict[key] = values
            morph_features = MorphosyntacticFeatureBundle()
            for key, values in morph_dict.items():
                for value in values:
                    feature_instance = from_ud(key, value)
                    if feature_instance:
                        morph_features[type(feature_instance)] = [feature_instance]
            # Find char indexes by searching for the word in input_text
            index_token = None
            index_char_start = None
            index_char_stop = None
            if input_text:

                # Use regex to find all occurrences of the word
                pattern = re.compile(re.escape(word))
                for match in pattern.finditer(input_text):
                    start, stop = match.start(), match.end()
                    if not is_span_used(start, stop):
                        index_char_start = start
                        index_char_stop = stop
                        used_spans.append((start, stop))
                        # Token index: count how many non-overlapping matches before this one
                        index_token = sum(1 for s, e in used_spans if s < start)
                        break
                if index_char_start is None:
                    print(
                        f"Warning: Could not find word '{word}' in input_text for index assignment."
                    )
            cltk_word: Word = Word(
                string=word,
                upos=pos_tag,
                features=morph_features,
                index_token=index_token,
                index_char_start=index_char_start,
                index_char_stop=index_char_stop,
            )
            # Optionally attach custom features to Word (for user inspection)
            if custom_features:
                cltk_word.definition = str(custom_features)
            words.append(cltk_word)
        doc.words = words
        return doc


if __name__ == "__main__":
    from cltk.languages.example_texts import get_example_text
    load_env_file()
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise CLTKException(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
        )
    MODEL: str = "gpt-4.1"
    TEMPERATURE: float = 1.0  # 0.2 recommended for consistent structured output

    LANGUAGE: str = "grc"
    CHATGPT_GRC: ChatGPT = ChatGPT(
        language=LANGUAGE, api_key=OPENAI_API_KEY, model=MODEL, temperature=TEMPERATURE
    )
    # DEMOSTHENES_2_4: str = "Ἐγὼ γάρ, ὦ ἄνδρες Ἀθηναῖοι, τὸ μὲν παρρησιάσασθαι περὶ ὧν σκοπῶ καὶ λέγω τῇ πόλει, πλείστου ἀξιῶ· τοῦτο γάρ μοι δοκεῖ τοῖς ἀγαθοῖς πολίταις ἴδιον εἶναι· τὸ δὲ μὴ λέγειν ἃ δοκεῖ, πολλοῦ μοι δοκεῖ χεῖρον εἶναι καὶ τοῦ ψεύδεσθαι."
    PLUTARCH_ANTHONY_27_2: str = "Καὶ γὰρ ἦν ὁ χρόνος ἐν ᾧ κατεπλεῖ Κλεοπάτρα κατὰ τὴν Κιλικίαν, παρακαλεσαμένη πρότερον τὸν Ἀντώνιον εἰς συνουσίαν. ἡ δὲ πλοῖον ἐν χρυσῷ πεπλουμένον ἔχουσα, τὰς μὲν νεᾶς ἀργυραῖς ἐστίλβειν κελεύσασα, τὸν δὲ αὐλὸν ἀνακρούοντα καὶ φλαυῖν τὰς τριήρεις ἰοῖς παντοδαποῖς ἀνακεκαλυμμένας, αὐτὴ καθήμενη χρυσῷ προσπεποίκιλτο καταπέτασμα, καὶ παίδες ὥσπερ Ἔρωτες περὶ αὐτὴν διῄεσαν."
    GRC_DOC: Doc = CHATGPT_GRC.generate(
        input_text=PLUTARCH_ANTHONY_27_2, print_raw_response=True
    )
    input("Press Enter to print final Doc ...")
    print(GRC_DOC)

    # JOB_1_13: str = "י וַיְהִי הַיּוֹם וּבָנָיו וּבְנוֹתָיו אֹכְלִים וְשֹׁתִים יַיִן בְּבֵית אֲחִיהֶם הַבְּכוֹר."
    # LANGUAGE: str = "hbo"
    # CHATGPT_HBO: ChatGPT = ChatGPT(language=LANGUAGE, api_key=OPENAI_API_KEY, model=MODEL)
    # JOB_DOC: Doc = CHATGPT_HBO.generate(input_text=JOB_1_13)
    # print(JOB_DOC)
