from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files as pkg_files
from pathlib import Path
from typing import Any, Literal, Optional

from pydantic import TypeAdapter

from cltk.core.cltk_logger import logger
from cltk.core.data_types_v3 import Dialect, Language

# If you ship the JSON with the package, place it under cltk/languages/
_DEFAULT_RESOURCE = "glottolog.json"


def _read_bytes(path: Optional[Path]) -> bytes:
    """Read JSON bytes from a filesystem path or packaged resource."""
    if path:
        logger.debug(f"Reading Glottolog JSON from file: {path}")
        p = Path(path)
        if not p.exists():
            logger.error(f"Glottolog JSON not found at path: {p}")
            raise FileNotFoundError(f"Glottolog JSON not found at path: {p}")
        data = p.read_bytes()
        logger.debug(f"Read {len(data)} bytes from {p}")
        return data
    # packaged data (cltk/languages/glottolog.json)
    try:
        logger.debug(f"Reading packaged Glottolog JSON resource: {_DEFAULT_RESOURCE}")
        data = (pkg_files(__package__) / _DEFAULT_RESOURCE).read_bytes()
        logger.debug(f"Read {len(data)} bytes from packaged resource")
        return data
    except Exception as e:
        logger.error(
            f"Failed to read packaged Glottolog JSON '{_DEFAULT_RESOURCE}': {e}"
        )
        raise


@lru_cache(maxsize=1)
def load_languages(path: Optional[str] = None) -> dict[str, Language]:
    """Load Language models from JSON. Returns mapping glottocode -> Language."""
    logger.info(
        f"Loading Glottolog languages (path={'packaged' if not path else path})"
    )
    try:
        raw = _read_bytes(Path(path) if path else None)
    except Exception as e:
        logger.error(f"Failed to read Glottolog JSON: {e}")
        raise
    try:
        data = json.loads(raw)
    except Exception as e:
        logger.error(f"Failed to parse Glottolog JSON: {e}")
        raise

    # Accept either dict[str, obj] or list[obj]
    if isinstance(data, dict):
        logger.debug("Top-level JSON is an object; validating as dict[str, Language]")
        adapter = TypeAdapter(dict[str, Language])
        langs = adapter.validate_python(data)
        logger.info(f"Validated {len(langs)} languages (dict form)")
        return langs

    if isinstance(data, list):
        logger.debug("Top-level JSON is an array; validating as list[Language]")
        adapter = TypeAdapter(list[Language])
        langs_list = adapter.validate_python(data)
        langs = {L.glottolog_id: L for L in langs_list}
        logger.info(f"Validated {len(langs)} languages (list form)")
        return langs

    msg = "Unexpected JSON top-level type; expected object or array."
    logger.error(msg)
    raise ValueError(msg)


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
    return " ".join(s.lower().split())


def _is_historic_like(L: Language, cutoff: int = HISTORIC_CUTOFF_YEAR) -> bool:
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


def build_indices(
    path: Optional[str] = None,
) -> dict[
    Literal["by_iso", "by_name_lang", "by_name_dialect", "by_dialect"],
    dict[str, Any],
]:
    """Build lookup indices:
    - by_iso: iso -> language glottocode
    - by_name_lang: lowercased language name/alt-name -> [language glottocode]
    - by_name_dialect: lowercased dialect name -> [dialect glottocode]
    - by_dialect: dialect glottocode -> parent language glottocode
    """
    logger.debug(
        f"Building Glottolog indices (path={'packaged' if not path else path})"
    )
    langs = load_languages(path)
    by_iso: dict[str, str] = {}
    by_name_lang: dict[str, list[str]] = {}
    by_name_dialect: dict[str, list[str]] = {}
    by_dialect: dict[str, str] = {}
    for g, L in langs.items():
        if L.iso:
            by_iso[L.iso.lower()] = g
        by_name_lang.setdefault(L.name.lower(), []).append(g)
        for nv in L.alt_names:
            by_name_lang.setdefault(nv.value.lower(), []).append(g)
        # Index dialects by their glottocode and name
        for d in L.dialects:
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


def get_language(key: str, path: Optional[str] = None) -> Language:
    """Lookup by glottocode, ISO, or name/alt-name."""
    logger.debug(
        f"Looking up language for key='{key}' (path={'packaged' if not path else path})"
    )
    langs: dict[str, Language] = load_languages(path)
    idx: dict[
        Literal["by_iso", "by_name_lang", "by_name_dialect", "by_dialect"],
        dict[str, Any],
    ] = build_indices(path)
    k: str = key.lower()
    # glottocode (language)
    if key in langs:
        logger.debug(f"Found language by glottocode: {key}")
        return langs[key]
    # glottocode (dialect) -> do NOT coerce to language; ask user to use get_dialect()
    parent = idx["by_dialect"].get(key)
    if parent:
        lang = langs[parent]
        msg = (
            f"'{key}' is a dialect of {lang.name} (glottolog_id={parent}). "
            f"Use get_dialect('{key}') to retrieve the dialect."
        )
        logger.info(msg)
        raise KeyError(msg)
    # ISO
    g: Optional[str] = idx["by_iso"].get(k)
    if g:
        logger.debug(f"Found language by ISO='{k}' -> glottocode='{g}'")
        return langs[g]
    msg = f"No language found for '{key}'"
    logger.error(msg)
    raise KeyError(msg)


def get_dialect(key: str, path: Optional[str] = None) -> tuple[Language, Dialect]:
    """Lookup a dialect by glottocode or exact dialect name.
    Returns (parent_language, dialect). Raises KeyError with guidance on failure.
    """
    logger.debug(
        f"Looking up dialect for key='{key}' (path={'packaged' if not path else path})"
    )
    langs: dict[str, Language] = load_languages(path)
    idx: dict[
        Literal["by_iso", "by_name_lang", "by_name_dialect", "by_dialect"],
        dict[str, Any],
    ] = build_indices(path)

    k = key.lower()

    # If the key is a language glottocode, direct user to get_language()
    if key in langs:
        msg = f"'{key}' is a language glottocode. Use get_language('{key}')."
        logger.info(msg)
        raise KeyError(msg)

    # If the key looks like a language ISO, direct user to get_language()
    if k in idx["by_iso"]:
        lang_id = idx["by_iso"][k]
        lang = langs[lang_id]
        msg = (
            f"'{key}' resolves to the language {lang.name} (glottolog_id={lang_id}). "
            f"Use get_language('{key}') for languages."
        )
        logger.info(msg)
        raise KeyError(msg)

    # Direct dialect glottocode
    parent = idx["by_dialect"].get(key) or idx["by_dialect"].get(k)
    if parent:
        lang = langs[parent]
        target_id = key if key in idx["by_dialect"] else k
        for d in lang.dialects:
            if d.glottolog_id == target_id:
                logger.debug(
                    f"Found dialect by id '{key}' under language '{lang.name}'"
                )
                return lang, d
        # Very unlikely: index points to parent but dialect not found; scan as fallback
        for L in langs.values():
            for d in L.dialects:
                if d.glottolog_id == target_id:
                    logger.debug(
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
                d = next((d for d in lang.dialects if d.glottolog_id == did), None)
                if d:
                    logger.debug(
                        f"Found dialect by name '{key}' -> {d.name} (id={did}) under '{lang.name}'"
                    )
                    return lang, d
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
        logger.info(msg)
        raise KeyError(msg)

    msg = f"No dialect found for '{key}'"
    logger.error(msg)
    raise KeyError(msg)


def resolve_languoid(
    key: str, path: Optional[str] = None
) -> tuple[Language, Optional[Dialect]]:
    """Resolve a language or dialect key into (Language, Optional[Dialect]).
    Accepts:
      - language glottocode (e.g., 'lati1261'), ISO (e.g., 'lat'), or exact language name/alt-name
      - dialect glottocode (e.g., 'demo1234') or exact dialect name
    Returns:
      - (Language, None) for languages
      - (Language, Dialect) for dialects
    Raises:
      - KeyError with guidance if nothing (or an ambiguous dialect name) matches.
    """
    logger.debug(
        f"Resolving languoid for key='{key}' (path={'packaged' if not path else path})"
    )

    langs: dict[str, Language] = load_languages(path)
    idx: dict[
        Literal["by_iso", "by_name_lang", "by_name_dialect", "by_dialect"],
        dict[str, Any],
    ] = build_indices(path)

    k = key.lower()

    # 1) Exact language glottocode
    if key in langs:
        L = langs[key]
        logger.debug(f"Resolved language by glottocode: {key} -> {L.name}")
        return L, None

    # 2) Exact dialect glottocode
    parent = idx["by_dialect"].get(key) or idx["by_dialect"].get(k)
    if parent:
        lang = langs[parent]
        target_id = key if key in idx["by_dialect"] else k
        for d in lang.dialects:
            if d.glottolog_id == target_id:
                logger.debug(
                    f"Resolved dialect by glottocode: {key} -> {d.name} (parent={lang.name})"
                )
                return lang, d
        # Fallback scan (should not be needed)
        for L in langs.values():
            for d in L.dialects:
                if d.glottolog_id == target_id:
                    logger.debug(
                        f"Resolved dialect by glottocode via fallback scan: {key} -> {d.name} (parent={L.name})"
                    )
                    return L, d
        msg = f"Dialect id '{key}' indexed but not found in model data."
        logger.error(msg)
        raise KeyError(msg)

    # 3) ISO (language only)
    g = idx["by_iso"].get(k)
    if g:
        L = langs[g]
        logger.debug(f"Resolved language by ISO: {key} -> {L.name} (glottolog_id={g})")
        return L, None

    # 4) Exact language name/alt-name (may be ambiguous) → prefer historic
    hits_lang: list[str] = idx["by_name_lang"].get(k, [])
    if hits_lang:
        if len(hits_lang) == 1:
            g0 = hits_lang[0]
            L = langs[g0]
            logger.debug(
                f"Resolved language by name: '{key}' -> {L.name} (glottolog_id={g0})"
            )
            return L, None
        cands = [langs[gx] for gx in hits_lang if gx in langs]
        cands.sort(key=_historic_rank, reverse=True)
        best = cands[0]
        logger.info(
            f"Ambiguous language name '{key}' matched {len(cands)} entries; "
            f"selecting '{best.name}' (glottolog_id={best.glottolog_id}) by historic preference."
        )
        return best, None

    # 5) Exact dialect name (may be ambiguous)
    hits_dia: list[str] = idx["by_name_dialect"].get(k, [])
    if hits_dia:
        if len(hits_dia) == 1:
            did = hits_dia[0]
            parent = idx["by_dialect"].get(did)
            if parent and parent in langs:
                lang = langs[parent]
                d = next((d for d in lang.dialects if d.glottolog_id == did), None)
                if d:
                    logger.debug(
                        f"Resolved dialect by name: '{key}' -> {d.name} (id={did}, parent={lang.name})"
                    )
                    return lang, d
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
        msg = (
            f"Ambiguous dialect name '{key}'. Please specify a dialect glottocode. "
            + ("Options: " + "; ".join(options) if options else "No options available.")
        )
        logger.info(msg)
        raise KeyError(msg)

    # 6) No match
    msg = f"No language or dialect found for '{key}'"
    logger.error(msg)
    raise KeyError(msg)
