"""This module holds the ``Process``es, related to embeddings,
that are called by ``Pipeline``s.
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


LATIN_WORD_EMBEDDING = make_embedding_algorithm(iso_code="lat")


@dataclass
class EmbeddingsProcess(Process):
    """To be inherited for each language's embeddings declarations.

    .. note::
        There can be no ``DefaultEmbeddingsProcess`` because word embeddings are naturally language-specific.

    Example: ``EmbeddingsProcess`` <- ``LatinEmbeddingsProcess``

    >>> from cltkv1.core.data_types import Doc
    >>> from cltkv1.embeddings.embeddings import EmbeddingsProcess
    >>> from cltkv1.core.data_types import Process
    >>> issubclass(EmbeddingsProcess, Process)
    True
    >>> emb_proc = EmbeddingsProcess(input_doc=Doc(raw="some input data"))
    """

    language: str = None


@dataclass
class LatinEmbeddingsProcess(EmbeddingsProcess):
    """The default Latin embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc
    >>> from cltkv1.embeddings.embeddings import LatinEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> embeddings = LatinEmbeddingsProcess(input_doc=Doc(raw=get_example_text("lat")[:23]))

    >>> embeddings.run()
    >>> embeddings.output_doc.embeddings
    [1, 2, 3]
    """

    algorithm = LATIN_WORD_EMBEDDING
    description: str = "Default embeddings for Latin."
    language: str = "lat"


if __name__ == "__main__":
    x = make_embedding_algorithm(iso_code="lat")
    print(x)

    LatinEmbeddingsProcess(language="lat")
