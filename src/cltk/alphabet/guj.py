"""The Gujarati alphabet.

>>> from cltk.alphabet import guj
>>> guj.VOWELS[:5]
['અ', 'આ', 'ઇ', 'ઈ', 'ઉ']
>>> guj.CONSONANTS[:5]
['ક', 'ખ', 'ગ', 'ઘ', 'ચ']
"""

__author__ = ["Dhruv Apte"]

DIGITS = ["૦", "૧", "૨", "૩", "૪", "૫", "૬", "૭", "૮", "૯", "૧૦"]

VOWELS = ["અ", "આ", "ઇ", "ઈ", "ઉ", "ઊ", "ઋ", "એ", "ઐ", "ઓ", "ઔ", "અં", "અઃ"]

DEPENDENT_VOWELS = ["ા ", "િ", "ી", "ો", "ૌ"]

CONSONANTS = [
    "ક",
    "ખ",
    "ગ",
    "ઘ",
    "ચ",
    "છ",
    "જ",
    "ઝ",
    "ઞ",
    "ટ",
    "ઠ",
    "ડ",
    "ઢ",
    "ણ",
    "ત",
    "થ",
    "દ",
    "ધ",
    "ન",
    "પ",
    "ફ",
    "બ",
    "ભ",
    "મ",
    "ય",
    "ર",
    "લ",
    "ળ",
    "વ",
    "શ",
    "ષ",
    "સ",
    "હ",
]

VELAR_CONSONANTS = ["ક", "ખ", "ગ", "ઘ", "ઙ"]

PALATAL_CONSONANTS = ["ચ", "છ", "જ", "ઝ", "ઞ"]

RETROFLEX_CONSONANTS = ["ટ", "ઠ", "ડ", "ઢ", "ણ"]

DENTAL_CONSONANTS = ["ત", "થ", "દ", "ધ", "ન"]

LABIAL_CONSONANTS = ["પ", "ફ", "બ", "ભ", "મ"]

SONORANT_CONSONANTS = ["ય", "ર", "લ", "વ"]

SIBILANT_CONSONANTS = ["શ", "ષ", "સ"]

GUTTURAL_CONSONANT = ["હ"]

ADDITIONAL_CONSONANTS = ["ળ", "ક્ષ", "જ્ઞ"]

MODIFIERS = [" ्", " ॓", " ॔"]
