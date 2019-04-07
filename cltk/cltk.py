"""Primary module for CLTK pipeline."""

from typing import List

class CLTK:
    """Primary class for NLP pipeline."""

    def __init__(self, doc: str, language: str) -> None:
        """Constructor for CLTK class.

        >>> cltk = CLTK('Itaque metu.', language='la')
        >>> isinstance(cltk, CLTK)
        True
        """
        self.doc = doc
        self.language = language

        self.tokenize_word = self.get_word_tokenizer()

    def get_word_tokenizer(self):
        """Fetches and returns callable tokenizer for appropriate language."""
        from cltk.tokenize import Tokenize
        tokenize = Tokenize(language=self.language)
        return tokenize

    @property
    def sentences(self) -> List[str]:
        """Split sentences.

        >>> cltk = CLTK('Itaque metu. Quo tibi, imperator.', language='la')
        >>> cltk.sentences
        ['Itaque metu', 'Quo tibi, imperator.']
        """
        sentences_split = self.doc.split('. ')
        return sentences_split

    @property
    def words(self) -> List[str]:
        """Split words into tokens.

        >>> cltk = CLTK('Quo tibi, imperator.', language='la')
        >>> cltk.words
        ['Quo', 'tibi,', 'imperator.']

        >>> cltk = CLTK('Quo tibi, imperator.', language='id')
        >>> cltk.words
        Traceback (most recent call last):
          ..
        cltk.exceptions.exceptions.UnknownLanguageError
        """
        words = self.tokenize_word.tokenize_text(self.doc)
        return words
