"""Module for tokenizers."""

from typing import List

class UnknownLanguageError(Exception):
    """Exception for when a user requests an NLP method that is not
    supported.
    """

def tokenizer_latin(text: str) -> List:
    """Latin word tokenizer.

    >>> catiline = 'Quo usque tandem abutere'
    >>> tokenizer_latin(text=catiline)
    ['Quo', 'usque', 'tandem', 'abutere']
    """
    words = text.split(' ')
    return words

class Tokenize:
    """Class for word tokenizing."""

    def __init__(self, language: str) -> None:
        """Constructor for Tokenizer class.

        >>> tokenize = Tokenize(language='la')
        >>> catiline = 'Quo usque tandem abutere'
        >>> tokenize.tokenize_text(catiline)
        ['Quo', 'usque', 'tandem', 'abutere']

        >>> tokenize = Tokenize(language='id')
        Traceback (most recent call last):
            ...
        cltk.tokenize.tokenize.UnknownLanguageError
        """
        self.language = language
        if self.language == 'la':
            self.tokenizer = tokenizer_latin
        else:
            raise UnknownLanguageError

    def tokenize_text(self, text) -> List[str]:
        """Tokenize text with appropriate tokenizer."""
        tokens = self.tokenizer(text=text)
        return tokens
