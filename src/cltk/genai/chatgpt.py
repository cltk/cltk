"""Call ChatGPT."""

import os
import re
from typing import Optional

from openai import OpenAI, OpenAIError

from cltk.alphabet.text_normalization import cltk_normalize
from cltk.core.cltk_logger import logger
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
        """Call the OpenAI API and return the response text, including lemma, gloss, NER, inflectional paradigm, and IPA pronunciation."""
        if not prompt_template:
            prompt = f"""For each word in the following {self.language.name} text, return a line in the following tab-separated format:
word<TAB>lemma<TAB>gloss<TAB>named_entity_type<TAB>inflectional_paradigm<TAB>IPA_pronunciation<TAB>POS|morphological_features (Universal Dependencies)

Text:
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
            logger.info(f"Raw response from OpenAI: {response.output_text}")
        return self._post_process_response(
            response=response.output_text,
            input_text=input_text,
            response_obj=response,
            print_raw_response=print_raw_response,
        )

    def _post_process_response(
        self,
        response: str,
        input_text: str,
        response_obj=None,
        print_raw_response: bool = False,
    ) -> Doc:
        """Post-process the response to format it correctly."""
        if print_raw_response:
            logger.debug(f"Raw OpenAI response: {response}")
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
        if print_raw_response:
            logger.debug(f"Cleaned response for word parsing: {cleaned_response}")
        word_level_info: dict[str, dict] = self._get_word_info(
            response=cleaned_response, print_raw_response=print_raw_response
        )
        if not word_level_info:
            logger.warning(
                "No word info parsed from response. Falling back to whitespace tokenization."
            )
            # Fallback: tokenize input_text and create minimal Word objects
            tokens = input_text.split()
            word_level_info = {
                token: {
                    "lemma": None,
                    "gloss": None,
                    "ner": None,
                    "paradigm": None,
                    "ipa": None,
                    "pos_morph": "X",
                }
                for token in tokens
            }
        doc: Doc = self._build_cltk_doc(
            word_info_dict=word_level_info, input_text=input_text
        )
        # Add ChatGPT metadata if available
        chatgpt_meta = {}
        if response_obj is not None:
            usage = getattr(response_obj, "usage", None)
            if usage is not None:
                chatgpt_meta["tokens_total"] = str(
                    getattr(
                        usage,
                        "total_tokens",
                        getattr(usage, "get", lambda k, d=None: d)("total_tokens", ""),
                    )
                )
            chatgpt_meta["model"] = str(
                getattr(response_obj, "model", getattr(self, "model", ""))
            )
            chatgpt_meta["temperature"] = str(getattr(self, "temperature", ""))
        doc.chatgpt = chatgpt_meta
        return doc

    def _get_word_info(
        self, response: str, print_raw_response: bool = False
    ) -> dict[str, dict]:
        """Extract all requested features from each word line. Add fallback if parsing fails."""
        word_info: dict[str, dict] = {}
        debug_lines = []
        # Expect tab-separated columns: word, lemma, gloss, NER, paradigm, IPA, POS|morph
        for line in response.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            debug_lines.append(line)
            parts = line.split("\t")
            if len(parts) >= 7:
                word, lemma, gloss, ner, paradigm, ipa, pos_morph = parts[:7]
                word_info[word] = {
                    "lemma": lemma if lemma else None,
                    "gloss": gloss if gloss else None,
                    "ner": ner if ner else None,
                    "paradigm": paradigm if paradigm else None,
                    "ipa": ipa if ipa else None,
                    "pos_morph": pos_morph,
                }
        # Fallback: try to parse lines with fewer columns or alternative formats
        if not word_info:
            if print_raw_response:
                logger.warning(
                    f"No words parsed from response. Attempting fallback parsing. Lines: {debug_lines}"
                )
            # Try to parse lines with at least word and POS|morph, using tab or space
            for line in response.split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Try tab, then space
                parts = line.split("\t")
                if len(parts) < 2:
                    parts = line.split()
                if len(parts) >= 2:
                    word = parts[0]
                    pos_morph = parts[-1]
                    word_info[word] = {
                        "lemma": None,
                        "gloss": None,
                        "ner": None,
                        "paradigm": None,
                        "ipa": None,
                        "pos_morph": pos_morph,
                    }
        if not word_info:
            if print_raw_response:
                logger.error(
                    f"Still no words parsed. Check prompt and response format. Lines: {debug_lines}"
                )
        else:
            if print_raw_response:
                logger.debug(f"Parsed word_info: {word_info}")
        return word_info

    def _build_cltk_doc(
        self,
        word_info_dict: dict[str, dict],
        input_text: str,
        print_raw_response: bool = False,
    ) -> Doc:
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
            norm_word = cltk_normalize(word)
            pos_info = info["pos_morph"].split("|")
            pos_tag = pos_info[0]
            morph_dict: dict[str, list[str]] = dict()
            custom_features: dict[str, list[str]] = dict()
            verbform_part_needed = False
            for feature in pos_info[1:]:
                if "=" not in feature:
                    continue
                key, value = feature.split("=")
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
            import re

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
                        break
            cltk_word: Word = Word(
                string=word,
                upos=pos_tag,
                features=morph_features,
                index_token=index_token,
                index_char_start=index_char_start,
                index_char_stop=index_char_stop,
            )
            # Set new features if present
            if info.get("lemma"):
                cltk_word.lemma = info["lemma"]
            if info.get("gloss"):
                cltk_word.definition = info["gloss"]
            if info.get("ner"):
                cltk_word.named_entity = info["ner"]
            if info.get("paradigm"):
                cltk_word.stem = info["paradigm"]
            if info.get("ipa"):
                cltk_word.phonetic_transcription = info["ipa"]
            if custom_features:
                if cltk_word.definition:
                    cltk_word.definition += f"; custom: {str(custom_features)}"
                else:
                    cltk_word.definition = str(custom_features)
            words.append(cltk_word)
        if not words:
            logger.warning(f"No Word objects created for input: {input_text}")
        else:
            logger.debug(
                f"Built {len(words)} Word objects: {[w.string for w in words]}"
            )
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
        # When iterating over doc.words, ensure it's a list
        words = doc.words if doc.words is not None else []
        for idx, word in enumerate(words, start=1):
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
            logger.info(f"Raw response from OpenAI: {response.output_text}")
        # Parse response: expect tab-separated columns per line
        dep_lines = [
            line.strip()
            for line in response.output_text.split("\n")
            if line.strip() and not line.strip().startswith("#")
        ]
        # Attach dependency info to each Word in the Doc
        for i, line in enumerate(dep_lines):
            parts = line.split("\t")
            if len(parts) < 4 or i >= len(words):
                continue  # skip malformed lines or out-of-range
            word_obj = words[i]
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
        Generate POS/morphological analysis, dependency parse, and enrich Doc with metadata (sentence segmentation, translation, summary, topic, discourse relations, coreferences).
        Returns a CLTK Doc with all information populated.
        """
        usage_meta = {}
        # POS/morphology
        pos_doc, pos_usage = self._call_with_usage(
            self.generate_pos,
            input_text=input_text,
            prompt_template=pos_prompt_template,
            print_raw_response=print_raw_response,
        )
        # Dependency
        dep_doc, dep_usage = self._call_with_usage(
            self.generate_dependency,
            doc=pos_doc,
            prompt_template=dep_prompt_template,
            print_raw_response=print_raw_response,
        )
        # Metadata
        metadata, metadata_usage = self._call_with_usage(
            self.generate_doc_metadata,
            input_text=input_text,
            print_raw_response=print_raw_response,
        )
        dep_doc.sentence_boundaries = metadata.get("sentence_boundaries", [])
        dep_doc.translation = metadata.get("translation", None)
        dep_doc.summary = metadata.get("summary", None)
        dep_doc.topic = metadata.get("topic", None)
        # Discourse relations
        discourse, discourse_usage = self._call_with_usage(
            self.generate_discourse_relations,
            input_text=input_text,
            print_raw_response=print_raw_response,
        )
        dep_doc.discourse_relations = discourse
        # Coreference resolution
        coref, coref_usage = self._call_with_usage(
            self.generate_coreferences,
            input_text=input_text,
            print_raw_response=print_raw_response,
        )
        dep_doc.coreferences = coref
        # Aggregate token usage
        tokens_per_call = {
            "pos": pos_usage,
            "dep": dep_usage,
            "metadata": metadata_usage,
            "discourse": discourse_usage,
            "coref": coref_usage,
        }
        total_tokens = sum(
            int(v)
            for v in tokens_per_call.values()
            if v is not None and str(v).isdigit()
        )
        dep_doc.chatgpt = {
            "tokens_total": total_tokens,
            "tokens_per_call": tokens_per_call,
            "model": self.model,
            "temperature": self.temperature,
        }
        return dep_doc

    def _call_with_usage(self, func, *args, **kwargs):
        """
        Helper to call a function and extract token usage from its response object or internal usage attributes.
        Returns (result, tokens_total) where result is the main output and tokens_total is an int or None.
        """
        if func == self.generate_pos:
            doc = func(*args, **kwargs)
            usage = (
                doc.chatgpt.get("tokens_total")
                if hasattr(doc, "chatgpt") and doc.chatgpt
                else None
            )
            return doc, usage
        elif func == self.generate_dependency:
            doc = func(*args, **kwargs)
            usage = (
                doc.chatgpt.get("tokens_total")
                if hasattr(doc, "chatgpt") and doc.chatgpt
                else None
            )
            return doc, usage
        elif func == self.generate_doc_metadata:
            result = func(*args, **kwargs)
            usage = getattr(self, "_last_metadata_usage", None)
            return result, usage
        elif func == self.generate_discourse_relations:
            result = func(*args, **kwargs)
            usage = getattr(self, "_last_discourse_usage", None)
            return result, usage
        elif func == self.generate_coreferences:
            result = func(*args, **kwargs)
            usage = getattr(self, "_last_coref_usage", None)
            return result, usage
        else:
            result = func(*args, **kwargs)
            usage = None
            if hasattr(result, "chatgpt") and result.chatgpt:
                usage = result.chatgpt.get("tokens_total")
            return result, usage

    def generate_doc_metadata(
        self,
        input_text: str,
        print_raw_response: bool = False,
    ) -> dict:
        """
        Call the OpenAI API to return sentence segmentation, translation, summary, and topic/domain classification for the input text.
        Returns a dict with keys: sentence_boundaries, translation, summary, topic.
        """
        prompt = f"""For the following text in {self.language.name}:

{input_text}

1. List each sentence on a new line. For each sentence, also return its character start and stop offsets in the original text, in the format: <sentence> <TAB> <start_offset> <TAB> <end_offset>.
2. Translate the entire text into English.
3. Summarize the text in 1-2 sentences.
4. Classify the topic or domain of the text (e.g., history, philosophy, poetry, law).

Return your answer as four sections, each starting with a header line:
---SENTENCES---
<sentence>\t<start>\t<end>
...
---TRANSLATION---
<translation>
---SUMMARY---
<summary>
---TOPIC---
<topic>
"""
        try:
            response = self.client.responses.create(
                model=self.model, input=prompt, temperature=self.temperature
            )
        except OpenAIError as openai_error:
            raise OpenAIInferenceError(f"An error from OpenAI occurred: {openai_error}")
        if print_raw_response:
            logger.info(f"Raw response from OpenAI: {response.output_text}")
        usage = getattr(response, "usage", None)
        usage_val = getattr(usage, "total_tokens", None)
        self._last_metadata_usage = (
            int(usage_val) if usage_val and str(usage_val).isdigit() else 0
        )
        # Parse response
        result = {}
        text = response.output_text
        # SENTENCES
        sentences_section = (
            text.split("---SENTENCES---")[-1].split("---TRANSLATION---")[0].strip()
        )
        sentence_boundaries = []
        for line in sentences_section.splitlines():
            parts = line.split("\t")
            if len(parts) == 3:
                sent, start, end = parts
                try:
                    start = int(start)
                    end = int(end)
                    sentence_boundaries.append((sent, start, end))
                except ValueError:
                    continue
        result["sentence_boundaries"] = sentence_boundaries
        # TRANSLATION
        translation_section = (
            text.split("---TRANSLATION---")[-1].split("---SUMMARY---")[0].strip()
        )
        result["translation"] = translation_section
        # SUMMARY
        summary_section = (
            text.split("---SUMMARY---")[-1].split("---TOPIC---")[0].strip()
        )
        result["summary"] = summary_section
        # TOPIC
        topic_section = text.split("---TOPIC---")[-1].strip()
        result["topic"] = topic_section
        return result

    def generate_discourse_relations(
        self,
        input_text: str,
        print_raw_response: bool = False,
    ) -> list[str]:
        """
        Call the OpenAI API to return discourse relations between sentences/clauses.
        Returns a list of relations.
        """
        prompt = f"""For the following text in {self.language.name}, for each sentence or clause, describe its discourse relation to the previous one (e.g., contrast, elaboration, cause, result). List each relation on a new line, in order.

{input_text}
"""
        try:
            response = self.client.responses.create(
                model=self.model, input=prompt, temperature=self.temperature
            )
        except OpenAIError as openai_error:
            raise OpenAIInferenceError(f"An error from OpenAI occurred: {openai_error}")
        if print_raw_response:
            logger.info(f"Raw response from OpenAI: {response.output_text}")
        usage = getattr(response, "usage", None)
        usage_val = getattr(usage, "total_tokens", None)
        self._last_discourse_usage = (
            int(usage_val) if usage_val and str(usage_val).isdigit() else 0
        )
        # Parse response
        relations = [
            line.strip() for line in response.output_text.splitlines() if line.strip()
        ]
        return relations

    def generate_coreferences(
        self,
        input_text: str,
        print_raw_response: bool = False,
    ) -> list[tuple[str, str, int, int]]:
        """
        Call the OpenAI API to return coreference resolution for pronouns and their referents.
        Returns a list of tuples: (pronoun, referent, sentence index, word index).
        """
        prompt = f"""For the following text in {self.language.name}, identify all pronouns and their referents. For each, return a line in the format: <pronoun> <TAB> <referent> <TAB> <sentence_index> <TAB> <word_index>.

{input_text}
"""
        try:
            response = self.client.responses.create(
                model=self.model, input=prompt, temperature=self.temperature
            )
        except OpenAIError as openai_error:
            raise OpenAIInferenceError(f"An error from OpenAI occurred: {openai_error}")
        if print_raw_response:
            logger.info(f"Raw response from OpenAI: {response.output_text}")
        usage = getattr(response, "usage", None)
        usage_val = getattr(usage, "total_tokens", None)
        self._last_coref_usage = (
            int(usage_val) if usage_val and str(usage_val).isdigit() else 0
        )
        # Parse response
        corefs = []
        for line in response.output_text.splitlines():
            parts = line.split("\t")
            if len(parts) == 4:
                pronoun, referent, sent_idx, word_idx = parts
                try:
                    sent_idx = int(sent_idx)
                    word_idx = int(word_idx)
                    corefs.append((pronoun, referent, sent_idx, word_idx))
                except ValueError:
                    continue
        return corefs

    def _map_non_ud_feature(self, key: str, value: str) -> list[tuple[str, str]]:
        """Map non-standard UD features to normalized format."""
        # For now, just return as a list of tuples
        return [(key, value)]

    def _normalize_feature_value(self, key: str, value: str) -> list:
        """Normalize UD feature values to canonical format."""
        # Placeholder: implement normalization logic or import from UD features module
        # For now, just return as a single-item list
        return [value]


if __name__ == "__main__":
    from cltk.languages.example_texts import get_example_text

    load_env_file()
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        logger.error(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
        )
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
        input_text=EXAMPLE_GRC, print_raw_response=True
    )
    input("Press Enter to print final Doc ...")
    logger.info(f"GRC_DOC words: {GRC_DOC.words}")
    input()
    logger.info(f"GRC_DOC chatgpt: {GRC_DOC.chatgpt}")

    # JOB_1_13: str = "י וַיְהִי הַיּוֹם וּבָנָיו וּבְנוֹתָיו אֹכְלִים וְשֹׁתִים יַיִן בְּבֵית אֲחִיהֶם הַבְּכוֹר."
    # LANGUAGE: str = "hbo"
    # CHATGPT_HBO: ChatGPT = ChatGPT(language=LANGUAGE, api_key=OPENAI_API_KEY, model=MODEL)
    # JOB_DOC: Doc = CHATGPT_HBO.generate(input_text=JOB_1_13)
    # print(JOB_DOC)
