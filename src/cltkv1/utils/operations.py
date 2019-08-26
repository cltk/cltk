"""Operations are distinct NLP algorithms that perform particular
processing for particular languages. Each ``Operation`` is to be used
in the ``Pipeline`` data type. For each ``Operation`` data type,
the two most important attributes are:

1. the particular function which it implements
2. data type required of input
3. data type produced

Inheritance example: ``Operation`` -> ``TokenizationOperation`` -> ``LatinTokenizationOperation``
"""

from dataclasses import dataclass
from typing import Any, Callable, Generic, List

from cltkv1.languages.glottolog import GREEK, LATIN
from cltkv1.tokenizers.sentence import DefaultSplitter, LatinSplitter
from cltkv1.tokenizers.word import DefaultTokenizer, LatinTokenizer, dummy_get_token
from cltkv1.utils.data_types import Word


@dataclass
class Operation:
    """For each type of NLP operation there needs to be a definition.
    It includes the type of data it expects (``str``, ``List[str]``,
    ``Word``, etc.) and what field withing ``Word`` it will populate.
    This base class is intended to be inherited by NLP operation
    types (e.g., ``TokenizationOperation`` or ``DependencyOperation``).
    """

    name: str
    description: str
    input: Any
    output: Any
    algorithm: Callable
    type: str


@dataclass
class TokenizationOperation(Operation):
    """To be inherited for each language's tokenization declaration.

    Example: ``TokenizationOperation`` -> ``LatinTokenizationOperation``
    """

    type = "tokenization"


@dataclass
class LatinTokenizationOperation(TokenizationOperation):
    """The default Latin tokenization algorithm"""

    name = "CLTK Dummy Latin Tokenizer"
    description = "This is a simple regex which divides on word spaces (``r'\w+)`` for illustrative purposes."
    input = str
    output = List[List[int]]
    algorithm = LatinTokenizer.dummy_get_token_indices
    language = LATIN


@dataclass
class DefaultTokenizationOperation(TokenizationOperation):
    """The default Latin tokenization algorithm"""

    name = "CLTK Dummy Tokenizer for any language"
    description = "This is a simple regex which divides on word spaces (``r'\w+)`` for illustrative purposes."
    input = str
    output = List[List[int]]
    algorithm = DefaultTokenizer.dummy_get_token_indices
    language = None


if __name__ == "__main__":
    lto = LatinTokenizationOperation
    print(lto.__dict__.keys())
    print(lto.name)
    print(lto.description)
    print(lto.language)
    print(lto.language.name)
    print(lto.language.latitude)
    print(lto.language.glottocode)
