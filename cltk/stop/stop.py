""" Code for building and working with stoplists
"""

## Goal: to build a stop list of from top 100 count using Counter

from collections import Counter

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'GPL License.'


class Stoplist():
    """ Create stoplists
    """

    def __init__(self, language=None):
        """ Initialize stoplist builder with option for language specific parameters
        :type language: str
        :param language : text from which to build the stoplist
        """
        self.language = language.lower()

    def build_stoplist(text, size=100):
        """
        :type language: int
        :param language : size of the output list
        :type language: str
        :param language : language in case of language-specific considerations
        """
        
        if self.language = 'latin':
            pass
            # set preprocessing
        else:
            pass
        
        text = text.split() # Load real tokenizer
        c = Counter(text)
        return c.most_common(size)
