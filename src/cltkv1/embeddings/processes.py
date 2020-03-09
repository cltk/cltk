"""This module holds the ``Process``es, related to embeddings,
that are called by ``Pipeline``s.

TODO: Add embedding FT Processes for [] "arb",[] "arc", [x] "got", [x] "lat", [] "pli", [] "san", [] "xno"
"""

from dataclasses import dataclass
from typing import Callable

import numpy as np

from cltkv1.core.data_types import Doc, Process
from cltkv1.embeddings.embeddings import FastTextEmbeddings


def make_embedding_algorithm(iso_code: str) -> Callable[[Doc], Doc]:
    """A closure for marshalling Docs to CLTK embedding methods."""
    embeddings_obj = FastTextEmbeddings(iso_code=iso_code)

    def algorithm(self, doc: Doc) -> Doc:

        embedding_length = None
        for word_obj in doc.words:
            if not embedding_length:
                embedding_length = embeddings_obj.get_embedding_length()
            word_embedding = embeddings_obj.get_word_vector(word=word_obj.string)
            if not isinstance(word_embedding, np.ndarray):
                word_embedding = np.zeros([embedding_length])
            word_obj.embedding = word_embedding

        return doc

    return algorithm


ARABIC_WORD_EMBEDDING = make_embedding_algorithm(iso_code="arb")
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
class ArabicEmbeddingsProcess(EmbeddingsProcess):
    """The default Arabic embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import LatinEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> language = "arb"
    >>> example_text = get_example_text(language)
    >>> tokens = [Word(string=token) for token in example_text.split(" ")]
    >>> a_process = ArabicEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
    >>> a_process.run()
    >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
    True
    """
    algorithm = ARABIC_WORD_EMBEDDING
    description: str = "Default embeddings for Arabic."
    language: str = "arb"


@dataclass
class GothicEmbeddingsProcess(EmbeddingsProcess):
    """The default Gothic embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import LatinEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> language = "got"
    >>> example_text = get_example_text(language)
    >>> tokens = [Word(string=token) for token in example_text.split(" ")]
    >>> a_process = GothicEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
    >>> a_process.run()
    >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
    True
    """
    algorithm = GOTHIC_WORD_EMBEDDING
    description: str = "Default embeddings for Gothic."
    language: str = "got"


@dataclass
class LatinEmbeddingsProcess(EmbeddingsProcess):
    """The default Latin embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import LatinEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> language = "lat"
    >>> example_text = get_example_text(language)
    >>> tokens = [Word(string=token) for token in example_text.split(" ")]
    >>> a_process = LatinEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
    >>> a_process.run()
    >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
    True
    """
    algorithm = LATIN_WORD_EMBEDDING
    description: str = "Default embeddings for Latin."
    language: str = "lat"
