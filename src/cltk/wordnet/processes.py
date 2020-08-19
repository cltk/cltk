"""``Process`` to wrap WordNet."""


from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Tuple

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process, Word
from cltk.wordnet.wordnet import WordNetCorpusReader, WordNetICCorpusReader


@dataclass
class WordNetProcess(Process):
    """A ``Process`` type to capture what the
    ``wordnet`` module can do for a
    given language.
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        """Returns a WordNetCorpusReader appropriate to the Document's language"""
        language = None
        if self.language == "lat":
            language = "lat"
        elif self.language == "grc":
            language = "grk"
        elif self.language == "san":
            language = "skt"
        if language is not None:
            return WordNetCorpusReader(language)

    def run(self, input_doc: Doc) -> Doc:
        """Adds a list of Synset objects, representing a Word's senses, to all lemmatized words"""

        output_doc = deepcopy(input_doc)

        wn = self.algorithm
        for word in output_doc.words:
            # TODO: map CLTK lemmas to WN lemmas
            if word.lemma:
                synsets = list(wn.lemma(word.lemma, return_ambiguous=False).synsets())
                word.synsets = synsets

        return output_doc
