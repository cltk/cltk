"""The Hindi alphabet.

>>> from cltk.alphabet import hin
>>> hin.VOWELS[:5]
['अ', 'आ', 'इ', 'ई', 'उ']
>>> hin.CONSONANTS[:5]
['क', 'ख', 'ग', 'घ', 'ङ']
>>> hin.SONORANT_CONSONANTS
['य', 'र', 'ल', 'व']
"""


# The digits in hindi from index 0 to 9.

DIGITS = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]

VOWELS = ["अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ"]

DEPENDENT_VOWELS = ["◌া", "ি", "◌ী", "◌ু", "◌ূ", "◌ৃ", "ে", "ৈ", "ো", "ৌ"]
# following are the general consonants
CONSONANTS = [
    "क",
    "ख",
    "ग",
    "घ",
    "ङ",
    "च",
    "छ",
    "ज",
    "झ",
    "ञ",
    "ट",
    "ठ",
    "ड",
    "ढ",
    "ण",
    "त",
    "थ",
    "द",
    "ध",
    "न",
    "प",
    "फ",
    "ब",
    "भ",
    "म",
]

# following are modified constants
MODIFIED_CONSTANTS = ["क़", "ग़", "ख़", "ज़", "ड़", "ढ़", "फ़"]


# the Semivowels are also in the script of hindi
SEMIVOWELS = ["य", "र", "ल", "व"]

# There are three sibilants:
SIBILANTS = ["श", "ष", "स"]

FRICATIVE = ["ह"]

# Anusvara is used for final velar nasal sound,
# Visarga adds voiceless breath after vowel,
# and Candrabindu is used to nasalize vowels

MODIFIERS = ["◌্", "◌ঁ", "◌ং", "◌ঃ"]

# Classification of alphabets according to how their sound is produced

VELAR_CONSONANTS = ["क", "ख", "ग", "घ", "ङ"]

PALATAL_CONSONANTS = ["च", "छ", "ज", "झ", "ञ"]

RETROFLEX_CONSONANTS = ["ट", "ठ", "ड", "ढ", "ण"]

DENTAL_CONSONANTS = ["त", "थ", "द", "ध", "न"]

LABIAL_CONSONANTS = ["प", "फ", "ब", "भ", "म"]

SONORANT_CONSONANTS = ["य", "र", "ल", "व"]

SIBILANT_CONSONANTS = ["श", "ष", "स"]

GUTTURAL_CONSONANT = ["ह"]

SIGNS = ["ॐ"]
