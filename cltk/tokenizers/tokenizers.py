"""Module for tokenizers."""

from typing import List

def tokenizer_latin(text: str) -> List[str]:
    """Latin word tokenizer. Just for example.

    >>> catiline = 'Quo usque tandem abutere'
    >>> tokenizer_latin(text=catiline)
    ['Quo', 'usque', 'tandem', 'abutere']
    """
    words = text.split(' ')
    return words


def tokenizer_generic(text: str) -> List[str]:
    """Latin word tokenizer. Just for example

    >>> catiline = 'Quo usque tandem abutere'
    >>> tokenizer_latin(text=catiline)
    ['Quo', 'usque', 'tandem', 'abutere']
    """
    words = text.split(' ')
    return words


class TokenizeWord:
    """Class for word tokenizing.

    TODO: Add doctest to illustrate expected use.
    """

    def __init__(self, language: str) -> None:
        """Constructor for Tokenizer class.

        >>> tokenize = TokenizeWord(language='latin')
        >>> catiline = 'Quo usque tandem abutere'
        >>> tokenize.tokenize_text(catiline)
        ['Quo', 'usque', 'tandem', 'abutere']

        >>> tokenize = TokenizeWord(language='UNKNOWNLANG')
        >>> text = 'AAA BBB CCC DDD'
        >>> tokenize.tokenize_text(text=text)
        ['AAA', 'BBB', 'CCC', 'DDD']
        """
        self.language = language
        if self.language == 'latin':
            self.tokenizer = tokenizer_latin
        else:
            self.tokenizer = tokenizer_generic

    def tokenize_text(self, text: str) -> List[str]:
        """Tokenize text with appropriate tokenizer."""
        tokens = self.tokenizer(text=text)
        return tokens
