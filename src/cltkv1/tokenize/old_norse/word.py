""" Code for word tokenization: Old Norse
"""

__author__ = ['Clément Besnier <clemsciences@gmail.com>',
              'Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import re
from cltk.tokenize.word import BaseRegexWordTokenizer
from cltk.tokenize.old_norse.params import OldNorseTokenizerPatterns

def WordTokenizer():
    return OldNorseRegexWordTokenizer()

class OldNorseRegexWordTokenizer(BaseRegexWordTokenizer):
    """
    Old Norse word tokenizer using regex
    """
    #     # TODO dealing with merges between verbs at the second person of the present tense and þú
    #     # -> -tu, -ðu, -du, -u : question
    #
    #     # TODO dealing with merges between verbs and sik -> st : middle voice

    def __init__(self: object, language:str = 'old_norse', patterns=OldNorseTokenizerPatterns):
        """
        :param language : language for word tokenization
        :type language: str
        """
        self.patterns = patterns
        super().__init__(language=language, patterns=self.patterns)
