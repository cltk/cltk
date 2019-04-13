"""Primary module for CLTK pipeline."""

from typing import List

from cltk.tokenizers import TokenizeWord
from cltk.wrappers.stanford import StanfordNLPWrapper


class NLP:
    """Primary class for NLP pipeline.

    >>> import cltk
    >>> nepos_hamilcar = 'At ille ut Carthaginem venit, multo aliter, ac sperarat, rem publicam se habentem cognovit. Namque diuturnitate externi mali tantum exarsit intestinum bellum, ut numquam in pari periculo fuerit Carthago, nisi cum deleta est. Primo mercennarii milites, qui adversus Romanos fuerant, desciverunt; quorum numerus erat XX milium.'
    >>> cltk_nlp = cltk.NLP(nepos_hamilcar, language='la')
    >>> cltk_nlp.language
    'la'
    # >>> cltk_nlp.words
    # ['At', 'ille', 'ut', 'Carthaginem', 'venit,', 'multo', 'aliter,', 'ac', 'sperarat,', 'rem', 'publicam', 'se', 'habentem', 'cognovit.', 'Namque', 'diuturnitate', 'externi', 'mali', 'tantum', 'exarsit', 'intestinum', 'bellum,', 'ut', 'numquam', 'in', 'pari', 'periculo', 'fuerit', 'Carthago,', 'nisi', 'cum', 'deleta', 'est.', 'Primo', 'mercennarii', 'milites,', 'qui', 'adversus', 'Romanos', 'fuerant,', 'desciverunt;', 'quorum', 'numerus', 'erat', 'XX', 'milium.']
    # >>> cltk_nlp.sentences
    # ['At ille ut Carthaginem venit, multo aliter, ac sperarat, rem publicam se habentem cognovit', 'Namque diuturnitate externi mali tantum exarsit intestinum bellum, ut numquam in pari periculo fuerit Carthago, nisi cum deleta est', 'Primo mercennarii milites, qui adversus Romanos fuerant, desciverunt; quorum numerus erat XX milium.']
    """

    def __init__(self, language: str) -> None:
        """Constructor for CLTK class.

        >>> cltk_nlp = NLP('Itaque metu.', language='la')
        >>> isinstance(cltk_nlp, NLP)
        True
        """
        self.language = language
        self.tokenizer_word = self._get_word_tokenizer()  # type: TokenizeWord
        self.stanford_obj = self._get_stanford_model()

    def parse_stanford(self, text: str):
        """Do the actual parsing of input text."""
        return self.stanford_obj.parse(text=text)

    def _get_stanford_model(self):
        """If available for a given language, get the entire
        object returned by the `stanfordnlp` project.
        """
        # return 'STAND IN FOR STANFORD OBJECT'
        return StanfordNLPWrapper(language=self.language)

    def _get_word_tokenizer(self) -> TokenizeWord:
        """Fetches and returns callable tokenizer for
        appropriate language.

        >>> cltk_nlp = NLP('Itaque metu.', language='latin')
        >>> isinstance(cltk_nlp.tokenizer_word, TokenizeWord)
        True
        """
        return TokenizeWord(language=self.language)

    # @property
    # def sentences(self) -> List[str]:
    #     """Split sentences.
    #
    #     >>> cltk_nlp = NLP('Itaque metu. Quo tibi, imperator.', language='la')
    #     >>> cltk_nlp.sentences
    #     ['Itaque metu', 'Quo tibi, imperator.']
    #     """
    #     sentences_split = self.doc.split('. ')
    #     return sentences_split

    # @property
    # def words(self) -> List[str]:
    #     """Split words into tokens.
    #
    #     >>> cltk_nlp = NLP('Quo tibi, imperator.', language='la')
    #     >>> cltk_nlp.words
    #     ['Quo', 'tibi,', 'imperator.']
    #
    #     >>> cltk_nlp = NLP('Quo tibi, imperator.', language='id')
    #     Traceback (most recent call last):
    #       ...
    #     cltk.exceptions.exceptions.UnknownLanguageError
    #     """
    #     words = self.tokenizer_word.tokenize_text(self.doc)
    #     return words


if __name__ == '__main__':

    # stanford_nlp_obj = StanfordNLPWrapper(language='greek', treebank='grc_proiel')
    cltk_nlp = NLP(language='greek')
    some_text = "Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι."

    stanford_parses = cltk_nlp.parse_stanford(text=some_text)
    print(dir(stanford_parses))  # 'conll_file', 'load_annotations', 'sentences', 'text', 'write_conll_to_file'
    print(stanford_parses)
