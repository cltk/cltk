"""Tokenizes sentences."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import pickle
from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer
import os


def tokenize_sentences(untokenized_string, language):
    """Reads language .pickle for right language"""
    if language == 'greek':
        path_rel = '~/cltk_data/greek/trained_model/cltk_linguistic_data/tokenizers/sentence/greek.pickle'  # pylint: disable=C0301
        language_punkt_vars = PunktLanguageVars
        language_punkt_vars.sent_end_chars = ('.', ';')
        language_punkt_vars.internal_punctuation = (',', '·')
    elif language == 'latin':
        path_rel = '~/cltk_data/latin/trained_model/cltk_linguistic_data/tokenizers/sentence/latin.pickle'  # pylint: disable=C0301
        language_punkt_vars = PunktLanguageVars
        language_punkt_vars.sent_end_chars = ('.', '?', ':')
        language_punkt_vars.internal_punctuation = (',', ';')
    else:
        print("No sentence tokenizer for this language available.")

    pickle_path = os.path.expanduser(path_rel)
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
