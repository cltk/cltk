""" Code for sentence tokenization: Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
from cltk.tokenize.sentence import BaseSentenceTokenizer, BasePunktSentenceTokenizer
from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars

def SentenceTokenizer(tokenizer:str = 'punkt'):
    if tokenizer=='punkt':
        return LatinPunktSentenceTokenizer()


class LatinLanguageVars(PunktLanguageVars):
    _re_non_word_chars = PunktLanguageVars._re_non_word_chars.replace("'",'')


class LatinPunktSentenceTokenizer(BasePunktSentenceTokenizer):
    """ PunktSentenceTokenizer trained on Latin
    """
    models_path = os.path.expanduser('~/cltk_data/latin/model/latin_models_cltk/tokenizers/sentence')
    missing_models_message = "BackoffLatinLemmatizer requires the ```latin_models_cltk``` to be in cltk_data. Please load this corpus."

    def __init__(self: object, language:str = 'latin'):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        BasePunktSentenceTokenizer.__init__(self, language='latin')
        self.model = LatinPunktSentenceTokenizer.models_path

        try:
            self.model =  open_pickle(os.path.join(self.models_path, 'latin_punkt.pickle'))
        except FileNotFoundError as err:
            raise type(err)(LatinPunktSentenceTokenizer.missing_models_message)

        self.lang_vars = LatinLanguageVars()
