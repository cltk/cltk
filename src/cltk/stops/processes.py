from dataclasses import dataclass

from boltons.cacheutils import cachedproperty
from boltons.strutils import split_punct_ws

from cltk.core.data_types import Process
from cltk.stops.words import Stops


@dataclass
class StopsProcess(Process):
    """

    >>> from cltk.core.data_types import Doc, Word
    >>> from cltk.stops.processes import StopsProcess
    >>> from cltk.languages.example_texts import get_example_text
    >>> lang = "lat"
    >>> words = [Word(string=token) for token in split_punct_ws(get_example_text(lang))]
    >>> stops_process = StopsProcess(input_doc=Doc(raw=get_example_text(lang), words=words), language=lang)
    >>> stops_process.run()
    >>> stops_process.output_doc.words[1].string
    'est'
    >>> stops_process.output_doc.words[1].stop
    True
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        return Stops(iso_code=self.language).get_stopwords()

    def run(self):
        """Note this marks a word a stop if there is a match on
        either the inflected form (``Word.string``) or the
        lemma (``Word.lemma``).
        """
        tmp_doc = self.input_doc
        stops_list = self.algorithm
        for index, word_obj in enumerate(tmp_doc.words):
            if (word_obj.string in stops_list) or (word_obj.lemma in stops_list):
                word_obj.stop = True
            else:
                word_obj.stop = False
            tmp_doc.words[index] = word_obj
        self.output_doc = tmp_doc
