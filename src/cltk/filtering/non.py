""" Code for punctuation removal: Old Norse
"""

__author__ = ["Clément Besnier <clemsciences@gmail.com>"]
__license__ = "MIT License."

from cltk.tokenizers.word import RegexWordTokenizer

OLD_NORSE_PUNCTUATION = [".", ",", ";", ":", '"', "'", "!", "?"]


class OldNorsePunctuationRemover:
    """"""

    def __init__(self):
        pass

    def filter(self, word):
        return word.string in OLD_NORSE_PUNCTUATION

    def __repr__(self):
        return f"<OldNorsePunctuationRemover>"

    def __call__(self, word):
        return self.filter(word)
