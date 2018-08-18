"""Persian alphabet"""

__author__ = "Iman Nazari"

# HAMZEH Family
HAMZEH = '\u0621'
ALEF_WITH_MAD = '\u0622'
ALEF_WITH_HAMZEH_ABOVE = '\u0623'
VE_WITH_HAMZA_ABOVE = '\u0624'
ALEF_WITH_HAMZEH_BELOW = '\u0625'
YE_WITH_HAMZA_ABOVE = '\u0626'

# واج‌ها
# Phonemes
ALEF = '\u0627'
BE = '\u0628'
PE = '\u067e'
TE = '\u062a'
SE = '\u062b'
JIM = '\u062c'
CHE = '\u0686'
HE = '\u062d'
KHE = '\u062e'
DAL = '\u062f'
ZAL = '\u0630'
RE = '\u0631'
ZE = '\u0632'
ZHE = '\u0698'
SIN = '\u0633'
SHIN = '\u0634'
SAD = '\u0635'
ZAD = '\u0636'
TA = '\u0637'
ZA = '\u0638'
EYN = '\u0639'
GHEYN = '\u063a'
FE = '\u0641'
GHAF = '\u0642'
KAF = '\u06a9'
GAF = '\u0642'
LAM = '\u0644'
MIM = '\u0645'
NOON = '\u0646'
VAV = '\u0648'
HE2 = '\u0647'
YE = '\u06cc'

# Punctuation marks
COMMA = '\u060C'
SEMICOLON = '\u061B'
QUESTION = '\u061F'

# Other symbols
PERCENT = '\u066a'
DECIMAL = '\u066b'
THOUSANDS = '\u066c'

# Necessary for writing
KESHIDEGI = '\u0640'
ZERO_WIDTH_NONE_JOINER = '\u200c'
ZERO_WIDTH_JOINER = '\u200d'

# تنوین‌ها
# Tanvins
TANVIN_FATHE = '\u064b'
TANVIN_ZAMME = '\u064c'
TANVIN_KASRE = '\u064d'

# واکه‌ها یا مصوت‌ها یا حروف صدادار
# Vowels
FATHE = '\u064e'
ZAMME = '\u064f'
KASRE = '\u0650'

# Diacritics
TASHDID = '\u0651'
SOKUN = '\u0652'
MAD = '\u0653'

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
    YE: 32
}

NUMERALS = {
    0: '۰',
    1: '۱',
    2: '۲',
    3: '۳',
    4: '۴',
    5: '۵',
    6: '۶',
    7: '۷',
    8: '۸',
    9: '۹'
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
    9: "نه"
}
