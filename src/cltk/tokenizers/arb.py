""" Code for word tokenization: Arabic
"""

__author__ = ["TK", "Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License."

from cltk.phonology.arb.utils.pyarabic import araby
from cltk.tokenizers.word import WordTokenizer


class ArabicWordTokenizer(WordTokenizer):
    """
    Class for word tokenizer using the pyarabic package:
    https://pypi.org/project/PyArabic/
    """

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        """
        return araby.tokenize(text)
