"""Build a sentence tokenizer for Greek.
Some guidance available here: http://wiki.apertium.org/wiki/Sentence_segmenting
"""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import pickle
from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer
import os
import sys


CLTK_DATA_DIR_REL = '~/cltk_data'
CLTK_DATA_DIR_ABS = os.path.expanduser(CLTK_DATA_DIR_REL)
GREEK_SENTENCE_TOKENIZER_DIR = os.path.join(CLTK_DATA_DIR_ABS,
                                            'compiled/sentence_tokens_greek')
PICKLE_FILE = 'greek.pickle'
PICKLE_FILE_PATH = os.path.join(GREEK_SENTENCE_TOKENIZER_DIR, PICKLE_FILE)

def tokenize_greek_sentences(input_string):
    """Tokenize incoming Greek strings and output a list.
    :param input_string: str
    :rtype : list
    """
    try:
        with open(PICKLE_FILE_PATH, 'rb') as open_pickle:
            training_set = pickle.load(open_pickle)
    except FileNotFoundError as err:
        print('greek.pickle not found. Install Greek sentence tokenization ruleset. Error: %s' % err)
        sys.exit()
    language_punkt_vars = PunktLanguageVars
    language_punkt_vars.sent_end_chars = ('.', ';',)
    language_punkt_vars.internal_punctuation = (',', '·')
    training_set.INCLUDE_ALL_COLLOCS = True
    training_set.INCLUDE_ABBREV_COLLOCS = True

    params = training_set.get_params()
    sbd = PunktSentenceTokenizer(params)
    tokenized_sentences = []
    for sentence in sbd.sentences_from_text(input_string,
                                            realign_boundaries=True):
        tokenized_sentences.append(sentence)
    return tokenized_sentences
