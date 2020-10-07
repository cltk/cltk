""" Code for word tokenization: Middle English
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License."

from cltk.tokenizers.word import RegexWordTokenizer

MiddleEnglishTokenizerPatterns = [
    (r"-", r" - "),
    (r"\n", r" "),
    (r"(?<=.)(?=[\.\";\,\:\[\]\(\)!&?])", r" "),
    (r"(?<=[\.\";\,\:\[\]\(\)!&?])(?=.)", r" "),
    (r"\s+", r" "),
]


class MiddleEnglishWordTokenizer(RegexWordTokenizer):
    """
    A regex-based tokenizer for Middle English.
    """

    def __init__(self):
        super().__init__(patterns=MiddleEnglishTokenizerPatterns)
