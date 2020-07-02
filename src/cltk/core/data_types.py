"""Custom data types for the CLTK. These types form the building blocks
of the NLP pipeline.


>>> from cltk.core.data_types import Language
>>> from cltk.core.data_types import Word
>>> from cltk.core.data_types import Process
>>> from cltk.core.data_types import Doc
>>> from cltk.core.data_types import Pipeline
"""

from dataclasses import dataclass
from typing import Dict, List, Type

import numpy


@dataclass
class Language:
    """For holding information about any given language. Used to
    encode data from ISO 639-3 and Glottolog at
    ``cltk.lagnuages.glottolog.LANGUAGES`` May be extended by
    user for dialects or languages not documented by ISO 639-3.

    >>> from cltk.core.data_types import Language
    >>> from cltk.languages.utils import get_lang
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

    >>> from cltk.core.data_types import Word
    >>> from cltk.languages.example_texts import get_example_text
    >>> get_example_text("lat")[:25]
    'Gallia est omnis divisa i'
    >>> from cltk.languages.utils import get_lang
    >>> latin = get_lang("lat")
    >>> Word(index_char_start=0, index_char_stop=6, index_token=0, string=get_example_text("lat")[0:6], pos="nom")
    Word(index_char_start=0, index_char_stop=6, index_token=0, index_sentence=None, string='Gallia', pos='nom', lemma=None, scansion=None, xpos=None, upos=None, dependency_relation=None, governor=None, features=None, embedding=None, stop=None, named_entity=None)
    """

    index_char_start: int = None
    index_char_stop: int = None
    index_token: int = None
    index_sentence: int = None
    string: str = None
    pos: str = None
    lemma: str = None
    scansion: str = None
    xpos: str = None  # treebank-specific POS tag (from stanza)
    upos: str = None  # universal POS tag (from stanza)
    dependency_relation: str = None  # (from stanza)
    governor: int = None
    features: Dict[str, str] = None  # morphological features (from stanza)
    embedding: numpy.ndarray = None
    stop: bool = None
    named_entity: bool = None


@dataclass
class Doc:
    """The object returned to the user from the ``NLP()`` class.
    Contains overall attributes of submitted texts, plus most
    importantly the processed tokenized text ``words``,
    being a list of ``Word`` types.

    >>> from cltk import NLP
    >>> from cltk.languages.example_texts import get_example_text
    >>> cltk_nlp = NLP(language="lat")
    >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lat"))
    >>> cltk_doc.raw[:38]
    'Gallia est omnis divisa in partes tres'
    >>> isinstance(cltk_doc.raw, str)
    True
    >>> cltk_doc.tokens[:10]
    ['Gallia', 'est', 'omnis', 'divisa', 'in', 'partes', 'tres', ',', 'quarum', 'unam']
    >>> cltk_doc.tokens_stops_filtered[:10]
    ['Gallia', 'omnis', 'divisa', 'partes', 'tres', ',', 'incolunt', 'Belgae', ',', 'aliam']
    >>> cltk_doc.pos[:3]
    ['NOUN', 'AUX', 'PRON']
    >>> cltk_doc.morphosyntactic_features[:3]
    [{'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, {'Mood': 'Ind', 'Number': 'Sing', 'Person': '3', 'Tense': 'Pres', 'VerbForm': 'Fin', 'Voice': 'Act'}, {'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing', 'PronType': 'Ind'}]
    >>> cltk_doc.lemmata[:5]
    ['mallis', 'sum', 'omnis', 'divido', 'in']
    >>> len(cltk_doc.sentences)
    9
    >>> len(cltk_doc.sentences[0])
    26
    >>> isinstance(cltk_doc.sentences[0][2], Word)
    True
    >>> cltk_doc.sentences[0][2].string
    'omnis'
    >>> len(cltk_doc.sentences_tokens)
    9
    >>> len(cltk_doc.sentences_tokens[0])
    26
    >>> isinstance(cltk_doc.sentences_tokens[0][2], str)
    True
    >>> cltk_doc.sentences_tokens[0][2]
    'omnis'
    >>> len(cltk_doc.sentences_strings)
    9
    >>> len(cltk_doc.sentences_strings[0])
    150
    >>> isinstance(cltk_doc.sentences_strings[0], str)
    True
    >>> cltk_doc.sentences_strings[1]
    'Hi omnes lingua , institutis , legibus inter se differunt .'
    >>> import numpy
    >>> isinstance(cltk_doc.embeddings[1], numpy.ndarray)
    True
    """

    language: str = None
    words: List[Word] = None
    pipeline: "Pipeline" = None
    raw: str = None
    embeddings_model = None

    @property
    def sentences(self) -> List[List[Word]]:
        """Returns a list of lists, with the inner list being a
         list of ``Word`` objects.
        """
        sentences = {}
        for word in self.words:
            sentence = sentences.get(word.index_sentence, {})
            sentence[word.index_token] = word
            sentences[word.index_sentence] = sentence

        sorted_values = lambda dict: [x[1] for x in sorted(dict.items())]

        return [sorted_values(sentence) for sentence in sorted_values(sentences)]

    @property
    def sentences_tokens(self) -> List[List[str]]:
        """Returns a list of lists, with the inner list being a
        list of word token strings.
        """
        sentences_list = self.sentences  # type: List[List[Word]]
        sentences_tokens = list()  # type: List[List[str]]
        for sentence in sentences_list:
            sentence_tokens = [word.string for word in sentence]  # type: List[str]
            sentences_tokens.append(sentence_tokens)
        return sentences_tokens

    @property
    def sentences_strings(self) -> List[str]:
        """Returns a list of strings, with each string being
        a sentence reconstructed from the word tokens.
        """
        sentences_list = self.sentences_tokens  # type: List[List[str]]
        sentences_str = list()  # type: List[List[str]]
        for sentence_tokens in sentences_list:  # type: List[str]
            sentence_tokens_str = " ".join(sentence_tokens)  # type: str
            sentences_str.append(sentence_tokens_str)
        return sentences_str

    def _get_words_attribute(self, attribute):
        return [getattr(word, attribute) for word in self.words]

    @property
    def tokens(self) -> List[str]:
        """Returns a list of string word tokens of all words in the doc."""
        tokens = self._get_words_attribute("string")  # type: List[str]
        return tokens

    @property
    def tokens_stops_filtered(self,) -> List[str]:
        """Returns a list of string word tokens of all words in the
        doc, but with stopwords removed.
        """
        tokens = self._get_words_attribute("string")  # type: List[str]
        # create equal-length list of True & False/None values
        is_token_stop = self._get_words_attribute("stop")  # type: List[bool]
        # remove from the token list any who index in ``is_token_stop`` is True
        tokens_no_stops = [
            token for index, token in enumerate(tokens) if not is_token_stop[index]
        ]  # type: List[str]
        return tokens_no_stops

    @property
    def pos(self) -> List[str]:
        """Returns a list of the POS tags of all words in the doc."""
        return self._get_words_attribute("upos")

    @property
    def morphosyntactic_features(self) -> List[Dict[str, str]]:
        """Returns a list of dictionaries containing the morphosyntactic features
        of each word (when available).
        Each dictionary specifies feature names as keys and feature values as values.
        """
        return self._get_words_attribute("features")

    @property
    def lemmata(self) -> List[str]:
        """Returns a list of lemmata, indexed to the word tokens
        provided by `Doc.tokens`.
        """
        return self._get_words_attribute("lemma")

    def __getitem__(self, word_index: int) -> Word:
        """Indexing operator overloaded to return the `Word` at index `word_index`.
        """
        return self.words[word_index]

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


@dataclass
class Pipeline:
    """Abstract ``Pipeline`` class to be inherited.

    # TODO: Consider adding a Unicode normalization as a default first Process

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.tokenizers import LatinTokenizationProcess
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
