"""This module implements syllabification processes for several languages.
You may extend **SyllabificationProcess** and see pre-defined examples.
"""


from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.phonology.ang.phonology import OldEnglishSyllabifier
from cltk.phonology.enm.phonology import MiddleEnglishSyllabifier
from cltk.phonology.gmh.phonology import MiddleHighGermanSyllabifier
from cltk.phonology.lat.phonology import LatinSyllabifier
from cltk.phonology.non.phonology import OldNorseSyllabifier


@dataclass
class SyllabificationProcess(Process):
    """This is the class to extend if you want to code your own syllabification
    process in the CLTK-style.
    """

    def run(self, input_doc: Doc) -> Doc:
        syllabifier = self.algorithm

        output_doc = deepcopy(input_doc)
        for word in output_doc.words:
            word.syllables = syllabifier(word.string.lower())

        return output_doc


class GreekSyllabificationProcess(SyllabificationProcess):
    """Syllabification ``Process`` for Ancient Greek.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import GreekTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk import NLP
    >>> a_pipeline = Pipeline(description="A custom Greek pipeline", processes=[GreekTokenizationProcess, DefaultPunctuationRemovalProcess, GreekSyllabificationProcess], language=get_lang("grc"))
    >>> nlp = NLP(language='grc', custom_pipeline=a_pipeline, suppress_banner=True)
    >>> text = get_example_text("grc")
    >>> cltk_doc = nlp(text)
    >>> [word.syllables for word in cltk_doc.words[:5]]
    [['ὅτι'], ['μὲν'], ['ὑμ', 'εῖς'], ['ὦ'], ['ἄν', 'δρ', 'ες']]

    """

    description = "The default Latin Syllabification process"

    @cachedproperty
    def algorithm(self):
        return LatinSyllabifier()


class LatinSyllabificationProcess(SyllabificationProcess):
    """Syllabification ``Process`` for Latin.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import LatinTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk import NLP
    >>> a_pipeline = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess, DefaultPunctuationRemovalProcess, LatinSyllabificationProcess], language=get_lang("lat"))
    >>> nlp = NLP(language='lat', custom_pipeline=a_pipeline, suppress_banner=True)
    >>> text = get_example_text("lat")
    >>> cltk_doc = nlp(text)
    >>> [word.syllables for word in cltk_doc.words[:5]]
    [['gal', 'li', 'a'], ['est'], ['om', 'nis'], ['di', 'vi', 'sa'], ['in']]
    """

    description = "The default Latin Syllabification process"

    @cachedproperty
    def algorithm(self):
        return LatinSyllabifier()


class MiddleEnglishSyllabificationProcess(SyllabificationProcess):
    """Syllabification ``Process`` for Middle English.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleEnglishTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Middle English pipeline", \
    processes=[MiddleEnglishTokenizationProcess, DefaultPunctuationRemovalProcess, MiddleEnglishSyllabificationProcess], \
    language=get_lang("enm"))
    >>> nlp = NLP(language='enm', custom_pipeline=pipe, suppress_banner=True)
    >>> text = get_example_text("enm").replace('\\n', ' ')
    >>> cltk_doc = nlp(text)
    >>> [word.syllables for word in cltk_doc.words[:5]]
    [['whi', 'lom'], ['as'], ['ol', 'de'], ['sto', 'ries'], ['tellen']]
    """

    description = "The default Middle English Syllabification process"

    @cachedproperty
    def algorithm(self):
        return MiddleEnglishSyllabifier()


class MiddleHighGermanSyllabificationProcess(SyllabificationProcess):
    """Syllabification ``Process`` for Middle High German.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleHighGermanTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Middle High German pipeline", \
    processes=[MiddleHighGermanTokenizationProcess, DefaultPunctuationRemovalProcess, \
    MiddleHighGermanSyllabificationProcess], language=get_lang("gmh"))
    >>> nlp = NLP(language='gmh', custom_pipeline=pipe, suppress_banner=True)
    >>> text = get_example_text("gmh")
    >>> cltk_doc = nlp(text)
    >>> [word.syllables for word in cltk_doc.words[:5]]
    [['uns'], ['ist'], ['in'], ['al', 'ten'], ['mæ', 'ren']]
    """

    description = "The default Middle High German syllabification process"

    @cachedproperty
    def algorithm(self):
        return MiddleHighGermanSyllabifier()


class OldEnglishSyllabificationProcess(SyllabificationProcess):
    """Syllabification ``Process`` for Old English.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import MiddleEnglishTokenizationProcess
    >>> from cltk.text.processes import DefaultPunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old English pipeline", \
    processes=[MiddleEnglishTokenizationProcess, DefaultPunctuationRemovalProcess, OldEnglishSyllabificationProcess], \
    language=get_lang("ang"))
    >>> nlp = NLP(language='ang', custom_pipeline=pipe, suppress_banner=True)
    >>> text = get_example_text("ang")
    >>> cltk_doc = nlp(text)
    >>> [word.syllables for word in cltk_doc.words[:5]]
    [['hwæt'], ['we'], ['gar', 'den', 'a'], ['in'], ['gear', 'da', 'gum']]

    """

    description = "The default Old English syllabification process"

    @cachedproperty
    def algorithm(self):
        return OldEnglishSyllabifier()


class OldNorseSyllabificationProcess(SyllabificationProcess):
    """Syllabification ``Process`` for Old Norse.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers.processes import OldNorseTokenizationProcess
    >>> from cltk.text.processes import OldNorsePunctuationRemovalProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
    processes=[OldNorseTokenizationProcess, OldNorsePunctuationRemovalProcess, OldNorseSyllabificationProcess], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline=pipe, suppress_banner=True)
    >>> text = get_example_text("non")
    >>> cltk_doc = nlp(text)
    >>> [word.syllables for word in cltk_doc.words[:5]]
    [['gyl', 'fi'], ['ko', 'nungr'], ['réð'], ['þar'], ['lön', 'dum']]
    """

    description = "The default Old Norse syllabification process"

    @cachedproperty
    def algorithm(self):
        return OldNorseSyllabifier()
