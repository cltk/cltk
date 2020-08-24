"""
Processes for poetry

"""

from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.phonology.non.orthophonology import OldNorsePhonologicalTranscriber


@dataclass
class PhonologicalTranscriptionProcess(Process):
    """

    """
    def run(self, input_doc: Doc) -> Doc:
        transcriber = self.algorithm

        output_doc = deepcopy(input_doc)
        for word in output_doc.words:
            word.phonological_transcription = transcriber(input_doc.raw)

        return output_doc


class OldNorsePhonologicalTranscriber(PhonologicalTranscriptionProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import OldNorseTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
    processes=[OldNorseTokenizationProcess, OldNorsePhonologicalTranscriber], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline = pipe)
    >>> nlp(get_example_text("non")).scanned_text

    """

    description = "The default Old Norse poetry process"

    @cachedproperty
    def algorithm(self):
        return OldNorsePhonologicalTranscriber()
