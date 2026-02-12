"""Core data models used throughout CLTK.

This module defines small, typed Pydantic models for linguistic metadata
and the main runtime containers (``Word``, ``Sentence``, ``Doc``), along with
lightweight abstractions for ``Process`` and ``Pipeline``. These types are the
building blocks of the NLP pipeline and are designed to be simple to serialize
and render well in documentation.
"""

from abc import abstractmethod
from collections import defaultdict
from datetime import date
from typing import Any, ClassVar, Iterable, Literal, Optional, TypeAlias, Union

import numpy as np
from pydantic import AnyUrl, BaseModel, Field, PrivateAttr, model_validator

from cltk.core.cltk_logger import logger
from cltk.core.provenance import ProvenanceRecord
from cltk.morphosyntax.ud_deprels import UDDeprelTag
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


BACKEND_TYPES: TypeAlias = Literal[
    "openai", "stanza", "spacy", "ollama", "ollama-cloud", "mistral"
]
AVAILABLE_OPENAI_MODELS: TypeAlias = Literal["gpt-5-mini", "gpt-5"]

AVAILABLE_MISTRAL_MODELS: TypeAlias = Literal[
    "mistral-large-latest",
    "magistral-small-latest",
    "mistral-medium-latest",
    "mistral-large-latest",
]

# Pronunciation modes for IPA rendering (especially Ancient Greek)
IPA_PRONUNCIATION_MODE: TypeAlias = Literal[
    "attic_5c_bce",
    "koine_1c_ce",
    "byzantine_medieval",
]


################# UD types below #################

# TODO: This will probably need to be expanded
InflectionalDomain = Literal["Nominal", "Verbal"]


class UDFeatureValue(BaseModel):
    """Canonical value for a UD feature key.

    Attributes:
        code: Short code for the value (e.g., ``"Masc"``).
        label: Human‑readable label (e.g., ``"Masculine"``).
        description: Longer explanation of the value.
        inflectional_class: Optional class of inflectional features this value belongs to (e.g., ``"Nominal"``, ``"Verbal"``).
        is_deprecated: Whether the value is deprecated in UD.

    """

    code: str  # e.g., "Masc"
    label: str  # e.g., "Masculine"
    description: str  # Full explanation
    inflectional_class: Optional[InflectionalDomain] = None
    is_deprecated: Optional[bool] = False


class UDFeature(BaseModel):
    """Canonical UD feature definition.

    Attributes:
        key: Feature key (e.g., ``"Case"``).
        category: High‑level category (lexical/inflectional/other).
        description: Description of the feature semantics.
        values: Mapping from value codes to their definitions.

    """

    key: str  # e.g., "Case"
    category: Literal["Lexical", "Inflectional", "Other"]
    description: str
    values: dict[str, UDFeatureValue]


class UDFeatureTag(BaseModel):
    """A single UD feature key/value tag.

    Validates a pair (``key``, ``value``) against the registry, attempting to
    normalize known variants via ``normalize_ud_feature_pair``.

    Attributes:
        key: UD feature key (e.g., ``"Case"``).
        value: UD feature value code (e.g., ``"Nom"``).
        value_label: Human‑readable label resolved from the registry.
        category: Feature category populated from the canonical definition.
        inflectional_class: Optional inflectional class for the feature.

    """

    # Use this when instantiated a tagged word
    key: str
    value: str
    value_label: str = ""
    category: Literal["Lexical", "Inflectional", "Other"] = "Lexical"
    inflectional_class: Optional[Literal["Nominal", "Verbal"]] = None

    @model_validator(mode="before")
    @classmethod
    def fill_fields(cls, data: dict) -> dict:
        """Pre-validate and enrich tag data using the feature registry.

        Attempts to normalize ``(key, value)`` pairs that are not found. On
        success, populates ``category``, ``inflectional_class``, and
        ``value_label`` based on the canonical ``UD_FEATURES_MAP`` entry.

        Args:
            data: Input dictionary with at least ``key`` and ``value``.

        Raises:
            ValueError: If required fields are missing or normalization fails.

        Returns:
            The enriched data dictionary for model construction.

        """
        from cltk.morphosyntax.normalization import normalize_ud_feature_pair
        from cltk.morphosyntax.ud_features import UD_FEATURES_MAP

        key = data.get("key")
        value = data.get("value")
        if not isinstance(key, str) or not isinstance(value, str):
            msg = "UDFeatureTag requires 'key' and 'value' as strings."
            logger.error(msg)
            raise ValueError(msg)
        if key not in UD_FEATURES_MAP or value not in UD_FEATURES_MAP[key].values:
            # Try to normalize
            normalized = normalize_ud_feature_pair(key, value)
            if normalized:
                key, value = normalized
                data["key"] = key
                data["value"] = value
            else:
                msg = f"Invalid value '{value}' for feature key '{key}'"
                raise ValueError(msg)
        feature = UD_FEATURES_MAP[key]
        if value not in feature.values:
            msg = f"Value '{value}' is not valid for feature key '{key}' even after normalization."
            raise ValueError(msg)
        data["category"] = feature.category
        data["inflectional_class"] = feature.values[value].inflectional_class
        data["value_label"] = feature.values[value].label
        return data

    def __str__(self) -> str:
        """Return a short, readable representation of the feature tag."""
        return f"UDFeatureTag({self.key}={self.value_label}" + ")"

    def __repr__(self) -> str:
        """Alias for ``__str__`` to aid debugging and logging."""
        return self.__str__()


class UDFeatureTagSet(BaseModel):
    """A collection of feature tags for a token.

    Attributes:
        features: Ordered list of ``UDFeatureTag`` entries.

    Notes:
        This uses a list to retain insertion order. A dictionary keyed by
        feature "key" may be more efficient for lookups in some contexts.

    """

    # `add_feature` would be a little faster if this were a dict
    # `features: dict[str, UDFeatureTag] = {}`
    features: list[UDFeatureTag] = []

    def add_feature(self, feature: UDFeatureTag) -> None:
        """Add a feature to the set if the key is not already present.

        Args:
            feature: Feature tag to add.

        Returns:
            None

        """
        if any(f.key == feature.key for f in self.features):
            logger.error(
                f"Feature with key '{feature.key}' already exists in the tag set."
            )
            return None
        self.features.append(feature)
        logger.debug(f"Added feature {feature.key} to UDFeatureTagSet.")

    def __str__(self) -> str:
        """Return a compact, readable representation of the tag set."""
        features_str = ", ".join(str(f) for f in self.features)
        return f"UDFeatureTagSet([{features_str}])"

    def __repr__(self) -> str:
        """Alias for ``__str__`` to aid debugging and logging."""
        return self.__str__()


################# UD types above #################


class CLTKGenAIResponse(BaseModel):
    """Response model for generative backend interactions (OpenAI/Ollama).

    Attributes:
      response: The generated text returned by the LLM.
      usage: Token usage information (input, output, total) when available.

    """

    response: str
    usage: dict[str, int]


class ScoredText(BaseModel):
    """Generic scored alternative, used for glosses and translations."""

    text: str
    probability: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    note: Optional[str] = None


class Gloss(BaseModel):
    """Contextual and dictionary glosses plus alternatives."""

    dictionary: Optional[str] = None
    context: Optional[str] = None
    alternatives: list[ScoredText] = Field(default_factory=list)


class LemmaTranslationCandidate(BaseModel):
    """Stable lemma-level translation candidate with an optional probability."""

    text: str
    probability: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    source: Optional[str] = None


class IPAEnrichment(BaseModel):
    """IPA transcription with explicit pronunciation mode."""

    value: str
    mode: IPA_PRONUNCIATION_MODE


class OrthographyHelper(BaseModel):
    """Orthography/phonology helpers to expose syllables and accent."""

    syllables: list[str] = Field(default_factory=list)
    stress: Optional[str] = None
    accent_class: Optional[str] = None
    phonology_trace: list[str] = Field(default_factory=list)


class PedagogicalNote(BaseModel):
    """Short, learner-facing note tied to a token or dependency relation."""

    token_index: Optional[int] = None
    relation: Optional[str] = None
    note: Optional[str] = None
    disambiguates: Optional[str] = None


class IdiomSpan(BaseModel):
    """Span-level idiom/MWE annotation."""

    id: Optional[str] = None
    token_indices: list[int] = Field(default_factory=list)
    phrase_gloss: Optional[str] = None
    kind: Optional[str] = None
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class WordEnrichment(BaseModel):
    """Bundle of enrichment data layered on top of morph/dependency analysis."""

    gloss: Optional[Gloss] = None
    lemma_translations: list[LemmaTranslationCandidate] = Field(default_factory=list)
    ipa: Optional[IPAEnrichment] = None
    orthography: Optional[OrthographyHelper] = None
    idiom_span_ids: list[str] = Field(default_factory=list)
    pedagogical_notes: list[PedagogicalNote] = Field(default_factory=list)


class Translation(BaseModel):
    """Structured translation with language metadata and notes."""

    source_lang_id: Optional[str] = None
    target_lang_id: Optional[str] = None
    text: str
    notes: Optional[str] = None
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class NameVariant(BaseModel):
    """Alternative name or label for a language or dialect.

    Attributes:
      value: The display string for the name.
      source: Optional provenance or catalogue name.
      script: Optional script tag (e.g., ISO 15924).
      language: Optional language code for the label text.

    """

    value: str
    source: Optional[str] = None
    script: Optional[str] = None
    language: Optional[str] = None


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

    glottolog_id: Optional[str] = None
    language_code: Optional[str] = None
    name: str
    status: Optional[Status] = None
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
    glottolog_id: Optional[str] = None
    identifiers: list[Identifier] = Field(default_factory=list)
    level: Optional[Level] = None
    status: Optional[Status] = None
    type: Optional[str] = None

    geo: Optional[GeoArea] = None
    timespan: Optional[Timespan] = None

    classification: Optional[Classification] = None
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

    _doc: Any = PrivateAttr(default=None)

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
    enrichment: Optional[WordEnrichment] = None
    annotation_sources: dict[str, str] = Field(default_factory=dict)
    confidence: dict[str, float] = Field(default_factory=dict)


class Sentence(CLTKBaseModel):
    """A sentence containing words and optional embedding."""

    _doc: Any = PrivateAttr(default=None)

    words: Optional[list[Word]] = Field(default_factory=list)
    index: Optional[int] = None
    embedding: Optional[np.ndarray] = None
    translation: Optional[Translation] = None
    annotation_sources: dict[str, str] = Field(default_factory=dict)


class ModelConfig(BaseModel):
    """Common base for backend configuration blocks."""

    model_config = {"extra": "forbid"}


class StanzaBackendConfig(ModelConfig):
    """Options specific to the Stanza backend."""

    model: Optional[str] = Field(
        default=None,
        description="Optional non-default Stanza model/treebank name to load.",
    )


class OpenAIBackendConfig(ModelConfig):
    """Options specific to the OpenAI/ChatGPT backend."""

    model: Optional[Union[AVAILABLE_OPENAI_MODELS, str]] = None
    temperature: float = Field(default=1.0, ge=0, le=2)
    max_output_tokens: Optional[int] = Field(default=None, gt=0)
    top_p: Optional[float] = Field(default=None, ge=0, le=1)
    presence_penalty: Optional[float] = Field(default=None, ge=-2, le=2)
    frequency_penalty: Optional[float] = Field(default=None, ge=-2, le=2)
    max_retries: int = Field(default=2, ge=0)
    api_key: Optional[str] = None


class MistralBackendConfig(ModelConfig):
    """Options specific to the Mistral backend."""

    model: Optional[Union[AVAILABLE_MISTRAL_MODELS, str]] = None
    temperature: float = Field(default=1.0, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, gt=0)
    top_p: Optional[float] = Field(default=None, ge=0, le=1)
    random_seed: Optional[int] = Field(default=None, ge=0)
    max_retries: int = Field(default=2, ge=0)
    api_key: Optional[str] = None


class OllamaBackendConfig(ModelConfig):
    """Options specific to the Ollama backend (local or remote)."""

    model: Optional[str] = None
    temperature: float = Field(default=0.8, ge=0)
    top_p: Optional[float] = Field(default=None, ge=0, le=1)
    num_ctx: Optional[int] = Field(default=None, gt=0)
    num_predict: Optional[int] = Field(default=None, gt=0)
    host: Optional[str] = Field(
        default="http://127.0.0.1",
        description="Base URL for the Ollama server, e.g., http://localhost or https://ollama.example.com.",
    )
    port: Optional[int] = Field(default=11434, ge=1, le=65535)
    use_cloud: bool = False
    api_key: Optional[str] = None
    options: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional model options passed directly to the Ollama client.",
    )
    max_retries: int = Field(default=2, ge=0)

    @property
    def base_url(self) -> Optional[str]:
        """Return a combined host:port string when both are provided."""
        if not self.host:
            return None
        base = self.host.rstrip("/")
        if self.port:
            # Avoid duplicating ports if the host already includes one
            if ":" in base.split("//")[-1]:
                return base
            return f"{base}:{self.port}"
        return base


class CLTKConfig(BaseModel):
    """Bundled configuration for initializing :class:`~cltk.nlp.NLP`."""

    language_code: Optional[str] = None
    language: Optional[Language] = None
    backend: BACKEND_TYPES = "stanza"
    model: Optional[str] = None
    custom_pipeline: Optional["Pipeline"] = None
    suppress_banner: bool = False

    stanza: Optional[StanzaBackendConfig] = None
    openai: Optional[OpenAIBackendConfig] = None
    mistral: Optional[MistralBackendConfig] = None
    ollama: Optional[OllamaBackendConfig] = None

    model_config = {"extra": "forbid"}

    @property
    def active_backend_config(
        self,
    ) -> Optional[ModelConfig]:
        """Return the config block matching ``backend``."""
        mapping: dict[str, Optional[ModelConfig]] = {
            "stanza": self.stanza,
            "openai": self.openai,
            "mistral": self.mistral,
            "ollama": self.ollama,
            "ollama-cloud": self.ollama,
            "spacy": None,
        }
        return mapping.get(self.backend)

    @model_validator(mode="after")
    def _ensure_single_backend_config(self) -> "CLTKConfig":
        """Ensure only one backend config block is provided at a time."""
        if not self.language_code and not self.language:
            raise ValueError("Provide language_code or language.")
        if self.language and not self.language_code:
            if not self.language.glottolog_id:
                raise ValueError(
                    "language.glottolog_id is required when language_code is not set."
                )
            self.language_code = self.language.glottolog_id
        configured = [
            name
            for name, cfg in (
                ("stanza", self.stanza),
                ("openai", self.openai),
                ("mistral", self.mistral),
                ("ollama", self.ollama),
            )
            if cfg is not None
        ]
        if len(configured) > 1:
            raise ValueError(
                f"Provide configuration for only one backend at a time: {', '.join(configured)}"
            )
        if configured:
            allowed_for_backend: dict[str, set[str]] = {
                "stanza": {"stanza"},
                "openai": {"openai"},
                "mistral": {"mistral"},
                "ollama": {"ollama"},
                "ollama-cloud": {"ollama"},
                "spacy": set(),
            }
            allowed = allowed_for_backend.get(self.backend, set())
            if allowed and configured[0] not in allowed:
                raise ValueError(
                    f"Config for '{configured[0]}' provided but backend is '{self.backend}'."
                )
        return self


class Doc(CLTKBaseModel):
    """Top‑level container returned from ``NLP()`` pipelines.

    Attributes:
      language: Language metadata associated with the text.
      words: Token‑level annotations (may be empty prior to analysis).
      pipeline: Pipeline instance that produced this document, if any.
      raw: Original raw text.
      normalized_text: Normalized version of the text.
      sentence_embeddings: Optional embeddings per sentence index.
      sentence_translations: Structured translations keyed by sentence index.
      translation: Optional document-level translation string (usually aggregated).
      translations: Collected structured translations (e.g., per sentence).
      summary: Optional summary of the document.
      topic: Optional topic classification.
      discourse_relations: Discourse relation labels (if available).
      coreferences: Coreference links as (mention, antecedent, i, j).
      sentence_boundaries: List of (start, stop) character offsets.
      genai_use: List of usage/metadata dicts from model calls.
      metadata: Arbitrary metadata about the document.

    """

    language: Language
    words: list[Word] = Field(default_factory=list)
    pipeline: Optional["Pipeline"] = None
    raw: Optional[str] = None
    normalized_text: Optional[str] = None
    embeddings_model: Optional[Any] = None
    sentence_embeddings: dict[int, np.ndarray] = Field(default_factory=dict)
    sentence_translations: dict[int, Translation] = Field(default_factory=dict)
    translation: Optional[str] = None
    translations: list[Translation] = Field(default_factory=list)
    summary: Optional[str] = None
    topic: Optional[str] = None
    discourse_relations: list[str] = Field(default_factory=list)
    coreferences: list[tuple[str, str, int, int]] = Field(default_factory=list)
    idiom_spans: list[IdiomSpan] = Field(default_factory=list)
    sentence_boundaries: list[tuple[int, int]] = Field(default_factory=list)
    genai_use: list[dict[str, Any]] = Field(default_factory=list)
    backend: Optional[BACKEND_TYPES] = None
    # Model alias/name for the selected backend. For OpenAI this should be
    # one of AVAILABLE_OPENAI_MODELS; for Ollama any model string is accepted.
    model: Optional[Union[BACKEND_TYPES, str]] = None
    dialect: Optional[Dialect] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    provenance: dict[str, ProvenanceRecord] = Field(default_factory=dict)
    default_provenance_id: Optional[str] = None
    sentence_annotation_sources: dict[int, dict[str, str]] = Field(default_factory=dict)

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

    @property
    def sentences(self) -> list[Sentence]:
        if not self.words:
            return []
        sents: dict[int, list[Word]] = defaultdict(list)
        for word in self.words or []:
            if word.index_sentence is not None:
                sents[word.index_sentence].append(word)
        for key in sents:
            for w in sents[key]:
                if w.index_token is None:
                    raise ValueError(f"Index token is not defined for {w.string}")
        for key in sents:
            sents[key].sort(
                key=lambda x: x.index_token if x.index_token is not None else -1
            )
        if self.sentence_embeddings is None:
            self.sentence_embeddings = dict()
        sentences: list[Sentence] = []
        for key, val in sorted(sents.items(), key=lambda x: x[0]):
            for w in val:
                try:
                    w._doc = self
                except Exception:
                    pass
            sentence = Sentence(
                words=val,
                index=key,
                embedding=self.sentence_embeddings.get(key),
                translation=self.sentence_translations.get(key),
                annotation_sources=self.sentence_annotation_sources.get(key, {}),
            )
            try:
                sentence._doc = self
            except Exception:
                pass
            sentences.append(sentence)
        return sentences

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

    # Stable, user-facing identifier for configuration and discovery.
    process_id: ClassVar[str] = ""
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
    # Spec-driven pipelines may store Process instances with configured fields.
    processes: Optional[list[Any]] = Field(default_factory=list)
    language: Optional[Language] = None
    dialect: Optional[Dialect] = None
    glottolog_id: Optional[str] = None
    # Optional PipelineSpec companion used by declarative pipelines.
    spec: Optional[Any] = None

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
                from cltk.languages.glottolog import get_language

                lang, dia = get_language(self.glottolog_id)
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

    def add_process(self, process: Any) -> None:
        """Append a process class to the pipeline order.

        Args:
          process: A ``Process`` subclass to add to the pipeline.

        """
        if self.processes is None:
            self.processes = []
        self.processes.append(process)

    def describe(self) -> list[str]:
        """Return a human-friendly list describing pipeline order."""
        lines: list[str] = []
        if self.spec and getattr(self.spec, "steps", None):
            try:
                from cltk.core.process_registry import ProcessRegistry

                registry = ProcessRegistry.list_processes()
            except Exception:
                registry = {}
            for idx, step in enumerate(self.spec.steps, 1):
                proc_cls = registry.get(step.id)
                class_name = proc_cls.__name__ if proc_cls else step.id
                provides = getattr(proc_cls, "provides", None) if proc_cls else None
                requires = getattr(proc_cls, "requires", None) if proc_cls else None
                status = "enabled" if step.enabled else "disabled"
                line = f"{idx}. {step.id} ({class_name}) [{status}]"
                if provides:
                    line += f" provides={_format_list(provides)}"
                if requires:
                    line += f" requires={_format_list(requires)}"
                lines.append(line)
            return lines
        for idx, proc in enumerate(self.processes or [], 1):
            pid = _process_id(proc)
            class_name = _process_name(proc)
            provides = getattr(proc, "provides", None)
            requires = getattr(proc, "requires", None)
            line = f"{idx}. {pid} ({class_name})"
            if provides:
                line += f" provides={_format_list(provides)}"
            if requires:
                line += f" requires={_format_list(requires)}"
            lines.append(line)
        return lines

    def enable(self, process_id: str) -> None:
        """Enable a step by process_id or class name."""
        if self.spec and getattr(self.spec, "steps", None):
            idx = _find_step_index(self.spec.steps, process_id)
            if idx is not None:
                self.spec.steps[idx].enabled = True
                self._sync_processes_from_spec()
            return
        if self.processes is None:
            self.processes = []
        if any(
            _matches_identifier(_process_id(p), process_id)
            or _process_name(p) == process_id
            for p in self.processes
        ):
            return
        try:
            from cltk.core.process_registry import ProcessRegistry

            registry = ProcessRegistry.list_processes()
        except Exception:
            registry = {}
        proc_cls = registry.get(process_id)
        if not proc_cls:
            for candidate in registry.values():
                if candidate.__name__ == process_id:
                    proc_cls = candidate
                    break
        if proc_cls:
            self.processes.append(proc_cls)

    def disable(self, process_id: str) -> None:
        """Disable a step by process_id or class name."""
        if self.spec and getattr(self.spec, "steps", None):
            idx = _find_step_index(self.spec.steps, process_id)
            if idx is not None:
                self.spec.steps[idx].enabled = False
                self._sync_processes_from_spec()
            return
        self._remove_process(process_id)

    def remove(self, process_id: str) -> None:
        """Remove a step from the pipeline entirely."""
        if self.spec and getattr(self.spec, "steps", None):
            registry = {}
            try:
                from cltk.core.process_registry import ProcessRegistry

                registry = ProcessRegistry.list_processes()
            except Exception:
                registry = {}
            original = list(self.spec.steps)
            self.spec.steps = [
                step
                for step in self.spec.steps
                if not _step_matches(step.id, process_id, registry)
            ]
            if self.spec.steps != original:
                self._sync_processes_from_spec()
            return
        self._remove_process(process_id)

    def move_before(self, process_id: str, before_process_id: str) -> None:
        """Move a step before another step."""
        if self.spec and getattr(self.spec, "steps", None):
            self._move_step(process_id, before_process_id, before=True)
            return
        self._move_process(process_id, before_process_id, before=True)

    def move_after(self, process_id: str, after_process_id: str) -> None:
        """Move a step after another step."""
        if self.spec and getattr(self.spec, "steps", None):
            self._move_step(process_id, after_process_id, before=False)
            return
        self._move_process(process_id, after_process_id, before=False)

    def to_spec(self) -> Any:
        """Return a best-effort PipelineSpec from this pipeline."""
        if self.spec is not None:
            return self.spec
        try:
            from cltk.pipeline.specs import PipelineSpec, StepSpec

            steps = [
                StepSpec(
                    id=_process_id(proc),
                    enabled=True,
                    config=(
                        proc.model_dump(exclude_none=True, exclude={"glottolog_id"})
                        if isinstance(proc, Process)
                        else {}
                    ),
                )
                for proc in (self.processes or [])
            ]
            return PipelineSpec(
                language=self.glottolog_id,
                steps=steps,
            )
        except Exception:
            return None

    @classmethod
    def from_toml(cls, path: str) -> "Pipeline":
        """Build a Pipeline from a TOML spec file."""
        from cltk.pipeline.compiler import compile_pipeline
        from cltk.pipeline.spec_io import load_pipeline_spec

        spec = load_pipeline_spec(path)
        pipeline = compile_pipeline(spec)
        return pipeline

    def _sync_processes_from_spec(self) -> None:
        """Rebuild process list from the stored PipelineSpec."""
        if not self.spec:
            return
        from cltk.pipeline.compiler import compile_processes

        self.processes = compile_processes(self.spec)

    def _remove_process(self, process_id: str) -> None:
        """Drop a process from the list by process_id or class name."""
        if not self.processes:
            return
        self.processes = [
            proc
            for proc in self.processes
            if not (
                _matches_identifier(_process_id(proc), process_id)
                or _process_name(proc) == process_id
            )
        ]

    def _move_process(self, process_id: str, anchor_id: str, *, before: bool) -> None:
        """Reorder processes by moving one before/after an anchor."""
        if not self.processes:
            return
        source_idx = _find_index(self.processes, process_id)
        target_idx = _find_index(self.processes, anchor_id)
        if source_idx is None or target_idx is None:
            return
        item = self.processes.pop(source_idx)
        insert_at = target_idx if before else target_idx + 1
        if source_idx < target_idx and before:
            insert_at -= 1
        if source_idx < target_idx and not before:
            insert_at -= 1
        self.processes.insert(insert_at, item)

    def _move_step(self, process_id: str, anchor_id: str, *, before: bool) -> None:
        """Reorder spec steps by moving one before/after an anchor."""
        if not self.spec or not getattr(self.spec, "steps", None):
            return
        source_idx = _find_step_index(self.spec.steps, process_id)
        target_idx = _find_step_index(self.spec.steps, anchor_id)
        if source_idx is None or target_idx is None:
            return
        item = self.spec.steps.pop(source_idx)
        insert_at = target_idx if before else target_idx + 1
        if source_idx < target_idx and before:
            insert_at -= 1
        if source_idx < target_idx and not before:
            insert_at -= 1
        self.spec.steps.insert(insert_at, item)
        self._sync_processes_from_spec()


def _process_name(proc: Any) -> str:
    """Return the class name for a process class or instance."""
    if isinstance(proc, type):
        return proc.__name__
    return str(proc.__class__.__name__)


def _process_id(proc: Any) -> str:
    """Return the stable process_id or fall back to class name."""
    pid = getattr(proc, "process_id", None)
    if isinstance(pid, str) and pid:
        return pid
    return _process_name(proc)


def _matches_identifier(value: str, identifier: str) -> bool:
    """Return True when identifiers match exactly."""
    return value == identifier


def _step_matches(
    step_id: Optional[str],
    identifier: str,
    registry: dict[str, type[Any]],
) -> bool:
    """Return True when a step id or class name matches the identifier."""
    if step_id == identifier:
        return True
    proc_cls = registry.get(step_id or "")
    return bool(proc_cls and proc_cls.__name__ == identifier)


def _find_index(processes: Iterable[Any], identifier: str) -> Optional[int]:
    """Find the index of a process by id or class name."""
    for idx, proc in enumerate(processes):
        if (
            _matches_identifier(_process_id(proc), identifier)
            or _process_name(proc) == identifier
        ):
            return idx
    return None


def _find_step_index(steps: Iterable[Any], identifier: str) -> Optional[int]:
    """Find the index of a spec step by id or class name."""
    for idx, step in enumerate(steps):
        step_id = getattr(step, "id", None)
        if step_id == identifier:
            return idx
    try:
        from cltk.core.process_registry import ProcessRegistry

        registry = ProcessRegistry.list_processes()
    except Exception:
        registry = {}
    for idx, step in enumerate(steps):
        step_id = getattr(step, "id", None)
        if not isinstance(step_id, str):
            continue
        proc_cls = registry.get(step_id)
        if proc_cls and proc_cls.__name__ == identifier:
            return idx
    return None


def _format_list(value: Any) -> str:
    """Format a list-like value as a comma-separated string."""
    if isinstance(value, str):
        return value
    if isinstance(value, Iterable):
        return ",".join(str(v) for v in value)
    return str(value)
