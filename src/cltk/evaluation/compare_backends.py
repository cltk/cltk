"""Compare CLTK NLP backends on the same text and report differences.

Example:
    >>> from cltk.evaluation.compare_backends import compare_backends
    >>> report = compare_backends(
    ...     "lati1261",
    ...     "Amor vincit omnia.",
    ...     ["stanza", "openai"],
    ... )
    >>> print(report["summary"]["agreement_rates"]["upos"])

Report schema (high-level):
    report = {
        "meta": {
            "language": str,
            "backends": list[str],
            "base_backend": str,
            "timestamp": str,
            "text_hash": str,
            "cltk_version": str | None,
        },
        "backends": {
            backend: {
                "model": str | None,
                "backend_config": dict | None,
                "metadata": dict,
            },
        },
        "sentences": [
            {
                "index": int,
                "text": str | None,
                "alignment": {
                    "base_backend": str,
                    "ops": {backend: list[dict]},
                    "strategy": {backend: str},
                    "edit_distance": {backend: int},
                },
                "tokens": [
                    {
                        "row": int,
                        "base_index": int | None,
                        "by_backend": {
                            backend: {
                                "index": int | None,
                                "string": str | None,
                                "lemma": str | None,
                                "upos": str | None,
                                "feats": str | None,
                                "head": int | None,
                                "deprel": str | None,
                            } | None,
                        },
                        "diff": {
                            field: {
                                "agree": bool,
                                "values": {backend: str | int | None},
                            },
                        },
                    },
                ],
                "metrics": {
                    "agreement_rates": {field: {pair: dict}},
                },
            },
        ],
        "summary": {
            "agreement_rates": {field: {pair: dict}},
            "most_disagreed_tokens": list[dict],
            "confusion": {
                "upos": {pair: {tag_a: {tag_b: int}}},
                "deprel": {pair: {tag_a: {tag_b: int}}},
            },
        },
    }

"""

import hashlib
import importlib
import importlib.metadata
import importlib.util
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable, Optional, TypedDict

from cltk.core.cltk_logger import logger
from cltk.core.data_types import (
    CLTKConfig,
    Doc,
    MistralBackendConfig,
    ModelConfig,
    OllamaBackendConfig,
    OpenAIBackendConfig,
    StanzaBackendConfig,
    Word,
)
from cltk.nlp import NLP
from cltk.sentence.utils import (
    extract_sentences_from_boundaries,
    split_sentences_multilang,
)

FieldName = str
COMPARE_FIELDS: tuple[FieldName, ...] = (
    "tokenization",
    "lemma",
    "upos",
    "feats",
    "head",
    "deprel",
)


@dataclass(frozen=True)
class NormalizedToken:
    """Comparable token representation extracted from a CLTK word."""

    index: Optional[int]
    string: Optional[str]
    lemma: Optional[str]
    upos: Optional[str]
    feats: Optional[str]
    head: Optional[int]
    deprel: Optional[str]


@dataclass(frozen=True)
class NormalizedSentence:
    """Comparable sentence representation with normalized tokens."""

    index: int
    text: Optional[str]
    tokens: list[NormalizedToken]


@dataclass(frozen=True)
class AlignmentOp:
    """Single alignment operation between base and other token lists."""

    op: str
    base_index: Optional[int]
    other_index: Optional[int]
    base_token: Optional[str]
    other_token: Optional[str]


@dataclass(frozen=True)
class AlignmentResult:
    """Alignment output with ops and edit cost metadata."""

    strategy: str
    cost: int
    ops: list[AlignmentOp]


class AlignmentRow(TypedDict):
    """Row structure for aligned token comparisons."""

    base_index: Optional[int]
    by_backend: dict[str, dict[str, Any] | None]


def compare_backends(
    language: str,
    text: str,
    backends: list[str],
    *,
    configs: dict[str, dict[str, Any]] | None = None,
    max_sentences: int | None = None,
    max_tokens: int | None = None,
) -> dict[str, Any]:
    """Run multiple NLP backends on the same text and compare their outputs.

    Args:
        language: Glottolog language id.
        text: Raw text to analyze.
        backends: Backend names (e.g., ["stanza", "openai", "ollama"]).
        configs: Optional per-backend config overrides, keyed by backend name.
        max_sentences: Optional cap on number of sentences to compare.
        max_tokens: Optional cap on tokens per sentence.

    Returns:
        A structured report dict. See module docstring for schema.

    """
    if not backends:
        raise ValueError("At least one backend is required.")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must be a non-empty string.")

    configs = configs or {}
    docs_by_backend: dict[str, Doc] = {}
    backend_meta: dict[str, dict[str, Any]] = {}
    for backend in backends:
        cltk_config = _build_cltk_config(
            language=language,
            backend=backend,
            overrides=configs.get(backend),
        )
        logger.info("Running backend '%s' for comparison.", backend)
        nlp = NLP(cltk_config=cltk_config, suppress_banner=True)
        doc = nlp.analyze(text)
        docs_by_backend[backend] = doc
        backend_meta[backend] = _collect_backend_meta(doc)

    return _compare_docs(
        language=language,
        text=text,
        backends=backends,
        docs_by_backend=docs_by_backend,
        backend_meta=backend_meta,
        max_sentences=max_sentences,
        max_tokens=max_tokens,
    )


def report_to_markdown(report: dict[str, Any]) -> str:
    """Render a compare_backends report as Markdown."""
    meta = report.get("meta", {})
    backends = meta.get("backends", [])
    lines: list[str] = []
    lines.append("# Compare Backends Report")
    lines.append("")
    lines.append("## Metadata")
    lines.append("")
    lines.append(f"- Language: {meta.get('language')}")
    lines.append(f"- Backends: {', '.join(backends)}")
    lines.append(f"- Base backend: {meta.get('base_backend')}")
    lines.append(f"- Timestamp: {meta.get('timestamp')}")
    lines.append(f"- Text hash: {meta.get('text_hash')}")
    cltk_version = meta.get("cltk_version")
    if cltk_version:
        lines.append(f"- CLTK version: {cltk_version}")

    summary = report.get("summary", {})
    agreement_rates = summary.get("agreement_rates", {})
    lines.append("")
    lines.append("## Agreement Rates")
    lines.append("")
    lines.append("| Field | Backend Pair | Agree | Total | Rate |")
    lines.append("| --- | --- | --- | --- | --- |")
    for field in COMPARE_FIELDS:
        field_rates = agreement_rates.get(field, {})
        for pair, stats in field_rates.items():
            agree = stats.get("agree", 0)
            total = stats.get("total", 0)
            rate = stats.get("rate")
            rate_str = f"{rate:.3f}" if isinstance(rate, float) else "-"
            lines.append(f"| {field} | {pair} | {agree} | {total} | {rate_str} |")

    lines.append("")
    lines.append("## Top Disagreements")
    lines.append("")
    lines.append("| Sentence | Row | Fields | Tokenization |")
    lines.append("| --- | --- | --- | --- |")
    for item in summary.get("most_disagreed_tokens", []):
        sent_idx = item.get("sentence_index")
        row = item.get("row")
        fields = ", ".join(item.get("fields", []))
        token_pairs = item.get("tokenization", {})
        tokens_str = "; ".join(f"{k}={v}" for k, v in token_pairs.items())
        lines.append(f"| {sent_idx} | {row} | {fields} | {tokens_str} |")

    sentences = report.get("sentences", [])
    if sentences:
        lines.append("")
        lines.append("## Per-Sentence Details")
        for sent in sentences:
            sent_idx = sent.get("index")
            sent_text = sent.get("text") or ""
            lines.append("")
            lines.append(f"### Sentence {sent_idx}")
            if sent_text:
                lines.append("")
                lines.append(sent_text)
            disagreement_rows = [
                tok
                for tok in sent.get("tokens", [])
                if any(
                    not tok.get("diff", {}).get(field, {}).get("agree", True)
                    for field in COMPARE_FIELDS
                )
            ]
            if not disagreement_rows:
                lines.append("")
                lines.append("No disagreements found.")
                continue
            lines.append("")
            lines.append("| Row | Tokenization |")
            lines.append("| --- | --- |")
            for tok in disagreement_rows[:20]:
                row = tok.get("row")
                token_values = (
                    tok.get("diff", {}).get("tokenization", {}).get("values", {})
                )
                tokens_str = "; ".join(f"{k}={v}" for k, v in token_values.items())
                lines.append(f"| {row} | {tokens_str} |")
            if len(disagreement_rows) > 20:
                lines.append("")
                lines.append(
                    f"Truncated {len(disagreement_rows) - 20} additional rows."
                )
    lines.append("")
    return "\n".join(lines)


def write_report(
    report: dict[str, Any],
    out_dir: str,
    basename: str = "compare_backends",
) -> list[str]:
    """Write report JSON, Markdown, and CSV tables to disk."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    json_path = out_path / f"{basename}.json"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True))
    written.append(str(json_path))

    md_path = out_path / f"{basename}.md"
    md_path.write_text(report_to_markdown(report))
    written.append(str(md_path))

    csv_paths = _write_csv_tables(report, out_path, basename)
    written.extend(csv_paths)
    return written


def _compare_docs(
    *,
    language: str,
    text: str,
    backends: list[str],
    docs_by_backend: dict[str, Doc],
    backend_meta: dict[str, dict[str, Any]],
    max_sentences: int | None,
    max_tokens: int | None,
) -> dict[str, Any]:
    """Compare normalized docs and build a full report payload."""
    base_backend = backends[0]
    backend_meta = {backend: backend_meta.get(backend, {}) for backend in backends}
    normalized: dict[str, list[NormalizedSentence]] = {}
    for backend in backends:
        doc = docs_by_backend[backend]
        normalized[backend] = _normalize_doc(
            doc=doc,
            language=language,
            max_sentences=max_sentences,
            max_tokens=max_tokens,
        )

    max_len = max(len(sents) for sents in normalized.values()) if normalized else 0
    sentences_report: list[dict[str, Any]] = []
    all_rows: list[dict[str, Any]] = []
    for i in range(max_len):
        per_backend: dict[str, NormalizedSentence] = {}
        for backend in backends:
            sents = normalized[backend]
            if i < len(sents):
                per_backend[backend] = sents[i]
            else:
                per_backend[backend] = NormalizedSentence(index=i, text=None, tokens=[])
        sentence_report = _compare_sentence(
            sentence_index=i,
            base_backend=base_backend,
            backends=backends,
            sentences=per_backend,
        )
        sentences_report.append(sentence_report)
        for tok in sentence_report["tokens"]:
            row_entry = {
                "sentence_index": i,
                "row": tok["row"],
                "by_backend": tok["by_backend"],
                "diff": tok["diff"],
            }
            all_rows.append(row_entry)

    summary = _build_summary(all_rows, backends)
    meta = {
        "language": language,
        "backends": backends,
        "base_backend": base_backend,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "text_hash": _text_hash(text),
        "cltk_version": _cltk_version(),
    }
    return {
        "meta": meta,
        "backends": backend_meta,
        "sentences": sentences_report,
        "summary": summary,
    }


def _compare_sentence(
    *,
    sentence_index: int,
    base_backend: str,
    backends: list[str],
    sentences: dict[str, NormalizedSentence],
) -> dict[str, Any]:
    """Align tokens for one sentence and compute per-field diffs."""
    base_sentence = sentences[base_backend]
    base_tokens = base_sentence.tokens
    base_strings = [_token_surface(tok) for tok in base_tokens]

    rows: list[AlignmentRow] = []
    for tok in base_tokens:
        rows.append(
            {
                "base_index": tok.index,
                "by_backend": {base_backend: _token_to_dict(tok)},
            }
        )

    mapping = {i: i for i in range(len(base_tokens))}
    align_ops: dict[str, list[dict[str, Any]]] = {}
    align_strategy: dict[str, str] = {}
    align_cost: dict[str, int] = {}
    align_ops[base_backend] = [
        asdict(
            AlignmentOp(
                op="match",
                base_index=i,
                other_index=i,
                base_token=base_strings[i],
                other_token=base_strings[i],
            )
        )
        for i in range(len(base_tokens))
    ]
    align_strategy[base_backend] = "positional"
    align_cost[base_backend] = 0

    for backend in backends:
        if backend == base_backend:
            continue
        other_tokens = sentences[backend].tokens
        other_strings = [_token_surface(tok) for tok in other_tokens]
        alignment = _align_tokens(base_strings, other_strings)
        align_ops[backend] = [asdict(op) for op in alignment.ops]
        align_strategy[backend] = alignment.strategy
        align_cost[backend] = alignment.cost

        base_i = 0
        other_i = 0
        for op in alignment.ops:
            if op.op == "insert":
                insert_at = mapping.get(base_i, len(rows))
                by_backend: dict[str, dict[str, Any] | None] = {}
                new_row: AlignmentRow = {
                    "base_index": None,
                    "by_backend": by_backend,
                }
                for existing in backends:
                    by_backend[existing] = None
                by_backend[backend] = _token_to_dict(other_tokens[other_i])
                rows.insert(insert_at, new_row)
                _shift_mapping(mapping, insert_at)
                other_i += 1
                continue

            row_idx = mapping.get(base_i)
            if row_idx is None:
                row_idx = len(rows)
                empty_by_backend: dict[str, dict[str, Any] | None] = {}
                rows.append({"base_index": None, "by_backend": empty_by_backend})
                mapping[base_i] = row_idx
            if op.op in ("match", "replace"):
                rows[row_idx]["by_backend"][backend] = _token_to_dict(
                    other_tokens[other_i]
                )
                other_i += 1
            elif op.op == "delete":
                rows[row_idx]["by_backend"][backend] = None
            base_i += 1

        _ensure_backend_keys(rows, backends)

    tokens_output: list[dict[str, Any]] = []
    for row_index, row in enumerate(rows):
        token_entry = {
            "row": row_index,
            "base_index": row.get("base_index"),
            "by_backend": row["by_backend"],
            "diff": _diff_row(row["by_backend"], backends),
        }
        tokens_output.append(token_entry)

    metrics = {
        "agreement_rates": _agreement_rates(tokens_output, backends),
    }
    sent_text = _pick_sentence_text(sentences, backends)
    return {
        "index": sentence_index,
        "text": sent_text,
        "alignment": {
            "base_backend": base_backend,
            "ops": align_ops,
            "strategy": align_strategy,
            "edit_distance": align_cost,
        },
        "tokens": tokens_output,
        "metrics": metrics,
    }


def _normalize_doc(
    *,
    doc: Doc,
    language: str,
    max_sentences: int | None,
    max_tokens: int | None,
) -> list[NormalizedSentence]:
    """Normalize a Doc into comparable sentences and tokens."""
    sentences: list[NormalizedSentence] = []
    sentence_texts: list[str] = []
    try:
        sentence_texts = doc.sentence_strings
    except Exception:
        sentence_texts = []

    doc_sentences: list[Any] = []
    try:
        doc_sentences = doc.sentences
    except Exception:
        doc_sentences = []

    if doc_sentences:
        for idx, sent in enumerate(doc_sentences):
            sent_index = sent.index if sent.index is not None else idx
            words = list(sent.words or [])
            tokens = _fill_token_indices([_normalize_word(word) for word in words])
            text = None
            if sent_index < len(sentence_texts):
                text = sentence_texts[sent_index]
            if text is None and tokens:
                text = " ".join(tok.string for tok in tokens if tok.string)
            sentences.append(
                NormalizedSentence(index=sent_index, text=text, tokens=tokens)
            )
    elif doc.words:
        tokens = _fill_token_indices([_normalize_word(word) for word in doc.words])
        text = doc.normalized_text or doc.raw
        if text is None and tokens:
            text = " ".join(tok.string for tok in tokens if tok.string)
        sentences.append(NormalizedSentence(index=0, text=text, tokens=tokens))
    else:
        text = doc.normalized_text or doc.raw or ""
        sentence_strings = _fallback_sentence_split(text, language)
        for idx, sent_text in enumerate(sentence_strings):
            tokens = _fallback_tokenize(sent_text)
            sentences.append(
                NormalizedSentence(index=idx, text=sent_text, tokens=tokens)
            )

    if max_sentences is not None:
        sentences = sentences[:max_sentences]
    if max_tokens is not None:
        trimmed: list[NormalizedSentence] = []
        for sent in sentences:
            trimmed.append(
                NormalizedSentence(
                    index=sent.index,
                    text=sent.text,
                    tokens=sent.tokens[:max_tokens],
                )
            )
        sentences = trimmed
    return sentences


def _fill_token_indices(tokens: list[NormalizedToken]) -> list[NormalizedToken]:
    """Ensure tokens have local indices for alignment."""
    filled: list[NormalizedToken] = []
    for i, token in enumerate(tokens):
        if token.index is not None:
            filled.append(token)
            continue
        filled.append(
            NormalizedToken(
                index=i,
                string=token.string,
                lemma=token.lemma,
                upos=token.upos,
                feats=token.feats,
                head=token.head,
                deprel=token.deprel,
            )
        )
    return filled


def _normalize_word(word: Word) -> NormalizedToken:
    """Extract normalized fields from a CLTK Word."""
    token_str = _normalize_str(getattr(word, "string", None))
    if token_str is None:
        for attr in ("text", "form"):
            token_str = _normalize_str(getattr(word, attr, None))
            if token_str is not None:
                break
    dep_obj = None
    for attr in (
        "dependency_relation",
        "deprel",
        "dep_rel",
        "relation",
        "ud_relation",
        "dependency_label",
        "dep_label",
    ):
        dep_obj = getattr(word, attr, None)
        if dep_obj is not None:
            break
    return NormalizedToken(
        index=_as_int(getattr(word, "index_token", None)),
        string=token_str,
        lemma=_normalize_str(getattr(word, "lemma", None)),
        upos=_normalize_tag(getattr(word, "upos", None)),
        feats=_normalize_feats(getattr(word, "features", None)),
        head=_normalize_head(word),
        deprel=_normalize_deprel(dep_obj),
    )


def _normalize_str(value: Any) -> Optional[str]:
    """Normalize a value to a stripped string."""
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    try:
        s = str(value).strip()
        return s if s else None
    except Exception:
        return None


def _normalize_tag(value: Any) -> Optional[str]:
    """Normalize a UD tag-like value to a string."""
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    for attr in ("tag", "code", "name", "value"):
        v = getattr(value, attr, None)
        if isinstance(v, str) and v:
            return v
    try:
        s = str(value)
        return s if s else None
    except Exception:
        return None


def _normalize_feats(value: Any) -> Optional[str]:
    """Normalize feature bundles to a stable string form."""
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        return s if s and s != "_" else None
    if isinstance(value, dict):
        dict_pairs = [(str(k), str(v)) for k, v in value.items() if v is not None]
        if not dict_pairs:
            return None
        dict_pairs.sort(key=lambda kv: (kv[0], kv[1]))
        return "|".join(f"{k}={v}" for k, v in dict_pairs)
    tags = getattr(value, "features", None)
    if tags is None and isinstance(value, Iterable):
        tags = list(value)
    tag_pairs: list[tuple[str, str]] = []
    if tags:
        for tag in tags:
            k = getattr(tag, "key", None)
            v = getattr(tag, "value", None)
            if isinstance(k, str) and isinstance(v, str) and k and v:
                tag_pairs.append((k, v))
    if not tag_pairs:
        return None
    tag_pairs.sort(key=lambda kv: (kv[0], kv[1]))
    return "|".join(f"{k}={v}" for k, v in tag_pairs)


def _normalize_head(word: Word) -> Optional[int]:
    """Normalize head/governor index to an int."""
    for attr in ("governor", "head", "head_index", "head_id"):
        val = getattr(word, attr, None)
        if val is not None:
            return _as_int(val)
    return None


def _normalize_deprel(value: Any) -> Optional[str]:
    """Normalize dependency relation to a string."""
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    for attr in ("code", "ud", "name", "value"):
        v = getattr(value, attr, None)
        if isinstance(v, str) and v:
            return v
    try:
        s = str(value)
        return s if s else None
    except Exception:
        return None


def _fallback_sentence_split(text: str, language: str) -> list[str]:
    """Split text into sentences when no boundaries exist."""
    if not text:
        return []
    try:
        boundaries = split_sentences_multilang(text, language)
    except Exception:
        boundaries = []
    if boundaries:
        return extract_sentences_from_boundaries(text, boundaries)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines if lines else [text.strip()]


def _fallback_tokenize(text: str) -> list[NormalizedToken]:
    """Tokenize text by whitespace as a fallback."""
    if not text:
        return []
    tokens: list[NormalizedToken] = []
    for i, token in enumerate(text.split()):
        tokens.append(
            NormalizedToken(
                index=i,
                string=token,
                lemma=None,
                upos=None,
                feats=None,
                head=None,
                deprel=None,
            )
        )
    return tokens


def _align_tokens(base: list[str], other: list[str]) -> AlignmentResult:
    """Align token strings using positional or DP alignment."""
    if base == other:
        positional_ops = [
            AlignmentOp(
                op="match",
                base_index=i,
                other_index=i,
                base_token=base[i],
                other_token=other[i],
            )
            for i in range(len(base))
        ]
        return AlignmentResult(strategy="positional", cost=0, ops=positional_ops)

    n = len(base)
    m = len(other)
    dp: list[list[int]] = [[0] * (m + 1) for _ in range(n + 1)]
    back: list[list[Optional[str]]] = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i
        back[i][0] = "delete"
    for j in range(1, m + 1):
        dp[0][j] = j
        back[0][j] = "insert"
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost_sub = dp[i - 1][j - 1] + (0 if base[i - 1] == other[j - 1] else 1)
            cost_del = dp[i - 1][j] + 1
            cost_ins = dp[i][j - 1] + 1
            if cost_sub <= cost_del and cost_sub <= cost_ins:
                dp[i][j] = cost_sub
                back[i][j] = "sub"
            elif cost_del <= cost_ins:
                dp[i][j] = cost_del
                back[i][j] = "delete"
            else:
                dp[i][j] = cost_ins
                back[i][j] = "insert"

    ops: list[AlignmentOp] = []
    i = n
    j = m
    while i > 0 or j > 0:
        move = back[i][j]
        if move == "sub":
            op = "match" if base[i - 1] == other[j - 1] else "replace"
            ops.append(
                AlignmentOp(
                    op=op,
                    base_index=i - 1,
                    other_index=j - 1,
                    base_token=base[i - 1],
                    other_token=other[j - 1],
                )
            )
            i -= 1
            j -= 1
        elif move == "delete":
            ops.append(
                AlignmentOp(
                    op="delete",
                    base_index=i - 1,
                    other_index=None,
                    base_token=base[i - 1],
                    other_token=None,
                )
            )
            i -= 1
        elif move == "insert":
            ops.append(
                AlignmentOp(
                    op="insert",
                    base_index=None,
                    other_index=j - 1,
                    base_token=None,
                    other_token=other[j - 1],
                )
            )
            j -= 1
        else:
            break
    ops.reverse()
    return AlignmentResult(strategy="dp", cost=dp[n][m], ops=ops)


def _diff_row(
    by_backend: dict[str, dict[str, Any] | None],
    backends: list[str],
) -> dict[str, dict[str, Any]]:
    """Compute per-field agreement for one aligned row."""
    diff: dict[str, dict[str, Any]] = {}
    for field in COMPARE_FIELDS:
        values: dict[str, Any] = {}
        for backend in backends:
            token = by_backend.get(backend)
            if token is None:
                values[backend] = None
            elif field == "tokenization":
                values[backend] = token.get("string")
            else:
                values[backend] = token.get(field)
        unique = {v for v in values.values()}
        agree = len(unique) <= 1
        diff[field] = {"agree": agree, "values": values}
    return diff


def _agreement_rates(
    tokens: list[dict[str, Any]],
    backends: list[str],
) -> dict[str, dict[str, dict[str, Any]]]:
    """Compute pairwise agreement rates across aligned rows."""
    rates: dict[str, dict[str, dict[str, Any]]] = {
        field: {} for field in COMPARE_FIELDS
    }
    for a, b in combinations(backends, 2):
        pair = _pair_key(a, b)
        for field in COMPARE_FIELDS:
            agree = 0
            total = 0
            for tok in tokens:
                a_token = tok["by_backend"].get(a)
                b_token = tok["by_backend"].get(b)
                if not _field_comparable(field, a_token, b_token):
                    continue
                total += 1
                a_val = _field_value(field, a_token)
                b_val = _field_value(field, b_token)
                if a_val == b_val:
                    agree += 1
            rate = (agree / total) if total else None
            rates[field][pair] = {"agree": agree, "total": total, "rate": rate}
    return rates


def _field_comparable(
    field: FieldName,
    a_token: dict[str, Any] | None,
    b_token: dict[str, Any] | None,
) -> bool:
    """Check whether a field is comparable for a token pair."""
    if field == "tokenization":
        return (a_token is not None) or (b_token is not None)
    return (a_token is not None) and (b_token is not None)


def _field_value(field: FieldName, token: dict[str, Any] | None) -> Any:
    """Extract a comparable field value from a token dict."""
    if token is None:
        return None
    if field == "tokenization":
        return token.get("string")
    return token.get(field)


def _build_summary(
    rows: list[dict[str, Any]],
    backends: list[str],
) -> dict[str, Any]:
    """Aggregate overall metrics and confusion tables."""
    summary = {
        "agreement_rates": _agreement_rates(rows, backends),
        "most_disagreed_tokens": _top_disagreements(rows, backends),
        "confusion": {
            "upos": _confusion(rows, backends, field="upos"),
            "deprel": _confusion(rows, backends, field="deprel"),
        },
    }
    return summary


def _top_disagreements(
    rows: list[dict[str, Any]],
    backends: list[str],
    *,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Return the highest-disagreement rows for summary."""
    scored: list[tuple[int, dict[str, Any]]] = []
    for row in rows:
        diff = row.get("diff", {})
        fields = []
        score = 0
        for field in COMPARE_FIELDS:
            values = diff.get(field, {}).get("values", {})
            unique = {v for v in values.values()}
            if len(unique) > 1:
                fields.append(field)
                score += len(unique) - 1
        if score:
            scored.append(
                (
                    score,
                    {
                        "sentence_index": row.get("sentence_index"),
                        "row": row.get("row"),
                        "fields": fields,
                        "tokenization": diff.get("tokenization", {}).get("values", {}),
                        "values": {
                            field: diff.get(field, {}).get("values", {})
                            for field in COMPARE_FIELDS
                        },
                    },
                )
            )
    scored.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in scored[:limit]]


def _confusion(
    rows: list[dict[str, Any]],
    backends: list[str],
    *,
    field: FieldName,
) -> dict[str, dict[str, dict[str, int]]]:
    """Build a confusion-like table for a field."""
    table: dict[str, dict[str, dict[str, int]]] = {}
    for a, b in combinations(backends, 2):
        pair = _pair_key(a, b)
        pair_table: dict[str, dict[str, int]] = {}
        for row in rows:
            a_token = row["by_backend"].get(a)
            b_token = row["by_backend"].get(b)
            if a_token is None or b_token is None:
                continue
            a_val = a_token.get(field)
            b_val = b_token.get(field)
            if not a_val or not b_val or a_val == b_val:
                continue
            pair_table.setdefault(str(a_val), {})
            pair_table[str(a_val)][str(b_val)] = (
                pair_table[str(a_val)].get(str(b_val), 0) + 1
            )
        table[pair] = pair_table
    return table


def _write_csv_tables(
    report: dict[str, Any],
    out_path: Path,
    basename: str,
) -> list[str]:
    """Write CSV tables for summary metrics and disagreements."""
    written: list[str] = []
    pd = _optional_pandas()

    agreement_rows: list[dict[str, Any]] = []
    for field, pairs in report.get("summary", {}).get("agreement_rates", {}).items():
        for pair, stats in pairs.items():
            agreement_rows.append(
                {
                    "field": field,
                    "backend_pair": pair,
                    "agree": stats.get("agree", 0),
                    "total": stats.get("total", 0),
                    "rate": stats.get("rate"),
                }
            )
    written.extend(
        _write_csv(out_path / f"{basename}_agreement.csv", agreement_rows, pd=pd)
    )

    for field in ("upos", "deprel"):
        rows: list[dict[str, Any]] = []
        confusion = report.get("summary", {}).get("confusion", {}).get(field, {})
        for pair, matrix in confusion.items():
            for left, right_map in matrix.items():
                for right, count in right_map.items():
                    rows.append(
                        {
                            "backend_pair": pair,
                            "left": left,
                            "right": right,
                            "count": count,
                        }
                    )
        written.extend(
            _write_csv(out_path / f"{basename}_confusion_{field}.csv", rows, pd=pd)
        )

    disagreements = report.get("summary", {}).get("most_disagreed_tokens", [])
    disagreement_rows: list[dict[str, Any]] = []
    for item in disagreements:
        disagreement_rows.append(
            {
                "sentence_index": item.get("sentence_index"),
                "row": item.get("row"),
                "fields": ",".join(item.get("fields", [])),
                "tokenization": "; ".join(
                    f"{k}={v}" for k, v in item.get("tokenization", {}).items()
                ),
            }
        )
    written.extend(
        _write_csv(
            out_path / f"{basename}_top_disagreements.csv",
            disagreement_rows,
            pd=pd,
        )
    )
    return written


def _write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    *,
    pd: Optional[Any],
) -> list[str]:
    """Write rows to a CSV file using pandas if available."""
    if pd is not None:
        df = pd.DataFrame(rows)
        df.to_csv(path, index=False)
        return [str(path)]
    import csv

    if not rows:
        path.write_text("")
        return [str(path)]
    with path.open("w", newline="") as fh:
        fieldnames = sorted({key for row in rows for key in row.keys()})
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return [str(path)]


def _optional_pandas() -> Optional[Any]:
    """Return pandas if installed, otherwise None."""
    if importlib.util.find_spec("pandas") is None:
        return None
    return importlib.import_module("pandas")


def _build_cltk_config(
    *,
    language: str,
    backend: str,
    overrides: Optional[dict[str, Any]],
) -> CLTKConfig:
    """Build a CLTKConfig for a specific backend with overrides."""
    overrides = overrides or {}
    backend_config: Optional[ModelConfig] = None
    if backend == "stanza":
        backend_config = StanzaBackendConfig(**overrides) if overrides else None
        return CLTKConfig(
            language_code=language,
            backend=backend,
            suppress_banner=True,
            stanza=backend_config,
        )
    if backend == "openai":
        backend_config = OpenAIBackendConfig(**overrides) if overrides else None
        return CLTKConfig(
            language_code=language,
            backend=backend,
            suppress_banner=True,
            openai=backend_config,
        )
    if backend == "mistral":
        backend_config = MistralBackendConfig(**overrides) if overrides else None
        return CLTKConfig(
            language_code=language,
            backend=backend,
            suppress_banner=True,
            mistral=backend_config,
        )
    if backend in ("ollama", "ollama-cloud"):
        backend_config = OllamaBackendConfig(**overrides) if overrides else None
        return CLTKConfig(
            language_code=language,
            backend=backend,
            suppress_banner=True,
            ollama=backend_config,
        )
    raise ValueError(f"Unsupported backend: {backend}")


def _collect_backend_meta(doc: Doc) -> dict[str, Any]:
    """Collect backend metadata from a Doc."""
    backend_config = doc.metadata.get("backend_config")
    if backend_config is not None and hasattr(backend_config, "model_dump"):
        backend_config = backend_config.model_dump()
    metadata: dict[str, Any] = {
        "backend": getattr(doc, "backend", None),
    }
    meta: dict[str, Any] = {
        "model": getattr(doc, "model", None),
        "backend_config": backend_config,
        "metadata": metadata,
    }
    stanza_package = doc.metadata.get("stanza_package")
    if stanza_package:
        metadata["stanza_package"] = stanza_package
    return meta


def _token_surface(token: NormalizedToken) -> str:
    """Choose the best surface string for alignment."""
    return token.string or token.lemma or ""


def _token_to_dict(token: NormalizedToken) -> dict[str, Any]:
    """Serialize a normalized token to a dict."""
    return asdict(token)


def _pick_sentence_text(
    sentences: dict[str, NormalizedSentence],
    backends: list[str],
) -> Optional[str]:
    """Pick the first available sentence text among backends."""
    for backend in backends:
        text = sentences[backend].text
        if text:
            return text
    return None


def _shift_mapping(mapping: dict[int, int], insert_at: int) -> None:
    """Shift row indices after inserting an alignment row."""
    for key, idx in list(mapping.items()):
        if idx >= insert_at:
            mapping[key] = idx + 1


def _ensure_backend_keys(
    rows: list[AlignmentRow],
    backends: list[str],
) -> None:
    """Ensure each row has keys for all backends."""
    for row in rows:
        by_backend = row["by_backend"]
        for backend in backends:
            by_backend.setdefault(backend, None)


def _pair_key(a: str, b: str) -> str:
    """Format a stable backend pair key."""
    return f"{a} vs {b}"


def _as_int(value: Any) -> Optional[int]:
    """Safely coerce a value to int."""
    try:
        return int(value)
    except Exception:
        return None


def _text_hash(text: str) -> str:
    """Return a short hash for the input text."""
    return hashlib.sha1(text.encode("utf-8"), usedforsecurity=False).hexdigest()[:10]


def _cltk_version() -> Optional[str]:
    """Return the installed CLTK version when available."""
    try:
        return importlib.metadata.version("cltk")
    except Exception:
        return None
