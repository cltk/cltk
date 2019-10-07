"""Tokenize sentences."""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Kyle P. Johnson <kyle@kyle-p-johnson.com>', 'Anoop Kunchukuttan <anoop.kunchukuttan@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import os
import re
import string
from typing import List, Dict, Tuple, Set, Any, Generator

from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer

from cltk.tokenize.latin.params import LatinLanguageVars
from cltk.tokenize.greek.params import GreekLanguageVars
from cltk.tokenize.sanskrit.params import SanskritLanguageVars

from cltk.utils.file_operations import open_pickle

INDIAN_LANGUAGES = ['bengali', 'hindi', 'marathi', 'sanskrit', 'telugu']

class BaseSentenceTokenizer:
    """ Base class for sentence tokenization"""

    def __init__(self, language: str = None):
        """ Initialize stoplist builder with option for language specific parameters
        :param language : language for sentence tokenization
        :type language: str
        """
        if language:
            self.language = language.lower()

    def tokenize(self, text: str, model: object = None):
        """
        Method for tokenizing sentences with pretrained punkt models; can
        be overridden by language-specific tokenizers.

        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        if not self.model:
            model = self.model

        tokenizer = self.model
        if self.lang_vars:
            tokenizer._lang_vars = self.lang_vars
        return tokenizer.tokenize(text)

    def _get_models_path(self, language):  # pragma: no cover
        return get_cltk_data_dir() + f'/{language}/model/{language}_models_cltk/tokenizers/sentence'


class BasePunktSentenceTokenizer(BaseSentenceTokenizer):
    """Base class for punkt sentence tokenization"""

    missing_models_message = "BasePunktSentenceTokenizer requires a language model."

    def __init__(self, language: str = None, lang_vars: object = None):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.language = language
        self.lang_vars = lang_vars
        super().__init__(language=self.language)
        if self.language:
            self.models_path = self._get_models_path(self.language)
            try:
                self.model = open_pickle(os.path.join(os.path.expanduser(self.models_path),
                                                      f'{self.language}_punkt.pickle'))
            except FileNotFoundError as err:
                raise type(err)(BasePunktSentenceTokenizer.missing_models_message)


class BaseRegexSentenceTokenizer(BaseSentenceTokenizer):
    """ Base class for regex sentence tokenization"""

    def __init__(self, language: str = None, sent_end_chars: List[str] = None):
        """
        :param language: language for sentence tokenization
        :type language: str
        :param sent_end_chars: list of sentence-ending punctuation marks
        :type sent_end_chars: list
        """
        BaseSentenceTokenizer.__init__(self, language)
        if sent_end_chars:
            self.sent_end_chars = sent_end_chars
            self.sent_end_chars_regex = '|'.join(self.sent_end_chars)
            self.pattern = rf'(?<=[{self.sent_end_chars_regex}])\s'
        else:
            raise Exception  # TODO add message, must specify sent_end_chars, or warn and use defaults

    def tokenize(self, text: str, model: object = None):
        """
        Method for tokenizing sentences with regular expressions.

        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        """
        sentences = re.split(self.pattern, text)
        return sentences


class TokenizeSentence(BasePunktSentenceTokenizer):  # pylint: disable=R0903
    """Tokenize sentences for the language given as argument, e.g.,
    ``TokenizeSentence('greek')``.
    """

    missing_models_message = "TokenizeSentence requires the models to be installed in cltk_data. Please load the correct models."

    def __init__(self, language: str):
        """Lower incoming language name and assemble variables.
        :type language: str
        :param language : Language for sentence tokenization.
        """
        self.language = language.lower()
        # Workaround for Latin—use old API syntax to load new sent tokenizer
        if self.language == 'latin':
            self.lang_vars = LatinLanguageVars()
            super().__init__(language='latin', lang_vars=self.lang_vars)

    def tokenize_sentences(self, untokenized_string: str):
        """Tokenize sentences by reading trained tokenizer and invoking
        ``PunktSentenceTokenizer()``.
        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :rtype : list of strings
        """
        # load tokenizer
        assert isinstance(untokenized_string, str), \
            'Incoming argument must be a string.'

        if self.language == 'latin':
            tokenizer = super()
        elif self.language == 'greek': # Workaround for regex tokenizer
            self.sent_end_chars=GreekLanguageVars.sent_end_chars
            self.sent_end_chars_regex = '|'.join(self.sent_end_chars)
            self.pattern = rf'(?<=[{self.sent_end_chars_regex}])\s'
        elif self.language in INDIAN_LANGUAGES:
            self.sent_end_chars=SanskritLanguageVars.sent_end_chars
            self.sent_end_chars_regex = '|'.join(self.sent_end_chars)
            self.pattern = rf'(?<=[{self.sent_end_chars_regex}])\s'
        else:
            # Warn that NLTK Punkt is being used by default???
            tokenizer = PunktSentenceTokenizer()

        # mk list of tokenized sentences
        if self.language == 'greek' or self.language in INDIAN_LANGUAGES:
            return re.split(self.pattern, untokenized_string)
        else:
            return tokenizer.tokenize(untokenized_string)

    def tokenize(self, untokenized_string: str, model=None):
        """Alias for tokenize_sentences()—NLTK's PlaintextCorpusReader needs a
        function called tokenize in functions used as a parameter for sentence
        tokenization.

        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        """
        return self.tokenize_sentences(untokenized_string)
