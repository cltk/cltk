""" Code for word tokenization: Arabic
"""

__author__ = ['TK',
              'Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

from cltk.tokenize.word import BaseArabyWordTokenizer

def WordTokenizer():
    return ArabicArabyWordTokenizer()

class ArabicArabyWordTokenizer(BaseArabyWordTokenizer):
    """
    Arabic word tokenizer using the pyarabic package:
    https://pypi.org/project/PyArabic/
    """
    def __init__(self: object, language:str = 'arabic'):
        """
        :param language : language for word tokenization
        :type language: str
        """
        super().__init__(language=language)
