""" Tokenization utilities
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import pickle
from abc import abstractmethod

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.tokenize.punkt import PunktLanguageVars

class BaseSentenceTokenizerTrainer(object):
    """ Train sentence tokenizer
    """

    def __init__(self, language=None, punctuation=None, strict=None, abbreviations=None):
        """ Initialize stoplist builder with option for language specific parameters
        :type language: str
        :param language : text from which to build the stoplist
        """
        if language:
            self.language = language.lower()

        self.punctuation = punctuation
        self.strict = strict
        self.abbreviations = abbreviations

    def train_sentence_tokenizer(self, text):
        """
        Train sentence tokenizer.
        """
        print(self.punctuation)
        return None

        # # Set punctuation
        # language_punkt_vars = PunktLanguageVars
        #
        # if self.punctuation or self.strict:
        #     language_punkt_vars.sent_end_chars = self.punctuation+self.strict
        #
        # # Set abbreviations
        # trainer = PunktTrainer(text, language_punkt_vars)
        # trainer.INCLUDE_ALL_COLLOCS = True
        # trainer.INCLUDE_ABBREV_COLLOCS = True
        #
        # tokenizer = PunktSentenceTokenizer(trainer.get_params())
        #
        # for abbreviation in self.abbreviations:
        #     tokenizer._params.abbrev_types.add(abbreviation)
        #
        # return tokenizer

    def pickle_sentence_tokenizer(self, filename, tokenizer):
        # Dump pickled tokenizer
        with open(filename, 'wb') as f:
            pickle.dump(tokenizer, f)
