"""Alphabet and text normalization for Latin."""

from cltk.alphabet.text_normalization import cltk_normalize


def normalize_lat(text: str) -> str:
    """The function for all default Latin normalization.

    TODO: Add parameters for stripping macrons, other unlikely chars. Perhaps use ``remove_non_ascii()``.
    """
    text_cltk_normalized = cltk_normalize(text=text)  # type: str
    return text_cltk_normalized
