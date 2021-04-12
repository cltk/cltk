"""Ottoman alphabet

Misc. notes:

- Based off Persian Alphabet Transliteration in CLTK by Iman Nazar
- Uses UTF-8 Encoding for Ottoman/Persian Letters
- When printing Arabic letters, they appear in the console from \
left to right and inconsistently linked, but correctly link and \
flow right to left when inputted into a word processor. The \
problems only exist in the terminal.

TODO: Add tests
"""

__author__ = ["Leonidas Mylonakis <>"]

# HEMZE Family
HEMZE = "\u0621"  # indicates initial vowel
ELIF_WITH_MAD = "\u0622"  # stretch elif
ELIF_WITH_HEMZE_ABOVE = "\u0623"
ELIF_WITH_HEMZE_BELOW = "\u0625"
VE_WITH_HEMZE_ABOVE = "\u0624"
YE_WITH_HEMZE_ABOVE = "\u0626"

HEMZE_FAMILY = [
    HEMZE,
    ELIF_WITH_MAD,
    ELIF_WITH_HEMZE_ABOVE,
    VE_WITH_HEMZE_ABOVE,
    ELIF_WITH_HEMZE_BELOW,
    YE_WITH_HEMZE_ABOVE,
]

# Basic Alphabet
ELIF = "\u0627"  # ا
BE = "\u0628"  # ب
PE = "\u067e"  # پ
TE = "\u062a"  # ت
SE = "\u062b"  # ث
CIM = "\u062c"  # ج
CHIM = "\u0686"  # چ
HA = "\u062d"  # ح
HI = "\u062e"  # خ
DAL = "\u062f"  # د
ZEL = "\u0630"  # ذ
RE = "\u0631"  # ر
ZE = "\u0632"  # ز
JE = "\u0698"  # ژ
SIN = "\u0633"  # س
SHIN = "\u0634"  # ش
SAD = "\u0635"  # ص
DAD = "\u0636"  # ض
TI = "\u0637"  # ط
ZI = "\u0638"  # ظ
AYN = "\u0639"  # ع
GAYN = "\u063a"  # غ
FE = "\u0641"  # ف
KAF = "\u0642"  # ق
KEF = "\u06a9"  # ك
GEF = "\u0642"  # (rarely used - normally written KEF) گ
NEF = "\ufbd3"  # (rarely used - normally written KEF) ڭ
LAM = "\u0644"  # ل
MIM = "\u0645"  # م
NUN = "\u0646"  # ن
VAV = "\u0648"  # و
HE = "\u0647"  # ه
YE = "\u06cc"  # ی

ALPHABET_BASIC = [
    ELIF,
    BE,
    PE,
    TE,
    SE,
    CIM,
    CHIM,
    HA,
    HI,
    DAL,
    ZEL,
    RE,
    ZE,
    JE,
    SIN,
    SHIN,
    SAD,
    DAD,
    TI,
    ZI,
    AYN,
    GAYN,
    FE,
    KAF,
    KEF,
    GEF,
    NEF,
    LAM,
    MIM,
    NUN,
    VAV,
    HE,
    YE,
]

STABLE_NOUNS = [
    BE,
    PE,
    TE,
    SE,
    CIM,
    CHIM,
    HA,
    HI,
    DAL,
    ZEL,
    RE,
    ZE,
    JE,
    SIN,
    SHIN,
    SAD,
    DAD,
    TI,
    ZI,
    AYN,
    GAYN,
    FE,
    KAF,
    KEF,
    GEF,
    NEF,
    LAM,
    MIM,
    NUN,
]

# Punctuation marks
COMMA = "\u060C"
SEMICOLON = "\u061B"
QUESTION = "\u061F"

PUNCTUATION_MARKS = [COMMA, SEMICOLON, QUESTION, "."]

# Other symbols
PERCENT = "\u066a"
DECIMAL = "\u066b"
THOUSANDS = "\u066c"

OTHER_SYMBOLS = [PERCENT, DECIMAL, THOUSANDS]

# FIGURE OUT THIS SECTION
# Necessary for writing
KESHIDEGI = "\u0640"  # Elongation
ZERO_WIDTH_NONE_JOINER = (
    "\u200c"  # Forces disconnect betweeen two letters (useful for HE in Ottoman)
)
ZERO_WIDTH_JOINER = "\u200d"

NECESSARY_FOR_WRITING = [KESHIDEGI, ZERO_WIDTH_JOINER, ZERO_WIDTH_NONE_JOINER]

# Tenvins (doubled short vowels to end them with 'n' sound)
TENVIN_USTUN = "\u064b"  # -en/an (accusative)
TENVIN_OTRE = "\u064c"  # -un/ün (nominative)
TENVIN_ESRE = "\u064d"  # -in (genitive)

TENVINS = [TENVIN_ESRE, TENVIN_OTRE, TENVIN_USTUN]

# Short Vowels
USTUN = "\u064e"  # fetha (a - above)
OTRE = "\u064f"  # damma (o - above)
ESRE = "\u0650"  # kesra (i - below)

SHORT_VOWELS = [USTUN, OTRE, ESRE]

# Diacritics
SHEDDE = "\u0651"  # accent / double consonant
SUKUN = "\u0652"  # signifies absence of short vowel. Silence
MAD = "\u0653"  # stretch elif

DIACRITICS = [SHEDDE, SUKUN, MAD]

# Special letters
HE_DISCONNECT = HE + ZERO_WIDTH_NONE_JOINER

SPECIAL_LETTERS = [HE_DISCONNECT]

ALPHABETIC_ORDER = {
    ELIF: 1,
    BE: 2,
    PE: 3,
    TE: 4,
    SE: 5,
    CIM: 6,
    CHIM: 7,
    HA: 8,
    HI: 9,
    DAL: 10,
    ZEL: 11,
    RE: 12,
    ZE: 13,
    JE: 14,
    SIN: 15,
    SHIN: 16,
    SAD: 17,
    DAD: 18,
    TI: 19,
    ZI: 20,
    AYN: 21,
    GAYN: 22,
    FE: 23,
    KAF: 24,
    KEF: 25,
    GEF: 26,
    NEF: 27,
    LAM: 28,
    MIM: 29,
    NUN: 30,
    VAV: 31,
    HE: 32,
    YE: 33,
}

NUMERALS = {  # 0-9. Formed left to write.
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
    0: "صفر",  # sıfır
    1: "بر",  # bir
    2: "ایكی",  # iki
    3: "اوچ",  # üç
    4: "درت",  # dört
    5: "بش",  # beş
    6: "آلتی",  # altı
    7: "یدی",  # yedi
    8: "سكیز",  # sekiz
    9: "طقوز",  # dokuz
}

# Lletter-numeral value pairs (Persian extras have no value)
LETTER_NUMERICAL_VALUE = {
    ELIF: 1,
    BE: 2,
    TE: 400,
    SE: 500,
    CIM: 3,
    HA: 8,
    HI: 600,
    DAL: 4,
    ZEL: 700,
    RE: 200,
    ZE: 7,
    SIN: 60,
    SHIN: 300,
    SAD: 90,
    DAD: 800,
    TI: 9,
    ZI: 900,
    AYN: 70,
    GAYN: 1000,
    FE: 80,
    KAF: 100,
    KEF: 20,
    LAM: 30,
    MIM: 40,
    NUN: 50,
    VAV: 6,
    HE: 5,
    YE: 10,
}

# Consonants with multiple values
KEF_K = "\u06a9"  # ك
KEF_G = "\u06a9"  # ك
KEF_GH = "\u06a9"  # ك
KEF_N = "\u06a9"  # ك
DAD_D = "\u0636"  # ض
DAD_Z = "\u0636"  # ض
DAL_D = "\u062f"  # د
DAL_T = "\u062f"  # د
TI_T = "\u0637"  # ط
TI_D = "\u0637"  # ط
BE_B = "\u0628"  # ب
BE_P = "\u0628"  # ب

# Vowels (with multiple values)
ELIF_A = "\u0627"  # ا
ELIF_E = "\u0627"  # ا
VAV_V = "\u0648"  # و
VAV_O = "\u0648"  # و
VAV_OE = "\u0648"  # و (ö)
VAV_U = "\u0648"  # و
VAV_UE = "\u0648"  # و (ü)
YE_Y = "\u06cc"  # ی
YE_I = "\u06cc"  # ی (dotless ı)
YE_IE = "\u06cc"  # ی (dotted i)

ALPHABET_EXTENDED = [
    ALPHABET_BASIC
    + HEMZE_FAMILY
    + SHORT_VOWELS
    + TENVINS
    + DIACRITICS
    + NECESSARY_FOR_WRITING
    + OTHER_SYMBOLS
    + PUNCTUATION_MARKS
    + SPECIAL_LETTERS
]
