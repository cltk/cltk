"""Processes for stemming.
"""

from copy import deepcopy
from dataclasses import dataclass

import cltk.stem.akk
import cltk.stem.enm
import cltk.stem.fro
import cltk.stem.gmh
import cltk.stem.lat
from cltk.core.data_types import Doc, Process, Word


@dataclass
class StemmingProcess(Process):
    """To be inherited for each language's stemming declarations.

    Example: ``StemmingProcess`` -> ``LatinStemmingProcess``

    >>> from cltk.stem.processes import StemmingProcess
    >>> from cltk.core.data_types import Process
    >>> issubclass(StemmingProcess, Process)
    True
    """

    def run(self, input_doc: Doc) -> Doc:
        stem = self.algorithm

        output_doc = deepcopy(input_doc)
        for word in output_doc.words:
            word.stem = stem(word.string)

        return output_doc


class LatinStemmingProcess(StemmingProcess):
    """The default Latin stemming algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import LatinTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess, LatinStemmingProcess], language=get_lang("lat"))
    >>> nlp = NLP(language='lat', custom_pipeline = pipe, suppress_banner=True)
    >>> nlp(get_example_text("lat")[:23]).stems
    ['Gall', 'est', 'omn', 'divis']

    """

    description = "Default stemmer for the Latin language."

    @staticmethod
    def algorithm(word: str) -> str:
        return cltk.stem.lat.stem(word)


class MiddleEnglishStemmingProcess(StemmingProcess):
    """The default Middle English stemming algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import MiddleEnglishTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Middle English pipeline", \
    processes=[MiddleEnglishTokenizationProcess, MiddleEnglishStemmingProcess], \
    language=get_lang("enm"))
    >>> nlp = NLP(language='enm', custom_pipeline = pipe, suppress_banner=True)
    >>> nlp(get_example_text("enm")[:29]).stems
    ['Whil', ',', 'as', 'olde', 'stor', 'lle']
    """

    description = "Default stemmer for the Middle English language."

    @staticmethod
    def algorithm(word: str) -> str:
        return cltk.stem.enm.stem(word)


class MiddleHighGermanStemmingProcess(StemmingProcess):
    """The default Middle High German stemming algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import MiddleHighGermanTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom MHG pipeline", \
    processes=[MiddleHighGermanTokenizationProcess, MiddleHighGermanStemmingProcess], \
    language=get_lang("gmh"))
    >>> nlp = NLP(language='gmh', custom_pipeline = pipe, suppress_banner=True)
    >>> nlp(get_example_text("gmh")[:29]).stems
    ['uns', 'ist', 'in', 'alten', 'mær', 'wund']
    """

    description = "Default stemmer for the Middle High German language."

    @staticmethod
    def algorithm(word: str) -> str:
        return cltk.stem.gmh.stem(word)


class OldFrenchStemmingProcess(StemmingProcess):
    """The default Old French stemming algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import OldFrenchTokenizationProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old French pipeline", \
    processes=[OldFrenchTokenizationProcess, OldFrenchStemmingProcess], \
    language=get_lang("fro"))
    >>> nlp = NLP(language='fro', custom_pipeline = pipe, suppress_banner=True)
    >>> nlp(get_example_text("fro")[:29]).stems
    ['un', 'aventu', 'vos', 'voil', 'di', 'mo']
    """

    description = "Default stemmer for the Old French language."

    @staticmethod
    def algorithm(word: str) -> str:
        return cltk.stem.fro.stem(word)
