""" Tokenization utilities
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import pickle
from abc import abstractmethod

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.tokenize.punkt import PunktLanguageVars

# from cltk.corpus.latin.readers import latinlibrary # Fix when readers is adopted
from cltk.corpus.latin import latinlibrary
from cltk.tokenize.latin.params import ABBREVIATIONS

class BaseSentenceTokenizerTrainer(object):
    """ Train sentence tokenizer
    """

    def __init__(self, language=None):
        """ Initialize stoplist builder with option for language specific parameters
        :type language: str
        :param language : text from which to build the stoplist
        """
        if language:
            self.language = language.lower()


    def _tokenizer_setup(self):
        self.punctuation = []
        self.strict = []


    def pickle_sentence_tokenizer(self, filename, tokenizer):
        # Dump pickled tokenizer
        with open(filename, 'wb') as f:
            pickle.dump(tokenizer, f)


    def train_sentence_tokenizer(self, text, punctuation=[], strict=[]):
        """
        Train sentence tokenizer.
        """

        self._tokenizer_setup()

        if punctuation:
            self.punctuation = punctuation

        if strict:
            self.strict = strict

        # Set punctuation
        language_punkt_vars = PunktLanguageVars
        language_punkt_vars.sent_end_chars = self.punctuation+self.strict

        # Set abbreviations
        trainer = PunktTrainer(text, language_punkt_vars)
        trainer.INCLUDE_ALL_COLLOCS = True
        trainer.INCLUDE_ABBREV_COLLOCS = True

        tokenizer = PunktSentenceTokenizer(trainer.get_params())

        for abbreviation in ABBREVIATIONS:
            tokenizer._params.abbrev_types.add(abbreviation)

        return tokenizer
