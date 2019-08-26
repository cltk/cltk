"""Operations are distinct NLP algorithms that perform particular
processing for particular languages. Each ``Operation`` is to be used
in the ``Pipeline`` data type. For each ``Operation`` data type,
the two most important attributes are:

1. the particular function which it implements
2. data type required of input
3. data type produced

Inheritance example: ``Operation`` -> ``TokenizationOperation`` -> ``LatinTokenizationOperation``

TODO: Consider creation ``operation.py`` files w/in each dir

TODO: Think about multiple inheritance using the Glottolog codes (changing these from namedtuple to dataclass first)
"""

from dataclasses import dataclass
from typing import Any, Callable, Generic, List

from cltkv1.tokenizers.sentence import DefaultSplitter, LatinSplitter
from cltkv1.tokenizers.word import DefaultTokenizer, LatinTokenizer, dummy_get_token
from cltkv1.utils.data_types import Word


# TODO: Language dataclasses just for illustrating. Re-implement from the Glottolog module.
@dataclass
class Language:
    name: str
    glossolog: str
    latitude: float
    longitude: float
    dates: List[float]
    family_id: str
    parent_id: str
    level: str
    iso639P3code: str
    type: str


LATIN = Language(
    name="Latin",
    glossolog="lati1261",
    latitude=60.2,
    longitude=50.5,
    dates=[200, 400],
    family_id="indo1319",
    parent_id="impe1234",
    level="language",
    iso639P3code="lat",
    type="a",
)

GREEK = Language(
    name="Ancient Greek",
    glossolog="anci1242",
    latitude=10.0,
    longitude=90.5,
    dates=[-1000, 1141],
    family_id="indo1319",
    parent_id="east2798",
    level="language",
    iso639P3code="grc",
    type="h",
)


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
    print(lto.language.glossolog)
