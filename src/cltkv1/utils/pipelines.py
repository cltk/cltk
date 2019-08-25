"""Default processing pipelines for languages."""

from dataclasses import dataclass
from typing import Callable, List

from cltkv1.tokenizers.sentence import DefaultSplitter, LatinSplitter
from cltkv1.tokenizers.word import (
    DefaultTokenizer,
    LatinTokenizer,
    dummy_get_sentence_indices,
    dummy_get_token,
)
from cltkv1.utils.data_types import Doc, Word


@dataclass
class Pipeline:
    sentence_tokenizer: Callable[[str], List[List[int]]] = None
    word_tokenizer: Callable[[str], List[Word]] = None
    dependency: str = None
    pos: str = None
    scansion: Callable[[str], str] = None


@dataclass
class DefaultPipeline(Pipeline):
    sentence_tokenizer = DefaultSplitter().dummy_get_indices
    word_tokenizer = DefaultTokenizer().dummy_get_token_indices


@dataclass
class LatinPipeline(Pipeline):
    sentence_tokenizer = LatinSplitter().dummy_get_indices
    word_tokenizer = LatinTokenizer().dummy_get_token_indices
