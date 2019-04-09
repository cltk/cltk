"""Primary module for CLTK pipeline."""

from typing import List

from cltk.tokenize import Tokenize

class NLP:
    """Primary class for NLP pipeline.

    >>> import cltk
    >>> nepos_hamilcar = 'At ille ut Carthaginem venit, multo aliter, ac sperarat, rem publicam se habentem cognovit. Namque diuturnitate externi mali tantum exarsit intestinum bellum, ut numquam in pari periculo fuerit Carthago, nisi cum deleta est. Primo mercennarii milites, qui adversus Romanos fuerant, desciverunt; quorum numerus erat XX milium.'
    >>> cltk_nlp = cltk.NLP(nepos_hamilcar, language='la')
    >>> cltk_nlp.language
    'la'
    >>> cltk_nlp.words
    ['At', 'ille', 'ut', 'Carthaginem', 'venit,', 'multo', 'aliter,', 'ac', 'sperarat,', 'rem', 'publicam', 'se', 'habentem', 'cognovit.', 'Namque', 'diuturnitate', 'externi', 'mali', 'tantum', 'exarsit', 'intestinum', 'bellum,', 'ut', 'numquam', 'in', 'pari', 'periculo', 'fuerit', 'Carthago,', 'nisi', 'cum', 'deleta', 'est.', 'Primo', 'mercennarii', 'milites,', 'qui', 'adversus', 'Romanos', 'fuerant,', 'desciverunt;', 'quorum', 'numerus', 'erat', 'XX', 'milium.']
    >>> cltk_nlp.sentences
    ['At ille ut Carthaginem venit, multo aliter, ac sperarat, rem publicam se habentem cognovit', 'Namque diuturnitate externi mali tantum exarsit intestinum bellum, ut numquam in pari periculo fuerit Carthago, nisi cum deleta est', 'Primo mercennarii milites, qui adversus Romanos fuerant, desciverunt; quorum numerus erat XX milium.']
    """

    def __init__(self, doc: str, language: str) -> None:
        """Constructor for CLTK class.

        >>> cltk_nlp = NLP('Itaque metu.', language='la')
        >>> isinstance(cltk_nlp, NLP)
        True
        """
        self.doc = doc
        self.language = language

        self.tokenize_word = self.get_word_tokenizer()  # type: Tokenize

    def get_word_tokenizer(self) -> Tokenize:
        """Fetches and returns callable tokenizer for appropriate language.

        >>> cltk_nlp = NLP('Itaque metu.', language='la')
        >>> isinstance(cltk_nlp.tokenize_word, Tokenize)
        True
        """
        return Tokenize(language=self.language)

    @property
    def sentences(self) -> List[str]:
        """Split sentences.

        >>> cltk_nlp = NLP('Itaque metu. Quo tibi, imperator.', language='la')
        >>> cltk_nlp.sentences
        ['Itaque metu', 'Quo tibi, imperator.']
        """
        sentences_split = self.doc.split('. ')
        return sentences_split

    @property
    def words(self) -> List[str]:
        """Split words into tokens.

        >>> cltk_nlp = NLP('Quo tibi, imperator.', language='la')
        >>> cltk_nlp.words
        ['Quo', 'tibi,', 'imperator.']

        >>> cltk_nlp = NLP('Quo tibi, imperator.', language='id')
        Traceback (most recent call last):
          ...
        cltk.exceptions.exceptions.UnknownLanguageError
        """
        words = self.tokenize_word.tokenize_text(self.doc)
        return words
