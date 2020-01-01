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

    def algorithm(input_doc : Doc) -> Doc:
        return tokenizer.tokenize(input_doc.raw)

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
    >>> tok = TokenizationProcess(data_input="some input data")
    """

    language = None


@dataclass
class DefaultTokenizationProcess(TokenizationProcess):
    """The default tokenization algorithm.

    >>> from cltkv1.tokenizers.word import DefaultTokenizationProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> tok = DefaultTokenizationProcess(data_input=EXAMPLE_TEXTS["non"][:29])
    >>> tok.description
    'Whitespace tokenizer inheriting from the NLTK'
    >>> tok.data_output
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
    >>> tok = LatinTokenizationProcess(data_input=EXAMPLE_TEXTS["lat"][:23])
    >>> tok.data_output
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
    >>> tok = GreekTokenizationProcess(data_input=EXAMPLE_TEXTS["grc"][:23])
    >>> tok.data_output
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
    >>> tok = AkkadianTokenizationProcess(data_input=EXAMPLE_TEXTS["akk"])
    >>> tok.data_output
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
    >>> tok = OldNorseTokenizationProcess(data_input=EXAMPLE_TEXTS["non"][:29])
    >>> tok.data_output
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
    >>> tok = MHGTokenizationProcess(data_input=EXAMPLE_TEXTS["gmh"][:29])
    >>> tok.data_output
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
    >>> tok = ArabicTokenizationProcess(data_input=EXAMPLE_TEXTS["arb"][:34])
    >>> tok.data_output
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
    >>> tok = OldFrenchTokenizationProcess(data_input=EXAMPLE_TEXTS["fro"][:37])
    >>> tok.data_output
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
    >>> tok = MiddleFrenchTokenizationProcess(data_input=EXAMPLE_TEXTS["frm"][:37])
    >>> tok.data_output
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
    >>> tok = MiddleEnglishTokenizationProcess(data_input=EXAMPLE_TEXTS["enm"][:31])
    >>> tok.data_output
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
    >>> tok = SanskritTokenizationProcess(data_input=EXAMPLE_TEXTS["san"][:31])
    >>> tok.data_output
    ['ईशा', 'वास्यम्', 'इदं', 'सर्वं', 'यत्', 'किञ्च']
    """

    algorithm: Callable = SANSKRIT_WORD_TOK
    description = "The default Middle English tokenizer"
    language = "san"
