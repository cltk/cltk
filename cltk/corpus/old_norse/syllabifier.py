"""
Sonority hierarchy for Old Norse
"""

__author__ = ["Clément Besnier <clemsicences@aol.com>", ]
__license__ = "MIT License"

# Used according to sonority principle
hierarchy = [
    ["a", "á", "æ", "e", "é", "i", "í", "o", "ǫ", "ø", "ö", "œ", "ó", "u", "ú", "y", "ý"],
    ["j"],
    ["m"],
    ["n"],
    ["p", "b", "d", "g", "t", "k"],
    ["c", "f", "s", "h", "v", "x", "z", "þ", "ð"],
    ["r"],
    ["l"]
]

invalid_onsets = ['lm', "fj", "nm", "rk", "nn", "tt", "ðr"]

# for old_norse_ipa
ipa_vowels = ["a", "ɛ", "i", "ɔ", "ɒ", "ø", "u", "y", "œ", "e", "o", "j"]

ipa_hierarchy = [ipa_vowels, ["r"], ["l"], ["m", "n"], ["f", "v", "θ", "ð", "s", "h"], ["b", "d", "g", "k", "p", "t"]]
