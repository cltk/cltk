"""This module holds the embeddings ``Process``es."""

import os
from collections.abc import ValuesView
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, Optional

import numpy as np
from boltons.cacheutils import cachedproperty

from cltk.core.cltk_logger import logger
from cltk.core.data_types import Doc, Process
from cltk.core.exceptions import CLTKException
from cltk.embeddings.embeddings import FastTextEmbeddings, Word2VecEmbeddings
from cltk.embeddings.sentence import get_sent_embeddings
from cltk.ner.spacy_ner import download_prompt
from cltk.utils import CLTK_DATA_DIR
from cltk.utils.file_operations import open_pickle

TFIDF_MAP: Dict[str, str] = {
    "lat": os.path.join(
        CLTK_DATA_DIR,
        "lat/model/lat_models_cltk/tfidf/",
    ),
}


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
    >>> emb_proc = EmbeddingsProcess()
    """

    language: str = None
    variant: str = "fasttext"
    embedding_length: int = None
    idf_model: Optional[Dict[str, float]] = field(repr=False, default=None)
    min_idf: Optional[np.float64] = None
    max_idf: Optional[np.float64] = None

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

    def run(self, input_doc: Doc) -> Doc:
        """Compute the embeddings."""
        output_doc = deepcopy(input_doc)
        # For word2vec-style embedding, used for word embeddings
        embeddings_obj = self.algorithm
        for index, word_obj in enumerate(output_doc.words):
            if not self.embedding_length:
                self.embedding_length = embeddings_obj.get_embedding_length()
            word_embedding = embeddings_obj.get_word_vector(word=word_obj.string)
            if not isinstance(word_embedding, np.ndarray):
                word_embedding = np.zeros([self.embedding_length])
            word_obj.embedding = word_embedding
            output_doc.words[index] = word_obj

        # For sentence embeddings, uses TF-IDF
        # This checks whether a file of Tf-IDF embeddings is available
        if not self.idf_model:
            # First check if user has hard coded the path as an OS variable
            fp_idf_os_env: Optional[str] = os.environ.get("WORD_IDF_FILE")
            if fp_idf_os_env:
                self.idf_model = open_pickle(path=fp_idf_os_env)
            # Check if IDF embeddings available available in CLTK repo
            elif TFIDF_MAP.get(self.language):
                model_path: str = TFIDF_MAP[self.language]
                if not os.path.isdir(model_path):
                    msg = f"TF-IDF model path '{model_path}' not found. Going to try to download it ..."
                    logger.warning(msg)
                    dl_msg = f"This part of the CLTK depends upon models from the CLTK project."
                    model_url = f"https://github.com/cltk/{self.language}_models_cltk"
                    download_prompt(
                        iso_code=self.language, message=dl_msg, model_url=model_url
                    )
                self.idf_model = open_pickle(path=f"{model_path}word_idf.pkl")
        # Min and max values are needed while generating sentence embeddings
        if self.idf_model and not self.min_idf:
            tfidf_values: ValuesView = self.idf_model.values()
            tfidf_values_array: np.array = np.array(list(tfidf_values))
            self.min_idf: np.float64 = tfidf_values_array.min()
            self.max_idf: np.float64 = tfidf_values_array.max()
        if self.idf_model:
            for index, sent_obj in enumerate(output_doc.sentences):
                output_doc.sentence_embeddings[index] = get_sent_embeddings(
                    sent=sent_obj,
                    idf_model=self.idf_model,
                    min_idf=self.min_idf,
                    max_idf=self.max_idf,
                    dimensions=self.embedding_length,
                )
        return output_doc


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
