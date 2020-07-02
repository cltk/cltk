"""This module holds the ``Process``es, related to embeddings,
that are called by ``Pipeline``s.
"""

from dataclasses import dataclass

import numpy as np
from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, Process
from cltk.core.exceptions import CLTKException
from cltk.embeddings.embeddings import FastTextEmbeddings, Word2VecEmbeddings


@dataclass
class EmbeddingsProcess(Process):
    """To be inherited for each language's embeddings declarations.

    .. note::
        There can be no ``DefaultEmbeddingsProcess`` because word embeddings are naturally language-specific.

    Example: ``EmbeddingsProcess`` <- ``LatinEmbeddingsProcess``

    >>> from cltk.core.data_types import Doc
    >>> from cltk.embeddings.processes import EmbeddingsProcess
    >>> from cltk.core.data_types import Process
    >>> issubclass(EmbeddingsProcess, Process)
    True
    >>> emb_proc = EmbeddingsProcess(input_doc=Doc(raw="some input data"))
    """

    language: str = None
    variant: str = "fasttext"

    @cachedproperty
    def algorithm(self):
        valid_variants = ["fasttext", "nlpl"]
        if self.variant == "fasttext":
            return FastTextEmbeddings(iso_code=self.language)
        elif self.variant == "nlpl":
            return Word2VecEmbeddings(iso_code=self.language)
        else:
            valid_variants_str = "', '".join(valid_variants)
            raise CLTKException(
                f"Invalid embeddings ``variant`` ``{self.variant}``. Available: '{valid_variants_str}'."
            )

    def run(self):
        tmp_doc = self.input_doc
        embedding_length = None
        embeddings_obj = self.algorithm
        for index, word_obj in enumerate(tmp_doc.words):
            if not embedding_length:
                embedding_length = embeddings_obj.get_embedding_length()
            word_embedding = embeddings_obj.get_word_vector(word=word_obj.string)
            if not isinstance(word_embedding, np.ndarray):
                word_embedding = np.zeros([embedding_length])
            word_obj.embedding = word_embedding
            tmp_doc.words[index] = word_obj
        self.output_doc = tmp_doc


@dataclass
class ArabicEmbeddingsProcess(EmbeddingsProcess):
    """The default Arabic embeddings algorithm."""

    description: str = "Default embeddings for Arabic."
    language: str = "arb"


@dataclass
class AramaicEmbeddingsProcess(EmbeddingsProcess):
    """The default Aramaic embeddings algorithm."""

    description: str = "Default embeddings for Aramaic."
    language: str = "arb"


@dataclass
class GothicEmbeddingsProcess(EmbeddingsProcess):
    """The default Gothic embeddings algorithm."""

    description: str = "Default embeddings for Gothic."
    language: str = "got"


@dataclass
class GreekEmbeddingsProcess(EmbeddingsProcess):
    """The default Ancient Greek embeddings algorithm."""

    language: str = "grc"
    description: str = "Default embeddings for Ancient Greek."
    variant: str = "nlpl"


@dataclass
class LatinEmbeddingsProcess(EmbeddingsProcess):
    """The default Latin embeddings algorithm."""

    language: str = "lat"
    description: str = "Default embeddings for Latin."


@dataclass
class OldEnglishEmbeddingsProcess(EmbeddingsProcess):
    """The default Old English embeddings algorithm."""

    description: str = "Default embeddings for Old English."
    language: str = "ang"


@dataclass
class PaliEmbeddingsProcess(EmbeddingsProcess):
    """The default Pali embeddings algorithm."""

    description: str = "Default embeddings for Pali."
    language: str = "pli"


@dataclass
class SanskritEmbeddingsProcess(EmbeddingsProcess):
    """The default Sanskrit embeddings algorithm."""

    description: str = "Default embeddings for Sanskrit."
    language: str = "san"
