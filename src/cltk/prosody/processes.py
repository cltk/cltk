"""
Processes for poetry

"""

from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process

from cltk.prosody.grc import GreekScanner
from cltk.prosody.lat.scanner import LatinScanner
# from cltk.prosody.gmh import MiddleHighGermanScanner
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
    >>> pipe = Pipeline(description="A custom Ancient Greek pipeline", \
    processes=[GreekTokenizationProcess, GreekPoetryProcess], \
    language=get_lang("grc"))
    >>> nlp = NLP(language='grc', custom_pipeline = pipe)
    >>> nlp(get_example_text("grc")).scanned_text
    ['˘˘˘˘¯¯¯˘¯¯¯¯˘¯˘˘˘¯¯˘¯˘¯˘¯¯¯x', '˘¯¯¯¯˘˘¯¯˘˘¯˘¯¯˘˘˘˘¯¯¯˘˘¯˘˘x', '¯¯˘¯¯˘¯˘˘¯¯¯˘¯¯˘x', '˘¯˘˘¯¯˘˘¯˘˘¯˘¯¯˘¯˘˘¯˘˘¯˘˘˘¯¯˘¯¯˘¯¯¯˘˘¯˘˘˘¯¯˘¯¯¯¯¯˘x', '˘¯¯¯¯¯¯˘˘¯˘˘˘˘¯˘˘˘¯¯¯˘¯˘¯¯¯˘¯˘¯¯¯¯¯¯˘¯¯˘¯˘¯˘¯¯˘¯¯˘˘˘¯¯¯¯˘˘¯¯˘¯˘¯¯˘¯˘˘¯¯˘¯x', '¯¯¯¯˘˘¯˘˘˘˘¯¯˘˘¯˘¯˘˘¯¯¯¯¯x', '¯¯˘¯¯˘˘¯˘¯¯˘¯¯˘˘¯˘¯¯˘˘˘¯˘¯˘¯¯˘¯¯¯˘¯¯˘˘¯¯˘˘˘¯˘˘˘¯¯¯˘˘˘˘¯¯¯˘˘¯¯˘¯¯¯¯˘˘˘¯˘˘˘˘¯˘˘¯¯¯¯˘˘¯¯˘¯¯˘˘¯˘¯˘˘˘¯˘˘˘˘˘¯¯¯¯˘¯˘¯¯˘˘¯˘¯¯˘¯¯˘¯˘¯˘x', '¯˘˘¯¯¯˘¯¯¯¯¯˘¯¯˘˘¯¯¯¯˘˘¯˘¯˘˘¯¯˘¯¯˘˘x', '¯¯¯¯˘˘¯¯˘¯¯¯¯¯˘˘¯˘˘¯¯˘˘˘x', '˘¯˘˘¯¯¯˘¯˘¯¯˘¯˘˘˘¯˘¯˘¯˘¯¯˘˘¯¯˘˘˘¯˘˘¯˘¯¯˘˘˘¯˘¯˘¯˘˘˘¯˘˘˘¯˘¯¯¯¯˘˘˘¯¯¯˘˘x', '˘¯˘¯¯x', '¯˘¯¯˘˘˘˘¯¯˘˘˘˘˘¯¯˘¯˘˘¯˘˘¯¯x', '˘¯¯¯˘¯˘¯¯˘˘˘¯˘x', '¯˘¯˘¯¯¯¯˘˘˘˘˘˘¯˘˘˘¯˘˘¯¯˘¯¯˘˘¯¯¯¯¯˘¯¯˘¯˘˘˘˘¯˘˘˘¯¯¯¯¯¯¯˘˘¯˘¯¯˘¯˘¯˘¯˘¯¯¯˘¯¯˘˘¯˘¯˘¯¯¯¯¯˘¯˘¯˘¯˘¯¯˘˘˘¯˘˘¯¯¯¯¯¯˘˘¯¯˘¯˘˘¯¯x', '˘¯¯¯˘¯¯˘˘¯¯˘¯˘˘¯¯˘x']
    """

    description = "The default Ancient Greek poetry process"

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
    ['u--u---u----x', '-uu-uuu--u-ux', 'uu-uuuuuuuuux', 'u-u---u----ux', '--uuu-uu---ux', '-uuu--u---uux', '----uuuuu--ux', '-u-u-uu---uux']
    """

    description = "The default Latin poetry process"

    @cachedproperty
    def algorithm(self):
        return LatinScanner()


# class MiddleHighGermanPoetryProcess(PoetryProcess):
#     """
#     >>> from cltk.core.data_types import Process, Pipeline
#     >>> from cltk.tokenizers.processes import MiddleHighGermanTokenizationProcess
#     >>> from cltk.languages.utils import get_lang
#     >>> from cltk.languages.example_texts import get_example_text
#     >>> from cltk.nlp import NLP
#     >>> pipe = Pipeline(description="A custom Middle High German pipeline", \
#     processes=[MiddleHighGermanTokenizationProcess, MiddleHighGermanPoetryProcess], \
#     language=get_lang("non"))
#     >>> nlp = NLP(language='non', custom_pipeline = pipe)
#     >>> nlp(get_example_text("non")).scanned_text
#
#     """
#
#     description = "The default Middle High German poetry process"
#
#     @cachedproperty
#     def algorithm(self):
#         return MiddleHighGermanScanner()


# class OldNorsePoetryProcess(PoetryProcess):
#     """
#     >>> from cltk.core.data_types import Process, Pipeline
#     >>> from cltk.tokenizers.processes import OldNorseTokenizationProcess
#     >>> from cltk.languages.utils import get_lang
#     >>> from cltk.languages.example_texts import get_example_text
#     >>> from cltk.nlp import NLP
#     >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
#     processes=[OldNorseTokenizationProcess, OldNorsePoetryProcess], \
#     language=get_lang("non"))
#     >>> nlp = NLP(language='non', custom_pipeline = pipe)
#     >>> text = ["Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."]
#     >>> nlp(text).scanned_text
#
#     """
#
#     description = "The default Old Norse poetry process"
#
#     @cachedproperty
#     def algorithm(self):
#         return OldNorseScanner()
