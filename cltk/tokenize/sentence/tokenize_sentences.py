"""Tokenizes sentences."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import pickle
from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer
import os


class TokenizeSentence(object):
    """Tokenize sentences."""

    def __init__(self):
        """Initializer. Should it do anything?"""
        pass

    def sentence_tokenizer(self, untokenized_string, language):
        """Reads language .pickle for right language"""
        if language == 'greek':
            pickle_path = os.path.expanduser('~/cltk_data/greek/tokenizers/sentence/greek.pickle')
            language_punkt_vars = PunktLanguageVars
            language_punkt_vars.sent_end_chars = ('.', ';')
            language_punkt_vars.internal_punctuation = (',', '·')
        elif language == 'latin':
            pickle_path = os.path.expanduser('~/cltk_data/latin/tokenizers/sentence/latin.pickle')
            language_punkt_vars = PunktLanguageVars
            language_punkt_vars.sent_end_chars = ('.', '?', ':')
            language_punkt_vars.internal_punctuation = (',', ';')
        else:
            print("No sentence tokenizer for this language available.")

        with open(pickle_path, 'rb') as open_pickle:
            tokenizer = pickle.load(open_pickle)
        tokenizer.INCLUDE_ALL_COLLOCS = True
        tokenizer.INCLUDE_ABBREV_COLLOCS = True
        params = tokenizer.get_params()
        sbd = PunktSentenceTokenizer(params)
        tokenized_sentences = []
        for sentence in sbd.sentences_from_text(untokenized_string,
                                                realign_boundaries=True):
            tokenized_sentences.append(sentence)
        return tokenized_sentences
