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

    >>> raw_text = "κατηγόρων’, οὐκ οἶδα: ἐγὼ δ᾽ οὖν"
    >>> split_trailing_punct(text=raw_text)
    'κατηγόρων ’, οὐκ οἶδα : ἐγὼ δ᾽ οὖν'
    """
    if not punctuation:
        # What about the curly thing (``᾽``) in eg ``δ᾽``
        punctuation = [":", "’", "”"]  # closing curly quotes
    new_chars: List[str] = list()
    for index, char in enumerate(text):
        if char in punctuation and index > 0:
            # Check whether the punct is attached to a word end
            prev_char = text[index - 1]
            # If a space already before the punct, then don't add space
            if prev_char.isspace():
                new_chars.append(char)
            else:
                # If no whitespace before, then do the split
                new_chars.append(f" {char}")
        else:
            new_chars.append(char)
    return "".join(new_chars)


def split_leading_punct(text: str, punctuation: Optional[List[str]] = None) -> str:
    """Some tokenizers, including that in Stanza, do not always
    handle punctuation properly. For example, an open curly
    quote  (``"‘κατηγόρων’"``) is not split into an extra punctuation
    token. This function does such splitting on raw text before
    being sent to such a tokenizer.

    Args:
        text: Input text string.
        punctuation: List of punctuation that should be split when before a word.

    Returns:
        Text string with leading punctuation separated by a whitespace character.

    >>> raw_text = "‘κατηγόρων’, οὐκ οἶδα: ἐγὼ δ᾽ οὖν"
    >>> split_leading_punct(text=raw_text)
    '‘ κατηγόρων’, οὐκ οἶδα: ἐγὼ δ᾽ οὖν'
    """
    if not punctuation:
        punctuation = ["‘", "“"]  # opening curly quotes
    new_chars: List[str] = list()
    last_char_idx = len(text) - 1
    for index, char in enumerate(text):
        # If at end of string, don't split
        if index == last_char_idx:
            new_chars.append(char)
            continue
        next_char = text[index + 1]
        # If there is already a whitespace ahead, do not add another
        if next_char.isspace():
            new_chars.append(char)
            continue
        else:
            if char in punctuation:
                new_chars.append(f"{char} ")
            else:
                new_chars.append(char)
    return "".join(new_chars)


def remove_odd_punct(text: str, punctuation: List[str] = None) -> str:
    """Remove certain characters that downstream processes do
    not handle well. It would be better to use ``split_leading_punct()``
    and ``split_trailing_punct()``, however the default models
    out of Stanza make very strange mistakes when, e.g., ``"‘"``
    is made its own token.

    What to do about the apostrophe following an elision (e.g.,
    ``"δ᾽""``)?

    >>> raw_text = "‘κατηγόρων’, οὐκ οἶδα: ἐγὼ δ᾽ οὖν"
    >>> remove_odd_punct(raw_text)
    'κατηγόρων, οὐκ οἶδα ἐγὼ δ᾽ οὖν'
    """
    if not punctuation:
        punctuation = ["‘", "“", ":", "’", "”"]
    chars: List[str] = [char for char in text if char not in punctuation]
    return "".join(chars)
