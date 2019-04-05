""" Code for word tokenization: Old French
"""

__author__ = ['TK',
              'Patrick J. Burns <patrick@diyclassics.org']
__license__ = 'MIT License.'

from cltk.tokenize.word import BaseArabyWordTokenizer

def WordTokenizer():
    return ArabicArabyWordTokenizer()

class ArabicArabyWordTokenizer(BaseArabyWordTokenizer):
    """
    """
    def __init__(self: object, language:str = 'arabic'):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        super().__init__(language=language)

if __name__=="__main__":
    t = ArabicArabyWordTokenizer()
    print(t.tokenize('انما الْمُؤْمِنُونَ اخوه فاصلحوا بَيْنَ اخويكم'))
