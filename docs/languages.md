# Finding Language IDs

CLTK identifies languages using Glottolog codes (for example, `lati1261`) and, when
available, ISO 639-3 codes (for example, `lat`). You can pass a Glottolog ID, an
ISO code, or an exact language name to CLTK and it will resolve to a canonical
Language (and optionally a Dialect).

## Quick ways to find a language ID

### 1) Check the pipeline maps

Supported language IDs for pipelines are listed in:

- `src/cltk/languages/pipelines.py`
  - `MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE`
  - `MAP_LANGUAGE_CODE_TO_STANZA_PIPELINE`

### 2) Search the curated language list

The curated list of Language objects is in:

- `src/cltk/languages/languages.py`

Each Language entry includes:

- `glottolog_id`
- `iso` (when available)

### 3) Resolve by name or code at runtime

You can resolve any Glottolog ID, ISO code, or exact name with:

```python
from cltk.languages.glottolog import get_language

language, dialect = get_language(lang_id="lati1261")
# or
language, dialect = get_language(lang_id="lat")
# or
language, dialect = get_language(lang_id="Latin")
```

## Dialect examples

Dialect resolution requires a Glottolog dialect ID or an exact dialect name.
ISO 639-3 codes do not identify dialects.

```python
from cltk.languages.glottolog import get_dialect, get_language

# Resolve a dialect glottocode
language, dialect = get_language(lang_id="otto1234")

# Or ask for a dialect explicitly
language, dialect = get_dialect("otto1234")
```

## Notes

- Glottolog IDs are stable identifiers used throughout CLTK.
- ISO 639-3 codes are available for many (but not all) languages.
- Some entries are dialects under a parent language; in those cases
  `get_language` returns the parent Language and a Dialect.

## Resources

- ISO 639-3 code tables: https://iso639-3.sil.org/code_tables/639/data
- Glottolog: https://glottolog.org/
