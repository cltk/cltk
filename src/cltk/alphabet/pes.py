"""The Persian alphabet.

TODO: Write tests.
"""


__author__ = "Iman Nazari"


import re

from cltk.alphabet import arb

# HAMZEH Family
HAMZEH = "\u0621"
ALEF_WITH_MAD = "\u0622"
ALEF_WITH_HAMZEH_ABOVE = "\u0623"
VE_WITH_HAMZA_ABOVE = "\u0624"
ALEF_WITH_HAMZEH_BELOW = "\u0625"
YE_WITH_HAMZA_ABOVE = "\u0626"

# واج‌ها
# Phonemes
ALEF = "\u0627"
BE = "\u0628"
PE = "\u067e"
TE = "\u062a"
SE = "\u062b"
JIM = "\u062c"
CHE = "\u0686"
HE = "\u062d"
KHE = "\u062e"
DAL = "\u062f"
ZAL = "\u0630"
RE = "\u0631"
ZE = "\u0632"
ZHE = "\u0698"
SIN = "\u0633"
SHIN = "\u0634"
SAD = "\u0635"
ZAD = "\u0636"
TA = "\u0637"
ZA = "\u0638"
EYN = "\u0639"
GHEYN = "\u063a"
FE = "\u0641"
GHAF = "\u0642"
KAF = "\u06a9"
GAF = "\u0642"
LAM = "\u0644"
MIM = "\u0645"
NOON = "\u0646"
VAV = "\u0648"
HE2 = "\u0647"
YE = "\u06cc"

# Punctuation marks
COMMA = "\u060C"
SEMICOLON = "\u061B"
QUESTION = "\u061F"

# Other symbols
PERCENT = "\u066a"
DECIMAL = "\u066b"
THOUSANDS = "\u066c"

# Necessary for writing
KESHIDEGI = "\u0640"
ZERO_WIDTH_NONE_JOINER = "\u200c"
ZERO_WIDTH_JOINER = "\u200d"

# تنوین‌ها
# Tanvins
TANVIN_FATHE = "\u064b"
TANVIN_ZAMME = "\u064c"
TANVIN_KASRE = "\u064d"

# واکه‌ها یا مصوت‌ها یا حروف صدادار
# Vowels
FATHE = "\u064e"
ZAMME = "\u064f"
KASRE = "\u0650"

# Diacritics
TASHDID = "\u0651"
SOKUN = "\u0652"
MAD = "\u0653"

HAMZEH_FAMILY = (
    HAMZEH,
    ALEF_WITH_MAD,
    ALEF_WITH_HAMZEH_ABOVE,
    VE_WITH_HAMZA_ABOVE,
    ALEF_WITH_HAMZEH_BELOW,
    YE_WITH_HAMZA_ABOVE,
)

ALPHABETIC_ORDER = {
    ALEF: 1,
    BE: 2,
    PE: 3,
    TE: 4,
    SE: 5,
    JIM: 6,
    CHE: 7,
    HE: 8,
    KHE: 9,
    DAL: 10,
    ZAL: 11,
    RE: 12,
    ZE: 13,
    ZHE: 14,
    SIN: 15,
    SHIN: 16,
    SAD: 17,
    ZAD: 18,
    TA: 19,
    ZA: 20,
    EYN: 21,
    GHEYN: 22,
    FE: 23,
    GHAF: 24,
    KAF: 25,
    GAF: 26,
    LAM: 27,
    MIM: 28,
    NOON: 29,
    VAV: 30,
    HE2: 31,
    YE: 32,
}

NUMERALS = {
    0: "۰",
    1: "۱",
    2: "۲",
    3: "۳",
    4: "۴",
    5: "۵",
    6: "۶",
    7: "۷",
    8: "۸",
    9: "۹",
}

NUMERALS_WRITINGS = {
    0: "صفر",
    1: "یک",
    2: "دو",
    3: "سه",
    4: "چهار",
    5: "پنج",
    6: "شش",
    7: "هفت",
    8: "هشت",
    9: "نه",
}


TO_REFORM = [
    {
        "characters": [
            arb.HAMZA,
            arb.HAMZA_BELOW,
            arb.HAMZA_ABOVE,
            arb.HAMZA_ISOLATED,
            arb.MINI_ALEF,
            arb.SMALL_ALEF,
            arb.SMALL_WAW,
            arb.SMALL_YEH,
            arb.KASHEEDA,
            arb.FATHATAN,
            arb.DAMMATAN,
            arb.KASRATAN,
            arb.FATHA,
            arb.DAMMA,
            arb.KASRA,
            arb.SHADDA,
            arb.SUKUN,
            arb.THOUSANDS,
            arb.DECIMAL,
        ],
        "to_be": "",
    },
    {
        "characters": [
            arb.ALEF_MADDA,
            arb.ALEF_WASLA,
            arb.HAMZA_BELOW_ALEF,
            arb.HAMZA_ABOVE_ALEF,
        ],
        "to_be": arb.ALEF,
    },
    {"characters": [arb.ALEF_MAKSURA, arb.YEH], "to_be": YE},
    {"characters": [KAF], "to_be": arb.KAF},
    {
        "characters": [
            arb.LAM_ALEF,
            arb.LAM_ALEF_HAMZA_ABOVE,
            arb.LAM_ALEF_HAMZA_BELOW,
            arb.LAM_ALEF_MADDA_ABOVE,
        ],
        "to_be": arb.LAM + arb.ALEF,
    },
    {"characters": [arb.TEH_MARBUTA], "to_be": HE2},
]


def mk_replacement_regex():
    replacement_dict = {}
    for rule in TO_REFORM:
        for character in rule["characters"]:
            replacement_dict[character] = rule["to_be"]

    for original_form, shaped_forms in arb.SHAPED_FORMS.items():
        for form in shaped_forms:
            replacement_dict[form] = replacement_dict.get(original_form, original_form)

    for i in range(10):
        replacement_dict[arb.EASTERN_ARABIC_NUMERALS[i]] = NUMERALS[i]
        replacement_dict[arb.WESTERN_ARABIC_NUMERALS[i]] = NUMERALS[i]
        # Use the commented parts for Word2Vec embeddings
        # replacementDict[NUMERALS[i]] = " %s " % NUMERALS_WRITINGS[i]

    # for char in '[!"#%\'()*+,-./:;<=>?@\[\]^_`{|}~’”“′‘\\\]؟؛«»،٪':
    #     replacementDict[char] = " "
    #
    # replacementDict[" +"] = " "

    return re.compile("(%s)" % "|".join(map(re.escape, replacement_dict.keys())))


REPLACEMENT_REGEX = mk_replacement_regex()


def normalize_text(text):
    return REPLACEMENT_REGEX.sub(
        lambda mo: REPLACEMENT_REGEX[mo.string[mo.start() : mo.end()]], text
    )
