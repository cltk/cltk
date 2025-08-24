from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files as pkg_files
from pathlib import Path
from typing import Any, Optional

from pydantic import TypeAdapter

from cltk.core.data_types_v3 import Language

# If you ship the JSON with the package, place it under cltk/languages/data/
_DEFAULT_RESOURCE = "glottolog.json"


def _read_bytes(path: Optional[Path]) -> bytes:
    if path:
        return Path(path).read_bytes()
    # packaged data (cltk/languages/glottolog.json)
    return (pkg_files(__package__) / _DEFAULT_RESOURCE).read_bytes()


@lru_cache(maxsize=1)
def load_languages(path: Optional[str] = None) -> dict[str, Language]:
    """Load Language models from JSON. Returns mapping glottocode -> Language."""
    raw = _read_bytes(Path(path) if path else None)
    data = json.loads(raw)

    # Accept either dict[str, obj] or list[obj]
    if isinstance(data, dict):
        adapter = TypeAdapter(dict[str, Language])
        return adapter.validate_python(data)

    if isinstance(data, list):
        adapter = TypeAdapter(list[Language])
        langs_list = adapter.validate_python(data)
        return {L.glottolog_id: L for L in langs_list}

    raise ValueError("Unexpected JSON top-level type; expected object or array.")


@lru_cache(maxsize=1)
def build_indices(path: Optional[str] = None) -> dict[str, dict[str, str]]:
    """Build simple lookup indices: by ISO code and by name/alt-name."""
    langs = load_languages(path)
    by_iso: dict[str, str] = {}
    by_name: dict[str, str] = {}
    for g, L in langs.items():
        if L.iso:
            by_iso[L.iso.lower()] = g
        by_name[L.name.lower()] = g
        for nv in L.alt_names:
            by_name[nv.value.lower()] = g
    return {"by_iso": by_iso, "by_name": by_name}


def get_language(key: str, path: Optional[str] = None) -> Language:
    """Lookup by glottocode, ISO, or name/alt-name."""
    langs = load_languages(path)
    idx = build_indices(path)
    k = key.lower()

    # glottocode
    if key in langs:
        return langs[key]
    # ISO
    g = idx["by_iso"].get(k)
    if g:
        return langs[g]
    # name/alt-name
    g = idx["by_name"].get(k)
    if g:
        return langs[g]

    raise KeyError(f"No language found for '{key}'")
