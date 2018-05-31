"""Tools for working with Levenshtein distance algorithm and distance ratio between strings.
"""

__author__ = ['Luke Hollis <lukehollis@gmail.com>', 'Eleftheria Chatziargyriou <ele.hatzy@gmail.com>']
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

        Args:
            :param w1: str
            :param w2: str
            :return: int

        Examples:

            >>> Levenshtein.Levenshtein_Distance('noctis', 'noctem')
            2

            >>> Levenshtein.Levenshtein_Distance('nox', 'nochem')
            4

            >>> Levenshtein.Levenshtein_Distance('orbis', 'robis')
            2
        """
        m, n = len(w1), len(w2)
        v1 = [i for i in range(n + 1)]
        v2 = [0 for i in range(n + 1)]

        for i in range(m):
            v2[0] = i + 1

            for j in range(n):
                delCost = v1[j + 1] + 1
                insCost = v2[j] + 1

                subCost = v1[j]
                if w1[i] != w2[j]: subCost += 1

                v2[j + 1] = min(delCost, insCost, subCost)
            v1, v2 = v2, v1

        return v1[-1]

    @staticmethod
    def Damerau_Levenshtein_Distance(w1, w2):
        """
        Computes Damerau-Levenshtein Distance between two words

        Args:
            :param w1: str
            :param w2: str
            :return int:

        Examples:
            For the most part, Damerau-Levenshtein behaves
            identically to Levenshtein:

            >>> Levenshtein.Damerau_Levenshtein_Distance('noctis', 'noctem')
            2

            >>> Levenshtein.Levenshtein_Distance('nox', 'nochem')
            4

            The strength of DL lies in detecting transposition of characters:

            >>> Levenshtein.Damerau_Levenshtein_Distance('orbis', 'robis')
            1

        """
        # Define alphabet
        alph = sorted(list(set(w1 + w2)))
        # Calculate alphabet size
        alph_s = len(alph)
        dam_ar = [0 for _ in range(alph_s)]
        mat = [[0 for _ in range(len(w2) + 2)] for _ in range(len(w1) + 2)]

        max_dist = len(w1) + len(w2)
        mat[0][0] = max_dist

        # Initialize matrix margin to the maximum possible distance (essentially inf) for ease of calculations (avoiding try blocks)

        for i in range(1, len(w1) + 2):
            mat[i][0] = max_dist
            mat[i][1] = i - 1

        for i in range(1, len(w2) + 2):
            mat[0][i] = max_dist
            mat[1][i] = i - 1

        for i in range(2, len(w1) + 2):
            tem = 0

            for j in range(2, len(w2) + 2):

                k = dam_ar[alph.index(w2[j - 2])]
                l = tem

                if w1[i - 2] == w2[j - 2]:
                    cost = 0
                    tem = j
                else:
                    cost = 1

                # The reccurence relation of DL is identical to that of Levenshtein with the addition of transposition
                mat[i][j] = min(mat[i - 1][j - 1] + cost, mat[i][j - 1] + 1, mat[i - 1][j] + 1,
                                mat[k - 1][l - 1] + i + j - k - l - 1)

            dam_ar[alph.index(w1[i - 2])] = i

        return mat[-1][-1]

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

        except ImportError as imp_err:  # pragma: no cover
            message = "'fuzzywuzzy' library required for this module: %s. Install with `pip install fuzzywuzzy python-Levenshtein`" % imp_err
            logger.error(message)
            print(message)
            raise ImportError

        return fuzz.ratio(string_a, string_b) / 100
    
  
