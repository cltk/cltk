"""Tools for working with Levenshtein distance algorithm and distance ratio between strings.
"""

__author__ = ['Luke Hollis <lukehollis@gmail.com>','Eleftheria Chatziargyriou <ele.hatzy@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


class Levenshtein:
    """A wrapper class for fuzzywuzzy's Levenshtein distance calculation methods."""

    def __init__(self):
        """Initialize class. Currently empty."""
        return

    @staticmethod
    def Levenshtein_Distance(w1, w2):
        """
        Computes Levenshtein Distance between two words
        
        :param w1: str
        :param w2: str
        :return: int
        """
        m,n = len(w1), len(w2)
        v1 = [i for i in range(n)]+[0]
        v2 = [0 for i in range(n+1)]
        
        for i in range(m):
            v2[0]+=1
            
            for j in range(n):
                delCost = v1[j+1] + 1
                insCost = v2[j] + 1
                
                subCost = v1[j]
                if w1[i] != w2[j]: subCost += 1
                
                v2[j+1] = min(delCost, insCost, subCost)
                
            v1,v2 = v2,v1
                
        return v1[n]
    
    @staticmethod
    def ratio(string_a, string_b):
        """At the most basic level, return a Levenshtein distance ratio via
        fuzzywuzzy.
        :param string_a: str
        :param string_b: str
        :return: float
        """
        from cltk.utils.cltk_logger import logger
        try: 
            from fuzzywuzzy import fuzz
        
        except ImportError as imp_err: # pragma: no cover
            message = "'fuzzywuzzy' library required for this module: %s. Install with `pip install fuzzywuzzy python-Levenshtein`" % imp_err
            logger.error(message)
            print(message)
            raise ImportError
            
        return fuzz.ratio(string_a, string_b)/100
