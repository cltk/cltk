""" Code for punctuation removal: Old Norse
"""

__author__ = ["Clément Besnier <clemsciences@gmail.com>"]
__license__ = "MIT License."

# from cltk.tokenizers.word import RegexWordTokenizer

OLD_NORSE_PUNCTUATION: list[str] = [".", ",", ";", ":", '"', "'", "!", "?"]


class OldNorsePunctuationRemover:
    """Remove punctuation for Old Norse."""

    def __init__(self):
        pass

    def filter(self, word) -> bool:
        return word.string in OLD_NORSE_PUNCTUATION

    def __repr__(self) -> str:
        return f"<OldNorsePunctuationRemover>"

    def __call__(self, word) -> bool:
        return self.filter(word)
