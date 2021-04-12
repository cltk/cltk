""" Tokenization utilities

TODO: KJ consider moving to ``scripts`` dir.
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License."

import inspect
import pickle
from abc import abstractmethod
from typing import Any, Dict, Generator, List, Set, Tuple

from nltk.tokenize.punkt import PunktLanguageVars, PunktSentenceTokenizer, PunktTrainer


class SentenceTokenizerTrainer:
    """Train sentences tokenizer"""

    def __init__(
        self: object,
        language: str = None,
        punctuation: List[str] = None,
        strict: bool = False,
        strict_punctuation: List[str] = None,
        abbreviations: List[str] = None,
    ):
        """Initialize stoplist builder with option for language specific parameters
        :type language: str
        :param language: text from which to build the stoplist
        :type punctuation: list
        :param punctuation: list of punctuation used to train sentences tokenizer
        :type strict: bool
        :param strict: option for including additional punctuation for tokenizer
        :type strict: list
        :param strict: list of additional punctuation used to train sentences tokenizer if strict is used
        :type abbreviations: list
        :param abbreviations: list of abbreviations used to train sentences tokenizer
        """
        if language:
            self.language = language.lower()

        self.strict = strict
        self.punctuation = punctuation
        self.strict_punctuation = strict_punctuation
        self.abbreviations = abbreviations

    def train_sentence_tokenizer(self: object, text: str):
        """
        Train sentences tokenizer.
        """
        language_punkt_vars = PunktLanguageVars

        # Set punctuation
        if self.punctuation:
            if self.strict:
                language_punkt_vars.sent_end_chars = (
                    self.punctuation + self.strict_punctuation
                )
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
        with open(filename, "wb") as f:
            pickle.dump(tokenizer, f)
