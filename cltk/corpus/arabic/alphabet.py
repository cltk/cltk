"""
   Arabic alphabet
   source 1 : pyarabic 'https://github.com/linuxscout/pyarabic'
   source 2 : arabicstemmer 'https://github.com/assem-ch/arabicstemmer/blob/master/algorithm/stemmer.sbl'
"""
__author__ = 'Lakhdar Benzahia <lakhdar[.]benzahia[at]gmail[.]com>'

# Arabic letters

# Hamza letter
HAMZA = '\u0621'
HAMZA_ABOVE_ALEF = '\u0623'
HAMZA_BELOW_ALEF = '\u0625'
ALEF_MADDA = '\u0622'
HAMZA_ABOVE_WAW = '\u0624'
HAMZA_ABOVE_YEH = '\u0626'

ALEF = '\u0627'
ALEF_MAKSURA = '\u0649'
BEH = '\u0628'
TEH_MARBUTA = '\u0629'
TEH = '\u062a'
THEH = '\u062b'
JEEM = '\u062c'
HAH = '\u062d'
KHAH = '\u062e'
DAL = '\u062f'
THEL = '\u0630'
REH = '\u0631'
ZAIN = '\u0632'
SEEN = '\u0633'
SHEEN = '\u0634'
SAD = '\u0635'
DAD = '\u0636'
TAH = '\u0637'
ZAH = '\u0638'
AIN = '\u0639'
GHAIN = '\u063a'
FEH = '\u0641'
QAF = '\u0642'
KAF = '\u0643'
LAM = '\u0644'
MEEM = '\u0645'
NOON = '\u0646'
HEH = '\u0647'
WAW =  '\u0648'
YEH =  '\u064a'

MINI_ALEF = '\u0670'
ALEF_WASLA  = '\u0671'
MADDA_ABOVE = '\u0653'
HAMZA_ABOVE = '\u0654'
HAMZA_BELOW = '\u0655'

# Small Letters
SMALL_ALEF = "\u0670"
SMALL_WAW = "\u06E5"
SMALL_YEH  = "\u06E6"

# Ligatures Lam-Alef
LAM_ALEF = '\ufefb'
LAM_ALEF_HAMZA_ABOVE = '\ufef7'
LAM_ALEF_HAMZA_BELOW = '\ufef9'
LAM_ALEF_MADDA_ABOVE = '\ufef5'


SIMPLE_LAM_ALEF = '\u0644\u0627'
SIMPLE_LAM_ALEF_HAMZA_ABOVE = '\u0644\u0623'
SIMPLE_LAM_ALEF_HAMZA_BELOW = '\u0644\u0625'
SIMPLE_LAM_ALEF_MADDA_ABOVE = '\u0644\u0622'

# shaped forms
LAM_ALEF_ISOLATED = '\ufefb'
LAM_ALEF_FINAL = '\ufefc'

LAM_ALEF_HAMZA_ABOVE_ISOLATED = '\ufef7'
LAM_ALEF_HAMZA_ABOVE_FINAL = '\ufef8'

LAM_ALEF_HAMZA_BELOW_ISOLATED = '\ufef9'
LAM_ALEF_HAMZA_BELOW_FINAL = '\ufefa'

LAM_ALEF_MADDA_ABOVE_ISOLATED = '\ufef5'
LAM_ALEF_MADDA_ABOVE_FINAL = '\ufef6'

HAMZA_ISOLATED = '\ufe80'

ALEF_HAMZA_ABOVE_ISOLATED = '\ufe83'
ALEF_HAMZA_ABOVE_FINAL = '\ufe84'

ALEF_HAMZA_BELOW_ISOLATED = '\ufe87'
ALEF_HAMZA_BELOW_FINAL = '\ufe88'

YEH_HAMZA_INITIAL = '\ufe8b'
YEH_HAMZA_MEDIAL = '\ufe8c'
YEH_HAMZA_ISOLATED = '\ufe89'
YEH_HAMZA_FINAL = '\ufe8a'

ALEF_MADDA_ISOLATED = '\ufe81'
ALEF_MADDA_FINAL = '\ufe82'

WAW_HAMZA_ISOLATED = '\ufe85'
WAW_HAMZA_FINAL = '\ufe86'

ALEF_ISOLATED = '\ufe8d'
ALEF_FINAL = '\ufe8e'

BEH_ISOLATED = '\ufe8f'
BEH_FINAL = '\ufe90'
BEH_INITIAL = '\ufe91'
BEH_MEDIAL = '\ufe92'

TEH_MARBUTA_ISOLATED = '\ufe93'
TEH_MARBUTA_FINAL = '\ufe94'

TEH_INITIAL = '\ufe97'
TEH_MEDIAL = '\ufe98'
TEH_ISOLATED = '\ufe95'
TEH_FINAL = '\ufe96'

THEH_INITIAL = '\ufe9b'
THEH_MEDIAL = '\ufe9c'
THEH_FINAL = '\ufe9a'
THEH_ISOLATED = '\ufe99'

JEEM_INITIAL = '\ufe9f'
JEEM_MEDIAL = '\ufea0'
JEEM_ISOLATED = '\ufe9d'
JEEM_FINAL = '\ufe9e'

HAH_INITIAL = '\ufea3'
HAH_MEDIAL = '\ufea4'
HAH_ISOLATED = '\ufea1'
HAH_FINAL = '\ufea2'

KHAH_INITIAL = '\ufea7'
KHAH_MEDIAL = '\ufea8'
KHAH_ISOLATED = '\ufea5'
KHAH_FINAL = '\ufea6'

DAL_ISOLATED = '\ufea9'
DAL_FINAL = '\ufeaa'

THEL_ISOLATED = '\ufeab'
THEL_FINAL = '\ufeac'

REH_ISOLATED = '\ufead'
REH_FINAL = '\ufeae'

ZAIN_ISOLATED = '\ufeaf'
ZAIN_FINAL = '\ufeb0'

SEEN_INITIAL = '\ufeb3'
SEEN_MEDIAL = '\ufeb4'
SEEN_ISOLATED = '\ufeb1'
SEEN_FINAL = '\ufeb2'

SHEEN_INITIAL = '\ufeb7'
SHEEN_MEDIAL = '\ufeb8'
SHEEN_ISOLATED = '\ufeb5'
SHEEN_FINAL = '\ufeb6'

SAD_INITIAL = '\ufebb'
SAD_MEDIAL = '\ufebc'
SAD_ISOLATED = '\ufeb9'
SAD_FINAL = '\ufeba'

DAD_INITIAL = '\ufebf'
DAD_MEDIAL = '\ufec0'
DAD_ISOLATED = '\ufebd'
DAD_FINAL = '\ufebe'

TAH_INITIAL = '\ufec3'
TAH_MEDIAL = '\ufec4'
TAH_ISOLATED = '\ufec1'
TAH_FINAL = '\ufec2'

ZAH_INITIAL = '\ufec7'
ZAH_MEDIAL = '\ufec8'
ZAH_ISOLATED = '\ufec5'
ZAH_FINAL = '\ufec6'

AIN_INITIAL = '\ufecb'
AIN_MEDIAL = '\ufecc'
AIN_ISOLATED = '\ufec9'
AIN_FINAL = '\ufeca'

GHAIN_INITIAL = '\ufecf'
GHAIN_MEDIAL = '\ufed0'
GHAIN_ISOLATED = '\ufecd'
GHAIN_FINAL = '\ufece'

FEH_INITIAL = '\ufed3'
FEH_MEDIAL = '\ufed4'
FEH_ISOLATED = '\ufed1'
FEH_FINAL = '\ufed2'

QAF_INITIAL = '\ufed7'
QAF_MEDIAL = '\ufed8'
QAF_ISOLATED = '\ufed5'
QAF_FINAL = '\ufed6'

KAF_INITIAL = '\ufedb'
KAF_MEDIAL = '\ufedC'
KAF_ISOLATED = '\ufed9'
KAF_FINAL = '\ufeda'

LAM_INITIAL = '\ufedf'
LAM_MEDIAL = '\ufed0'
LAM_ISOLATED = '\ufedd'
LAM_FINAL = '\ufede'

MEEM_INITIAL = '\ufee3'
MEEM_MEDIAL = '\ufee4'
MEEM_ISOLATED = '\ufee1'
MEEM_FINAL = '\ufee2'

NOON_INITIAL = '\ufee7'
NOON_MEDIAL = '\ufee8'
NOON_ISOLATED = '\ufee5'
NOON_FINAL = '\ufee6'

HEH_INITIAL = '\ufeeb'
HEH_MEDIAL = '\ufeec'
HEH_ISOLATED = '\ufee9'
HEH_FINAL = '\ufeea'

WAW_ISOLATED = '\ufeed'
WAW_FINAL = '\ufeee'

ALEF_MAKSURA_ISOLATED = '\ufeef'
ALEF_MAKSURA_FINAL = '\ufef0'

YEH_INITIAL = '\ufef3'
YEH_MEDIAL = '\ufef4'
YEH_ISOLATED = '\ufef1'
YEH_FINAL = '\ufef2'

# Punctuation marks
COMMA = '\u060C'
SEMICOLON = '\u061B'
QUESTION = '\u061F'

# Kasheeda, Tatweel
KASHEEDA = '\u0640'

# Other symbols
PERCENT = '\u066a'
DECIMAL = '\u066b'
THOUSANDS = '\u066c'
STAR = '\u066d'
FULL_STOP = '\u06d4'
BYTE_ORDER_MARK = '\ufeff'

#Diacritics
FATHATAN = '\u064b'
DAMMATAN = '\u064c'
KASRATAN = '\u064d'
FATHA = '\u064e'
DAMMA = '\u064f'
KASRA = '\u0650'
SHADDA = '\u0651'
SUKUN = '\u0652'

# groups

HAMZAT = (  HAMZA,
            HAMZA_ABOVE_ALEF,
            HAMZA_BELOW_ALEF,
            ALEF_MADDA,
            HAMZA_ABOVE_WAW,
            HAMZA_ABOVE_YEH,
            HAMZA_ABOVE,
            HAMZA_BELOW
            )

ALEFAT = (
            ALEF,
            ALEF_MADDA,
            HAMZA_BELOW_ALEF,
            HAMZA_ABOVE_ALEF,
            ALEF_WASLA,
            ALEF_MAKSURA,
            SMALL_ALEF,
        )

WEAK = (ALEF,  WAW,  YEH,  ALEF_MAKSURA)

YEHLIKE = (YEH,   HAMZA_ABOVE_YEH, ALEF_MAKSURA, SMALL_YEH)

WAWLIKE = (WAW, HAMZA_ABOVE_WAW, SMALL_WAW)

TEHLIKE = (TEH, TEH_MARBUTA)

SMALL = (SMALL_ALEF, SMALL_WAW, SMALL_YEH)


LETTERS = (
        ALEF,  BEH,  TEH,  TEH_MARBUTA,  THEH,  JEEM,  HAH,  KHAH,
        DAL, THEL, REH,  ZAIN,  SEEN,  SHEEN,  SAD,  DAD,  TAH,  ZAH,
        AIN,  GHAIN,  FEH,  QAF,  KAF,  LAM,  MEEM,  NOON,  HEH,  WAW,  YEH,
        HAMZA,   ALEF_MADDA,  HAMZA_ABOVE_ALEF,  HAMZA_ABOVE_WAW,  HAMZA_BELOW_ALEF,
        HAMZA_ABOVE_YEH,
        )

TASHKEEL = (FATHATAN, DAMMATAN, KASRATAN,
            FATHA, DAMMA, KASRA,
            SUKUN, SHADDA
            )

HARAKAT = (FATHATAN, DAMMATAN, KASRATAN,
            FATHA, DAMMA, KASRA,
            SUKUN
            )

SHORTHARAKAT = (FATHA,   DAMMA,   KASRA,  SUKUN)

TANWEEN = (FATHATAN, DAMMATAN, KASRATAN)


NOT_DEF_HARAKA = KASHEEDA

LIGATURES_LAM_ALEF = (LAM_ALEF, LAM_ALEF_HAMZA_ABOVE, LAM_ALEF_HAMZA_BELOW, LAM_ALEF_MADDA_ABOVE)


ALPHABETIC_ORDER = {
                ALEF: 1,
                BEH: 2,
                TEH: 3,
                TEH_MARBUTA: 3,
                THEH: 4,
                JEEM: 5,
                HAH: 6,
                KHAH: 7,
                DAL: 8,
                THEL: 9,
                REH: 10,
                ZAIN: 11,
                SEEN: 12,
                SHEEN: 13,
                SAD: 14,
                DAD: 15,
                TAH: 16,
                ZAH: 17,
                AIN: 18,
                GHAIN: 19,
                FEH: 20,
                QAF: 21,
                KAF: 22,
                LAM: 23,
                MEEM: 24,
                NOON: 25,
                HEH: 26,
                WAW: 27,
                YEH: 28,
                HAMZA: 29,

                ALEF_MADDA: 29,
                HAMZA_ABOVE_ALEF: 29,
                HAMZA_ABOVE_WAW: 29,
                HAMZA_BELOW_ALEF: 29,
                HAMZA_ABOVE_YEH: 29,
                }

NAMES = {
                ALEF:  "ألف",
                BEH: "باء",
                TEH: 'تاء',
                TEH_MARBUTA: 'تاء مربوطة',
                THEH: 'ثاء',
                JEEM: 'جيم',
                HAH: 'حاء',
                KHAH: 'خاء',
                DAL: 'دال',
                THEL: 'ذال',
                REH: 'راء',
                ZAIN: 'زاي',
                SEEN: 'سين',
                SHEEN: 'شين',
                SAD: 'صاد',
                DAD: 'ضاد',
                TAH: 'طاء',
                ZAH: 'ظاء',
                AIN: 'عين',
                GHAIN: 'غين',
                FEH: 'فاء',
                QAF: 'قاف',
                KAF: 'كاف',
                LAM: 'لام',
                MEEM: 'ميم',
                NOON: 'نون',
                HEH: 'هاء',
                WAW: 'واو',
                YEH: 'ياء',
                HAMZA: 'همزة',

                KASHEEDA: 'تطويل',
                ALEF_MADDA: 'ألف ممدودة',
                ALEF_MAKSURA: 'ألف مقصورة',
                HAMZA_ABOVE_ALEF: 'همزة على الألف',
                HAMZA_ABOVE_WAW: 'همزة على الواو',
                HAMZA_BELOW_ALEF: 'همزة تحت الألف',
                HAMZA_ABOVE_YEH: 'همزة على الياء',
                FATHATAN: 'فتحتان',
                DAMMATAN: 'ضمتان',
                KASRATAN: 'كسرتان',
                FATHA: 'فتحة',
                DAMMA: 'ضمة',
                KASRA: 'كسرة',
                SHADDA: 'شدة',
                SUKUN: 'سكون',
                }

SHAPED_FORMS = {
                HAMZA: HAMZA_ISOLATED,
                HAMZA_ABOVE_ALEF: (ALEF_HAMZA_ABOVE_ISOLATED, ALEF_HAMZA_ABOVE_FINAL),
                HAMZA_BELOW_ALEF: (ALEF_HAMZA_BELOW_ISOLATED, ALEF_HAMZA_BELOW_FINAL),
                HAMZA_ABOVE_YEH: (YEH_HAMZA_ISOLATED, YEH_HAMZA_INITIAL, YEH_HAMZA_MEDIAL, YEH_HAMZA_FINAL),
                ALEF_MADDA: (ALEF_MADDA_ISOLATED, ALEF_MADDA_FINAL),
                HAMZA_ABOVE_WAW: (WAW_HAMZA_ISOLATED, WAW_HAMZA_FINAL),
                ALEF: (ALEF_ISOLATED, ALEF_FINAL),
                BEH: (BEH_ISOLATED, BEH_FINAL, BEH_INITIAL, BEH_MEDIAL),
                TEH_MARBUTA: (TEH_MARBUTA_ISOLATED, TEH_MARBUTA_FINAL),
                TEH: (TEH_ISOLATED, TEH_INITIAL, TEH_MEDIAL, TEH_FINAL),
                THEH: (THEH_ISOLATED, THEH_INITIAL, THEH_MEDIAL, THEH_FINAL),
                JEEM: (JEEM_ISOLATED, JEEM_INITIAL, JEEM_MEDIAL, JEEM_FINAL),
                HAH: (HAH_ISOLATED, HAH_INITIAL, HAH_MEDIAL, HAH_FINAL),
                KHAH: (KHAH_ISOLATED, KHAH_INITIAL, KHAH_MEDIAL, KHAH_FINAL),
                DAL: (DAL_ISOLATED, DAL_FINAL),
                THEL: (THEL_ISOLATED, THEL_FINAL),
                REH: (REH_ISOLATED, REH_FINAL),
                ZAIN: (ZAIN_ISOLATED, ZAIN_FINAL),
                SEEN: (SEEN_ISOLATED, SEEN_INITIAL, SEEN_MEDIAL, SEEN_FINAL),
                SHEEN: (SHEEN_ISOLATED, SHEEN_INITIAL, SHEEN_MEDIAL, SHEEN_FINAL),
                SAD: (SAD_ISOLATED, SAD_INITIAL, SAD_MEDIAL, SAD_FINAL),
                DAD: (DAD_ISOLATED, DAD_INITIAL, DAD_MEDIAL, DAD_FINAL),
                TAH: (TAH_ISOLATED, TAH_INITIAL, TAH_MEDIAL, TAH_FINAL),
                ZAH: (ZAH_ISOLATED, ZAH_INITIAL, ZAH_MEDIAL, ZAH_FINAL),
                AIN: (AIN_ISOLATED, AIN_INITIAL, AIN_MEDIAL, AIN_FINAL),
                GHAIN: (GHAIN_ISOLATED, GHAIN_INITIAL, GHAIN_MEDIAL, GHAIN_FINAL),
                FEH: (FEH_ISOLATED, FEH_INITIAL, FEH_MEDIAL, FEH_FINAL),
                QAF: (QAF_ISOLATED, QAF_INITIAL, QAF_MEDIAL, QAF_FINAL),
                KAF: (KAF_ISOLATED, KAF_INITIAL, KAF_MEDIAL, KAF_FINAL),
                LAM: (LAM_ISOLATED, LAM_INITIAL, LAM_MEDIAL, LAM_FINAL),
                MEEM: (MEEM_ISOLATED, MEEM_INITIAL, MEEM_MEDIAL, MEEM_FINAL),
                NOON: (NOON_ISOLATED, NOON_INITIAL, NOON_MEDIAL, NOON_FINAL),
                HEH: (HEH_ISOLATED, HEH_INITIAL, HEH_MEDIAL, HEH_FINAL),
                WAW: (WAW_ISOLATED, WAW_FINAL),
                ALEF_MAKSURA: (ALEF_MAKSURA_ISOLATED, ALEF_MAKSURA_FINAL),
                YEH: (YEH_ISOLATED, YEH_INITIAL, YEH_MEDIAL, YEH_FINAL),
                LAM_ALEF: (LAM_ALEF_ISOLATED, LAM_ALEF_FINAL),
                LAM_ALEF_HAMZA_ABOVE: (LAM_ALEF_HAMZA_ABOVE_ISOLATED, LAM_ALEF_HAMZA_ABOVE_FINAL),
                LAM_ALEF_HAMZA_BELOW: (LAM_ALEF_HAMZA_BELOW_ISOLATED, LAM_ALEF_HAMZA_BELOW_FINAL),
                LAM_ALEF_MADDA_ABOVE: (LAM_ALEF_MADDA_ABOVE_ISOLATED, LAM_ALEF_MADDA_ABOVE_FINAL)
                }


PUNCTUATION_MARKS = [COMMA, SEMICOLON, QUESTION]


WESTERN_ARABIC_NUMERALS = ['0','1','2','3','4','5','6','7','8','9']

EASTERN_ARABIC_NUMERALS = ['۰', '۱', '۲', '۳', '٤', '۵', '٦', '۷', '۸', '۹']
