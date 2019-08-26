"""Default processing pipelines for languages. The purpose of
these dataclasses is to represent:

1. the types of NLP operations that the CLTK can do
2. the order in which operations are to be executed
3. specifying what downstream features a particular implemented operation requires
"""

from dataclasses import dataclass
from typing import Callable, List

from cltkv1.utils.data_types import Doc, Word
from cltkv1.utils.operations import (
    GREEK,
    LATIN,
    DefaultTokenizationOperation,
    LatinTokenizationOperation,
)


@dataclass
class Pipeline:
    sentence_splitter: Callable[[str], List[List[int]]] = None
    word_tokenizer: Callable[[str], List[Word]] = None
    dependency: str = None
    pos: str = None
    scansion: Callable[[str], str] = None


@dataclass
class DefaultPipeline(Pipeline):
    # sentence_splitter = DefaultSplitter().dummy_get_indices
    # word_tokenizer =
    pass


@dataclass
class LatinPipeline(Pipeline):
    # sentence_splitter = LatinSplitter().dummy_get_indices
    word_tokenizer = LatinTokenizationOperation
    language = LATIN


@dataclass
class GreekPipeline(Pipeline):
    # sentence_splitter = DefaultSplitter().dummy_get_indices
    word_tokenizer = DefaultTokenizationOperation
    language = GREEK


if __name__ == "__main__":

    # latin
    gesta_danorum = (
        "Malo præterea virum regnare quam patrem. Malo regis coniunx quam nata censeri."
    )

    lat_pipeline = LatinPipeline
    lat_fn_word_tok = lat_pipeline.word_tokenizer
    print("Algo:", lat_fn_word_tok.algorithm)
    print("In:", lat_fn_word_tok.input)
    print("Out:", lat_fn_word_tok.output)

    idx_tokens = lat_fn_word_tok.algorithm(gesta_danorum)
    print("Words:", idx_tokens)
