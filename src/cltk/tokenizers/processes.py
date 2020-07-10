"""Module for tokenizers.

TODO: Think about adding check somewhere if a contrib (not user) chooses an unavailable item
"""

from dataclasses import dataclass
from typing import Callable

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process, Word


from cltk.tokenizers.word import RegexWordTokenizer
from cltk.tokenizers.akk import AkkadianWordTokenizer
from cltk.tokenizers.arb import ArabicWordTokenizer
from cltk.tokenizers.lat.lat import LatinWordTokenizer
from cltk.tokenizers.enm import MiddleEnglishTokenizerPatterns
from cltk.tokenizers.gmh import MiddleHighGermanTokenizerPatterns
from cltk.tokenizers.fro import OldFrenchTokenizerPatterns
from cltk.tokenizers.non import OldNorseTokenizerPatterns

from nltk.tokenize.treebank import TreebankWordTokenizer


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
        """
        The backoff tokenizer, from NLTK.
        """
        return TreebankWordTokenizer()
    
    def run(self):
        tmp_doc = self.input_doc
        tmp_doc.words = list()
        tokenizer_obj = self.algorithm
       
        for index, token in enumerate(tokenizer_obj.tokenize(tmp_doc.raw)):
            word_obj = Word(string=token, index_token=index)
            tmp_doc.words.append(word_obj)
        
        self.output_doc = tmp_doc


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
class AkkadianTokenizationProcess(TokenizationProcess):
    """The default Akkadian tokenization algorithm.

    TODO: Change function or post-process to separate tokens from language labels

    >>> from cltk.tokenizers import AkkadianTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = AkkadianTokenizationProcess(input_doc=Doc(raw=get_example_text("akk")))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    [('u2-wa-a-ru', 'akkadian'), ('at-ta', 'akkadian'), ('e2-kal2-la-ka', 'akkadian'), ('_e2_-ka', 'sumerian'), ('wu-e-er', 'akkadian')]
    """

    language = "akk"
    description = "Default tokenizer for the Akkadian language."

    @cachedproperty
    def algorithm(self):
        return AkkadianWordTokenizer()


@dataclass
class ArabicTokenizationProcess(TokenizationProcess):
    """The default Arabic tokenization algorithm.

    >>> from cltk.tokenizers import ArabicTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = ArabicTokenizationProcess(input_doc=Doc(raw=get_example_text("arb")[:34]))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    ['كهيعص', '﴿', '١', '﴾', 'ذِكْرُ', 'رَحْمَتِ', 'رَبِّكَ']
    """

    language = "arb"
    description = "Default tokenizer for the Arabic language."

    @cachedproperty
    def algorithm(self):
        return ArabicWordTokenizer()


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

    @cachedproperty
    def algorithm(self):
        return TreebankWordTokenizer()


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

    @cachedproperty
    def algorithm(self):
        return LatinWordTokenizer()


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

    description = "Default Middle High German tokenizer"
    language = "gmh"

    @cachedproperty
    def algorithm(self):
        return RegexWordTokenizer(MiddleHighGermanTokenizerPatterns)


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

    @cachedproperty
    def algorithm(self):
        return RegexWordTokenizer(MiddleEnglishTokenizerPatterns)

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

    @cachedproperty
    def algorithm(self):
        return RegexWordTokenizer(OldFrenchTokenizerPatterns)

@dataclass
class MiddleFrenchTokenizationProcess(TokenizationProcess):
    """The default Middle French tokenization algorithm.

    >>> from cltk.tokenizers import MiddleFrenchTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = MiddleFrenchTokenizationProcess(input_doc=Doc(raw=get_example_text("frm")[:37]))
    >>> tokenizer_process.run()
    >>> tokenizer_process.output_doc.tokens
    ['Attilius', 'Regulus', ',', 'general', 'de', "l'", 'armée']
    """

    description = "Default tokenizer for the Middle French language."
    language = "frm"

    @cachedproperty
    def algorithm(self):
        return RegexWordTokenizer(OldFrenchTokenizerPatterns)


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

    @cachedproperty
    def algorithm(self):
        return RegexWordTokenizer(OldNorseTokenizerPatterns)

