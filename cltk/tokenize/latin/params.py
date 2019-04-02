""" Params: Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

from nltk.tokenize.punkt import PunktLanguageVars

PRAENOMINA = ['a', 'agr', 'ap', 'c', 'cn', 'd', 'f', 'k', 'l', "m'", 'm', 'mam', 'n', 'oct', 'opet', 'p', 'post', 'pro', 'q', 's', 'ser', 'sert', 'sex', 'st', 't', 'ti', 'v', 'vol', 'vop', 'a', 'ap', 'c', 'cn', 'd', 'f', 'k', 'l', 'm', "m'", 'mam', 'n', 'oct', 'opet', 'p', 'paul', 'post', 'pro', 'q', 'ser', 'sert', 'sex', 'sp', 'st', 'sta', 't', 'ti', 'v', 'vol', 'vop']

CALENDAR = ['ian', 'febr', 'mart', 'apr', 'mai', 'iun', 'iul', 'aug', 'sept', 'oct', 'nov', 'dec'] \
            + ['kal', 'non', 'id', 'a.d']

MISC = ['coll', 'cos', 'ord', 'pl.', 's.c', 'suff', 'trib']

ABBREVIATIONS = set(
                   PRAENOMINA +
                   CALENDAR +
                   MISC
                   )

class LatinLanguageVars(PunktLanguageVars):
    _re_non_word_chars = PunktLanguageVars._re_non_word_chars.replace("'",'')
