"""The Bengali alphabet.

>>> from cltk.alphabet import ben
>>> ben.VOWELS[:5]
['অ', 'আ', 'ই', 'ঈ', 'উ']
>>> ben.DEPENDENT_VOWELS[:5]
['◌া', 'ি', '◌ী', '◌ু', '◌ূ']
>>> ben.CONSONANTS[:5]
['ক', 'খ', 'গ', 'ঘ ', 'ঙ']
"""


# The digits in bengali start from index 0 to 9.
DIGITS = ["০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯"]

VOWELS = ["অ", "আ", "ই", "ঈ", "উ", "ঊ", "এ", "ঐ", "ও", "ঔ"]

DEPENDENT_VOWELS = ["◌া", "ি", "◌ী", "◌ু", "◌ূ", "◌ৃ", "ে", "ৈ", "ো", "ৌ"]

CONSONANTS = [
    "ক",
    "খ",
    "গ",
    "ঘ ",
    "ঙ",
    "চ",
    " ছ ",
    "জ",
    "ঝ",
    " ঞ",
    "ট",
    " ঠ",
    "ড",
    " ঢ",
    "ণ",
    "ত",
    "থ",
    " দ",
    " ধ",
    " ন",
    "প",
    "ফ",
    "ব",
    "ভ",
    "ম",
    "য",
    "র",
    "ল",
    "শ",
    "ষ",
    "স",
    "হ",
    "ড় ",
    "ঢ়",
    "য়",
    "ৎ‌",
]

# Along with consonants and vowels there are some special modifiers,
# called Virama, Visarga, Anusvara, Candrabindu and Ishar.
# Anusvara is used for final velar nasal sound, Visarga adds
# voiceless breath after vowel and Candrabindu is used to nasalize vowels
MODIFIERS = ["◌্", "◌ঁ", "◌ং", "◌ঃ"]
