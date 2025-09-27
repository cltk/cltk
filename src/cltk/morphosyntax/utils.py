"""Morphosyntax utilities used by CLTK pipelines.

# Internal; no stability guarantees
"""

import asyncio
import concurrent.futures
import hashlib
from typing import Any, Optional, cast, get_args

from colorama import Fore, Style
from pydantic import ValidationError as PydanticValidationError
from tqdm import tqdm

from cltk.core.cltk_logger import bind_context, logger
from cltk.core.data_types import (
    AVAILABLE_OPENAI_MODELS,
    CLTKGenAIResponse,
    Doc,
    Word,
)
from cltk.core.exceptions import CLTKException
from cltk.core.logging_utils import bind_from_doc
from cltk.genai.ollama import AsyncOllamaConnection, OllamaConnection
from cltk.genai.openai import AsyncOpenAIConnection, OpenAIConnection
from cltk.genai.prompts import morphosyntax_prompt
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
    client: Optional[Any] = None,
) -> Doc:
    """Call the configured generative backend and return UD token annotations for a short span.

    Args:
        doc: A document whose ``normalized_text`` contains a single sentence (or short span) to analyze.
        sentence_idx: Optional sentence index for logging/aggregation.
        max_retries: Number of attempts if the model fails to return a TSV code block.
        client: Optional connection instance (OpenAI or Ollama) for making API calls.

    Returns:
        The same ``Doc`` instance with ``words`` and per‑call usage appended
        to ``doc.openai``.

    Raises:
        OpenAIInferenceError: If the OpenAI API call fails (when using the OpenAI backend).
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
    pinfo = morphosyntax_prompt(lang_or_dialect_name, doc.normalized_text)
    prompt = pinfo.text
    # Structured logging context
    try:
        glottolog_id: Optional[str]
        if doc.dialect and doc.dialect.glottolog_id:
            glottolog_id = doc.dialect.glottolog_id
        else:
            glottolog_id = doc.language.glottolog_id
    except Exception:
        glottolog_id = None
    try:
        doc_hash = (
            hashlib.sha1(
                doc.normalized_text.encode("utf-8"), usedforsecurity=False
            ).hexdigest()[:10]
            if doc.normalized_text
            else None
        )
    except Exception:
        doc_hash = None
    log = bind_context(
        doc_id=doc_hash,
        sentence_idx=sentence_idx,
        model=str(doc.model) if doc.model else None,
        glottolog_id=glottolog_id,
        prompt_version=str(pinfo.version),
    )
    log.info("[prompt] %s v%s hash=%s", pinfo.kind, pinfo.version, pinfo.digest)
    import os as _os

    if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {"1", "true", "yes", "on"}:
        log.debug(prompt)
    # code_blocks: list[Any] = []
    if not doc.backend:
        msg_no_backend: str = "Doc must have `.backend` set to 'openai', 'ollama', or 'ollama-cloud' to use generate_pos."
        log.error(msg_no_backend)
        raise CLTKException(msg_no_backend)
    if not doc.model:
        msg_no_backend_version: str = (
            "Doc missing `.model`. Set to a supported model to use generate_pos."
        )
        log.info(msg_no_backend_version)
        raise CLTKException(msg_no_backend_version)
    if doc.backend == "openai":
        if doc.model not in get_args(AVAILABLE_OPENAI_MODELS):
            msg_unsupported_backend_version: str = (
                f"Doc has unsupported `.model`: {doc.model}. "
                f"Supported versions are: {get_args(AVAILABLE_OPENAI_MODELS)}."
            )
            log.error(msg_unsupported_backend_version)
            raise CLTKException(msg_unsupported_backend_version)
        if not client:
            openai_model: AVAILABLE_OPENAI_MODELS = cast(
                AVAILABLE_OPENAI_MODELS, doc.model
            )
            client = OpenAIConnection(model=openai_model)
    elif doc.backend in ("ollama", "ollama-cloud"):
        if not client:
            client = OllamaConnection(
                model=str(doc.model),
                use_cloud=doc.backend == "ollama-cloud",
            )
    else:
        raise CLTKException(
            f"Unsupported backend for generate_pos: {doc.backend}. Use 'openai', 'ollama', or 'ollama-cloud'."
        )
    openai_res_obj: CLTKGenAIResponse = client.generate(
        prompt=prompt, max_retries=max_retries
    )
    openai_res: str = openai_res_obj.response
    openai_usage: dict[str, int] = openai_res_obj.usage
    if not doc.openai:
        doc.openai = list()
    doc.openai.append(openai_usage)

    parsed_pos_tags: list[dict[str, str]] = _parse_tsv_table(openai_res)
    if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {"1", "true", "yes", "on"}:
        log.debug(f"Parsed POS tags:\n{parsed_pos_tags}")
    cleaned_pos_tags: list[dict[str, Optional[str]]] = [
        {k: (None if v == "_" else v) for k, v in d.items()} for d in parsed_pos_tags
    ]
    if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {"1", "true", "yes", "on"}:
        log.debug(f"Cleaned POS tags:\n{cleaned_pos_tags}")
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
                log.error(
                    f"{pos_dict['form']}: Invalid 'upos' field in POS dict: {pos_dict}, `upos_val_raw`='{upos_val_raw}'. Error: {e}"
                )
        else:
            log.error(f"Missing 'upos' field in POS dict: {pos_dict}.")
            log.error(f"`code_block` from LLM: {openai_res}")
        word: Word = Word(
            string=pos_dict.get("form", None),
            index_token=word_idx,
            lemma=pos_dict.get("lemma", None),
            upos=udpos,
        )
        # Add morphology features to each Word object
        feats_raw: Optional[str] = pos_dict.get("feats", None)
        log.debug(f"feats_raw: {feats_raw}")
        if not feats_raw:
            words.append(word)
            log.debug(
                f"No features found for {word.string}, skipping feature assignment."
            )
            continue
        features_tag_set: Optional[UDFeatureTagSet] = None
        try:
            features_tag_set = convert_pos_features_to_ud(feats_raw=feats_raw)
        except ValueError as e:
            msg: str = f"{word.string}: Failed to create features_tag_set from '{feats_raw}' for '{word.string}': {e}"
            log.error(msg)
            # Only write to disk if explicitly enabled for both file logging and content
            if _os.getenv("CLTK_LOG_TO_FILE", "").strip().lower() in {
                "1",
                "true",
                "yes",
                "on",
            } and _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
                "1",
                "true",
                "yes",
                "on",
            }:
                try:
                    with open("features_err.log", "a", encoding="utf-8") as f:
                        f.write(msg + "\n")
                except Exception:
                    # Never fail the pipeline due to logging to disk
                    pass
            word.features = features_tag_set
            # TODO: Re-raise this error
            # raise ValueError(msg)
        if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            log.debug(f"features_tag_set for {word.string}: {features_tag_set}")
        word.features = features_tag_set
        words.append(word)
    log.debug(f"Created {len(words)} Word objects from POS tags.")
    if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {"1", "true", "yes", "on"}:
        log.debug("Words: %s", ", ".join([word.string or "" for word in words]))
    if not doc.words:
        log.debug("`input_doc.words` is empty. Setting with new words.")
        doc.words = words
    else:
        # TODO: Handle case where input_doc.words already has data
        log.warning("`input_doc.words` already has data. Not overwriting.")
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
    log.debug("Set character indexes for each word in input_doc.words.")

    # Add sentence idx to Word objects
    if sentence_idx is not None:
        for word in doc.words:
            word.index_sentence = sentence_idx
        log.debug(
            f"Set sentence index {sentence_idx} for all words in input_doc.words."
        )
    else:
        log.warning("No sentence index provided. Skipping sentence index assignment.")
    return doc


def generate_gpt_morphosyntax(doc: Doc) -> Doc:
    log = bind_from_doc(doc)
    if not doc.model:
        msg: str = "Document model is not set."
        log.error(msg)
        raise ValueError(msg)
    client: Any
    if doc.backend == "openai":
        if doc.model not in get_args(AVAILABLE_OPENAI_MODELS):
            raise CLTKException(
                f"Doc has unsupported `.model`: {doc.model}. Supported: {get_args(AVAILABLE_OPENAI_MODELS)}."
            )
        openai_model: AVAILABLE_OPENAI_MODELS = cast(AVAILABLE_OPENAI_MODELS, doc.model)
        client = OpenAIConnection(model=openai_model)
    elif doc.backend in ("ollama", "ollama-cloud"):
        client = OllamaConnection(
            model=str(doc.model),
            use_cloud=doc.backend == "ollama-cloud",
        )
    else:
        raise CLTKException(
            f"Unsupported backend for morphosyntax: {doc.backend}. Use 'openai', 'ollama', or 'ollama-cloud'."
        )
    if not doc.normalized_text:
        msg = "Input document must have either `.normalized_text`."
        log.error(msg)
        raise ValueError(msg)
    # POS/morphology
    tmp_docs: list[Doc] = list()
    for sent_idx, sentence_string in tqdm(
        enumerate(doc.sentence_strings),
        total=len(doc.sentence_strings),
        desc=Fore.GREEN
        + "Processing sentences with LLM for UD features"
        + Style.RESET_ALL,
        unit="sentence",
    ):
        tmp_doc = Doc(
            language=doc.language,
            normalized_text=sentence_string,
            backend=doc.backend,
            model=doc.model,
        )
        tmp_doc = generate_pos(
            doc=tmp_doc,
            sentence_idx=sent_idx,
            client=client,
        )
        tmp_docs.append(tmp_doc)
        bind_from_doc(doc, sentence_idx=sent_idx).info(
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
    # Aggregate token counts across all tmp_docs
    openai_total_tokens = {"input": 0, "output": 0, "total": 0}
    for doc in tmp_docs:
        if doc.openai and isinstance(doc.openai[0], dict):
            for k in openai_total_tokens:
                openai_total_tokens[k] += doc.openai[0].get(k, 0)
        else:
            msg_bad_tokens: str = "Failed to get token usage field from POS tagging."
            log.error(msg_bad_tokens)
            raise CLTKException(msg_bad_tokens)
    _update_doc_openai_stage(doc, stage="pos", stage_tokens=openai_total_tokens)
    log.debug(
        f"Combined {len(all_words)} words from all tmp_docs and updated token indices."
    )
    # Assign to your main Doc
    doc.words = all_words
    log.debug(f"Doc after POS tagging:\n{doc}")
    assert doc.normalized_text
    log.debug(
        f"Completed processing POS for text starting with {doc.normalized_text[:50]} ..."
    )
    return doc


async def generate_gpt_morphosyntax_async(
    doc: Doc,
    *,
    max_concurrency: int = 4,
    max_retries: int = 2,
) -> Doc:
    """Async variant of ``generate_gpt_morphosyntax`` with concurrency.

    Runs one request per sentence concurrently (bounded by ``max_concurrency``)
    using the appropriate async client for the selected backend
    (:class:`AsyncOpenAIConnection` or :class:`AsyncOllamaConnection`). Keeps the
    one‑sentence‑per‑request contract for simpler parsing and error isolation
    while reducing wall‑clock time for long documents.

    Args:
        doc: Document whose ``sentence_strings`` will be annotated.
        max_concurrency: Maximum number of in‑flight LLM requests.
        max_retries: Per‑request retry budget.

    Returns:
        The input ``doc`` enriched with ``words`` and aggregated generative
        usage across all sentence calls (stored in ``doc.openai``).

    Raises:
        ValueError: If backend configuration is missing.
        CLTKException: If per‑sentence parsing fails in unexpected ways.

    """
    log = bind_from_doc(doc)
    log.info(
        "[async] Starting morphosyntax generation for %s sentences",
        len(doc.sentence_strings),
    )
    if not doc.model:
        msg = "Document model is not set."
        log.error(msg)
        raise ValueError(msg)
    if not doc.normalized_text:
        msg = "Input document must have `.normalized_text`."
        log.error(msg)
        raise ValueError(msg)

    if doc.backend == "openai":
        if doc.model not in get_args(AVAILABLE_OPENAI_MODELS):
            raise CLTKException(
                f"Doc has unsupported `.model`: {doc.model}. Supported: {get_args(AVAILABLE_OPENAI_MODELS)}."
            )
        openai_model: AVAILABLE_OPENAI_MODELS = cast(AVAILABLE_OPENAI_MODELS, doc.model)
        conn: Any = AsyncOpenAIConnection(model=openai_model)
    elif doc.backend in ("ollama", "ollama-cloud"):
        conn = AsyncOllamaConnection(
            model=str(doc.model),
            use_cloud=doc.backend == "ollama-cloud",
        )
    else:
        raise CLTKException(
            f"Unsupported backend for async morphosyntax: {doc.backend}."
        )

    # Prepare prompts per sentence
    lang_or_dialect_name = doc.dialect.name if doc.dialect else doc.language.name

    def build_prompt(sentence: str) -> str:
        return (
            f"For the following {lang_or_dialect_name} text, tokenize the text and return one line per token. "
            "For each token, provide the FORM, LEMMA, UPOS, and FEATS fields following Universal Dependencies (UD) guidelines.\n\n"
            "Rules:\n"
            "- Always use strict UD morphological tags (not a simplified system).\n"
            "- Split off enclitics and contractions as separate tokens.\n"
            "- Always include punctuation as separate tokens with UPOS=PUNCT and FEATS=_.\n"
            "- For uncertain, rare, or dialectal forms, always provide the most standard dictionary lemma and supply a best‑effort UD tag. Do not skip any tokens.\n"
            '- Separate UD features with a pipe ("|"). Do not use a semi‑colon or other characters.\n'
            "- Preserve the spelling of the text exactly as given (including diacritics, breathings, and subscripts). Do not normalize.\n"
            "- If a lemma or feature is uncertain, still provide the closest standard form and UD features. Never leave fields blank and never ask for clarification.\n"
            "- If full accuracy is not possible, always provide a best‑effort output without asking for clarification.\n"
            "- Never request to perform the task in multiple stages; always deliver the final TSV in one step.\n"
            "- Do not ask for confirmation, do not explain your reasoning, and do not include any commentary. Output only the TSV table.\n"
            "- Always output all four fields: FORM, LEMMA, UPOS, FEATS.\n"
            '- The result **must be a markdown code block** (beginning and ending in "```") containing only a tab‑delimited table (TSV) with the following header row:\n\n'
            "FORM\tLEMMA\tUPOS\tFEATS\n\n"
            f"Text:\n\n{sentence}\n"
        )

    sem = asyncio.Semaphore(max_concurrency)

    async def process_one(i: int, sentence: str) -> tuple[int, Doc, dict[str, int]]:
        prompt = build_prompt(sentence)
        log_i = bind_from_doc(doc, sentence_idx=i)
        log_i.debug("[async] Scheduling sentence #%s (%d chars)", i, len(sentence))
        async with sem:
            log_i.debug("[async] Dispatching sentence #%s", i)
            res: CLTKGenAIResponse = await conn.generate_async(
                prompt=prompt, max_retries=max_retries
            )
            log_i.debug("[async] Received response for sentence #%s", i)
        tmp = Doc(
            language=doc.language,
            normalized_text=sentence,
            backend=doc.backend,
            model=doc.model,
        )
        # Parse TSV and construct words (reuse sync logic pieces)
        parsed = _parse_tsv_table(res.response)
        cleaned: list[dict[str, Optional[str]]] = [
            {k: (None if v == "_" else v) for k, v in d.items()} for d in parsed
        ]
        words: list[Word] = []
        for word_idx, pos_dict in enumerate(cleaned):
            upos_val = pos_dict.get("upos")
            udpos = None
            if upos_val:
                try:
                    udpos = UDPartOfSpeechTag(tag=upos_val)
                except PydanticValidationError as e:  # pragma: no cover - defensive
                    log_i.error(
                        "[async] %s: Invalid 'upos' in POS dict: %s (error: %s)",
                        pos_dict.get("form"),
                        pos_dict,
                        e,
                    )
            else:
                log_i.error("[async] Missing 'upos' in POS dict: %s", pos_dict)
            word = Word(
                string=pos_dict.get("form"),
                index_token=word_idx,
                lemma=pos_dict.get("lemma"),
                upos=udpos,
            )
            feats_raw = pos_dict.get("feats")
            if feats_raw:
                try:
                    word.features = convert_pos_features_to_ud(feats_raw=feats_raw)
                except ValueError as e:  # pragma: no cover - defensive
                    log_i.error(
                        "[async] %s: Failed to parse features '%s': %s",
                        word.string,
                        feats_raw,
                        e,
                    )
            words.append(word)

        # Character offsets within the sentence string
        start = 0
        for idx, w in enumerate(words):
            if not w.string:
                w.index_char_start = None
                w.index_char_stop = None
                continue
            pos = sentence.find(w.string, start)
            if pos != -1:
                w.index_char_start = pos
                w.index_char_stop = pos + len(w.string)
                start = w.index_char_stop or start
        for w in words:
            w.index_sentence = i
        tmp.words = words
        # Track usage per sentence for aggregation later
        return i, tmp, res.usage

    tasks = [process_one(i, s) for i, s in enumerate(doc.sentence_strings)]
    log.info(
        "[async] Dispatching %d tasks with max_concurrency=%d",
        len(tasks),
        max_concurrency,
    )
    results = await asyncio.gather(*tasks)
    results_sorted = sorted(results, key=lambda x: x[0])

    # Flatten words, set global token indices
    all_words: list[Word] = []
    token_counter = 0
    aggregated_usage = {"input": 0, "output": 0, "total": 0}
    for idx, tmp, usage in results_sorted:
        for k in aggregated_usage:
            aggregated_usage[k] += usage.get(k, 0)
        for w in tmp.words:
            w.index_token = token_counter
            all_words.append(w)
            token_counter += 1

    doc.words = all_words
    _update_doc_openai_stage(doc, stage="pos", stage_tokens=aggregated_usage)
    log.info(
        "[async] Completed morphosyntax generation: %d tokens across %d sentences",
        len(all_words),
        len(doc.sentence_strings),
    )
    return doc


def generate_gpt_morphosyntax_concurrent(
    doc: Doc,
    *,
    max_concurrency: int = 4,
    max_retries: int = 2,
) -> Doc:
    """Run the async morphosyntax generator safely but appears synchronous from the outside.

    - If there is no running event loop (typical scripts/CLIs), uses
      ``asyncio.run`` directly.
    - If an event loop is already running (e.g., Jupyter, FastAPI), this spins
      up a worker thread and runs a fresh event loop there to avoid the
      "cannot call asyncio.run() from a running event loop" error.

    The output is identical to calling :func:`generate_gpt_morphosyntax_async`
    and returns the same ``Doc`` instance enriched with morphosyntax and
    aggregated usage.

    Args:
        doc: Input document with sentences, language, and backend configured.
        max_concurrency: Maximum concurrent LLM requests.
        max_retries: Per‑request retry budget.

    Returns:
        The input ``Doc`` updated in place, same as the async variant.

    """
    log = bind_from_doc(doc)
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        log.info("[async-wrap] No running event loop detected; using asyncio.run()")
        return asyncio.run(
            generate_gpt_morphosyntax_async(
                doc,
                max_concurrency=max_concurrency,
                max_retries=max_retries,
            )
        )
    else:
        log.info(
            "[async-wrap] Running inside an event loop; dispatching to worker thread"
        )

        def _runner() -> Doc:
            return asyncio.run(
                generate_gpt_morphosyntax_async(
                    doc,
                    max_concurrency=max_concurrency,
                    max_retries=max_retries,
                )
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            fut = ex.submit(_runner)
            result = fut.result()
            log.info("[async-wrap] Completed in worker thread")
            return result


def _update_doc_openai_stage(
    doc: Doc, *, stage: str, stage_tokens: dict[str, int]
) -> None:
    """Update doc.openai with stage-specific and overall totals.

    Keeps one entry per stage (e.g., "pos", "dep") and a single "overall" sum.
    """
    stage_norm = stage.strip().lower()
    in_tokens = int(stage_tokens.get("input", 0))
    out_tokens = int(stage_tokens.get("output", 0))
    tot_tokens = int(stage_tokens.get("total", 0))

    entries: list[dict[str, Any]] = []
    for e in doc.openai or []:
        if isinstance(e, dict):
            s = str(e.get("stage", "")).lower()
            if s and s not in {stage_norm, "overall"}:
                entries.append(e)
    # Add/replace this stage
    entries.append(
        {
            "stage": stage_norm,
            "input": in_tokens,
            "output": out_tokens,
            "total": tot_tokens,
        }
    )
    # Compute overall from all non-overall entries
    overall = {"input": 0, "output": 0, "total": 0}
    for e in entries:
        s = str(e.get("stage", "")).lower()
        if s == "overall":
            continue
        for k in overall:
            try:
                val: Any = e.get(k, 0)
                overall[k] += int(val)
            except Exception:
                pass
    entries.append({"stage": "overall", **overall})
    doc.openai = entries
