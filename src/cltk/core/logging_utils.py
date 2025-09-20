"""Helpers for structured logging context.

Small utilities to produce a contextual logger adapter from common CLTK
containers without introducing circular imports in ``cltk.core.cltk_logger``.
"""

import hashlib
import logging
from typing import Optional, Protocol

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import Doc


class HasGlottologId(Protocol):
    glottolog_id: Optional[str]


def _maybe_hash(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    try:
        return hashlib.sha1(text.encode("utf-8"), usedforsecurity=False).hexdigest()[
            :10
        ]
    except Exception:
        return None


def _glottolog_id_from_doc(doc: Doc) -> Optional[str]:
    try:
        if doc.dialect and doc.dialect.glottolog_id:
            return doc.dialect.glottolog_id
        return doc.language.glottolog_id
    except Exception:
        return None


def bind_from_doc(
    doc: Doc,
    *,
    sentence_idx: Optional[int] = None,
    prompt_version: Optional[str] = None,
) -> logging.LoggerAdapter:
    """Return a structured logger bound with context derived from ``doc``.

    Binds the following fields when available:
      - doc_id: sha1 of ``normalized_text`` (or ``raw``) truncated to 10 chars
      - sentence_idx: provided by caller
      - model: ``doc.model`` string
      - glottolog_id: from ``doc.dialect`` or ``doc.language``
      - prompt_version: provided by caller
    """
    doc_id = _maybe_hash(doc.normalized_text or doc.raw)
    model = str(doc.model) if getattr(doc, "model", None) else None
    gid = _glottolog_id_from_doc(doc)
    return bind_context(
        doc_id=doc_id,
        sentence_idx=sentence_idx,
        model=model,
        glottolog_id=gid,
        prompt_version=prompt_version,
    )


def plog(pipeline_like: HasGlottologId) -> logging.LoggerAdapter:
    """Return a contextual logger for a Pipeline-like object.

    Extracts ``glottolog_id`` from the object if present and binds it for
    consistent, filterable logs during pipeline initialization.
    """
    gid = getattr(pipeline_like, "glottolog_id", None)
    return bind_context(glottolog_id=gid)


def glog(glottolog_id: Optional[str]) -> logging.LoggerAdapter:
    """Return a logger bound with a specific ``glottolog_id``.

    Small alias used by language/glottolog operations for brevity.
    """
    return bind_context(glottolog_id=glottolog_id)
