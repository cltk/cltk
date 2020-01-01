"""Module for tokenizers.

TODO: Think about adding check somewhere if a contrib (not user) chooses an unavailable item
"""

from dataclasses import dataclass
from typing import Callable

from cltk.tokenize.word import WordTokenizer

from cltkv1.utils.data_types import Process, Doc


# a closure for marshalling Docs to CLTK tokenizers
def make_tokenizer_algorithm(language : str) -> Callable[[Doc], Doc]:
    tokenizer = WordTokenizer(language = language)

    def algorithm(self, doc : Doc) -> Doc:
        doc.tokens = tokenizer.tokenize(doc.raw)
        return doc

    return algorithm

AKKADIAN_WORD_TOK = make_tokenizer_algorithm(language="akkadian")
ARABIC_WORD_TOK = make_tokenizer_algorithm(language="arabic")
GREEK_WORD_TOK = make_tokenizer_algorithm(language="greek")
LATIN_WORD_TOK = make_tokenizer_algorithm(language="latin")
MIDDLE_ENGLISH_WORD_TOK = make_tokenizer_algorithm(language="middle_english")
MIDDLE_FRENCH_WORD_TOK = make_tokenizer_algorithm(language="middle_french")
MIDDLE_HIGH_GERMAN_WORD_TOK = make_tokenizer_algorithm(language="middle_high_german")
MULTILINGUAL_WORD_TOK = make_tokenizer_algorithm(language="multilingual")
OLD_FRENCH_WORD_TOK = make_tokenizer_algorithm(language="old_french")
OLD_NORSE_WORD_TOK = make_tokenizer_algorithm(language="old_norse")
SANSKRIT_WORD_TOK = make_tokenizer_algorithm(language="sanskrit")


@dataclass
class TokenizationProcess(Process):
    """To be inherited for each language's tokenization declarations.

    Example: ``TokenizationProcess`` -> ``LatinTokenizationProcess``

    >>> from cltkv1.tokenizers.word import TokenizationProcess
    >>> from cltkv1.utils.data_types import Process
    >>> issubclass(TokenizationProcess, Process)
    True
    >>> tok = TokenizationProcess(input_doc = Doc(raw="some input data"))
    """

    language = None


@dataclass
class DefaultTokenizationProcess(TokenizationProcess):
    """The default tokenization algorithm.

    >>> from cltkv1.tokenizers.word import DefaultTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = DefaultTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["non"][:29]))
    >>> tok.description
    'Whitespace tokenizer inheriting from the NLTK'
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    algorithm = MULTILINGUAL_WORD_TOK
    description = "Whitespace tokenizer inheriting from the NLTK"
    language = None


@dataclass
class LatinTokenizationProcess(TokenizationProcess):
    """The default Latin tokenization algorithm.

    >>> from cltkv1.tokenizers import LatinTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = LatinTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["lat"][:23]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['Gallia', 'est', 'omnis', 'divisa']
    """

    algorithm = LATIN_WORD_TOK
    description = "Default tokenizer for Latin"
    language = "lat"


@dataclass
class GreekTokenizationProcess(TokenizationProcess):
    """The default Greek tokenization algorithm.

    >>> from cltkv1.tokenizers import GreekTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = GreekTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["grc"][:23]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['ὅτι', 'μὲν', 'ὑμεῖς', ',', 'ὦ', 'ἄνδρες']
    """

    algorithm = GREEK_WORD_TOK
    description = "Default Greek tokenizer"
    language = "grc"


@dataclass
class AkkadianTokenizationProcess(TokenizationProcess):
    """The default Akkadian tokenization algorithm.

    >>> from cltkv1.tokenizers import AkkadianTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = AkkadianTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["akk"]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    [('u2-wa-a-ru', 'akkadian'), ('at-ta', 'akkadian'), ('e2-kal2-la-ka', 'akkadian'), ('_e2_-ka', 'sumerian'), ('wu-e-er', 'akkadian')]
    """

    algorithm = AKKADIAN_WORD_TOK
    description = "Default Akkadian tokenizer"
    language = "akk"


@dataclass
class OldNorseTokenizationProcess(TokenizationProcess):
    """The default OldNorse tokenization algorithm.

    >>> from cltkv1.tokenizers import OldNorseTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = OldNorseTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["non"][:29]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    algorithm = OLD_NORSE_WORD_TOK
    description = "Default Old Norse tokenizer"
    language = "non"


@dataclass
class MHGTokenizationProcess(TokenizationProcess):
    """The default Middle High German tokenization algorithm.

    >>> from cltkv1.tokenizers import MHGTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = MHGTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["gmh"][:29]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['Ik', 'gihorta', 'ðat', 'seggen', 'ðat', 'sih']
    """

    algorithm = MIDDLE_HIGH_GERMAN_WORD_TOK
    description = "The default Middle High German tokenizer"
    language = "gmh"


@dataclass
class ArabicTokenizationProcess(TokenizationProcess):
    """The default Arabic tokenization algorithm.

    >>> from cltkv1.tokenizers import ArabicTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = ArabicTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["arb"][:34]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['كهيعص', '﴿', '١', '﴾', 'ذِكْرُ', 'رَحْمَتِ', 'رَبِّكَ']
    """

    algorithm = ARABIC_WORD_TOK
    description = "Default Arabic tokenizer"
    language = "arb"


@dataclass
class OldFrenchTokenizationProcess(TokenizationProcess):
    """The default Old French tokenization algorithm.

    >>> from cltkv1.tokenizers import OldFrenchTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = OldFrenchTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["fro"][:37]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['Une', 'aventure', 'vos', 'voil', 'dire', 'Molt', 'bien']
    """

    algorithm = OLD_FRENCH_WORD_TOK
    description = "Default Old French tokenizer"
    language = "fro"


@dataclass
class MiddleFrenchTokenizationProcess(TokenizationProcess):
    """The default Middle French tokenization algorithm.

    >>> from cltkv1.tokenizers import MiddleFrenchTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = MiddleFrenchTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["frm"][:37]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['Attilius', 'Regulus', ',', 'general', 'de', "l'", 'armée']
    """

    algorithm = MIDDLE_FRENCH_WORD_TOK
    description = "Default Middle French tokenizer"
    language = "frm"


@dataclass
class MiddleEnglishTokenizationProcess(TokenizationProcess):
    """The default Middle English tokenization algorithm.

    >>> from cltkv1.tokenizers import MiddleEnglishTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = MiddleEnglishTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["enm"][:31]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['Whilom', ',', 'as', 'olde', 'stories', 'tellen']
    """

    algorithm = MIDDLE_ENGLISH_WORD_TOK
    description = "Default Middle English tokenizer"
    language = "enm"


@dataclass
class SanskritTokenizationProcess(TokenizationProcess):
    """The default Middle English tokenization algorithm.

    >>> from cltkv1.tokenizers import SanskritTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = SanskritTokenizationProcess(input_doc = Doc(raw=EXAMPLE_TEXTS["san"][:31]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['ईशा', 'वास्यम्', 'इदं', 'सर्वं', 'यत्', 'किञ्च']
    """

    algorithm = SANSKRIT_WORD_TOK
    description = "The default Middle English tokenizer"
    language = "san"
