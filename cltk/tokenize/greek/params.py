""" Params: Greek
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

from nltk.tokenize.punkt import PunktLanguageVars

class GreekLanguageVars(PunktLanguageVars):
    sent_end_chars = ['.', ';', '·']
