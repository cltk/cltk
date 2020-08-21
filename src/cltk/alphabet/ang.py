"""The Old English alphabet.

>>> from cltk.alphabet import ang
>>> ang.DIGITS[:5]
['ān', 'tƿeġen', 'þrēo', 'fēoƿer', 'fīf']
>>> ang.DIPHTHONGS[:5]
['ea', 'eo', 'ie']
"""

# digits [1-10]
DIGITS = [
    "ān",
    "tƿeġen",
    "þrēo",
    "fēoƿer",
    "fīf",
    "seox",
    "seofon",
    "eahta",
    "niġon",
    "tīen",
]

ALPHABET = [
    "a",
    "æ",
    "b",
    "c",
    "d",
    "ð",
    "e",
    "f",
    "g",
    "h",
    "i",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "w",
    "ƿ",
    "x",
    "y",
    "þ",
]

CONSONANTS = [
    "b",
    "c",
    "cȝ",
    "cg",
    "d",
    "ð",
    "f",
    "ff",
    "ȝ",
    "g",
    "h",
    "l",
    "n",
    "p",
    "r",
    "s",
    "ss",
    "sc",
    "t",
    "þ",
    "þþ",
    "ƿ",
    "w",
]

VOWELS = ["a", "æ", "e", "i", "o", "u", "y"]

DIPHTHONGS = ["ea", "eo", "ie"]
