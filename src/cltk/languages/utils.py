"""Utility functions for keeping track of languages."""

from cltk.core.data_types import Language
from cltk.languages.glottolog import load_languages

# Build a fast lookup for dialect codes like "egy-dem" → (iso, dialect)
LANGUAGES = load_languages()
_DIALECT_INDEX: dict[str, Language] = {}
for iso_key, lang in LANGUAGES.items():
    for dialect in lang.dialects:
        # lang.selected_dialect = dialect
        _DIALECT_INDEX[dialect.language_code] = lang


# def get_lang(language_code: str) -> Language:
#     """Return a Language by ISO 639-3 code (e.g., 'lat') or by dialect code (e.g., 'egy-dem').

#     If a dialect code is provided, this returns the base Language object with
#     `selected_dialect` set to that Dialect.

#     >>> from cltk.languages.utils import get_lang
#     >>> get_lang("akk").iso
#     'akk'
#     >>> get_lang("xxx")
#     Traceback (most recent call last):
#       ...
#     cltk.core.exceptions.UnknownLanguageError: Unknown language code 'xxx'.
#     """
#     # Rewrite incorrect codes
#     if language_code == "arb":
#         logger.warning(f"Rewriting language code '{language_code}' to 'arb-cla'.")
#         language_code = "arb-cla"
#         input()
#     elif language_code == "egy":
#         egy_dialects: str = ", ".join(
#             [f'"{d.language_code}" ({d.name})' for d in LANGUAGES["egy"].dialects]
#         )
#         msg: str = (
#             f"Language code 'egy' is ambiguous. Please choose a dialect: {egy_dialects}."
#         )
#         logger.error(msg)
#         raise UnknownLanguageError(msg)
#     # Exact ISO code hit
#     try:
#         return LANGUAGES[language_code]
#     except KeyError:
#         pass
#     # Look for dialect code
#     try:
#         lang_with_dialect = _DIALECT_INDEX[language_code]
#     except KeyError:
#         msg: str = f"Unknown language code '{language_code}'."
#         raise UnknownLanguageError(msg)
#     # Return a fresh copy annotated with the requested dialect (Dialect object, not just code)
#     return lang_with_dialect.model_copy(
#         # update={"selected_dialect": lang_with_dialect.selected_dialect}
#     )


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
                codes.append(f'{d.name} ("{d.language_code}")')
    return codes
