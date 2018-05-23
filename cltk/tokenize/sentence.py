"""Tokenize sentences."""

import os
import re
import string
from typing import Any
from typing import Dict  # pylint: disable=unused-import
from typing import List
from typing import Tuple

from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer

from cltk.utils.file_operations import open_pickle

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>', 'Anoop Kunchukuttan']  # type: List[str]
__license__ = 'MIT License. See LICENSE.'  # type: str

PUNCTUATION = {'greek':
                   {'external': ['.', ';'],
                    'internal': [',', '·'],
                    'file': 'greek.pickle', },
               'latin':
                   {'external': ['.', '?', '!', ':'],
                    'internal': [',', ';'],
                    'file': 'latin.pickle', }}  # type: Dict[str, Dict[str, Any]]

INDIAN_LANGUAGES = ['bengali', 'hindi', 'marathi', 'sanskrit', 'telugu']


class TokenizeSentence():  # pylint: disable=R0903
    """Tokenize sentences for the language given as argument, e.g.,
    ``TokenizeSentence('greek')``.
    """

    def __init__(self, language: str) -> None:
        """Lower incoming language name and assemble variables.
        :type language: str
        :param language : Language for sentence tokenization.
        """
        self.language = language.lower()  # type:str

        if self.language not in INDIAN_LANGUAGES:
            self.internal_punctuation, self.external_punctuation, self.tokenizer_path = \
                self._setup_language_variables(self.language)

    @staticmethod
    def _setup_language_variables(lang: str) -> Tuple[Tuple[str, ...], Tuple[str, ...], str]:
        """Check for language availability and presence of tokenizer file,
        then read punctuation characters for language and build tokenizer file
        path.
        :param lang: The language argument given to the class.
        :type lang: str
        :rtype (str, str, str)
        """
        assert lang in PUNCTUATION.keys(), \
            'Sentence tokenizer not available for {0} language.'.format(lang)
        internal_punctuation = PUNCTUATION[lang]['internal']  # type: Tuple[str, ...]
        external_punctuation = PUNCTUATION[lang]['external']  # type: Tuple[str, ...]
        file = PUNCTUATION[lang]['file']  # type: str
        rel_path = os.path.join('~/cltk_data', lang, 'model/' + lang + '_models_cltk/tokenizers/sentence')  # type: str  # pylint: disable=line-too-long
        # rel_path = os.path.join('~/cltk_data',
        #                         lang,
        #                         'model/' + lang + '_models_cltk/tokenizers/sentence')  # type: str
        path = os.path.expanduser(rel_path)  # type: str
        tokenizer_path = os.path.join(path, file)  # type: str
        assert os.path.isfile(tokenizer_path), \
            'CLTK linguistics data not found for language {0}'.format(lang)
        return internal_punctuation, external_punctuation, tokenizer_path

    def _setup_tokenizer(self, tokenizer: Any) -> Any:
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
        print(type(params))
        return PunktSentenceTokenizer(params)

    def tokenize_sentences(self, untokenized_string: str) -> List[str]:
        """Tokenize sentences by reading trained tokenizer and invoking
        ``PunktSentenceTokenizer()``.
        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :rtype : list of strings
        """
        # load tokenizer
        assert isinstance(untokenized_string, str), \
            'Incoming argument must be a string.'
        tokenizer_pickle = open_pickle(self.tokenizer_path)  # type: Any
        tokenizer = self._setup_tokenizer(tokenizer_pickle)  # type: Any

        # mk list of tokenized sentences
        tokenized_sentences = []  # type: List[str]
        for sentence in tokenizer.sentences_from_text(untokenized_string, realign_boundaries=True):  # pylint: disable=line-too-long
            tokenized_sentences.append(sentence)
        return tokenized_sentences

    @staticmethod
    def indian_punct_tokenize_regex(untokenized_string: str) -> List[str]:
        """A trivial tokenizer which just tokenizes on the punctuation boundaries.
        This also includes punctuation, namely the the purna virama ("|") and
        deergha virama ("॥"), for Indian language scripts.

        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :rtype : list of strings
        """
        # The replace , deletes the ' | ' from the punctuation string provided by the library
        modified_punctuations = string.punctuation.replace("|", "")  # type: str
        indian_punct_pattern = re.compile(r'(['+modified_punctuations+'\u0964\u0965'+']|\|+)')  # type: Any  # pylint: disable=line-too-long
        tok_str = indian_punct_pattern.sub(r' \1 ', untokenized_string.replace('\t', ' '))  # type: str  # pylint: disable=line-too-long
        return re.sub(r'[ ]+', u' ', tok_str).strip(' ').split(' ')

    def tokenize(self, untokenized_string: str) -> List[str]:
        """NLTK's PlaintextCorpusReader needs a function called tokenize
        in functions used as a parameter for sentence tokenization.
        So this is an alias for tokenize_sentences().
        """
        if self.language in INDIAN_LANGUAGES:
            return self.indian_punct_tokenize_regex(untokenized_string)
        return self.tokenize_sentences(untokenized_string)
