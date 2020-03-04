"""This module holds the ``Process``es, related to embeddings,
that are called by ``Pipeline``s.

TODO: Add embedding Processes for "arb", "arc", [] "got", [x] "lat", "pli", "san", "xno"
"""

from dataclasses import dataclass
from typing import Callable

from cltkv1.core.data_types import Doc, Process
from cltkv1.embeddings.embeddings import FastTextEmbeddings


def make_embedding_algorithm(iso_code: str) -> Callable[[Doc], Doc]:
    """A closure for marshalling Docs to CLTK embedding methods."""
    embeddings_obj = FastTextEmbeddings(iso_code=iso_code)

    def algorithm(self, doc: Doc) -> Doc:
        # doc.embeddings = list()

        for word_obj in doc.words:
            word_embedding = embeddings_obj.get_word_vector(word=word_obj.string)
            word_obj.embedding = word_embedding
            # doc.embeddings.append(word_obj)

        return doc

    return algorithm


GOTHIC_WORD_EMBEDDING = make_embedding_algorithm(iso_code="got")
LATIN_WORD_EMBEDDING = make_embedding_algorithm(iso_code="lat")


@dataclass
class EmbeddingsProcess(Process):
    """To be inherited for each language's embeddings declarations.

    .. note::
        There can be no ``DefaultEmbeddingsProcess`` because word embeddings are naturally language-specific.

    Example: ``EmbeddingsProcess`` <- ``LatinEmbeddingsProcess``

    >>> from cltkv1.core.data_types import Doc
    >>> from cltkv1.embeddings.processes import EmbeddingsProcess
    >>> from cltkv1.core.data_types import Process
    >>> issubclass(EmbeddingsProcess, Process)
    True
    >>> emb_proc = EmbeddingsProcess(input_doc=Doc(raw="some input data"))
    """

    language: str = None


@dataclass
class LatinEmbeddingsProcess(EmbeddingsProcess):
    """The default Latin embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import LatinEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> tokens = [Word(string=token) for token in " ".split(get_example_text("lat"))]
    >>> proc = LatinEmbeddingsProcess(input_doc=Doc(raw=get_example_text("lat"), words=tokens))

    >>> proc.run()
    >>> proc.output_doc

    # >>> embeddings.output_doc.embeddings
    # [1, 2, 3]
    """

    algorithm = LATIN_WORD_EMBEDDING
    description: str = "Default embeddings for Latin."
    language: str = "lat"


@dataclass
class GothicEmbeddingsProcess(EmbeddingsProcess):
    """The default Latin embeddings algorithm.

    # >>> from cltkv1.core.data_types import Doc
    # >>> from cltkv1.embeddings.processes import GothicEmbeddingsProcess
    # >>> from cltkv1.utils.example_texts import get_example_text
    # >>> embeddings = GothicEmbeddingsProcess(input_doc=Doc(raw=get_example_text("got")[:23]))
    #
    # >>> embeddings.run()
    # >>> embeddings.output_doc.embeddings
    # [1, 2, 3]
    """

    algorithm = GOTHIC_WORD_EMBEDDING
    description: str = "Default embeddings for Gothic."
    language: str = "got"
