"""For computing embeddings for lists of words."""

from typing import Dict, List, Tuple, Union, ValuesView

import numpy as np
from sklearn.decomposition import TruncatedSVD

from cltk.core import Sentence


def rescale_idf(val: float, min_idf: float, max_idf: float) -> float:
    """Rescale idf values."""
    return (val - min_idf) / (max_idf - min_idf)


def compute_pc(x: np.ndarray, npc: int = 1) -> np.ndarray:
    """Compute the principal components. DO NOT MAKE THE DATA ZERO MEAN!

    :param x: X[i,:] is a data point
    :param npc: number of principal components to remove
    :return: component_[i,:] is the i-th pc

    This has been adapted from the SIF paper code: `https://openreview.net/pdf?id=SyK00v5xx`.
    """
    svd: TruncatedSVD = TruncatedSVD(n_components=npc, n_iter=7, random_state=0)
    svd.fit(x)
    return svd.components_


def remove_pc(x: np.ndarray, npc: int = 1) -> np.ndarray:
    """Remove the projection on the principal components. Calling this on a collection of sentence embeddings, prior to comparison, may improve accuracy.

    :param x: X[i,:] is a data point
    :param npc: number of principal components to remove
    :return: XX[i, :] is the data point after removing its projection

    This has been adapted from the SIF paper code: `https://openreview.net/pdf?id=SyK00v5xx`.
    """
    pc: np.ndarray = compute_pc(x, npc)
    if npc == 1:
        xx: np.ndarray = x - x.dot(pc.transpose()) * pc
    else:
        xx: np.ndarray = x - x.dot(pc.transpose()).dot(pc)
    return xx


def get_sent_embeddings(
    sent: Sentence,
    idf_model: Dict[str, Union[float, np.float64]],
    min_idf: Union[float, np.float64],
    max_idf: Union[float, np.float64],
    dimensions: int = 300,
) -> np.ndarray:
    """Provides the weighted average of a sentence's word vectors.

    Expectations:
    Word can only appear once in a sentence, multiple occurrences are collapsed.
    Must have 2 or more embeddings, otherwise Principle Component cannot be found and removed.

    :param sent: ``Sentence``
    :param idf_model: a dictionary of tokens and idf values
    :param min_idf: the min idf score to use for scaling
    :param max_idf: the max idf score to use for scaling
    :param dimensions: the number of dimensions of the embedding

    :return ndarray: values of the sentence embedding, or returns an array of zeroes if no sentence embedding could be computed.
    """
    map_word_embedding: Dict[str, Tuple[np.float64, np.ndarray]] = {
        token.string: (
            rescale_idf(idf_model.get(token.string.lower(), min_idf), min_idf, max_idf),
            token.embedding,
        )
        for token in sent.words
        if not np.all((token.embedding == 0))  # skip processing empty embeddings
    }
    weight_embedding_tuple: ValuesView = map_word_embedding.values()
    # We can't create a sentence embedding for just one word
    if len(weight_embedding_tuple) < 2:
        return np.zeros(dimensions)
    weights, embeddings = zip(*weight_embedding_tuple)
    if sum(weights) == 0:
        return np.zeros(dimensions)
    scale_factor: np.float64 = 1 / sum(weights)
    scaled_weights: List[np.float64] = [weight * scale_factor for weight in weights]
    scaled_values: np.ndarray = np.array(scaled_weights)
    # Apply our weighted terms to the adjusted embeddings
    weighted_embeds: np.ndarray = embeddings * scaled_values[:, None]
    return np.sum(weighted_embeds, axis=0)
