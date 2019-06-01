""" Code for word tokenization: Old French
"""

__author__ = ['Natasha Voake <natashavoake@gmail.com>',
              'Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

from cltk.tokenize.word import BaseRegexWordTokenizer
from cltk.tokenize.old_french.params import OldFrenchTokenizerPatterns

def WordTokenizer():
    return OldFrenchRegexWordTokenizer()

class OldFrenchRegexWordTokenizer(BaseRegexWordTokenizer):
    """
    Old French word tokenizer using regex
    """
    def __init__(self: object, language:str = 'old_french', patterns=OldFrenchTokenizerPatterns):
        """
        :param language : language for word tokenization
        :type language: str
        """
        self.patterns = patterns
        super().__init__(language=language, patterns=self.patterns)
