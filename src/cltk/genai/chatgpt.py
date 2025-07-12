"""Call ChatGPT."""

import os
from typing import Optional

from openai import OpenAI
from openai import OpenAIError

from cltk.core.data_types import Doc, Language, Word
from cltk.core.exceptions import CLTKException, OpenAIInferenceError
from cltk.languages.utils import get_lang
from cltk.morphology.morphosyntax import MorphosyntacticFeatureBundle, from_ud
from cltk.utils.utils import load_env_file


class ChatGPT:
    def __init__(self, language: str, api_key: str, model: str = "gpt-4.1"):
        """Initialize the ChatGPT class and set up OpenAI connection."""
        self.api_key = api_key
        self.language: Language = get_lang(language)
        self.model: str = model
        self.client: OpenAI = OpenAI(api_key=self.api_key)

    def generate(self,  input_text: str, prompt_template: Optional[str] = None, print_raw_response: bool = False) -> Doc:
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
                model=self.model,
                input=prompt
            )
        except OpenAIError as openai_error:
            raise OpenAIInferenceError(f"An error from OpenAI occurred: {openai_error}")
        if print_raw_response:
            print("Raw response from OpenAI:", response.output_text)
        return self._post_process_response(response=response.output_text)

    def _post_process_response(self, response: str) -> Doc:
        """Post-process the response to format it correctly."""
        # Locate the start and end of the morphological tagging section
        start_index = response.find("---")
        end_index = response.rfind("---")
        if start_index == -1 or end_index == -1:
            raise OpenAIInferenceError("Response format is incorrect. Expected '---' markers not found.")

        # Extract the relevant section
        relevant_section = response[start_index + 3:end_index].strip()

        # Remove any extra whitespace or empty lines
        lines = [line.strip() for line in relevant_section.split("\n") if line.strip()]

        # Reconstruct the cleaned response
        cleaned_response = "\n".join(lines)

        # Parse the cleaned response
        word_level_info: dict[str, str] = self._get_word_info(response=cleaned_response)
        doc: Doc = self._build_cltk_doc(word_info_dict=word_level_info)
        return doc

    def _get_word_info(self, response: str, print_raw_response: bool = False) -> dict[str, str]:
        """Extract part of speech and morphological information from a word."""
        import re
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

    def _build_cltk_doc(self, word_info_dict: dict[str, str]) -> Doc:
        """Build a CLTK Doc object from the response."""

        doc = Doc(language=self.language.name)
        words: list[Word] = list()
        print("word_info_dict:", word_info_dict)
        for word, info in word_info_dict.items():
            pos_info = info.split("|")
            pos_tag = pos_info[0]
            morph_dict: dict[str, str] = dict()
            for feature in pos_info[1:]:
                if "=" not in feature:
                    continue  # Skip empty or malformed features
                key, value = feature.split("=")
                morph_dict[key] = value
            morph_features = MorphosyntacticFeatureBundle()
            for key, value in morph_dict.items():
                feature_instance = from_ud(key, value)
                if feature_instance:
                    morph_features[type(feature_instance)] = [feature_instance]

            cltk_word: Word = Word(
                string=word,
                upos=pos_tag,
                features=morph_features
            )
            print(cltk_word)
            print("")
            words.append(cltk_word)
        doc.words = words
        return doc


if __name__ == "__main__":
    load_env_file()
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise CLTKException("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    MODEL: str = "gpt-4.1"

    LANGUAGE: str = "grc"
    CHATGPT_GRC: ChatGPT = ChatGPT(language=LANGUAGE, api_key=OPENAI_API_KEY, model=MODEL)
    DEMOSTHENES_2_4: str = "Ἐγὼ γάρ, ὦ ἄνδρες Ἀθηναῖοι, τὸ μὲν παρρησιάσασθαι περὶ ὧν σκοπῶ καὶ λέγω τῇ πόλει, πλείστου ἀξιῶ· τοῦτο γάρ μοι δοκεῖ τοῖς ἀγαθοῖς πολίταις ἴδιον εἶναι· τὸ δὲ μὴ λέγειν ἃ δοκεῖ, πολλοῦ μοι δοκεῖ χεῖρον εἶναι καὶ τοῦ ψεύδεσθαι."
    DEMOSTHENES_DOC: Doc = CHATGPT_GRC.generate(input_text=DEMOSTHENES_2_4, print_raw_response=True)
    print(DEMOSTHENES_DOC)

    # JOB_1_13: str = "י וַיְהִי הַיּוֹם וּבָנָיו וּבְנוֹתָיו אֹכְלִים וְשֹׁתִים יַיִן בְּבֵית אֲחִיהֶם הַבְּכוֹר."
    # LANGUAGE: str = "hbo"
    # CHATGPT_HBO: ChatGPT = ChatGPT(language=LANGUAGE, api_key=OPENAI_API_KEY, model=MODEL)
    # POS_HBO: str = CHATGPT_HBO.generate(input_text=JOB_1_13)
    # print(POS_HBO)
