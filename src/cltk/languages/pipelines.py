"""Language pipelines and mappings.

This module defines many language‑specific pipeline classes (mostly
LLM‑backed via OpenAI or Ollama) and central mappings from Glottolog codes to
default pipelines. Pipelines are lightweight containers that list a small
sequence of processes such as normalization, sentence splitting, and
generative annotation.
"""

from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from cltk.core.data_types import Pipeline
from cltk.core.logging_utils import plog
from cltk.dependency.processes import (
    AkkadianGenAIDependencyProcess,
    AlbanianGenAIDependencyProcess,
    AmmoniteGenAIDependencyProcess,
    AncientGreekGenAIDependencyProcess,
    AssameseGenAIDependencyProcess,
    AvestanGenAIDependencyProcess,
    AwadhiGenAIDependencyProcess,
    BactrianGenAIDependencyProcess,
    BagriGenAIDependencyProcess,
    BaihuaChineseGenAIDependencyProcess,
    BengaliGenAIDependencyProcess,
    BiblicalHebrewGenAIDependencyProcess,
    BrajGenAIDependencyProcess,
    CarianGenAIDependencyProcess,
    ChagataiGenAIDependencyProcess,
    ChurchSlavicGenAIDependencyProcess,
    ClassicalArabicGenAIDependencyProcess,
    ClassicalArmenianGenAIDependencyProcess,
    ClassicalBurmeseGenAIDependencyProcess,
    ClassicalMandaicGenAIDependencyProcess,
    ClassicalMongolianGenAIDependencyProcess,
    ClassicalSanskritGenAIDependencyProcess,
    ClassicalSyriacGenAIDependencyProcess,
    ClassicalTibetanGenAIDependencyProcess,
    CopticGenAIDependencyProcess,
    CuneiformLuwianGenAIDependencyProcess,
    DemoticGenAIDependencyProcess,
    EarlyIrishGenAIDependencyProcess,
    EasternPanjabiGenAIDependencyProcess,
    EdomiteGenAIDependencyProcess,
    GandhariGenAIDependencyProcess,
    GeezGenAIDependencyProcess,
    GothicGenAIDependencyProcess,
    GujaratiGenAIDependencyProcess,
    HatranGenAIDependencyProcess,
    HausaGenAIDependencyProcess,
    HieroglyphicLuwianGenAIDependencyProcess,
    HindiGenAIDependencyProcess,
    HittiteGenAIDependencyProcess,
    JewishBabylonianAramaicGenAIDependencyProcess,
    KashmiriGenAIDependencyProcess,
    KhariBoliGenAIDependencyProcess,
    KhotaneseGenAIDependencyProcess,
    LateEgyptianGenAIDependencyProcess,
    LatinGenAIDependencyProcess,
    LatvianGenAIDependencyProcess,
    LiteraryChineseGenAIDependencyProcess,
    LithuanianGenAIDependencyProcess,
    LycianAGenAIDependencyProcess,
    LydianGenAIDependencyProcess,
    MagadhiPrakritGenAIDependencyProcess,
    MaharastriPrakritGenAIDependencyProcess,
    MarathiGenAIDependencyProcess,
    MeiteiGenAIDependencyProcess,
    MiddleAramaicGenAIDependencyProcess,
    MiddleArmenianGenAIDependencyProcess,
    MiddleBretonGenAIDependencyProcess,
    MiddleChineseGenAIDependencyProcess,
    MiddleCornishGenAIDependencyProcess,
    MiddleEgyptianGenAIDependencyProcess,
    MiddleEnglishGenAIDependencyProcess,
    MiddleFrenchGenAIDependencyProcess,
    MiddleHighGermanGenAIDependencyProcess,
    MiddleMongolGenAIDependencyProcess,
    MiddlePersianGenAIDependencyProcess,
    MoabiteGenAIDependencyProcess,
    MogholiGenAIDependencyProcess,
    NewarGenAIDependencyProcess,
    NumidianGenAIDependencyProcess,
    OdiaGenAIDependencyProcess,
    OfficialAramaicGenAIDependencyProcess,
    OldAramaicGenAIDependencyProcess,
    OldAramaicSamalianGenAIDependencyProcess,
    OldBurmeseGenAIDependencyProcess,
    OldChineseGenAIDependencyProcess,
    OldEgyptianGenAIDependencyProcess,
    OldEnglishGenAIDependencyProcess,
    OldFrenchGenAIDependencyProcess,
    OldHighGermanGenAIDependencyProcess,
    OldHungarianGenAIDependencyProcess,
    OldJapaneseGenAIDependencyProcess,
    OldJurchenGenAIDependencyProcess,
    OldMiddleWelshGenAIDependencyProcess,
    OldNorseGenAIDependencyProcess,
    OldPersianGenAIDependencyProcess,
    OldPrussianGenAIDependencyProcess,
    OldTamilGenAIDependencyProcess,
    OldTurkicGenAIDependencyProcess,
    PalaicGenAIDependencyProcess,
    PaliGenAIDependencyProcess,
    ParthianGenAIDependencyProcess,
    PhoenicianGenAIDependencyProcess,
    SamalianGenAIDependencyProcess,
    SauraseniPrakritGenAIDependencyProcess,
    SgawKarenGenAIDependencyProcess,
    SindhiGenAIDependencyProcess,
    SinhalaGenAIDependencyProcess,
    SogdianGenAIDependencyProcess,
    TaitaGenAIDependencyProcess,
    TangutGenAIDependencyProcess,
    TokharianAGenAIDependencyProcess,
    TokharianBGenAIDependencyProcess,
    TumshuqeseGenAIDependencyProcess,
    UgariticGenAIDependencyProcess,
    UrduGenAIDependencyProcess,
    VedicSanskritGenAIDependencyProcess,
)
from cltk.morphosyntax.processes import (
    AkkadianGenAIMorphosyntaxProcess,
    AlbanianGenAIMorphosyntaxProcess,
    AmmoniteGenAIMorphosyntaxProcess,
    AncientGreekGenAIMorphosyntaxProcess,
    AssameseGenAIMorphosyntaxProcess,
    AvestanGenAIMorphosyntaxProcess,
    AwadhiGenAIMorphosyntaxProcess,
    BactrianGenAIMorphosyntaxProcess,
    BagriGenAIMorphosyntaxProcess,
    BaihuaChineseGenAIMorphosyntaxProcess,
    BengaliGenAIMorphosyntaxProcess,
    BiblicalHebrewGenAIMorphosyntaxProcess,
    BrajGenAIMorphosyntaxProcess,
    CarianGenAIMorphosyntaxProcess,
    ChagataiGenAIMorphosyntaxProcess,
    ChurchSlavicGenAIMorphosyntaxProcess,
    ClassicalArabicGenAIMorphosyntaxProcess,
    ClassicalArmenianGenAIMorphosyntaxProcess,
    ClassicalBurmeseGenAIMorphosyntaxProcess,
    ClassicalMandaicGenAIMorphosyntaxProcess,
    ClassicalMongolianGenAIMorphosyntaxProcess,
    ClassicalSanskritGenAIMorphosyntaxProcess,
    ClassicalSyriacGenAIMorphosyntaxProcess,
    ClassicalTibetanGenAIMorphosyntaxProcess,
    CopticGenAIMorphosyntaxProcess,
    CuneiformLuwianGenAIMorphosyntaxProcess,
    DemoticGenAIMorphosyntaxProcess,
    EarlyIrishGenAIMorphosyntaxProcess,
    EasternPanjabiGenAIMorphosyntaxProcess,
    EdomiteGenAIMorphosyntaxProcess,
    GandhariGenAIMorphosyntaxProcess,
    GeezGenAIMorphosyntaxProcess,
    GothicGenAIMorphosyntaxProcess,
    GujaratiGenAIMorphosyntaxProcess,
    HatranGenAIMorphosyntaxProcess,
    HausaGenAIMorphosyntaxProcess,
    HieroglyphicLuwianGenAIMorphosyntaxProcess,
    HindiGenAIMorphosyntaxProcess,
    HittiteGenAIMorphosyntaxProcess,
    JewishBabylonianAramaicGenAIMorphosyntaxProcess,
    KashmiriGenAIMorphosyntaxProcess,
    KhariBoliGenAIMorphosyntaxProcess,
    KhotaneseGenAIMorphosyntaxProcess,
    LateEgyptianGenAIMorphosyntaxProcess,
    LatinGenAIMorphosyntaxProcess,
    LatvianGenAIMorphosyntaxProcess,
    LiteraryChineseGenAIMorphosyntaxProcess,
    LithuanianGenAIMorphosyntaxProcess,
    LycianAGenAIMorphosyntaxProcess,
    LydianGenAIMorphosyntaxProcess,
    MagadhiPrakritGenAIMorphosyntaxProcess,
    MaharastriPrakritGenAIMorphosyntaxProcess,
    MarathiGenAIMorphosyntaxProcess,
    MeiteiGenAIMorphosyntaxProcess,
    MiddleAramaicGenAIMorphosyntaxProcess,
    MiddleArmenianGenAIMorphosyntaxProcess,
    MiddleBretonGenAIMorphosyntaxProcess,
    MiddleChineseGenAIMorphosyntaxProcess,
    MiddleCornishGenAIMorphosyntaxProcess,
    MiddleEgyptianGenAIMorphosyntaxProcess,
    MiddleEnglishGenAIMorphosyntaxProcess,
    MiddleFrenchGenAIMorphosyntaxProcess,
    MiddleHighGermanGenAIMorphosyntaxProcess,
    MiddleMongolGenAIMorphosyntaxProcess,
    MiddlePersianGenAIMorphosyntaxProcess,
    MoabiteGenAIMorphosyntaxProcess,
    MogholiGenAIMorphosyntaxProcess,
    NewarGenAIMorphosyntaxProcess,
    NumidianGenAIMorphosyntaxProcess,
    OdiaGenAIMorphosyntaxProcess,
    OfficialAramaicGenAIMorphosyntaxProcess,
    OldAramaicGenAIMorphosyntaxProcess,
    OldAramaicSamalianGenAIMorphosyntaxProcess,
    OldBurmeseGenAIMorphosyntaxProcess,
    OldChineseGenAIMorphosyntaxProcess,
    OldEgyptianGenAIMorphosyntaxProcess,
    OldEnglishGenAIMorphosyntaxProcess,
    OldFrenchGenAIMorphosyntaxProcess,
    OldHighGermanGenAIMorphosyntaxProcess,
    OldHungarianGenAIMorphosyntaxProcess,
    OldJapaneseGenAIMorphosyntaxProcess,
    OldJurchenGenAIMorphosyntaxProcess,
    OldMiddleWelshGenAIMorphosyntaxProcess,
    OldNorseGenAIMorphosyntaxProcess,
    OldPersianGenAIMorphosyntaxProcess,
    OldPrussianGenAIMorphosyntaxProcess,
    OldTamilGenAIMorphosyntaxProcess,
    OldTurkicGenAIMorphosyntaxProcess,
    PalaicGenAIMorphosyntaxProcess,
    PaliGenAIMorphosyntaxProcess,
    ParthianGenAIMorphosyntaxProcess,
    PhoenicianGenAIMorphosyntaxProcess,
    SamalianGenAIMorphosyntaxProcess,
    SauraseniPrakritGenAIMorphosyntaxProcess,
    SgawKarenGenAIMorphosyntaxProcess,
    SindhiGenAIMorphosyntaxProcess,
    SinhalaGenAIMorphosyntaxProcess,
    SogdianGenAIMorphosyntaxProcess,
    TaitaGenAIMorphosyntaxProcess,
    TangutGenAIMorphosyntaxProcess,
    TokharianAGenAIMorphosyntaxProcess,
    TokharianBGenAIMorphosyntaxProcess,
    TumshuqeseGenAIMorphosyntaxProcess,
    UgariticGenAIMorphosyntaxProcess,
    UrduGenAIMorphosyntaxProcess,
    VedicSanskritGenAIMorphosyntaxProcess,
)
from cltk.sentence.processes import (
    AkkadianSentenceSplittingProcess,
    AlbanianSentenceSplittingProcess,
    AmmoniteSentenceSplittingProcess,
    AncientGreekSentenceSplittingProcess,
    AncientHebrewSentenceSplittingProcess,
    AssameseSentenceSplittingProcess,
    AvestanSentenceSplittingProcess,
    AwadhiSentenceSplittingProcess,
    BactrianSentenceSplittingProcess,
    BagriSentenceSplittingProcess,
    BaihuaChineseSentenceSplittingProcess,
    BengaliSentenceSplittingProcess,
    BrajSentenceSplittingProcess,
    CarianSentenceSplittingProcess,
    ChagataiSentenceSplittingProcess,
    ChurchSlavonicSentenceSplittingProcess,
    ClassicalArabicSentenceSplittingProcess,
    ClassicalArmenianSentenceSplittingProcess,
    ClassicalBurmeseSentenceSplittingProcess,
    ClassicalMandaicSentenceSplittingProcess,
    ClassicalMongolianSentenceSplittingProcess,
    ClassicalSanskritSentenceSplittingProcess,
    ClassicalSyriacSentenceSplittingProcess,
    ClassicalTibetanSentenceSplittingProcess,
    CopticSentenceSplittingProcess,
    CuneiformLuwianSentenceSplittingProcess,
    DemoticSentenceSplittingProcess,
    EarlyIrishSentenceSplittingProcess,
    EdomiteSentenceSplittingProcess,
    GandhariSentenceSplittingProcess,
    GeezSentenceSplittingProcess,
    GothicSentenceSplittingProcess,
    GujaratiSentenceSplittingProcess,
    HatranSentenceSplittingProcess,
    HausaSentenceSplittingProcess,
    HieroglyphicLuwianSentenceSplittingProcess,
    HindiSentenceSplittingProcess,
    HittiteSentenceSplittingProcess,
    JewishBabylonianAramaicSentenceSplittingProcess,
    KashmiriSentenceSplittingProcess,
    KhariBoliSentenceSplittingProcess,
    KhotaneseSentenceSplittingProcess,
    LateEgyptianSentenceSplittingProcess,
    LatinSentenceSplittingProcess,
    LatvianSentenceSplittingProcess,
    LiteraryChineseSentenceSplittingProcess,
    LithuanianSentenceSplittingProcess,
    LycianASentenceSplittingProcess,
    LydianSentenceSplittingProcess,
    MagadhiPrakritSentenceSplittingProcess,
    MaharastriPrakritSentenceSplittingProcess,
    MarathiSentenceSplittingProcess,
    MeiteiSentenceSplittingProcess,
    MiddleAramaicSentenceSplittingProcess,
    MiddleArmenianSentenceSplittingProcess,
    MiddleBretonSentenceSplittingProcess,
    MiddleChineseSentenceSplittingProcess,
    MiddleCornishSentenceSplittingProcess,
    MiddleEgyptianSentenceSplittingProcess,
    MiddleEnglishSentenceSplittingProcess,
    MiddleFrenchSentenceSplittingProcess,
    MiddleHighGermanSentenceSplittingProcess,
    MiddleMongolSentenceSplittingProcess,
    MiddlePersianSentenceSplittingProcess,
    MoabiteSentenceSplittingProcess,
    MogholiSentenceSplittingProcess,
    NewarSentenceSplittingProcess,
    NumidianSentenceSplittingProcess,
    OdiaSentenceSplittingProcess,
    OfficialAramaicSentenceSplittingProcess,
    OldAramaicSamalianSentenceSplittingProcess,
    OldAramaicSentenceSplittingProcess,
    OldBurmeseSentenceSplittingProcess,
    OldChineseSentenceSplittingProcess,
    OldEgyptianSentenceSplittingProcess,
    OldEnglishSentenceSplittingProcess,
    OldFrenchSentenceSplittingProcess,
    OldHighGermanSentenceSplittingProcess,
    OldHungarianSentenceSplittingProcess,
    OldJapaneseSentenceSplittingProcess,
    OldJurchenSentenceSplittingProcess,
    OldMiddleWelshSentenceSplittingProcess,
    OldNorseSentenceSplittingProcess,
    OldPersianSentenceSplittingProcess,
    OldPrussianSentenceSplittingProcess,
    OldTamilSentenceSplittingProcess,
    OldTurkicSentenceSplittingProcess,
    PalaicSentenceSplittingProcess,
    PaliSentenceSplittingProcess,
    PanjabiSentenceSplittingProcess,
    ParthianSentenceSplittingProcess,
    PhoenicianSentenceSplittingProcess,
    SamalianSentenceSplittingProcess,
    SauraseniPrakritSentenceSplittingProcess,
    SgawKarenSentenceSplittingProcess,
    SindhiSentenceSplittingProcess,
    SinhalaSentenceSplittingProcess,
    SogdianSentenceSplittingProcess,
    TaitaSentenceSplittingProcess,
    TangutSentenceSplittingProcess,
    TocharianASentenceSplittingProcess,
    TocharianBSentenceSplittingProcess,
    TumshuqeseSentenceSplittingProcess,
    UgariticSentenceSplittingProcess,
    UrduSentenceSplittingProcess,
    VedicSanskritSentenceSplittingProcess,
)
from cltk.text.processes import MultilingualNormalizeProcess

if TYPE_CHECKING:  # for type checkers only
    from cltk.stanza.processes import StanzaAnalyzeProcess as StanzaAnalyzeProcessType
else:  # runtime resolution
    StanzaAnalyzeProcessType = object  # sentinel

RuntimeStanzaAnalyzeProcess: Any
try:
    from cltk.stanza.processes import (
        StanzaAnalyzeProcess as RuntimeStanzaAnalyzeProcess,
    )

    _STANZA_AVAILABLE = True
except Exception:  # pragma: no cover - stanza optional
    RuntimeStanzaAnalyzeProcess = None
    _STANZA_AVAILABLE = False


def ensure_stanza_available() -> None:
    """Raise an informative error when stanza-backed processes are missing."""
    if not _STANZA_AVAILABLE or RuntimeStanzaAnalyzeProcess is None:
        msg = "Stanza backend requested but stanza is not installed. Install with: pip install 'cltk[stanza]'"
        raise ImportError(msg)


def _stanza_processes_default() -> list[Any]:
    """Return the standard stanza pipeline processes, ensuring availability."""
    ensure_stanza_available()
    return [MultilingualNormalizeProcess, RuntimeStanzaAnalyzeProcess]


class LatinStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Latin."""

    description: Optional[str] = "Stanza pipeline for the Latin language."
    glottolog_id: Optional[str] = "lati1261"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LatinStanzaPipeline with language: {self.language}"
        )
        plog(self).info("LatinStanzaPipeline created.")


class AncientGreekStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Ancient Greek."""

    description: Optional[str] = "Stanza pipeline for the Ancient Greek language."
    glottolog_id: Optional[str] = "anci1242"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing AncientGreekStanzaPipeline with language: {self.language}"
        )
        plog(self).info("AncientGreekStanzaPipeline created.")


class AkkadianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Akkadian."""

    description: Optional[str] = "Pipeline for the Akkadian language"
    glottolog_id: Optional[str] = "akka1240"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AkkadianSentenceSplittingProcess,
            AkkadianGenAIMorphosyntaxProcess,
            AkkadianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        plog(self).debug(
            f"Initializing AkkadianGenAIPipeline with language: {self.language.name}"
        )
        plog(self).info("AkkadianGenAIPipeline created.")


class ClassicalArabicGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Arabic."""

    description: Optional[str] = "Pipeline for the Arabic language"
    glottolog_id: Optional[str] = "clas1259"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalArabicSentenceSplittingProcess,
            ClassicalArabicGenAIMorphosyntaxProcess,
            ClassicalArabicGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing ArabicGenAIPipeline with language: {self.language}"
        )
        plog(self).info("ArabicGenAIPipeline created.")


#
class ClassicalSyriacGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Syriac."""

    description: Optional[str] = "Pipeline for the Classical Syriac language"
    glottolog_id: Optional[str] = "clas1252"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalSyriacSentenceSplittingProcess,
            ClassicalSyriacGenAIMorphosyntaxProcess,
            ClassicalSyriacGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        plog(self).debug(
            f"Initializing ClassicalSyriacGenAIPipeline with language: {self.language.name}"
        )
        plog(self).info("ClassicalSyriacGenAIPipeline created.")


# ClassicalTibetanPipeline
class ClassicalTibetanPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Tibetan."""

    description: Optional[str] = "Pipeline for the Classical Tibetan language"
    glottolog_id: Optional[str] = "clas1254"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalTibetanSentenceSplittingProcess,
            ClassicalTibetanGenAIMorphosyntaxProcess,
            ClassicalTibetanGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        plog(self).debug(
            f"Initializing ClassicalTibetanGenAIPipeline with language: {self.language.name}"
        )
        plog(self).info("ClassicalTibetanGenAIPipeline created.")


class CopticGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Coptic."""

    description: Optional[str] = "OpenAI Pipeline for the Coptic language."
    glottolog_id: Optional[str] = "copt1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CopticSentenceSplittingProcess,
            CopticGenAIMorphosyntaxProcess,
            CopticGenAIDependencyProcess,
        ]
    )


class GothicGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic."""

    description: Optional[str] = "Pipeline for the Gothic language"
    glottolog_id: Optional[str] = "goth1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GothicSentenceSplittingProcess,
            GothicGenAIMorphosyntaxProcess,
            GothicGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GothicGenAIPipeline with language: {self.language}"
        )
        plog(self).info("GothicGenAIPipeline created.")


class AncientGreekGenAIPipeline(Pipeline):
    """Pipeline for Ancient Greek using normalization and OpenAI annotation only."""

    description: Optional[str] = "Pipeline for Ancient Greek with OpenAI annotation"
    glottolog_id: Optional[str] = "anci1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            # AncientGreekNormalizeProcess,
            MultilingualNormalizeProcess,
            AncientGreekSentenceSplittingProcess,
            AncientGreekGenAIMorphosyntaxProcess,
            AncientGreekGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GreekGenAIPipeline with language: {self.language}"
        )
        plog(self).info("GreekGenAIPipeline created.")


class BiblicalHebrewGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Hebrew."""

    description: Optional[str] = "Pipeline for the Ancient Hebrew language."
    glottolog_id: Optional[str] = "anci1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AncientHebrewSentenceSplittingProcess,
            BiblicalHebrewGenAIMorphosyntaxProcess,
            BiblicalHebrewGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(f"Initializing LatinPipeline with language: {self.language}")
        plog(self).info("LatinPipeline created.")


class LatinGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Latin."""

    description: Optional[str] = "OpenAI Pipeline for the Latin language."
    glottolog_id: Optional[str] = "lati1261"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            # LatinNormalizeProcess,
            MultilingualNormalizeProcess,
            LatinSentenceSplittingProcess,
            LatinGenAIMorphosyntaxProcess,
            LatinGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(f"Initializing LatinPipeline with language: {self.language}")
        plog(self).info("LatinPipeline created.")


class MiddleEnglishGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle English."""

    description: Optional[str] = "Pipeline for the Middle English language"
    glottolog_id: Optional[str] = "midd1317"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleEnglishSentenceSplittingProcess,
            MiddleEnglishGenAIMorphosyntaxProcess,
            MiddleEnglishGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleEnglishGenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleEnglishGenAIPipeline created.")


class MiddleFrenchGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle French."""

    description: Optional[str] = "Pipeline for the Middle French language"
    glottolog_id: Optional[str] = "midd1316"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleFrenchSentenceSplittingProcess,
            MiddleFrenchGenAIMorphosyntaxProcess,
            MiddleFrenchGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleFrenchGenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleFrenchGenAIPipeline created.")


class MiddlePersianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Persian (Pahlavi)."""

    description: Optional[str] = "Pipeline for the Middle Persian (Pahlavi) language"
    glottolog_id: Optional[str] = "pahl1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddlePersianSentenceSplittingProcess,
            MiddlePersianGenAIMorphosyntaxProcess,
            MiddlePersianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddlePersianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddlePersianGenAIPipeline created.")


class ImperialAramaicGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Official Aramaic."""

    description: Optional[str] = "OpenAI Pipeline for the Official Aramaic language."
    glottolog_id: Optional[str] = "impe1235"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OfficialAramaicSentenceSplittingProcess,
            OfficialAramaicGenAIMorphosyntaxProcess,
            OfficialAramaicGenAIDependencyProcess,
        ]
    )


class ChurchSlavonicGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for (Old) Church Slavonic."""

    description: Optional[str] = "Pipeline for the Church Slavonic language"
    glottolog_id: Optional[str] = "chur1257"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ChurchSlavonicSentenceSplittingProcess,
            ChurchSlavicGenAIMorphosyntaxProcess,
            ChurchSlavicGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing ChurchSlavonicGenAIPipeline with language: {self.language}"
        )
        plog(self).info("ChurchSlavonicGenAIPipeline")


class OldEnglishGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old English."""

    description: Optional[str] = "Pipeline for the Old English language"
    glottolog_id: Optional[str] = "olde1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldEnglishSentenceSplittingProcess,
            OldEnglishGenAIMorphosyntaxProcess,
            OldEnglishGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        plog(self).debug(
            f"Initializing OldEnglishGenAIPipeline with language: {self.language.name}"
        )
        plog(self).info("OldEnglishGenAIPipeline created.")


class OldFrenchGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old French."""

    description: Optional[str] = "Pipeline for the Old French language"
    glottolog_id: Optional[str] = "oldf1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldFrenchSentenceSplittingProcess,
            OldFrenchGenAIMorphosyntaxProcess,
            OldFrenchGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldFrenchGenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldFrenchGenAIPipeline created.")


class OldNorseGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Norse."""

    description: Optional[str] = "Pipeline for the Old Norse language"
    glottolog_id: Optional[str] = "oldn1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldNorseSentenceSplittingProcess,
            OldNorseGenAIMorphosyntaxProcess,
            OldNorseGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldNorseGenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldNorseGenAIPipeline created.")


class PaliGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Pali."""

    description: Optional[str] = "Pipeline for the Pali language"
    glottolog_id: Optional[str] = "pali1273"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PaliSentenceSplittingProcess,
            PaliGenAIMorphosyntaxProcess,
            PaliGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(f"Initializing PaliPipeline with language: {self.language}")
        plog(self).info("PaliPipeline created.")


class ClassicalSanskritGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Sanskrit."""

    description: Optional[str] = "Pipeline for the Classical Sanskrit language"
    glottolog_id: Optional[str] = "vedi1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalSanskritSentenceSplittingProcess,
            ClassicalSanskritGenAIMorphosyntaxProcess,
            ClassicalSanskritGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing ClassicalSanskritGenAIPipeline with language: {self.language}"
        )
        plog(self).info("ClassicalSanskritGenAIPipeline created.")


class VedicSanskritGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Vedic Sanskrit."""

    description: Optional[str] = "Pipeline for the Vedic Sanskrit language"
    glottolog_id: Optional[str] = "clas1258"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            VedicSanskritSentenceSplittingProcess,
            VedicSanskritGenAIMorphosyntaxProcess,
            VedicSanskritGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing VedicSanskritGenAIPipeline with language: {self.language}"
        )
        plog(self).info("VedicSanskritGenAIPipeline created.")


class OldHighGermanGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old High German."""

    description: Optional[str] = "Pipeline for the Old High German language"
    glottolog_id: Optional[str] = "oldh1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            # MiddleHighGermanTokenizationProcess,  # Substitute with OldHighGermanTokenizationProcess if available
            OldHighGermanSentenceSplittingProcess,
            OldHighGermanGenAIMorphosyntaxProcess,
            OldHighGermanGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldHighGermanGenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldHighGermanGenAIPipeline created.")


class MiddleHighGermanGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle High German."""

    description: Optional[str] = "Pipeline for the Middle High German language"
    glottolog_id: Optional[str] = "midd1343"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleHighGermanSentenceSplittingProcess,
            MiddleHighGermanGenAIMorphosyntaxProcess,
            MiddleHighGermanGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleHighGermanGenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleHighGermanGenAIPipeline created.")


class LiteraryChineseGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Literary (or Classical) Chinese."""

    description: Optional[str] = (
        "Pipeline for the Literary (or Classical) Chinese language"
    )
    glottolog_id: Optional[str] = "lite1248"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LiteraryChineseSentenceSplittingProcess,
            LiteraryChineseGenAIMorphosyntaxProcess,
            LiteraryChineseGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LiteraryChineseGenAIPipeline with language: {self.language}"
        )
        plog(self).info("LiteraryChineseGenAIPipeline created.")


class ChurchSlavonicStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Church Slavonic."""

    description: Optional[str] = "Stanza pipeline for the Church Slavonic language."
    glottolog_id: Optional[str] = "chur1257"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing ChurchSlavonicStanzaPipeline with language: {self.language}"
        )
        plog(self).info("ChurchSlavonicStanzaPipeline created.")


class OldFrenchStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Old French."""

    description: Optional[str] = "Stanza pipeline for the Old French language."
    glottolog_id: Optional[str] = "oldf1239"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldFrenchStanzaPipeline with language: {self.language}"
        )
        plog(self).info("OldFrenchStanzaPipeline created.")


class GothicStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Gothic."""

    description: Optional[str] = "Stanza pipeline for the Gothic language."
    glottolog_id: Optional[str] = "goth1244"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GothicStanzaPipeline with language: {self.language}"
        )
        plog(self).info("GothicStanzaPipeline created.")


class OldEnglishStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Old English."""

    description: Optional[str] = "Stanza pipeline for the Old English language."
    glottolog_id: Optional[str] = "olde1238"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldEnglishStanzaPipeline with language: {self.language}"
        )
        plog(self).info("OldEnglishStanzaPipeline created.")


class LiteraryChineseStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Literary Chinese."""

    description: Optional[str] = "Stanza pipeline for the Literary Chinese language."
    glottolog_id: Optional[str] = "lite1248"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LiteraryChineseStanzaPipeline with language: {self.language}"
        )
        plog(self).info("LiteraryChineseStanzaPipeline created.")


class OttomanTurkishStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Ottoman Turkish."""

    description: Optional[str] = "Stanza pipeline for the Ottoman Turkish language."
    glottolog_id: Optional[str] = "otto1234"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OttomanTurkishStanzaPipeline with language: {self.language}"
        )
        plog(self).info("OttomanTurkishStanzaPipeline created.")


class ClassicalArmenianStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Classical Armenian."""

    description: Optional[str] = "Stanza pipeline for the Classical Armenian language."
    glottolog_id: Optional[str] = "clas1256"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing ClassicalArmenianStanzaPipeline with language: {self.language}"
        )
        plog(self).info("ClassicalArmenianStanzaPipeline created.")


class CopticStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Coptic."""

    description: Optional[str] = "Stanza pipeline for the Coptic language."
    glottolog_id: Optional[str] = "copt1239"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing CopticStanzaPipeline with language: {self.language}"
        )
        plog(self).info("CopticStanzaPipeline created.")


class OldRussianStanzaPipeline(Pipeline):
    """Stanza-backed pipeline for Old Russian (Old East Slavic)."""

    description: Optional[str] = "Stanza pipeline for the Old Russian language."
    glottolog_id: Optional[str] = "oldr1238"
    processes: Optional[list[Any]] = Field(default_factory=_stanza_processes_default)

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldRussianStanzaPipeline with language: {self.language}"
        )
        plog(self).info("OldRussianStanzaPipeline created.")


class DemoticGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Demotic Egyptian."""

    description: Optional[str] = "Pipeline for the Demotic Egyptian language"
    glottolog_id: Optional[str] = "demo1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            DemoticSentenceSplittingProcess,
            DemoticGenAIMorphosyntaxProcess,
            DemoticGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing DemoticGenAIPipeline with language: {self.language}"
        )
        plog(self).info("DemoticGenAIPipeline created.")


class HittiteGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Hittite."""

    description: Optional[str] = "Pipeline for the Hittite language"
    glottolog_id: Optional[str] = "hitt1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HittiteSentenceSplittingProcess,
            HittiteGenAIMorphosyntaxProcess,
            HittiteGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing HittiteGenAIPipeline with language: {self.language}"
        )
        plog(self).info("HittiteGenAIPipeline created.")


class TocharianAGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Tocharian A."""

    description: Optional[str] = "Pipeline for the Tocharian A language"
    glottolog_id: Optional[str] = "toch1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TocharianASentenceSplittingProcess,
            TokharianAGenAIMorphosyntaxProcess,
            TokharianAGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing TocharianAGenAIPipeline with language: {self.language}"
        )
        plog(self).info("TocharianAGenAIPipeline created.")


class TocharianBGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Tocharian B."""

    description: Optional[str] = "Pipeline for the Tocharian B language"
    glottolog_id: Optional[str] = "toch1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TocharianBSentenceSplittingProcess,
            TokharianBGenAIMorphosyntaxProcess,
            TokharianBGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing TocharianBGenAIPipeline with language: {self.language}"
        )
        plog(self).info("TocharianBGenAIPipeline created.")


class AvestanGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Avestan."""

    description: Optional[str] = "Pipeline for the Avestan language"
    glottolog_id: Optional[str] = "aves1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AvestanSentenceSplittingProcess,
            AvestanGenAIMorphosyntaxProcess,
            AvestanGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing AvestanGenAIPipeline with language: {self.language}"
        )
        plog(self).info("AvestanGenAIPipeline created.")


class BactrianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Bactrian."""

    description: Optional[str] = "Pipeline for the Bactrian language"
    glottolog_id: Optional[str] = "bact1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BactrianSentenceSplittingProcess,
            BactrianGenAIMorphosyntaxProcess,
            BactrianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing BactrianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("BactrianGenAIPipeline created.")


class SogdianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Sogdian."""

    description: Optional[str] = "Pipeline for the Sogdian language"
    glottolog_id: Optional[str] = "sogd1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SogdianSentenceSplittingProcess,
            SogdianGenAIMorphosyntaxProcess,
            SogdianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing SogdianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("SogdianGenAIPipeline created.")


class KhotaneseGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Khotanese."""

    description: Optional[str] = "Pipeline for the Khotanese language"
    glottolog_id: Optional[str] = "khot1251"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            KhotaneseSentenceSplittingProcess,
            KhotaneseGenAIMorphosyntaxProcess,
            KhotaneseGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing KhotaneseGenAIPipeline with language: {self.language}"
        )
        plog(self).info("KhotaneseGenAIPipeline created.")


class TumshuqeseGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Tumshuqese."""

    description: Optional[str] = "Pipeline for the Tumshuqese language"
    glottolog_id: Optional[str] = "tums1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TumshuqeseSentenceSplittingProcess,
            TumshuqeseGenAIMorphosyntaxProcess,
            TumshuqeseGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing TumshuqeseGenAIPipeline with language: {self.language}"
        )
        plog(self).info("TumshuqeseGenAIPipeline created.")


class OldPersianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Persian."""

    description: Optional[str] = "Pipeline for the Old Persian language"
    glottolog_id: Optional[str] = "oldp1254"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldPersianSentenceSplittingProcess,
            OldPersianGenAIMorphosyntaxProcess,
            OldPersianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldPersianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldPersianGenAIPipeline created.")


class EarlyIrishGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Irish."""

    description: Optional[str] = "Pipeline for the Old Irish language"
    glottolog_id: Optional[str] = "oldi1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            EarlyIrishSentenceSplittingProcess,
            EarlyIrishGenAIMorphosyntaxProcess,
            EarlyIrishGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldIrishGenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldIrishGenAIPipeline created.")


class UgariticGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Ugaritic."""

    description: Optional[str] = "Pipeline for the Ugaritic language"
    glottolog_id: Optional[str] = "ugar1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            UgariticSentenceSplittingProcess,
            UgariticGenAIMorphosyntaxProcess,
            UgariticGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing UgariticGenAIPipeline with language: {self.language}"
        )
        plog(self).info("UgariticGenAIPipeline created.")


class PhoenicianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Phoenician (Punic)."""

    description: Optional[str] = "Pipeline for the Phoenician (Punic) language"
    glottolog_id: Optional[str] = "phoe1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PhoenicianSentenceSplittingProcess,
            PhoenicianGenAIMorphosyntaxProcess,
            PhoenicianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing PhoenicianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("PhoenicianGenAIPipeline created.")


class GeezGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Geʿez (Classical Ethiopic)."""

    description: Optional[str] = "Pipeline for the Geʿez (Classical Ethiopic) language"
    glottolog_id: Optional[str] = "geez1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GeezSentenceSplittingProcess,
            GeezGenAIMorphosyntaxProcess,
            GeezGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GeezGenAIPipeline with language: {self.language}"
        )
        plog(self).info("GeezGenAIPipeline created.")


class MiddleEgyptianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Egyptian."""

    description: Optional[str] = "Pipeline for the Middle Egyptian language"
    glottolog_id: Optional[str] = "midd1369"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleEgyptianSentenceSplittingProcess,
            MiddleEgyptianGenAIMorphosyntaxProcess,
            MiddleEgyptianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleEgyptianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleEgyptianGenAIPipeline created.")


class OldEgyptianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Egyptian."""

    description: Optional[str] = "Pipeline for the Old Egyptian language"
    glottolog_id: Optional[str] = "olde1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldEgyptianSentenceSplittingProcess,
            OldEgyptianGenAIMorphosyntaxProcess,
            OldEgyptianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldEgyptianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldEgyptianGenAIPipeline created.")


class LateEgyptianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Late Egyptian."""

    description: Optional[str] = "Pipeline for the Late Egyptian language"
    glottolog_id: Optional[str] = "late1256"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LateEgyptianSentenceSplittingProcess,
            LateEgyptianGenAIMorphosyntaxProcess,
            LateEgyptianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LateEgyptianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("LateEgyptianGenAIPipeline created.")


class ParthianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Parthian."""

    description: Optional[str] = "Pipeline for the Parthian language"
    glottolog_id: Optional[str] = "part1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ParthianSentenceSplittingProcess,
            ParthianGenAIMorphosyntaxProcess,
            ParthianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LateEgyptianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("LateEgyptianGenAIPipeline created.")


class OldMiddleWelshGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Welsh."""

    description: Optional[str] = "Pipeline for the Middle Welsh language"
    glottolog_id: Optional[str] = "oldw1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldMiddleWelshSentenceSplittingProcess,
            OldMiddleWelshGenAIMorphosyntaxProcess,
            OldMiddleWelshGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleWelshGenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleWelshGenAIPipeline created.")


class MiddleBretonGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Breton."""

    description: Optional[str] = "Pipeline for the Middle Breton language"
    glottolog_id: Optional[str] = "oldb1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleBretonSentenceSplittingProcess,
            MiddleBretonGenAIMorphosyntaxProcess,
            MiddleBretonGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleBretonGenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleBretonGenAIPipeline created.")


class CornishGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Cornish."""

    description: Optional[str] = "Pipeline for the Cornish language"
    glottolog_id: Optional[str] = "corn1251"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleCornishSentenceSplittingProcess,
            MiddleCornishGenAIMorphosyntaxProcess,
            MiddleCornishGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing CornishGenAIPipeline with language: {self.language}"
        )
        plog(self).info("CornishGenAIPipeline created.")


class OldPrussianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Prussian."""

    description: Optional[str] = "Pipeline for the Old Prussian language"
    glottolog_id: Optional[str] = "prus1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldPrussianSentenceSplittingProcess,
            OldPrussianGenAIMorphosyntaxProcess,
            OldPrussianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldPrussianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldPrussianGenAIPipeline created.")


class LithuanianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Lithuanian."""

    description: Optional[str] = "Pipeline for the Lithuanian language"
    glottolog_id: Optional[str] = "lith1251"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LithuanianSentenceSplittingProcess,
            LithuanianGenAIMorphosyntaxProcess,
            LithuanianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LithuanianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("LithuanianGenAIPipeline created.")


class LatvianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Latvian."""

    description: Optional[str] = "Pipeline for the Latvian language"
    glottolog_id: Optional[str] = "latv1249"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LatvianSentenceSplittingProcess,
            LatvianGenAIMorphosyntaxProcess,
            LatvianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LatvianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("LatvianGenAIPipeline created.")


class AlbanianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Albanian."""

    description: Optional[str] = "Pipeline for the Albanian language"
    glottolog_id: Optional[str] = "gheg1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AlbanianSentenceSplittingProcess,
            AlbanianGenAIMorphosyntaxProcess,
            AlbanianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing AlbanianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("AlbanianGenAIPipeline created.")


class ClassicalArmenianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Armenian."""

    description: Optional[str] = "Pipeline for the Classical Armenian language"
    glottolog_id: Optional[str] = "clas1256"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalArmenianSentenceSplittingProcess,
            ClassicalArmenianGenAIMorphosyntaxProcess,
            ClassicalArmenianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing ClassicalArmenianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("ClassicalArmenianGenAIPipeline created.")


class MiddleArmenianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Armenian."""

    description: Optional[str] = "Pipeline for the Middle Armenian language"
    glottolog_id: Optional[str] = "midd1364"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleArmenianSentenceSplittingProcess,
            MiddleArmenianGenAIMorphosyntaxProcess,
            MiddleArmenianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleArmenianGenAIPipeline with language: {self.language}"
        )


class CuneiformLuwianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Cuneiform Luwian."""

    description: Optional[str] = "Pipeline for the Cuneiform Luwian language"
    glottolog_id: Optional[str] = "cune1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CuneiformLuwianSentenceSplittingProcess,
            CuneiformLuwianGenAIMorphosyntaxProcess,
            CuneiformLuwianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing CuneiformLuwianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("CuneiformLuwianGenAIPipeline created.")


class HieroglyphicLuwianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Hieroglyphic Luwian."""

    description: Optional[str] = "Pipeline for the Hieroglyphic Luwian language"
    glottolog_id: Optional[str] = "hier1240"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HieroglyphicLuwianSentenceSplittingProcess,
            HieroglyphicLuwianGenAIMorphosyntaxProcess,
            HieroglyphicLuwianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing HieroglyphicLuwianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("HieroglyphicLuwianGenAIPipeline created.")


class LycianAGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Lycian."""

    description: Optional[str] = "Pipeline for the Lycian language"
    glottolog_id: Optional[str] = "lyci1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LycianASentenceSplittingProcess,
            LycianAGenAIMorphosyntaxProcess,
            LycianAGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LycianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("LycianGenAIPipeline created.")


class LydianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Lydian."""

    description: Optional[str] = "Pipeline for the Lydian language"
    glottolog_id: Optional[str] = "lydi1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LydianSentenceSplittingProcess,
            LydianGenAIMorphosyntaxProcess,
            LydianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LydianGenAIPipeline with language: {self.language}"
        )
        plog(self).info("LydianGenAIPipeline created.")


class PalaicGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Palaic."""

    description: Optional[str] = "Pipeline for the Palaic language"
    glottolog_id: Optional[str] = "pala1331"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PalaicSentenceSplittingProcess,
            PalaicGenAIMorphosyntaxProcess,
            PalaicGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing PalaicGenAIPipeline with language: {self.language}"
        )
        plog(self).info("PalaicGenAIPipeline created.")


class CarianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Carian."""

    description: Optional[str] = "Pipeline for the Carian language"
    glottolog_id: Optional[str] = "cari1274"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CarianSentenceSplittingProcess,
            CarianGenAIMorphosyntaxProcess,
            CarianGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing CarianGenAIPipeline with language: {self.language}"
        )


class SauraseniPrakritGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Sauraseni Prakrit."""

    description: Optional[str] = "Pipeline for the Sauraseni Prakrit language"
    glottolog_id: Optional[str] = "saur1252"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SauraseniPrakritSentenceSplittingProcess,
            SauraseniPrakritGenAIMorphosyntaxProcess,
            SauraseniPrakritGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing SauraseniPrakritGenAIPipeline with language: {self.language}"
        )
        plog(self).info("SauraseniPrakritGenAIPipeline created.")


class MaharastriPrakritGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Maharastri Prakrit."""

    description: Optional[str] = "Pipeline for the Maharastri Prakrit language"
    glottolog_id: Optional[str] = "maha1305"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MaharastriPrakritSentenceSplittingProcess,
            MaharastriPrakritGenAIMorphosyntaxProcess,
            MaharastriPrakritGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MaharastriPrakritGenAIPipeline with language: {self.language}"
        )
        plog(self).info("MaharastriPrakritGenAIPipeline created.")


class MagadhiPrakritGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Magadhi Prakrit."""

    description: Optional[str] = "Pipeline for the Magadhi Prakrit language"
    glottolog_id: Optional[str] = "maga1260"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MagadhiPrakritSentenceSplittingProcess,
            MagadhiPrakritGenAIMorphosyntaxProcess,
            MagadhiPrakritGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MagadhiPrakritGenAIPipeline with language: {self.language}"
        )
        plog(self).info("MagadhiPrakritGenAIPipeline created.")


class GandhariGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Gandhari."""

    description: Optional[str] = "Pipeline for the Gandhari language"
    glottolog_id: Optional[str] = "gand1259"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GandhariSentenceSplittingProcess,
            GandhariGenAIMorphosyntaxProcess,
            GandhariGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GandhariGenAIPipeline with language: {self.language}"
        )
        plog(self).info("GandhariGenAIPipeline created.")


# Hindi and closely related lects
class HindiGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Hindi (glottocode hind1269)."""

    description: Optional[str] = "Pipeline for the Hindi language"
    glottolog_id: Optional[str] = "hind1269"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HindiSentenceSplittingProcess,
            HindiGenAIMorphosyntaxProcess,
            HindiGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing HindiGenAIPipeline with language: {self.language}"
        )
        plog(self).info("HindiGenAIPipeline created.")


class KhariBoliGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Khari Boli (Hindi dialect)."""

    description: Optional[str] = "Pipeline for the Khari Boli dialect of Hindi"
    glottolog_id: Optional[str] = "khad1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            KhariBoliSentenceSplittingProcess,
            KhariBoliGenAIMorphosyntaxProcess,
            KhariBoliGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing KhariBoliGenAIPipeline with language: {self.language}"
        )
        plog(self).info("KhariBoliGenAIPipeline created.")


class BrajGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Braj Bhasha."""

    description: Optional[str] = "Pipeline for the Braj Bhasha language"
    glottolog_id: Optional[str] = "braj1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BrajSentenceSplittingProcess,
            BrajGenAIMorphosyntaxProcess,
            BrajGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing BrajGenAIPipeline with language: {self.language}"
        )
        plog(self).info("BrajGenAIPipeline created.")


class AwadhiGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Awadhi."""

    description: Optional[str] = "Pipeline for the Awadhi language"
    glottolog_id: Optional[str] = "awad1243"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AwadhiSentenceSplittingProcess,
            AwadhiGenAIMorphosyntaxProcess,
            AwadhiGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing AwadhiGenAIPipeline with language: {self.language}"
        )
        plog(self).info("AwadhiGenAIPipeline created.")


class UrduGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Urdu."""

    description: Optional[str] = "Pipeline for the Urdu language"
    glottolog_id: Optional[str] = "urdu1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            UrduSentenceSplittingProcess,
            UrduGenAIMorphosyntaxProcess,
            UrduGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing UrduGenAIPipeline with language: {self.language}"
        )
        plog(self).info("UrduGenAIPipeline created.")


# Eastern Indo-Aryan and Western IA additions
class BengaliGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Bengali."""

    description: Optional[str] = "Pipeline for the Bengali language"
    glottolog_id: Optional[str] = "beng1280"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BengaliSentenceSplittingProcess,
            BengaliGenAIMorphosyntaxProcess,
            BengaliGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing BengaliGenAIPipeline with language: {self.language}"
        )
        plog(self).info("BengaliGenAIPipeline created.")


class OdiaGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Odia (Oriya)."""

    description: Optional[str] = "Pipeline for the Odia language"
    glottolog_id: Optional[str] = "oriy1255"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OdiaSentenceSplittingProcess,
            OdiaGenAIMorphosyntaxProcess,
            OdiaGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OdiaGenAIPipeline with language: {self.language}"
        )
        plog(self).info("OdiaGenAIPipeline created.")


class AssameseGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Assamese."""

    description: Optional[str] = "Pipeline for the Assamese language"
    glottolog_id: Optional[str] = "assa1263"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AssameseSentenceSplittingProcess,
            AssameseGenAIMorphosyntaxProcess,
            AssameseGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing AssameseGenAIPipeline with language: {self.language}"
        )
        plog(self).info("AssameseGenAIPipeline created.")


class GujaratiGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Gujarati."""

    description: Optional[str] = "Pipeline for the Gujarati language"
    glottolog_id: Optional[str] = "guja1252"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GujaratiSentenceSplittingProcess,
            GujaratiGenAIMorphosyntaxProcess,
            GujaratiGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GujaratiGenAIPipeline with language: {self.language}"
        )
        plog(self).info("GujaratiGenAIPipeline created.")


class MarathiGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Marathi."""

    description: Optional[str] = "Pipeline for the Marathi language"
    glottolog_id: Optional[str] = "mara1378"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MarathiSentenceSplittingProcess,
            MarathiGenAIMorphosyntaxProcess,
            MarathiGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MarathiGenAIPipeline with language: {self.language}"
        )
        plog(self).info("MarathiGenAIPipeline created.")


class SinhalaGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Sinhala."""

    description: Optional[str] = "Pipeline for the Sinhala language"
    glottolog_id: Optional[str] = "sinh1246"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SinhalaSentenceSplittingProcess,
            SinhalaGenAIMorphosyntaxProcess,
            SinhalaGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing SinhalaGenAIPipeline with language: {self.language}"
        )
        plog(self).info("SinhalaGenAIPipeline created.")


class EasternPanjabiGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Eastern Panjabi."""

    description: Optional[str] = "Pipeline for the Eastern Panjabi language"
    glottolog_id: Optional[str] = "panj1256"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PanjabiSentenceSplittingProcess,
            EasternPanjabiGenAIMorphosyntaxProcess,
            EasternPanjabiGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing EasternPanjabiGenAIPipeline with language: {self.language}"
        )
        plog(self).info("EasternPanjabiGenAIPipeline created.")


class SindhiGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Sindhi."""

    description: Optional[str] = "Pipeline for the Sindhi language"
    glottolog_id: Optional[str] = "sind1272"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SindhiSentenceSplittingProcess,
            SindhiGenAIMorphosyntaxProcess,
            SindhiGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing SindhiGenAIPipeline with language: {self.language}"
        )
        plog(self).info("SindhiGenAIPipeline created.")


class KashmiriGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Kashmiri."""

    description: Optional[str] = "Pipeline for the Kashmiri language"
    glottolog_id: Optional[str] = "kash1277"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            KashmiriSentenceSplittingProcess,
            KashmiriGenAIMorphosyntaxProcess,
            KashmiriGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing KashmiriGenAIPipeline with language: {self.language}"
        )
        plog(self).info("KashmiriGenAIPipeline created.")


# Sino-Tibetan additions
class OldChineseGenAIPipeline(Pipeline):
    """Pipeline for Old Chinese."""

    description: Optional[str] = "Pipeline for Old Chinese"
    glottolog_id: Optional[str] = "oldc1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldChineseSentenceSplittingProcess,
            OldChineseGenAIMorphosyntaxProcess,
            OldChineseGenAIDependencyProcess,
        ]
    )


class MiddleChineseGenAIPipeline(Pipeline):
    """Pipeline for Middle Chinese."""

    description: Optional[str] = "Pipeline for Middle Chinese"
    glottolog_id: Optional[str] = "midd1344"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleChineseSentenceSplittingProcess,
            MiddleChineseGenAIMorphosyntaxProcess,
            MiddleChineseGenAIDependencyProcess,
        ]
    )


class BaihuaChineseGenAIPipeline(Pipeline):
    """Pipeline for Early Vernacular Chinese (Baihua)."""

    description: Optional[str] = "Pipeline for Early Vernacular Chinese (Baihua)"
    glottolog_id: Optional[str] = "clas1255"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BaihuaChineseSentenceSplittingProcess,
            BaihuaChineseGenAIMorphosyntaxProcess,
            BaihuaChineseGenAIDependencyProcess,
        ]
    )


class OldBurmeseGenAIPipeline(Pipeline):
    """Pipeline for Old Burmese."""

    description: Optional[str] = "Pipeline for Old Burmese"
    glottolog_id: Optional[str] = "oldb1235"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldBurmeseSentenceSplittingProcess,
            OldBurmeseGenAIMorphosyntaxProcess,
            OldBurmeseGenAIDependencyProcess,
        ]
    )


class ClassicalBurmeseGenAIPipeline(Pipeline):
    """Pipeline for Classical/Nuclear Burmese."""

    description: Optional[str] = "Pipeline for Classical Burmese"
    glottolog_id: Optional[str] = "nucl1310"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalBurmeseSentenceSplittingProcess,
            ClassicalBurmeseGenAIMorphosyntaxProcess,
            ClassicalBurmeseGenAIDependencyProcess,
        ]
    )


class TangutGenAIPipeline(Pipeline):
    """Pipeline for Tangut (Xixia)."""

    description: Optional[str] = "Pipeline for the Tangut language"
    glottolog_id: Optional[str] = "tang1334"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TangutSentenceSplittingProcess,
            TangutGenAIMorphosyntaxProcess,
            TangutGenAIDependencyProcess,
        ]
    )


class NewarGenAIPipeline(Pipeline):
    """Pipeline for Newar (Classical Nepal Bhasa)."""

    description: Optional[str] = "Pipeline for the Newar language"
    glottolog_id: Optional[str] = "newa1246"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            NewarSentenceSplittingProcess,
            NewarGenAIMorphosyntaxProcess,
            NewarGenAIDependencyProcess,
        ]
    )


class MeiteiGenAIPipeline(Pipeline):
    """Pipeline for Meitei (Classical Manipuri)."""

    description: Optional[str] = "Pipeline for the Meitei (Classical Manipuri) language"
    glottolog_id: Optional[str] = "mani1292"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MeiteiSentenceSplittingProcess,
            MeiteiGenAIMorphosyntaxProcess,
            MeiteiGenAIDependencyProcess,
        ]
    )


class SgawKarenGenAIPipeline(Pipeline):
    """Pipeline for Sgaw Karen."""

    description: Optional[str] = "Pipeline for the Sgaw Karen language"
    glottolog_id: Optional[str] = "sgaw1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SgawKarenSentenceSplittingProcess,
            SgawKarenGenAIMorphosyntaxProcess,
            SgawKarenGenAIDependencyProcess,
        ]
    )


class MiddleMongolGenAIPipeline(Pipeline):
    """Pipeline for Middle Mongol."""

    description: Optional[str] = "Pipeline for the Middle Mongol language"
    glottolog_id: Optional[str] = "midd1351"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleMongolSentenceSplittingProcess,
            MiddleMongolGenAIMorphosyntaxProcess,
            MiddleMongolGenAIDependencyProcess,
        ]
    )


class ClassicalMongolianGenAIPipeline(Pipeline):
    """Pipeline for Classical Mongolian."""

    description: Optional[str] = "Pipeline for the Classical Mongolian language"
    glottolog_id: Optional[str] = "mong1331"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalMongolianSentenceSplittingProcess,
            ClassicalMongolianGenAIMorphosyntaxProcess,
            ClassicalMongolianGenAIDependencyProcess,
        ]
    )


class MogholiGenAIPipeline(Pipeline):
    """Pipeline for Mogholi (Moghol)."""

    description: Optional[str] = "Pipeline for the Mogholi (Moghol) language"
    glottolog_id: Optional[str] = "mogh1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MogholiSentenceSplittingProcess,
            MogholiGenAIMorphosyntaxProcess,
            MogholiGenAIDependencyProcess,
        ]
    )


class BagriGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Bagri (Rajasthani)."""

    description: Optional[str] = "Pipeline for the Bagri (Rajasthani) language"
    glottolog_id: Optional[str] = "bagr1243"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BagriSentenceSplittingProcess,
            BagriGenAIMorphosyntaxProcess,
            BagriGenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing BagriGenAIPipeline with language: {self.language}"
        )
        plog(self).info("BagriGenAIPipeline created.")


# Additional Afroasiatic, Altaic-adjacent, Uralic, Turkic, Dravidian pipelines
class NumidianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Numidian (Ancient Berber)."""

    description: Optional[str] = "Pipeline for the Numidian (Ancient Berber) language"
    glottolog_id: Optional[str] = "numi1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            NumidianSentenceSplittingProcess,
            NumidianGenAIMorphosyntaxProcess,
            NumidianGenAIDependencyProcess,
        ]
    )


class TaitaGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Taita (Cushitic)."""

    description: Optional[str] = "Pipeline for the Cushitic Taita language"
    glottolog_id: Optional[str] = "tait1247"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TaitaSentenceSplittingProcess,
            TaitaGenAIMorphosyntaxProcess,
            TaitaGenAIDependencyProcess,
        ]
    )


class HausaGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Hausa."""

    description: Optional[str] = "Pipeline for the Hausa language"
    glottolog_id: Optional[str] = "haus1257"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HausaSentenceSplittingProcess,
            HausaGenAIMorphosyntaxProcess,
            HausaGenAIDependencyProcess,
        ]
    )


class OldJurchenGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Jurchen."""

    description: Optional[str] = "Pipeline for the Old Jurchen language"
    glottolog_id: Optional[str] = "jurc1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldJurchenSentenceSplittingProcess,
            OldJurchenGenAIMorphosyntaxProcess,
            OldJurchenGenAIDependencyProcess,
        ]
    )


class OldJapaneseGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Japanese."""

    description: Optional[str] = "Pipeline for the Old Japanese language"
    glottolog_id: Optional[str] = "japo1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldJapaneseSentenceSplittingProcess,
            OldJapaneseGenAIMorphosyntaxProcess,
            OldJapaneseGenAIDependencyProcess,
        ]
    )


class OldHungarianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Hungarian."""

    description: Optional[str] = "Pipeline for the Old Hungarian language"
    glottolog_id: Optional[str] = "oldh1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldHungarianSentenceSplittingProcess,
            OldHungarianGenAIMorphosyntaxProcess,
            OldHungarianGenAIDependencyProcess,
        ]
    )


class ChagataiGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Chagatai."""

    description: Optional[str] = "Pipeline for the Chagatai language"
    glottolog_id: Optional[str] = "chag1247"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ChagataiSentenceSplittingProcess,
            ChagataiGenAIMorphosyntaxProcess,
            ChagataiGenAIDependencyProcess,
        ]
    )


class OldTurkicGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Turkic."""

    description: Optional[str] = "Pipeline for the Old Turkic language"
    glottolog_id: Optional[str] = "oldu1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldTurkicSentenceSplittingProcess,
            OldTurkicGenAIMorphosyntaxProcess,
            OldTurkicGenAIDependencyProcess,
        ]
    )


class OldTamilGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Tamil."""

    description: Optional[str] = "Pipeline for the Old Tamil language"
    glottolog_id: Optional[str] = "oldt1248"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldTamilSentenceSplittingProcess,
            OldTamilGenAIMorphosyntaxProcess,
            OldTamilGenAIDependencyProcess,
        ]
    )


# Northwest Semitic and Aramaic additions
class MoabiteGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Moabite."""

    description: Optional[str] = "Pipeline for the Moabite language"
    glottolog_id: Optional[str] = "moab1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MoabiteSentenceSplittingProcess,
            MoabiteGenAIMorphosyntaxProcess,
            MoabiteGenAIDependencyProcess,
        ]
    )


class AmmoniteGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Ammonite."""

    description: Optional[str] = "Pipeline for the Ammonite language"
    glottolog_id: Optional[str] = "ammo1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AmmoniteSentenceSplittingProcess,
            AmmoniteGenAIMorphosyntaxProcess,
            AmmoniteGenAIDependencyProcess,
        ]
    )


class EdomiteGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Edomite."""

    description: Optional[str] = "Pipeline for the Edomite language"
    glottolog_id: Optional[str] = "edom1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            EdomiteSentenceSplittingProcess,
            EdomiteGenAIMorphosyntaxProcess,
            EdomiteGenAIDependencyProcess,
        ]
    )


class OldAramaicGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Aramaic (up to 700 BCE)."""

    description: Optional[str] = "Pipeline for Old Aramaic (up to 700 BCE)"
    glottolog_id: Optional[str] = "olda1246"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldAramaicSentenceSplittingProcess,
            OldAramaicGenAIMorphosyntaxProcess,
            OldAramaicGenAIDependencyProcess,
        ]
    )


class OldAramaicSamalianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Aramaic–Samʾalian."""

    description: Optional[str] = "Pipeline for Old Aramaic–Samʾalian"
    glottolog_id: Optional[str] = "olda1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldAramaicSamalianSentenceSplittingProcess,
            OldAramaicSamalianGenAIMorphosyntaxProcess,
            OldAramaicSamalianGenAIDependencyProcess,
        ]
    )


class MiddleAramaicGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Aramaic."""

    description: Optional[str] = "Pipeline for Middle Aramaic"
    glottolog_id: Optional[str] = "midd1366"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleAramaicSentenceSplittingProcess,
            MiddleAramaicGenAIMorphosyntaxProcess,
            MiddleAramaicGenAIDependencyProcess,
        ]
    )


class ClassicalMandaicGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Mandaic."""

    description: Optional[str] = "Pipeline for Classical Mandaic"
    glottolog_id: Optional[str] = "clas1253"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalMandaicSentenceSplittingProcess,
            ClassicalMandaicGenAIMorphosyntaxProcess,
            ClassicalMandaicGenAIDependencyProcess,
        ]
    )


class HatranGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Hatran."""

    description: Optional[str] = "Pipeline for Hatran"
    glottolog_id: Optional[str] = "hatr1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HatranSentenceSplittingProcess,
            HatranGenAIMorphosyntaxProcess,
            HatranGenAIDependencyProcess,
        ]
    )


class JewishBabylonianAramaicGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Jewish Babylonian Aramaic."""

    description: Optional[str] = "Pipeline for Jewish Babylonian Aramaic"
    glottolog_id: Optional[str] = "jewi1240"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            JewishBabylonianAramaicSentenceSplittingProcess,
            JewishBabylonianAramaicGenAIMorphosyntaxProcess,
            JewishBabylonianAramaicGenAIDependencyProcess,
        ]
    )


class SamalianGenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Samʾalian."""

    description: Optional[str] = "Pipeline for Samʾalian"
    glottolog_id: Optional[str] = "sama1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SamalianSentenceSplittingProcess,
            SamalianGenAIMorphosyntaxProcess,
            SamalianGenAIDependencyProcess,
        ]
    )


MAP_LANGUAGE_CODE_TO_STANZA_PIPELINE: dict[str, type[Pipeline]] = {
    # Seed a few languages where Stanza has robust models
    "lati1261": LatinStanzaPipeline,
    "anci1242": AncientGreekStanzaPipeline,
    "chur1257": ChurchSlavonicStanzaPipeline,
    "oldf1239": OldFrenchStanzaPipeline,
    "goth1244": GothicStanzaPipeline,
    "lite1248": LiteraryChineseStanzaPipeline,
    "olde1238": OldEnglishStanzaPipeline,
    "otto1234": OttomanTurkishStanzaPipeline,
    "clas1256": ClassicalArmenianStanzaPipeline,
    "copt1239": CopticStanzaPipeline,
    "oldr1238": OldRussianStanzaPipeline,  # Old East Slavic
}


MAP_LANGUAGE_CODE_TO_SPACY_PIPELINE: dict[str, type[Pipeline]] = dict()


MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE: dict[str, type[Pipeline]] = {
    # Indo-European family
    ## Italic
    "lati1261": LatinGenAIPipeline,
    "oldf1239": OldFrenchGenAIPipeline,
    "midd1316": MiddleFrenchGenAIPipeline,
    # Other Romance languages
    ## Hellenic
    "anci1242": AncientGreekGenAIPipeline,
    # Mycenaean Greek (Linear B tablets, ca. 1400–1200 BCE).
    # Medieval/Byzantine Greek
    "oldi1245": EarlyIrishGenAIPipeline,
    "oldw1239": OldMiddleWelshGenAIPipeline,
    "bret1244": MiddleBretonGenAIPipeline,
    "corn1251": CornishGenAIPipeline,
    ## Germanic
    # Proto-Norse
    "goth1244": GothicGenAIPipeline,
    "oldh1241": OldHighGermanGenAIPipeline,
    "midd1343": MiddleHighGermanGenAIPipeline,
    "oldn1244": OldNorseGenAIPipeline,
    "olde1238": OldEnglishGenAIPipeline,
    "midd1317": MiddleEnglishGenAIPipeline,
    ## Balto-Slavic
    "chur1257": ChurchSlavonicGenAIPipeline,
    "prus1238": OldPrussianGenAIPipeline,
    "lith1251": LithuanianGenAIPipeline,
    "latv1249": LatvianGenAIPipeline,
    "gheg1238": AlbanianGenAIPipeline,
    ## Armenian, Earliest texts: 5th c. CE (Bible translation by Mesrop Mashtots, who created the script)
    "clas1256": ClassicalArmenianGenAIPipeline,
    "midd1364": MiddleArmenianGenAIPipeline,
    # Note this is only a parent, not true languoid
    ## Anatolian
    "hitt1242": HittiteGenAIPipeline,
    "cune1239": CuneiformLuwianGenAIPipeline,
    "hier1240": HieroglyphicLuwianGenAIPipeline,
    "lyci1241": LycianAGenAIPipeline,
    "lydi1241": LydianGenAIPipeline,
    "pala1331": PalaicGenAIPipeline,
    "cari1274": CarianGenAIPipeline,
    ## Tocharian
    "tokh1242": TocharianAGenAIPipeline,
    "tokh1243": TocharianBGenAIPipeline,
    ## Indo-Iranian
    ## Iranian languages
    ### SW Iranian
    "oldp1254": OldPersianGenAIPipeline,
    "pahl1241": MiddlePersianGenAIPipeline,
    ### NW Iranian
    "part1239": ParthianGenAIPipeline,
    ### E Iranian
    "aves1237": AvestanGenAIPipeline,
    "bact1239": BactrianGenAIPipeline,
    "sogd1245": SogdianGenAIPipeline,
    "khot1251": KhotaneseGenAIPipeline,
    "tums1237": TumshuqeseGenAIPipeline,
    # Indo-Aryan (Indic): Sanskrit (Vedic & Classical), Prakrits, Pali, later medieval languages (Hindi, Bengali, etc.)
    ## Old Indo-Aryan
    "vedi1234": VedicSanskritGenAIPipeline,
    "clas1258": ClassicalSanskritGenAIPipeline,
    # Prakrits (Middle Indo-Aryan, ca. 500 BCE–500 CE)
    "pali1273": PaliGenAIPipeline,
    # Ardhamāgadhī, Śaurasenī, Mahārāṣṭrī, etc. — languages of Jain/Buddhist texts and early drama.
    # ? Glotto says alt_name for Pali; Ardhamāgadhī, literary language associated with Magadha (eastern India); Jain canonical texts (the Āgamas) are written primarily in Ardhamāgadhī
    "saur1252": SauraseniPrakritGenAIPipeline,
    "maha1305": MaharastriPrakritGenAIPipeline,
    "maga1260": MagadhiPrakritGenAIPipeline,
    "gand1259": GandhariGenAIPipeline,  ## Middle Indo-Aryan
    # "Maithili": "mait1250"; Apabhraṃśa; "Apabhramsa" is alt_name; (500–1200 CE); Bridges Prakrits → New Indo-Aryan
    ## New Indo-Aryan
    ## Medieval languages (~1200 CE onward):
    # Early forms of Hindi, Bengali, Gujarati, Marathi, Punjabi, Oriya, Sinhala, etc
    # North-Western / Hindi Belt
    "hind1269": HindiGenAIPipeline,
    "khad1239": KhariBoliGenAIPipeline,
    "braj1242": BrajGenAIPipeline,
    "awad1243": AwadhiGenAIPipeline,
    "urdu1245": UrduGenAIPipeline,
    # Eastern Indo-Aryan
    "beng1280": BengaliGenAIPipeline,
    "oriy1255": OdiaGenAIPipeline,
    "assa1263": AssameseGenAIPipeline,
    # Western Indo-Aryan
    "guja1252": GujaratiGenAIPipeline,
    "mara1378": MarathiGenAIPipeline,
    # Southern Indo-Aryan / adjacency
    "sinh1246": SinhalaGenAIPipeline,
    # Northwestern frontier
    "panj1256": EasternPanjabiGenAIPipeline,
    "sind1272": SindhiGenAIPipeline,
    "kash1277": KashmiriGenAIPipeline,
    "bagr1243": BagriGenAIPipeline,
    # Afroasiatic family
    ## Semitic languages
    ### East Semitic
    "akka1240": AkkadianGenAIPipeline,
    # Eblaite
    ### West Semitic
    "ugar1238": UgariticGenAIPipeline,
    "phoe1239": PhoenicianGenAIPipeline,
    "moab1234": MoabiteGenAIPipeline,
    "ammo1234": AmmoniteGenAIPipeline,
    "edom1234": EdomiteGenAIPipeline,
    "anci1244": BiblicalHebrewGenAIPipeline,
    # Medieval Hebrew: No Glottolog
    # "moab1234": Moabite
    # "ammo1234": Ammonite
    # "edom1234": Edomite
    # Old Aramaic (ca. 1000–700 BCE, inscriptions).
    # "olda1246": "Old Aramaic (up to 700 BCE)",
    # "Old Aramaic-Sam'alian": "olda1245"
    "impe1235": ImperialAramaicGenAIPipeline,
    "olda1246": OldAramaicGenAIPipeline,
    "olda1245": OldAramaicSamalianGenAIPipeline,
    "midd1366": MiddleAramaicGenAIPipeline,
    "clas1253": ClassicalMandaicGenAIPipeline,
    "hatr1234": HatranGenAIPipeline,
    "jewi1240": JewishBabylonianAramaicGenAIPipeline,
    "sama1234": SamalianGenAIPipeline,
    # "midd1366": Middle Aramaic (200 BCE – 700 CE), includes Biblical Aramaic, Palmyrene, Nabataean, Targumic Aramaic.
    # Eastern Middle Aramaic
    ##  Classical Mandaic, Hatran, Jewish Babylonian Aramaic dialects, and Classical Syriac
    "clas1252": ClassicalSyriacGenAIPipeline,
    ### NW Semitic
    ## South Semitic
    # Old South Arabian (OSA)
    "geez1241": GeezGenAIPipeline,
    ### Central Semitic (bridge between NW and South)
    # Pre-Islamic Arabic
    "clas1259": ClassicalArabicGenAIPipeline,  # Dialect
    # Glotto doesn't have medieval arabic; Medieval Arabic: scientific, philosophical, historical works dominate much of the Islamic Golden Age corpus.
    ## Egyptian languages
    "olde1242": OldEgyptianGenAIPipeline,
    "midd1369": MiddleEgyptianGenAIPipeline,
    "late1256": LateEgyptianGenAIPipeline,
    "demo1234": DemoticGenAIPipeline,
    "copt1239": CopticGenAIPipeline,
    ## Berber
    "numi1241": NumidianGenAIPipeline,
    "tait1247": TaitaGenAIPipeline,
    ## Chadic
    # ; "haus1257": "Hausa"; Hausa; Essentially oral until medieval period, when Hausa is written in Ajami (Arabic script).
    "haus1257": HausaGenAIPipeline,
    "lite1248": LiteraryChineseGenAIPipeline,
    "clas1254": ClassicalTibetanPipeline,
    # Sino-Tibetan family
    # | **Early Vernacular Chinese (Baihua)**   | ca. 10th – 18th c. CE | *(under `clas1255`)* |
    # | **Old Tibetan**                         | 7th – 10th c. CE     | *(not separately coded)* |
    "oldc1244": OldChineseGenAIPipeline,
    "midd1344": MiddleChineseGenAIPipeline,
    "clas1255": BaihuaChineseGenAIPipeline,
    "oldb1235": OldBurmeseGenAIPipeline,
    "nucl1310": ClassicalBurmeseGenAIPipeline,
    "tang1334": TangutGenAIPipeline,
    "newa1246": NewarGenAIPipeline,
    "mani1292": MeiteiGenAIPipeline,
    "sgaw1245": SgawKarenGenAIPipeline,
    # Mongolic family
    "mong1329": MiddleMongolGenAIPipeline,
    "mong1331": ClassicalMongolianGenAIPipeline,  #  TODO: No glottolog broken
    "mogh1245": MogholiGenAIPipeline,
    # Altaic-Adj.
    "jurc1239": OldJurchenGenAIPipeline,
    # Japonic
    "japo1237": OldJapaneseGenAIPipeline,
    # Uralic
    "oldh1242": OldHungarianGenAIPipeline,
    # Turkic
    "chag1247": ChagataiGenAIPipeline,
    "oldu1238": OldTurkicGenAIPipeline,
    # TODO: Make pipeline for Ottoman Turkish
    # "otto1234": OttomanTurkishGenAIPipeline,
    # Dravidian
    "oldt1248": OldTamilGenAIPipeline,
    # Pre-Modern Literate Language Families (Non-Euro/Afroasiatic/Sino-Tibetan/Mongolic)
    # | Family         | Language / Stage           | Approx. Period      | Glottocode     |
    # |----------------|-----------------------------|----------------------|----------------|
    # | Dravidian      | Old Tamil                   | ca. 300 BCE–300 CE   | `oldt1248`     |
    # |                | Middle Tamil                | medieval             | *(not coded)*  |
    # |                | Old Kannada                 | from 5th c. CE       | *(not coded)*  |
    # |                | Old Telugu                  | from 6th c. CE       | *(not coded)*  |
    # |                | Old Malayalam               | from 13th c. CE      | *(not coded)*  |
    # | Turkic         | Old Turkic                  | 8th–10th c. CE       | `oldu1238`     |
    # |                | Chagatai                    | 15th–18th c. CE      | `chag1247`     |
    # | Uralic         | Old Hungarian               | 12th–13th c. CE      | `oldh1242`     |
    # | Koreanic       | Old Korean                  | 7th–10th c. CE       | *(not coded)*  |
    # |                | Middle Korean               | 15th c. onward       | *(not coded)*  |
    # | Japonic        | Old Japanese                | 8th c. CE            | `japo1237`     |
    # | Altaic-Adj.    | Old Jurchen                 | 12th–13th c. CE      | *`jurc1239`*  |
    # |                | Manchu                      | 17th–18th c. CE      | *(not coded)*  |
    # | Austroasiatic  | Old Mon                     | from 6th c. CE       | *(not coded)*  |
    # |                | Old Khmer                   | from 7th c. CE       | *(not coded)*  |
    # | Austronesian   | Old Javanese (Kawi)         | from 8th c. CE       | *(not coded)*  |
    # |                | Classical Malay             | from 7th c. CE onward| *(not coded)*  |
    # | Tai–Kadai      | Old Thai                    | from 13th c. CE      | *(not coded)*  |
}
