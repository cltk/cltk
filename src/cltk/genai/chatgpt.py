"""Call ChatGPT."""

import os
import re
from typing import Optional

from openai import OpenAI, OpenAIError

from cltk.alphabet.text_normalization import cltk_normalize
from cltk.core.data_types import Doc, Language, Word
from cltk.core.exceptions import CLTKException, OpenAIInferenceError
from cltk.languages.utils import get_lang
from cltk.morphology.morphosyntax import (
    FORM_UD_MAP,
    MorphosyntacticFeatureBundle,
    from_ud,
)
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

    def generate_pos(
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

    def _post_process_response(self, response: str, input_text: str) -> Doc:
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
        value = re.sub(r"\s*\(.*?\)", "", value)
        value = value.split()[0]
        if "/" in value:
            return value.split("/")
        # Specific rewrites
        if key == "Tense" and value in ["Aor"]:
            return ["Past"]
        if key == "Tense" and value in ["Plup"]:
            return ["Pqp"]
        if key == "Tense" and value in ["Imperf", "Imperfect"]:
            return ["Imp"]
        if key == "Tense" and value in ["Pluperf"]:
            return ["Pqp"]
        if key == "Degree" and value in ["Comp"]:
            return ["Cmp"]
        if key == "Degree" and value in ["Compar"]:
            return ["Cmp"]
        if key == "Voice" and value == "Perf":
            return ["Act"]
        if key == "Voice" and value == "Med":
            return ["Mid"]
        if key == "Aspect" and value == "Aor":
            return ["Perf"]
        if key == "Aspect" and value == "Pres":
            return []
        if key == "Person" and value == "-":
            return []
        if key == "Mood" and value == "Part":
            return []
        if key == "Value":
            return [value]  # Will be mapped to NumValue by feature mapping logic
        return [value]

    def _build_cltk_doc(self, word_info_dict: dict[str, str], input_text: str) -> Doc:
        doc = Doc(
            language=self.language.name,
            raw=input_text,
            normalized_text=cltk_normalize(input_text),
        )
        words: list[Word] = list()
        used_spans = []  # List of (start, stop) for already matched words

        def is_span_used(start, stop):
            for s, e in used_spans:
                if not (stop <= s or start >= e):
                    return True
            return False

        for idx, (word, info) in enumerate(word_info_dict.items()):
            # Normalize word for matching
            norm_word = cltk_normalize(word)
            pos_info = info.split("|")
            pos_tag = pos_info[0]
            morph_dict: dict[str, list[str]] = dict()
            custom_features: dict[str, list[str]] = dict()
            verbform_part_needed = False
            for feature in pos_info[1:]:
                if "=" not in feature:
                    continue  # Skip empty or malformed features
                key, value = feature.split("=")
                # Try to map non-UD features
                if key not in FORM_UD_MAP:
                    mapped = self._map_non_ud_feature(key, value)
                    for mapped_key, mapped_value in mapped:
                        if mapped_key in FORM_UD_MAP:
                            values = self._normalize_feature_value(
                                mapped_key, mapped_value
                            )
                            if values:
                                morph_dict[mapped_key] = values
                        else:
                            if mapped_key not in custom_features:
                                custom_features[mapped_key] = []
                            custom_features[mapped_key].append(mapped_value)
                else:
                    values = self._normalize_feature_value(key, value)
                    if key == "Mood" and value == "Part":
                        verbform_part_needed = True
                    if values:
                        morph_dict[key] = values
            # If Mood=Part was present, ensure VerbForm=Part is added
            if verbform_part_needed and (
                "VerbForm" not in morph_dict
                or "Part" not in morph_dict.get("VerbForm", [])
            ):
                if "VerbForm" in morph_dict:
                    morph_dict["VerbForm"].append("Part")
                else:
                    morph_dict["VerbForm"] = ["Part"]
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
            norm_input_text = cltk_normalize(input_text)
            pattern = re.compile(re.escape(norm_word))
            found = False
            for match in pattern.finditer(norm_input_text):
                start, stop = match.start(), match.end()
                if not is_span_used(start, stop):
                    index_char_start = start
                    index_char_stop = stop
                    used_spans.append((start, stop))
                    index_token = sum(1 for s, e in used_spans if s < start)
                    found = True
                    break
            if not found:
                # Log normalized word and input text
                print(
                    f"[MATCH FAIL] Normalized word: '{norm_word}' not found in normalized input text."
                )
                print(f"[MATCH FAIL] Normalized input text: '{norm_input_text}'")
                # Try more robust matching: ignore accents and case
                import unicodedata

                def strip_accents(s):
                    return "".join(
                        c
                        for c in unicodedata.normalize("NFD", s)
                        if unicodedata.category(c) != "Mn"
                    )

                norm_word_stripped = strip_accents(norm_word).lower()
                norm_input_text_stripped = strip_accents(norm_input_text).lower()
                pattern_stripped = re.compile(re.escape(norm_word_stripped))
                for match in pattern_stripped.finditer(norm_input_text_stripped):
                    start, stop = match.start(), match.end()
                    if not is_span_used(start, stop):
                        index_char_start = start
                        index_char_stop = stop
                        used_spans.append((start, stop))
                        index_token = sum(1 for s, e in used_spans if s < start)
                        print(
                            f"[MATCH RECOVERED] Found by accent/case-insensitive match: '{norm_word_stripped}'"
                        )
                        break
            if index_char_start is None:
                print(
                    f"Warning: Could not find word '{word}' in input_text for index assignment (even after accent/case-insensitive matching)."
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

    def generate_dependency(
        self,
        doc: Doc,
        prompt_template: Optional[str] = None,
        print_raw_response: bool = False,
    ) -> Doc:
        """
        Call the OpenAI API to generate Universal Dependencies syntax (dependency) information for each word in the Doc.
        Returns a CLTK Doc with dependency info added to each Word (governor, dependency_relation, etc.).
        """
        # Prepare input for prompt: line-by-line tokens with features
        lines = []
        for idx, word in enumerate(doc.words, start=1):
            features_str = "|".join(
                f"{key.__name__}={val[0].name if hasattr(val[0], 'name') else val[0]}"
                for key, val in word.features.items()
                if val and val[0] is not None
            )
            line = f"{idx}\t{word.string}\t{word.upos}"
            if features_str:
                line += f"\t{features_str}"
            lines.append(line)
        token_table = "\n".join(lines)
        if not prompt_template:
            prompt = f"""Given the following Ancient Greek text and its Universal Dependencies POS and morphological tags, return the syntactic dependency parse for each word in UD format (index, word, head index, relation, and all UD features):\n\n{token_table}\n\nReturn each word on its own line, with columns: index, word, head index, relation, and all UD features. Do not return a parse tree, only line-by-line explanations."""
        else:
            prompt = prompt_template.format(token_table=token_table)
        try:
            response = self.client.responses.create(
                model=self.model, input=prompt, temperature=self.temperature
            )
        except OpenAIError as openai_error:
            raise OpenAIInferenceError(f"An error from OpenAI occurred: {openai_error}")
        if print_raw_response:
            print("Raw response from OpenAI:", response.output_text)
        # Parse response: expect tab-separated columns per line
        dep_lines = [
            line.strip()
            for line in response.output_text.split("\n")
            if line.strip() and not line.strip().startswith("#")
        ]
        # Attach dependency info to each Word in the Doc
        for i, line in enumerate(dep_lines):
            parts = line.split("\t")
            if len(parts) < 4 or i >= len(doc.words):
                continue  # skip malformed lines or out-of-range
            word_obj = doc.words[i]
            word_obj.governor = int(parts[2]) if parts[2].isdigit() else None
            word_obj.dependency_relation = parts[3]
            if len(parts) > 4:
                # Normalize each extra feature
                normalized_extras = []
                for feat in parts[4:]:
                    if "=" in feat:
                        key, value = feat.split("=", 1)
                        norm_values = self._normalize_feature_value(key, value)
                        for norm_value in norm_values:
                            normalized_extras.append(f"{key}={norm_value}")
                    else:
                        normalized_extras.append(feat)
                extra = "|".join(normalized_extras)
                if word_obj.definition:
                    word_obj.definition += f"; dep: {extra}"
                else:
                    word_obj.definition = f"dep: {extra}"
        return doc

    def generate_all(
        self,
        input_text: str,
        pos_prompt_template: Optional[str] = None,
        dep_prompt_template: Optional[str] = None,
        print_raw_response: bool = False,
    ) -> Doc:
        """
        Generate both POS/morphological analysis and dependency parse for the input text.
        Returns a CLTK Doc with all information populated.
        """
        doc = self.generate_pos(
            input_text=input_text,
            prompt_template=pos_prompt_template,
            print_raw_response=print_raw_response,
        )
        doc = self.generate_dependency(
            doc=doc,
            prompt_template=dep_prompt_template,
            print_raw_response=print_raw_response,
        )
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
    DEMOSTHENES_2_4: str = "Ἐγὼ γάρ, ὦ ἄνδρες Ἀθηναῖοι, τὸ μὲν παρρησιάσασθαι περὶ ὧν σκοπῶ καὶ λέγω τῇ πόλει, πλείστου ἀξιῶ· τοῦτο γάρ μοι δοκεῖ τοῖς ἀγαθοῖς πολίταις ἴδιον εἶναι· τὸ δὲ μὴ λέγειν ἃ δοκεῖ, πολλοῦ μοι δοκεῖ χεῖρον εἶναι καὶ τοῦ ψεύδεσθαι."
    PLUTARCH_ANTHONY_27_2: str = "Καὶ γὰρ ἦν ὁ χρόνος ἐν ᾧ κατεπλεῖ Κλεοπάτρα κατὰ τὴν Κιλικίαν, παρακαλεσαμένη πρότερον τὸν Ἀντώνιον εἰς συνουσίαν. ἡ δὲ πλοῖον ἐν χρυσῷ πεπλουμένον ἔχουσα, τὰς μὲν νεᾶς ἀργυραῖς ἐστίλβειν κελεύσασα, τὸν δὲ αὐλὸν ἀνακρούοντα καὶ φλαυῖν τὰς τριήρεις ἰοῖς παντοδαποῖς ἀνακεκαλυμμένας, αὐτὴ καθήμενη χρυσῷ προσπεποίκιλτο καταπέτασμα, καὶ παίδες ὥσπερ Ἔρωτες περὶ αὐτὴν διῄεσαν."
    EXAMPLE_GRC: str = get_example_text("grc")
    GRC_DOC: Doc = CHATGPT_GRC.generate_all(
        input_text=PLUTARCH_ANTHONY_27_2, print_raw_response=True
    )
    input("Press Enter to print final Doc ...")
    print(GRC_DOC)

    # JOB_1_13: str = "י וַיְהִי הַיּוֹם וּבָנָיו וּבְנוֹתָיו אֹכְלִים וְשֹׁתִים יַיִן בְּבֵית אֲחִיהֶם הַבְּכוֹר."
    # LANGUAGE: str = "hbo"
    # CHATGPT_HBO: ChatGPT = ChatGPT(language=LANGUAGE, api_key=OPENAI_API_KEY, model=MODEL)
    # JOB_DOC: Doc = CHATGPT_HBO.generate(input_text=JOB_1_13)
    # print(JOB_DOC)
