"""Language-specific word tokenizers. Primary purpose is
to handle enclitics.
"""

__author__ = [
    "Patrick J. Burns <patrick@diyclassics.org>",
    "Kyle P. Johnson <kyle@kyle-p-johnson.com>",
    "Natasha Voake <natashavoake@gmail.com>",
    "Clément Besnier <clem@clementbesnier.fr>",
    "Andrew Deloucas <adeloucas@g.harvard.edu>",
    "Todd Cook <todd.g.cook@gmail.com>",
]

__license__ = "MIT License. See LICENSE."

import logging
import re
from abc import abstractmethod
from typing import List

from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize.punkt import PunktParameters, PunktSentenceTokenizer


class WordTokenizer:
    """Base class for word tokenizers"""

    @abstractmethod
    def tokenize(self, text: str, model: object = None):
        """
        Create a list of tokens from a string.
        This method should be overridden by subclasses of WordTokenizer.
        """
        pass

    @abstractmethod
    def tokenize_sign(self, text: str, model: object = None):
        """
        Create a list of tokens from a string, for cuneiform signs..
        This method should be overridden by subclasses of WordTokenizer.
        """
        pass

    @staticmethod
    def compute_indices(text: str, tokens):
        indices = []
        for i, token in enumerate(tokens):
            if 1 <= i:
                current_index = indices[-1] + len(tokens[i - 1])
                indices.append(current_index + text[current_index:].find(token))
            else:
                indices.append(text.find(token))
        return indices


class PunktWordTokenizer(WordTokenizer):
    """Class for punkt word tokenization"""

    def __init__(self, sent_tokenizer: object = None):
        """
        :param language : language for sentences tokenization
        :type language: str
        """
        if sent_tokenizer:
            self.sent_tokenizer = sent_tokenizer()
        else:
            punkt_param = PunktParameters()
            self.sent_tokenizer = PunktSentenceTokenizer(punkt_param)

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        """
        sents = self.sent_tokenizer.tokenize(text)
        tokenizer = TreebankWordTokenizer()
        return [item for sublist in tokenizer.tokenize_sents(sents) for item in sublist]


class RegexWordTokenizer(WordTokenizer):
    """Class for regex-based word tokenization"""

    def __init__(self, patterns: List[str] = None):
        """
        :param language : language for sentences tokenization
        :type language: str
        :param patterns: regex patterns for word tokenization
        :type patterns: list of strings
        """
        self.patterns = patterns

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        for pattern in self.patterns:
            text = re.sub(pattern[0], pattern[1], text)
        return text.split()


class CLTKTreebankWordTokenizer(TreebankWordTokenizer):
    @staticmethod
    def compute_indices(text: str, tokens):
        indices = []
        for i, token in enumerate(tokens):
            if 1 <= i:
                current_index = indices[-1] + len(tokens[i - 1])
                indices.append(current_index + text[current_index:].find(token))
            else:
                indices.append(text.find(token))
        return indices
