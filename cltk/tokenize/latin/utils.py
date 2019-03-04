""" Tokenization utilities: Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import pickle 

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.tokenize.punkt import PunktLanguageVars

from cltk.corpus.latin.readers import latinlibrary
from cltk.tokenize.latin.params import ABBREVIATIONS

from cltk.tokenize.utils import BaseSentenceTokenizerTrainer


class SentenceTokenizerTrainer(BaseSentenceTokenizerTrainer):
    """ """
    def __init__(self):
        BaseSentenceTokenizerTrainer.__init__(self, language='latin')

        
    def _tokenizer_setup(self):
        self.punctuation = ['.', '?', '!']
        self.strict = [';', ':', '—']


if __name__ == "__main__":
    text = latinlibrary.raw()
    trainer = SentenceTokenizerTrainer()
    tokenizer = trainer.train_sentence_tokenizer(text)
    trainer.pickle_sentence_tokenizer('{}.pickle'.format(trainer.language), tokenizer)
    
#    tokenizer = pickle.load(open('{}.pickle'.format(trainer.language), 'rb'))
