"""Provenance helpers for reproducible CLTK annotations."""

from __future__ import annotations

import hashlib
import json
import platform as _platform
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel

_SENSITIVE_KEYS = {"api_key", "token", "password", "secret", "key"}


class ProvenanceRecord(BaseModel):
    """Compact record describing how annotations were produced."""

    id: str
    created_at: datetime
    language: Optional[str] = None
    backend: Optional[str] = None
    process: Optional[str] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    prompt_version: Optional[str] = None
    prompt_digest: Optional[str] = None
    config_digest: Optional[str] = None
    config: Optional[dict[str, Any]] = None
    cltk_version: Optional[str] = None
    python_version: Optional[str] = None
    platform: Optional[str] = None
    notes: Optional[dict[str, Any]] = None

    model_config = {"arbitrary_types_allowed": True}


def canonical_json(obj: Any) -> str:
    """Return a stable JSON string with sorted keys and no whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_hex(text: str) -> str:
    """Return a SHA256 hex digest for the given text."""
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def make_provenance_id(prefix: str = "prov_") -> str:
    """Return a short-ish unique identifier for provenance records."""
    return f"{prefix}{uuid.uuid4().hex}"


def _redact_config(config: dict[str, Any]) -> dict[str, Any]:
    """Drop sensitive config keys before persistence."""
    redacted: dict[str, Any] = {}
    for key, value in config.items():
        lowered = str(key).lower()
        if any(token in lowered for token in _SENSITIVE_KEYS):
            continue
        if isinstance(value, dict):
            redacted[key] = _redact_config(value)
        else:
            redacted[key] = value
    return redacted


def normalize_config(config: Any) -> Optional[dict[str, Any]]:
    """Normalize backend config into a JSON-friendly, redacted dict."""
    if config is None:
        return None
    data: Optional[dict[str, Any]]
    if isinstance(config, BaseModel):
        data = config.model_dump(exclude_none=True)
    elif isinstance(config, dict):
        data = dict(config)
    else:
        data = {"value": str(config)}
    data = _redact_config(data)
    return data or None


def extract_doc_config(doc: Any) -> Optional[dict[str, Any]]:
    """Pull a safe config snapshot from a Doc-like object."""
    meta = getattr(doc, "metadata", None)
    cfg: Any = None
    if isinstance(meta, dict):
        cfg = meta.get("backend_config")
    config = normalize_config(cfg)
    if isinstance(meta, dict):
        stanza_package = meta.get("stanza_package")
        if stanza_package:
            if config is None:
                config = {}
            config["stanza_package"] = stanza_package
    return config


def build_provenance_record(
    *,
    language: Optional[str] = None,
    backend: Optional[str] = None,
    process: Optional[str] = None,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    prompt_version: Optional[str] = None,
    prompt_text: Optional[str] = None,
    prompt_digest: Optional[str] = None,
    config: Optional[dict[str, Any]] = None,
    config_digest: Optional[str] = None,
    cltk_version: Optional[str] = None,
    python_version: Optional[str] = None,
    platform: Optional[str] = None,
    notes: Optional[dict[str, Any]] = None,
    created_at: Optional[datetime] = None,
    record_id: Optional[str] = None,
) -> ProvenanceRecord:
    """Build a ProvenanceRecord, computing digests when needed."""
    if created_at is None:
        created_at = datetime.now(timezone.utc)
    if record_id is None:
        record_id = make_provenance_id()
    if prompt_digest is None and prompt_text:
        prompt_digest = sha256_hex(prompt_text)
    if config_digest is None and config:
        try:
            config_digest = sha256_hex(canonical_json(config))
        except Exception:
            config_digest = None
    if cltk_version is None:
        try:
            import cltk

            cltk_version = cltk.__version__
        except Exception:
            cltk_version = None
    if python_version is None:
        try:
            python_version = _platform.python_version()
        except Exception:
            python_version = None
    if platform is None:
        try:
            platform = _platform.platform()
        except Exception:
            platform = None
    return ProvenanceRecord(
        id=record_id,
        created_at=created_at,
        language=language,
        backend=backend,
        process=process,
        model=model,
        provider=provider,
        prompt_version=prompt_version,
        prompt_digest=prompt_digest,
        config_digest=config_digest,
        config=config,
        cltk_version=cltk_version,
        python_version=python_version,
        platform=platform,
        notes=notes,
    )


def add_provenance_record(
    doc: Any, record: ProvenanceRecord, *, set_default: bool = False
) -> str:
    """Add a provenance record to a Doc-like object and return its id."""
    try:
        prov_map = getattr(doc, "provenance", None)
        if prov_map is None:
            doc.provenance = {}
            prov_map = doc.provenance
        if isinstance(prov_map, dict):
            prov_map[record.id] = record
        if set_default and not getattr(doc, "default_provenance_id", None):
            doc.default_provenance_id = record.id
    except Exception:
        pass
    return record.id


def get_token_provenance(
    word: Any, field: str, doc: Optional[Any] = None
) -> Optional[ProvenanceRecord]:
    """Return the provenance record for a word field, if resolvable."""
    try:
        sources = getattr(word, "annotation_sources", None) or {}
        prov_id = sources.get(field)
    except Exception:
        prov_id = None
    if not prov_id:
        return None
    doc_obj = doc or getattr(word, "doc", None) or getattr(word, "_doc", None)
    if doc_obj is None:
        return None
    prov_map = getattr(doc_obj, "provenance", None)
    if isinstance(prov_map, dict):
        return prov_map.get(prov_id)
    return None


def get_sentence_provenance(
    sentence: Any, field: str, doc: Optional[Any] = None
) -> Optional[ProvenanceRecord]:
    """Return the provenance record for a sentence field, if resolvable."""
    try:
        sources = getattr(sentence, "annotation_sources", None) or {}
        prov_id = sources.get(field)
    except Exception:
        prov_id = None
    if not prov_id:
        return None
    doc_obj = doc or getattr(sentence, "doc", None) or getattr(sentence, "_doc", None)
    if doc_obj is None:
        prov_map = getattr(sentence, "provenance", None)
    else:
        prov_map = getattr(doc_obj, "provenance", None)
    if isinstance(prov_map, dict):
        return prov_map.get(prov_id)
    return None
