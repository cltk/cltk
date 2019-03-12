""" Tokenization utilities
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import pickle
from abc import abstractmethod
from typing import List, Dict, Tuple, Set, Any, Generator
import inspect

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.tokenize.punkt import PunktLanguageVars

class BaseSentenceTokenizerTrainer():
    """ Train sentence tokenizer
    """

    def __init__(self: object, language: str = None,
                    punctuation: List[str] = None,
                    strict: bool = False,
                    strict_punctuation: List[str] = None,
                    abbreviations: List[str] = None):
        """ Initialize stoplist builder with option for language specific parameters
        :type language: str
        :param language: text from which to build the stoplist
        :type punctuation: list
        :param punctuation: list of punctuation used to train sentence tokenizer
        :type strict: bool
        :param strict: option for including additional punctuation for tokenizer
        :type strict: list
        :param strict: list of additional punctuation used to train sentence tokenizer if strict is used
        :type abbreviations: list
        :param abbreviations: list of abbreviations used to train sentence tokenizer
        """
        if language:
            self.language = language.lower()

        self.strict = strict
        self.punctuation = punctuation
        self.strict_punctuation = strict_punctuation
        self.abbreviations = abbreviations

    def train_sentence_tokenizer(self: object, text: str):
        """
        Train sentence tokenizer.
        """
        language_punkt_vars = PunktLanguageVars

        # Set punctuation
        if self.punctuation:
            if self.strict:
                language_punkt_vars.sent_end_chars = self.punctuation.extend(self.strict_punctuation)
            else:
                language_punkt_vars.sent_end_chars = self.punctuation

        # Set abbreviations
        trainer = PunktTrainer(text, language_punkt_vars)
        trainer.INCLUDE_ALL_COLLOCS = True
        trainer.INCLUDE_ABBREV_COLLOCS = True

        tokenizer = PunktSentenceTokenizer(trainer.get_params())

        if self.abbreviations:
            for abbreviation in self.abbreviations:
                tokenizer._params.abbrev_types.add(abbreviation)

        return tokenizer

    def pickle_sentence_tokenizer(self: object, filename: str, tokenizer: object):
        # Dump pickled tokenizer
        with open(filename, 'wb') as f:
            pickle.dump(tokenizer, f)

if __name__ == '__main__':
    latin_text = "O di inmortales! ubinam gentium sumus? in qua urbe vivimus? quam rem publicam habemus? Hic, hic sunt in nostro numero, patres conscripti, in hoc orbis terrae sanctissimo gravissimoque consilio, qui de nostro omnium interitu, qui de huius urbis atque adeo de orbis terrarum exitio cogitent! Hos ego video consul et de re publica sententiam rogo et, quos ferro trucidari oportebat, eos nondum voce volnero! Fuisti igitur apud Laecam illa nocte, Catilina, distribuisti partes Italiae, statuisti, quo quemque proficisci placeret, delegisti, quos Romae relinqueres, quos tecum educeres, discripsisti urbis partes ad incendia, confirmasti te ipsum iam esse exiturum, dixisti paulum tibi esse etiam nunc morae, quod ego viverem."  # pylint: disable=line-too-long
    trainer = BaseSentenceTokenizerTrainer('latin')
    print(type(trainer.train_sentence_tokenizer(latin_text)))
    print(isinstance(trainer.train_sentence_tokenizer(latin_text), object))
