from typing import Optional, get_args

from colorama import Fore, Style
from pydantic_core._pydantic_core import ValidationError as PydanticValidationError
from tqdm import tqdm

from cltk.core.cltk_logger import logger
from cltk.core.data_types import (
    AVAILABLE_OPENAI_MODELS,
    CLTKGenAIResponse,
    Doc,
    Word,
)
from cltk.core.exceptions import CLTKException
from cltk.genai.chatgpt import ChatGPTConnection
from cltk.morphosyntax.ud_features import UDFeatureTagSet, convert_pos_features_to_ud
from cltk.morphosyntax.ud_pos import UDPartOfSpeechTag


def _parse_tsv_table(tsv_string: str) -> list[dict[str, str]]:
    # TODO: Remove duplicate name -- this is the one being invoked, I think
    lines = [line.strip() for line in tsv_string.strip().splitlines() if line.strip()]
    header = ["form", "lemma", "upos", "feats"]
    data = []
    for line in lines:
        # Skip markdown code block markers
        if line.startswith("```"):
            continue
        parts = line.split("\t")
        if len(parts) == 4:
            # Skip the header row if present
            if [p.lower() for p in parts] == header:
                continue
            entry = dict(zip(header, parts))
            data.append(entry)
        else:
            logger.debug(f"Skipping malformed line: {line}")
    return data


def generate_pos(
    doc: Doc,
    sentence_idx: Optional[int] = None,
    max_retries: int = 2,
    client: Optional[ChatGPTConnection] = None,
) -> Doc:
    """Call OpenAI and return UD token annotations for a short span.

    Args:
        doc: A document whose ``normalized_text`` contains a single sentence
        (or short span) to analyze.
        sentence_idx: Optional sentence index for logging/aggregation.
        max_retries: Number of attempts if the model fails to return a TSV
        code block.
        client: Optional ChatGPT connection instance for making API calls.

    Returns:
        The same ``Doc`` instance with ``words`` and per‑call usage appended
        to ``doc.chatgpt``.

    Raises:
        OpenAIInferenceError: If the API call fails.
        CLTKException: If the response is empty or cannot be parsed.
        ValueError: If an unsupported model alias is specified.

    """
    if not doc.normalized_text:
        raise CLTKException("Input document must have `.normalized_text` set.")
    if doc.dialect:
        lang_or_dialect_name: str = doc.dialect.name
    else:
        lang_or_dialect_name = doc.language.name
    # if self.language.selected_dialect_name:
    #     lang_or_dialect_name = self.language.selected_dialect_name
    # else:
    #     lang_or_dialect_name = self.language.name
    prompt: str = f"""For the following {lang_or_dialect_name} text, tokenize the text and return one line per token. For each token, provide the FORM, LEMMA, UPOS, and FEATS fields following Universal Dependencies (UD) guidelines.

Rules:
- Always use strict UD morphological tags (not a simplified system).
- Split off enclitics and contractions as separate tokens.
- Always include punctuation as separate tokens with UPOS=PUNCT and FEATS=_.
- For uncertain, rare, or dialectal forms, always provide the most standard dictionary lemma and supply a best-effort UD tag. Do not skip any tokens.
- Separate UD features with a pipe ("|"). Do not use a semi-colon or other characters.
- Preserve the spelling of the text exactly as given (including diacritics, breathings, and subscripts). Do not normalize.
- If a lemma or feature is uncertain, still provide the closest standard form and UD features. Never leave fields blank and never ask for clarification.
- If full accuracy is not possible, always provide a best-effort output without asking for clarification.
- Never request to perform the task in multiple stages; always deliver the final TSV in one step.
- Do not ask for confirmation, do not explain your reasoning, and do not include any commentary. Output only the TSV table.
- Always output all four fields: FORM, LEMMA, UPOS, FEATS.
- The result **must be a markdown code block** (beginning and ending in "```") containing only a tab-delimited table (TSV) with the following header row:

FORM    LEMMA   UPOS    FEATS

Text:\n\n{doc.normalized_text}
"""
    logger.debug(prompt)
    # code_blocks: list[Any] = []
    if not doc.backend:
        msg_no_backend: str = (
            "Doc must have `.backend` set to 'chatgpt' to use generate_pos."
        )
        logger.error(msg_no_backend)
        raise CLTKException(msg_no_backend)
    if not doc.backend_version:
        msg_no_backend_version: str = (
            "Doc missing `.backend_version`. Setting to 'gpt-5.0' to use generate_pos."
        )
        logger.info(msg_no_backend_version)
        raise CLTKException(msg_no_backend_version)
    if doc.backend_version not in get_args(AVAILABLE_OPENAI_MODELS):
        msg_unsupported_backend_version: str = f"Doc has unsupported `.backend_version`: {doc.backend_version}. Supported versions are: {get_args(AVAILABLE_OPENAI_MODELS)}."
        logger.error(msg_unsupported_backend_version)
        raise CLTKException(msg_unsupported_backend_version)
    if not client:
        client = ChatGPTConnection(model=doc.backend_version)
    chatgpt_res_obj: CLTKGenAIResponse = client.generate(
        prompt=prompt, max_retries=max_retries
    )
    chatgpt_res: str = chatgpt_res_obj.response
    chatgpt_usage: dict[str, int] = chatgpt_res_obj.usage
    if not doc.chatgpt:
        doc.chatgpt = list()
    doc.chatgpt.append(chatgpt_usage)

    parsed_pos_tags: list[dict[str, str]] = _parse_tsv_table(chatgpt_res)
    logger.debug(f"Parsed POS tags:\n{parsed_pos_tags}")
    cleaned_pos_tags: list[dict[str, Optional[str]]] = [
        {k: (None if v == "_" else v) for k, v in d.items()} for d in parsed_pos_tags
    ]
    logger.debug(f"Cleaned POS tags:\n{cleaned_pos_tags}")
    # Create Word objects from cleaned POS tags
    words: list[Word] = list()
    for word_idx, pos_dict in enumerate(cleaned_pos_tags):
        upos_val_raw: Optional[str] = pos_dict.get("upos", None)
        udpos: Optional[UDPartOfSpeechTag] = None
        if upos_val_raw:
            # TODO: Do check if tag is valid or try to correct if this raises error
            try:
                udpos = UDPartOfSpeechTag(tag=upos_val_raw)
            except PydanticValidationError as e:
                logger.error(
                    f"{pos_dict['form']}: Invalid 'upos' field in POS dict: {pos_dict}, `upos_val_raw`='{upos_val_raw}'. Error: {e}"
                )
        else:
            logger.error(f"Missing 'upos' field in POS dict: {pos_dict}.")
            logger.error(f"`code_block` from LLM: {chatgpt_res}")
        word: Word = Word(
            string=pos_dict.get("form", None),
            index_token=word_idx,
            lemma=pos_dict.get("lemma", None),
            upos=udpos,
        )
        # Add morphology features to each Word object
        feats_raw: Optional[str] = pos_dict.get("feats", None)
        logger.debug(f"feats_raw: {feats_raw}")
        if not feats_raw:
            words.append(word)
            logger.debug(
                f"No features found for {word.string}, skipping feature assignment."
            )
            continue
        features_tag_set: Optional[UDFeatureTagSet] = None
        try:
            features_tag_set = convert_pos_features_to_ud(feats_raw=feats_raw)
        except ValueError as e:
            msg: str = f"{word.string}: Failed to create features_tag_set from '{feats_raw}' for '{word.string}': {e}"
            logger.error(msg)
            with open("features_err.log", "a") as f:
                f.write(msg + "\n")
            word.features = features_tag_set
            # TODO: Re-raise this error
            # raise ValueError(msg)
        logger.debug(f"features_tag_set for {word.string}: {features_tag_set}")
        word.features = features_tag_set
        words.append(word)
    logger.debug(f"Created {len(words)} Word objects from POS tags.")
    logger.debug("Words: %s", ", ".join([word.string or "" for word in words]))
    if not doc.words:
        logger.debug("`input_doc.words` is empty. Setting with new words.")
        doc.words = words
    else:
        # TODO: Handle case where input_doc.words already has data
        logger.warning("`input_doc.words` already has data. Not overwriting.")
        raise CLTKException(
            "`input_doc.words` already has data. Not overwriting. "
            "Consider clearing it first if you want to replace."
        )

    # Get start/stop indexes for each word in the input text
    assert doc.normalized_text
    start = 0
    for word_idx, word in enumerate(doc.words):
        if not word.string:
            word.index_char_start = None
            word.index_char_stop = None
            doc.words[word_idx] = word
            continue
        char_idx = doc.normalized_text.find(word.string, start)
        if char_idx != -1:
            word.index_char_start = char_idx
            word.index_char_stop = char_idx + len(word.string)
            start = word.index_char_stop  # move past this word for next search
        else:
            word.index_char_start = None
            word.index_char_stop = None
        doc.words[word_idx] = word
    logger.debug("Set character indexes for each word in input_doc.words.")

    # Add sentence idx to Word objects
    if sentence_idx is not None:
        for word in doc.words:
            word.index_sentence = sentence_idx
        logger.debug(
            f"Set sentence index {sentence_idx} for all words in input_doc.words."
        )
    else:
        logger.warning(
            "No sentence index provided. Skipping sentence index assignment."
        )
    return doc


def generate_gpt_morphosyntax(doc: Doc) -> Doc:
    if not doc.backend_version:
        msg: str = "Document backend version is not set."
        logger.error(msg)
        raise ValueError(msg)
    client: ChatGPTConnection = ChatGPTConnection(model=doc.backend_version)
    if not doc.normalized_text:
        msg = "Input document must have either `.normalized_text`."
        logger.error(msg)
        raise ValueError(msg)
    # POS/morphology
    tmp_docs: list[Doc] = list()
    for sent_idx, sentence_string in tqdm(
        enumerate(doc.sentence_strings),
        total=len(doc.sentence_strings),
        desc=Fore.GREEN
        + "Processing sentences with ChatGPT for UD features"
        + Style.RESET_ALL,
        unit="sentence",
    ):
        tmp_doc = Doc(
            language=doc.language,
            normalized_text=sentence_string,
            backend=doc.backend,
            backend_version=doc.backend_version,
        )
        tmp_doc = generate_pos(
            doc=tmp_doc,
            sentence_idx=sent_idx,
            client=client,
        )
        tmp_docs.append(tmp_doc)
        logger.info(
            f"Completed POS tagging to sentence #{sent_idx + 1} of {len(doc.sentence_strings)}"
        )
    # Combine all Word objects from tmp_docs into a single list
    all_words: list[Word] = list()
    token_counter: int = 0
    for doc in tmp_docs:
        for word in doc.words:
            word.index_token = token_counter
            all_words.append(word)
            token_counter += 1
    # Concat ChatGPT token counts
    # Aggregate ChatGPT token counts across all tmp_docs
    chatgpt_total_tokens = {"input": 0, "output": 0, "total": 0}
    for doc in tmp_docs:
        if doc.chatgpt and isinstance(doc.chatgpt[0], dict):
            for k in chatgpt_total_tokens:
                chatgpt_total_tokens[k] += doc.chatgpt[0].get(k, 0)
        else:
            msg_bad_tokens: str = (
                "Failed to get ChatGPT tokens usage field from POS tagging."
            )
            logger.error(msg_bad_tokens)
            raise CLTKException(msg_bad_tokens)
    doc.chatgpt = [chatgpt_total_tokens]
    logger.debug(
        f"Combined {len(all_words)} words from all tmp_docs and updated token indices."
    )
    # Assign to your main Doc
    doc.words = all_words
    logger.debug(f"Doc after POS tagging:\n{doc}")
    assert doc.normalized_text
    logger.debug(
        f"Completed processing POS for text starting with {doc.normalized_text[:50]} ..."
    )
    return doc
