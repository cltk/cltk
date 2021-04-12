"""Module for tokenizers.

TODO: Think about adding check somewhere if a contrib (not user) chooses an unavailable item
"""

from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty
from nltk.tokenize.treebank import TreebankWordTokenizer

from cltk.core.data_types import Doc, Process, Word
from cltk.tokenizers.akk import AkkadianWordTokenizer
from cltk.tokenizers.arb import ArabicWordTokenizer
from cltk.tokenizers.enm import MiddleEnglishWordTokenizer
from cltk.tokenizers.fro import OldFrenchWordTokenizer
from cltk.tokenizers.gmh import MiddleHighGermanWordTokenizer
from cltk.tokenizers.lat.lat import LatinWordTokenizer
from cltk.tokenizers.non import OldNorseWordTokenizer
from cltk.tokenizers.word import CLTKTreebankWordTokenizer


@dataclass
class TokenizationProcess(Process):
    """To be inherited for each language's tokenization declarations.

    Example: ``TokenizationProcess`` -> ``LatinTokenizationProcess``

    >>> from cltk.tokenizers.processes import TokenizationProcess
    >>> from cltk.core.data_types import Process
    >>> issubclass(TokenizationProcess, Process)
    True
    >>> tok = TokenizationProcess()
    """

    @cachedproperty
    def algorithm(self):
        """
        The backoff tokenizer, from NLTK.
        """
        return CLTKTreebankWordTokenizer()

    def run(self, input_doc: Doc) -> Doc:
        output_doc = deepcopy(input_doc)
        output_doc.words = []
        tokenizer_obj = self.algorithm

        tokens = tokenizer_obj.tokenize(output_doc.raw)
        indices = tokenizer_obj.compute_indices(output_doc.raw, tokens)
        for index, token in enumerate(tokens):
            word_obj = Word(
                string=token,
                index_token=index,
                index_char_start=indices[index],
                index_char_stop=indices[index] + len(token),
            )
            output_doc.words.append(word_obj)
        return output_doc


@dataclass
class MultilingualTokenizationProcess(TokenizationProcess):
    """The default tokenization algorithm.

    >>> from cltk.tokenizers.processes import MultilingualTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = MultilingualTokenizationProcess()
    >>> output_doc = tokenizer_process.run(Doc(raw=get_example_text("non")[:29]))
    >>> output_doc.tokens
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']

    >>> [word.index_char_start for word in output_doc.words]
    [0, 6, 14, 18, 22]
    >>> [word.index_char_stop for word in output_doc.words]
    [5, 13, 17, 21, 28]
    """

    description = "Default tokenizer for languages lacking a dedicated tokenizer. This is a whitespace tokenizer inheriting from the NLTK."


@dataclass
class AkkadianTokenizationProcess(TokenizationProcess):
    """The default Akkadian tokenization algorithm.

    TODO: Change function or post-process to separate tokens from language labels

    >>> from cltk.tokenizers import AkkadianTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = AkkadianTokenizationProcess()
    >>> output_doc = tokenizer_process.run(input_doc=Doc(raw=get_example_text("akk")))
    >>> output_doc.tokens
    [('u2-wa-a-ru', 'akkadian'), ('at-ta', 'akkadian'), ('e2-kal2-la-ka', 'akkadian'), ('_e2_-ka', 'sumerian'), ('wu-e-er', 'akkadian')]
    """

    description = "Default tokenizer for the Akkadian language."

    @cachedproperty
    def algorithm(self):
        return AkkadianWordTokenizer()


@dataclass
class ArabicTokenizationProcess(TokenizationProcess):
    """The default Arabic tokenization algorithm.

    >>> from cltk.tokenizers import ArabicTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = ArabicTokenizationProcess()
    >>> output_doc = tokenizer_process.run(input_doc=Doc(raw=get_example_text("arb")[:34]))
    >>> output_doc.tokens
    ['كهيعص', '﴿', '١', '﴾', 'ذِكْرُ', 'رَحْمَتِ', 'رَبِّكَ']
    """

    description = "Default tokenizer for the Arabic language."

    @cachedproperty
    def algorithm(self):
        return ArabicWordTokenizer()


@dataclass
class GreekTokenizationProcess(TokenizationProcess):
    """The default Greek tokenization algorithm.

    >>> from cltk.tokenizers import GreekTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = GreekTokenizationProcess()
    >>> output_doc = tokenizer_process.run(input_doc=Doc(raw=get_example_text("grc")[:23]))
    >>> output_doc.tokens
    ['ὅτι', 'μὲν', 'ὑμεῖς', ',', 'ὦ', 'ἄνδρες']
    """

    description = "Default tokenizer for the Greek language."

    @cachedproperty
    def algorithm(self):
        return CLTKTreebankWordTokenizer()


@dataclass
class LatinTokenizationProcess(TokenizationProcess):
    """The default Latin tokenization algorithm.

    >>> from cltk.tokenizers import LatinTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = LatinTokenizationProcess()
    >>> output_doc = tokenizer_process.run(input_doc=Doc(raw=get_example_text("lat")[:23]))
    >>> output_doc.tokens
    ['Gallia', 'est', 'omnis', 'divisa']
    """

    description = "Default tokenizer for the Latin language."

    @cachedproperty
    def algorithm(self):
        return LatinWordTokenizer()


@dataclass
class MiddleHighGermanTokenizationProcess(TokenizationProcess):
    """The default Middle High German tokenization algorithm.

    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = MiddleHighGermanTokenizationProcess()
    >>> output_doc = tokenizer_process.run(input_doc=Doc(raw=get_example_text("gmh")[:29]))
    >>> output_doc.tokens
    ['Uns', 'ist', 'in', 'alten', 'mæren', 'wunder']
    """

    description = "Default Middle High German tokenizer"

    @cachedproperty
    def algorithm(self):
        return MiddleHighGermanWordTokenizer()


@dataclass
class MiddleEnglishTokenizationProcess(TokenizationProcess):
    """The default Middle English tokenization algorithm.

    >>> from cltk.tokenizers import MiddleEnglishTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = MiddleEnglishTokenizationProcess()
    >>> output_doc = tokenizer_process.run(input_doc=Doc(raw=get_example_text("enm")[:31]))
    >>> output_doc.tokens
    ['Whilom', ',', 'as', 'olde', 'stories', 'tellen']
    """

    description = "Default Middle English tokenizer"

    @cachedproperty
    def algorithm(self):
        return MiddleEnglishWordTokenizer()


@dataclass
class OldFrenchTokenizationProcess(TokenizationProcess):
    """The default Old French tokenization algorithm.

    >>> from cltk.tokenizers import OldFrenchTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tok = OldFrenchTokenizationProcess()
    >>> output_doc = tok.run(input_doc=Doc(raw=get_example_text("fro")[:37]))
    >>> output_doc.tokens
    ['Une', 'aventure', 'vos', 'voil', 'dire', 'Molt', 'bien']
    """

    description = "Default tokenizer for the Old French language."

    @cachedproperty
    def algorithm(self):
        return OldFrenchWordTokenizer()


@dataclass
class MiddleFrenchTokenizationProcess(TokenizationProcess):
    """The default Middle French tokenization algorithm.

    >>> from cltk.tokenizers import MiddleFrenchTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tokenizer_process = MiddleFrenchTokenizationProcess()
    >>> output_doc = tokenizer_process.run(input_doc=Doc(raw=get_example_text("frm")[:37]))
    >>> output_doc.tokens
    ['Attilius', 'Regulus', ',', 'general', 'de', "l'", 'armée']
    """

    description = "Default tokenizer for the Middle French language."

    @cachedproperty
    def algorithm(self):
        return OldFrenchWordTokenizer()


@dataclass
class OldNorseTokenizationProcess(TokenizationProcess):
    """The default OldNorse tokenization algorithm.

    >>> from cltk.tokenizers import OldNorseTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> tok = OldNorseTokenizationProcess()
    >>> output_doc = tok.run(input_doc=Doc(raw=get_example_text("non")[:29]))
    >>> output_doc.tokens
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    description = "Default Old Norse tokenizer"

    @cachedproperty
    def algorithm(self):
        return OldNorseWordTokenizer()
