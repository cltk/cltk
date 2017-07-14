#!/usr/bin/python
# -*- coding=utf-8 -*-
"""
Arabic module

Features:
=========

    * Arabic letters classification
    * Text tokenization
    * Strip Harakat ( all, except Shadda, tatweel, last_haraka)
    * Sperate and  join Letters and Harakat
    * Reduce tashkeel
    * Mesure tashkeel similarity ( Harakats, fully or partially vocalized, similarity with a template)
    * Letters normalization ( Ligatures and Hamza)

@author: Taha Zerrouki
@contact: taha dot zerrouki at gmail dot com
@copyright: Arabtechies,  Arabeyes,   Taha Zerrouki
@license: GPL
@date:2010/03/01
@version: 0.1
"""
from __future__ import absolute_import

import re

if __name__ == "__main__":
    import stack
else:
    from cltk.support.arabic.pyarabic import stack

__author__ = 'Lakhdar Benzahia, <lakhdar.benzahia@gmail.com>'
__reviewers__ = ['Taha Zerrouki taha.zerrouki@gmail.com', 'Kyle P. Johnson <kyle@kyle-p-johnson.com>']


COMMA = u'\u060C'
SEMICOLON = u'\u061B'
QUESTION = u'\u061F'
HAMZA = u'\u0621'
ALEF_MADDA = u'\u0622'
ALEF_HAMZA_ABOVE = u'\u0623'
WAW_HAMZA = u'\u0624'
ALEF_HAMZA_BELOW = u'\u0625'
YEH_HAMZA = u'\u0626'
ALEF = u'\u0627'
BEH = u'\u0628'
TEH_MARBUTA = u'\u0629'
TEH = u'\u062a'
THEH = u'\u062b'
JEEM = u'\u062c'
HAH = u'\u062d'
KHAH = u'\u062e'
DAL = u'\u062f'
THAL = u'\u0630'
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
TATWEEL = u'\u0640'
FEH = u'\u0641'
QAF = u'\u0642'
KAF = u'\u0643'
LAM = u'\u0644'
MEEM = u'\u0645'
NOON = u'\u0646'
HEH = u'\u0647'
WAW = u'\u0648'
ALEF_MAKSURA = u'\u0649'
YEH = u'\u064a'
MADDA_ABOVE = u'\u0653'
HAMZA_ABOVE = u'\u0654'
HAMZA_BELOW = u'\u0655'
ZERO = u'\u0660'
ONE = u'\u0661'
TWO = u'\u0662'
THREE = u'\u0663'
FOUR = u'\u0664'
FIVE = u'\u0665'
SIX = u'\u0666'
SEVEN = u'\u0667'
EIGHT = u'\u0668'
NINE = u'\u0669'
PERCENT = u'\u066a'
DECIMAL = u'\u066b'
THOUSANDS = u'\u066c'
STAR = u'\u066d'
MINI_ALEF = u'\u0670'
ALEF_WASLA = u'\u0671'
FULL_STOP = u'\u06d4'
BYTE_ORDER_MARK = u'\ufeff'

# Diacritics
FATHATAN = u'\u064b'
DAMMATAN = u'\u064c'
KASRATAN = u'\u064d'
FATHA = u'\u064e'
DAMMA = u'\u064f'
KASRA = u'\u0650'
SHADDA = u'\u0651'
SUKUN = u'\u0652'

# Small Letters
SMALL_ALEF = u"\u0670"
SMALL_WAW = u"\u06E5"
SMALL_YEH = u"\u06E6"
# Ligatures
LAM_ALEF = u'\ufefb'
LAM_ALEF_HAMZA_ABOVE = u'\ufef7'
LAM_ALEF_HAMZA_BELOW = u'\ufef9'
LAM_ALEF_MADDA_ABOVE = u'\ufef5'
SIMPLE_LAM_ALEF = u'\u0644\u0627'
SIMPLE_LAM_ALEF_HAMZA_ABOVE = u'\u0644\u0623'
SIMPLE_LAM_ALEF_HAMZA_BELOW = u'\u0644\u0625'
SIMPLE_LAM_ALEF_MADDA_ABOVE = u'\u0644\u0622'
# groups
LETTERS = u''.join([
    ALEF, BEH, TEH, TEH_MARBUTA, THEH, JEEM, HAH, KHAH,
    DAL, THAL, REH, ZAIN, SEEN, SHEEN, SAD, DAD, TAH, ZAH,
    AIN, GHAIN, FEH, QAF, KAF, LAM, MEEM, NOON, HEH, WAW, YEH,
    HAMZA, ALEF_MADDA, ALEF_HAMZA_ABOVE, WAW_HAMZA, ALEF_HAMZA_BELOW,
    YEH_HAMZA,
])

TASHKEEL = (FATHATAN, DAMMATAN, KASRATAN,
            FATHA, DAMMA, KASRA,
            SUKUN,
            SHADDA)
HARAKAT = (FATHATAN, DAMMATAN, KASRATAN,
           FATHA, DAMMA, KASRA,
           SUKUN
           )
SHORTHARAKAT = (FATHA, DAMMA, KASRA, SUKUN)

TANWIN = (FATHATAN, DAMMATAN, KASRATAN)

NOT_DEF_HARAKA = TATWEEL
LIGUATURES = (
    LAM_ALEF,
    LAM_ALEF_HAMZA_ABOVE,
    LAM_ALEF_HAMZA_BELOW,
    LAM_ALEF_MADDA_ABOVE,
)
HAMZAT = (HAMZA, WAW_HAMZA, YEH_HAMZA, HAMZA_ABOVE, HAMZA_BELOW,
          ALEF_HAMZA_BELOW, ALEF_HAMZA_ABOVE,
          )
ALEFAT = (ALEF, ALEF_MADDA, ALEF_HAMZA_ABOVE,
          ALEF_HAMZA_BELOW, ALEF_WASLA, ALEF_MAKSURA, SMALL_ALEF,
          )
WEAK = (ALEF, WAW, YEH, ALEF_MAKSURA)
YEHLIKE = (YEH, YEH_HAMZA, ALEF_MAKSURA, SMALL_YEH)

WAWLIKE = (WAW, WAW_HAMZA, SMALL_WAW)
TEHLIKE = (TEH, TEH_MARBUTA)

SMALL = (SMALL_ALEF, SMALL_WAW, SMALL_YEH)
MOON = (HAMZA, ALEF_MADDA, ALEF_HAMZA_ABOVE, ALEF_HAMZA_BELOW,
        ALEF, BEH, JEEM, HAH, KHAH, AIN, GHAIN,
        FEH, QAF, KAF, MEEM, HEH, WAW, YEH)

SUN = (TEH, THEH, DAL, THAL, REH, ZAIN, SEEN, SHEEN,
       SAD, DAD, TAH, ZAH, LAM, NOON,)

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
    THAL: 9,
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
    ALEF_HAMZA_ABOVE: 29,
    WAW_HAMZA: 29,
    ALEF_HAMZA_BELOW: 29,
    YEH_HAMZA: 29,
}
NAMES = {
    ALEF: u"ألف",
    BEH: u"باء",
    TEH: u'تاء',
    TEH_MARBUTA: u'تاء مربوطة',
    THEH: u'ثاء',
    JEEM: u'جيم',
    HAH: u'حاء',
    KHAH: u'خاء',
    DAL: u'دال',
    THAL: u'ذال',
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

    TATWEEL: u'تطويل',
    ALEF_MADDA: u'ألف ممدودة',
    ALEF_MAKSURA: u'ألف مقصورة',
    ALEF_HAMZA_ABOVE: u'همزة على الألف',
    WAW_HAMZA: u'همزة على الواو',
    ALEF_HAMZA_BELOW: u'همزة تحت الألف',
    YEH_HAMZA: u'همزة على الياء',
    FATHATAN: u'فتحتان',
    DAMMATAN: u'ضمتان',
    KASRATAN: u'كسرتان',
    FATHA: u'فتحة',
    DAMMA: u'ضمة',
    KASRA: u'كسرة',
    SHADDA: u'شدة',
    SUKUN: u'سكون',
}
# regular expretion

HARAKAT_PATTERN = re.compile(u"[" + u"".join(HARAKAT) + u"]", re.UNICODE)
# ~ """ pattern to strip Harakat"""
LASTHARAKA_PATTERN = \
    re.compile(u"[%s]$|[%s]" % (u"".join(HARAKAT), u''.join(TANWIN)), re.UNICODE)
# ~ """ Pattern to strip only the last haraka """
SHORTHARAKAT_PATTERN = \
    re.compile(u"[" + u"".join(SHORTHARAKAT) + u"]", re.UNICODE)
# ~ Pattern to lookup Short Harakat(Fatha, Damma, Kasra, sukun, tanwin),
# but not shadda
TASHKEEL_PATTERN = re.compile(u"[" + u"".join(TASHKEEL) + u"]", re.UNICODE)
# ~ """ Harakat and shadda pattern  """
HAMZAT_PATTERN = re.compile(u"[" + u"".join(HAMZAT) + u"]", re.UNICODE)
# ~ """ all hamzat pattern"""
ALEFAT_PATTERN = re.compile(u"[" + u"".join(ALEFAT) + u"]", re.UNICODE)
# ~ """ all alef like letters """
LIGUATURES_PATTERN = re.compile(u"[" + u"".join(LIGUATURES) + u"]", re.UNICODE)
# ~ """ all liguatures pattern """
TOKEN_PATTERN = re.compile(u"([\w%s]+)" % u"".join(TASHKEEL), re.UNICODE)
TOKEN_REPLACE = re.compile('\t|\r|\f|\v| ')


# ~ """ pattern to tokenize a text"""
################################################
# { is letter functions
################################################
def is_sukun(archar):
    """Checks for Arabic Sukun Mark.
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar == SUKUN


def is_shadda(archar):
    """Checks for Arabic Shadda Mark.
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar == SHADDA


def is_tatweel(archar):
    """Checks for Arabic Tatweel letter modifier.
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar == TATWEEL


def is_tanwin(archar):
    """Checks for Arabic Tanwin Marks (FATHATAN,  DAMMATAN,  KASRATAN).
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in TANWIN


def is_tashkeel(archar):
    """Checks for Arabic Tashkeel Marks (
        - FATHA, DAMMA, KASRA,  SUKUN,
        - SHADDA,
        - FATHATAN, DAMMATAN,  KASRATAn).
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in TASHKEEL


def is_haraka(archar):
    """Checks for Arabic Harakat Marks (FATHA, DAMMA, KASRA, SUKUN, TANWIN).
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in HARAKAT


def is_shortharaka(archar):
    """Checks for Arabic  short Harakat Marks (FATHA, DAMMA, KASRA, SUKUN).
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in SHORTHARAKAT


def is_ligature(archar):
    """Checks for Arabic  Ligatures like LamAlef.
    (LAM_ALEF,  LAM_ALEF_HAMZA_ABOVE,  LAM_ALEF_HAMZA_BELOW,  LAM_ALEF_MADDA_ABOVE)
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in LIGUATURES


def is_hamza(archar):
    """Checks for Arabic  Hamza forms.
    HAMZAT are (HAMZA,  WAW_HAMZA,  YEH_HAMZA,  HAMZA_ABOVE,  HAMZA_BELOW, ALEF_HAMZA_BELOW,  ALEF_HAMZA_ABOVE )
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in HAMZAT


def is_alef(archar):
    """Checks for Arabic Alef forms.
    ALEFAT = (ALEF,  ALEF_MADDA,  ALEF_HAMZA_ABOVE,  ALEF_HAMZA_BELOW, ALEF_WASLA,  ALEF_MAKSURA )
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in ALEFAT


def is_yehlike(archar):
    """Checks for Arabic Yeh forms.
    Yeh forms : YEH,  YEH_HAMZA,  SMALL_YEH,  ALEF_MAKSURA
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in YEHLIKE


def is_wawlike(archar):
    """Checks for Arabic Waw like forms.
    Waw forms : WAW,  WAW_HAMZA,  SMALL_WAW
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in WAWLIKE


def is_teh(archar):
    """Checks for Arabic Teh forms.
    Teh forms : TEH,  TEH_MARBUTA
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in TEHLIKE


def is_small(archar):
    """Checks for Arabic Small letters.
    SMALL Letters : SMALL ALEF,  SMALL WAW,  SMALL YEH
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in SMALL


def is_weak(archar):
    """Checks for Arabic Weak letters.
    Weak Letters : ALEF,  WAW,  YEH,  ALEF_MAKSURA
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in WEAK


def is_moon(archar):
    """Checks for Arabic Moon letters.
    Moon Letters :
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in MOON


def is_sun(archar):
    """Checks for Arabic Sun letters.
    Moon Letters :
    @param archar: arabic unicode char
    @type archar: unicode
    @return:
    @rtype:Boolean
    """
    return archar in SUN


#####################################
# { general  letter functions
#####################################
def order(archar):
    """return Arabic letter order between 1 and 29.
    Alef order is 1,  Yeh is 28,  Hamza is 29.
    Teh Marbuta has the same ordre with Teh,  3.
    @param archar: arabic unicode char
    @type archar: unicode
    @return: arabic order.
    @rtype: integer
    """
    return ALPHABETIC_ORDER.get(archar, 0)


def name(archar):
    """return Arabic letter name in arabic.     Alef order is 1,  Yeh is 28,
    Hamza is 29. Teh Marbuta has the same ordre with Teh,  3.
    @param archar: arabic unicode char
    @type archar: unicode
    @return: arabic name.
    @rtype: unicode
    """
    return NAMES.get(archar, u'')


def arabicrange():
    u"""return a list of arabic characteres .
    Return a list of characteres between \u060c to \u0652
    @return: list of arabic characteres.
    @rtype: unicode
    """
    mylist = []
    for i in range(0x0600, 0x00653):
        try:
            mylist.append(unichr(i))
        except NameError:
            # python 3 compatible
            mylist.append(chr(i))
        except ValueError:
            pass
    return mylist


#####################################
# { Has letter functions
#####################################
def has_shadda(word):
    """Checks if the arabic word  contains shadda.
    @param word: arabic unicode char
    @type word: unicode
    @return: if shadda exists
    @rtype:Boolean
    """
    if re.search(SHADDA, word):
        return True
    return False


#####################################
# { word and text functions
#####################################
def is_vocalized(word):
    """Checks if the arabic word is vocalized.
    the word musn't  have any spaces and pounctuations.
    @param word: arabic unicode char
    @type word: unicode
    @return: if the word is vocalized
    @rtype:Boolean
    """
    if word.isalpha():
        return False
    for char in word:
        if is_tashkeel(char):
            return True
    else:
        return False


def is_vocalizedtext(text):
    """Checks if the arabic text is vocalized.
    The text can contain many words and spaces
    @param text: arabic unicode char
    @type text: unicode
    @return: if the word is vocalized
    @rtype:Boolean
    """
    if re.search(HARAKAT_PATTERN, text):
        return True
    else:
        return False


def is_arabicstring(text):
    """ Checks for an  Arabic standard Unicode block characters
    An arabic string can contain spaces,  digits and pounctuation.
    but only arabic standard characters,  not extended arabic
    @param text: input text
    @type text: unicode
    @return: True if all charaters are in Arabic block
    @rtype: Boolean
    """
    if re.search(u"([^\u0600-\u0652%s%s%s\s\d])" \
                         % (LAM_ALEF, LAM_ALEF_HAMZA_ABOVE, LAM_ALEF_MADDA_ABOVE), text):
        return False
    return True


def is_arabicrange(text):
    """ Checks for an  Arabic Unicode block characters
    @param text: input text
    @type text: unicode
    @return: True if all charaters are in Arabic block
    @rtype: Boolean
    """
    if re.search(u"([^\u0600-\u06ff\ufb50-\ufdff\ufe70-\ufeff\u0750-\u077f])", \
                 text):
        return False
    return True


def is_arabicword(word):
    """ Checks for an valid Arabic  word.
    An Arabic word not contains spaces,  digits and pounctuation
    avoid some spelling error,   TEH_MARBUTA must be at the end.
    @param word: input word
    @type word: unicode
    @return: True if all charaters are in Arabic block
    @rtype: Boolean
    """
    if len(word) == 0:
        return False
    elif re.search(u"([^\u0600-\u0652%s%s%s])" \
                           % (LAM_ALEF, LAM_ALEF_HAMZA_ABOVE, LAM_ALEF_MADDA_ABOVE), word):
        return False
    elif is_haraka(word[0]) or word[0] in (WAW_HAMZA, YEH_HAMZA):
        return False
    # if Teh Marbuta or Alef_Maksura not in the end
    elif re.match(u"^(.)*[%s](.)+$" % ALEF_MAKSURA, word):
        return False
    elif re.match(u"^(.)*[%s]([^%s%s%s])(.)+$" % \
                          (TEH_MARBUTA, DAMMA, KASRA, FATHA), word):
        return False
    else:
        return True


#####################################
# {Char functions
#####################################
def first_char(word):
    """
    Return the first char
    @param word: given word
    @type word: unicode
    @return: the first char
    @rtype: unicode char
    """
    return word[0]


def second_char(word):
    """
    Return the second char
    @param word: given word
    @type word: unicode
    @return: the first char
    @rtype: unicode char
    """
    return word[1:2]


def last_char(word):
    """
    Return the last letter
    example: zerrouki; 'i' is the last.
    @param word: given word
    @type word: unicode
    @return: the last letter
    @rtype: unicode char
    """
    return word[-1:]


def secondlast_char(word):
    """
    Return the second last letter example: zerrouki; 'k' is the second last.
    @param word: given word
    @type word: unicode
    @return: the second last letter
    @rtype: unicode char
    """
    return word[-2:-1]


#####################################
# {Strip functions
#####################################
def strip_harakat(text):
    """Strip Harakat from arabic word except Shadda.
    The striped marks are :
        - FATHA,  DAMMA,  KASRA
        - SUKUN
        - FATHATAN,  DAMMATAN,  KASRATAN,


    @param text: arabic text.
    @type text: unicode.
    @return: return a striped text.
    @rtype: unicode.
    """
    # if text:
    # return  re.sub(HARAKAT_PATTERN, u'', text)
    # return text
    if not text:
        return text
    elif is_vocalized(text):
        for char in HARAKAT:
            text = text.replace(char, '')
    return text


def strip_lastharaka(text):
    """Strip the last Haraka from arabic word except Shadda.
    The striped marks are :
        - FATHA,  DAMMA,  KASRA
        - SUKUN
        - FATHATAN,  DAMMATAN,  KASRATAN

    @param text: arabic text.
    @type text: unicode.
    @return: return a striped text.
    @rtype: unicode.
    """
    if text:
        if is_vocalized(text):
            return re.sub(LASTHARAKA_PATTERN, u'', text)
    return text


def strip_tashkeel(text):
    """Strip vowels from a text,  include Shadda.
    The striped marks are :
        - FATHA,  DAMMA,  KASRA
        - SUKUN
        - SHADDA
        - FATHATAN,  DAMMATAN,  KASRATAN,  ,  ,  .

    @param text: arabic text.
    @type text: unicode.
    @return: return a striped text.
    @rtype: unicode.
    """
    if not text:
        return text
    elif is_vocalized(text):
        for char in TASHKEEL:
            text = text.replace(char, '')
    return text


def strip_tatweel(text):
    """
    Strip tatweel from a text and return a result text.

    @param text: arabic text.
    @type text: unicode.
    @return: return a striped text.
    @rtype: unicode.

    """
    return text.replace(TATWEEL, '')


def strip_shadda(text):
    """
    Strip Shadda from a text and return a result text.

    @param text: arabic text.
    @type text: unicode.
    @return: return a striped text.
    @rtype: unicode.
    """
    return text.replace(SHADDA, '')


def normalize_ligature(text):
    """Normalize Lam Alef ligatures into two letters (LAM and ALEF),
    and Tand return a result text.
    Some systems present lamAlef ligature as a single letter,
    this function convert it into two letters,
    The converted letters into  LAM and ALEF are :
        - LAM_ALEF,  LAM_ALEF_HAMZA_ABOVE,  LAM_ALEF_HAMZA_BELOW,  LAM_ALEF_MADDA_ABOVE

    @param text: arabic text.
    @type text: unicode.
    @return: return a converted text.
    @rtype: unicode.
    """
    if text:
        return LIGUATURES_PATTERN.sub(u'%s%s' % (LAM, ALEF), text)
    return text


def normalize_hamza(word):
    """Standardize the Hamzat into one form of hamza,
    replace Madda by hamza and alef.
    Replace the LamAlefs by simplified letters.

    @param word: arabic text.
    @type word: unicode.
    @return: return a converted text.
    @rtype: unicode.
    """
    if word.startswith(ALEF_MADDA):
        if len(word) >= 3 and (word[1] not in HARAKAT) and \
                (word[2] == SHADDA or len(word) == 3):
            word = HAMZA + ALEF + word[1:]
        else:
            word = HAMZA + HAMZA + word[1:]
    # convert all Hamza from into one form
    word = word.replace(ALEF_MADDA, HAMZA + HAMZA)
    word = HAMZAT_PATTERN.sub(HAMZA, word)
    return word


def separate(word, extract_shadda=False):
    """
    separate the letters from the vowels,  in arabic word,
    if a letter hasn't a haraka,  the not definited haraka is attributed.
    return ( letters, vowels)
    @param word: the input word
    @type word: unicode
    @param extract_shadda: extract shadda as seperate text
    @type extract_shadda: Boolean
    @return: ( letters, vowels)
    @rtype:couple of unicode
    """
    stack1 = stack.Stack(word)
    # the word is inversed in the stack
    stack1.items.reverse()
    letters = stack.Stack()
    marks = stack.Stack()
    vowels = HARAKAT
    last1 = stack1.pop()
    # if the last element must be a letter,
    # the arabic word can't starts with a haraka
    # in th stack the word is inversed
    while last1 in vowels:
        last1 = stack1.pop()
    while last1 != None:
        if last1 in vowels:
            # we can't have two harakats beside.
            # the shadda is considered as a letter
            marks.pop()
            marks.push(last1)
        elif last1 == SHADDA:
            # is the element is a Shadda,
            # the previous letter must have a sukun as mark,
            # and the shadda take the indefinate  mark
            marks.pop()
            marks.push(SUKUN)
            marks.push(NOT_DEF_HARAKA)
            letters.push(SHADDA)
        else:
            marks.push(NOT_DEF_HARAKA)
            letters.push(last1)
        last1 = stack1.pop()
    if extract_shadda:
        # the shadda is considered as letter
        wordletters = u''.join(letters.items)
        # print wordletters.encode('utf8')
        shaddaplaces = re.sub(u'[^%s]' % SHADDA, TATWEEL, wordletters)
        shaddaplaces = re.sub(u'%s%s' % (TATWEEL, SHADDA), SHADDA, shaddaplaces)
        # print wordletters.encode('utf8')
        wordletters = strip_shadda(wordletters)
        # print wordletters.encode('utf8')
        return (wordletters, u''.join(marks.items), shaddaplaces)
    else:
        return (u''.join(letters.items), u''.join(marks.items))


def joint(letters, marks):
    """ joint the letters with the marks
    the length ot letters and marks must be equal
    return word
    @param letters: the word letters
    @type letters: unicode
    @param marks: the word marks
    @type marks: unicode
    @return: word
    @rtype: unicode
    """
    # The length ot letters and marks must be equal
    if len(letters) != len(marks):
        return ""
    stack_letter = stack.Stack(letters)
    stack_letter.items.reverse()
    stack_mark = stack.Stack(marks)
    stack_mark.items.reverse()

    word_stack = stack.Stack()
    last_letter = stack_letter.pop()
    last_mark = stack_mark.pop()
    vowels = HARAKAT
    while last_letter != None and last_mark != None:
        if last_letter == SHADDA:
            top = word_stack.pop()
            if top not in vowels:
                word_stack.push(top)
            word_stack.push(last_letter)
            if last_mark != NOT_DEF_HARAKA:
                word_stack.push(last_mark)
        else:
            word_stack.push(last_letter)
            if last_mark != NOT_DEF_HARAKA:
                word_stack.push(last_mark)

        last_letter = stack_letter.pop()
        last_mark = stack_mark.pop()

    if not (stack_letter.is_empty() and stack_mark.is_empty()):
        return False
    else:
        return ''.join(word_stack.items)


def vocalizedlike(word1, word2):
    """
    if the two words has the same letters and the same harakats,  this fuction return True.
    The two words can be full vocalized,  or partial vocalized

    @param word1: first word
    @type word1: unicode
    @param word2: second word
    @type word2: unicode
    @return: if two words have similar vocalization
    @rtype: Boolean
    """
    if vocalized_similarity(word1, word2) < 0:
        return False
    else:
        return True


# -------------------------
# Function def vaznlike(word1, wazn):
# -------------------------
def waznlike(word1, wazn):
    """If the  word1 is like a wazn (pattern),
    the letters must be equal,
    the wazn has FEH,  AIN,  LAM letters.
    this are as generic letters.
    The two words can be full vocalized,  or partial vocalized

    @param word1: input word
    @type word1: unicode
    @param wazn: given word template  وزن
    @type wazn: unicode
    @return: if two words have similar vocalization
    @rtype: Boolean
    """
    stack1 = stack.Stack(word1)
    stack2 = stack.Stack(wazn)
    root = stack.Stack()
    last1 = stack1.pop()
    last2 = stack2.pop()
    vowels = HARAKAT
    while last1 != None and last2 != None:
        if last1 == last2 and last2 not in (FEH, AIN, LAM):
            last1 = stack1.pop()
            last2 = stack2.pop()
        elif last1 not in vowels and last2 in (FEH, AIN, LAM):
            root.push(last1)
            # ~ print "t"
            last1 = stack1.pop()
            last2 = stack2.pop()
        elif last1 in vowels and last2 not in vowels:
            last1 = stack1.pop()
        elif last1 not in vowels and last2 in vowels:
            last2 = stack2.pop()
        else:
            break
    # reverse the root letters
    root.items.reverse()
    # ~ print " the root is ",  root.items#"".join(root.items)
    if not (stack1.is_empty() and stack2.is_empty()):
        return False
    else:
        return True


def shaddalike(partial, fully):
    """
    If the two words has the same letters and the same harakats,  this fuction return True.
    The first word is partially vocalized, the second is fully
    if the partially contians a shadda, it must be at the same place in the fully


    @param partial: the partially vocalized word
    @type partial: unicode
    @param fully: the fully vocalized word
    @type fully: unicode
    @return: if contains shadda
    @rtype: Boolean
    """
    # المدخل ليس به شدة، لا داعي للبحث
    if not has_shadda(partial):
        return True
    # المدخل به شدة، والنتيجة ليس بها شدة، خاطئ
    elif not has_shadda(fully) and has_shadda(partial):
        return False
        # المدخل والمخرج بهما شدة، نتأكد من موقعهما
    partial = strip_harakat(partial)
    fully = strip_harakat(fully)
    pstack = stack.Stack(partial)
    vstack = stack.Stack(fully)
    plast = pstack.pop()
    vlast = vstack.pop()
    # if debug: print "+0",  Pstack,  Vstack
    while plast != None and vlast != None:
        if plast == vlast:
            plast = pstack.pop()
            vlast = vstack.pop()
        elif plast == SHADDA and vlast != SHADDA:
            # if debug: print "+2",  Pstack.items, Plast,  Vstack.items, Vlast
            break
        elif plast != SHADDA and vlast == SHADDA:
            # if debug: print "+2",  Pstack.items, Plast,  Vstack.items, Vlast
            vlast = vstack.pop()
        else:
            # if debug: print "+2",  Pstack.items, Plast,  Vstack.items, Vlast
            break
    if not (pstack.is_empty() and vstack.is_empty()):
        return False
    else:
        return True


def reduce_tashkeel(text):
    """Reduce the Tashkeel,  by deleting evident cases.

    @param text: the input text fully vocalized.
    @type text: unicode.
    @return : partially vocalized text.
    @rtype: unicode.

    """
    patterns = [
        # delete all fathat,   except on waw and yeh
        u"(?<!(%s|%s))(%s|%s)" % (WAW, YEH, SUKUN, FATHA),
        # delete damma if followed by waw.
        u"%s(?=%s)" % (DAMMA, WAW),
        # delete kasra if followed by yeh.
        u"%s(?=%s)" % (KASRA, YEH),
        # delete fatha if followed by alef to reduce yeh maftouha
        #  and waw maftouha before alef.
        u"%s(?=%s)" % (FATHA, ALEF),
        # delete fatha from yeh and waw if they are in the word begining.
        u"(?<=\s(%s|%s))%s" % (WAW, YEH, FATHA),
        # delete kasra if preceded by Hamza below alef.
        u"(?<=%s)%s" % (ALEF_HAMZA_BELOW, KASRA),
    ]
    reduced = text
    for pat in patterns:
        reduced = re.sub(pat, '', reduced)
    return reduced


def vocalized_similarity(word1, word2):
    """
    if the two words has the same letters and the same harakats,  this function return True.
    The two words can be full vocalized, or partial vocalized

    @param word1: first word
    @type word1: unicode
    @param word2: second word
    @type word2: unicode
    @return: return if words are similar, else return negative number of errors
    @rtype: Boolean / int
    """

    stack1 = stack.Stack(word1)
    stack2 = stack.Stack(word2)
    last1 = stack1.pop()
    last2 = stack2.pop()
    err_count = 0
    vowels = HARAKAT
    while last1 != None and last2 != None:
        if last1 == last2:
            last1 = stack1.pop()
            last2 = stack2.pop()
        elif last1 in vowels and last2 not in vowels:
            last1 = stack1.pop()
        elif last1 not in vowels and last2 in vowels:
            last2 = stack2.pop()
        else:
            # break
            if last1 == SHADDA:
                last1 = stack1.pop()
            elif last2 == SHADDA:
                last2 = stack2.pop()
            else:
                last1 = stack1.pop()
                last2 = stack2.pop()
                err_count += 1
    if err_count > 0:
        return -err_count
    else:
        return True


def tokenize(text=u""):
    """
    Tokenize text into words.

    @param text: the input text.
    @type text: unicode.
    @return: list of words.
    @rtype: list.
    """
    if text == u'':
        return []
    else:
        # split tokens
        mylist = TOKEN_PATTERN.split(text)
        # don't remove newline \n
        mylist = [TOKEN_REPLACE.sub('', x) for x in mylist if x]
        # remove empty substring
        mylist = [x for x in mylist if x]
        return mylist


if __name__ == "__main__":
    # ~WORDS = [u'الْدَرَاجَةُ', u'الدّرّاجة',
    # ~u'سّلّامْ', ]
    # ~for wrd in WORDS:
    # ~l, m, s = separate(wrd, True)
    # ~l = joint(l, s)
    # ~print u'\t'.join([wrd,  l, m, s]).encode('utf8')
    # ~newword =  joint(l, m)
    # ~assert (newword != wrd)

    print("like: ", vocalizedlike(u'مُتَوَهِّمًا', u'متوهمًا'))
    print("sim: ", vocalized_similarity(u'ثمّ', u'ثُمَّ'))
    print("like: ", vocalizedlike(u'ثمّ', u'ثُمَّ'))
    print("sim: ", vocalized_similarity(u'ثم', u'ثُمَّ'))
    print("like: ", vocalizedlike(u'ثم', u'ثُمَّ'))
    print("sim: ", vocalized_similarity(u'مُتَوَهِّمًا', u'متوهمًا'))
    print("sim: ", vocalized_similarity(u'مُتَوَهِّمًا', u'متوهمًا'))
