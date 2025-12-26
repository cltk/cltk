"""Output dispatch helpers for the CLTK CLI (pure; no I/O)."""

from typing import Any, Callable, Optional

from cltk.core.data_types import Doc, Translation, Word
from cltk.utils.file_outputs import (
    doc_to_conllu,
    doc_to_feature_table,
    format_readers_guide,
)

OutputPayload = str | dict[str, Any] | Any

OUTPUT_TARGETS: dict[str, Callable[[Doc], OutputPayload]] = {
    "raw": lambda doc: _render_raw(doc),
    "conllu": doc_to_conllu,
    "feature-table": doc_to_feature_table,
    "readers-guide": format_readers_guide,
    "json": lambda doc: doc_to_json(doc),
}

OUTPUT_FORMATS: dict[str, set[str]] = {
    "feature-table": {"csv", "tsv", "parquet"},
    "json": {"pretty", "min"},
}

DEFAULT_FORMATS: dict[str, str] = {
    "feature-table": "csv",
    "json": "pretty",
}


def normalize_output_name(name: str) -> str:
    """Normalize output identifiers."""
    return name.strip().lower()


def normalize_format(name: Optional[str]) -> Optional[str]:
    """Normalize format identifiers."""
    if name is None:
        return None
    return name.strip().lower()


def resolve_format(out: str, fmt: Optional[str]) -> Optional[str]:
    """Validate and resolve the output format for an output target."""
    out_name = normalize_output_name(out)
    fmt_name = normalize_format(fmt)
    allowed = OUTPUT_FORMATS.get(out_name)
    if allowed is None:
        if fmt_name is not None:
            raise ValueError(f"--format is not supported for output '{out_name}'.")
        return None
    if fmt_name is None:
        return DEFAULT_FORMATS.get(out_name)
    if fmt_name not in allowed:
        allowed_list = ", ".join(sorted(allowed))
        raise ValueError(
            f"Unsupported format '{fmt_name}' for output '{out_name}'. "
            f"Choose from: {allowed_list}."
        )
    return fmt_name


def render_output(
    doc: Doc,
    out: str,
    *,
    max_sentences: Optional[int] = None,
    max_tokens: Optional[int] = None,
) -> OutputPayload:
    """Render output for a document using the named output target."""
    out_name = normalize_output_name(out)
    renderer = OUTPUT_TARGETS.get(out_name)
    if renderer is None:
        allowed = ", ".join(sorted(OUTPUT_TARGETS))
        raise ValueError(f"Unsupported output '{out_name}'. Choose from: {allowed}.")
    if out_name == "raw":
        return raw_summary(doc, max_sentences=max_sentences, max_tokens=max_tokens)
    if out_name == "json":
        return doc_to_json(doc, max_sentences=max_sentences, max_tokens=max_tokens)
    sliced = _slice_doc(doc, max_sentences=max_sentences, max_tokens=max_tokens)
    return renderer(sliced)


def doc_to_json(
    doc: Doc,
    *,
    max_sentences: Optional[int] = None,
    max_tokens: Optional[int] = None,
) -> dict[str, Any]:
    """Return a JSON-serializable structure for a ``Doc``."""
    sliced = _slice_doc(doc, max_sentences=max_sentences, max_tokens=max_tokens)
    groups = _group_words(sliced)
    language = sliced.language
    dialect = sliced.dialect
    data: dict[str, Any] = {
        "meta": {
            "language": {
                "name": language.name,
                "glottolog_id": language.glottolog_id,
                "iso_639_3": language.iso,
            },
            "dialect": {
                "name": dialect.name,
                "glottolog_id": dialect.glottolog_id,
                "language_code": dialect.language_code,
            }
            if dialect
            else None,
            "backend": sliced.backend,
            "model": sliced.model,
            "pipeline": sliced.pipeline.__class__.__name__ if sliced.pipeline else None,
        },
        "text": {
            "raw": sliced.raw,
            "normalized": sliced.normalized_text,
        },
        "sentences": [],
    }
    sentences: list[dict[str, Any]] = []
    for sent_idx, words in groups:
        sent_text = " ".join([w.string for w in words if w.string]).strip()
        translation = (
            _serialize_translation(sliced.sentence_translations.get(sent_idx))
            if sent_idx is not None
            else None
        )
        tokens: list[dict[str, Any]] = []
        for token_idx, word in enumerate(words, start=1):
            tokens.append(
                {
                    "index_token": word.index_token,
                    "token_index_sentence": token_idx,
                    "index_char_start": word.index_char_start,
                    "index_char_stop": word.index_char_stop,
                    "string": word.string,
                    "lemma": word.lemma,
                    "upos": _serialize_upos(word),
                    "xpos": word.xpos,
                    "features": _serialize_features(word),
                    "dependency_relation": _serialize_deprel(word),
                    "governor": word.governor,
                }
            )
        sentences.append(
            {
                "index": sent_idx,
                "text": sent_text or None,
                "translation": translation,
                "tokens": tokens,
            }
        )
    data["sentences"] = sentences
    return data


def ensure_text_payload(payload: OutputPayload, out: str) -> str:
    """Ensure a rendered payload is text."""
    if isinstance(payload, str):
        return payload
    raise ValueError(f"Output '{out}' did not produce text.")


def ensure_json_payload(payload: OutputPayload, out: str) -> dict[str, Any]:
    """Ensure a rendered payload is JSON-serializable dict."""
    if isinstance(payload, dict):
        return payload
    raise ValueError(f"Output '{out}' did not produce JSON.")


def raw_summary(
    doc: Doc,
    *,
    max_sentences: Optional[int] = None,
    max_tokens: Optional[int] = None,
) -> str:
    """Return a human-readable summary for ``Doc``."""
    total_sentences = len(_group_words(doc))
    total_tokens = len(doc.words or [])
    sliced = _slice_doc(doc, max_sentences=max_sentences, max_tokens=max_tokens)
    out_sentences = len(_group_words(sliced))
    out_tokens = len(sliced.words or [])

    lang = doc.language
    backend = doc.backend or "unknown"
    model = doc.model
    lines = [
        f"Language: {lang.name} ({lang.glottolog_id})",
        f"Backend: {backend}" + (f" (model: {model})" if model else ""),
        f"Sentences: {out_sentences}",
        f"Tokens: {out_tokens}",
    ]
    if (max_sentences or max_tokens) and (
        total_sentences != out_sentences or total_tokens != out_tokens
    ):
        lines.append(
            "Limits: "
            f"sentences={max_sentences or '-'}, "
            f"tokens={max_tokens or '-'} "
            f"(original {total_sentences} sentences, {total_tokens} tokens)"
        )
    return "\n".join(lines).rstrip() + "\n"


def _render_raw(doc: Doc) -> str:
    """Proxy to the raw summary renderer."""
    return raw_summary(doc)


def _group_words(doc: Doc) -> list[tuple[Optional[int], list[Word]]]:
    """Group words by sentence index in display order."""
    words: list[Word] = getattr(doc, "words", []) or []
    if not words:
        return []

    grouped: dict[Optional[int], list[tuple[int, Word]]] = {}
    order: list[Optional[int]] = []
    for order_idx, word in enumerate(words):
        sent_idx = getattr(word, "index_sentence", None)
        if sent_idx not in grouped:
            grouped[sent_idx] = []
            order.append(sent_idx)
        grouped[sent_idx].append((order_idx, word))

    def _sort_key(item: tuple[int, Word]) -> int:
        """Sort tokens by sentence index when available."""
        idx_token: Optional[int] = getattr(item[1], "index_token", None)
        return idx_token if isinstance(idx_token, int) else item[0]

    grouped_words: list[tuple[Optional[int], list[Word]]] = []
    for sent_idx in order:
        entries = sorted(grouped[sent_idx], key=_sort_key)
        grouped_words.append((sent_idx, [word for _, word in entries]))
    return grouped_words


def _slice_doc(
    doc: Doc,
    *,
    max_sentences: Optional[int],
    max_tokens: Optional[int],
) -> Doc:
    """Return a shallow copy of the doc limited by sentences/tokens."""
    if max_sentences is None and max_tokens is None:
        return doc
    groups = _group_words(doc)
    if max_sentences is not None:
        if max_sentences <= 0:
            raise ValueError("--max-sentences must be a positive integer.")
        groups = groups[:max_sentences]
    if max_tokens is not None:
        if max_tokens <= 0:
            raise ValueError("--max-tokens must be a positive integer.")
        groups = [(idx, words[:max_tokens]) for idx, words in groups]
    selected: list[Word] = [word for _, words in groups for word in words]
    return doc.model_copy(update={"words": selected})


def _serialize_features(word: Word) -> dict[str, str]:
    """Flatten UD feature tags into a simple mapping."""
    feats = getattr(word, "features", None)
    feature_list = getattr(feats, "features", None)
    if not feature_list:
        return {}
    output: dict[str, str] = {}
    for feat in feature_list:
        key = getattr(feat, "key", None)
        value = getattr(feat, "value", None)
        if key and value:
            output[str(key)] = str(value)
    return output


def _serialize_deprel(word: Word) -> Optional[dict[str, Optional[str]]]:
    """Serialize dependency relation data for JSON output."""
    dep = getattr(word, "dependency_relation", None)
    if not dep:
        return None
    return {
        "code": getattr(dep, "code", None),
        "name": getattr(dep, "name", None),
        "subtype": getattr(dep, "subtype", None),
    }


def _serialize_upos(word: Word) -> Optional[dict[str, Optional[str]]]:
    """Serialize UPOS tag data for JSON output."""
    upos = getattr(word, "upos", None)
    if not upos:
        return None
    return {
        "tag": getattr(upos, "tag", None),
        "name": getattr(upos, "name", None),
    }


def _serialize_translation(
    translation: Optional[Translation],
) -> Optional[dict[str, Optional[str]]]:
    """Serialize translation metadata for JSON output."""
    if translation is None:
        return None
    return {
        "source_lang_id": translation.source_lang_id,
        "target_lang_id": translation.target_lang_id,
        "text": translation.text,
        "notes": translation.notes,
    }
