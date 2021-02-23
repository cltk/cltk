"""
Processes for dictionary lookup.
"""

from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.core.exceptions import CLTKException
from cltk.lexicon.lat import LatinLewisLexicon

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


@dataclass
class LexiconProcess(Process):
    """To be inherited for each language's dictionary declarations.

    Example: ``LexiconProcess`` -> ``LatinLexiconProcess``

    >>> from cltk.lemmatize.processes import LemmatizationProcess
    >>> from cltk.core.data_types import Process
    >>> issubclass(LexiconProcess, Process)
    True
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        if self.language == "lat":
            lex_class = LatinLewisLexicon()
        else:
            raise CLTKException(f"No lookup algorithm for language '{self.language}'.")
        return lex_class

    def run(self, input_doc: Doc) -> Doc:
        lookup_algo = self.algorithm
        output_doc = deepcopy(input_doc)
        for word in output_doc.words:
            word.definition = lookup_algo.lookup(word.lemma)
        return output_doc


class LatinLexiconProcess(LexiconProcess):
    """The default Latin dictionary lookup algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import LatinTokenizationProcess
    >>> from cltk.lemmatize.processes import LatinLemmatizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Latin pipeline", \
    processes=[LatinTokenizationProcess, LatinLemmatizationProcess, LatinLexiconProcess], \
    language=get_lang("lat"))
    >>> nlp = NLP(language='lat', custom_pipeline=pipe)
    >>> cltk_doc = nlp.analyze(text=get_example_text("lat"))
    >>> [word.definition for word in cltk_doc.words][:5]
    ['?', '?', '?']
    """

    description = "Dictionary lookup process for Latin"
    language = "lat"

    @cachedproperty
    def algorithm(self):
        return LatinLewisLexicon()
