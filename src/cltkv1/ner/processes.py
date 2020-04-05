"""This module holds the ``Process``es for NER."""

from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltkv1.core.data_types import Doc, Process
from cltkv1.ner.ner import tag_ner


@dataclass
class NERProcess(Process):
    """To be inherited for each language's NER declarations.

    >>> from cltkv1.core.data_types import Doc
    >>> from cltkv1.ner.processes import NERProcess
    >>> from cltkv1.core.data_types import Process
    >>> issubclass(NERProcess, Process)
    True
    >>> emb_proc = NERProcess(input_doc=Doc(raw="some input data"))
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        return tag_ner(lang=self.language)

    # xxx
    def run(self):
        tmp_doc = self.input_doc
        ner_obj = self.algorithm
        for index, word_obj in enumerate(tmp_doc.words):
            word_ner = ner_obj.tag_ner(word=word_obj.string)
            word_obj.named_entity = word_ner
            tmp_doc.words[index] = word_obj
        self.output_doc = tmp_doc


# @dataclass
# class LatinEmbeddingsProcess(EmbeddingsProcess):
#     """The default Latin embeddings algorithm.
#
#     >>> from cltkv1.core.data_types import Doc, Word
#     >>> from cltkv1.ner.ner import LatinEmbeddingsProcess
#     >>> from cltkv1.utils.example_texts import get_example_text
#     >>> language = "lat"
#     >>> example_text = get_example_text(language)
#     >>> tokens = [Word(string=token) for token in example_text.split(" ")]
#     >>> a_process = LatinEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
#     >>> a_process.run()
#     >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
#     True
#     """
#
#     language: str = "lat"
#     description: str = "Default embeddings for Latin."
#
#
# @dataclass
# class OldEnglishEmbeddingsProcess(EmbeddingsProcess):
#     """The default Old French embeddings algorithm.
#
#     >>> from cltkv1.core.data_types import Doc, Word
#     >>> from cltkv1.ner.ner import OldFrenchEmbeddingsProcess
#     >>> from cltkv1.utils.example_texts import get_example_text
#     >>> language = "fro"
#     >>> example_text = get_example_text(language)
#     >>> tokens = [Word(string=token) for token in example_text.split(" ")]
#     >>> a_process = OldFrenchEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
#     >>> a_process.run()
#     >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
#     True
#     """
#
#     description: str = "Default embeddings for Old French."
#     language: str = "ang"
