"""Custom data types for the CLTK. These types form the building blocks
of the NLP pipeline.


>>> from cltkv1.utils.data_types import Language
>>> from cltkv1.utils.data_types import Word
>>> from cltkv1.utils.data_types import Process
>>> from cltkv1.utils.data_types import MultiProcess
>>> from cltkv1.utils.data_types import Doc
>>> from cltkv1.utils.data_types import Pipeline
"""

from dataclasses import dataclass
from typing import Any, Callable, List, Type, Union


@dataclass
class Language:
    """For holding information about any given language. Used to
    encode data from ISO 639-3 and Glottolog at
    ``cltkv1.lagnuages.glottolog.LANGUAGES`` May be extended by
    user for dialects or languages not documented by ISO 639-3.

    >>> from cltkv1.utils.data_types import Language
    >>> from cltkv1.languages.glottolog import LANGUAGES
    >>> latin = LANGUAGES["lat"]
    >>> isinstance(latin, Language)
    True
    >>> latin
    Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, dates=[], family_id='indo1319', parent_id='impe1234', level='language', iso_639_3_code='lat', type='a')
    """

    name: str  # Glottolog description
    glottolog_id: str
    latitude: float
    longitude: float
    dates: List[int]  # add later; not available from Glottolog or ISO list
    family_id: str  # from Glottolog
    parent_id: str  # from Glottolog
    level: str  # a language or a dialect
    iso_639_3_code: str
    type: str  # "a" for ancient and "h" for historical; this from Glottolog


@dataclass
class Word:
    """Contains attributes of each processed word in a list of
    words. Designed to be used in the ``Doc.words`` dataclass.

    >>> from cltkv1.utils.data_types import Word
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> EXAMPLE_TEXTS["lat"][:25]
    'Gallia est omnis divisa i'
    >>> from cltkv1.languages.glottolog import LANGUAGES
    >>> latin = LANGUAGES["lat"]
    >>> Word(index_char_start=0, index_char_stop=6, index_token=0, string=EXAMPLE_TEXTS["lat"][0:6], pos="nom")
    Word(index_char_start=0, index_char_stop=6, index_token=0, index_sentence=None, string='Gallia', pos='nom', lemma=None, scansion=None, xpos=None, upos=None, dependency_relation=None, governor=None, parent_token=None, feats=None)
    """

    index_char_start: int = None
    index_char_stop: int = None
    index_token: int = None
    index_sentence: int = None
    string: str = None
    pos: str = None
    lemma: str = None
    scansion: str = None
    xpos: str = None  # treebank-specific POS tag (from stanfordnlp)
    upos: str = None  # universal POS tag (from stanfordnlp)
    dependency_relation: str = None  # (from stanfordnlp)
    governor: str = None  # (from stanfordnlp)
    parent_token: str = None  # (from stanfordnlp)
    feats: str = None  # morphological features (from stanfordnlp)


@dataclass
class Process:
    """For each type of NLP process there needs to be a definition.
    It includes the type of data it expects (``str``, ``List[str]``,
    ``Word``, etc.) and what field within ``Word`` it will populate.
    This base class is intended to be inherited by NLP process
    types (e.g., ``TokenizationProcess`` or ``DependencyProcess``).

    >>> a_process = Process(data_input="input words here")
    """

    data_input: Union[str, List[str]]
    algorithm = None
    language = None

    @property
    def data_output(self) -> Any:
        """Attribute for subclassed ``Process`` objects to return
        ``data_input`` that has been processed by the ``algorithm``.

        >>> a_process = Process(data_input="input words here")
        >>> a_process.data_output
        Traceback (most recent call last):
          ...
        NotImplementedError
        """
        if self.algorithm:
            return self.algorithm(self.data_input)
        raise NotImplementedError


@dataclass
class MultiProcess(Process):
    """A class to be called directly or inherited from when
    a particular NLP algo does more than one process, such
    as tokenization and tagging together.

    >>> def multi_fn(_str: str) -> List[str]:    return _str.upper().split()
    >>> a_multi_process = MultiProcess(data_input="Some words for processing.", algorithm=multi_fn)
    >>> a_multi_process.data_output
    ['SOME', 'WORDS', 'FOR', 'PROCESSING.']
    """

    algorithm: Callable


@dataclass
class Doc:
    """The object returned to the user from the ``NLP()`` class.
    Contains overall attributes of submitted texts, plus most
    importantly the processed tokenized text ``words``,
    being a list of ``Word`` types.
    """

    indices_sentences: List[List[int]] = None
    indices_tokens: List[List[int]] = None
    language: str = None
    words: List[Word] = None
    pipeline: List[Process] = None
    raw: str = None


@dataclass
class Pipeline:
    """Abstract ``Pipeline`` class to be inherited.

    # TODO: Consider adding a Unicode normalization as a default first Process

    >>> from cltkv1.utils.data_types import Process, Pipeline
    >>> from cltkv1.languages.glottolog import LANGUAGES
    >>> from cltkv1.tokenizers import LatinTokenizationProcess
    >>> a_pipeline = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess], language=LANGUAGES["lat"])
    >>> a_pipeline.description
    'A custom Latin pipeline'
    >>> issubclass(a_pipeline.processes[0], Process)
    True
    """

    description: str
    processes: List[Type[Process]]
    language: Language
