"""Custom data types for the CLTK. These types form the building blocks
of the NLP pipeline.


>>> from cltkv1.core.data_types import Language
>>> from cltkv1.core.data_types import Word
>>> from cltkv1.core.data_types import Process
>>> from cltkv1.core.data_types import Doc
>>> from cltkv1.core.data_types import Pipeline
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Type, Union

import numpy


@dataclass
class Language:
    """For holding information about any given language. Used to
    encode data from ISO 639-3 and Glottolog at
    ``cltkv1.lagnuages.glottolog.LANGUAGES`` May be extended by
    user for dialects or languages not documented by ISO 639-3.

    >>> from cltkv1.core.data_types import Language
    >>> from cltkv1.languages.utils import get_lang
    >>> latin = get_lang("lat")
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

    >>> from cltkv1.core.data_types import Word
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> get_example_text("lat")[:25]
    'Gallia est omnis divisa i'
    >>> from cltkv1.languages.utils import get_lang
    >>> latin = get_lang("lat")
    >>> Word(index_char_start=0, index_char_stop=6, index_token=0, string=get_example_text("lat")[0:6], pos="nom")
    Word(index_char_start=0, index_char_stop=6, index_token=0, index_sentence=None, string='Gallia', pos='nom', lemma=None, scansion=None, xpos=None, upos=None, dependency_relation=None, governor=None, parent=None, features=None, embedding=None)
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
    governor: "Word" = None
    parent: "Word" = None
    features: Dict[str, str] = None  # morphological features (from stanfordnlp)
    embedding: numpy.ndarray = None
    stop: bool = None


@dataclass
class Doc:
    """The object returned to the user from the ``NLP()`` class.
    Contains overall attributes of submitted texts, plus most
    importantly the processed tokenized text ``words``,
    being a list of ``Word`` types.

    >>> from cltkv1 import NLP
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> cltk_nlp = NLP(language="lat")
    >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lat"))
    >>> cltk_doc.raw[:38]
    'Gallia est omnis divisa in partes tres'
    >>> isinstance(cltk_doc.raw, str)
    True
    """

    language: str = None
    words: List[Word] = None
    pipeline: "Pipeline" = None
    raw: str = None
    embeddings_model = None

    @property
    def sentences(self) -> List[List[Word]]:
        sentences = {}
        for word in self.words:
            sentence = sentences.get(word.index_sentence, {})
            sentence[word.index_token] = word
            sentences[word.index_sentence] = sentence

        sorted_values = lambda dict: [x[1] for x in sorted(dict.items())]

        return [sorted_values(sentence) for sentence in sorted_values(sentences)]

    def _get_words_attribute(self, attribute):
        return [getattr(word, attribute) for word in self.words]

    @property
    def tokens(self) -> List[str]:
        """Returns a list of string word tokens of all words in the doc.

        TODO: Add option to filter stopwords.

        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.example_texts import get_example_text
        >>> cltk_nlp = NLP(language="lat")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lat"))
        >>> cltk_doc.tokens[:10]
        ['Gallia', 'est', 'omnis', 'divisa', 'in', 'partes', 'tres', ',', 'quarum', 'unam']
        """
        return self._get_words_attribute("string")

    @property
    def pos(self) -> List[str]:
        """Returns a list of the POS tags of all words in the doc.

        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.example_texts import get_example_text
        >>> cltk_nlp = NLP(language="lat")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lat"))
        >>> cltk_doc.pos[:3]
        ['NOUN', 'AUX', 'DET']
        """
        return self._get_words_attribute("upos")

    @property
    def morphosyntactic_features(self) -> Dict[str, str]:
        """Returns a list of dictionaries containing the morphosyntactic features
        of each word (when available).
        Each dictionary specifies feature names as keys and feature values as values.

        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.example_texts import get_example_text
        >>> cltk_nlp = NLP(language="lat")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lat"))
        >>> cltk_doc.morphosyntactic_features[:3]
        [{'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, {'Mood': 'Ind', 'Number': 'Sing', 'Person': '3', 'Tense': 'Pres', 'VerbForm': 'Fin', 'Voice': 'Act'}, {'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing', 'PronType': 'Ind'}]
        """
        return self._get_words_attribute("features")

    @property
    def lemmata(self) -> List[str]:
        """Returns a list of lemmata, indexed to the word tokens
        provided by `Doc.tokens`.

        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.example_texts import get_example_text
        >>> cltk_nlp = NLP(language="lat")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lat"))
        >>> cltk_doc.lemmata[:5]
        ['aallius', 'sum', 'omnis', 'divido', 'in']
        """
        return self._get_words_attribute("lemma")

    @property
    def embeddings(self):
        """Returns an embedding for each word.

        TODO: Consider option to use lemma
        """
        return self._get_words_attribute("embedding")


@dataclass
class Process:
    """For each type of NLP process there needs to be a definition.
    It includes the type of data it expects (``str``, ``List[str]``,
    ``Word``, etc.) and what field within ``Word`` it will populate.
    This base class is intended to be inherited by NLP process
    types (e.g., ``TokenizationProcess`` or ``DependencyProcess``).

    >>> a_process = Process(input_doc=Doc(raw="input words here"))
    """

    input_doc: Doc
    output_doc: Doc = None

    # def run(self) -> None:
    #     """Method for subclassed ``Process`` Run ``algorithm`` on a
    #     ``Doc`` object to set ``output_doc`` to the resulting ``Doc```.
    #
    #     This method puts execution of the process into the hands of the client.
    #     It must be called before reading the ``output_doc`` attribute.
    #
    #     >>> a_process = Process(input_doc=Doc(raw="input words here"))
    #     >>> a_process.run()
    #     Traceback (most recent call last):
    #       ...
    #     NotImplementedError
    #     """
    #     if self.algorithm:
    #         self.output_doc = self.algorithm(self.input_doc)
    #     else:
    #         raise NotImplementedError


@dataclass
class Pipeline:
    """Abstract ``Pipeline`` class to be inherited.

    # TODO: Consider adding a Unicode normalization as a default first Process

    >>> from cltkv1.core.data_types import Process, Pipeline
    >>> from cltkv1.languages.utils import get_lang
    >>> from cltkv1.tokenizers import LatinTokenizationProcess
    >>> a_pipeline = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess], language=get_lang("lat"))
    >>> a_pipeline.description
    'A custom Latin pipeline'
    >>> issubclass(a_pipeline.processes[0], Process)
    True
    """

    description: str
    processes: List[Type[Process]]
    language: Language

    def add_process(self, process):
        self.processes.append(process)


if __name__ == "__main__":
    doc = Doc(language="lat", words=["amo", "amas", "amat"], raw="amo amas amat")
    print(doc)
    print(doc.embeddings)
