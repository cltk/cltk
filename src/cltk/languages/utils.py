"""Utility functions for keeping track of languages."""

from cltk.core.data_types_v2 import Dialect, Language
from cltk.core.exceptions import UnknownLanguageError
from cltk.languages.glottolog_v2 import LANGUAGES

# Build a fast lookup for dialect codes like "egy-dem" → (iso, dialect)
_DIALECT_INDEX: dict[str, Language] = {}
for iso_key, lang in LANGUAGES.items():
    for dialect in lang.dialects:
        lang.selected_dialect = (
            dialect.code
        )  # Set the selected dialect for the base language
        _DIALECT_INDEX[dialect.code] = lang


def get_lang(code: str) -> Language:
    """Return a Language by ISO 639-3 code (e.g., 'lat') or by dialect code (e.g., 'egy-dem').

    If a dialect code is provided, this returns the base Language object with
    `selected_dialect` set to that Dialect.

    >>> from cltk.languages.utils import get_lang
    >>> get_lang("akk").iso
    'akk'
    >>> get_lang("xxx")
    Traceback (most recent call last):
      ...
    cltk.core.exceptions.UnknownLanguageError: Unknown language code 'xxx'.
    """
    # Exact ISO code hit
    try:
        return LANGUAGES[code]
    except KeyError:
        pass
    # Look for dialect code
    try:
        lang_with_dialect = _DIALECT_INDEX[code]
    except KeyError:
        msg: str = f"Unknown language code '{code}'."
        raise UnknownLanguageError(msg)
    # Return a fresh copy annotated with the requested dialect (Dialect object, not just code)
    return lang_with_dialect.model_copy(
        update={"selected_dialect": lang_with_dialect.selected_dialect}
    )


def find_iso_name(common_name: str) -> list[str]:
    """Find codes by matching the human name. Returns ISO codes and dialect codes.

    Matches against Language.name and Dialect.name (case-insensitive substring).
    """
    q = common_name.lower()
    codes: list[str] = []

    # Match language names
    for iso_key, language_obj in LANGUAGES.items():
        if q in language_obj.name.lower():
            codes.append(iso_key)

    # Match dialect names (return dialect codes, e.g., 'egy-dem')
    for iso_key, language_obj in LANGUAGES.items():
        for d in language_obj.dialects or []:
            if q in d.name.lower():
                codes.append(d.code)

    return codes
