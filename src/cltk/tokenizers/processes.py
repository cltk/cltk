"""Module for tokenizers.

TODO: Think about adding check somewhere if a contrib (not user) chooses an unavailable item
"""

from dataclasses import dataclass
from typing import Callable

from boltons.cacheutils import cachedproperty
from cltk.tokenize.word import WordTokenizer

from cltk.core.data_types import Doc, Process, Word


@dataclass
class TokenizationProcess(Process):
    """To be inherited for each language's tokenization declarations.

    Example: ``TokenizationProcess`` -> ``LatinTokenizationProcess``

    >>> from cltk.tokenizers.processes import TokenizationProcess
    >>> from cltk.core.data_types import Process
    >>> issubclass(TokenizationProcess, Process)
    True
    >>> tok = TokenizationProcess(input_doc=Doc(raw="some input data"))
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        # TODO: Map these or better refactor tok code when moving over
        # print("???", self.language)
        if self.language == "lat":
            self.language = "latin"
        elif self.language == "grc":
            self.language = "greek"
        elif self.language == "akk":
            self.language = "akkadian"
        elif self.language == "arb":
            self.language = "arabic"
        elif self.language == "fro":
            self.language = "old_french"
        elif self.language == "frm":
            self.language = "middle_french"
        elif self.language == "ang":
            self.language = "old_english"
        elif self.language == "enm":
            self.language = "middle_english"
        elif self.language == "gmh":
            self.language = "middle_high_german"
        elif self.language == "san":
            self.language = "sanskrit"
        elif self.language == "non":
            self.language = "old_norse"
        elif self.language == "multilingual":
            self.language = "multilingual"
        else:
            self.language = "multilingual"
        return WordTokenizer(language=self.language)

    def run(self):
        tmp_doc = self.input_doc
        tmp_doc.words = list()
        tokenizer_obj = self.algorithm
        for index, token in enumerate(tokenizer_obj.tokenize(tmp_doc.raw)):
            word_obj = Word(string=token, index_token=index)
            tmp_doc.words.append(word_obj)
        self.output_doc = tmp_doc


@dataclass
class AkkadianTokenizationProcess(TokenizationProcess):
    """The default Akkadian tokenization algorithm.

    TODO: Change function or post-process to separate tokens from language labels

    >>> from cltk.tokenizers import AkkadianTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = AkkadianTokenizationProcess(input_doc=Doc(raw=get_example_text("akk")))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    ['u2-wa-a-ru', 'at-ta', 'e2-kal2-la-ka', '_e2_-ka', 'wu-e-er']
    """

    language = "akk"
    description = "Default tokenizer for the Akkadian language."


@dataclass
class ArabicTokenizationProcess(TokenizationProcess):
    """The default Arabic tokenization algorithm.

    >>> from cltk.tokenizers import ArabicTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = ArabicTokenizationProcess(input_doc=Doc(raw=get_example_text("arb")[:34]))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    ['كهيعص', '﴿١﴾', 'ذِكْرُ', 'رَحْمَتِ', 'رَبِّكَ']
    """

    language = "arb"
    description = "Default tokenizer for the Arabic language."


@dataclass
class GreekTokenizationProcess(TokenizationProcess):
    """The default Greek tokenization algorithm.

    >>> from cltk.tokenizers import GreekTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = GreekTokenizationProcess(input_doc=Doc(raw=get_example_text("grc")[:23]))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    ['ὅτι', 'μὲν', 'ὑμεῖς', ',', 'ὦ', 'ἄνδρες']
    """

    language = "grc"
    description = "Default tokenizer for the Greek language."


@dataclass
class LatinTokenizationProcess(TokenizationProcess):
    """The default Latin tokenization algorithm.

    >>> from cltk.tokenizers import LatinTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = LatinTokenizationProcess(input_doc=Doc(raw=get_example_text("lat")[:23]))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    ['Gallia', 'est', 'omnis', 'divisa']
    """

    language = "lat"
    description = "Default tokenizer for the Latin language."


@dataclass
class MHGTokenizationProcess(TokenizationProcess):
    """The default Middle High German tokenization algorithm.

    >>> from cltk.tokenizers import MHGTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = MHGTokenizationProcess(input_doc=Doc(raw=get_example_text("gmh")[:29]))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    ['Ik', 'gihorta', 'ðat', 'seggen', 'ðat', 'sih']
    """

    description = "The default Middle High German tokenizer"
    language = "gmh"


@dataclass
class MiddleEnglishTokenizationProcess(TokenizationProcess):
    """The default Middle English tokenization algorithm.

    >>> from cltk.tokenizers import MiddleEnglishTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = MiddleEnglishTokenizationProcess(input_doc=Doc(raw=get_example_text("enm")[:31]))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    ['Whilom', ',', 'as', 'olde', 'stories', 'tellen']
    """

    description = "Default Middle English tokenizer"
    language = "enm"


@dataclass
class MiddleFrenchTokenizationProcess(TokenizationProcess):
    """The default Middle French tokenization algorithm.

    >>> from cltk.tokenizers import MiddleFrenchTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = MiddleFrenchTokenizationProcess(input_doc=Doc(raw=get_example_text("frm")[:37]))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    ['Attilius', 'Regulus', ',', 'general', 'de', "l'armée"]
    """

    description = "Default tokenizer for the Middle French language."
    language = "frm"


@dataclass
class MultilingualTokenizationProcess(TokenizationProcess):
    """The default tokenization algorithm.

    >>> from cltk.tokenizers.processes import MultilingualTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = MultilingualTokenizationProcess(input_doc=Doc(raw=get_example_text("non")[:29]))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    language = "multilingual"
    description = "Default tokenizer for languages lacking a dedicated tokenizer. This is a whitespace tokenizer inheriting from the NLTK."


@dataclass
class OldFrenchTokenizationProcess(TokenizationProcess):
    """The default Old French tokenization algorithm.

    >>> from cltk.tokenizers import OldFrenchTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tok = OldFrenchTokenizationProcess(input_doc=Doc(raw=get_example_text("fro")[:37]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['Une', 'aventure', 'vos', 'voil', 'dire', 'Molt', 'bien']
    """

    description = "Default tokenizer for the Old French language."
    language = "fro"


@dataclass
class OldNorseTokenizationProcess(TokenizationProcess):
    """The default OldNorse tokenization algorithm.

    >>> from cltk.tokenizers import OldNorseTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tok = OldNorseTokenizationProcess(input_doc=Doc(raw=get_example_text("non")[:29]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    description = "Default Old Norse tokenizer"
    language = "non"


@dataclass
class SanskritTokenizationProcess(TokenizationProcess):
    """The default Middle English tokenization algorithm.

    >>> from cltk.tokenizers import SanskritTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tok = SanskritTokenizationProcess(input_doc=Doc(raw=get_example_text("san")[:31]))
    >>> tok.run()
    >>> tok.output_doc.tokens
    ['ईशा', 'वास्यम्', 'इदं', 'सर्वं', 'यत्', 'किञ्च']
    """

    description = "The default Middle English tokenizer"
    language = "san"
