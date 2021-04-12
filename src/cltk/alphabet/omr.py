"""The alphabet for Marathi.

# Using the International Alphabet of Sanskrit Transliteration (IAST), these vowels are represented thus


>>> from cltk.alphabet import omr
>>> omr.VOWELS[:5]
['अ', 'आ', 'इ', 'ई', 'उ']
>>> omr.IAST_VOWELS[:5]
['a', 'ā', 'i', 'ī', 'u']
>>> list(zip(omr.SEMI_VOWELS, omr.IAST_SEMI_VOWELS))
[('य', 'y'), ('र', 'r'), ('ल', 'l'), ('व', 'w')]
"""

__author__ = ["Mahesh Bhosale <bhosalems24@gmail.com>"]


# 0 to 9
DIGITS = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]

# Each vowel has an independent form and a mātrā form, which is used for modifying consonants
VOWELS = ["अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ", "अॅ", "ऑ"]
IAST_VOWELS = ["a", "ā", "i", "ī", "u", "ū", "ṛ", "e", "ai", "o", "au", "ae", "ao"]

# CONSONENTS
VELAR_CONSONANTS = ["क", "ख", "ग", "घ", "ङ"]
PALATAL_CONSONANTS = ["च", "छ", "ज", "झ", "ञ"]
RETROFLEX_CONSONANTS = ["ट", "ठ", "ड", "ढ", "ण"]
DENTAL_CONSONANTS = ["त", "थ", "द", "ध", "न"]
LABIAL_CONSONANTS = ["प", "फ", "ब", "भ", "म"]

IAST_VELAR_CONSONANTS = ["k", "kh", "g", "gh", "ṅ"]
IAST_PALATAL_CONSONANTS = ["c", "ch", "j", "jh", "ñ"]
IAST_RETROFLEX_CONSONANTS = ["ṭ", "ṭh", "ḍ", "ḍh", "ṇ"]
IAST_DENTAL_CONSONANTS = ["t", "th", "d", "dh", "n"]
IAST_LABIAL_CONSONANTS = ["p", "ph", "b", "bh", "m"]

# SEMI_VOWELS
SEMI_VOWELS = ["य", "र", "ल", "व"]
IAST_SEMI_VOWELS = ["y", "r", "l", "w"]

# SIBILANTS
SIBILANTS = ["श", "ष", "स"]
IAST_SIBILANTS = ["ś", "ṣ", "s"]

# FRIACTICE_CONSTANT

# There is one fricative consonant in marathi
FRIACTIVE_CONSONANTS = ["ह"]
IAST_FRIACTIVE_CONSONANTS = ["h"]

# ADDITIONAL_CONSTANTS
ADDITIONAL_CONSONANTS = ["ळ", "क्ष", "ज्ञ"]
IAST_ADDITIONAL_CONSONANTS = ["La", "kSha", "dnya"]
