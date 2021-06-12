"""Functions for preprocessing texts. Not language-specific."""

from typing import List, Optional
from unicodedata import normalize


def cltk_normalize(text, compatibility=True):
    if compatibility:
        return normalize("NFKC", text)
    else:
        return normalize("NFC", text)


def remove_non_ascii(input_string):
    """Remove non-ascii characters
    Source: http://stackoverflow.com/a/1342373
    """
    no_ascii = "".join(i for i in input_string if ord(i) < 128)
    return no_ascii


def remove_non_latin(input_string, also_keep=None):
    """Remove non-Latin characters.
    `also_keep` should be a list which will add chars (e.g. punctuation)
    that will not be filtered.
    """
    if also_keep:
        also_keep += [" "]
    else:
        also_keep = [" "]
    latin_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    latin_chars += latin_chars.lower()
    latin_chars += "".join(also_keep)
    no_latin = "".join([char for char in input_string if char in latin_chars])
    return no_latin


def split_trailing_punct(text: str, punctuation: Optional[List[str]] = None) -> str:
    """Some tokenizers, including that in Stanza, do not always
    handle punctuation properly. For example, a trailing colon (``"οἶδα:"``)
    is not split into an extra punctuation token. This function
    does such splitting on raw text before being sent to such
    a tokenizer.

    Args:
        text: Input text string.
        punctuation: List of punctuation that should be split when trailing a word.

    Returns:
        Text string with trailing punctuation separated by a whitespace character.

    >>> raw_text = "κατηγόρων, οὐκ οἶδα: ἐγὼ δ᾽ οὖν"
    >>> split_trailing_punct(text=raw_text)
    'κατηγόρων, οὐκ οἶδα : ἐγὼ δ᾽ οὖν'
    """
    if not punctuation:
        punctuation = [":", "'"]
    new_chars: List[str] = list()
    for char in text:
        if char in punctuation:
            new_chars.append(" :")
        else:
            new_chars.append(char)
    return "".join(new_chars)
