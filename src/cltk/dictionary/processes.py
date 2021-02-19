"""
Processes for dictionary lookup.
"""

from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.lemmatize.ang import OldEnglishDictionaryLemmatizer
from cltk.lemmatize.fro import OldFrenchDictionaryLemmatizer
from cltk.lemmatize.grc import GreekBackoffLemmatizer
from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.lemmatize.non import OldNorseLemmatizationProcess
from cltk.lemmatize.processes import GreekLemmatizationProcess, LatinLemmatizationProcess

from cltk.dictionary.grc import GreekDictionary
from cltk.dictionary.lat import LatinDictionary


@dataclass
class DictionaryProcess(Process):
    """To be inherited for each language's dictionary declarations.

    Example: ``DictionaryProcess`` -> ``LatinDictionaryProcess``

    >>> from cltk.lemmatize.processes import LemmatizationProcess
    >>> from cltk.core.data_types import Process
    >>> issubclass(DictionaryProcess, Process)
    True
    """

    def run(self, input_doc: Doc) -> Doc:
        dictionary_lookup = self.algorithm

        output_doc = deepcopy(input_doc)
        for word in output_doc.words:
            word.definition = dictionary_lookup(word.lemma)

        return output_doc


class GreekDictionaryProcess(DictionaryProcess):
    """The default Ancient Greek dictionary lookup algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import MultilingualTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Greek pipeline", \
    processes=[MultilingualTokenizationProcess, GreekLemmatizationProcess, GreekDictionaryProcess], \
    language=get_lang("grc"))
    >>> nlp = NLP(language='grc', custom_pipeline = pipe)
    >>> nlp(get_example_text("grc")).lemmata[30:40]
    ['ἔλεγον.', 'καίτοι', 'ἀληθές', 'γε', 'ὡς', 'ἔπος', 'εἰπεῖν', 'οὐδὲν', 'εἰρήκασιν.', 'μάλιστα']
    """

    description = "Dictionary lookup process for Ancient Greek"

    @cachedproperty
    def algorithm(self):
        return GreekDictionary()


class LatinDictionaryProcess(DictionaryProcess):
    """The default Latin dictionary lookup algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import LatinTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Latin pipeline", \
    processes=[LatinTokenizationProcess, LatinLemmatizationProcess, LatinDictionaryProcess], \
    language=get_lang("lat"))
    >>> nlp = NLP(language='lat', custom_pipeline = pipe)
    >>> nlp(get_example_text("lat")).lemmata[30:40]
    ['institutis', ',', 'legibus', 'inter', 'se', 'differunt', '.', 'Gallos', 'ab', 'Aquitanis']
    """

    description = "Dictionary lookup process for Latin"

    @cachedproperty
    def algorithm(self):
        return LatinDictionary()


class OldNorseDictionaryProcess(DictionaryProcess):
    """The default Old Norse dictionary lookup algorithm

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import OldNorseTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
    processes=[OldNorseTokenizationProcess, OldNorseLemmatizationProcess, OldNorseDictionaryProcess], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline = pipe)
    >>> nlp(get_example_text("non")).lemmata[30:40]

    ""
    """