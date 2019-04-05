""" Code for word tokenization: Greek
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import re

from nltk.tokenize.treebank import TreebankWordTokenizer

from cltk.tokenize.word import BasePunktWordTokenizer
from cltk.tokenize.greek.sentence import GreekRegexSentenceTokenizer

def WordTokenizer():
    return GreekPunktWordTokenizer()

class GreekPunktWordTokenizer(BasePunktWordTokenizer):
    """
    """

    def __init__(self: object, language:str = 'greek', sent_tokenizer=GreekRegexSentenceTokenizer):
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
    text = "Θουκυδίδης Ἀθηναῖος ξυνέγραψε τὸν πόλεμον τῶν Πελοποννησίων καὶ Ἀθηναίων, ὡς ἐπολέμησαν πρὸς ἀλλήλους, ἀρξάμενος εὐθὺς καθισταμένου καὶ ἐλπίσας μέγαν τε ἔσεσθαι καὶ ἀξιολογώτατον τῶν προγεγενημένων, τεκμαιρόμενος ὅτι ἀκμάζοντές τε ᾖσαν ἐς αὐτὸν ἀμφότεροι παρασκευῇ τῇ πάσῃ καὶ τὸ ἄλλο Ἑλληνικὸν ὁρῶν ξυνιστάμενον πρὸς ἑκατέρους, τὸ μὲν εὐθύς, τὸ δὲ καὶ διανοούμενον."
    w = GreekPunktWordTokenizer()
    tokens = w.tokenize(text)
    for i, token in enumerate(tokens, 1):
        print(f'{i}: {token}')
    pass
