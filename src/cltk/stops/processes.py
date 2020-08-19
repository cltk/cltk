from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty
from boltons.strutils import split_punct_ws

from cltk.core.data_types import Doc, Process
from cltk.stops.words import Stops


@dataclass
class StopsProcess(Process):
    """

    >>> from cltk.core.data_types import Doc, Word
    >>> from cltk.stops.processes import StopsProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> lang = "lat"
    >>> words = [Word(string=token) for token in split_punct_ws(get_example_text(lang))]
    >>> stops_process = StopsProcess(language=lang)
    >>> output_doc = stops_process.run(Doc(raw=get_example_text(lang), words=words))
    >>> output_doc.words[1].string
    'est'
    >>> output_doc.words[1].stop
    True
    """

    @cachedproperty
    def algorithm(self):
        return Stops(iso_code=self.language).get_stopwords()

    def run(self, input_doc: Doc) -> Doc:
        """Note this marks a word a stop if there is a match on
        either the inflected form (``Word.string``) or the
        lemma (``Word.lemma``).
        """
        output_doc = deepcopy(input_doc)
        stops_list = self.algorithm

        for index, word_obj in enumerate(output_doc.words):
            if (word_obj.string in stops_list) or (word_obj.lemma in stops_list):
                word_obj.stop = True
            else:
                word_obj.stop = False
            output_doc.words[index] = word_obj

        return output_doc
