"""Custom data types for the CLTK. These types form the building blocks
of the NLP pipeline.


>>> from cltk.core.data_types import Language
>>> from cltk.core.data_types import Word
>>> from cltk.core.data_types import Process
>>> from cltk.core.data_types import Doc
>>> from cltk.core.data_types import Pipeline
"""

import importlib
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, Type, Union

import numpy as np

from cltk.morphology.morphosyntax import MorphosyntacticFeatureBundle
from cltk.morphology.universal_dependencies_features import MorphosyntacticFeature
from cltk.utils import pascal_case

ud_mod = importlib.import_module("cltk.morphology.universal_dependencies_features")


@dataclass(frozen=True)
class Language:
    """For holding information about any given language. Used to
    encode data from ISO 639-3 and Glottolog at
    ``cltk.languages.glottolog.LANGUAGES``. May be extended by
    user for dialects or languages not documented by ISO 639-3.

    >>> from cltk.core.data_types import Language
    >>> from cltk.languages.utils import get_lang
    >>> lat = get_lang("lat")
    >>> isinstance(lat, Language)
    True
    >>> lat
    Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, family_id='indo1319', parent_id='impe1234', level='language', iso_639_3_code='lat', type='a', dates=[])
    """

    name: str  # Glottolog description
    glottolog_id: str
    latitude: float
    longitude: float
    family_id: str  # from Glottolog
    parent_id: str  # from Glottolog
    level: str  # a language or a dialect
    iso_639_3_code: str
    type: str  # "a" for ancient and "h" for historical; this from Glottolog
    dates: list[int] = None  # add later; not available from Glottolog or ISO list


@dataclass
class Word:
    """Contains attributes of each processed word in a list of
    words. Designed to be used in the ``Doc.words`` dataclass.

    >>> from cltk.core.data_types import Word
    >>> Word(index_char_start=0, index_char_stop=6, string="Gallia")
    Word(index_char_start=0, index_char_stop=6, index_token=None, index_sentence=None, string='Gallia', pos=None, lemma=None, stem=None, scansion=None, xpos=None, upos=None, dependency_relation=None, governor=None, features={}, category={}, stop=None, named_entity=None, syllables=None, phonetic_transcription=None, definition=None)

    """

    index_char_start: Optional[int] = None
    index_char_stop: Optional[int] = None
    index_token: Optional[int] = None
    index_sentence: Optional[int] = None
    string: Optional[str] = None
    pos: Optional[MorphosyntacticFeature] = None
    lemma: Optional[str] = None
    stem: Optional[str] = None
    scansion: Optional[str] = None
    xpos: Optional[str] = None  # treebank-specific POS tag (from Stanza or Spacy)
    upos: Optional[str] = None  # universal POS tag (from Stanza or Spacy)
    dependency_relation: Optional[str] = None  # (from Stanza or Spacy)
    governor: Optional[int] = None
    features: MorphosyntacticFeatureBundle = MorphosyntacticFeatureBundle()
    category: MorphosyntacticFeatureBundle = MorphosyntacticFeatureBundle()
    embedding: np.ndarray = field(repr=False, default=None)
    stop: Optional[bool] = None
    named_entity: Optional[bool] = None
    syllables: list[str] = None
    phonetic_transcription: Optional[str] = None
    definition: Optional[str] = None

    def __getitem__(
        self, feature_name: Union[str, Type[MorphosyntacticFeature]]
    ) -> list[MorphosyntacticFeature]:
        """Accessor to help get morphosyntatic features from a word object."""
        return self.features[feature_name]

    def __getattr__(self, item: str):
        """Accessor to help get morphosyntatic features from a word object."""
        feature_name = pascal_case(item)
        if feature_name in ud_mod.__dict__:
            return self.features[feature_name]
        else:
            raise AttributeError(item)


@dataclass
class Sentence:
    """
    The Data Container for sentences.
    """

    words: list[Word] = None
    index: int = None
    embedding: np.ndarray = field(repr=False, default=None)

    def __getitem__(self, item: int) -> Word:
        """This indexing operation descends into the word list structure."""
        return self.words[item]

    def __len__(self) -> int:
        """Returns the number of tokens in the sentence"""
        return len(self.words)


@dataclass
class Doc:
    """The object returned to the user from the ``NLP()`` class.
    Contains overall attributes of submitted texts, plus most
    importantly the processed tokenized text ``words``,
    being a list of ``Word`` types.

    >>> from cltk import NLP
    >>> from cltk.languages.example_texts import get_example_text
    >>> cltk_nlp = NLP(language="lat", suppress_banner=True)
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
    ['NOUN', 'AUX', 'DET']
    >>> cltk_doc.morphosyntactic_features[:3]
    [{Case: [nominative], Gender: [feminine], InflClass: [ind_eur_a], Number: [singular]}, {InflClass: [lat_anom], Number: [singular], VerbForm: [finite]}, {Case: [nominative], Gender: [feminine], InflClass: [ind_eur_i], Number: [singular], PronominalType: [indefinite]}]
    >>> cltk_doc[0].gender
    [feminine]
    >>> cltk_doc[0]['Case']
    [nominative]
    >>> cltk_doc.lemmata[:5]
    ['Gallia', 'sum', 'omnis', 'divisa', 'in']
    >>> len(cltk_doc.sentences)
    9
    >>> len(cltk_doc.sentences[0])
    26
    >>> type(cltk_doc.sentences[0][2])
    <class 'cltk.core.data_types.Word'>
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
    >>> import numpy as np
    >>> isinstance(cltk_doc.embeddings[1], np.ndarray)
    True
    """

    language: str = None
    words: list[Word] = None
    pipeline: "Pipeline" = None  # Note: type should be ``Pipeline`` w/o quotes
    raw: str = None
    normalized_text: str = None
    embeddings_model = None
    sentence_embeddings: dict[int, np.ndarray] = field(repr=False, default=None)

    @property
    def sentences(self) -> list[Sentence]:
        """Returns a list of ``Sentence``s, with each ``Sentence`` being a container for a
        list of ``Word`` objects."""
        sents: dict[int, list[Word]] = defaultdict(list)
        for word in self.words:
            sents[word.index_sentence].append(word)
        for key in sents:
            for w in sents[key]:
                if w.index_token is None:
                    raise ValueError(f"Index token is not defined for {w.string}")

        for key in sents:
            sents[key].sort(key=lambda x: x.index_token)
        # Sometimes not available, nor initialized; e.g. stanza
        if not self.sentence_embeddings:
            self.sentence_embeddings = dict()
        return [
            Sentence(words=val, index=key, embedding=self.sentence_embeddings.get(key))
            for key, val in sorted(sents.items(), key=lambda x: x[0])
        ]

    @property
    def sentences_tokens(self) -> list[list[str]]:
        """Returns a list of lists, with the inner list being a
        list of word token strings.
        """
        sentences_tokens: list[list[str]] = list()
        for sentence in self.sentences:
            sentence_tokens: list[str] = [word.string for word in sentence]
            sentences_tokens.append(sentence_tokens)
        return sentences_tokens

    @property
    def sentences_strings(self) -> list[str]:
        """Returns a list of strings, with each string being
        a sentence reconstructed from the word tokens.
        """
        sentences_list: list[list[str]] = self.sentences_tokens
        sentences_str: list[str] = list()
        for sentence_tokens in sentences_list:  # type: list[str]
            if self.language == "akk":
                # 'akk' produces list[tuple[str, str]]
                sentence_tokens_str = " ".join([tup[0] for tup in sentence_tokens])
            else:
                sentence_tokens_str: str = " ".join(sentence_tokens)
            sentences_str.append(sentence_tokens_str)
        return sentences_str

    def _get_words_attribute(self, attribute):
        return [getattr(word, attribute) for word in self.words]

    @property
    def tokens(self) -> list[str]:
        """Returns a list of string word tokens of all words in the doc."""
        tokens = self._get_words_attribute("string")
        return tokens

    @property
    def tokens_stops_filtered(
        self,
    ) -> list[str]:
        """Returns a list of string word tokens of all words in the
        doc, but with stopwords removed.
        """
        tokens: list[str] = self._get_words_attribute("string")
        # create equal-length list of True & False/None values
        is_token_stop: list[bool] = self._get_words_attribute("stop")
        # remove from the token list any who index in ``is_token_stop`` is True
        tokens_no_stops: list[str] = [
            token for index, token in enumerate(tokens) if not is_token_stop[index]
        ]
        return tokens_no_stops

    @property
    def pos(self) -> list[str]:
        """Returns a list of the POS tags of all words in the doc."""
        return self._get_words_attribute("upos")

    @property
    def morphosyntactic_features(self) -> list[MorphosyntacticFeatureBundle]:
        """Returns a list of `MorphosyntacticFeatureBundle` containing the morphosyntactic features
        of each word (when available).
        """
        return self._get_words_attribute("features")

    @property
    def lemmata(self) -> list[str]:
        """Returns a list of lemmata, indexed to the word tokens
        provided by `Doc.tokens`.
        """
        return self._get_words_attribute("lemma")

    @property
    def stems(self) -> list[str]:
        """Returns a list of word stems, indexed to the word tokens
        provided by `Doc.tokens`.
        """
        stems = self._get_words_attribute("stem")
        return stems

    def __getitem__(self, word_index: int) -> Word:
        """Indexing operator overloaded to return the `Word` at index `word_index`."""
        return self.words[word_index]

    @property
    def embeddings(self):
        """Returns an embedding for each word.

        TODO: Consider option to use lemma
        """
        return self._get_words_attribute("embedding")


@dataclass
class Process(ABC):
    """For each type of NLP process there needs to be a definition.
    It includes the type of data it expects (``str``, ``list[str]``,
    ``Word``, etc.) and what field within ``Word`` it will populate.
    This base class is intended to be inherited by NLP process
    types (e.g., ``TokenizationProcess`` or ``DependencyProcess``).

    """

    language: str = None

    @abstractmethod
    def run(self, input_doc: Doc) -> Doc:
        pass


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
    processes: list[Type[Process]]
    language: Language

    def add_process(self, process: Type[Process]):
        self.processes.append(process)
