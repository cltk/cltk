""" Code for word tokenization: Middle English
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>', ]
__license__ = 'MIT License.'

import re
from cltk.tokenize.word import BaseRegexWordTokenizer
from cltk.tokenize.middle_english.params import MiddleEnglishTokenizerPatterns


def WordTokenizer():
    return MiddleEnglishRegexWordTokenizer()


class MiddleEnglishRegexWordTokenizer(BaseRegexWordTokenizer):
    """
    Middle English word tokenizer using regex
    """
    def __init__(self: object, language:str = 'middle_english', patterns=MiddleEnglishTokenizerPatterns):
        """
        :param language : language for word tokenization
        :type language: str
        """
        self.patterns = patterns
        super().__init__(language='middle_english', patterns=self.patterns)
