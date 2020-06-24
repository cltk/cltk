"""Language-specific word tokenizers. Primary purpose is
to handle enclitics.
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Natasha Voake <natashavoake@gmail.com>',
              'Clément Besnier <clemsciences@aol.com>',
              'Andrew Deloucas <adeloucas@g.harvard.edu>',
              'Todd Cook <todd.g.cook@gmail.com>']

__license__ = 'MIT License. See LICENSE.'

import logging
import re
from abc import abstractmethod
from typing import List

from nltk.tokenize.punkt import PunktParameters
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize.treebank import TreebankWordTokenizer

from cltk.tokenize.akkadian.word import tokenize_akkadian_words, tokenize_akkadian_signs
from cltk.corpus.arabic.utils.pyarabic import araby
from cltk.tokenize.greek.sentence import GreekRegexSentenceTokenizer
from cltk.tokenize.latin.word import WordTokenizer as LatinWordTokenizer
from cltk.tokenize.middle_english.params import MiddleEnglishTokenizerPatterns
from cltk.tokenize.middle_high_german.params import MiddleHighGermanTokenizerPatterns
from cltk.tokenize.old_norse.params import OldNorseTokenizerPatterns
from cltk.tokenize.old_french.params import OldFrenchTokenizerPatterns

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class WordTokenizer:  # pylint: disable=too-few-public-methods
    """Tokenize according to rules specific to a given language."""

    def __init__(self, language):
        """Take language as argument to the class. Check availability and
        setup class variables."""
        self.language = language
        self.available_languages = ['akkadian',
                                    'arabic',
                                    'french',  # defaults to old_french
                                    'greek',
                                    'latin',
                                    'middle_english',
                                    'middle_french',
                                    'middle_high_german',
                                    'old_french',
                                    'old_norse',
                                    'sanskrit',
                                    'multilingual']

        assert self.language in self.available_languages, \
            "Specific tokenizer not available for '{0}'. Only available for: '{1}'.".format(
                self.language,
                self.available_languages)

        # raise languages-specific warnings
        if self.language == 'french':
            self.language = 'old_french'
            LOG.warning("'french' defaults to 'old_french'. 'middle_french' also available.")  # pylint: disable=line-too-long

        if self.language == 'arabic':
            self.toker = BaseArabyWordTokenizer('arabic')
        elif self.language == 'french':
            self.toker = BaseRegexWordTokenizer('old_french',
                                                OldFrenchTokenizerPatterns)
        elif self.language == 'greek':
            self.toker = BasePunktWordTokenizer('greek',
                                                GreekRegexSentenceTokenizer)
        elif self.language == 'latin':
            self.toker = LatinWordTokenizer()
        elif self.language == 'old_norse':
            self.toker = BaseRegexWordTokenizer('old_norse',
                                                OldNorseTokenizerPatterns)
        elif self.language == 'middle_english':
            self.toker = BaseRegexWordTokenizer('middle_english',
                                                MiddleEnglishTokenizerPatterns)
        elif self.language == 'middle_french':
            self.toker = BaseRegexWordTokenizer('old_french',
                                                OldFrenchTokenizerPatterns)
        elif self.language == 'middle_high_german':
            self.toker = BaseRegexWordTokenizer('middle_high_german',
                                                MiddleHighGermanTokenizerPatterns)
        elif self.language == 'old_french':
            self.toker = BaseRegexWordTokenizer('old_french',
                                                OldFrenchTokenizerPatterns)
        else:
            LOG.warning("Falling back to default tokenizer, the NLTK's `TreebankWordTokenizer()`.")
            self.toker = TreebankWordTokenizer()

    def tokenize(self, text):
        """Tokenize incoming string."""
        if self.language == 'akkadian':
            return tokenize_akkadian_words(text)
        return self.toker.tokenize(text)

    def tokenize_sign(self, word):
        """This is for tokenizing cuneiform signs."""
        if self.language == 'akkadian':
            sign_tokens = tokenize_akkadian_signs(word)
        else:
            sign_tokens = 'Language must be written using cuneiform.'
        return sign_tokens


class BaseWordTokenizer:
    """ Base class for word tokenization"""

    def __init__(self, language: str = None):
        """
        :param language : language for word tokenization
        :type language: str
        """
        if language:
            self.language = language.lower()

    @abstractmethod
    def tokenize(self, text: str, model: object = None):
        """
        Create a list of tokens from a string.
        This method should be overridden by subclasses of BaseWordTokenizer.
        """
        pass


class BasePunktWordTokenizer(BaseWordTokenizer):
    """Base class for punkt word tokenization"""

    def __init__(self, language: str = None, sent_tokenizer: object = None):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.language = language
        super().__init__(language=self.language)
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


class BaseRegexWordTokenizer(BaseWordTokenizer):
    """Base class for regex word tokenization"""

    def __init__(self, language: str = None, patterns: List[str] = None):
        """
        :param language : language for sentence tokenization
        :type language: str
        :param patterns: regex patterns for word tokenization
        :type patterns: list of strings
        """
        self.language = language
        self.patterns = patterns
        super().__init__(language=self.language)

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


class BaseArabyWordTokenizer(BaseWordTokenizer):
    """
    Base class for word tokenizer using the pyarabic package:
    https://pypi.org/project/PyArabic/
    """

    def __init__(self, language: str = None):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.language = language
        super().__init__(language=self.language)

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        """
        return araby.tokenize(text)
