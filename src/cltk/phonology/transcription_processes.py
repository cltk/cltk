"""This module provides phonological/phonetic transcribers for several languages.
**PhonologicalTranscriptionProcess** is the parent-class for all other custom transcription processes.
"""


from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.phonology.ang.phonology import OldEnglishTranscription
from cltk.phonology.gmh.phonology import MiddleHighGermanTranscription

# from cltk.phonology.akk import AkkadianPhonologicalTranscriber
# from cltk.phonology.arb import ArabicPhonologicalTranscriber
from cltk.phonology.got.phonology import GothicTranscription
from cltk.phonology.grc.phonology import GreekTranscription
from cltk.phonology.lat.phonology import LatinTranscription
from cltk.phonology.non.old_swedish.phonology import OldSwedishTranscription
from cltk.phonology.non.orthophonology import OldNorsePhonologicalTranscriber

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


@dataclass
class PhonologicalTranscriptionProcess(Process):
    """General phonological transcription `Process`."""

    def run(self, input_doc: Doc) -> Doc:
        transcriber = self.algorithm

        output_doc = deepcopy(input_doc)
        for word in output_doc.words:
            word.phonetic_transcription = transcriber(word.string.lower())
        return output_doc


# class AkkadianPhonologicalTranscriberProcess(PhonologicalTranscriptionProcess):
#     """
#     >>> from cltk.core.data_types import Process, Pipeline
#     >>> from cltk.tokenizers.processes import AkkadianTokenizationProcess
#     >>> from cltk.languages.utils import get_lang
#     >>> from cltk.languages.example_texts import get_example_text
#     >>> from cltk.nlp import NLP
#     >>> pipe = Pipeline(description="A custom Akkadian pipeline", \
#     processes=[AkkadianTokenizationProcess, AkkadianPhonologicalTranscriberProcess], \
#     language=get_lang("akk"))
#     >>> nlp = NLP(language='akk', custom_pipeline=pipe)
#     >>> nlp(get_example_text("akk")).phonetic_transcription
#
#     """
#
#     description = "The default Akkadian transcription process"
#
#     @cachedproperty
#     def algorithm(self):
#         return AkkadianPhonologicalTranscriber()


# class ArabicPhonologicalTranscriberProcess(PhonologicalTranscriptionProcess):
#     """
#     >>> from cltk.core.data_types import Process, Pipeline
#     >>> from cltk.tokenizers.processes import ArabicTokenizationProcess
#     >>> from cltk.languages.utils import get_lang
#     >>> from cltk.languages.example_texts import get_example_text
#     >>> from cltk.nlp import NLP
#     >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
#     processes=[ArabicTokenizationProcess, ArabicPhonologicalTranscriberProcess], \
#     language=get_lang("arb"))
#     >>> nlp = NLP(language='arb', custom_pipeline=pipe)
#     >>> text = get_example_text("arb")
#     >>> [word.phonetic_transcription for word in nlp(text)]
#
#     """
#
#     description = "The default Arabic transcription process"
#
#     @cachedproperty
#     def algorithm(self):
#         return ArabicPhonologicalTranscriber()


class GothicPhonologicalTranscriberProcess(PhonologicalTranscriptionProcess):
    """Phonological transcription `Process` for Gothic.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import OldNorseTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Gothic pipeline", \
    processes=[OldNorseTokenizationProcess, DefaultPunctuationRemovalProcess, \
    GothicPhonologicalTranscriberProcess], language=get_lang("got"))
    >>> nlp = NLP(language='got', custom_pipeline=pipe, suppress_banner=True)
    >>> text = get_example_text("got")
    >>> cltk_doc = nlp(text)
    >>> [word.phonetic_transcription for word in cltk_doc.words[:5]]
    ['swa', 'liuhtjɛ', 'liuhaθ', 'jzwar', 'jn']
    """

    description = "The default Gothic transcription process"

    @cachedproperty
    def algorithm(self):
        return GothicTranscription()


class GreekPhonologicalTranscriberProcess(PhonologicalTranscriptionProcess):
    """Phonological transcription `Process` for Ancient Greek.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import GreekTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Greek pipeline", \
    processes=[GreekTokenizationProcess, DefaultPunctuationRemovalProcess,\
    GreekPhonologicalTranscriberProcess], language=get_lang("grc"))
    >>> nlp = NLP(language='grc', custom_pipeline=pipe, suppress_banner=True)
    >>> text = get_example_text("grc")
    >>> cltk_doc = nlp(text)
    >>> [word.phonetic_transcription for word in cltk_doc.words[:5]]
    ['hó.ti', 'men', 'hy.mệːs', 'ɔ̂ː', 'ɑ́n.dres']
    """

    description = "The default Greek transcription process"

    @cachedproperty
    def algorithm(self):
        return GreekTranscription()


class LatinPhonologicalTranscriberProcess(PhonologicalTranscriptionProcess):
    """Phonological transcription `Process` for Latin.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import LatinTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk import NLP
    >>> a_pipeline = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess, DefaultPunctuationRemovalProcess, LatinPhonologicalTranscriberProcess], language=get_lang("lat"))
    >>> nlp = NLP(language="lat", custom_pipeline=a_pipeline, suppress_banner=True)
    >>> text = get_example_text("lat")
    >>> cltk_doc = nlp.analyze(text)
    >>> [word.phonetic_transcription for word in cltk_doc.words][:5]
    ['[gaɫlɪ̣ja]', '[ɛst̪]', '[ɔmn̪ɪs]', '[d̪ɪwɪsa]', '[ɪn̪]']
    """

    description = "The default Latin transcription process"

    @cachedproperty
    def algorithm(self):
        return LatinTranscription()


class MiddleHighGermanPhonologicalTranscriberProcess(PhonologicalTranscriptionProcess):
    """Phonological transcription `Process` for Middle High German.
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleHighGermanTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Middle High German pipeline", \
    processes=[MiddleHighGermanTokenizationProcess, DefaultPunctuationRemovalProcess, \
    MiddleHighGermanPhonologicalTranscriberProcess], language=get_lang("gmh"))
    >>> nlp = NLP(language='gmh', custom_pipeline=pipe, suppress_banner=True)
    >>> text = get_example_text("gmh")
    >>> cltk_doc = nlp(text)
    >>> [word.phonetic_transcription for word in cltk_doc.words[:5]]
    ['ʊns', 'ɪst', 'ɪn', 'alten', 'mɛren']
    """

    description = "The default Middle High German transcription process"

    @cachedproperty
    def algorithm(self):
        return MiddleHighGermanTranscription()


class OldEnglishPhonologicalTranscriberProcess(PhonologicalTranscriptionProcess):
    """Phonological transcription `Process` for Old English.
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleEnglishTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old English pipeline", \
    processes=[MiddleEnglishTokenizationProcess, DefaultPunctuationRemovalProcess, \
    OldEnglishPhonologicalTranscriberProcess], language=get_lang("ang"))
    >>> nlp = NLP(language='ang', custom_pipeline=pipe, suppress_banner=True)
    >>> text = get_example_text("ang")
    >>> cltk_doc = nlp(text)
    >>> [word.phonetic_transcription for word in cltk_doc.words[:5]]
    ['ʍæt', 'we', 'gɑrˠdenɑ', 'in', 'gæːɑrˠdɑgum']
    """

    description = "The default Old English transcription process"

    @cachedproperty
    def algorithm(self):
        return OldEnglishTranscription()


class OldNorsePhonologicalTranscriberProcess(PhonologicalTranscriptionProcess):
    """Phonological transcription `Process` for Old Norse.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import OldNorseTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
    processes=[OldNorseTokenizationProcess, DefaultPunctuationRemovalProcess, \
    OldNorsePhonologicalTranscriberProcess], language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline=pipe, suppress_banner=True)
    >>> text = get_example_text("non")
    >>> cltk_doc = nlp(text)
    >>> [word.phonetic_transcription for word in cltk_doc.words[:5]]
    ['gylvi', 'kɔnunɣr', 'reːð', 'θar', 'lœndum']

    """

    description = "The default Old Norse poetry process"

    @cachedproperty
    def algorithm(self):
        return OldNorsePhonologicalTranscriber()


class OldSwedishPhonologicalTranscriberProcess(PhonologicalTranscriptionProcess):
    """Phonological transcription `Process` for Old Swedish.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import OldNorseTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Swedish pipeline", \
    processes=[OldNorseTokenizationProcess, DefaultPunctuationRemovalProcess, \
    OldSwedishPhonologicalTranscriberProcess], language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline=pipe, suppress_banner=True)
    >>> text = "Far man kunu oc dör han för en hun far barn. oc sigher hun oc hænnæ frændær."
    >>> cltk_doc = nlp(text)
    >>> [word.phonetic_transcription for word in cltk_doc.words[:5]]
    ['far', 'man', 'kunu', 'ok', 'dør']
    """

    description = "The default Old Swedish transcription process"

    @cachedproperty
    def algorithm(self):
        return OldSwedishTranscription()
