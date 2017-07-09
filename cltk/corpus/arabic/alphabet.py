"""
   Arabic alphabet
   source 1 : pyarabic 'https://github.com/linuxscout/pyarabic'
   source 2 : arabicstemmer 'https://github.com/assem-ch/arabicstemmer/blob/master/algorithm/stemmer.sbl'
"""
__author__ = 'Lakhdar Benzahia <lakhdar[.]benzahia[at]gmail[.]com>'

# Arabic letters

# Hamza letter
HAMZA = u'\u0621'
HAMZA_ABOVE_ALEF = u'\u0623'
HAMZA_BELOW_ALEF = u'\u0625'
ALEF_MADDA = u'\u0622'
HAMZA_ABOVE_WAW = u'\u0624'
HAMZA_ABOVE_YEH = u'\u0626'

ALEF = u'\u0627'
ALEF_MAKSURA = u'\u0649'
BEH = u'\u0628'
TEH_MARBUTA = u'\u0629'
TEH = u'\u062a'
THEH = u'\u062b'
JEEM = u'\u062c'
HAH = u'\u062d'
KHAH = u'\u062e'
DAL = u'\u062f'
THEL = u'\u0630'
REH = u'\u0631'
ZAIN = u'\u0632'
SEEN = u'\u0633'
SHEEN = u'\u0634'
SAD = u'\u0635'
DAD = u'\u0636'
TAH = u'\u0637'
ZAH = u'\u0638'
AIN = u'\u0639'
GHAIN = u'\u063a'
FEH = u'\u0641'
QAF = u'\u0642'
KAF = u'\u0643'
LAM = u'\u0644'
MEEM = u'\u0645'
NOON = u'\u0646'
HEH = u'\u0647'
WAW =  u'\u0648'
YEH =  u'\u064a'

MINI_ALEF = u'\u0670'
ALEF_WASLA  = u'\u0671'
MADDA_ABOVE = u'\u0653'
HAMZA_ABOVE = u'\u0654'
HAMZA_BELOW = u'\u0655'

# Small Letters
SMALL_ALEF = u"\u0670"
SMALL_WAW = u"\u06E5"
SMALL_YEH  = u"\u06E6"

# Ligatures Lam-Alef
LAM_ALEF = u'\ufefb'
LAM_ALEF_HAMZA_ABOVE = u'\ufef7'
LAM_ALEF_HAMZA_BELOW = u'\ufef9'
LAM_ALEF_MADDA_ABOVE = u'\ufef5'


SIMPLE_LAM_ALEF = u'\u0644\u0627'
SIMPLE_LAM_ALEF_HAMZA_ABOVE = u'\u0644\u0623'
SIMPLE_LAM_ALEF_HAMZA_BELOW = u'\u0644\u0625'
SIMPLE_LAM_ALEF_MADDA_ABOVE = u'\u0644\u0622'

# shaped forms
LAM_ALEF_ISOLATED = u'\ufefb'
LAM_ALEF_FINAL = u'\ufefc'

LAM_ALEF_HAMZA_ABOVE_ISOLATED = u'\ufef7'
LAM_ALEF_HAMZA_ABOVE_FINAL = u'\ufef8'

LAM_ALEF_HAMZA_BELOW_ISOLATED = u'\ufef9'
LAM_ALEF_HAMZA_BELOW_FINAL = u'\ufefa'

LAM_ALEF_MADDA_ABOVE_ISOLATED = u'\ufef5'
LAM_ALEF_MADDA_ABOVE_FINAL = u'\ufef6'

HAMZA_ISOLATED = u'\ufe80'

ALEF_HAMZA_ABOVE_ISOLATED = u'\ufe83'
ALEF_HAMZA_ABOVE_FINAL = u'\ufe84'

ALEF_HAMZA_BELOW_ISOLATED = u'\ufe87'
ALEF_HAMZA_BELOW_FINAL = u'\ufe88'

YEH_HAMZA_INITIAL = u'\ufe8b'
YEH_HAMZA_MEDIAL = u'\ufe8c'
YEH_HAMZA_ISOLATED = u'\ufe89'
YEH_HAMZA_FINAL = u'\ufe8a'

ALEF_MADDA_ISOLATED = u'\ufe81'
ALEF_MADDA_FINAL = u'\ufe82'

WAW_HAMZA_ISOLATED = u'\ufe85'
WAW_HAMZA_FINAL = u'\ufe86'

ALEF_ISOLATED = u'\ufe8d'
ALEF_FINAL = u'\ufe8e'

BEH_ISOLATED = u'\ufe8f'
BEH_FINAL = u'\ufe90'
BEH_INITIAL = u'\ufe91'
BEH_MEDIAL = u'\ufe92'

TEH_MARBUTA_ISOLATED = u'\ufe93'
TEH_MARBUTA_FINAL = u'\ufe94'

TEH_INITIAL = u'\ufe97'
TEH_MEDIAL = u'\ufe98'
TEH_ISOLATED = u'\ufe95'
TEH_FINAL = u'\ufe96'

THEH_INITIAL = u'\ufe9b'
THEH_MEDIAL = u'\ufe9c'
THEH_FINAL = u'\ufe9a'
THEH_ISOLATED = u'\ufe99'

JEEM_INITIAL = u'\ufe9f'
JEEM_MEDIAL = u'\ufea0'
JEEM_ISOLATED = u'\ufe9d'
JEEM_FINAL = u'\ufe9e'

HAH_INITIAL = u'\ufea3'
HAH_MEDIAL = u'\ufea4'
HAH_ISOLATED = u'\ufea1'
HAH_FINAL = u'\ufea2'

KHAH_INITIAL = u'\ufea7'
KHAH_MEDIAL = u'\ufea8'
KHAH_ISOLATED = u'\ufea5'
KHAH_FINAL = u'\ufea6'

DAL_ISOLATED = u'\ufea9'
DAL_FINAL = u'\ufeaa'

THEL_ISOLATED = u'\ufeab'
THEL_FINAL = u'\ufeac'

REH_ISOLATED = u'\ufead'
REH_FINAL = u'\ufeae'

ZAIN_ISOLATED = u'\ufeaf'
ZAIN_FINAL = u'\ufeb0'

SEEN_INITIAL = u'\ufeb3'
SEEN_MEDIAL = u'\ufeb4'
SEEN_ISOLATED = u'\ufeb1'
SEEN_FINAL = u'\ufeb2'

SHEEN_INITIAL = u'\ufeb7'
SHEEN_MEDIAL = u'\ufeb8'
SHEEN_ISOLATED = u'\ufeb5'
SHEEN_FINAL = u'\ufeb6'

SAD_INITIAL = u'\ufebb'
SAD_MEDIAL = u'\ufebc'
SAD_ISOLATED = u'\ufeb9'
SAD_FINAL = u'\ufeba'

DAD_INITIAL = u'\ufebf'
DAD_MEDIAL = u'\ufec0'
DAD_ISOLATED = u'\ufebd'
DAD_FINAL = u'\ufebe'

TAH_INITIAL = u'\ufec3'
TAH_MEDIAL = u'\ufec4'
TAH_ISOLATED = u'\ufec1'
TAH_FINAL = u'\ufec2'

ZAH_INITIAL = u'\ufec7'
ZAH_MEDIAL = u'\ufec8'
ZAH_ISOLATED = u'\ufec5'
ZAH_FINAL = u'\ufec6'

AIN_INITIAL = u'\ufecb'
AIN_MEDIAL = u'\ufecc'
AIN_ISOLATED = u'\ufec9'
AIN_FINAL = u'\ufeca'

GHAIN_INITIAL = u'\ufecf'
GHAIN_MEDIAL = u'\ufed0'
GHAIN_ISOLATED = u'\ufecd'
GHAIN_FINAL = u'\ufece'

FEH_INITIAL = u'\ufed3'
FEH_MEDIAL = u'\ufed4'
FEH_ISOLATED = u'\ufed1'
FEH_FINAL = u'\ufed2'

QAF_INITIAL = u'\ufed7'
QAF_MEDIAL = u'\ufed8'
QAF_ISOLATED = u'\ufed5'
QAF_FINAL = u'\ufed6'

KAF_INITIAL = u'\ufedb'
KAF_MEDIAL = u'\ufedC'
KAF_ISOLATED = u'\ufed9'
KAF_FINAL = u'\ufeda'

LAM_INITIAL = u'\ufedf'
LAM_MEDIAL = u'\ufed0'
LAM_ISOLATED = u'\ufedd'
LAM_FINAL = u'\ufede'

MEEM_INITIAL = u'\ufee3'
MEEM_MEDIAL = u'\ufee4'
MEEM_ISOLATED = u'\ufee1'
MEEM_FINAL = u'\ufee2'

NOON_INITIAL = u'\ufee7'
NOON_MEDIAL = u'\ufee8'
NOON_ISOLATED = u'\ufee5'
NOON_FINAL = u'\ufee6'

HEH_INITIAL = u'\ufeeb'
HEH_MEDIAL = u'\ufeec'
HEH_ISOLATED = u'\ufee9'
HEH_FINAL = u'\ufeea'

WAW_ISOLATED = u'\ufeed'
WAW_FINAL = u'\ufeee'

ALEF_MAKSURA_ISOLATED = u'\ufeef'
ALEF_MAKSURA_FINAL = u'\ufef0'

YEH_INITIAL = u'\ufef3'
YEH_MEDIAL = u'\ufef4'
YEH_ISOLATED = u'\ufef1'
YEH_FINAL = u'\ufef2'

# Punctuation marks
COMMA = u'\u060C'
SEMICOLON = u'\u061B'
QUESTION = u'\u061F'

# Kasheeda, Tatweel
KASHEEDA = u'\u0640'

# Other symbols
PERCENT = u'\u066a'
DECIMAL = u'\u066b'
THOUSANDS = u'\u066c'
STAR = u'\u066d'
FULL_STOP = u'\u06d4'
BYTE_ORDER_MARK = u'\ufeff'

#Diacritics
FATHATAN = u'\u064b'
DAMMATAN = u'\u064c'
KASRATAN = u'\u064d'
FATHA = u'\u064e'
DAMMA = u'\u064f'
KASRA = u'\u0650'
SHADDA = u'\u0651'
SUKUN = u'\u0652'

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


LETTERS = u''.join([
        ALEF,  BEH,  TEH,  TEH_MARBUTA,  THEH,  JEEM,  HAH,  KHAH,
        DAL, THEL, REH,  ZAIN,  SEEN,  SHEEN,  SAD,  DAD,  TAH,  ZAH,
        AIN,  GHAIN,  FEH,  QAF,  KAF,  LAM,  MEEM,  NOON,  HEH,  WAW,  YEH,
        HAMZA,   ALEF_MADDA,  HAMZA_ABOVE_ALEF,  HAMZA_ABOVE_WAW,  HAMZA_BELOW_ALEF,
        HAMZA_ABOVE_YEH,
        ])

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
                ALEF:  u"ألف",
                BEH: u"باء",
                TEH: u'تاء',
                TEH_MARBUTA: u'تاء مربوطة',
                THEH: u'ثاء',
                JEEM: u'جيم',
                HAH: u'حاء',
                KHAH: u'خاء',
                DAL: u'دال',
                THEL: u'ذال',
                REH: u'راء',
                ZAIN: u'زاي',
                SEEN: u'سين',
                SHEEN: u'شين',
                SAD: u'صاد',
                DAD: u'ضاد',
                TAH: u'طاء',
                ZAH: u'ظاء',
                AIN: u'عين',
                GHAIN: u'غين',
                FEH: u'فاء',
                QAF: u'قاف',
                KAF: u'كاف',
                LAM: u'لام',
                MEEM: u'ميم',
                NOON: u'نون',
                HEH: u'هاء',
                WAW: u'واو',
                YEH: u'ياء',
                HAMZA: u'همزة',

                KASHEEDA: u'تطويل',
                ALEF_MADDA: u'ألف ممدودة',
                ALEF_MAKSURA: u'ألف مقصورة',
                HAMZA_ABOVE_ALEF: u'همزة على الألف',
                HAMZA_ABOVE_WAW: u'همزة على الواو',
                HAMZA_BELOW_ALEF: u'همزة تحت الألف',
                HAMZA_ABOVE_YEH: u'همزة على الياء',
                FATHATAN: u'فتحتان',
                DAMMATAN: u'ضمتان',
                KASRATAN: u'كسرتان',
                FATHA: u'فتحة',
                DAMMA: u'ضمة',
                KASRA: u'كسرة',
                SHADDA: u'شدة',
                SUKUN: u'سكون',
                }

HAMZAT_STRING = u"".join(HAMZAT)

HARAKAT_STRING = u"".join(HARAKAT)

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
