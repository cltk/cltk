"""
Processes for poetry

"""

from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process

from cltk.prosody.grc import GreekScanner
from cltk.prosody.lat.scanner import LatinScanner
from cltk.prosody.gmh import MiddleHighGermanScanner
from cltk.prosody.non import OldNorseScanner


@dataclass
class PoetryProcess(Process):
    """

    """
    def run(self, input_doc: Doc) -> Doc:
        scanner = self.algorithm

        output_doc = deepcopy(input_doc)
        output_doc.scanned_text = scanner(input_doc.raw)

        return output_doc


class GreekPoetryProcess(PoetryProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import GreekTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
    processes=[GreekTokenizationProcess, GreekPoetryProcess], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline = pipe)
    >>> nlp(get_example_text("non")).scanned_text

    """

    description = "The default Greek poetry process"

    @cachedproperty
    def algorithm(self):
        return GreekScanner()


class LatinPoetryProcess(PoetryProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import LatinTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Latin pipeline", \
    processes=[LatinTokenizationProcess, LatinPoetryProcess], \
    language=get_lang("lat"))
    >>> nlp = NLP(language='lat', custom_pipeline = pipe)
    >>> nlp(get_example_text("lat")).scanned_text

    """

    description = "The default Latin poetry process"

    @cachedproperty
    def algorithm(self):
        return LatinScanner()


class MiddleHighGermanPoetryProcess(PoetryProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleHighGermanTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Middle High German pipeline", \
    processes=[MiddleHighGermanTokenizationProcess, MiddleHighGermanPoetryProcess], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline = pipe)
    >>> nlp(get_example_text("non")).scanned_text

    """

    description = "The default Middle High German poetry process"

    @cachedproperty
    def algorithm(self):
        return MiddleHighGermanScanner()


class OldNorsePoetryProcess(PoetryProcess):
    """
    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import OldNorseTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
    processes=[OldNorseTokenizationProcess, OldNorsePoetryProcess], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline = pipe)
    >>> nlp(get_example_text("non")).scanned_text

    """

    description = "The default Old Norse poetry process"

    @cachedproperty
    def algorithm(self):
        return OldNorseScanner()
