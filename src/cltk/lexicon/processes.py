"""
Processes for dictionary lookup.
"""

from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.lemmatize.processes import LatinLemmatizationProcess

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

    def run(self, input_doc: Doc) -> Doc:
        lookup = self.algorithm

        output_doc = deepcopy(input_doc)
        for word in output_doc.words:
            word.definition = lookup(word.lemma)

        return output_doc


class LatinLexiconProcess(LexiconProcess):
    """The default Latin dictionary lookup algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.tokenizers import LatinTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text
    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Latin pipeline", \
    processes=[LatinTokenizationProcess, LatinLemmatizationProcess, LatinLexiconProcess], \
    language=get_lang("lat"))
    >>> nlp = NLP(language='lat', custom_pipeline = pipe)
    >>> nlp(get_example_text("lat")).lemmata[30:40]
    ['institutis', ',', 'legibus', 'inter', 'se', 'differunt', '.', 'Gallos', 'ab', 'Aquitanis']
    """

    description = "Dictionary lookup process for Latin"

    @cachedproperty
    def algorithm(self):
        return LatinLewisLexicon()
