"""Core data models used throughout CLTK.

This module defines small, typed Pydantic models for linguistic metadata
and the main runtime containers (``Word``, ``Sentence``, ``Doc``), along with
lightweight abstractions for ``Process`` and ``Pipeline``. These types are the
building blocks of the NLP pipeline and are designed to be simple to serialize
and render well in documentation.
"""

from abc import abstractmethod
from datetime import date
from typing import Any, Literal, Optional, TypeAlias, Union

import numpy as np
from pydantic import AnyUrl, BaseModel, Field, model_validator

from cltk.core.cltk_logger import logger
from cltk.morphosyntax.ud_deprels import UDDeprelTag
from cltk.morphosyntax.ud_features import UDFeatureTagSet
from cltk.morphosyntax.ud_pos import UDPartOfSpeechTag

# --- Type aliases (mark with TypeAlias to appease linters/IDEs) ---------------
Level: TypeAlias = Literal["family", "language", "dialect"]
Status: TypeAlias = Literal[
    "living", "extinct", "second language only", "artificial", "unattested", "unknown"
]
Macroarea: TypeAlias = Literal[
    "Africa",
    "Eurasia",
    "Papunesia",
    "Australia",
    "North America",
    "South America",
    "Antarctica",
]
ISOType: TypeAlias = Literal["639-1", "639-2", "639-3"]
# left-to-right, right-to-left, top-to-bottom, bottom-to-top
ScriptDir: TypeAlias = Literal["ltr", "rtl", "ttb", "btt"]


class CLTKGenAIResponse(BaseModel):
    """Response model for generative backend interactions (OpenAI/Ollama).

    Attributes:
      response: The generated text returned by the LLM.
      usage: Token usage information (input, output, total) when available.

    """

    response: str
    usage: dict[str, int]


class NameVariant(BaseModel):
    """Alternative name or label for a language or dialect.

    Attributes:
      value: The display string for the name.
      source: Optional provenance or catalogue name.
      script: Optional script tag (e.g., ISO 15924).

    """

    value: str
    source: Optional[str] = None
    script: Optional[str] = None


class Identifier(BaseModel):
    """External identifier record.

    Attributes:
      scheme: Identifier scheme (e.g., ``glottocode``, ``iso639-3``).
      value: Identifier value.

    """

    scheme: str
    value: str


class GeoPoint(BaseModel):
    """Geographic point in decimal degrees."""

    lat: float
    lon: float


class GeoArea(BaseModel):
    """Geographic coverage for a language or dialect."""

    centroid: Optional[GeoPoint] = None
    macroareas: list[Macroarea] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)


class Timespan(BaseModel):
    """Approximate temporal coverage for a resource or orthography."""

    start: Optional[int] = None
    end: Optional[int] = None
    note: Optional[str] = None


class SourceRef(BaseModel):
    """Bibliographic source/citation reference."""

    key: str
    pages: Optional[str] = None
    note: Optional[str] = None
    url: Optional[AnyUrl] = None


class Classification(BaseModel):
    """Taxonomic/phylogenetic information for a language."""

    level: Level
    parent_glottocode: Optional[str] = None
    lineage: list[str] = Field(default_factory=list)  # ancestors (root-first)
    children_glottocodes: list[str] = Field(default_factory=list)


class Endangerment(BaseModel):
    """Endangerment status summary (if available)."""

    status: Optional[str] = None
    source: Optional[str] = None
    date_assessed: Optional[date] = None
    note: Optional[str] = None


class Link(BaseModel):
    """External hyperlink with title."""

    title: str
    url: AnyUrl


class TransliterationSystem(BaseModel):
    """Transliteration scheme description and provenance."""

    name: str
    standard_body: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    sources: list[SourceRef] = Field(default_factory=list)


class Orthography(BaseModel):
    """Orthography used for a language/dialect in a given period/region."""

    name: str
    script: str
    direction: Optional[ScriptDir] = None
    period: Optional[Timespan] = None
    region: Optional[str] = None
    description: Optional[str] = None
    conventions: list[str] = Field(default_factory=list)
    transliteration: list[TransliterationSystem] = Field(default_factory=list)
    sample: Optional[str] = None
    sources: list[SourceRef] = Field(default_factory=list)
    links: list[Link] = Field(default_factory=list)


class Dialect(BaseModel):
    """Dialect metadata record from Glottolog‑derived data."""

    glottolog_id: str
    language_code: str
    name: str
    status: Status = "unknown"
    alt_names: list[NameVariant] = Field(default_factory=list)
    identifiers: list[Identifier] = Field(default_factory=list)
    geo: Optional[GeoArea] = None
    timespan: Optional[Timespan] = None
    scripts: list[str] = Field(default_factory=list)
    orthographies: list[Orthography] = Field(default_factory=list)
    sources: list[SourceRef] = Field(default_factory=list)
    links: list[Link] = Field(default_factory=list)


class Language(BaseModel):
    """Language metadata record from Glottolog‑derived data."""

    name: str
    glottolog_id: str
    identifiers: list[Identifier] = Field(default_factory=list)
    level: Level
    status: Status = "unknown"
    type: Optional[str] = None

    geo: Optional[GeoArea] = None
    timespan: Optional[Timespan] = None

    classification: Classification
    family_id: Optional[str] = None
    parent_id: Optional[str] = None

    iso: Optional[str] = None
    iso_set: dict[ISOType, str] = Field(default_factory=dict)
    alt_names: list[NameVariant] = Field(default_factory=list)

    scripts: list[str] = Field(default_factory=list)
    orthographies: list[Orthography] = Field(default_factory=list)

    sources: list[SourceRef] = Field(default_factory=list)
    links: list[Link] = Field(default_factory=list)

    dialects: list[Dialect] = Field(default_factory=list)
    default_variety_id: Optional[str] = None

    glottolog_version: Optional[str] = None
    commit_sha: Optional[str] = None
    last_updated: Optional[date] = None

    endangerment: Optional[Endangerment] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None
    dates: list[int] = Field(default_factory=list)

    newick: Optional[str] = None


class CLTKBaseModel(BaseModel):
    """Base Pydantic model for CLTK runtime containers."""

    model_config = {"arbitrary_types_allowed": True}


class Word(CLTKBaseModel):
    """Contains attributes of each processed word in a list of words."""

    index_char_start: Optional[int] = None
    index_char_stop: Optional[int] = None
    index_token: Optional[int] = None
    index_sentence: Optional[int] = None
    string: Optional[str] = None
    # pos: Optional[MorphosyntacticFeature] = None
    lemma: Optional[str] = None
    upos: Optional[UDPartOfSpeechTag] = None
    features: Optional[UDFeatureTagSet] = None
    dependency_relation: Optional[UDDeprelTag] = None
    governor: Optional[int] = None
    stem: Optional[str] = None
    scansion: Optional[str] = None
    xpos: Optional[str] = None
    embedding: Optional[np.ndarray] = None
    stop: Optional[bool] = None
    named_entity: Optional[str] = None
    syllables: Optional[list[str]] = Field(default_factory=list)
    phonetic_transcription: Optional[str] = None
    definition: Optional[str] = None

    # def __getitem__(self, feature_name: Union[str, type[MorphosyntacticFeature]]) -> list[MorphosyntacticFeature]:
    #     return self.features[feature_name]

    # def __getattr__(self, item: str):
    #     feature_name = pascal_case(item)
    #     if feature_name in ud_mod.__dict__:
    #         return self.features[feature_name]
    #     else:
    #         raise AttributeError(item)


class Sentence(CLTKBaseModel):
    """A sentence containing words and optional embedding."""

    words: Optional[list[Word]] = Field(default_factory=list)
    index: Optional[int] = None
    embedding: Optional[np.ndarray] = None

    # def __getitem__(self, item: int) -> Word:
    #     if not self.words:
    #         raise IndexError("No words in sentence.")
    #     return self.words[item]

    # def __len__(self) -> int:
    #     if not self.words:
    #         return 0
    #     return len(self.words)


BACKEND_TYPES: TypeAlias = Literal[
    "openai", "stanza", "spacy", "ollama", "ollama-cloud"
]
AVAILABLE_OPENAI_MODELS: TypeAlias = Literal["gpt-5-mini", "gpt-5"]


class Doc(CLTKBaseModel):
    """Top‑level container returned from ``NLP()`` pipelines.

    Attributes:
      language: Language metadata associated with the text.
      words: Token‑level annotations (may be empty prior to analysis).
      pipeline: Pipeline instance that produced this document, if any.
      raw: Original raw text.
      normalized_text: Normalized version of the text.
      sentence_embeddings: Optional embeddings per sentence index.
      translation: Optional translation of the document.
      summary: Optional summary of the document.
      topic: Optional topic classification.
      discourse_relations: Discourse relation labels (if available).
      coreferences: Coreference links as (mention, antecedent, i, j).
      sentence_boundaries: List of (start, stop) character offsets.
      openai: List of usage/metadata dicts from model calls.

    """

    language: Language
    words: list[Word] = Field(default_factory=list)
    pipeline: Optional["Pipeline"] = None
    raw: Optional[str] = None
    normalized_text: Optional[str] = None
    embeddings_model: Optional[Any] = None
    sentence_embeddings: dict[int, np.ndarray] = Field(default_factory=dict)
    translation: Optional[str] = None
    summary: Optional[str] = None
    topic: Optional[str] = None
    discourse_relations: list[str] = Field(default_factory=list)
    coreferences: list[tuple[str, str, int, int]] = Field(default_factory=list)
    sentence_boundaries: list[tuple[int, int]] = Field(default_factory=list)
    openai: list[dict[str, Any]] = Field(default_factory=list)
    backend: Optional[BACKEND_TYPES] = None
    # Model alias/name for the selected backend. For OpenAI this should be
    # one of AVAILABLE_OPENAI_MODELS; for Ollama any model string is accepted.
    model: Optional[Union[BACKEND_TYPES, str]] = None
    dialect: Optional[Dialect] = None

    @property
    def sentence_strings(self) -> list[str]:
        """Return sentence strings derived from boundaries and text.

        Returns:
          A list of substrings of ``normalized_text`` cut by
          ``sentence_boundaries``. Returns an empty list if either field is
          missing.

        """
        # TODO: Decide if this is preventable
        from cltk.sentence.utils import extract_sentences_from_boundaries

        if not self.normalized_text or not self.sentence_boundaries:
            logger.warning(
                "`Doc.normalized_text` or `.sentence_boundaries` is empty, cannot return sentence strings."
            )
            return []
        return extract_sentences_from_boundaries(
            self.normalized_text, self.sentence_boundaries
        )

    # @property
    # def sentences(self) -> list[Sentence]:
    #     if not self.words:
    #         return []
    #     sents: dict[int, list[Word]] = defaultdict(list)
    #     for word in self.words or []:
    #         if word.index_sentence is not None:
    #             sents[word.index_sentence].append(word)
    #     for key in sents:
    #         for w in sents[key]:
    #             if w.index_token is None:
    #                 raise ValueError(f"Index token is not defined for {w.string}")
    #     for key in sents:
    #         sents[key].sort(
    #             key=lambda x: x.index_token if x.index_token is not None else -1
    #         )
    #     if self.sentence_embeddings is None:
    #         self.sentence_embeddings = dict()
    #     return [
    #         Sentence(words=val, index=key, embedding=self.sentence_embeddings.get(key))
    #         for key, val in sorted(sents.items(), key=lambda x: x[0])
    #     ]

    # @property
    # def sentences_tokens(self) -> list[list[str]]:
    #     sentences_tokens: list[list[str]] = list()
    #     for sentence in self.sentences:
    #         sentence_tokens: list[str] = [
    #             word.string for word in sentence if word.string is not None
    #         ]
    #         sentences_tokens.append(sentence_tokens)
    #     return sentences_tokens

    # @property
    # def sentences_strings(self) -> list[str]:
    #     sentences_list: list[list[str]] = self.sentences_tokens
    #     sentences_str: list[str] = list()
    #     for sentence_tokens in sentences_list:
    #         sentence_tokens_str: str = " ".join(
    #             [t for t in sentence_tokens if t is not None]
    #         )
    #         sentences_str.append(sentence_tokens_str)
    #     return sentences_str

    # def _get_words_attribute(self, attribute):
    #     if not self.words:
    #         return []
    #     return [
    #         getattr(word, attribute) for word in self.words if hasattr(word, attribute)
    #     ]

    # @property
    # def tokens(self) -> list[str]:
    #     return self._get_words_attribute("string")

    # @property
    # def tokens_stops_filtered(self) -> list[str]:
    #     tokens: list[str] = self._get_words_attribute("string")
    #     is_token_stop: list[bool] = self._get_words_attribute("stop")
    #     tokens_no_stops: list[str] = [
    #         token
    #         for index, token in enumerate(tokens)
    #         if index < len(is_token_stop) and not is_token_stop[index]
    #     ]
    #     return tokens_no_stops

    # @property
    # def pos(self) -> list[str]:
    #     return self._get_words_attribute("upos")

    # @property
    # def morphosyntactic_features(self) -> list[MorphosyntacticFeatureBundle]:
    #     return self._get_words_attribute("features")

    # @property
    # def lemmata(self) -> list[str]:
    #     return self._get_words_attribute("lemma")

    # @property
    # def stems(self) -> list[str]:
    #     return self._get_words_attribute("stem")

    # def __getitem__(self, word_index: int) -> Word:
    #     if not self.words:
    #         raise IndexError("No words in Doc.")
    #     return self.words[word_index]

    # @property
    # def embeddings(self):
    #     return self._get_words_attribute("embedding")


class Process(BaseModel):
    """Abstract base for NLP processes operating on a ``Doc``.

    Subclasses implement ``run()`` to transform or enrich a document.

    Attributes:
      glottolog_id: Optional target language code for language‑specific logic.

    """

    glottolog_id: Optional[str] = None

    @abstractmethod
    def run(self, input_doc: Doc) -> Doc:
        """Process ``input_doc`` and return an enriched/modified copy."""
        pass


class Pipeline(BaseModel):
    """Composable set of processes to analyze a document.

    Attributes:
      description: Human‑readable description.
      processes: Ordered list of process classes to apply.
      language: Resolved language metadata.
      dialect: Resolved dialect metadata (if applicable).
      glottolog_id: Language code used for auto‑resolution.

    """

    description: Optional[str] = None
    # Pydantic model classes use a custom metaclass, which mypy treats as
    # ModelMetaclass rather than type[Process]. To avoid metaclass typing
    # conflicts in subclasses' default_factory lists, keep this as list[Any]
    # while callers can still treat items as type[Process] at runtime.
    processes: Optional[list[Any]] = Field(default_factory=list)
    language: Optional[Language] = None
    dialect: Optional[Dialect] = None
    glottolog_id: Optional[str] = None

    @model_validator(mode="after")
    def _auto_resolve_language_and_dialect(self) -> "Pipeline":
        """Fill in language/dialect from ``glottolog_id`` when missing.

        Returns:
          Self, with ``language`` and/or ``dialect`` populated if resolution
          succeeds.

        """
        # Only resolve if at least one is missing
        if (self.language is None or self.dialect is None) and self.glottolog_id:
            try:
                # Late import to avoid core<->languages circular import at module import time
                from cltk.languages.glottolog import resolve_languoid

                lang, dia = resolve_languoid(self.glottolog_id)
                if self.language is None:
                    self.language = lang
                if self.dialect is None:
                    self.dialect = dia
            except Exception as e:
                # Don’t hard-fail here; subclasses can assert/validate if required
                logger.debug(
                    f"Pipeline auto-resolve skipped for '{self.glottolog_id}': {e}"
                )
        return self

    def add_process(self, process: type[Process]) -> None:
        """Append a process class to the pipeline order.

        Args:
          process: A ``Process`` subclass to add to the pipeline.

        """
        if self.processes is None:
            self.processes = []
        self.processes.append(process)
