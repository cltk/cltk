"""Default processing pipelines for languages."""

from dataclasses import dataclass
from typing import Callable, List

from cltkv1.tokenizers.tokenizers import _dummy_get_sentence_indices, _dummy_get_token
from cltkv1.utils.cltk_dataclasses import Text, Word


@dataclass
class Pipeline:
    sentence_tokenizer: Callable[[str], List[List[int]]] = None
    word_tokenizer: Callable[[str], List[Word]] = None
    dependency: str = None
    pos: str = None
    scansion: Callable[[str], str] = None


@dataclass
class GenericPipeline(Pipeline):
    sentence_tokenizer = _dummy_get_sentence_indices
    word_tokenizer = _dummy_get_token


@dataclass
class LatinPipeline(Pipeline):
    sentence_tokenizer = _dummy_get_sentence_indices
    word_tokenizer = _dummy_get_token
