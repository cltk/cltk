"""
Offer tools for working with Levenshtein distance algorithm and distance ratio between strings.

Requirements:
fuzzywuzzy

Good-to-haves:
python-Levenshtein

"""

from cltk.tokenize.sentence import TokenizeSentence
from cltk.utils.cltk_logger import logger

try:
    from fuzzywuzzy import fuzz
except ImportError as imp_err:
    logger.error("'fuzzywuzzy' library required for this module: %s" % imp_err)
    raise ImportError


__author__ = 'Luke Hollis <lukehollis@gmail.com>'
__license__ = 'MIT License. See LICENSE.'


class Levenshtein:
    """A class for doing string similarity comparisons."""

    def __init__(self):
        """Initialize class. Currently empty."""
        return

    @staticmethod
    def ratio(self, string_a, string_b):
        """At the most basic level, return a Levenshtein distance ratio via
        fuzzywuzzy.
        :param string_a: str
        :param string_b: str
        :return: float
        """

        return fuzz.ratio(string_a, string_b)/100


    @staticmethod
    def distance_sentences(language, string_a, string_b):
        """Tokenize two input strings on sentence boundary and return a
        matrix of Levenshtein distance ratios.
        :param language: str (language name)
        :param string_a: str
        :param string_b: str
        :return: float
        """

        sentences_a = []
        sentences_b = []
        ratios = []

        # Make the latin tokenizer
        if language == "latin":
            sentence_tokenizer = TokenizeSentence('latin')

        # Make the greek tokenizer
        elif language == "greek":
            sentence_tokenizer = TokenizeSentence('greek')

        # Otherwise, if language, is unsupported, throw error stating accepted Language
        # values that may be used to tokenize sentences
        else:
            print("Language for sentence tokenization not recognized. "
                  "Accepted values are 'latin' and 'greek'.")
            return

        # Tokenize input strings
        sentences_a = sentence_tokenizer.tokenize_sentences(string_a)
        sentences_b = sentence_tokenizer.tokenize_sentences(string_b)

        # Build matrix of lev distance ratios
        for i, sent_a in enumerate(sentences_a):
            ratios.append([])
            for sent_b in sentences_b:
                ratios[i].append(fuzz.ratio(sent_a, sent_b)/100)

        return ratios
