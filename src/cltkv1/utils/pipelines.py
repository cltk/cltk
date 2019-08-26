"""Default processing pipelines for languages. The purpose of
these dataclasses is to represent:

1. the types of NLP operations that the CLTK can do
2. the order in which operations are to be executed
3. specifying what downstream features a particular implemented operation requires
"""

from dataclasses import dataclass
from typing import Callable, List

from cltkv1.tokenizers.sentence import DefaultSplitter, LatinSplitter
from cltkv1.tokenizers.word import DefaultTokenizer, LatinTokenizer, dummy_get_token
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


if __name__ == "__main__":
    # pipeline = Pipeline
    # print(pipeline.sentence_tokenizer)

    gen_pipe = DefaultPipeline
    fn_sent_tok = gen_pipe.sentence_tokenizer
    fn_word_tok = gen_pipe.word_tokenizer

    old_norse_volupsa = "Hljóðs bið ek allar helgar kindir, meiri ok minni mögu Heimdallar; viltu, at ek, Valföðr. vel framtelja forn spjöll fíra, þau er fremst um man."
    sent_ind = fn_sent_tok(old_norse_volupsa)
    print(sent_ind)

    gesta_danorum = (
        "Malo præterea virum regnare quam patrem. Malo regis coniunx quam nata censeri."
    )
    tok_ind = fn_word_tok(gesta_danorum)
    print(tok_ind)
