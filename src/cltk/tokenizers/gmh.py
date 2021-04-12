""" Code for word tokenization: Middle High German
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License."

from cltk.tokenizers.word import RegexWordTokenizer

# As far as I know, hyphens were never used for compounds, so the tokenizer treats all hyphens as line-breaks
MiddleHighGermanTokenizerPatterns = [
    (r"-\n", r"-"),
    (r"\n", r" "),
    (r"(?<=.)(?=[\.\";\,\:\[\]\(\)!&?])", r" "),
    (r"(?<=[\.\";\,\:\[\]\(\)!&?])(?=.)", r" "),
    (r"\s+", r" "),
]


class MiddleHighGermanWordTokenizer(RegexWordTokenizer):
    """
    A regex-based tokenizer for Middle High German.
    """

    def __init__(self):
        super().__init__(patterns=MiddleHighGermanTokenizerPatterns)
