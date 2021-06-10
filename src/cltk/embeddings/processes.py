"""This module holds the embeddings ``Process``es."""
import os
import pickle
from collections.abc import KeysView, ValuesView
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
from boltons.cacheutils import cachedproperty
from sklearn.decomposition import TruncatedSVD

from cltk.core.cltk_logger import logger
from cltk.core.data_types import Doc, Process, Sentence
from cltk.core.exceptions import CLTKException
from cltk.embeddings.embeddings import FastTextEmbeddings, Word2VecEmbeddings
from cltk.ner.spacy_ner import download_prompt
from cltk.utils import CLTK_DATA_DIR


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
    word_idf: Optional[Dict[str, float]] = field(repr=False, default=None)
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
        embeddings_obj = self.algorithm
        for index, word_obj in enumerate(output_doc.words):
            if not self.embedding_length:
                self.embedding_length = embeddings_obj.get_embedding_length()
            word_embedding = embeddings_obj.get_word_vector(word=word_obj.string)
            if not isinstance(word_embedding, np.ndarray):
                word_embedding = np.zeros([self.embedding_length])
            word_obj.embedding = word_embedding
            output_doc.words[index] = word_obj

        if not self.word_idf:
            # You can bring your own model
            if os.environ.get("WORD_IDF_FILE"):
                with open(os.environ.get("WORD_IDF_FILE"), "rb") as fin:
                    self.word_idf = pickle.load(fin)
            elif TFIDF_MAP.get(self.language):
                model_path = TFIDF_MAP[self.language]
                if not os.path.isdir(model_path):
                    msg = f"TFIDF model path '{model_path}' not found. Going to try to download it ..."
                    logger.warning(msg)
                    dl_msg = f"This part of the CLTK depends upon models from the CLTK project."
                    model_url = f"https://github.com/cltk/{self.language}_models_cltk"
                    download_prompt(
                        iso_code=self.language, message=dl_msg, model_url=model_url
                    )
                else:
                    with open(f"{model_path}word_idf.pkl", "rb") as fin:
                        self.word_idf = pickle.load(fin)
        # These values are needed while generating sentence embeddings
        if self.word_idf and not self.min_idf:
            self.min_idf = np.min(np.array(list(self.word_idf.values())))
            self.max_idf = np.max(np.array(list(self.word_idf.values())))
        if self.word_idf:
            output_doc.sentence_embeddings = {}  # type: Dict[int, np.ndarray]
            for index, sent_obj in enumerate(output_doc.sentences):
                output_doc.sentence_embeddings[index] = get_sent_embeddings(
                    sent_obj,
                    self.word_idf,
                    self.min_idf,
                    self.max_idf,
                    self.embedding_length,
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


TFIDF_MAP: Dict[str, str] = {
    "lat": os.path.join(
        CLTK_DATA_DIR,
        "lat/model/lat_models_cltk/tfidf/",
    ),
}


def rescale_idf(val: float, min_idf: float, max_idf: float) -> float:
    """
    rescale idf values
    """
    return (val - min_idf) / (max_idf - min_idf)


def compute_pc(X: np.ndarray, npc: int = 1) -> np.ndarray:
    """
    Compute the principal components. DO NOT MAKE THE DATA ZERO MEAN!
    :param X: X[i,:] is a data point
    :param npc: number of principal components to remove
    :return: component_[i,:] is the i-th pc

    This has been adapted from the SIF paper code: https://openreview.net/pdf?id=SyK00v5xx
    """
    svd = TruncatedSVD(n_components=npc, n_iter=7, random_state=0)
    svd.fit(X)
    return svd.components_


def remove_pc(X: np.ndarray, npc: int = 1):
    """
    Remove the projection on the principal components
    :param X: X[i,:] is a data point
    :param npc: number of principal components to remove
    :return: XX[i, :] is the data point after removing its projection

    This has been adapted from the SIF paper code: https://openreview.net/pdf?id=SyK00v5xx
    """
    pc = compute_pc(X, npc)
    if npc == 1:
        XX = X - X.dot(pc.transpose()) * pc
    else:
        XX = X - X.dot(pc.transpose()).dot(pc)
    return XX


def get_sent_embeddings(
    sent: Sentence,
    word_idf: Dict[str, float],
    min_idf: float,
    max_idf: float,
    dimensions: int = 300,
) -> np.ndarray:
    """
    Provides the weighted average of a sentence's word vectors
    with the principle component removed.

    Expectations:
    Word can only appear once in a sentence, multiple occurrences are collapsed.
    Must have 2 or more embeddings, otherwise Principle Component cannot be found and removed.

    :param sent: ``Sentence``
    :param word_idf: a dictionary of tokens and idf values
    :param min_idf: the min idf score to use for scaling
    :param max_idf: the max idf score to use for scaling
    :param dimensions: the number of dimensions of the embedding

    :return ndarray: values of the sentence embedding, or returns an array of zeroes
    if no sentence embedding could be computed.
    """
    embed_map: Dict[str, Tuple[np.float64, np.ndarray]] = {
        tmp.string: (
            rescale_idf(word_idf.get(tmp.string.lower(), min_idf), min_idf, max_idf),
            tmp.embedding,
        )
        for tmp in sent.words
        if not np.all((tmp.embedding == 0))  # skip processing empty embeddings
    }
    words: KeysView = embed_map.keys()
    weights_embedds: ValuesView = embed_map.values()
    # We can't create a sentence embedding for just one word
    if len(weights_embedds) < 2:
        return np.zeros(dimensions)
    weights, embedds = zip(*weights_embedds)
    if sum(weights) == 0:
        return np.zeros(dimensions)
    embedds: np.ndarray = remove_pc(np.array(embedds))
    scale_factor: np.float64 = 1 / sum(weights)
    scaled_vals: np.float64 = np.array([tmp * scale_factor for tmp in weights])
    # Apply our weighted terms to the adjusted embeddings
    weighted_embeds: np.ndarray = embedds * scaled_vals[:, None]
    return np.sum(weighted_embeds, axis=0)
