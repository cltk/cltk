"""
The hyphenation/syllabification algorithm is based on the typical syllable
structure model of onset/nucleus/coda. An additional problem arises with the
distinction between long and short vowels, since many use identical graphemes
for both long and short vowels. The great vowel shift that dates back to the
early stages of ME poses an additional problem.
"""

__author__ = ["Eleftheria Chatziargyriou <ele.hatzy@gmail.com>"]
__license__ = "MIT License"

SHORT_VOWELS = ["a", "e", "i", "o", "u", "y", "æ"]

LONG_VOWELS = ["aa", "ee", "oo", "ou", "ow", "ae"]

DIPHTHONGS = ["th", "gh", "ht", "ch"]

TRIPHTHONGS = ["ght", "ghl"]

CONSONANTS = [
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "l",
    "m",
    "n",
    "p",
    "r",
    "s",
    "t",
    "x",
    "ð",
    "þ",
    "ƿ",
]

hierarchy = [
    ["a", "æ", "e", "i", "o", "u", "y"],
    ["m", "n"],
    ["p", "b", "d", "g", "t", "k", "q", "ð", "w"],
    ["c", "f", "s", "h", "v", "x", "þ"],
    ["r", "ƿ"],
    ["l"],
]
