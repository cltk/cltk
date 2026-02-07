"""Utilities for GenAI-driven translation."""

import asyncio
import concurrent.futures
import json
from typing import Any, Callable, Optional, cast, get_args

from cltk.core.cltk_logger import logger
from cltk.core.data_types import (
    AVAILABLE_MISTRAL_MODELS,
    AVAILABLE_OPENAI_MODELS,
    CLTKGenAIResponse,
    Doc,
    IdiomSpan,
    MistralBackendConfig,
    ModelConfig,
    OllamaBackendConfig,
    OpenAIBackendConfig,
    Sentence,
    Translation,
    UDFeatureTagSet,
    Word,
)
from cltk.core.exceptions import CLTKException
from cltk.core.logging_utils import bind_from_doc
from cltk.core.provenance import (
    add_provenance_record,
    build_provenance_record,
    extract_doc_config,
)
from cltk.genai.mistral import MistralConnection
from cltk.genai.ollama import OllamaConnection
from cltk.genai.openai import OpenAIConnection
from cltk.genai.prompts import PromptInfo, _hash_prompt, translation_prompt
from cltk.morphosyntax.utils import _update_doc_genai_stage

PromptBuilder = Callable[[str, str, str], PromptInfo] | PromptInfo | str
TranslationPromptBuilder = PromptBuilder


def _get_backend_config(doc: Doc) -> Optional[ModelConfig]:
    """Extract backend configuration attached to the document, if any."""
    try:
        cfg = doc.metadata.get("backend_config")
    except Exception:
        return None
    return cfg if isinstance(cfg, ModelConfig) else None


def _format_feats(feats: Optional[UDFeatureTagSet]) -> str:
    """Serialize UDFeatureTagSet into a UD FEATS string (e.g., Case=Nom|Number=Sing)."""
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


def _strip_code_fences(text: str) -> str:
    """Remove Markdown code fences if present."""
    stripped = text.strip()
    if stripped.startswith("```"):
        try:
            stripped = stripped.strip("`")
            if "\n" in stripped:
                stripped = stripped.split("\n", 1)[1]
            if "```" in stripped:
                stripped = stripped.rsplit("```", 1)[0]
        except Exception:
            pass
    return stripped.strip()


def _parse_translation_payload(raw: str) -> dict[str, Any]:
    """Parse JSON payload returned by the LLM for translations."""
    cleaned = _strip_code_fences(raw)
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return cast(dict[str, Any], parsed)
        if isinstance(parsed, str):
            return {"translation": parsed}
    except Exception as e:  # pragma: no cover - defensive logging
        logger.error("[translate] Failed to parse translation payload: %s", e)
    return {"translation": cleaned}


def _safe_confidence(val: Any) -> Optional[float]:
    """Return a confidence score in [0,1] or None if invalid."""
    try:
        fval = float(val)
    except (TypeError, ValueError):
        return None
    if fval < 0 or fval > 1:
        return None
    return fval


def _gloss_summary(word: Word) -> str:
    """Return a compact gloss summary for a word, if available."""
    if not word.enrichment or not word.enrichment.gloss:
        return ""
    gloss = word.enrichment.gloss
    parts: list[str] = []
    if gloss.dictionary:
        parts.append(f"dict={gloss.dictionary}")
    if gloss.context:
        parts.append(f"context={gloss.context}")
    if gloss.alternatives:
        alts = "; ".join(a.text for a in gloss.alternatives if a.text)
        if alts:
            parts.append(f"alts={alts}")
    return "; ".join(parts)


def _lemma_translations_summary(word: Word) -> str:
    """Summarize lemma-level translations with probabilities when present."""
    if not word.enrichment:
        return ""
    texts: list[str] = []
    for cand in word.enrichment.lemma_translations or []:
        if cand.text:
            prob = ""
            if cand.probability is not None:
                prob = f" ({cand.probability:.2f})"
            texts.append(f"{cand.text}{prob}")
    return "; ".join(texts)


def _pedagogy_summary(word: Word) -> str:
    """Summarize pedagogy notes for translation context."""
    if not word.enrichment:
        return ""
    notes: list[str] = []
    for note in word.enrichment.pedagogical_notes or []:
        if note.note:
            notes.append(note.note)
    return " | ".join(notes)


def _build_translation_context(
    *,
    sentence: Sentence,
    idioms: list[IdiomSpan],
    sentence_text: Optional[str],
) -> str:
    """Construct a rich context string for translation."""
    token_lines: list[str] = ["INDEX\tFORM\tLEMMA\tUPOS\tFEATS\tHEAD\tDEPREL"]
    enrich_lines: list[str] = ["INDEX\tGLOSS\tLEMMA_TRANSLATIONS\tIDIOMS\tPEDAGOGY"]
    words: list[Word] = sentence.words or []
    global_to_local: dict[int, int] = {}
    for idx, w in enumerate(words, 1):
        if w.index_token is not None:
            global_to_local[w.index_token] = idx
        upos = getattr(getattr(w, "upos", None), "tag", None) or "_"
        feats = _format_feats(getattr(w, "features", None))
        head_val = "_"
        if w.governor is None:
            head_val = "0"
        else:
            try:
                head_val = str(int(w.governor) + 1)
            except Exception:
                head_val = "_"
        deprel_val = getattr(getattr(w, "dependency_relation", None), "tag", None)
        deprel_val = deprel_val or "_"
        token_lines.append(
            "\t".join(
                [
                    str(idx),
                    w.string or "",
                    w.lemma or "_",
                    upos,
                    feats,
                    head_val,
                    deprel_val,
                ]
            )
        )
        gloss = _gloss_summary(w)
        lemma_trans = _lemma_translations_summary(w)
        idiom_ids = []
        if w.enrichment:
            idiom_ids = w.enrichment.idiom_span_ids
        pedagogy = _pedagogy_summary(w)
        enrich_lines.append(
            "\t".join(
                [
                    str(idx),
                    gloss or "_",
                    lemma_trans or "_",
                    ", ".join(idiom_ids) if idiom_ids else "_",
                    pedagogy or "_",
                ]
            )
        )

    sentence_word_indices = {w.index_token for w in words if w.index_token is not None}
    idiom_lines: list[str] = []
    for idiom in idioms or []:
        if not idiom.token_indices:
            continue
        if not sentence_word_indices.intersection(set(idiom.token_indices)):
            continue
        local_positions = [
            global_to_local[ti] for ti in idiom.token_indices if ti in global_to_local
        ]
        idiom_lines.append(
            f"{idiom.id or 'idiom'}: tokens {local_positions or '?'}; "
            f"phrase_gloss={idiom.phrase_gloss or '_'}; kind={idiom.kind or '_'}; "
            f"confidence={idiom.confidence if idiom.confidence is not None else '_'}"
        )
    idiom_section = "\n".join(idiom_lines) if idiom_lines else "None"

    source_sentence = sentence_text
    if not source_sentence:
        source_sentence = " ".join([w.string for w in words if w.string] or []).strip()
    return (
        f"Source sentence:\n{source_sentence or '_'}\n\n"
        "Tokens with morphosyntax and dependencies:\n"
        + "\n".join(token_lines)
        + "\n\nEnrichment hints:\n"
        + "\n".join(enrich_lines)
        + "\n\nIdioms and multi-word expressions:\n"
        + idiom_section
    )


def _resolve_translation_prompt(
    *,
    lang_or_dialect_name: str,
    target_language: str,
    context: str,
    builder: Optional[PromptBuilder],
) -> PromptInfo:
    """Resolve the translation prompt from defaults or a custom builder."""
    if builder is None:
        return translation_prompt(lang_or_dialect_name, target_language, context)
    if isinstance(builder, PromptInfo):
        return builder
    if isinstance(builder, str):
        formatted = builder.format(
            lang_or_dialect_name=lang_or_dialect_name,
            target_language=target_language,
            context=context,
        )
        version = "custom-1"
        return PromptInfo(
            kind="translation",
            version=version,
            text=formatted,
            digest=_hash_prompt("translation", version, formatted),
        )
    if callable(builder):
        return builder(lang_or_dialect_name, target_language, context)
    raise TypeError("Unsupported prompt_builder type for translation.")


def _build_translation_from_payload(
    payload: dict[str, Any],
    *,
    source_lang_id: Optional[str],
    target_lang_id: Optional[str],
    target_language: str,
) -> Optional[Translation]:
    """Construct a Translation object from model output."""
    if not payload:
        return None
    translation_text = payload.get("translation") or payload.get("text")
    notes = payload.get("notes") or payload.get("note")
    if not translation_text and isinstance(payload, dict):
        # Fall back to any single string value
        for val in payload.values():
            if isinstance(val, str) and val.strip():
                translation_text = val
                break
    if not translation_text:
        return None
    confidence = _safe_confidence(payload.get("confidence"))
    return Translation(
        source_lang_id=source_lang_id,
        target_lang_id=target_lang_id or target_language,
        text=str(translation_text).strip(),
        notes=str(notes).strip() if isinstance(notes, str) and notes.strip() else None,
        confidence=confidence,
    )


def generate_translation_for_sentence(
    *,
    doc: Doc,
    sentence_idx: int,
    sentence: Sentence,
    client: Any,
    target_language: str,
    target_language_id: Optional[str],
    source_lang_id: Optional[str],
    prompt_builder: Optional[PromptBuilder],
    prompt_profile: Optional[str],
    prompt_digest: Optional[str],
    max_retries: int,
    provenance_process: Optional[str] = None,
) -> tuple[Optional[Translation], dict[str, int]]:
    """Call the LLM for a single sentence translation."""
    lang_or_dialect_name = doc.dialect.name if doc.dialect else doc.language.name
    sentence_text = None
    try:
        if doc.sentence_strings and sentence_idx < len(doc.sentence_strings):
            sentence_text = doc.sentence_strings[sentence_idx]
    except Exception:
        sentence_text = None
    context = _build_translation_context(
        sentence=sentence,
        idioms=doc.idiom_spans or [],
        sentence_text=sentence_text,
    )
    pinfo = _resolve_translation_prompt(
        lang_or_dialect_name=lang_or_dialect_name,
        target_language=target_language,
        context=context,
        builder=prompt_builder,
    )
    prompt = pinfo.text

    log = bind_from_doc(
        doc, sentence_idx=sentence_idx, prompt_version=str(pinfo.version)
    )
    log.info("[prompt] %s v%s hash=%s", pinfo.kind, pinfo.version, pinfo.digest)
    import os as _os

    if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {"1", "true", "yes", "on"}:
        log.debug(prompt)

    lang_id = None
    try:
        if doc.dialect and doc.dialect.glottolog_id:
            lang_id = doc.dialect.glottolog_id
        else:
            lang_id = doc.language.glottolog_id
    except Exception:
        lang_id = None
    config_snapshot = extract_doc_config(doc)
    notes = {
        "prompt_kind": pinfo.kind,
        "sentence_idx": sentence_idx,
        "target_language": target_language,
        "target_language_id": target_language_id,
    }
    if prompt_profile:
        notes["prompt_profile"] = prompt_profile
    prov_record = build_provenance_record(
        language=lang_id,
        backend=doc.backend,
        process=provenance_process or "translation",
        model=str(doc.model) if doc.model else None,
        provider=str(doc.backend) if doc.backend else None,
        prompt_version=str(pinfo.version),
        prompt_text=prompt,
        prompt_digest=prompt_digest,
        config=config_snapshot,
        notes=notes,
    )
    prov_id = add_provenance_record(
        doc, prov_record, set_default=doc.default_provenance_id is None
    )

    res_obj: CLTKGenAIResponse = client.generate(prompt=prompt, max_retries=max_retries)
    payload = _parse_translation_payload(res_obj.response)
    translation = _build_translation_from_payload(
        payload,
        source_lang_id=source_lang_id,
        target_lang_id=target_language_id,
        target_language=target_language,
    )
    if translation is None:
        log.warning("[translate] Empty translation for sentence #%s", sentence_idx + 1)
    if prov_id and translation is not None:
        if not doc.sentence_annotation_sources:
            doc.sentence_annotation_sources = {}
        entry = doc.sentence_annotation_sources.get(sentence_idx, {})
        entry["translation"] = prov_id
        doc.sentence_annotation_sources[sentence_idx] = entry
    return translation, res_obj.usage


def generate_gpt_translation(
    doc: Doc,
    *,
    target_language: str = "Modern US English",
    target_language_id: Optional[str] = "en-US",
    prompt_builder: Optional[PromptBuilder] = None,
    prompt_profile: Optional[str] = None,
    prompt_digest: Optional[str] = None,
    max_retries: int = 2,
    provenance_process: Optional[str] = None,
) -> Doc:
    """Sequential translation across sentences using prior annotations."""
    log = bind_from_doc(doc)
    if not doc.words:
        msg = "Doc must contain tokens (with morph + dependency/enrichment) before translation."
        log.error(msg)
        raise CLTKException(msg)
    if not doc.backend:
        msg_backend = "Doc must set `.backend` to use translation."
        log.error(msg_backend)
        raise CLTKException(msg_backend)
    if not doc.model:
        msg_model = "Doc missing `.model`. Set to a supported model for translation."
        log.error(msg_model)
        raise CLTKException(msg_model)

    backend_config = _get_backend_config(doc)
    if backend_config and getattr(backend_config, "max_retries", None) is not None:
        max_retries = int(getattr(backend_config, "max_retries"))

    client: Any
    if doc.backend == "openai":
        if doc.model not in get_args(AVAILABLE_OPENAI_MODELS):
            msg_unsupported_backend_version: str = (
                f"Doc has unsupported `.model`: {doc.model}. "
                f"Supported versions are: {get_args(AVAILABLE_OPENAI_MODELS)}."
            )
            log.error(msg_unsupported_backend_version)
            raise CLTKException(msg_unsupported_backend_version)
        openai_cfg = (
            backend_config if isinstance(backend_config, OpenAIBackendConfig) else None
        )
        client = OpenAIConnection(
            model=cast(AVAILABLE_OPENAI_MODELS, doc.model),
            api_key=getattr(openai_cfg, "api_key", None),
            temperature=getattr(openai_cfg, "temperature", 1.0),
        )
    elif doc.backend in ("ollama", "ollama-cloud"):
        ollama_cfg = (
            backend_config if isinstance(backend_config, OllamaBackendConfig) else None
        )
        host = None
        if ollama_cfg:
            host = ollama_cfg.base_url or ollama_cfg.host
        client = OllamaConnection(
            model=str(doc.model),
            use_cloud=doc.backend == "ollama-cloud",
            host=host,
            api_key=getattr(ollama_cfg, "api_key", None),
            temperature=getattr(ollama_cfg, "temperature", None),
            top_p=getattr(ollama_cfg, "top_p", None),
            num_ctx=getattr(ollama_cfg, "num_ctx", None),
            num_predict=getattr(ollama_cfg, "num_predict", None),
            options=getattr(ollama_cfg, "options", None),
        )
    elif doc.backend == "mistral":
        if doc.model not in get_args(AVAILABLE_MISTRAL_MODELS):
            msg_unsupported_mistral_version: str = (
                f"Doc has unsupported `.model`: {doc.model}. "
                f"Supported versions are: {get_args(AVAILABLE_MISTRAL_MODELS)}."
            )
            log.error(msg_unsupported_mistral_version)
            raise CLTKException(msg_unsupported_mistral_version)
        mistral_cfg = (
            backend_config if isinstance(backend_config, MistralBackendConfig) else None
        )
        client = MistralConnection(
            model=cast(AVAILABLE_MISTRAL_MODELS, doc.model),
            api_key=getattr(mistral_cfg, "api_key", None),
            temperature=getattr(mistral_cfg, "temperature", 1.0),
        )
    else:
        raise CLTKException(f"Unsupported backend for translation: {doc.backend}.")

    genai_total_tokens = {"input": 0, "output": 0, "total": 0}
    translations_map: dict[int, Translation] = {}
    translations_list: list[Translation] = []

    sentences: list[Sentence]
    if doc.sentences:
        sentences = doc.sentences
    else:
        sentences = [Sentence(words=doc.words, index=0)]

    source_lang_id: Optional[str] = None
    try:
        source_lang_id = (
            doc.dialect.glottolog_id if doc.dialect else doc.language.glottolog_id
        )
    except Exception:
        source_lang_id = None

    for sent in sentences:
        if not sent.words:
            continue
        sent_idx = getattr(sent, "index", None)
        translation_obj, usage = generate_translation_for_sentence(
            doc=doc,
            sentence_idx=sent_idx if sent_idx is not None else 0,
            sentence=sent,
            client=client,
            target_language=target_language,
            target_language_id=target_language_id,
            source_lang_id=source_lang_id,
            prompt_builder=prompt_builder,
            prompt_profile=prompt_profile,
            prompt_digest=prompt_digest,
            max_retries=max_retries,
            provenance_process=provenance_process,
        )
        if translation_obj is not None:
            translations_map[sent_idx if sent_idx is not None else 0] = translation_obj
            translations_list.append(translation_obj)
        for k in genai_total_tokens:
            genai_total_tokens[k] += usage.get(k, 0)
        bind_from_doc(doc, sentence_idx=sent_idx).info(
            f"[translate] Completed translation for sentence #{(sent_idx or 0) + 1}"
        )

    doc.sentence_translations = translations_map
    doc.translations = translations_list
    if translations_map:
        ordered = [
            translations_map[idx].text
            for idx in sorted(translations_map.keys())
            if translations_map[idx].text
        ]
        doc.translation = " ".join(ordered)

    _update_doc_genai_stage(doc, stage="translate", stage_tokens=genai_total_tokens)
    log.info(
        "[translate] Completed translation: %d sentences (%d tokens)",
        len(translations_map),
        len(doc.words),
    )
    return doc


def generate_gpt_translation_concurrent(
    doc: Doc,
    *,
    target_language: str = "Modern US English",
    target_language_id: Optional[str] = "en-US",
    prompt_builder: Optional[PromptBuilder] = None,
    prompt_profile: Optional[str] = None,
    prompt_digest: Optional[str] = None,
    max_retries: int = 2,
    provenance_process: Optional[str] = None,
) -> Doc:
    """Safely call translation even when an event loop is running."""
    log = bind_from_doc(doc)
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        log.info("[async-wrap] No running event loop; using direct translation.")
        return generate_gpt_translation(
            doc,
            target_language=target_language,
            target_language_id=target_language_id,
            prompt_builder=prompt_builder,
            prompt_profile=prompt_profile,
            prompt_digest=prompt_digest,
            max_retries=max_retries,
            provenance_process=provenance_process,
        )

    def _runner() -> Doc:
        """Run translation inside a worker thread when an event loop exists."""
        return generate_gpt_translation(
            doc,
            target_language=target_language,
            target_language_id=target_language_id,
            prompt_builder=prompt_builder,
            prompt_profile=prompt_profile,
            prompt_digest=prompt_digest,
            max_retries=max_retries,
            provenance_process=provenance_process,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(_runner)
        result = fut.result()
        log.info("[async-wrap] Completed translation in worker thread")
        return result
