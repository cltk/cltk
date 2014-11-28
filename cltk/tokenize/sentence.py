"""Tokenizes sentences."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import pickle
from pickle import PickleError
from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer
import os
import sys


class TokenizeSentence(object):  # pylint: disable=R0903
    """Tokenize sentences."""

    def __init__(self: object, language: str):
        """Initializer. Should it do anything?
        :type self: object
        :param language : Language for sentence tokenization.
        """
        self.language = language.lower()
        self.lang_punct, self.pickle_path = self._setup_variables(self.language)

    def _setup_variables(self, lang):
        """"Read punctuation details for a language and assemble pickle
        path.
        TODO: move `punctuation` to somewhere accessible to the rest of the
        class or module.
        """
        rel_path = os.path.join('~/cltk_data', self.language,
                                'trained_model/cltk_linguistic_data/tokenizers/sentence')  # pylint: disable=C0301
        punctuation = {'greek':
                           {'external': ('.', ';'),
                            'internal': (',', '·'),
                            'file': 'greek.pickle',},
                       'latin':
                           {'external': ('.', '?', ':'),
                            'internal': (',', ';'),
                            'file': 'latin.pickle',}}
        assert lang in punctuation.keys(), 'Sentence tokenizer not available for chosen language.'  # pylint: disable=C0301
        lang_punct = punctuation[lang]
        path = os.path.expanduser(rel_path)
        pickle_path = os.path.join(path, lang_punct['file'])
        return lang_punct, pickle_path



    def _setup_tokenizer(self, tokenizer: object):
        """Add tokenizer and punctuation variables.
        :type tokenizer: object
        :param tokenizer : Unpickled tokenizer object.
        :rtype : object
        """
        language_punkt_vars = PunktLanguageVars
        language_punkt_vars.sent_end_chars = self.lang_punct['external']
        language_punkt_vars.internal_punctuation = self.lang_punct['internal']
        tokenizer.INCLUDE_ALL_COLLOCS = True
        tokenizer.INCLUDE_ABBREV_COLLOCS = True
        params = tokenizer.get_params()
        return PunktSentenceTokenizer(params)

    def tokenize_sentences(self: object, untokenized_string: str):
        """Reads language tokenizer and invokes ``PunktSentenceTokenizer()``.
        :type self: object
        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :rtype : str
        """
        assert isinstance(untokenized_string, str), 'Incoming argument must be a string.'  # pylint: disable=C0301

        tokenizer = open_pickle(self.pickle_path)
        pst = self._setup_tokenizer(tokenizer)

        # mk list of tokenized sentences
        tokenized_sentences = []
        return [tokenized_sentences.append(sentence)
                for sentence
                in pst.sentences_from_text(untokenized_string,
                                           realign_boundaries=True)]


def open_pickle(path: str):
    """Open a pickle and returns pickle object.
    :type path: str
    :param : path: File path to pickle file to be opened.
    :rtype : object
    """
    try:
        with open(path, 'rb') as opened_pickle:
            try:
                return pickle.load(opened_pickle)
            except PickleError as pickle_error:
                print(pickle_error)
                sys.exit(1)
    except IOError as io_err:
        print(io_err)
        sys.exit(1)
