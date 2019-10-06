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

def SentenceTokenizer(tokenizer:str = 'punkt'):
    if tokenizer=='punkt':
        return LatinPunktSentenceTokenizer()


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
        self.models_path = LatinPunktSentenceTokenizer.models_path
        super().__init__(language='latin', lang_vars=self.lang_vars)

        try:
            self.model =  open_pickle(os.path.join(self.models_path, 'latin_punkt.pickle'))
        except FileNotFoundError as err:
            raise type(err)(LatinPunktSentenceTokenizer.missing_models_message)

        if self.strict:
            PunktLanguageVars.sent_end_chars=STRICT_PUNCTUATION
        else:
            PunktLanguageVars.sent_end_chars=PUNCTUATION


if __name__ == "__main__":
    t = LatinPunktSentenceTokenizer(strict=True)
    test = """in principio creavit Deus caelum et terram; terra autem erat inanis et vacua et tenebrae super faciem abyssi et spiritus Dei ferebatur super aquas; dixitque Deus fiat lux et facta est lux; et vidit Deus lucem quod esset bona et divisit lucem ac tenebras."""
    sents = t.tokenize(test)
    print(sents)
