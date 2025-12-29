"""Utility functions for keeping track of languages."""

from cltk.core.data_types import Language
from cltk.languages.languages import LANGUAGES

# Build a fast lookup for dialect codes like "egy-dem" → (iso, dialect)
_DIALECT_INDEX: dict[str, Language] = {}
for iso_key, lang in LANGUAGES.items():
    for dialect in lang.dialects:
        # lang.selected_dialect = dialect
        if not dialect.language_code:
            continue
        _DIALECT_INDEX[dialect.language_code] = lang


def find_iso_name(common_name: str) -> list[str]:
    """Find codes by matching the human name. Returns ISO or Glottolog language and dialect codes.

    Matches against Language.name and Dialect.name (case-insensitive substring).
    """
    q = common_name.lower()
    codes: list[str] = []
    # Match language names
    for iso_key, language_obj in LANGUAGES.items():
        if q in language_obj.name.lower():
            codes.append(f'{language_obj.name} ("{iso_key}")')
    # Match dialect names (return dialect codes, e.g., 'egy-dem')
    for iso_key, language_obj in LANGUAGES.items():
        for d in language_obj.dialects or []:
            if q in d.name.lower():
                if d.language_code:
                    codes.append(f'{d.name} ("{d.language_code}")')
    return codes
