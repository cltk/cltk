"""

"""


from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process

from cltk.phonology.akk import AkkadianSyllabifier
from cltk.phonology.lat import LatinSyllabifier
from cltk.phonology.middle_english import MiddleEnglishSyllabifier
from cltk.phonology.middle_high_german import MiddleHighGermanSyllabifier
from cltk.phonology.non import OldNorseSyllabifier
from cltk.phonology.old_english import OldEnglishSyllabifier


@dataclass
class SyllabificationProcess(Process):
    """

    """
    def run(self, input_doc: Doc) -> Doc:
        syllabifier = self.algorithm

        output_doc = deepcopy(input_doc)
        for word in output_doc.words:
            word.phonological_transcription = syllabifier(input_doc.raw)

        return output_doc


class AkkadianSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import AkkadianTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Akkadian pipeline", \
    processes=[AkkadianTokenizationProcess, AkkadianSyllabificationProcess], \
    language=get_lang("akk"))
    >>> nlp = NLP(language='akk', custom_pipeline = pipe)
    >>> nlp(get_example_text("akk")).phonological_transcription

    """

    description = "The default Old Norse poetry process"

    @cachedproperty
    def algorithm(self):
        return AkkadianSyllabifier()


class GothicSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import GothicTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Akkadian pipeline", \
    processes=[GothicTokenizationProcess, GothicSyllabificationProcess], \
    language=get_lang("akk"))
    >>> nlp = NLP(language='akk', custom_pipeline = pipe)
    >>> nlp(get_example_text("akk")).syllables

    """

    description = "The default Old Norse poetry process"

    @cachedproperty
    def algorithm(self):
        return GothicSyllabifier()


class LatinSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import AkkadianTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Akkadian pipeline", \
    processes=[AkkadianTokenizationProcess, LatinSyllabificationProcess], \
    language=get_lang("akk"))
    >>> nlp = NLP(language='lat', custom_pipeline = pipe)
    >>> nlp(get_example_text("lat")).phonological_transcription

    """

    description = "The default Latin Syllabification process"

    @cachedproperty
    def algorithm(self):
        return LatinSyllabifier()


class MiddleEnglishSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleEnglishTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Middle English pipeline", \
    processes=[MiddleEnglishTokenizationProcess, AkkadianSyllbificationProcess], \
    language=get_lang("akk"))
    >>> nlp = NLP(language='akk', custom_pipeline = pipe)
    >>> nlp(get_example_text("akk")).phonological_transcription

    """

    description = "The default Middle English Syllabification process"

    @cachedproperty
    def algorithm(self):
        return MiddleEnglishSyllabifier()


class MiddleHighGermanSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleHighGermanTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Akkadian pipeline", \
    processes=[MiddleHighGermanTokenizationProcess, MiddleHighGermanSyllabificationProcess], \
    language=get_lang("mhg"))
    >>> nlp = NLP(language='mhg', custom_pipeline = pipe)
    >>> nlp(get_example_text("mhg")).phonological_transcription

    """

    description = "The default Middle High German syllabification process"

    @cachedproperty
    def algorithm(self):
        return MiddleHighGermanSyllabifier()


class OldEnglishSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import OldEnglishTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old English pipeline", \
    processes=[OldEnglishTokenizationProcess, OldEnglishSyllabificationProcess], \
    language=get_lang("akk"))
    >>> nlp = NLP(language='akk', custom_pipeline = pipe)
    >>> nlp(get_example_text("akk")).phonological_transcription

    """

    description = "The default Old English syllabification process"

    @cachedproperty
    def algorithm(self):
        return OldEnglishSyllabifier()


class OldNorseSyllabificationProcess(SyllabificationProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import OldNorseTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Akkadian pipeline", \
    processes=[OldNorseTokenizationProcess, OldNorseSyllabificationProcess], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline = pipe)
    >>> nlp(get_example_text("non")).phonological_transcription

    """

    description = "The default Old Norse syllabification process"

    @cachedproperty
    def algorithm(self):
        return OldNorseSyllabifier()
