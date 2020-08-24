"""
Processes for poetry

"""

from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.prosody.non import OldNorseScanner


@dataclass
class PoetryProcess(Process):
    """

    """
    def run(self, input_doc: Doc) -> Doc:
        scanner = self.algorithm

        output_doc = deepcopy(input_doc)
        output_doc.scanned_text = scanner(input_doc.string)

        return output_doc


class OldNorsePoetryProcess(PoetryProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import MultilingualTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
    processes=[MultilingualTokenizationProcess, OldNorsePoetryProcess], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline = pipe)
    >>> nlp(get_example_text("non")).scanned_paragraphs

    """

    description = "The default Old Norse poetry process"

    @cachedproperty
    def algorithm(self):
        return OldNorseScanner()
