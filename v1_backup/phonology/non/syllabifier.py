"""
Sonority hierarchy for Old Norse
"""

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]
__license__ = "MIT License"

# Used according to sonority principle
hierarchy = [
    [
        "a",
        "á",
        "æ",
        "e",
        "é",
        "i",
        "í",
        "o",
        "ǫ",
        "ø",
        "ö",
        "œ",
        "ó",
        "u",
        "ú",
        "y",
        "ý",
    ],
    ["j"],
    ["m"],
    ["n"],
    ["p", "b", "d", "g", "t", "k"],
    ["c", "f", "s", "h", "v", "x", "z", "þ", "ð"],
    ["r"],
    ["l"],
]

VOWELS = hierarchy[0]
LONG_VOWELS = ["ö", "ø", "á", "æ", "œ", "é", "í", "ó", "ú", "ý"]
SHORT_VOWELS = ["a", "e", "i", "o", "u", "y", "ǫ"]

# For i-umlaut
BACK_TO_FRONT_VOWELS = {
    "a": "e",
    "á": "æ",
    "ǫ": "ø",
    "o": "ø",
    "ó": "œ",
    "u": "y",
    "ú": "ý",
    "jú": "ý",
    "jó": "ý",
    "ö": "ø",
    "au": "ey",
}

DIPHTHONGS = ["ey", "au", "ei"]
CONSONANTS = [consonant for level in hierarchy[1:] for consonant in level]

invalid_onsets = ["lm", "fj", "nm", "rk", "nn", "tt", "ðr"]

# for old_norse_ipa
ipa_vowels = ["a", "ɛ", "i", "ɔ", "ɒ", "ø", "u", "y", "œ", "e", "o", "j"]

ipa_hierarchy = [
    ipa_vowels,
    ["r"],
    ["l"],
    ["m", "n"],
    ["f", "v", "θ", "ð", "s", "h"],
    ["b", "d", "g", "k", "p", "t"],
]
