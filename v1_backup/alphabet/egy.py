"""Convert MdC transliterated text to Unicode."""

import re

__author__ = ["Doğu Kaan Eraslan <kaaneraslan@gmail.com>"]


def mdc_unicode(string, q_kopf=True):
    """
    parameters:
    string: str
    q_kopf: boolean
    return:
    unicode_text: str
    The translitterated text passes to the
    function under the variable 'string'.
    The search and replace operation
    is done for the related caracters. If
    the q_kopf parameter is False, we replace
    'q' with 'ḳ'
    """
    # lettres miniscules/lower case letters/küçük harfler
    alef = string.replace("\u0041", "\ua723")  # A -> ꜣ
    ayin = alef.replace("\u0061", "\ua725")  # a -> ꜥ
    h_dot = ayin.replace("\u0048", "\u1e25")  # H -> ḥ
    h_breve = h_dot.replace("\u0078", "\u1e2b")  # x -> ḫ
    h_line = h_breve.replace("\u0058", "\u1e96")  # X -> ẖ
    h_circum_below = h_line.replace("\u0056", "\u0068" + "\u032d")  # V -> 
    shin = h_circum_below.replace("\u0053", "\u0161")  # S -> š
    s_acute = shin.replace("\u0063", "\u015b")  # c -> ś
    tche = s_acute.replace("\u0054", "\u1e6f")  # T -> ṯ
    t_circum_below = tche.replace("\u0076", "\u1e71")  # v -> ṱ
    djed = t_circum_below.replace("\u0044", "\u1e0f")  # D -> ḏ
    egy_yod = djed.replace("\u0069", "\u0069" + "\u0486")  # i -> i҆
    equal = egy_yod.replace("\u003d", "\u2e17")  # = -> ⸗
    left_brackets = equal.replace("\u003c", "\u2329")  # < -> 〈
    right_brackets = left_brackets.replace("\u003e", "\u232a")  # > -> 〉

    if q_kopf is False:
        kopf = right_brackets.replace("\u0071", "\u1e33")  # q -> ḳ
        kopf_capital = kopf.replace("\u0051", "\u1e32")  # Q -> Ḳ
    else:
        kopf_capital = right_brackets

    # LETTRES MAJUSCULES/ UPPER CASE LETTERS/ BÜYÜK HARFLER
    h2_capital = re.sub("[\u00a1\u0040]", "\u1e24", kopf_capital)  # ¡|@ -> Ḥ
    h3_capital = re.sub("[\u0023\u00a2]", "\u1e2a", h2_capital)  # #|¢ -> Ḫ
    h4_capital = re.sub("[\u0024\u00a3]", "\u0048" + "\u0331", h3_capital)  # $|£ -> H̱
    shin_capital = re.sub("[\u00a5\u005e]", "\u0160", h4_capital)  # ¥|^ -> Š
    tche_capital = re.sub("[\u002a\u00a7]", "\u1e6e", shin_capital)  # *|§ -> Ṯ
    djed_capital = re.sub("[\u00a9\u002b]", "\u1e0e", tche_capital)  # ©|+ -> Ḏ
    unicode_text = djed_capital.replace("\u0043", "\u015a")  # C -> Ś

    return unicode_text
