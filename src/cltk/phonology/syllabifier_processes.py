"""

"""


from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.phonology.ang.phonology import OldEnglishSyllabifier
from cltk.phonology.enm.phonology import MiddleEnglishSyllabifier
from cltk.phonology.gmh.phonology import MiddleHighGermanSyllabifier

# from cltk.phonology.akk import AkkadianSyllabifier
from cltk.phonology.lat.phonology import LatinSyllabifier
from cltk.phonology.non.phonology import OldNorseSyllabifier


@dataclass
class SyllabificationProcess(Process):
    """

    """

    def run(self, input_doc: Doc) -> Doc:
        syllabifier = self.algorithm

        output_doc = deepcopy(input_doc)
        for word in output_doc.words:
            word.syllables = syllabifier(word.string.lower())

        return output_doc


# class AkkadianSyllabificationProcess(Process):
#     """
#     >>> from cltk.core.data_types import Process, Pipeline
#     >>> from cltk.tokenizers.processes import AkkadianTokenizationProcess
#     >>> from cltk.filtering.processes import DefaultPunctuationRemovalProcess
#     >>> from cltk.languages.utils import get_lang
#     >>> from cltk.languages.example_texts import get_example_text
#     >>> from cltk.nlp import NLP
#     >>> pipe = Pipeline(description="A custom Akkadian pipeline", \
#     processes=[AkkadianTokenizationProcess, DefaultPunctuationRemovalProcess, AkkadianSyllabificationProcess], \
#     language=get_lang("akk"))
#     >>> nlp = NLP(language='akk', custom_pipeline = pipe)
#     >>> text = get_example_text("akk")
#     >>> print(text)
#
#     >>> [word.syllables for word in nlp(text)[:5]]
#
#     """
#
#     description = "The default Akkadian syllabification process"
#
#     def run(self, input_doc: Doc) -> Doc:
#         syllabifier = self.algorithm
#
#         output_doc = deepcopy(input_doc)
#         for word in output_doc.words:
#             word.syllables = syllabifier(word.string)
#
#         return output_doc
#
#     @cachedproperty
#     def algorithm(self):
#         return AkkadianSyllabifier()


# class GothicSyllabificationProcess(SyllabificationProcess):
#     """
#     >>> from cltk.core.data_types import Process, Pipeline
#     >>> from cltk.tokenizers.processes import GothicTokenizationProcess
#     >>> from cltk.filtering.processes import DefaultPunctuationRemovalProcess
#     >>> from cltk.languages.utils import get_lang
#     >>> from cltk.languages.example_texts import get_example_text
#     >>> from cltk.nlp import NLP
#     >>> pipe = Pipeline(description="A custom Gothic pipeline", \
#     processes=[GothicTokenizationProcess, GothicSyllabificationProcess], \
#     language=get_lang("akk"))
#     >>> nlp = NLP(language='akk', custom_pipeline = pipe)
#     >>> nlp(get_example_text("akk")).syllables
#
#     """
#
#     description = "The default Gothic syllabification process"
#
#     @cachedproperty
#     def algorithm(self):
#         return GothicSyllabifier()


class LatinSyllabificationProcess(SyllabificationProcess):
    """Syllabification ``Process`` for Latin.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import LatinTokenizationProcess
    >>> from cltk.filtering.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk import NLP
    >>> a_pipeline = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess, DefaultPunctuationRemovalProcess, LatinSyllabificationProcess], language=get_lang("lat"))
    >>> nlp = NLP(language='lat', custom_pipeline = pipe)
    >>> text = get_example_text("lat")
    >>> [word.syllables for word in cltk_doc.words[:5]]
    [['gal', 'li', 'a'], ['est'], ['om', 'nis'], ['di', 'vi', 'sa'], ['in']]
    """

    description = "The default Latin Syllabification process"

    @cachedproperty
    def algorithm(self):
        return LatinSyllabifier()


class MiddleEnglishSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleEnglishTokenizationProcess
    >>> from cltk.filtering.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Middle English pipeline", \
    processes=[MiddleEnglishTokenizationProcess, DefaultPunctuationRemovalProcess, MiddleEnglishSyllabificationProcess], \
    language=get_lang("enm"))
    >>> nlp = NLP(language='enm', custom_pipeline=pipe)
    >>> text = get_example_text("enm").replace('\\n', ' ')
    >>> [word.syllables for word in nlp(text)[:5]]
    [['whi', 'lom'], ['as'], ['ol', 'de'], ['sto', 'ries'], ['tellen']]
    """

    description = "The default Middle English Syllabification process"

    @cachedproperty
    def algorithm(self):
        return MiddleEnglishSyllabifier()


class MiddleHighGermanSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleHighGermanTokenizationProcess
    >>> from cltk.filtering.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Middle High German pipeline", \
    processes=[MiddleHighGermanTokenizationProcess, DefaultPunctuationRemovalProcess, \
    MiddleHighGermanSyllabificationProcess], language=get_lang("gmh"))
    >>> nlp = NLP(language='gmh', custom_pipeline=pipe)
    >>> text = get_example_text("gmh")
    >>> [word.syllables for word in nlp(text)[:5]]
    [['uns'], ['ist'], ['in'], ['al', 'ten'], ['mæ', 'ren']]
    """

    description = "The default Middle High German syllabification process"

    @cachedproperty
    def algorithm(self):
        return MiddleHighGermanSyllabifier()


class OldEnglishSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleEnglishTokenizationProcess
    >>> from cltk.filtering.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old English pipeline", \
    processes=[MiddleEnglishTokenizationProcess, DefaultPunctuationRemovalProcess, OldEnglishSyllabificationProcess], \
    language=get_lang("ang"))
    >>> nlp = NLP(language='ang', custom_pipeline=pipe)
    >>> text = get_example_text("ang")

    >>> [word.syllables for word in nlp(text)[:5]]
    [['hwæt'], ['we'], ['gar', 'den', 'a'], ['in'], ['gear', 'da', 'gum']]

    """

    description = "The default Old English syllabification process"

    @cachedproperty
    def algorithm(self):
        return OldEnglishSyllabifier()


class OldNorseSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import OldNorseTokenizationProcess
    >>> from cltk.filtering.processes import OldNorsePunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
    processes=[OldNorseTokenizationProcess, OldNorsePunctuationRemovalProcess, OldNorseSyllabificationProcess], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline=pipe)
    >>> text = get_example_text("non")
    >>> [word.syllables for word in nlp(text)[:5]]
    [['gyl', 'fi'], ['ko', 'nungr'], ['réð'], ['þar'], ['lön', 'dum']]
    """

    description = "The default Old Norse syllabification process"

    @cachedproperty
    def algorithm(self):
        return OldNorseSyllabifier()
