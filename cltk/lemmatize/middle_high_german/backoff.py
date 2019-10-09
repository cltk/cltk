"""Module for lemmatizing Middle High German—includes several classes for different
lemmatizing approaches--based on training data, etc.
 These can be chained together using the backoff parameter. Also,
includes a pre-built chain that uses models in latin_models_cltk repo
called BackoffMHGLemmatizer.

The logic behind the backoff lemmatizer is based on backoff POS-tagging in
NLTK and repurposes several of the tagging classes for lemmatization
tasks. See here for more info on sequential backoff tagging in NLTK:
http://www.nltk.org/_modules/nltk/tag/sequential.html
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>', 'Clément Besnier <clemsciences@aol.com>']
__license__ = 'MIT License. See LICENSE.'

import os
import re
from typing import List, Dict, Tuple, Set, Any, Generator
import reprlib

from cltk import get_cltk_data_dir
from cltk.lemmatize.backoff import IdentityLemmatizer, DictLemmatizer, UnigramLemmatizer

from cltk.utils.file_operations import open_pickle


# Unused for now
# def backoff_lemmatizer(train_sents, lemmatizer_classes, backoff=None):
#    """From Python Text Processing with NLTK Cookbook."""
#    for cls in lemmatizer_classes:
#        backoff = cls(train_sents, backoff=backoff)
#    return backoff

def _randomize_data(train: List[list], seed: int):
    import random
    random.seed(seed)
    random.shuffle(train)
    pos_train_sents = train[:4000]
    lem_train_sents = [[(item[0], item[1]) for item in sent] for sent in train]
    train_sents = lem_train_sents[:4000]
    test_sents = lem_train_sents[4000:5000]

    return pos_train_sents, train_sents, test_sents


class BackoffMHGLemmatizer:
    """Suggested backoff chain; includes at least on of each
    type of major sequential backoff class from backoff.py
    """

    models_path = os.path.normpath(get_cltk_data_dir() +
                                   '/middle_high_german/model/middle_high_german_models_cltk/lemmata/backoff')

    def __init__(self, train: List[list] = None, seed: int = 3, verbose: bool = False):
        self.models_path = BackoffMHGLemmatizer.models_path

        missing_models_message = "BackoffLatinLemmatizer requires the ```middle_high_german_models_cltk``` " \
                                 "to be in cltk_data. Please load this corpus."
        self.train = train
        self.seed = seed
        self.VERBOSE = verbose

        try:
            self.train = open_pickle(os.path.join(self.models_path, 'middle_high_german_pos_lemmatized_sents.pickle'))
            self.LATIN_OLD_MODEL = open_pickle(os.path.join(self.models_path, 'middle_high_german_lemmata_cltk.pickle'))
            self.LATIN_MODEL = open_pickle(os.path.join(self.models_path, 'middle_high_german_model.pickle'))
        except FileNotFoundError as err:
            raise type(err)(missing_models_message)

        self.pos_train_sents, self.train_sents, self.test_sents = _randomize_data(self.train, self.seed)
        self._define_lemmatizer()

    def _define_lemmatizer(self):
        # Suggested backoff chain--should be tested for optimal order
        self.backoff0 = None
        self.backoff1 = IdentityLemmatizer(verbose=self.VERBOSE)
        self.backoff2 = DictLemmatizer(lemmas=self.MHG_OLD_MODEL, source='ReferenzKorpus Mittelhochdeutsch Lemmata',
                                       backoff=self.backoff1, verbose=self.VERBOSE)
        self.backoff3 = UnigramLemmatizer(self.train_sents, source='CLTK Sentence Training Data', backoff=self.backoff2,
                                          verbose=self.VERBOSE)
        # self.backoff4 = DictLemmatizer(lemmas=self.MHG_MODEL, source='Latin Model', backoff=self.backoff3,
        #                                verbose=self.VERBOSE)
        self.lemmatizer = self.backoff3

    def lemmatize(self, tokens: List[str]):
        lemmas = self.lemmatizer.lemmatize(tokens)
        return lemmas

    def evaluate(self):
        if self.VERBOSE:
            raise AssertionError("evaluate() method only works when verbose: bool = False")
        return self.lemmatizer.evaluate(self.test_sents)

    def __repr__(self):
        return f'<BackoffMHGLemmatizer v0.1>'


# Accuracty test available below——keep? delete?
# if __name__ == "__main__":
#
#    # Set up training sentences
#    rel_path = os.path.join('~/cltk_data/latin/model/latin_models_cltk/lemmata/backoff')
#    path = os.path.expanduser(rel_path)
#
#    # Check for presence of latin_pos_lemmatized_sents
#    file = 'latin_pos_lemmatized_sents.pickle'
#
#    latin_pos_lemmatized_sents_path = os.path.join(path, file)
#    if os.path.isfile(latin_pos_lemmatized_sents_path):
#        latin_pos_lemmatized_sents = open_pickle(latin_pos_lemmatized_sents_path)
#    else:
#        latin_pos_lemmatized_sents = []
#        print('The file %s is not available in cltk_data' % file)
#
#
#    RUN = 10
#    ACCURACIES = []
#
#    for I in range(RUN):
#        LEMMATIZER = BackoffLatinLemmatizer(latin_pos_lemmatized_sents)
#        ACC = LEMMATIZER.evaluate()
#        ACCURACIES.append(ACC)
#        print('{:.2%}'.format(ACC))
#
#    print('\nTOTAL (Run %d) times' % RUN)
#    print('{:.2%}'.format(sum(ACCURACIES) / RUN))
