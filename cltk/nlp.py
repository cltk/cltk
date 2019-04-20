"""Primary module for CLTK pipeline."""

from typing import List

from cltk.tokenizers import TokenizeWord
from cltk.wrappers.stanford import StanfordNLPWrapper


class NLP:
    """Primary class for NLP pipeline.

    >>> cltk_nlp = NLP(language='greek')
    Use ...
    >>> cltk_nlp.language
    'greek'

    #
    # >>> xen_anab = "Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι."
    # >>> nlp_xen_anab = cltk_nlp.parse_stanford(xen_anab)
    # >>> import stanfordnlp
    # >>> isinstance(nlp_xen_anab , stanfordnlp.pipeline.doc.Document)
    # True

    # >>> nlp_xen_anab.words
    # ['At', 'ille', 'ut', 'Carthaginem', 'venit,', 'multo', 'aliter,', 'ac', 'sperarat,', 'rem', 'publicam', 'se', 'habentem', 'cognovit.', 'Namque', 'diuturnitate', 'externi', 'mali', 'tantum', 'exarsit', 'intestinum', 'bellum,', 'ut', 'numquam', 'in', 'pari', 'periculo', 'fuerit', 'Carthago,', 'nisi', 'cum', 'deleta', 'est.', 'Primo', 'mercennarii', 'milites,', 'qui', 'adversus', 'Romanos', 'fuerant,', 'desciverunt;', 'quorum', 'numerus', 'erat', 'XX', 'milium.']
    # >>> nlp_xen_anab.sentences
    # ['At ille ut Carthaginem venit, multo aliter, ac sperarat, rem publicam se habentem cognovit', 'Namque diuturnitate externi mali tantum exarsit intestinum bellum, ut numquam in pari periculo fuerit Carthago, nisi cum deleta est', 'Primo mercennarii milites, qui adversus Romanos fuerant, desciverunt; quorum numerus erat XX milium.']
    """

    def __init__(self, language: str) -> None:
        """Constructor for CLTK class.

        # >>> cltk_nlp = NLP('Itaque metu.', language='la')
        # >>> isinstance(cltk_nlp, NLP)
        # True
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

        # >>> cltk_nlp = NLP('Itaque metu.', language='latin')
        # >>> isinstance(cltk_nlp.tokenizer_word, TokenizeWord)
        # True
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
    #     cltk.utils.exceptions.UnknownLanguageError
    #     """
    #     words = self.tokenizer_word.tokenize_text(self.doc)
    #     return words


if __name__ == '__main__':

    # stanford_nlp_obj = StanfordNLPWrapper(language='greek', treebank='grc_proiel')
    # nepos_hamilcar = 'At ille ut Carthaginem venit, multo aliter, ac sperarat, rem publicam se habentem cognovit. Namque diuturnitate externi mali tantum exarsit intestinum bellum, ut numquam in pari periculo fuerit Carthago, nisi cum deleta est. Primo mercennarii milites, qui adversus Romanos fuerant, desciverunt; quorum numerus erat XX milium.'


    cltk_nlp = NLP(language='greek')
    xen_anab = "Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι."

    nlp_xen_anab = cltk_nlp.parse_stanford(text=xen_anab)
    import stanfordnlp
    print(isinstance(nlp_xen_anab, stanfordnlp.pipeline.doc.Document) == True)  # True
    # print(dir(nlp_xen_anab))
    print(nlp_xen_anab.text == xen_anab)


    # 'conll_file', 'load_annotations', 'sentences', 'text', 'write_conll_to_file'
    # print(nlp_xen_anab.conll_file)
    # print(nlp_xen_anab.load_annotations)
    # print(nlp_xen_anab.write_conll_to_file)


    # sentences
    nlp_xen_anab_first_sent = nlp_xen_anab.sentences[0]
    # print(dir(nlp_xen_anab_first_sent))  # build_dependencies', 'dependencies', 'print_dependencies', 'print_tokens', 'print_words', 'tokens', 'words'
    print(nlp_xen_anab_first_sent.tokens[0].index == '1')
    print(nlp_xen_anab_first_sent.tokens[0].text == 'Δαρείου')
    first_word = nlp_xen_anab_first_sent.tokens[0].words[0]  # 'dependency_relation', 'feats', 'governor', 'index', 'lemma', 'parent_token', 'pos', 'text', 'upos', 'xpos'
    print(first_word.dependency_relation == 'iobj')
    print(first_word.feats == 'Case=Gen|Gender=Masc|Number=Sing')
    print(first_word.governor == 4)
    print(first_word.index == '1')
    print(first_word.lemma == 'Δαρεῖος')
    print(first_word.pos == 'Ne')
    print(first_word.text == 'Δαρείου')
    print(first_word.upos == 'PROPN')
    print(first_word.xpos == 'Ne')
    # print(first_word.parent_token)  # <Token index=1;words=[<Word index=1;text=Δαρείου;lemma=Δαρεῖος;upos=PROPN;xpos=Ne;feats=Case=Gen|Gender=Masc|Number=Sing;governor=4;dependency_relation=iobj>]>

    # print_dependencies
    # nlp_xen_anab_first_sent.print_dependencies()
    printed_dependencies = """('Δαρείου', '4', 'iobj')
('καὶ', '1', 'cc')
('Παρυσάτιδος', '1', 'conj')
('γίγνονται', '0', 'root')
('παῖδες', '4', 'nsubj')
('δύο,', '5', 'nmod')
('πρεσβύτερος', '5', 'amod')
('μὲν', '7', 'discourse')
('Ἀρταξέρξης,', '7', 'nsubj')
('νεώτερος', '7', 'conj')
('δὲ', '10', 'discourse')
('Κῦρος:', '10', 'orphan')
"""





