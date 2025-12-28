"""Utilities for resolving CLTK language data.

This module resolves user-supplied keys (ISO codes, names, Glottolog IDs) into
``(Language, Optional[Dialect])`` pairs using the curated language data in
``languages.py``.
"""

from typing import Any, Literal, Optional

from cltk.core.cltk_logger import logger
from cltk.core.data_types import Dialect, Language
from cltk.core.logging_utils import glog
from cltk.languages.languages import LANGUAGES

HISTORIC_CUTOFF_YEAR: int = 1700
_HISTORIC_MODIFIERS: set[str] = {
    "ancient",
    "old",
    "middle",
    "classical",
    "late",
    "early",
    "medieval",
    "archaic",
    "literary",
    "demotic",
}


def _norm(s: str) -> str:
    """Normalize whitespace and case for robust comparisons."""
    return " ".join(s.lower().split())


def _is_historic_like(L: Language, cutoff: int = HISTORIC_CUTOFF_YEAR) -> bool:
    """Return True if a language looks historic/ancient per simple heuristics.

    Heuristics consider endangerment, explicit tokens like "ancient/old/middle",
    and an earliest timespan prior to ``cutoff``.
    """
    try:
        if getattr(L, "status", None) in {"extinct", "unattested"}:
            return True
    except Exception:
        pass
    ts = getattr(L, "timespan", None)
    if ts:
        years = [
            v
            for v in (getattr(ts, "start", None), getattr(ts, "end", None))
            if isinstance(v, int)
        ]
        if years and min(years) <= cutoff:
            return True
    name_tokens = set(_norm(L.name).split())
    if name_tokens & _HISTORIC_MODIFIERS:
        return True
    for nv in getattr(L, "alt_names", []):
        if set(_norm(nv.value).split()) & _HISTORIC_MODIFIERS:
            return True
    return False


def _historic_rank(
    L: Language, cutoff: int = HISTORIC_CUTOFF_YEAR
) -> tuple[int, int, int]:
    """Return a tuple scoring how plausibly historic a language is.

    Higher tuples (by lexicographic order) indicate stronger historicity.
    """
    is_hist = 1 if _is_historic_like(L, cutoff=cutoff) else 0
    has_mod = 1 if (set(_norm(L.name).split()) & _HISTORIC_MODIFIERS) else 0
    ts = getattr(L, "timespan", None)
    years = [
        v
        for v in (getattr(ts, "start", None), getattr(ts, "end", None))
        if isinstance(v, int)
    ]
    earliest = min(years) if years else 9999
    return (is_hist, has_mod, -earliest)


def _build_indices() -> (
    dict[
        Literal["by_iso", "by_name_lang", "by_name_dialect", "by_dialect"],
        dict[str, Any],
    ]
):
    """Build lookup indices for languages and dialects from ``LANGUAGES``.

    Indices built:
      - ``by_iso``: ISO -> language glottocode
      - ``by_name_lang``: lowercased language name/alt-name -> [language glottocode]
      - ``by_name_dialect``: lowercased dialect name -> [dialect glottocode]
      - ``by_dialect``: dialect glottocode -> parent language glottocode
    """
    by_iso: dict[str, str] = {}
    by_name_lang: dict[str, list[str]] = {}
    by_name_dialect: dict[str, list[str]] = {}
    by_dialect: dict[str, str] = {}
    for g, L in LANGUAGES.items():
        if L.iso:
            by_iso[L.iso.lower()] = g
        by_name_lang.setdefault(L.name.lower(), []).append(g)
        for nv in L.alt_names:
            by_name_lang.setdefault(nv.value.lower(), []).append(g)
        for d in L.dialects:
            if not d.glottolog_id:
                continue
            by_dialect[d.glottolog_id] = g
            by_name_dialect.setdefault(d.name.lower(), []).append(d.glottolog_id)
    logger.info(
        f"Built indices: by_iso={len(by_iso)} entries, "
        f"by_name_lang_keys={len(by_name_lang)}, "
        f"by_name_dialect_keys={len(by_name_dialect)}, "
        f"by_dialect={len(by_dialect)}"
    )
    return {
        "by_iso": by_iso,
        "by_name_lang": by_name_lang,
        "by_name_dialect": by_name_dialect,
        "by_dialect": by_dialect,
    }


def get_dialect(key: str) -> tuple[Language, Dialect]:
    """Return ``(Language, Dialect)`` by dialect glottocode or exact dialect name.

    Dialect resolution requires a Glottolog dialect ID or an exact dialect name.
    ISO 639-3 codes are language-level and cannot identify dialects.

    Args:
      key: Dialect glottocode or exact dialect name.

    Returns:
      A tuple of (parent ``Language``, matching ``Dialect``).

    Raises:
      KeyError: If the key refers to a language, or no dialect can be found
        (with hints on ambiguous names).

    """
    logger.debug(f"Looking up dialect for key='{key}'")
    langs: dict[str, Language] = LANGUAGES
    idx = _build_indices()

    k = key.lower()

    if key in langs or k in langs:
        msg = f"'{key}' is a language glottocode. Use get_language('{key}')."
        glog(k).info(msg)
        raise KeyError(msg)

    if k in idx["by_iso"]:
        lang_id = idx["by_iso"][k]
        lang = langs[lang_id]
        msg = (
            f"'{key}' resolves to the language {lang.name} (glottolog_id={lang_id}). "
            f"Use get_language('{key}') for languages."
        )
        glog(lang_id).info(msg)
        raise KeyError(msg)

    # Direct dialect glottocode
    parent = idx["by_dialect"].get(key) or idx["by_dialect"].get(k)
    if parent:
        lang = langs[parent]
        target_id = key if key in idx["by_dialect"] else k
        for d in lang.dialects:
            if d.glottolog_id == target_id:
                glog(key).debug(
                    f"Found dialect by id '{key}' under language '{lang.name}'"
                )
                return lang, d
        # Very unlikely: index points to parent but dialect not found; scan as fallback
        for L in langs.values():
            for d in L.dialects:
                if d.glottolog_id == target_id:
                    glog(key).debug(
                        f"Found dialect by id '{key}' under language '{L.name}' (fallback scan)"
                    )
                    return L, d
        msg = f"Dialect id '{key}' indexed but not found in model data."
        logger.error(msg)
        raise KeyError(msg)

    # Exact dialect name (lowercased) may map to multiple dialect ids
    hits = idx["by_name_dialect"].get(k, [])
    if hits:
        if len(hits) == 1:
            did = hits[0]
            parent = idx["by_dialect"].get(did)
            if parent and parent in langs:
                lang = langs[parent]
                dialect_match = next(
                    (d for d in lang.dialects if d.glottolog_id == did), None
                )
                if dialect_match:
                    glog(did).debug(
                        f"Found dialect by name '{key}' -> {dialect_match.name} (id={did}) under '{lang.name}'"
                    )
                    return lang, dialect_match
        # Ambiguous name → ask for a glottocode, list a few options
        options: list[str] = []
        for did in hits[:5]:
            p = idx["by_dialect"].get(did)
            if p and p in langs:
                lang = langs[p]
                dname = next(
                    (d.name for d in lang.dialects if d.glottolog_id == did), did
                )
                options.append(
                    f"{dname} (dialect id={did}, parent={lang.name}, glottolog_id={p})"
                )
        msg = (
            f"Ambiguous dialect name '{key}'. Please specify a dialect glottocode. "
            + ("Options: " + "; ".join(options) if options else "No options available.")
        )
        glog(key).info(msg)
        raise KeyError(msg)

    msg = f"No dialect found for '{key}'"
    logger.error(msg)
    raise KeyError(msg)


def get_language(lang_id: str) -> tuple[Language, Optional[Dialect]]:
    """Resolve a language or dialect key.

    Args:
      lang_id: Language glottocode/ISO/name or dialect glottocode/name.

    Returns:
      (``Language``, ``None``) for a language; (``Language``, ``Dialect``) for a
      dialect.

    Raises:
      KeyError: If nothing matches (or name is ambiguous without a glottocode).

    """
    logger.debug(f"Resolving languoid for key='{lang_id}'")

    langs: dict[str, Language] = LANGUAGES
    idx = _build_indices()

    k = lang_id.strip()
    if not k:
        msg = "Language identifier cannot be empty."
        logger.error(msg)
        raise KeyError(msg)
    k_lower = k.lower()

    # 1) Exact language glottocode
    if k in langs:
        L = langs[k]
        glog(k).debug(f"Resolved language by glottocode: {k} -> {L.name}")
        return L, None
    if k_lower in langs:
        L = langs[k_lower]
        glog(k_lower).debug(
            f"Resolved language by glottocode: {k} -> {L.name} (normalized)"
        )
        return L, None

    # 2) Exact dialect glottocode
    parent = idx["by_dialect"].get(k) or idx["by_dialect"].get(k_lower)
    if parent:
        lang = langs[parent]
        target_id = k if k in idx["by_dialect"] else k_lower
        for d in lang.dialects:
            if d.glottolog_id == target_id:
                glog(target_id).debug(
                    f"Resolved dialect by glottocode: {k} -> {d.name} (parent={lang.name})"
                )
                return lang, d
        # Fallback scan (should not be needed)
        for L in langs.values():
            for d in L.dialects:
                if d.glottolog_id == target_id:
                    glog(target_id).debug(
                        f"Resolved dialect by glottocode via fallback scan: {k} -> {d.name} (parent={L.name})"
                    )
                    return L, d
        msg = f"Dialect id '{k}' indexed but not found in model data."
        logger.error(msg)
        raise KeyError(msg)

    # 3) ISO (language only)
    g = idx["by_iso"].get(k_lower)
    if g:
        L = langs[g]
        glog(g).debug(f"Resolved language by ISO: {k} -> {L.name} (glottolog_id={g})")
        return L, None

    # 4) Exact language name/alt-name (may be ambiguous) → prefer historic
    hits_lang: list[str] = idx["by_name_lang"].get(k_lower, [])
    if hits_lang:
        if len(hits_lang) == 1:
            g0 = hits_lang[0]
            L = langs[g0]
            glog(g0).debug(
                f"Resolved language by name: '{k}' -> {L.name} (glottolog_id={g0})"
            )
            return L, None
        cands = [langs[gx] for gx in hits_lang if gx in langs]
        cands.sort(key=_historic_rank, reverse=True)
        best = cands[0]
        glog(best.glottolog_id).info(
            f"Ambiguous language name '{k}' matched {len(cands)} entries; "
            f"selecting '{best.name}' (glottolog_id={best.glottolog_id}) by historic preference."
        )
        return best, None

    # 5) Exact dialect name (may be ambiguous)
    hits_dia: list[str] = idx["by_name_dialect"].get(k_lower, [])
    if hits_dia:
        if len(hits_dia) == 1:
            did = hits_dia[0]
            parent = idx["by_dialect"].get(did)
            if parent and parent in langs:
                lang = langs[parent]
                dialect_match = next(
                    (d for d in lang.dialects if d.glottolog_id == did), None
                )
                if dialect_match:
                    glog(did).debug(
                        f"Resolved dialect by name: '{k}' -> {dialect_match.name} (id={did}, parent={lang.name})"
                    )
                    return lang, dialect_match
        # Ambiguous dialect name → ask for a glottocode, list options
        options: list[str] = []
        for did in hits_dia[:5]:
            p = idx["by_dialect"].get(did)
            if p and p in langs:
                lang = langs[p]
                dname = next(
                    (d.name for d in lang.dialects if d.glottolog_id == did), did
                )
                options.append(
                    f"{dname} (dialect id={did}, parent={lang.name}, glottolog_id={p})"
                )
        msg = f"Ambiguous dialect name '{k}'. Please specify a dialect glottocode. " + (
            "Options: " + "; ".join(options) if options else "No options available."
        )
        glog(k).info(msg)
        raise KeyError(msg)

    # 6) No match
    msg = f"No language or dialect found for '{k}'"
    logger.error(msg)
    raise KeyError(msg)
