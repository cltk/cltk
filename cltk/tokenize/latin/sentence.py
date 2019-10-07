""" Code for sentence tokenization: Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
import nltk
from nltk.tokenize.punkt import PunktLanguageVars
from cltk.tokenize.sentence import BaseSentenceTokenizer, BasePunktSentenceTokenizer
from cltk.tokenize.latin.params import LatinLanguageVars, PUNCTUATION, STRICT_PUNCTUATION
from cltk.utils.file_operations import open_pickle

def SentenceTokenizer(tokenizer:str = 'punkt', strict:bool = False):
    if tokenizer=='punkt':
        return LatinPunktSentenceTokenizer(strict=strict)


class LatinPunktSentenceTokenizer(BasePunktSentenceTokenizer):
    """ PunktSentenceTokenizer trained on Latin
    """
    models_path = os.path.normpath(get_cltk_data_dir() + '/latin/model/latin_models_cltk/tokenizers/sentence')
    missing_models_message = "LatinPunktSentenceTokenizer requires the ```latin_models_cltk``` to be in cltk_data. Please load this corpus."

    def __init__(self: object, language:str = 'latin', strict:bool = False):
        """
        :param language : language for sentence tokenization
        :type language: str
        :param strict : allow for stricter puctuation for sentence tokenization
        :type strict: bool
        """
        self.lang_vars = LatinLanguageVars()
        self.strict = strict
        super().__init__(language='latin', lang_vars=self.lang_vars)
        self.models_path = LatinPunktSentenceTokenizer.models_path

        try:
            self.model =  open_pickle(os.path.join(self.models_path, 'latin_punkt.pickle'))
        except FileNotFoundError as err:
            raise type(err)(LatinPunktSentenceTokenizer.missing_models_message)

        if self.strict:
            PunktLanguageVars.sent_end_chars=STRICT_PUNCTUATION
        else:
            PunktLanguageVars.sent_end_chars=PUNCTUATION
