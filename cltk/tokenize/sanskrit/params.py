""" Params: Sanksrit
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import string
from nltk.tokenize.punkt import PunktLanguageVars

class SanskritLanguageVars(PunktLanguageVars):
    sent_end_chars = ['\u0964', '\u0965', '\|', '\|\|']
