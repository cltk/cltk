"""Tools for working with Levenshtein distance algorithm and distance ratio between strings.
"""

from cltk.utils.cltk_logger import logger
try:
    from fuzzywuzzy import fuzz
except ImportError as imp_err:
    message = "'fuzzywuzzy' library required for this module: %s. Install with `pip install fuzzywuzzy python-Levenshtein`" % imp_err
    logger.error(message)
    print(message)
    raise ImportError


__author__ = ['Luke Hollis <lukehollis@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


class Levenshtein:
    """A wrapper class for fuzzywuzzy's Levenshtein distance calculation methods."""

    def __init__(self):
        """Initialize class. Currently empty."""
        return

    @staticmethod
    def ratio(string_a, string_b):
        """At the most basic level, return a Levenshtein distance ratio via
        fuzzywuzzy.
        :param string_a: str
        :param string_b: str
        :return: float
        """

        return fuzz.ratio(string_a, string_b)/100
