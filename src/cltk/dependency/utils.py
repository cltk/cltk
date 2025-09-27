import asyncio
import concurrent.futures
from typing import Any, Optional, cast, get_args

from colorama import Fore, Style
from tqdm import tqdm

from cltk.core.cltk_logger import logger
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
from cltk.morphosyntax.ud_deprels import UDDeprelTag, get_ud_deprel_tag
from cltk.morphosyntax.ud_features import UDFeatureTagSet
from cltk.morphosyntax.utils import _update_doc_openai_stage


def _parse_dep_tsv_table(tsv_string: str) -> list[dict[str, str]]:
    """Parse a minimal dependency TSV with columns FORM, HEAD, DEPREL.

    The function is intentionally strict to keep parsing predictable. It accepts
    an optional header row (case‑insensitive) and ignores Markdown code fences.
    """
    lines = [line.strip() for line in tsv_string.strip().splitlines() if line.strip()]
    header = ["form", "head", "deprel"]
    out: list[dict[str, str]] = []
    for line in lines:
        if line.startswith("```"):
            continue
        parts = line.split("\t")
        # Allow extra columns but only take the first three in order
        if len(parts) < 3:
            logger.debug(
                "[dep] Skipping malformed line (expected 3+ columns): %s", line
            )
            continue
        maybe_header = [p.lower() for p in parts[:3]]
        if maybe_header == header:
            # Skip header row
            continue
        entry = dict(zip(header, parts[:3]))
        out.append(entry)
    return out


def _format_feats(feats: Optional[UDFeatureTagSet]) -> str:
    """Serialize a UDFeatureTagSet into a UD FEATS string (e.g., "Case=Nom|Number=Sing").

    Returns "_" when no features are present.
    """
    try:
        if not feats or not getattr(feats, "features", None):
            return "_"
        items: list[str] = []
        for f in feats.features:
            key = getattr(f, "key", None)
            val = getattr(f, "value", None)
            if key and val:
                items.append(f"{key}={val}")
        return "|".join(items) if items else "_"
    except Exception:  # pragma: no cover - defensive
        return "_"


def generate_dependency_tree(
    doc: Doc,
    sentence_idx: Optional[int] = None,
    max_retries: int = 2,
    client: Optional[Any] = None,
) -> Doc:
    """Call the configured generative backend and return UD dependency annotations for a short span.

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
    # If words are available, supply them to the model to ensure alignment
    token_table = None
    if doc.words:
        lines: list[str] = ["INDEX\tFORM\tUPOS\tFEATS"]
        for idx, w in enumerate(doc.words, 1):
            upos = getattr(getattr(w, "upos", None), "tag", None) or "_"
            feats = _format_feats(getattr(w, "features", None))
            tok_form = w.string or ""
            lines.append(f"{idx}\t{tok_form}\t{upos}\t{feats}")
        token_table = "\n".join(lines)

    if token_table:
        from cltk.genai.prompts import dependency_prompt_from_tokens

        pinfo = dependency_prompt_from_tokens(token_table)
    else:
        from cltk.genai.prompts import dependency_prompt_from_text

        pinfo = dependency_prompt_from_text(lang_or_dialect_name, doc.normalized_text)
    prompt = pinfo.text
    log = bind_from_doc(
        doc, sentence_idx=sentence_idx, prompt_version=str(pinfo.version)
    )
    log.info("[prompt] %s v%s hash=%s", pinfo.kind, pinfo.version, pinfo.digest)
    import os as _os

    if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {"1", "true", "yes", "on"}:
        log.debug(prompt)
    # code_blocks: list[Any] = []
    if not doc.backend:
        msg_no_backend: str = "Doc must have `.backend` set to 'openai', 'ollama', or 'ollama-cloud' to use generate_dependency_tree."
        log.error(msg_no_backend)
        raise CLTKException(msg_no_backend)
    if not doc.model:
        msg_no_backend_version: str = "Doc missing `.model`. Set to a supported model to use generate_dependency_tree."
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
            f"Unsupported backend for dependency generation: {doc.backend}."
        )
    openai_res_obj: CLTKGenAIResponse = client.generate(
        prompt=prompt, max_retries=max_retries
    )
    openai_res: str = openai_res_obj.response
    openai_usage: dict[str, int] = openai_res_obj.usage
    if not doc.openai:
        doc.openai = list()
    doc.openai.append(openai_usage)

    rows = _parse_dep_tsv_table(openai_res)
    if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {"1", "true", "yes", "on"}:
        log.debug(f"[dep] Parsed rows:\n{rows}")
    # If we already have words, update them in place; otherwise, create fresh Word objects
    words: list[Word] = list(doc.words) if doc.words else []
    for i, row in enumerate(rows):
        form_val: Optional[str] = row.get("form")
        head_raw: Optional[str] = row.get("head")
        deprel_raw: Optional[str] = row.get("deprel")
        if not form_val or head_raw is None or deprel_raw is None:
            log.error("[dep] Missing fields in row: %s", row)
            continue
        # Validate deprel (support subtypes like obl:tmod)
        main, subtype = (deprel_raw.split(":", 1) + [None])[:2]
        tag: Optional[UDDeprelTag] = None
        try:
            if main is not None:
                tag = get_ud_deprel_tag(main, subtype=subtype)
            else:
                log.error("[dep] Main deprel is None for row: %s", row)
        except ValueError as e:  # invalid subtype
            log.error("[dep] Invalid deprel '%s': %s", deprel_raw, e)
        # Convert HEAD (UD 1-based; 0=root) → governor index (0-based) or None
        governor: Optional[int]
        try:
            head_val = int(head_raw)
            governor = None if head_val == 0 else head_val - 1
        except ValueError:
            log.error("[dep] Non-integer HEAD '%s' for form '%s'", head_raw, form_val)
            governor = None
        if i < len(words):
            # Update existing word, preserving lemma/upos/features
            w = words[i]
            if not w.string:
                w.string = form_val
            w.dependency_relation = tag
            w.governor = governor
            words[i] = w
        else:
            word = Word(
                string=form_val,
                index_token=i,
                dependency_relation=tag,
                governor=governor,
            )
            words.append(word)
    log.debug("[dep] Created %d Word objects with dependency info.", len(words))
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
    log.debug("[dep] Set character indexes for each word in input_doc.words.")

    # Add sentence idx to Word objects
    if sentence_idx is not None:
        for word in doc.words:
            word.index_sentence = sentence_idx
        log.debug(
            f"[dep] Set sentence index {sentence_idx} for all words in input_doc.words."
        )
    else:
        log.warning(
            "[dep] No sentence index provided. Skipping sentence index assignment."
        )
    return doc


def generate_gpt_dependency(doc: Doc) -> Doc:
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
            f"Unsupported backend for dependency parsing: {doc.backend}."
        )
    if not doc.normalized_text:
        msg = "Input document must have either `.normalized_text`."
        log.error(msg)
        raise ValueError(msg)
    # Dependency per sentence
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
        # Use existing morphosyntax tokens for this sentence if available
        if doc.words:
            sent_words = [
                w for w in doc.words if getattr(w, "index_sentence", None) == sent_idx
            ]
            # shallow copy to avoid mutating the original prematurely
            tmp_doc.words = (
                [Word(**w.model_dump()) for w in sent_words] if sent_words else []
            )
        tmp_doc = generate_dependency_tree(
            doc=tmp_doc,
            sentence_idx=sent_idx,
            client=client,
        )
        tmp_docs.append(tmp_doc)
        bind_from_doc(doc, sentence_idx=sent_idx).info(
            f"[dep] Completed dependency parse for sentence #{sent_idx + 1} of {len(doc.sentence_strings)}"
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
    # Merge with any existing totals (e.g., from prior processes)
    combined_tokens = {"input": 0, "output": 0, "total": 0}
    if isinstance(doc.openai, list) and doc.openai and isinstance(doc.openai[0], dict):
        for k in combined_tokens:
            combined_tokens[k] += int(doc.openai[0].get(k, 0))
    for k in combined_tokens:
        combined_tokens[k] += int(openai_total_tokens.get(k, 0))
    _update_doc_openai_stage(doc, stage="dep", stage_tokens=openai_total_tokens)
    log.debug(
        f"Combined {len(all_words)} words from all tmp_docs and updated token indices."
    )
    # Assign to your main Doc
    doc.words = all_words
    log.debug(f"[dep] Doc after dependency parsing:\n{doc}")
    assert doc.normalized_text
    log.debug(
        f"[dep] Completed dependency parsing for text starting with {doc.normalized_text[:50]} ..."
    )
    return doc


async def generate_gpt_dependency_async(
    doc: Doc,
    *,
    max_concurrency: int = 4,
    max_retries: int = 2,
) -> Doc:
    """Async variant of ``generate_gpt_dependency`` with concurrency.

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
        "[async-dep] Starting dependency generation for %s sentences",
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
            f"Unsupported backend for async dependency parsing: {doc.backend}."
        )

    # Prepare prompts per sentence
    lang_or_dialect_name = doc.dialect.name if doc.dialect else doc.language.name

    def build_prompt_from_words(words: list[Word]) -> str:
        lines = ["INDEX\tFORM\tUPOS\tFEATS"]
        for idx, w in enumerate(words, 1):
            upos = getattr(getattr(w, "upos", None), "tag", None) or "_"
            feats = _format_feats(getattr(w, "features", None))
            tok_form = w.string or ""
            lines.append(f"{idx}\t{tok_form}\t{upos}\t{feats}")
        table = "\n".join(lines)
        return (
            "Using the following tokens with UPOS and FEATS, produce a dependency parse as TSV with exactly three columns: FORM, HEAD, DEPREL.\n\n"
            "Rules:\n"
            "- Use strict UD dependency relations only (e.g., nsubj, obj, obl:tmod, root).\n"
            "- Do not change, split, merge, or reorder tokens. Use the tokens as given.\n"
            "- HEAD refers to the 1-based index of the head token in the given token order (0 for root).\n"
            "- Output must be a Markdown code block containing only a tab-delimited table with the header: FORM\tHEAD\tDEPREL.\n\n"
            f"Tokens:\n\n{table}\n\n"
            "Output only the dependency table."
        )

    sem = asyncio.Semaphore(max_concurrency)

    async def process_one(
        i: int, sentence: str, sentence_words: list[Word]
    ) -> tuple[int, Doc, dict[str, int]]:
        prompt = (
            build_prompt_from_words(sentence_words)
            if sentence_words
            else (
                f"For the following {lang_or_dialect_name} text, first tokenize the sentence. For each token, output FORM, HEAD, DEPREL.\n\nText:\n\n{sentence}\n"
            )
        )
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
        # Parse TSV and update words in place if available
        parsed = _parse_dep_tsv_table(res.response)
        words: list[Word] = (
            [Word(**w.model_dump()) for w in sentence_words] if sentence_words else []
        )
        for word_idx, row in enumerate(parsed):
            form_val: Optional[str] = row.get("form")
            head_raw: Optional[str] = row.get("head")
            deprel_raw: Optional[str] = row.get("deprel")
            if not form_val or head_raw is None or deprel_raw is None:
                log_i.error("[async-dep] Missing fields in row: %s", row)
                continue
            main, subtype = (deprel_raw.split(":", 1) + [None])[:2]
            tag = None
            try:
                if main is not None:
                    tag = get_ud_deprel_tag(main, subtype=subtype)
                else:
                    log_i.error("[async-dep] Main deprel is None for row: %s", row)
                    tag = None
            except ValueError as e:  # pragma: no cover - defensive
                log_i.error("[async-dep] Invalid deprel '%s': %s", deprel_raw, e)
            try:
                head_val = int(head_raw)
                governor = None if head_val == 0 else head_val - 1
            except ValueError:
                log_i.error(
                    "[async-dep] Non-integer HEAD '%s' for form '%s'",
                    head_raw,
                    form_val,
                )
                governor = None
            if word_idx < len(words):
                w = words[word_idx]
                if not w.string:
                    w.string = form_val
                w.dependency_relation = tag
                w.governor = governor
                words[word_idx] = w
            else:
                word = Word(
                    string=form_val,
                    index_token=word_idx,
                    dependency_relation=tag,
                    governor=governor,
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

    # Prepare words per sentence from existing morphosyntax (if any)
    sent_words_map = {
        i: [w for w in (doc.words or []) if getattr(w, "index_sentence", None) == i]
        for i in range(len(doc.sentence_strings))
    }
    tasks = [
        process_one(i, s, sent_words_map.get(i, []))
        for i, s in enumerate(doc.sentence_strings)
    ]
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
    _update_doc_openai_stage(doc, stage="dep", stage_tokens=aggregated_usage)
    log.info(
        "[async-dep] Completed dependency generation: %d tokens across %d sentences",
        len(all_words),
        len(doc.sentence_strings),
    )
    return doc


def generate_gpt_dependency_concurrent(
    doc: Doc,
    *,
    max_concurrency: int = 4,
    max_retries: int = 2,
) -> Doc:
    """Run the async dependency generator safely but appears synchronous from the outside.

    - If there is no running event loop (typical scripts/CLIs), uses
      ``asyncio.run`` directly.
    - If an event loop is already running (e.g., Jupyter, FastAPI), this spins
      up a worker thread and runs a fresh event loop there to avoid the
      "cannot call asyncio.run() from a running event loop" error.

    The output is identical to calling :func:`generate_gpt_dependency_async`
    and returns the same ``Doc`` instance enriched with dependency and
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
            generate_gpt_dependency_async(
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
                generate_gpt_dependency_async(
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
