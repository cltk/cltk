""" Code for word tokenization: Middle High German
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>', ]
__license__ = 'MIT License.'

import re
from cltk.tokenize.word import BaseRegexWordTokenizer
from cltk.tokenize.middle_high_german.params import MiddleHighGermanTokenizerPatterns


def WordTokenizer():
    return MiddleHighGermanRegexWordTokenizer()


class MiddleHighGermanRegexWordTokenizer(BaseRegexWordTokenizer):
    """
    Middle High German word tokenizer using regex
    """
    def __init__(self: object, language:str = 'middle_high_german', patterns=MiddleHighGermanTokenizerPatterns):
        """
        :param language : language for word tokenization
        :type language: str
        """
        self.patterns = patterns
        super().__init__(language='middle_english', patterns=self.patterns)
