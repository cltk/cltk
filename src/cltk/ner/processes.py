"""This module holds the ``Process``es for NER."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, List

from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.ner.ner import tag_ner


@dataclass
class NERProcess(Process):
    """To be inherited for each language's NER declarations.

    >>> from cltk.core.data_types import Doc
    >>> from cltk.ner.processes import NERProcess
    >>> from cltk.core.data_types import Process
    >>> issubclass(NERProcess, Process)
    True
    >>> emb_proc = NERProcess()
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        return tag_ner

    def run(self, input_doc: Doc) -> Doc:
        output_doc = deepcopy(input_doc)

        ner_obj = self.algorithm
        entity_values = ner_obj(
            iso_code=self.language, input_tokens=input_doc.tokens
        )  # type: List[Any]
        for index, word_obj in enumerate(output_doc.words):
            word_obj.named_entity = entity_values[index]
            output_doc.words[index] = word_obj

        return output_doc


@dataclass
class GreekNERProcess(NERProcess):
    """The default Greek NER algorithm.

    .. todo::
       Update doctest w/ production model

    >>> from cltk.core.data_types import Doc, Word
    >>> from cltk.languages.example_texts import get_example_text
    >>> from boltons.strutils import split_punct_ws
    >>> text = "ἐπὶ δ᾽ οὖν τοῖς πρώτοις τοῖσδε Περικλῆς ὁ Ξανθίππου ᾑρέθη λέγειν. καὶ ἐπειδὴ καιρὸς ἐλάμβανε, προελθὼν ἀπὸ τοῦ σήματος ἐπὶ βῆμα ὑψηλὸν πεποιημένον, ὅπως ἀκούοιτο ὡς ἐπὶ πλεῖστον τοῦ ὁμίλου, ἔλεγε τοιάδε."
    >>> tokens = [Word(string=token) for token in split_punct_ws(text)]
    >>> a_process = GreekNERProcess()
    >>> output_doc = a_process.run(Doc(raw=text, words=tokens))
    >>> output_doc.words[7].string
    'ὁ'
    >>> output_doc.words[7].named_entity
    False
    >>> output_doc.words[8].string
    'Ξανθίππου'
    >>> output_doc.words[8].named_entity
    False

    """

    language: str = "grc"
    description: str = "Default NER for Greek."


@dataclass
class OldEnglishNERProcess(NERProcess):
    """The default OE NER algorithm.

    .. todo::
       Update doctest w/ production model

    >>> from cltk.core.data_types import Doc, Word
    >>> from cltk.languages.example_texts import get_example_text
    >>> from boltons.strutils import split_punct_ws
    >>> text = get_example_text(iso_code="ang")
    >>> tokens = [Word(string=token) for token in split_punct_ws(text)]
    >>> a_process = OldEnglishNERProcess()
    >>> output_doc = a_process.run(Doc(raw=text, words=tokens))
    >>> output_doc.words[2].string, output_doc.words[2].named_entity
    ('Gardena', 'LOCATION')
    """

    language: str = "ang"
    description: str = "Default NER for Old English."


@dataclass
class LatinNERProcess(NERProcess):
    """The default Latin NER algorithm.

    >>> from cltk.core.data_types import Doc, Word
    >>> from cltk.languages.example_texts import get_example_text
    >>> from boltons.strutils import split_punct_ws
    >>> tokens = [Word(string=token) for token in split_punct_ws(get_example_text("lat"))]
    >>> a_process = LatinNERProcess()
    >>> output_doc = a_process.run(Doc(raw=get_example_text("lat"), words=tokens))
    >>> [word.named_entity for word in output_doc.words][:20]
    ['LOCATION', False, False, False, False, False, False, False, False, False, 'LOCATION', False, 'LOCATION', False, False, False, False, 'LOCATION', False, 'LOCATION']
    """

    language: str = "lat"
    description: str = "Default NER for Latin."


@dataclass
class OldFrenchNERProcess(NERProcess):
    """The default Old French NER algorithm.

    >>> from cltk.core.data_types import Doc, Word
    >>> from cltk.languages.example_texts import get_example_text
    >>> from boltons.strutils import split_punct_ws
    >>> tokens = [Word(string=token) for token in split_punct_ws(get_example_text("fro"))]
    >>> a_process = OldFrenchNERProcess()
    >>> output_doc = a_process.run(Doc(raw=get_example_text("fro"), words=tokens))
    >>> output_doc.words[30].string
    'Bretaigne'
    >>> output_doc.words[30].named_entity
    'LOC'
    >>> output_doc.words[31].named_entity
    False
    """

    language: str = "fro"
    description: str = "Default NER for Old French."
