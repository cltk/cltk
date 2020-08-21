"""The Odia alphabet.

>>> from cltk.alphabet import ory
>>> ory.VOWELS["0B05"]
'ଅ'
>>> ory.STRUCTURED_CONSONANTS["0B15"]
'କ'
"""

__author__ = ["Nishchith Shetty <inishchith@gmail.com>"]


# Oriya Unicode Standard

VOWELS = {
    "0B05": "ଅ",
    "0B06": "ଆ",
    "0B07": "ଇ",
    "0B08": "ଈ",
    "0B09": "ଉ",
    "0B0A": "ଊ",
    "0B0B": "ଋ",
    "N/A1": "ୠ",
    "0B0C": "ଌ",
    "N/A2": "ୡ",
    "0B0F": "ଏ",
    "0B10": "ଐ",
    "0B13": "ଓ",
    "0B14": "ଔ",
}

STRUCTURED_CONSONANTS = {
    "0B15": "କ",
    "0B16": "ଖ",
    "0B17": "ଗ",
    "0B18": "ଘ",
    "0B19": "ଙ",
    "0B1A": "ଚ",
    "0B1B": "ଛ",
    "0B1C": "ଜ",
    "0B1D": "ଝ",
    "0B1E": "ଞ",
    "0B1F": "ଟ",
    "0B20": "ଠ",
    "0B21": "ଡ",
    "0B22": "ଢ",
    "0B23": "ଣ",
    "0B24": "ତ",
    "0B25": "ଥ",
    "0B26": "ଦ",
    "0B27": "ଧ",
    "0B28": "ନ",
    "0B2A": "ପ",
    "0B2B": "ଫ",
    "0B2C": "ବ",
    "0B2D": "ଭ",
    "0B2E": "ମ",
    "0B2F": "ଯ",
    "0B30": "ର",
    "0B32": "ଲ",
    "0B33": "ଳ",
    "0B35": "ଵ",
    "0B36": "ଶ",
    "0B37": "ଷ",
    "0B38": "ସ",
    "0B39": "ହ",
}

# The structured consonants are classified according to where the tongue
# touches the palate of the mouth and are classified accordingly int
# five structured groups.
# These consonants are shown here with their IAST transcriptions.
VELAR_CONSONANTS = ["କ", "ଖ", "ଗ", "ଘ", "ଙ"]
VELAR_CONSONANTS_PRONONCIATION = ["ka", "kha", "ga", "gha", "ṅa"]

PALATAL_CONSONANTS = ["ଚ", "ଛ", "ଜ", "ଝ", "ଞ"]
PALATAL_CONSONANTS_PRONOUNCIATION = ["ca", "cha", "ja", "jha", "ña"]

RETROFLEX_CONSONANTS = ["ଟ", "ଠ", "ଡ", "ଢ", "ଣ"]
RETROFLEX_CONSONANTS_PRONOUNCIATION = ["ṭa", "ṭha", "ḍa", "ḍha", "ṇa"]

DENTAL_CONSONANTS = ["ତ", "ଥ", "ଦ", "ଧ", "ନ"]
DENTAL_CONSONANTS_PRONOUNCIATION = ["ta", "tha", "da", "dha", "na"]

LABIALS_CONSONANTS = ["ପ", "ଫ", "ବ", "ଭ", "ମ"]
LABIALS_CONSONANTS_PRONOUNCIATION = ["pa", "pha", "ba", "bha", "ma"]

UNSTRUCTURED_CONSONANTS = ["ଯ", "ୟ", "ର", "ଲ", "ଳ", "ୱ", "ଶ", "ଷ", "ସ", "ହ", "କ୍ଷ"]

NUMERALS = ["୦", "୧", "୨", "୩", "୪", "୫", "୬", "୭", "୮", "୯"]
EXTRA_NUMERICAL_SYMBOLS = ["୵", "୶", "୷", "୲", "୳", "୴"]
EXTRA_NUMERICAL_SYMBOLS_DESC = ["1/16", "1/8", "3/16", "1/4", "1/2", "3/4"]

# Anusvara is used for final velar nasal sound,
# Visarga adds voiceless breath after vowel
# Candrabindu is used to nasalize vowels
MODIFIERS = ["◌্", "◌ঁ", "◌ং", "◌ঃ"]
