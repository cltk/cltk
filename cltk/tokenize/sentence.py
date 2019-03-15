"""Tokenize sentences."""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Kyle P. Johnson <kyle@kyle-p-johnson.com>', 'Anoop Kunchukuttan']
__license__ = 'MIT License. See LICENSE.'

import os
import re
import string
from typing import List, Dict, Tuple, Set, Any, Generator

from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer

from cltk.tokenize.latin.params import LatinLanguageVars
from cltk.tokenize.greek.params import GreekLanguageVars

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
        return f'~/cltk_data/{language}/model/{language}_models_cltk/tokenizers/sentence'


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
        elif self.language == 'greek':
            pass
        elif self.language not in INDIAN_LANGUAGES:
            self.internal_punctuation, self.external_punctuation, self.tokenizer_path = \
                self._setup_language_variables(self.language)

    def _setup_language_variables(self, lang: str):  # pragma: no cover
        """Check for language availability and presence of tokenizer file,
        then read punctuation characters for language and build tokenizer file
        path.
        :param lang: The language argument given to the class.
        :type lang: str
        :rtype (str, str, str)
        """
        assert lang in PUNCTUATION.keys(), \
            'Sentence tokenizer not available for {0} language.'.format(lang)
        internal_punctuation = PUNCTUATION[lang]['internal']
        external_punctuation = PUNCTUATION[lang]['external']
        file = PUNCTUATION[lang]['file']
        tokenizer_path = os.path.join(os.path.expanduser(self._get_models_path(language=lang)),
                                      file)
        assert os.path.isfile(tokenizer_path), \
            'CLTK linguistics data not found for language {0} {}'.format(lang)
        return internal_punctuation, external_punctuation, tokenizer_path

    def _setup_tokenizer(self, tokenizer: object):  # pragma: no cover
        """Add tokenizer and punctuation variables.
        :type tokenizer: object
        :param tokenizer : Unpickled tokenizer object.
        :rtype : object
        """
        language_punkt_vars = PunktLanguageVars
        language_punkt_vars.sent_end_chars = self.external_punctuation
        language_punkt_vars.internal_punctuation = self.internal_punctuation
        tokenizer.INCLUDE_ALL_COLLOCS = True
        tokenizer.INCLUDE_ABBREV_COLLOCS = True
        params = tokenizer.get_params()
        return PunktSentenceTokenizer(params)

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
            self.models_path = self._get_models_path(self.language)
            try:
                self.model = open_pickle(
                    os.path.expanduser(os.path.join(self.models_path, 'latin_punkt.pickle')))
            except FileNotFoundError as err:
                raise type(err)(TokenizeSentence.missing_models_message + self.models_path)
            tokenizer = self.model
            tokenizer._lang_vars = self.lang_vars
        elif self.language == 'greek': # Workaround for regex tokenizer
            self.sent_end_chars=GreekLanguageVars.sent_end_chars
            self.sent_end_chars_regex = '|'.join(self.sent_end_chars)
            self.pattern = rf'(?<=[{self.sent_end_chars_regex}])\s'
        else:
            tokenizer = open_pickle(self.tokenizer_path)
            tokenizer = self._setup_tokenizer(tokenizer)

        # mk list of tokenized sentences
        if self.language == 'latin':
            return tokenizer.tokenize(untokenized_string)
        elif self.language == 'greek':
            return re.split(self.pattern, untokenized_string)
        else:
            tokenized_sentences = [sentence for sentence in
                                   tokenizer.sentences_from_text(untokenized_string,
                                                                 realign_boundaries=True)]
            return tokenized_sentences

    def indian_punctuation_tokenize_regex(self, untokenized_string: str):
        """A trivial tokenizer which just tokenizes on the punctuation boundaries.
        This also includes punctuation, namely the the purna virama ("|") and
        deergha virama ("॥"), for Indian language scripts.

        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :rtype : list of strings
        """
        modified_punctuations = string.punctuation.replace("|",
                                                           "")  # The replace , deletes the ' | ' from the punctuation string provided by the library
        indian_punctuation_pattern = re.compile(
            '([' + modified_punctuations + '\u0964\u0965' + ']|\|+)')
        tok_str = indian_punctuation_pattern.sub(r' \1 ', untokenized_string.replace('\t', ' '))
        return re.sub(r'[ ]+', u' ', tok_str).strip(' ').split(' ')

    def tokenize(self, untokenized_string: str, model=None):
        """Alias for tokenize_sentences()—NLTK's PlaintextCorpusReader needs a
        function called tokenize in functions used as a parameter for sentence
        tokenization.

        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        """
        if self.language in INDIAN_LANGUAGES:
            return self.indian_punctuation_tokenize_regex(untokenized_string)
        else:
            return self.tokenize_sentences(untokenized_string)
