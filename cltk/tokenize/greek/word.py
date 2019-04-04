""" Code for word tokenization: Greek
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import re

from nltk.tokenize.treebank import TreebankWordTokenizer

from cltk.tokenize.word import BasePunktWordTokenizer
from cltk.tokenize.greek.sentence import SentenceTokenizer

def WordTokenizer():
    return GreekPunktSentenceTokenizer()

class GreekPunktWordTokenizer(BasePunktWordTokenizer):
    """
    """

    def __init__(self: object, language:str = 'greek', sent_tokenizer=SentenceTokenizer):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        super().__init__(language='greek')
        self.sent_tokenizer = sent_tokenizer()

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        sents = self.sent_tokenizer.tokenize(text)
        tokenizer = TreebankWordTokenizer()
        return [item for sublist in tokenizer.tokenize_sents(sents) for item in sublist]

if __name__ == '__main__':
    text = """ἀλλὰ τοὺς νόμους καὶ τὸν ὅρκον, ἐν ᾧ πρὸς ἅπασι τοῖς ἄλλοις δικαίοις καὶ τοῦτο γέγραπται, τὸ ὁμοίως ἀμφοῖν ἀκροάσασθαι. τοῦτο δ᾽ ἐστὶν οὐ μόνον τὸ μὴ προκατεγνωκέναι μηδέν, οὐδὲ τὸ τὴν εὔνοιαν ἴσην ἀποδοῦναι, ἀλλὰ τὸ καὶ τῇ τάξει καὶ τῇ ἀπολογίᾳ, ὡς βεβούληται καὶ προῄρηται τῶν ἀγωνιζομένων ἕκαστος, οὕτως ἐᾶσαι χρήσασθαι."""
    w = GreekPunktWordTokenizer()
    tokens = w.tokenize(text)
    for i, token in enumerate(tokens, 1):
        print(f'{i}: {token}')
    pass
