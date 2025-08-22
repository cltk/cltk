from copy import copy
from functools import cached_property

from boltons.strutils import split_punct_ws

from cltk.core.data_types_v2 import Doc, Process
from cltk.stops.words import Stops


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

    @cached_property
    def algorithm(self):
        return Stops(iso_code=self.language_code).get_stopwords()

    def run(self, input_doc: Doc) -> Doc:
        """Note this marks a word a stop if there is a match on
        either the inflected form (``Word.string``) or the
        lemma (``Word.lemma``).
        """
        output_doc: Doc = copy(input_doc)
        stops_list: StopsProcess = self.algorithm

        for index, word_obj in enumerate(output_doc.words):
            if (word_obj.string in stops_list) or (word_obj.lemma in stops_list):
                word_obj.stop: bool = True
            else:
                word_obj.stop: bool = False
            output_doc.words[index] = word_obj

        return output_doc
