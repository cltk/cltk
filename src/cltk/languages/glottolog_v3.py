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


@lru_cache(maxsize=1)
def build_indices(
    path: Optional[str] = None,
) -> dict[Literal["by_iso", "by_name", "by_dialect"], dict[str, str]]:
    """Build lookup indices:
    - by_iso: iso -> language glottocode
    - by_name: lowercased name/alt-name -> language OR dialect glottocode
    - by_dialect: dialect glottocode -> parent language glottocode
    """
    logger.debug(
        f"Building Glottolog indices (path={'packaged' if not path else path})"
    )
    langs = load_languages(path)
    by_iso: dict[str, str] = {}
    by_name: dict[str, str] = {}
    by_dialect: dict[str, str] = {}
    for g, L in langs.items():
        if L.iso:
            by_iso[L.iso.lower()] = g
        by_name[L.name.lower()] = g
        for nv in L.alt_names:
            by_name[nv.value.lower()] = g
        # Index dialects by their glottocode and name
        for d in L.dialects:
            by_dialect[d.glottolog_id] = g
            # Let dialect names be discoverable via by_name; value points to the dialect id
            by_name.setdefault(d.name.lower(), d.glottolog_id)
    logger.info(
        f"Built indices: by_iso={len(by_iso)} entries, by_name={len(by_name)} entries, by_dialect={len(by_dialect)}"
    )
    return {"by_iso": by_iso, "by_name": by_name, "by_dialect": by_dialect}


def get_language(key: str, path: Optional[str] = None) -> Language:
    """Lookup by glottocode, ISO, or name/alt-name."""
    logger.debug(
        f"Looking up language for key='{key}' (path={'packaged' if not path else path})"
    )
    langs: dict[str, Language] = load_languages(path)
    idx: dict[Literal["by_iso", "by_name", "by_dialect"], dict[str, str]] = (
        build_indices(path)
    )
    k: str = key.lower()
    # glottocode (language)
    if key in langs:
        logger.debug(f"Found language by glottocode: {key}")
        return langs[key]
    # glottocode (dialect) -> return parent language
    parent = idx["by_dialect"].get(key)
    if parent:
        logger.debug(
            f"Found dialect glottocode '{key}', returning parent language '{parent}'"
        )
        return langs[parent]
    # ISO
    g: Optional[str] = idx["by_iso"].get(k)
    if g:
        logger.debug(f"Found language by ISO='{k}' -> glottocode='{g}'")
        return langs[g]
    # name/alt-name (may map to a language or a dialect)
    hit: Optional[str] = idx["by_name"].get(k)
    if hit:
        # If name maps to a language id, return it; if it maps to a dialect id, return its parent
        if hit in langs:
            logger.debug(f"Found language by name='{k}' -> glottocode='{hit}'")
            return langs[hit]
        parent = idx["by_dialect"].get(hit)
        if parent:
            logger.debug(
                f"Found dialect by name='{k}' -> dialect='{hit}', parent glottocode='{parent}'"
            )
            return langs[parent]
    msg = f"No language found for '{key}'"
    logger.error(msg)
    raise KeyError(msg)


def get_dialect(key: str, path: Optional[str] = None) -> tuple[Language, Dialect]:
    """Lookup a dialect by glottocode, ISO, or name/alt-name."""
    logger.debug(
        f"Looking up dialect for key='{key}' (path={'packaged' if not path else path})"
    )
    langs: dict[str, Language] = load_languages(path)
    idx: dict[Literal["by_iso", "by_name", "by_dialect"], dict[str, str]] = (
        build_indices(path)
    )
    k: str = key.lower()
    # glottocode (dialect)
    if key in langs:
        logger.debug(f"Found dialect by glottocode: {key}")
        lang = langs[key]
        return lang, lang.dialects[0]  # Return the first dialect found
    # ISO
    g: Optional[str] = idx["by_iso"].get(k)
    if g:
        logger.debug(f"Found dialect by ISO='{k}' -> glottocode='{g}'")
        lang = langs[g]
        return lang, lang.dialects[0]
    # name/alt-name (must map to a dialect)
    hit: Optional[str] = idx["by_name"].get(k)
    if hit:
        logger.debug(f"Found dialect by name='{k}' -> glottocode='{hit}'")
        # Ensure the hit is a dialect glottocode
        if hit in langs and langs[hit].dialects:
            lang = langs[hit]
            return lang, lang.dialects[0]
    msg = f"No dialect found for '{key}'"
    logger.error(msg)
    raise KeyError(msg)
