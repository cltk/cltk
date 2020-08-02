""" Code for word tokenization: Old Norse
"""

__author__ = [
    "Clément Besnier <clemsciences@gmail.com>",
    "Patrick J. Burns <patrick@diyclassics.org>",
]
__license__ = "MIT License."

from cltk.tokenizers.word import RegexWordTokenizer

# As far as I know, hyphens were never used for compounds, so the tokenizer treats all hyphens as line-breaks
OldNorseTokenizerPatterns = [(r"\'", r"' "), (r"(?<=.)(?=[.!?)(\";:,«»\-])", " ")]


class OldNorseWordTokenizer(RegexWordTokenizer):
    """A regex-based tokenizer for Old Norse."""

    def __init__(self):
        super().__init__(patterns=OldNorseTokenizerPatterns)
