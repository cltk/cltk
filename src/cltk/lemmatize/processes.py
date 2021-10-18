"""Processes for lemmatization."""

from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.lemmatize.ang import OldEnglishDictionaryLemmatizer
from cltk.lemmatize.fro import OldFrenchDictionaryLemmatizer
from cltk.lemmatize.grc import GreekBackoffLemmatizer
from cltk.lemmatize.lat import LatinBackoffLemmatizer


@dataclass
class LemmatizationProcess(Process):
    """To be inherited for each language's lemmatization declarations.

    Example: ``LemmatizationProcess`` -> ``LatinLemmatizationProcess``

    >>> from cltk.lemmatize.processes import LemmatizationProcess
    >>> from cltk.core.data_types import Process
    >>> issubclass(LemmatizationProcess, Process)
    True
    """

    def run(self, input_doc: Doc) -> Doc:
        lemmatizer = self.algorithm

        output_doc = deepcopy(input_doc)
        for word in output_doc.words:
            word.lemma = lemmatizer(word.string)

        return output_doc


class GreekLemmatizationProcess(LemmatizationProcess):
    """The default Ancient Greek lemmatization algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import MultilingualTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Greek pipeline", \
    processes=[MultilingualTokenizationProcess, GreekLemmatizationProcess], \
    language=get_lang("grc"))
    >>> nlp = NLP(language='grc', custom_pipeline=pipe, suppress_banner=True)
    >>> nlp(get_example_text("grc")).lemmata[30:40]
    ['ἔλεγον.', 'καίτοι', 'ἀληθές', 'γε', 'ὡς', 'ἔπος', 'εἰπεῖν', 'οὐδὲν', 'εἰρήκασιν.', 'μάλιστα']
    """

    description = "Lemmatization process for Ancient Greek"

    @cachedproperty
    def algorithm(self):
        return GreekBackoffLemmatizer()


class LatinLemmatizationProcess(LemmatizationProcess):
    """The default Latin lemmatization algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import LatinTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Latin pipeline", \
    processes=[LatinTokenizationProcess, LatinLemmatizationProcess], \
    language=get_lang("lat"))
    >>> nlp = NLP(language='lat', custom_pipeline=pipe, suppress_banner=True)
    >>> nlp(get_example_text("lat")).lemmata[30:40]
    ['institutis', ',', 'legibus', 'inter', 'se', 'differunt', '.', 'Gallos', 'ab', 'Aquitanis']
    """

    description = "Lemmatization process for Latin"

    @cachedproperty
    def algorithm(self):
        return LatinBackoffLemmatizer()


@dataclass
class OldEnglishLemmatizationProcess(LemmatizationProcess):
    """The default Old English lemmatization algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import MultilingualTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old English pipeline", \
    processes=[MultilingualTokenizationProcess, OldEnglishLemmatizationProcess], \
    language=get_lang("ang"))
    >>> nlp = NLP(language='ang', custom_pipeline=pipe, suppress_banner=True)
    >>> nlp(get_example_text("ang")).lemmata[30:40]
    ['siððan', 'ær', 'weorþan', 'feasceaft', 'findan', ',', 'he', 'se', 'frofre', 'gebidan']
    """

    description = "Lemmatization process for Old English"

    @cachedproperty
    def algorithm(self):
        return OldEnglishDictionaryLemmatizer()


@dataclass
class OldFrenchLemmatizationProcess(LemmatizationProcess):
    """The default Old French lemmatization algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import MultilingualTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old French pipeline", \
    processes=[MultilingualTokenizationProcess, OldFrenchLemmatizationProcess], \
    language=get_lang("fro"))
    >>> nlp = NLP(language='fro', custom_pipeline=pipe, suppress_banner=True)
    >>> nlp(get_example_text("fro")).lemmata[30:40]
    ['avenir', 'jadis', 'en', 'bretaingne', 'avoir', '.I.', 'molt', 'riche', 'chevalier', 'PUNK']
    """

    description = "Lemmatization process for Old French"

    @cachedproperty
    def algorithm(self):
        return OldFrenchDictionaryLemmatizer()
