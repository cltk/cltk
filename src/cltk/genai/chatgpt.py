"""Call ChatGPT."""

import os
import re
import sys
import unicodedata
from copy import deepcopy
from typing import Optional

from openai import OpenAI, OpenAIError
from openai.types.responses.response import Response
from openai.types.responses.response_usage import ResponseUsage

from cltk.alphabet.grc.grc import split_ancient_greek_sentences
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

    def generate_all(
        self,
        input_doc: Doc,
    ) -> Doc:
        """
        Generate POS/morphological analysis, dependency parse, and enrich Doc with metadata (sentence segmentation, translation, summary, topic, discourse relations, coreferences).
        Returns a CLTK Doc with all information populated.
        """
        if not input_doc.raw and not input_doc.normalized_text:
            logger.warning(
                "Input document must have either `.normalized_text` or `raw` text."
            )
        if not input_doc.normalized_text:
            logger.info("Normalizing input_doc.raw to input_doc.normalized_text.")
            input_doc.normalized_text = cltk_normalize(input_doc.raw)
        # Get sentence indices if not set already
        if not input_doc.sentence_boundaries:
            input_doc.sentence_boundaries = split_ancient_greek_sentences(
                text=input_doc.normalized_text
            )
            logger.info(f"Found {len(input_doc.sentence_boundaries)} sentences.")

        # POS/morphology
        tmp_docs: list[Doc] = list()
        for sent_idx, sentence_boundary in enumerate(input_doc.sentence_boundaries):
            tmp_doc = deepcopy(input_doc)
            tmp_doc = self.generate_pos(
                input_doc=tmp_doc,
                sentence_idx=sent_idx,
            )
            tmp_docs.append(tmp_doc)
            logger.debug(f"`input_doc` after ChatGPT POS tagging:\n{input_doc}")
            print(tmp_doc)
        # Combine all Word objects from tmp_docs into a single list
        all_words: list[Word] = list()
        token_counter: int = 0
        for doc in tmp_docs:
            for word in doc.words:
                word.index_token = token_counter
                all_words.append(word)
                token_counter += 1
        logger.debug(
            f"Combined {len(all_words)} words from all tmp_docs and updated token indices."
        )
        # Assign to your main Doc
        input_doc.words = all_words
        logger.debug(f"Doc after POS tagging:\n{input_doc}")
        sys.exit(1)

        # Dependency
        dep_doc, dep_tokens_used = self._call_with_usage(
            self.generate_dependency,
            doc=pos_doc,
            prompt_template=dep_prompt_template,
            print_raw_response=print_raw_response,
        )
        # Metadata
        metadata, metadata_tokens_used = self._call_with_usage(
            self.generate_doc_metadata,
            input_text=input_doc.normalized_text,
            print_raw_response=print_raw_response,
        )
        dep_doc.sentence_boundaries = metadata.get("sentence_boundaries", [])
        dep_doc.translation = metadata.get("translation", None)
        dep_doc.summary = metadata.get("summary", None)
        dep_doc.topic = metadata.get("topic", None)
        # Discourse relations
        discourse, discourse_tokens_used = self._call_with_usage(
            self.generate_discourse_relations,
            input_text=input_doc.normalized_text,
            print_raw_response=print_raw_response,
        )
        dep_doc.discourse_relations = discourse
        # Coreference resolution
        coref, coref_tokens_used = self._call_with_usage(
            self.generate_coreferences,
            input_text=input_doc.normalized_text,
            print_raw_response=print_raw_response,
        )
        dep_doc.coreferences = coref
        # Aggregate token usage
        tokens_per_call = {
            "pos": pos_tokens_used,
            "dep": dep_tokens_used,
            "metadata": metadata_tokens_used,
            "discourse": discourse_tokens_used,
            "coref": coref_tokens_used,
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

    def generate_pos(
        self,
        input_doc: Doc,
        sentence_idx: Optional[int] = None,
    ) -> Doc:
        """Call the OpenAI API and return the response text, including lemma, gloss, NER, inflectional paradigm, and IPA pronunciation."""
        prompt = f"""For the following {self.language.name} text, tokenize the text and return one line per token. For each token, provide the FORM, LEMMA, UPOS, and FEATS fields according to Universal Dependencies guidelines.

Return the result as a markdown code block containing a tab-delimited table (TSV format) with the following columns:

FORM\tLEMMA\tUPOS\tFEATS

Do not include any explanation, commentary, or extra formatting. Only output the table inside a markdown code block.

Text: {input_doc.normalized_text}
"""
        try:
            chatgpt_response: Response = self.client.responses.create(
                model=self.model, input=prompt, temperature=self.temperature
            )
        except OpenAIError as openai_error:
            raise OpenAIInferenceError(f"An error from OpenAI occurred: {openai_error}")
        logger.debug(f"Raw response from OpenAI: {chatgpt_response.output_text}")
        chatgpt_usage: dict[str, int] = self.chatgpt_response_tokens(
            response=chatgpt_response
        )
        logger.info(f"ChatGPT usage: {chatgpt_usage}")
        if not input_doc.chatgpt:
            input_doc.chatgpt = list()
        input_doc.chatgpt.append(chatgpt_usage)
        if not input_doc.normalized_text:
            raise CLTKException("Input document must have `.normalized_text` set.")
        if not chatgpt_response.output_text:
            raise CLTKException(
                "No output text returned from OpenAI. Check your prompt and API key."
            )
        raw_chatgpt_response_normalized: str = cltk_normalize(
            text=chatgpt_response.output_text
        )

        def extract_code_blocks(text):
            # This regex finds all text between triple backticks
            return re.findall(r"```(?:[a-zA-Z]*\n)?(.*?)```", text, re.DOTALL)

        code_blocks = extract_code_blocks(raw_chatgpt_response_normalized)
        if not code_blocks:
            logger.warning("No code blocks found in ChatGPT response.")
            raise CLTKException("No code blocks found in ChatGPT response.")
        code_block: str = code_blocks[0].strip()
        logger.debug(f"Extracted code block:\n{code_block}")

        def parse_tsv_table(tsv_string: str) -> list[dict[str, str]]:
            lines: list[str] = [
                line.strip() for line in tsv_string.strip().splitlines() if line.strip()
            ]
            header: list[str] | None = None
            data: list[dict[str, str]] = []
            for line in lines:
                if header is None:
                    header = [col.strip().lower() for col in line.split("\t")]
                    continue
                parts = line.split("\t")
                if len(parts) == 4:
                    entry: dict[str, str] = dict(zip(header, parts))
                    data.append(entry)
            return data

        parsed_pos_tags: list[dict[str, str]] = parse_tsv_table(code_block)
        logger.debug(f"Parsed POS tags:\n{parsed_pos_tags}")
        cleaned_pos_tags: list[dict[str, Optional[str]]] = [
            {k: (None if v == "_" else v) for k, v in d.items()}
            for d in parsed_pos_tags
        ]
        logger.debug(f"Cleaned POS tags:\n{cleaned_pos_tags}")
        # Create Word objects from cleaned POS tags
        words: list[Word] = list()
        for word_idx, pos_dict in enumerate(cleaned_pos_tags):
            word: Word = Word(
                string=pos_dict.get("form", None),
                index_token=word_idx,
                lemma=pos_dict.get("lemma", None),
                upos=pos_dict.get("upos", None),
            )
            # Add morphology features to each Word object
            feats_raw: Optional[str] = pos_dict.get("feats", None)
            features_bundle: Optional[MorphosyntacticFeatureBundle] = None
            if not feats_raw:
                features_bundle = None
            else:
                features_bundle = MorphosyntacticFeatureBundle()
                feats: list[str] = feats_raw.split("|")
                for feat in feats:
                    if "=" in feat:
                        key, value = feat.split("=", 1)
                        if key in FORM_UD_MAP:
                            values = self._normalize_feature_value(key, value)
                            for val in values:
                                feature_instance = from_ud(key, val)
                                if feature_instance:
                                    features_bundle[type(feature_instance)] = [
                                        feature_instance
                                    ]
                                else:
                                    # Handle unknown feature keys
                                    logger.warning(
                                        f"Unknown feature key: {key} for '{word.string}'. Please check the input text and try again."
                                    )
                                    # input()
                        else:
                            # Handle unknown feature keys
                            logger.warning(
                                f"Unknown feature key: {key} for '{word.string}'"
                            )
                            # input()
                word.features = features_bundle
            words.append(word)
        logger.debug(f"Created {len(words)} Word objects from POS tags.")
        logger.debug("Words: %s", ", ".join([word.string or "" for word in words]))
        if not input_doc.words:
            logger.debug("`input_doc.words` is empty. Setting with new words.")
            input_doc.words = words
        else:
            # TODO: Handle case where input_doc.words already has data
            logger.warning("`input_doc.words` already has data. Not overwriting.")
            raise CLTKException(
                "`input_doc.words` already has data. Not overwriting. "
                "Consider clearing it first if you want to replace."
            )

        # Get start/stop indexes for each word in the input text
        start = 0
        for word_idx, word in enumerate(input_doc.words):
            if not word.string:
                word.index_char_start = None
                word.index_char_stop = None
                input_doc.words[word_idx] = word
                continue
            char_idx = input_doc.normalized_text.find(word.string, start)
            if char_idx != -1:
                word.index_char_start = char_idx
                word.index_char_stop = char_idx + len(word.string)
                start = word.index_char_stop  # move past this word for next search
            else:
                word.index_char_start = None
                word.index_char_stop = None
            input_doc.words[word_idx] = word
        logger.debug("Set character indexes for each word in input_doc.words.")

        # Add sentence idx to Word objects
        if sentence_idx is not None:
            for word in input_doc.words:
                word.index_sentence = sentence_idx
            logger.debug(
                f"Set sentence index {sentence_idx} for all words in input_doc.words."
            )
        else:
            logger.warning(
                "No sentence index provided. Skipping sentence index assignment."
            )
        return input_doc

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
            # TODO: Update this after change to Doc.language to type `Language``
            prompt = f"""Given the following '{doc.language}' text and its Universal Dependencies POS and morphological tags, return the syntactic dependency parse for each word in UD format (index, word, head index, relation, and all UD features):\n\n{token_table}\n\nReturn each word on its own line, with columns: index, word, head index, relation, and all UD features. Do not return a parse tree, only line-by-line explanations."""
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

    # def _call_with_usage(self, func, *args, **kwargs):
    #     """Helper to call a function and extract token usage from its response object or internal usage attributes.
    #     Returns (result, tokens_total) where result is the main output and tokens_total is an int or None.
    #     """
    #     if func == self.generate_pos:
    #         doc = func(*args, **kwargs)
    #         usage = (
    #             doc.chatgpt.get("tokens_total")
    #             if hasattr(doc, "chatgpt") and doc.chatgpt
    #             else None
    #         )
    #         return doc, usage
    #     elif func == self.generate_dependency:
    #         doc = func(*args, **kwargs)
    #         usage = (
    #             doc.chatgpt.get("tokens_total")
    #             if hasattr(doc, "chatgpt") and doc.chatgpt
    #             else None
    #         )
    #         return doc, usage
    #     elif func == self.generate_doc_metadata:
    #         result = func(*args, **kwargs)
    #         usage = getattr(self, "_last_metadata_usage", None)
    #         return result, usage
    #     elif func == self.generate_discourse_relations:
    #         result = func(*args, **kwargs)
    #         usage = getattr(self, "_last_discourse_usage", None)
    #         return result, usage
    #     elif func == self.generate_coreferences:
    #         result = func(*args, **kwargs)
    #         usage = getattr(self, "_last_coref_usage", None)
    #         return result, usage
    #     else:
    #         result = func(*args, **kwargs)
    #         usage = None
    #         if hasattr(result, "chatgpt") and result.chatgpt:
    #             usage = result.chatgpt.get("tokens_total")
    #         return result, usage

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

    def parse_tsv_table(self, response: str) -> list[dict[str, str]]:
        """Parse a TSV table with columns FORM, LEMMA, UPOS, FEATS into a list of dicts."""
        lines = [line.strip() for line in response.splitlines() if line.strip()]
        data: list[dict[str, str]] = []
        header = None
        for line in lines:
            # Skip markdown code block markers
            if line.startswith("```"):
                continue
            # Find header
            if header is None:
                if all(
                    col in line.upper() for col in ("FORM", "LEMMA", "UPOS", "FEATS")
                ):
                    header = [col.strip().lower() for col in line.split("\t")]
                    continue
            # Parse data rows
            if header is not None:
                parts = line.split("\t")
                if len(parts) != 4:
                    continue  # skip malformed lines
                entry = dict(zip(header, parts))
                data.append(entry)
        if not data:
            raise CLTKException(
                f"No valid TSV word info found in response:\n{response}"
            )
        return data

    def chatgpt_response_tokens(self, response: Response) -> dict[str, int]:
        """Extract token usage information from an OpenAI Response object."""
        usage = getattr(response, "usage", None)
        tokens: dict[str, int] = {"input": 0, "output": 0, "total": 0}
        if not usage:
            logger.warning(
                "No usage information found in response. Tokens used may not be available."
            )
            return tokens
        tokens["input"] = int(getattr(usage, "input_tokens", 0))
        tokens["output"] = int(getattr(usage, "output_tokens", 0))
        tokens["total"] = int(getattr(usage, "total_tokens", 0))
        if tokens["total"] == 0:
            logger.warning(
                "No tokens used reported in response. This may indicate an issue with the API call."
            )
        return tokens


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
    EX_DOC: Doc = Doc(
        raw=EXAMPLE_GRC, language="grc", normalized_text=cltk_normalize(EXAMPLE_GRC)
    )
    GRC_DOC: Doc = CHATGPT_GRC.generate_all(input_doc=EX_DOC, print_raw_response=True)
    input("Press Enter to print final Doc ...")
    logger.info(f"GRC_DOC words: {GRC_DOC.words}")
    logger.info(f"GRC_DOC chatgpt: {GRC_DOC.chatgpt}")

    # JOB_1_13: str = "י וַיְהִי הַיּוֹם וּבָנָיו וּבְנוֹתָיו אֹכְלִים וְשֹׁתִים יַיִן בְּבֵית אֲחִיהֶם הַבְּכוֹר."
    # LANGUAGE: str = "hbo"
    # CHATGPT_HBO: ChatGPT = ChatGPT(language=LANGUAGE, api_key=OPENAI_API_KEY, model=MODEL)
    # JOB_DOC: Doc = CHATGPT_HBO.generate(input_text=JOB_1_13)
    # print(JOB_DOC)
