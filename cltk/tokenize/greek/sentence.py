""" Code for sentence tokenization: Greek
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
import re

from cltk.tokenize.sentence import BaseSentenceTokenizer, RegexSentenceTokenizer, PunktSentenceTokenizer
from cltk.utils.file_operations import open_pickle

from nltk.tokenize.punkt import PunktLanguageVars

def SentenceTokenizer(tokenizer: str = 'regex'):
    if tokenizer=='punkt':
        return GreekPunktSentenceTokenizer()
    if tokenizer=='regex':
        return GreekRegexSentenceTokenizer()


class GreekLanguageVars(PunktLanguageVars):
    sent_end_chars = ('.', ';', '·')


class GreekPunktSentenceTokenizer(PunktSentenceTokenizer):
    """ PunktSentenceTokenizer trained on Ancient Greek
    """
    models_path = os.path.expanduser('~/cltk_data/greek/model/greek_models_cltk/tokenizers/sentence')
    missing_models_message = "BackoffLatinLemmatizer requires the ```greek_models_cltk``` to be in cltk_data. Please load this corpus."

    def __init__(self: object, language: str = 'greek'):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        PunktSentenceTokenizer.__init__(self, language='greek')
        self.models_path = GreekPunktSentenceTokenizer.models_path

        try:
            self.model =  open_pickle(os.path.join(self.models_path, 'greek_punkt.pickle'))
        except FileNotFoundError as err:
            raise type(err)(GreekPunktSentenceTokenizer.missing_models_message)

        self.lang_vars = GreekLanguageVars()


class GreekRegexSentenceTokenizer(RegexSentenceTokenizer):
    def __init__(self: object):
        RegexSentenceTokenizer.__init__(self, language='greek', sent_end_chars=GreekLanguageVars.sent_end_chars)
