""" Tokenization utilities: Latin
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License."

import pickle
from typing import Any, Dict, Generator, List, Set, Tuple

from cltk.tokenize.latin.params import ABBREVIATIONS
from cltk.tokenize.utils import BaseSentenceTokenizerTrainer
from nltk.tokenize.punkt import PunktLanguageVars, PunktSentenceTokenizer, PunktTrainer


class LatinSentenceTokenizerTrainer(BaseSentenceTokenizerTrainer):
    """ """

    def __init__(self: object, strict: bool = False):
        self.strict = strict
        self.punctuation = [".", "?", "!"]
        self.strict_punctuation = [";", ":", "—"]
        self.abbreviations = ABBREVIATIONS

        super().__init__(
            language="latin",
            punctuation=self.punctuation,
            strict=self.strict,
            strict_punctuation=self.strict_punctuation,
            abbreviations=self.abbreviations,
        )
