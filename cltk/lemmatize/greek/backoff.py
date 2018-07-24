"""Module for lemmatizing Greek—NOT READY
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

import os
import pickle

import re

from cltk.lemmatize.backoff import (DefaultLemmatizer, IdentityLemmatizer,
                                    UnigramLemmatizer, RegexpLemmatizer,
                                    TrainLemmatizer, DictionaryLemmatizer)
from cltk.lemmatize.greek.greek import greek_sub_patterns, greek_pps
from cltk.lemmatize.greek.greek_model import GREEK_MODEL
from cltk.utils.file_operations import open_pickle


class PPLemmatizer(RegexpLemmatizer):
    # Not implemented yet
    pass

class BackoffLemmatizer(object):
    """Suggested backoff chain; includes at least on of each
    type of major sequential backoff class from backoff.py

    ### Putting it all together
    ### BETA Version of the Backoff Lemmatizer
    """

    def __init__(self, train=None):
        self.GREEK_MODEL = GREEK_MODEL
        self.greek_sub_patterns = greek_sub_patterns
        # self.tagged_sents = self._get_tagged_sents()
        self.train_sents = train
#        self.greek_verb_patterns = greek_verb_patterns
#        self.greek_pps = greek_pps
        self.rel_path = os.path.join('~/cltk_data/greek/model/greek_models_cltk/lemmata/backoff')
        self.path = os.path.expanduser(self.rel_path)

        # Check for presence of GREEK_OLD_MODEL
        file = 'greek_lemmata_cltk.pickle'

        old_model_path = os.path.join(self.path, file)
        if os.path.isfile(old_model_path):
            self.GREEK_OLD_MODEL = open_pickle(old_model_path)
        else:
            self.GREEK_OLD_MODEL = {}
            print('The file %s is not available in cltk_data' % file)

        self._define_lemmatizer()

    def _define_lemmatizer(self):
        #Suggested backoff chain--should be tested for optimal order
        backoff0 = None
        backoff1 = IdentityLemmatizer()
        backoff2 = DictionaryLemmatizer(model=self.GREEK_OLD_MODEL, backoff=backoff1)
        backoff3 = RegexpLemmatizer(self.greek_sub_patterns, backoff=backoff2)
        backoff4 = TrainLemmatizer(train=self.train_sents, backoff=backoff3)
        backoff5 = DictionaryLemmatizer(model=self.GREEK_MODEL, backoff=backoff4)
        self.lemmatizer = backoff5


    def lemmatize(self, tokens):
        lemmas = self.lemmatizer.lemmatize(tokens)
        return lemmas


if __name__ == "__main__":
    tagged_sents = pickle.load(open("greek_tagged_sents.p", "rb" ))
    from random import Random
    Random(4).shuffle(tagged_sents)
    train_sents = tagged_sents[:30000]

    l = BackoffLemmatizer(train=train_sents)
    test = """περὶ πολλοῦ ἂν ποιησαίμην , ὦ ἄνδρες , τὸ τοιούτους ὑμᾶς ἐμοὶ
    δικαστὰς περὶ τούτου τοῦ πράγματος γενέσθαι, οἷοίπερ ἂν ὑμῖν αὐτοῖς εἴητε
    τοιαῦτα πεπονθότες: εὖ γὰρ οἶδ᾽ ὅτι, εἰ τὴν αὐτὴν γνώμην περὶ τῶν ἄλλων
    ἔχοιτε, ἥνπερ περὶ ὑμῶν αὐτῶν, οὐκ ἂν εἴη: ὅστις οὐκ ἐπὶ τοῖς γεγενημένοις
    ἀγανακτοίη , ἀλλὰ πάντες ἂν περὶ τῶν τὰ τοιαῦτα ἐπιτηδευόντων τὰς ζημίας
    μικρὰς ἡγοῖσθε .""".split()
    print(l.lemmatize(test))
