"""The alphabet for Middle High German. Source:

- *Schreibkonventionen des klassischen Mittelhochdeutschen*, Simone Berchtold
- https://de.wikipedia.org/wiki/Mittelhochdeutsch

The consonants of Middle High German are categorized as:

- Stops: ⟨p t k/c/q b d g⟩
- Affricates: ⟨pf/ph tz/z⟩
- Fricatives: ⟨v f s ȥ sch ch h⟩
- Nasals: ⟨m n⟩
- Liquids: ⟨l r⟩
- Semivowels: ⟨w j⟩

Misc. notes:

- c is used at the beginning of only loanwords and is pronounced the same as k (e.g. calant, cappitain)
- Double consonants are pronounced the same way as their corresponding letters in Modern Standard German (e.g. pp/p)
- schl, schm, schn, schw are written in MHG as sw, sl, sm, sn
- æ (also seen as ae), œ (also seen as oe) and iu denote the use of Umlaut over â, ô and û respectively
- ȥ or ʒ is used in modern handbooks and grammars to indicate the s or s-like sound which arose from Germanic t in the High German consonant shift.

>>> from cltk.alphabet import gmh
>>> gmh.CONSONANTS[:5]
['b', 'd', 'g', 'h', 'f']
>>> gmh.VOWELS[:5]
['a', 'ë', 'e', 'i', 'o']
"""

import re
import unicodedata

ALPHABET = [
    "a",
    "ë",
    "e",
    "i",
    "o",
    "u",
    "ä",
    "ö",
    "ü",
    "â",
    "ê",
    "î",
    "ô",
    "û",
    "æ",
    "œ",
    "iu",
    "b",
    "d",
    "g",
    "h",
    "f",
    "c",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "t",
    "v",
    "w",
    "z",
    "ȥ",
]


CONSONANTS = [
    "b",
    "d",
    "g",
    "h",
    "f",
    "c",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "t",
    "v",
    "w",
    "z",
]

VOWELS = [
    "a",
    "ë",
    "e",
    "i",
    "o",
    "u",
    "ä",
    "ö",
    "ü",
    "â",
    "ê",
    "î",
    "ô",
    "û",
    "æ",
    "œ",
    "iu",
]

SHORT_VOWELS = ["a", "ë", "e", "i", "o", "u", "ä", "ö", "ü"]

LONG_VOWELS = ["â", "ê", "î", "ô", "û", "æ", "œ", "iu"]

DIPHTHONGS = ["ei", "ie", "ou", "öu", "uo", "üe", "ch", "ng", "nt"]
TRIPHTHONGS = ["sch"]


def normalize_middle_high_german(
    text: str,
    to_lower_all: bool = True,
    to_lower_beginning: bool = False,
    alpha_conv: bool = True,
    punct: bool = True,
    ascii: bool = False,
):
    """Normalize input string.

    >>> from cltk.alphabet import gmh
    >>> from cltk.languages.example_texts import get_example_text
    >>> gmh.normalize_middle_high_german(get_example_text("gmh"))[:50]
    'uns ist in alten\\nmæren wunders vil geseit\\nvon hele'

    :param text:
    :param to_lower_beginning:
    :param to_lower_all: convert whole text to lowercase
    :param alpha_conv: convert alphabet to canonical form
    :param punct: remove punctuation
    :param ascii: returns ascii form
    :return: normalized text
    """

    if to_lower_all:
        text = text.lower()
    if to_lower_beginning:
        text = text[0].lower() + text[1:]
        text = re.sub(r"(?<=[\.\?\!]\s)(\w)", lambda x: x.group(1).lower(), text)
    if alpha_conv:
        text = (
            text.replace("ē", "ê")
            .replace("ī", "î")
            .replace("ā", "â")
            .replace("ō", "ô")
            .replace("ū", "û")
        )
        text = text.replace("ae", "æ").replace("oe", "œ")
    if punct:
        text = re.sub(r"[\.\";\,\:\[\]\(\)!&?‘]", "", text)
    if ascii:
        text = unicodedata.normalize("NFKD", text).encode(
            "ASCII", "ignore"
        )  # Encode into ASCII, returns a bytestring
        text = text.decode("utf-8")  # Convert back to string
    return text
