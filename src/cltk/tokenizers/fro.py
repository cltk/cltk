""" Code for word tokenization: Old French
"""

__author__ = [
    "Natasha Voake <natashavoake@gmail.com>",
    "Patrick J. Burns <patrick@diyclassics.org>",
]
__license__ = "MIT License."

from cltk.tokenizers.word import RegexWordTokenizer

OldFrenchTokenizerPatterns = [
    (r"’", r"'"),
    (r"\'", r"' "),
    (r"(?<=.)(?=[.!?)(\";:,«»\-])", " "),
]


class OldFrenchWordTokenizer(RegexWordTokenizer):
    """
    A regex-based tokenizer for Old French.
    """

    def __init__(self):
        super().__init__(patterns=OldFrenchTokenizerPatterns)
