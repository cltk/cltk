"""Utilities for GenAI-driven enrichment (glosses, IPA, idioms, pedagogy)."""

import asyncio
import concurrent.futures
import json
from typing import Any, Callable, Optional, cast, get_args

from cltk.core.cltk_logger import logger
from cltk.core.data_types import (
    AVAILABLE_MISTRAL_MODELS,
    AVAILABLE_OPENAI_MODELS,
    IPA_PRONUNCIATION_MODE,
    CLTKGenAIResponse,
    Doc,
    Gloss,
    IdiomSpan,
    IPAEnrichment,
    LemmaTranslationCandidate,
    MistralBackendConfig,
    ModelConfig,
    OllamaBackendConfig,
    OpenAIBackendConfig,
    OrthographyHelper,
    PedagogicalNote,
    ScoredText,
    Sentence,
    Word,
    WordEnrichment,
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
from cltk.genai.prompts import PromptInfo, _hash_prompt, enrichment_prompt
from cltk.morphosyntax.ud_features import UDFeatureTagSet
from cltk.morphosyntax.utils import _update_doc_genai_stage

# Prompt override type: callable, PromptInfo, or literal string.
# Callable receives (lang_or_dialect_name, token_table, ipa_mode)
PromptBuilder = (
    Callable[[str, str, IPA_PRONUNCIATION_MODE], PromptInfo] | PromptInfo | str
)


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


def _build_token_table(words: list[Word]) -> str:
    """Construct TSV with token + morph + dependency info."""
    lines: list[str] = ["INDEX\tFORM\tLEMMA\tUPOS\tFEATS\tHEAD\tDEPREL"]
    for idx, w in enumerate(words, 1):
        upos = getattr(getattr(w, "upos", None), "tag", None) or "_"
        feats = _format_feats(getattr(w, "features", None))
        head_val = "_"  # 1-based head, 0 for root
        if w.governor is None:
            head_val = "0"
        else:
            try:
                head_val = str(int(w.governor) + 1)
            except Exception:
                head_val = "_"
        deprel_val = getattr(getattr(w, "dependency_relation", None), "tag", None)
        deprel_val = deprel_val or "_"
        lines.append(
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
    return "\n".join(lines)


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


def _parse_enrichment_payload(raw: str) -> dict[str, Any]:
    """Parse JSON payload returned by the LLM."""
    try:
        cleaned = _strip_code_fences(raw)
        return cast(dict[str, Any], json.loads(cleaned))
    except Exception as e:
        logger.error("[enrich] Failed to parse enrichment payload: %s", e)
        return {}


def _safe_probability(val: Any) -> Optional[float]:
    """Return a probability in [0,1] or None if invalid."""
    try:
        fval = float(val)
        if 0.0 <= fval <= 1.0:
            return fval
    except Exception:
        return None
    return None


def _normalize_gloss_dictionary(value: Any) -> Optional[str]:
    """Normalize gloss dictionary values to a single string."""
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, str):
                if item.strip():
                    parts.append(item.strip())
                continue
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())
                continue
            try:
                text = str(item).strip()
                if text:
                    parts.append(text)
            except Exception:
                continue
        return "; ".join(parts) if parts else None
    try:
        text = str(value).strip()
        return text if text else None
    except Exception:
        return None


def _build_gloss(gloss_obj: Any) -> Optional[Gloss]:
    """Build a Gloss from a dict or a simple string."""
    if isinstance(gloss_obj, str):
        return Gloss(context=gloss_obj)
    if not isinstance(gloss_obj, dict):
        return None
    return Gloss(
        dictionary=_normalize_gloss_dictionary(gloss_obj.get("dictionary")),
        context=gloss_obj.get("context"),
        alternatives=[
            ScoredText(
                text=str(alt.get("text", "")),
                probability=_safe_probability(alt.get("probability")),
                note=alt.get("note"),
            )
            for alt in gloss_obj.get("alternatives", []) or []
            if isinstance(alt, dict) and alt.get("text")
        ],
    )


def _build_translations(candidates: Any) -> list[LemmaTranslationCandidate]:
    """Convert raw translation candidates to LemmaTranslationCandidate objects."""
    out: list[LemmaTranslationCandidate] = []
    if not candidates:
        return out
    for cand in candidates:
        if not isinstance(cand, dict):
            continue
        text = cand.get("text")
        if not text:
            continue
        out.append(
            LemmaTranslationCandidate(
                text=str(text),
                probability=_safe_probability(cand.get("probability")),
                source=cand.get("source"),
            )
        )
    return out


def _build_orthography(orth_dict: Any) -> Optional[OrthographyHelper]:
    """Construct an OrthographyHelper from a dict payload."""
    if not isinstance(orth_dict, dict):
        return None
    return OrthographyHelper(
        syllables=[str(s) for s in orth_dict.get("syllables", []) or []],
        stress=orth_dict.get("stress"),
        accent_class=orth_dict.get("accent_class"),
        phonology_trace=[str(s) for s in orth_dict.get("phonology_trace", []) or []],
    )


def _build_pedagogical_notes(notes: Any) -> list[PedagogicalNote]:
    """Convert raw pedagogical note entries to PedagogicalNote objects."""
    out: list[PedagogicalNote] = []
    if not notes:
        return out
    for note in notes:
        if not isinstance(note, dict):
            continue
        text = note.get("note")
        if not text:
            continue
        out.append(
            PedagogicalNote(
                token_index=note.get("token_index"),
                relation=note.get("relation"),
                note=text,
                disambiguates=note.get("disambiguates"),
            )
        )
    return out


def _apply_token_confidence(
    word: Word, conf_obj: Any, fields: Optional[set[str]] = None
) -> None:
    """Attach token-level confidence values, optionally filtered by fields."""
    if not isinstance(conf_obj, dict):
        return
    mapping = {
        "gloss": "gloss",
        "lemma_translations": "lemma_translations",
        "ipa": "ipa",
        "orthography": "orthography",
        "pedagogy": "pedagogical_notes",
    }
    if fields is None:
        allowed = set(mapping)
    else:
        allowed = set()
        if "lexicon" in fields:
            allowed.update({"gloss", "lemma_translations"})
        if "phonology" in fields:
            allowed.update({"ipa", "orthography"})
        if "pedagogy" in fields:
            allowed.update({"pedagogy"})
    for key, field in mapping.items():
        if key not in allowed:
            continue
        conf_val = _safe_probability(conf_obj.get(key))
        if conf_val is not None:
            word.confidence[field] = conf_val


def _apply_payload_to_words(
    sent_words: list[Word],
    payload: dict[str, Any],
    sentence_idx: int,
    provenance_id: Optional[str] = None,
    fields: Optional[set[str]] = None,
) -> tuple[list[Word], list[IdiomSpan]]:
    """Attach enrichment fields and return idiom spans, honoring field filters."""
    idioms_out: list[IdiomSpan] = []
    token_items = payload.get("tokens") if isinstance(payload, dict) else None
    if not isinstance(token_items, list):
        return sent_words, idioms_out

    include_lexicon = fields is None or "lexicon" in fields
    include_phonology = fields is None or "phonology" in fields
    include_idioms = fields is None or "idioms" in fields
    include_pedagogy = fields is None or "pedagogy" in fields

    # Map sentence-local idx (1-based) to Word
    idx_to_word: dict[int, Word] = {}
    for i, w in enumerate(sent_words, 1):
        idx_to_word[i] = w

    # Apply token-level enrichment
    for token_obj in token_items:
        if not isinstance(token_obj, dict):
            continue
        idx = token_obj.get("index")
        if not isinstance(idx, int):
            continue
        word = idx_to_word.get(idx)
        if word is None:
            continue

        gloss = _build_gloss(token_obj.get("gloss")) if include_lexicon else None

        ipa_obj = None
        orth = None
        if include_phonology:
            ipa_raw = token_obj.get("ipa")
            if isinstance(ipa_raw, dict):
                mode = ipa_raw.get("mode")
                if mode:
                    try:
                        ipa_mode_val = cast(IPA_PRONUNCIATION_MODE, mode)
                    except Exception:
                        ipa_mode_val = None
                else:
                    ipa_mode_val = None
                ipa_value = ipa_raw.get("value")
                if ipa_value:
                    ipa_obj = IPAEnrichment(
                        value=str(ipa_value), mode=ipa_mode_val or "attic_5c_bce"
                    )
            orth = _build_orthography(token_obj.get("orthography"))

        translations = (
            _build_translations(token_obj.get("lemma_translations"))
            if include_lexicon
            else []
        )
        notes = (
            _build_pedagogical_notes(token_obj.get("pedagogy"))
            if include_pedagogy
            else []
        )
        idiom_ids = (
            [str(iid) for iid in token_obj.get("idiom_span_ids", []) or []]
            if include_idioms
            else []
        )

        if fields is None:
            word.enrichment = WordEnrichment(
                gloss=gloss,
                lemma_translations=translations,
                ipa=ipa_obj,
                orthography=orth,
                idiom_span_ids=idiom_ids,
                pedagogical_notes=notes,
            )
        else:
            enrichment = word.enrichment or WordEnrichment()
            if include_lexicon:
                enrichment.gloss = gloss
                enrichment.lemma_translations = translations
            if include_phonology:
                enrichment.ipa = ipa_obj
                enrichment.orthography = orth
            if include_idioms:
                enrichment.idiom_span_ids = idiom_ids
            if include_pedagogy:
                enrichment.pedagogical_notes = notes
            word.enrichment = enrichment

        _apply_token_confidence(word, token_obj.get("confidence"), fields=fields)
        if provenance_id:
            if include_lexicon:
                word.annotation_sources["gloss"] = provenance_id
                word.annotation_sources["lemma_translations"] = provenance_id
            if include_phonology:
                word.annotation_sources["ipa"] = provenance_id
                word.annotation_sources["orthography"] = provenance_id
            if include_pedagogy:
                word.annotation_sources["pedagogical_notes"] = provenance_id
        # Optionally propagate syllables/IPA to existing fields for convenience
        if include_phonology and orth and orth.syllables:
            word.syllables = orth.syllables
        if include_phonology and ipa_obj and ipa_obj.value:
            word.phonetic_transcription = ipa_obj.value
        idx_to_word[idx] = word

    # Build idiom spans (span-level)
    if not include_idioms:
        ordered_words = [idx_to_word[i] for i in sorted(idx_to_word.keys())]
        return ordered_words, idioms_out
    for idiom_obj in payload.get("idioms", []) or []:
        if not isinstance(idiom_obj, dict):
            continue
        token_idxs = idiom_obj.get("token_indices") or []
        token_idxs = [ti for ti in token_idxs if isinstance(ti, int)]
        if not token_idxs:
            continue
        global_idxs: list[int] = []
        for ti in token_idxs:
            w_opt = idx_to_word.get(ti)
            if w_opt and w_opt.index_token is not None:
                global_idxs.append(w_opt.index_token)
        idiom = IdiomSpan(
            id=str(idiom_obj.get("id")) if idiom_obj.get("id") else None,
            token_indices=global_idxs,
            phrase_gloss=idiom_obj.get("phrase_gloss"),
            kind=idiom_obj.get("kind"),
            confidence=_safe_probability(idiom_obj.get("confidence")),
        )
        idioms_out.append(idiom)
        # Attach span id to member words for easy lookup
        span_id = idiom.id
        if span_id:
            for ti in token_idxs:
                w_opt = idx_to_word.get(ti)
                if w_opt and w_opt.enrichment:
                    if span_id not in w_opt.enrichment.idiom_span_ids:
                        w_opt.enrichment.idiom_span_ids.append(span_id)
                    idx_to_word[ti] = w_opt

    ordered_words = [idx_to_word[i] for i in sorted(idx_to_word.keys())]
    return ordered_words, idioms_out


def _resolve_enrichment_prompt(
    *,
    lang_or_dialect_name: str,
    token_table: str,
    ipa_mode: IPA_PRONUNCIATION_MODE,
    builder: Optional[PromptBuilder],
) -> PromptInfo:
    """Resolve the enrichment prompt from defaults or a custom builder."""
    if builder is None:
        return enrichment_prompt(lang_or_dialect_name, token_table, ipa_mode)
    if isinstance(builder, PromptInfo):
        return builder
    if isinstance(builder, str):
        formatted = builder.format(
            lang_or_dialect_name=lang_or_dialect_name,
            token_table=token_table,
            ipa_mode=ipa_mode,
        )
        version = "custom-1"
        return PromptInfo(
            kind="enrichment",
            version=version,
            text=formatted,
            digest=_hash_prompt("enrichment", version, formatted),
        )
    if callable(builder):
        return builder(lang_or_dialect_name, token_table, ipa_mode)
    raise TypeError("Unsupported prompt_builder type for enrichment.")


def generate_enrichment_for_sentence(
    *,
    doc: Doc,
    sentence_idx: int,
    words: list[Word],
    client: Any,
    ipa_mode: IPA_PRONUNCIATION_MODE,
    max_retries: int,
    prompt_builder: Optional[PromptBuilder],
    prompt_profile: Optional[str],
    prompt_digest: Optional[str],
    fields: Optional[set[str]] = None,
    provenance_process: Optional[str] = None,
) -> tuple[list[Word], list[IdiomSpan], dict[str, int]]:
    """Call the LLM for one sentence, optionally filtered by fields."""
    lang_or_dialect_name = doc.dialect.name if doc.dialect else doc.language.name
    token_table = _build_token_table(words)
    pinfo = _resolve_enrichment_prompt(
        lang_or_dialect_name=lang_or_dialect_name,
        token_table=token_table,
        ipa_mode=ipa_mode,
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
        "ipa_mode": ipa_mode,
    }
    if prompt_profile:
        notes["prompt_profile"] = prompt_profile
    prov_record = build_provenance_record(
        language=lang_id,
        backend=doc.backend,
        process=provenance_process or "enrichment",
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
    payload = _parse_enrichment_payload(res_obj.response)
    updated_words, idioms = _apply_payload_to_words(
        words, payload, sentence_idx, provenance_id=prov_id, fields=fields
    )
    return updated_words, idioms, res_obj.usage


def generate_gpt_enrichment(
    doc: Doc,
    *,
    ipa_mode: IPA_PRONUNCIATION_MODE = "attic_5c_bce",
    prompt_builder: Optional[PromptBuilder] = None,
    prompt_profile: Optional[str] = None,
    prompt_digest: Optional[str] = None,
    fields: Optional[set[str]] = None,
    max_retries: int = 2,
    provenance_process: Optional[str] = None,
) -> Doc:
    """Sequential enrichment across sentences, optionally scoped by fields."""
    log = bind_from_doc(doc)
    if not doc.words:
        msg = "Doc must contain tokens (with morph + dependency) before enrichment."
        log.error(msg)
        raise CLTKException(msg)
    if not doc.backend:
        msg_backend = "Doc must set `.backend` to use enrichment."
        log.error(msg_backend)
        raise CLTKException(msg_backend)
    if not doc.model:
        msg_model = "Doc missing `.model`. Set to a supported model for enrichment."
        log.error(msg_model)
        raise CLTKException(msg_model)

    backend_config = _get_backend_config(doc)
    if backend_config and getattr(backend_config, "max_retries", None) is not None:
        max_retries = int(getattr(backend_config, "max_retries"))

    # Reuse one client across all sentences
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
        raise CLTKException(f"Unsupported backend for enrichment: {doc.backend}.")

    genai_total_tokens = {"input": 0, "output": 0, "total": 0}
    all_idioms: list[IdiomSpan] = []

    # Prefer sentence grouping from token annotations
    sentences: list[Sentence]
    if doc.sentences:
        sentences = doc.sentences
    else:
        # Fallback: treat all words as one sentence
        sentences = [Sentence(words=doc.words, index=0)]

    for sent in sentences:
        if not sent.words:
            continue
        sent_idx = getattr(sent, "index", None)
        words = sent.words
        updated_words, idioms, usage = generate_enrichment_for_sentence(
            doc=doc,
            sentence_idx=sent_idx if sent_idx is not None else 0,
            words=words,
            client=client,
            ipa_mode=ipa_mode,
            max_retries=max_retries,
            prompt_builder=prompt_builder,
            prompt_profile=prompt_profile,
            prompt_digest=prompt_digest,
            fields=fields,
            provenance_process=provenance_process,
        )
        # updated_words are references into doc.words via doc.sentences; no reassignment needed
        all_idioms.extend(idioms)
        for k in genai_total_tokens:
            genai_total_tokens[k] += usage.get(k, 0)
        bind_from_doc(doc, sentence_idx=sent_idx).info(
            f"[enrich] Completed enrichment for sentence #{(sent_idx or 0) + 1}"
        )

    # Store idiom spans at doc level only when idioms are included.
    if fields is None or "idioms" in fields:
        doc.idiom_spans = all_idioms
    _update_doc_genai_stage(doc, stage="enrich", stage_tokens=genai_total_tokens)
    log.info(
        "[enrich] Completed enrichment: %d tokens across %d sentences",
        len(doc.words),
        len(sentences),
    )
    return doc


def generate_gpt_enrichment_concurrent(
    doc: Doc,
    *,
    ipa_mode: IPA_PRONUNCIATION_MODE = "attic_5c_bce",
    prompt_builder: Optional[PromptBuilder] = None,
    prompt_profile: Optional[str] = None,
    prompt_digest: Optional[str] = None,
    fields: Optional[set[str]] = None,
    max_retries: int = 2,
    provenance_process: Optional[str] = None,
) -> Doc:
    """Safely call enrichment even when an event loop is running, honoring field filters."""
    log = bind_from_doc(doc)
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        log.info("[async-wrap] No running event loop; using direct enrichment.")
        return generate_gpt_enrichment(
            doc,
            ipa_mode=ipa_mode,
            prompt_builder=prompt_builder,
            prompt_profile=prompt_profile,
            prompt_digest=prompt_digest,
            fields=fields,
            max_retries=max_retries,
            provenance_process=provenance_process,
        )

    def _runner() -> Doc:
        """Run enrichment inside a worker thread when an event loop exists."""
        return generate_gpt_enrichment(
            doc,
            ipa_mode=ipa_mode,
            prompt_builder=prompt_builder,
            prompt_profile=prompt_profile,
            prompt_digest=prompt_digest,
            fields=fields,
            max_retries=max_retries,
            provenance_process=provenance_process,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(_runner)
        result = fut.result()
        log.info("[async-wrap] Completed enrichment in worker thread")
        return result
