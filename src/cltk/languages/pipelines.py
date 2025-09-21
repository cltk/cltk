"""Language pipelines and mappings.

This module defines many language‑specific pipeline classes (mostly
OpenAI‑backed) and central mappings from Glottolog codes to default pipelines.
Pipelines are lightweight containers that list a small sequence of processes
such as normalization, sentence splitting, and generative annotation.
"""

from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from cltk.core.data_types import Pipeline
from cltk.core.logging_utils import plog
from cltk.dependency.processes import (
    AkkadianOpenAIDependencyProcess,
    AlbanianOpenAIDependencyProcess,
    AmmoniteOpenAIDependencyProcess,
    AncientGreekOpenAIDependencyProcess,
    AssameseOpenAIDependencyProcess,
    AvestanOpenAIDependencyProcess,
    AwadhiOpenAIDependencyProcess,
    BactrianOpenAIDependencyProcess,
    BagriOpenAIDependencyProcess,
    BaihuaChineseOpenAIDependencyProcess,
    BengaliOpenAIDependencyProcess,
    BiblicalHebrewOpenAIDependencyProcess,
    BrajOpenAIDependencyProcess,
    CarianOpenAIDependencyProcess,
    ChagataiOpenAIDependencyProcess,
    ChurchSlavicOpenAIDependencyProcess,
    ClassicalArabicOpenAIDependencyProcess,
    ClassicalArmenianOpenAIDependencyProcess,
    ClassicalBurmeseOpenAIDependencyProcess,
    ClassicalMandaicOpenAIDependencyProcess,
    ClassicalMongolianOpenAIDependencyProcess,
    ClassicalSanskritOpenAIDependencyProcess,
    ClassicalSyriacOpenAIDependencyProcess,
    ClassicalTibetanOpenAIDependencyProcess,
    CopticOpenAIDependencyProcess,
    CuneiformLuwianOpenAIDependencyProcess,
    DemoticOpenAIDependencyProcess,
    EarlyIrishOpenAIDependencyProcess,
    EasternPanjabiOpenAIDependencyProcess,
    EdomiteOpenAIDependencyProcess,
    GandhariOpenAIDependencyProcess,
    GeezOpenAIDependencyProcess,
    GothicOpenAIDependencyProcess,
    GujaratiOpenAIDependencyProcess,
    HatranOpenAIDependencyProcess,
    HausaOpenAIDependencyProcess,
    HieroglyphicLuwianOpenAIDependencyProcess,
    HindiOpenAIDependencyProcess,
    HittiteOpenAIDependencyProcess,
    JewishBabylonianAramaicOpenAIDependencyProcess,
    KashmiriOpenAIDependencyProcess,
    KhariBoliOpenAIDependencyProcess,
    KhotaneseOpenAIDependencyProcess,
    LateEgyptianOpenAIDependencyProcess,
    LatinOpenAIDependencyProcess,
    LatvianOpenAIDependencyProcess,
    LiteraryChineseOpenAIDependencyProcess,
    LithuanianOpenAIDependencyProcess,
    LycianAOpenAIDependencyProcess,
    LydianOpenAIDependencyProcess,
    MagadhiPrakritOpenAIDependencyProcess,
    MaharastriPrakritOpenAIDependencyProcess,
    MarathiOpenAIDependencyProcess,
    MeiteiOpenAIDependencyProcess,
    MiddleAramaicOpenAIDependencyProcess,
    MiddleArmenianOpenAIDependencyProcess,
    MiddleBretonOpenAIDependencyProcess,
    MiddleChineseOpenAIDependencyProcess,
    MiddleCornishOpenAIDependencyProcess,
    MiddleEgyptianOpenAIDependencyProcess,
    MiddleEnglishOpenAIDependencyProcess,
    MiddleFrenchOpenAIDependencyProcess,
    MiddleHighGermanOpenAIDependencyProcess,
    MiddleMongolOpenAIDependencyProcess,
    MiddlePersianOpenAIDependencyProcess,
    MoabiteOpenAIDependencyProcess,
    MogholiOpenAIDependencyProcess,
    NewarOpenAIDependencyProcess,
    NumidianOpenAIDependencyProcess,
    OdiaOpenAIDependencyProcess,
    OfficialAramaicOpenAIDependencyProcess,
    OldAramaicOpenAIDependencyProcess,
    OldAramaicSamalianOpenAIDependencyProcess,
    OldBurmeseOpenAIDependencyProcess,
    OldChineseOpenAIDependencyProcess,
    OldEgyptianOpenAIDependencyProcess,
    OldEnglishOpenAIDependencyProcess,
    OldFrenchOpenAIDependencyProcess,
    OldHighGermanOpenAIDependencyProcess,
    OldHungarianOpenAIDependencyProcess,
    OldJapaneseOpenAIDependencyProcess,
    OldJurchenOpenAIDependencyProcess,
    OldMiddleWelshOpenAIDependencyProcess,
    OldNorseOpenAIDependencyProcess,
    OldPersianOpenAIDependencyProcess,
    OldPrussianOpenAIDependencyProcess,
    OldTamilOpenAIDependencyProcess,
    OldTurkicOpenAIDependencyProcess,
    PalaicOpenAIDependencyProcess,
    PaliOpenAIDependencyProcess,
    ParthianOpenAIDependencyProcess,
    PhoenicianOpenAIDependencyProcess,
    SamalianOpenAIDependencyProcess,
    SauraseniPrakritOpenAIDependencyProcess,
    SgawKarenOpenAIDependencyProcess,
    SindhiOpenAIDependencyProcess,
    SinhalaOpenAIDependencyProcess,
    SogdianOpenAIDependencyProcess,
    TaitaOpenAIDependencyProcess,
    TangutOpenAIDependencyProcess,
    TokharianAOpenAIDependencyProcess,
    TokharianBOpenAIDependencyProcess,
    TumshuqeseOpenAIDependencyProcess,
    UgariticOpenAIDependencyProcess,
    UrduOpenAIDependencyProcess,
    VedicSanskritOpenAIDependencyProcess,
)
from cltk.morphosyntax.processes import (
    AkkadianOpenAIMorphosyntaxProcess,
    AlbanianOpenAIMorphosyntaxProcess,
    AmmoniteOpenAIMorphosyntaxProcess,
    AncientGreekOpenAIMorphosyntaxProcess,
    AssameseOpenAIMorphosyntaxProcess,
    AvestanOpenAIMorphosyntaxProcess,
    AwadhiOpenAIMorphosyntaxProcess,
    BactrianOpenAIMorphosyntaxProcess,
    BagriOpenAIMorphosyntaxProcess,
    BaihuaChineseOpenAIMorphosyntaxProcess,
    BengaliOpenAIMorphosyntaxProcess,
    BiblicalHebrewOpenAIMorphosyntaxProcess,
    BrajOpenAIMorphosyntaxProcess,
    CarianOpenAIMorphosyntaxProcess,
    ChagataiOpenAIMorphosyntaxProcess,
    ChurchSlavicOpenAIMorphosyntaxProcess,
    ClassicalArabicOpenAIMorphosyntaxProcess,
    ClassicalArmenianOpenAIMorphosyntaxProcess,
    ClassicalBurmeseOpenAIMorphosyntaxProcess,
    ClassicalMandaicOpenAIMorphosyntaxProcess,
    ClassicalMongolianOpenAIMorphosyntaxProcess,
    ClassicalSanskritOpenAIMorphosyntaxProcess,
    ClassicalSyriacOpenAIMorphosyntaxProcess,
    ClassicalTibetanOpenAIMorphosyntaxProcess,
    CopticOpenAIMorphosyntaxProcess,
    CuneiformLuwianOpenAIMorphosyntaxProcess,
    DemoticOpenAIMorphosyntaxProcess,
    EarlyIrishOpenAIMorphosyntaxProcess,
    EasternPanjabiOpenAIMorphosyntaxProcess,
    EdomiteOpenAIMorphosyntaxProcess,
    GandhariOpenAIMorphosyntaxProcess,
    GeezOpenAIMorphosyntaxProcess,
    GothicOpenAIMorphosyntaxProcess,
    GujaratiOpenAIMorphosyntaxProcess,
    HatranOpenAIMorphosyntaxProcess,
    HausaOpenAIMorphosyntaxProcess,
    HieroglyphicLuwianOpenAIMorphosyntaxProcess,
    HindiOpenAIMorphosyntaxProcess,
    HittiteOpenAIMorphosyntaxProcess,
    JewishBabylonianAramaicOpenAIMorphosyntaxProcess,
    KashmiriOpenAIMorphosyntaxProcess,
    KhariBoliOpenAIMorphosyntaxProcess,
    KhotaneseOpenAIMorphosyntaxProcess,
    LateEgyptianOpenAIMorphosyntaxProcess,
    LatinOpenAIMorphosyntaxProcess,
    LatvianOpenAIMorphosyntaxProcess,
    LiteraryChineseOpenAIMorphosyntaxProcess,
    LithuanianOpenAIMorphosyntaxProcess,
    LycianAOpenAIMorphosyntaxProcess,
    LydianOpenAIMorphosyntaxProcess,
    MagadhiPrakritOpenAIMorphosyntaxProcess,
    MaharastriPrakritOpenAIMorphosyntaxProcess,
    MarathiOpenAIMorphosyntaxProcess,
    MeiteiOpenAIMorphosyntaxProcess,
    MiddleAramaicOpenAIMorphosyntaxProcess,
    MiddleArmenianOpenAIMorphosyntaxProcess,
    MiddleBretonOpenAIMorphosyntaxProcess,
    MiddleChineseOpenAIMorphosyntaxProcess,
    MiddleCornishOpenAIMorphosyntaxProcess,
    MiddleEgyptianOpenAIMorphosyntaxProcess,
    MiddleEnglishOpenAIMorphosyntaxProcess,
    MiddleFrenchOpenAIMorphosyntaxProcess,
    MiddleHighGermanOpenAIMorphosyntaxProcess,
    MiddleMongolOpenAIMorphosyntaxProcess,
    MiddlePersianOpenAIMorphosyntaxProcess,
    MoabiteOpenAIMorphosyntaxProcess,
    MogholiOpenAIMorphosyntaxProcess,
    NewarOpenAIMorphosyntaxProcess,
    NumidianOpenAIMorphosyntaxProcess,
    OdiaOpenAIMorphosyntaxProcess,
    OfficialAramaicOpenAIMorphosyntaxProcess,
    OldAramaicOpenAIMorphosyntaxProcess,
    OldAramaicSamalianOpenAIMorphosyntaxProcess,
    OldBurmeseOpenAIMorphosyntaxProcess,
    OldChineseOpenAIMorphosyntaxProcess,
    OldEgyptianOpenAIMorphosyntaxProcess,
    OldEnglishOpenAIMorphosyntaxProcess,
    OldFrenchOpenAIMorphosyntaxProcess,
    OldHighGermanOpenAIMorphosyntaxProcess,
    OldHungarianOpenAIMorphosyntaxProcess,
    OldJapaneseOpenAIMorphosyntaxProcess,
    OldJurchenOpenAIMorphosyntaxProcess,
    OldMiddleWelshOpenAIMorphosyntaxProcess,
    OldNorseOpenAIMorphosyntaxProcess,
    OldPersianOpenAIMorphosyntaxProcess,
    OldPrussianOpenAIMorphosyntaxProcess,
    OldTamilOpenAIMorphosyntaxProcess,
    OldTurkicOpenAIMorphosyntaxProcess,
    PalaicOpenAIMorphosyntaxProcess,
    PaliOpenAIMorphosyntaxProcess,
    ParthianOpenAIMorphosyntaxProcess,
    PhoenicianOpenAIMorphosyntaxProcess,
    SamalianOpenAIMorphosyntaxProcess,
    SauraseniPrakritOpenAIMorphosyntaxProcess,
    SgawKarenOpenAIMorphosyntaxProcess,
    SindhiOpenAIMorphosyntaxProcess,
    SinhalaOpenAIMorphosyntaxProcess,
    SogdianOpenAIMorphosyntaxProcess,
    TaitaOpenAIMorphosyntaxProcess,
    TangutOpenAIMorphosyntaxProcess,
    TokharianAOpenAIMorphosyntaxProcess,
    TokharianBOpenAIMorphosyntaxProcess,
    TumshuqeseOpenAIMorphosyntaxProcess,
    UgariticOpenAIMorphosyntaxProcess,
    UrduOpenAIMorphosyntaxProcess,
    VedicSanskritOpenAIMorphosyntaxProcess,
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


class AkkadianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Akkadian."""

    description: Optional[str] = "Pipeline for the Akkadian language"
    glottolog_id: Optional[str] = "akka1240"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AkkadianSentenceSplittingProcess,
            AkkadianOpenAIMorphosyntaxProcess,
            AkkadianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        plog(self).debug(
            f"Initializing AkkadianOpenAIPipeline with language: {self.language.name}"
        )
        plog(self).info("AkkadianOpenAIPipeline created.")


class ClassicalArabicOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Arabic."""

    description: Optional[str] = "Pipeline for the Arabic language"
    glottolog_id: Optional[str] = "clas1259"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalArabicSentenceSplittingProcess,
            ClassicalArabicOpenAIMorphosyntaxProcess,
            ClassicalArabicOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing ArabicOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("ArabicOpenAIPipeline created.")


#
class ClassicalSyriacOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Syriac."""

    description: Optional[str] = "Pipeline for the Classical Syriac language"
    glottolog_id: Optional[str] = "clas1252"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalSyriacSentenceSplittingProcess,
            ClassicalSyriacOpenAIMorphosyntaxProcess,
            ClassicalSyriacOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        plog(self).debug(
            f"Initializing ClassicalSyriacOpenAIPipeline with language: {self.language.name}"
        )
        plog(self).info("ClassicalSyriacOpenAIPipeline created.")


# ClassicalTibetanPipeline
class ClassicalTibetanPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Tibetan."""

    description: Optional[str] = "Pipeline for the Classical Tibetan language"
    glottolog_id: Optional[str] = "clas1254"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalTibetanSentenceSplittingProcess,
            ClassicalTibetanOpenAIMorphosyntaxProcess,
            ClassicalTibetanOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        plog(self).debug(
            f"Initializing ClassicalTibetanOpenAIPipeline with language: {self.language.name}"
        )
        plog(self).info("ClassicalTibetanOpenAIPipeline created.")


class CopticOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Coptic."""

    description: Optional[str] = "OpenAI Pipeline for the Coptic language."
    glottolog_id: Optional[str] = "copt1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CopticSentenceSplittingProcess,
            CopticOpenAIMorphosyntaxProcess,
            CopticOpenAIDependencyProcess,
        ]
    )


class GothicOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic."""

    description: Optional[str] = "Pipeline for the Gothic language"
    glottolog_id: Optional[str] = "goth1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GothicSentenceSplittingProcess,
            GothicOpenAIMorphosyntaxProcess,
            GothicOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GothicOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("GothicOpenAIPipeline created.")


class AncientGreekOpenAIPipeline(Pipeline):
    """Pipeline for Ancient Greek using normalization and OpenAI annotation only."""

    description: Optional[str] = "Pipeline for Ancient Greek with OpenAI annotation"
    glottolog_id: Optional[str] = "anci1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            # AncientGreekNormalizeProcess,
            MultilingualNormalizeProcess,
            AncientGreekSentenceSplittingProcess,
            AncientGreekOpenAIMorphosyntaxProcess,
            AncientGreekOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GreekOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("GreekOpenAIPipeline created.")


class BiblicalHebrewOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Hebrew."""

    description: Optional[str] = "Pipeline for the Ancient Hebrew language."
    glottolog_id: Optional[str] = "anci1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AncientHebrewSentenceSplittingProcess,
            BiblicalHebrewOpenAIMorphosyntaxProcess,
            BiblicalHebrewOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(f"Initializing LatinPipeline with language: {self.language}")
        plog(self).info("LatinPipeline created.")


class LatinOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Latin."""

    description: Optional[str] = "OpenAI Pipeline for the Latin language."
    glottolog_id: Optional[str] = "lati1261"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            # LatinNormalizeProcess,
            MultilingualNormalizeProcess,
            LatinSentenceSplittingProcess,
            LatinOpenAIMorphosyntaxProcess,
            LatinOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(f"Initializing LatinPipeline with language: {self.language}")
        plog(self).info("LatinPipeline created.")


class MiddleEnglishOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle English."""

    description: Optional[str] = "Pipeline for the Middle English language"
    glottolog_id: Optional[str] = "midd1317"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleEnglishSentenceSplittingProcess,
            MiddleEnglishOpenAIMorphosyntaxProcess,
            MiddleEnglishOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleEnglishOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleEnglishOpenAIPipeline created.")


class MiddleFrenchOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle French."""

    description: Optional[str] = "Pipeline for the Middle French language"
    glottolog_id: Optional[str] = "midd1316"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleFrenchSentenceSplittingProcess,
            MiddleFrenchOpenAIMorphosyntaxProcess,
            MiddleFrenchOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleFrenchOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleFrenchOpenAIPipeline created.")


class MiddlePersianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Persian (Pahlavi)."""

    description: Optional[str] = "Pipeline for the Middle Persian (Pahlavi) language"
    glottolog_id: Optional[str] = "pahl1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddlePersianSentenceSplittingProcess,
            MiddlePersianOpenAIMorphosyntaxProcess,
            MiddlePersianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddlePersianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddlePersianOpenAIPipeline created.")


class ImperialAramaicOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Official Aramaic."""

    description: Optional[str] = "OpenAI Pipeline for the Official Aramaic language."
    glottolog_id: Optional[str] = "impe1235"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OfficialAramaicSentenceSplittingProcess,
            OfficialAramaicOpenAIMorphosyntaxProcess,
            OfficialAramaicOpenAIDependencyProcess,
        ]
    )


class ChurchSlavonicOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for (Old) Church Slavonic."""

    description: Optional[str] = "Pipeline for the Church Slavonic language"
    glottolog_id: Optional[str] = "chur1257"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ChurchSlavonicSentenceSplittingProcess,
            ChurchSlavicOpenAIMorphosyntaxProcess,
            ChurchSlavicOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing ChurchSlavonicOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("ChurchSlavonicOpenAIPipeline")


class OldEnglishOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old English."""

    description: Optional[str] = "Pipeline for the Old English language"
    glottolog_id: Optional[str] = "olde1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldEnglishSentenceSplittingProcess,
            OldEnglishOpenAIMorphosyntaxProcess,
            OldEnglishOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        plog(self).debug(
            f"Initializing OldEnglishOpenAIPipeline with language: {self.language.name}"
        )
        plog(self).info("OldEnglishOpenAIPipeline created.")


class OldFrenchOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old French."""

    description: Optional[str] = "Pipeline for the Old French language"
    glottolog_id: Optional[str] = "oldf1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldFrenchSentenceSplittingProcess,
            OldFrenchOpenAIMorphosyntaxProcess,
            OldFrenchOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldFrenchOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldFrenchOpenAIPipeline created.")


class OldNorseOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Norse."""

    description: Optional[str] = "Pipeline for the Old Norse language"
    glottolog_id: Optional[str] = "oldn1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldNorseSentenceSplittingProcess,
            OldNorseOpenAIMorphosyntaxProcess,
            OldNorseOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldNorseOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldNorseOpenAIPipeline created.")


class PaliOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Pali."""

    description: Optional[str] = "Pipeline for the Pali language"
    glottolog_id: Optional[str] = "pali1273"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PaliSentenceSplittingProcess,
            PaliOpenAIMorphosyntaxProcess,
            PaliOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(f"Initializing PaliPipeline with language: {self.language}")
        plog(self).info("PaliPipeline created.")


class ClassicalSanskritOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Sanskrit."""

    description: Optional[str] = "Pipeline for the Classical Sanskrit language"
    glottolog_id: Optional[str] = "vedi1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalSanskritSentenceSplittingProcess,
            ClassicalSanskritOpenAIMorphosyntaxProcess,
            ClassicalSanskritOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing ClassicalSanskritOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("ClassicalSanskritOpenAIPipeline created.")


class VedicSanskritOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Vedic Sanskrit."""

    description: Optional[str] = "Pipeline for the Vedic Sanskrit language"
    glottolog_id: Optional[str] = "clas1258"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            VedicSanskritSentenceSplittingProcess,
            VedicSanskritOpenAIMorphosyntaxProcess,
            VedicSanskritOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing VedicSanskritOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("VedicSanskritOpenAIPipeline created.")


class OldHighGermanOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old High German."""

    description: Optional[str] = "Pipeline for the Old High German language"
    glottolog_id: Optional[str] = "oldh1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            # MiddleHighGermanTokenizationProcess,  # Substitute with OldHighGermanTokenizationProcess if available
            OldHighGermanSentenceSplittingProcess,
            OldHighGermanOpenAIMorphosyntaxProcess,
            OldHighGermanOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldHighGermanOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldHighGermanOpenAIPipeline created.")


class MiddleHighGermanOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle High German."""

    description: Optional[str] = "Pipeline for the Middle High German language"
    glottolog_id: Optional[str] = "midd1343"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleHighGermanSentenceSplittingProcess,
            MiddleHighGermanOpenAIMorphosyntaxProcess,
            MiddleHighGermanOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleHighGermanOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleHighGermanOpenAIPipeline created.")


class LiteraryChineseOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Literary (or Classical) Chinese."""

    description: Optional[str] = (
        "Pipeline for the Literary (or Classical) Chinese language"
    )
    glottolog_id: Optional[str] = "lite1248"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LiteraryChineseSentenceSplittingProcess,
            LiteraryChineseOpenAIMorphosyntaxProcess,
            LiteraryChineseOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LiteraryChineseOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("LiteraryChineseOpenAIPipeline created.")


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


class DemoticOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Demotic Egyptian."""

    description: Optional[str] = "Pipeline for the Demotic Egyptian language"
    glottolog_id: Optional[str] = "demo1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            DemoticSentenceSplittingProcess,
            DemoticOpenAIMorphosyntaxProcess,
            DemoticOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing DemoticOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("DemoticOpenAIPipeline created.")


class HittiteOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Hittite."""

    description: Optional[str] = "Pipeline for the Hittite language"
    glottolog_id: Optional[str] = "hitt1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HittiteSentenceSplittingProcess,
            HittiteOpenAIMorphosyntaxProcess,
            HittiteOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing HittiteOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("HittiteOpenAIPipeline created.")


class TocharianAOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Tocharian A."""

    description: Optional[str] = "Pipeline for the Tocharian A language"
    glottolog_id: Optional[str] = "toch1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TocharianASentenceSplittingProcess,
            TokharianAOpenAIMorphosyntaxProcess,
            TokharianAOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing TocharianAOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("TocharianAOpenAIPipeline created.")


class TocharianBOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Tocharian B."""

    description: Optional[str] = "Pipeline for the Tocharian B language"
    glottolog_id: Optional[str] = "toch1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TocharianBSentenceSplittingProcess,
            TokharianBOpenAIMorphosyntaxProcess,
            TokharianBOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing TocharianBOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("TocharianBOpenAIPipeline created.")


class AvestanOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Avestan."""

    description: Optional[str] = "Pipeline for the Avestan language"
    glottolog_id: Optional[str] = "aves1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AvestanSentenceSplittingProcess,
            AvestanOpenAIMorphosyntaxProcess,
            AvestanOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing AvestanOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("AvestanOpenAIPipeline created.")


class BactrianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Bactrian."""

    description: Optional[str] = "Pipeline for the Bactrian language"
    glottolog_id: Optional[str] = "bact1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BactrianSentenceSplittingProcess,
            BactrianOpenAIMorphosyntaxProcess,
            BactrianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing BactrianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("BactrianOpenAIPipeline created.")


class SogdianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Sogdian."""

    description: Optional[str] = "Pipeline for the Sogdian language"
    glottolog_id: Optional[str] = "sogd1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SogdianSentenceSplittingProcess,
            SogdianOpenAIMorphosyntaxProcess,
            SogdianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing SogdianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("SogdianOpenAIPipeline created.")


class KhotaneseOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Khotanese."""

    description: Optional[str] = "Pipeline for the Khotanese language"
    glottolog_id: Optional[str] = "khot1251"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            KhotaneseSentenceSplittingProcess,
            KhotaneseOpenAIMorphosyntaxProcess,
            KhotaneseOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing KhotaneseOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("KhotaneseOpenAIPipeline created.")


class TumshuqeseOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Tumshuqese."""

    description: Optional[str] = "Pipeline for the Tumshuqese language"
    glottolog_id: Optional[str] = "tums1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TumshuqeseSentenceSplittingProcess,
            TumshuqeseOpenAIMorphosyntaxProcess,
            TumshuqeseOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing TumshuqeseOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("TumshuqeseOpenAIPipeline created.")


class OldPersianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Persian."""

    description: Optional[str] = "Pipeline for the Old Persian language"
    glottolog_id: Optional[str] = "oldp1254"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldPersianSentenceSplittingProcess,
            OldPersianOpenAIMorphosyntaxProcess,
            OldPersianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldPersianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldPersianOpenAIPipeline created.")


class EarlyIrishOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Irish."""

    description: Optional[str] = "Pipeline for the Old Irish language"
    glottolog_id: Optional[str] = "oldi1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            EarlyIrishSentenceSplittingProcess,
            EarlyIrishOpenAIMorphosyntaxProcess,
            EarlyIrishOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldIrishOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldIrishOpenAIPipeline created.")


class UgariticOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Ugaritic."""

    description: Optional[str] = "Pipeline for the Ugaritic language"
    glottolog_id: Optional[str] = "ugar1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            UgariticSentenceSplittingProcess,
            UgariticOpenAIMorphosyntaxProcess,
            UgariticOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing UgariticOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("UgariticOpenAIPipeline created.")


class PhoenicianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Phoenician (Punic)."""

    description: Optional[str] = "Pipeline for the Phoenician (Punic) language"
    glottolog_id: Optional[str] = "phoe1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PhoenicianSentenceSplittingProcess,
            PhoenicianOpenAIMorphosyntaxProcess,
            PhoenicianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing PhoenicianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("PhoenicianOpenAIPipeline created.")


class GeezOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Geʿez (Classical Ethiopic)."""

    description: Optional[str] = "Pipeline for the Geʿez (Classical Ethiopic) language"
    glottolog_id: Optional[str] = "geez1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GeezSentenceSplittingProcess,
            GeezOpenAIMorphosyntaxProcess,
            GeezOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GeezOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("GeezOpenAIPipeline created.")


class MiddleEgyptianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Egyptian."""

    description: Optional[str] = "Pipeline for the Middle Egyptian language"
    glottolog_id: Optional[str] = "midd1369"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleEgyptianSentenceSplittingProcess,
            MiddleEgyptianOpenAIMorphosyntaxProcess,
            MiddleEgyptianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleEgyptianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleEgyptianOpenAIPipeline created.")


class OldEgyptianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Egyptian."""

    description: Optional[str] = "Pipeline for the Old Egyptian language"
    glottolog_id: Optional[str] = "olde1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldEgyptianSentenceSplittingProcess,
            OldEgyptianOpenAIMorphosyntaxProcess,
            OldEgyptianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldEgyptianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldEgyptianOpenAIPipeline created.")


class LateEgyptianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Late Egyptian."""

    description: Optional[str] = "Pipeline for the Late Egyptian language"
    glottolog_id: Optional[str] = "late1256"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LateEgyptianSentenceSplittingProcess,
            LateEgyptianOpenAIMorphosyntaxProcess,
            LateEgyptianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LateEgyptianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("LateEgyptianOpenAIPipeline created.")


class ParthianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Parthian."""

    description: Optional[str] = "Pipeline for the Parthian language"
    glottolog_id: Optional[str] = "part1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ParthianSentenceSplittingProcess,
            ParthianOpenAIMorphosyntaxProcess,
            ParthianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LateEgyptianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("LateEgyptianOpenAIPipeline created.")


class OldMiddleWelshOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Welsh."""

    description: Optional[str] = "Pipeline for the Middle Welsh language"
    glottolog_id: Optional[str] = "oldw1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldMiddleWelshSentenceSplittingProcess,
            OldMiddleWelshOpenAIMorphosyntaxProcess,
            OldMiddleWelshOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleWelshOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleWelshOpenAIPipeline created.")


class MiddleBretonOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Breton."""

    description: Optional[str] = "Pipeline for the Middle Breton language"
    glottolog_id: Optional[str] = "oldb1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleBretonSentenceSplittingProcess,
            MiddleBretonOpenAIMorphosyntaxProcess,
            MiddleBretonOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleBretonOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("MiddleBretonOpenAIPipeline created.")


class CornishOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Cornish."""

    description: Optional[str] = "Pipeline for the Cornish language"
    glottolog_id: Optional[str] = "corn1251"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleCornishSentenceSplittingProcess,
            MiddleCornishOpenAIMorphosyntaxProcess,
            MiddleCornishOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing CornishOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("CornishOpenAIPipeline created.")


class OldPrussianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Prussian."""

    description: Optional[str] = "Pipeline for the Old Prussian language"
    glottolog_id: Optional[str] = "prus1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldPrussianSentenceSplittingProcess,
            OldPrussianOpenAIMorphosyntaxProcess,
            OldPrussianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OldPrussianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("OldPrussianOpenAIPipeline created.")


class LithuanianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Lithuanian."""

    description: Optional[str] = "Pipeline for the Lithuanian language"
    glottolog_id: Optional[str] = "lith1251"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LithuanianSentenceSplittingProcess,
            LithuanianOpenAIMorphosyntaxProcess,
            LithuanianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LithuanianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("LithuanianOpenAIPipeline created.")


class LatvianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Latvian."""

    description: Optional[str] = "Pipeline for the Latvian language"
    glottolog_id: Optional[str] = "latv1249"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LatvianSentenceSplittingProcess,
            LatvianOpenAIMorphosyntaxProcess,
            LatvianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LatvianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("LatvianOpenAIPipeline created.")


class AlbanianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Albanian."""

    description: Optional[str] = "Pipeline for the Albanian language"
    glottolog_id: Optional[str] = "gheg1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AlbanianSentenceSplittingProcess,
            AlbanianOpenAIMorphosyntaxProcess,
            AlbanianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing AlbanianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("AlbanianOpenAIPipeline created.")


class ClassicalArmenianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Armenian."""

    description: Optional[str] = "Pipeline for the Classical Armenian language"
    glottolog_id: Optional[str] = "clas1256"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalArmenianSentenceSplittingProcess,
            ClassicalArmenianOpenAIMorphosyntaxProcess,
            ClassicalArmenianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing ClassicalArmenianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("ClassicalArmenianOpenAIPipeline created.")


class MiddleArmenianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Armenian."""

    description: Optional[str] = "Pipeline for the Middle Armenian language"
    glottolog_id: Optional[str] = "midd1364"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleArmenianSentenceSplittingProcess,
            MiddleArmenianOpenAIMorphosyntaxProcess,
            MiddleArmenianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MiddleArmenianOpenAIPipeline with language: {self.language}"
        )


class CuneiformLuwianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Cuneiform Luwian."""

    description: Optional[str] = "Pipeline for the Cuneiform Luwian language"
    glottolog_id: Optional[str] = "cune1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CuneiformLuwianSentenceSplittingProcess,
            CuneiformLuwianOpenAIMorphosyntaxProcess,
            CuneiformLuwianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing CuneiformLuwianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("CuneiformLuwianOpenAIPipeline created.")


class HieroglyphicLuwianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Hieroglyphic Luwian."""

    description: Optional[str] = "Pipeline for the Hieroglyphic Luwian language"
    glottolog_id: Optional[str] = "hier1240"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HieroglyphicLuwianSentenceSplittingProcess,
            HieroglyphicLuwianOpenAIMorphosyntaxProcess,
            HieroglyphicLuwianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing HieroglyphicLuwianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("HieroglyphicLuwianOpenAIPipeline created.")


class LycianAOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Lycian."""

    description: Optional[str] = "Pipeline for the Lycian language"
    glottolog_id: Optional[str] = "lyci1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LycianASentenceSplittingProcess,
            LycianAOpenAIMorphosyntaxProcess,
            LycianAOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LycianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("LycianOpenAIPipeline created.")


class LydianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Lydian."""

    description: Optional[str] = "Pipeline for the Lydian language"
    glottolog_id: Optional[str] = "lydi1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LydianSentenceSplittingProcess,
            LydianOpenAIMorphosyntaxProcess,
            LydianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing LydianOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("LydianOpenAIPipeline created.")


class PalaicOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Palaic."""

    description: Optional[str] = "Pipeline for the Palaic language"
    glottolog_id: Optional[str] = "pala1331"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PalaicSentenceSplittingProcess,
            PalaicOpenAIMorphosyntaxProcess,
            PalaicOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing PalaicOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("PalaicOpenAIPipeline created.")


class CarianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Carian."""

    description: Optional[str] = "Pipeline for the Carian language"
    glottolog_id: Optional[str] = "cari1274"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CarianSentenceSplittingProcess,
            CarianOpenAIMorphosyntaxProcess,
            CarianOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing CarianOpenAIPipeline with language: {self.language}"
        )


class SauraseniPrakritOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Sauraseni Prakrit."""

    description: Optional[str] = "Pipeline for the Sauraseni Prakrit language"
    glottolog_id: Optional[str] = "saur1252"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SauraseniPrakritSentenceSplittingProcess,
            SauraseniPrakritOpenAIMorphosyntaxProcess,
            SauraseniPrakritOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing SauraseniPrakritOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("SauraseniPrakritOpenAIPipeline created.")


class MaharastriPrakritOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Maharastri Prakrit."""

    description: Optional[str] = "Pipeline for the Maharastri Prakrit language"
    glottolog_id: Optional[str] = "maha1305"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MaharastriPrakritSentenceSplittingProcess,
            MaharastriPrakritOpenAIMorphosyntaxProcess,
            MaharastriPrakritOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MaharastriPrakritOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("MaharastriPrakritOpenAIPipeline created.")


class MagadhiPrakritOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Magadhi Prakrit."""

    description: Optional[str] = "Pipeline for the Magadhi Prakrit language"
    glottolog_id: Optional[str] = "maga1260"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MagadhiPrakritSentenceSplittingProcess,
            MagadhiPrakritOpenAIMorphosyntaxProcess,
            MagadhiPrakritOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MagadhiPrakritOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("MagadhiPrakritOpenAIPipeline created.")


class GandhariOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Gandhari."""

    description: Optional[str] = "Pipeline for the Gandhari language"
    glottolog_id: Optional[str] = "gand1259"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GandhariSentenceSplittingProcess,
            GandhariOpenAIMorphosyntaxProcess,
            GandhariOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GandhariOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("GandhariOpenAIPipeline created.")


# Hindi and closely related lects
class HindiOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Hindi (glottocode hind1269)."""

    description: Optional[str] = "Pipeline for the Hindi language"
    glottolog_id: Optional[str] = "hind1269"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HindiSentenceSplittingProcess,
            HindiOpenAIMorphosyntaxProcess,
            HindiOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing HindiOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("HindiOpenAIPipeline created.")


class KhariBoliOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Khari Boli (Hindi dialect)."""

    description: Optional[str] = "Pipeline for the Khari Boli dialect of Hindi"
    glottolog_id: Optional[str] = "khad1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            KhariBoliSentenceSplittingProcess,
            KhariBoliOpenAIMorphosyntaxProcess,
            KhariBoliOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing KhariBoliOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("KhariBoliOpenAIPipeline created.")


class BrajOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Braj Bhasha."""

    description: Optional[str] = "Pipeline for the Braj Bhasha language"
    glottolog_id: Optional[str] = "braj1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BrajSentenceSplittingProcess,
            BrajOpenAIMorphosyntaxProcess,
            BrajOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing BrajOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("BrajOpenAIPipeline created.")


class AwadhiOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Awadhi."""

    description: Optional[str] = "Pipeline for the Awadhi language"
    glottolog_id: Optional[str] = "awad1243"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AwadhiSentenceSplittingProcess,
            AwadhiOpenAIMorphosyntaxProcess,
            AwadhiOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing AwadhiOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("AwadhiOpenAIPipeline created.")


class UrduOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Urdu."""

    description: Optional[str] = "Pipeline for the Urdu language"
    glottolog_id: Optional[str] = "urdu1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            UrduSentenceSplittingProcess,
            UrduOpenAIMorphosyntaxProcess,
            UrduOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing UrduOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("UrduOpenAIPipeline created.")


# Eastern Indo-Aryan and Western IA additions
class BengaliOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Bengali."""

    description: Optional[str] = "Pipeline for the Bengali language"
    glottolog_id: Optional[str] = "beng1280"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BengaliSentenceSplittingProcess,
            BengaliOpenAIMorphosyntaxProcess,
            BengaliOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing BengaliOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("BengaliOpenAIPipeline created.")


class OdiaOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Odia (Oriya)."""

    description: Optional[str] = "Pipeline for the Odia language"
    glottolog_id: Optional[str] = "oriy1255"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OdiaSentenceSplittingProcess,
            OdiaOpenAIMorphosyntaxProcess,
            OdiaOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing OdiaOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("OdiaOpenAIPipeline created.")


class AssameseOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Assamese."""

    description: Optional[str] = "Pipeline for the Assamese language"
    glottolog_id: Optional[str] = "assa1263"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AssameseSentenceSplittingProcess,
            AssameseOpenAIMorphosyntaxProcess,
            AssameseOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing AssameseOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("AssameseOpenAIPipeline created.")


class GujaratiOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Gujarati."""

    description: Optional[str] = "Pipeline for the Gujarati language"
    glottolog_id: Optional[str] = "guja1252"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GujaratiSentenceSplittingProcess,
            GujaratiOpenAIMorphosyntaxProcess,
            GujaratiOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing GujaratiOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("GujaratiOpenAIPipeline created.")


class MarathiOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Marathi."""

    description: Optional[str] = "Pipeline for the Marathi language"
    glottolog_id: Optional[str] = "mara1378"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MarathiSentenceSplittingProcess,
            MarathiOpenAIMorphosyntaxProcess,
            MarathiOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing MarathiOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("MarathiOpenAIPipeline created.")


class SinhalaOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Sinhala."""

    description: Optional[str] = "Pipeline for the Sinhala language"
    glottolog_id: Optional[str] = "sinh1246"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SinhalaSentenceSplittingProcess,
            SinhalaOpenAIMorphosyntaxProcess,
            SinhalaOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing SinhalaOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("SinhalaOpenAIPipeline created.")


class EasternPanjabiOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Eastern Panjabi."""

    description: Optional[str] = "Pipeline for the Eastern Panjabi language"
    glottolog_id: Optional[str] = "panj1256"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PanjabiSentenceSplittingProcess,
            EasternPanjabiOpenAIMorphosyntaxProcess,
            EasternPanjabiOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing EasternPanjabiOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("EasternPanjabiOpenAIPipeline created.")


class SindhiOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Sindhi."""

    description: Optional[str] = "Pipeline for the Sindhi language"
    glottolog_id: Optional[str] = "sind1272"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SindhiSentenceSplittingProcess,
            SindhiOpenAIMorphosyntaxProcess,
            SindhiOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing SindhiOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("SindhiOpenAIPipeline created.")


class KashmiriOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Kashmiri."""

    description: Optional[str] = "Pipeline for the Kashmiri language"
    glottolog_id: Optional[str] = "kash1277"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            KashmiriSentenceSplittingProcess,
            KashmiriOpenAIMorphosyntaxProcess,
            KashmiriOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing KashmiriOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("KashmiriOpenAIPipeline created.")


# Sino-Tibetan additions
class OldChineseOpenAIPipeline(Pipeline):
    """Pipeline for Old Chinese."""

    description: Optional[str] = "Pipeline for Old Chinese"
    glottolog_id: Optional[str] = "oldc1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldChineseSentenceSplittingProcess,
            OldChineseOpenAIMorphosyntaxProcess,
            OldChineseOpenAIDependencyProcess,
        ]
    )


class MiddleChineseOpenAIPipeline(Pipeline):
    """Pipeline for Middle Chinese."""

    description: Optional[str] = "Pipeline for Middle Chinese"
    glottolog_id: Optional[str] = "midd1344"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleChineseSentenceSplittingProcess,
            MiddleChineseOpenAIMorphosyntaxProcess,
            MiddleChineseOpenAIDependencyProcess,
        ]
    )


class BaihuaChineseOpenAIPipeline(Pipeline):
    """Pipeline for Early Vernacular Chinese (Baihua)."""

    description: Optional[str] = "Pipeline for Early Vernacular Chinese (Baihua)"
    glottolog_id: Optional[str] = "clas1255"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BaihuaChineseSentenceSplittingProcess,
            BaihuaChineseOpenAIMorphosyntaxProcess,
            BaihuaChineseOpenAIDependencyProcess,
        ]
    )


class OldBurmeseOpenAIPipeline(Pipeline):
    """Pipeline for Old Burmese."""

    description: Optional[str] = "Pipeline for Old Burmese"
    glottolog_id: Optional[str] = "oldb1235"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldBurmeseSentenceSplittingProcess,
            OldBurmeseOpenAIMorphosyntaxProcess,
            OldBurmeseOpenAIDependencyProcess,
        ]
    )


class ClassicalBurmeseOpenAIPipeline(Pipeline):
    """Pipeline for Classical/Nuclear Burmese."""

    description: Optional[str] = "Pipeline for Classical Burmese"
    glottolog_id: Optional[str] = "nucl1310"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalBurmeseSentenceSplittingProcess,
            ClassicalBurmeseOpenAIMorphosyntaxProcess,
            ClassicalBurmeseOpenAIDependencyProcess,
        ]
    )


class TangutOpenAIPipeline(Pipeline):
    """Pipeline for Tangut (Xixia)."""

    description: Optional[str] = "Pipeline for the Tangut language"
    glottolog_id: Optional[str] = "tang1334"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TangutSentenceSplittingProcess,
            TangutOpenAIMorphosyntaxProcess,
            TangutOpenAIDependencyProcess,
        ]
    )


class NewarOpenAIPipeline(Pipeline):
    """Pipeline for Newar (Classical Nepal Bhasa)."""

    description: Optional[str] = "Pipeline for the Newar language"
    glottolog_id: Optional[str] = "newa1246"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            NewarSentenceSplittingProcess,
            NewarOpenAIMorphosyntaxProcess,
            NewarOpenAIDependencyProcess,
        ]
    )


class MeiteiOpenAIPipeline(Pipeline):
    """Pipeline for Meitei (Classical Manipuri)."""

    description: Optional[str] = "Pipeline for the Meitei (Classical Manipuri) language"
    glottolog_id: Optional[str] = "mani1292"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MeiteiSentenceSplittingProcess,
            MeiteiOpenAIMorphosyntaxProcess,
            MeiteiOpenAIDependencyProcess,
        ]
    )


class SgawKarenOpenAIPipeline(Pipeline):
    """Pipeline for Sgaw Karen."""

    description: Optional[str] = "Pipeline for the Sgaw Karen language"
    glottolog_id: Optional[str] = "sgaw1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SgawKarenSentenceSplittingProcess,
            SgawKarenOpenAIMorphosyntaxProcess,
            SgawKarenOpenAIDependencyProcess,
        ]
    )


class MiddleMongolOpenAIPipeline(Pipeline):
    """Pipeline for Middle Mongol."""

    description: Optional[str] = "Pipeline for the Middle Mongol language"
    glottolog_id: Optional[str] = "midd1351"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleMongolSentenceSplittingProcess,
            MiddleMongolOpenAIMorphosyntaxProcess,
            MiddleMongolOpenAIDependencyProcess,
        ]
    )


class ClassicalMongolianOpenAIPipeline(Pipeline):
    """Pipeline for Classical Mongolian."""

    description: Optional[str] = "Pipeline for the Classical Mongolian language"
    glottolog_id: Optional[str] = "mong1331"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalMongolianSentenceSplittingProcess,
            ClassicalMongolianOpenAIMorphosyntaxProcess,
            ClassicalMongolianOpenAIDependencyProcess,
        ]
    )


class MogholiOpenAIPipeline(Pipeline):
    """Pipeline for Mogholi (Moghol)."""

    description: Optional[str] = "Pipeline for the Mogholi (Moghol) language"
    glottolog_id: Optional[str] = "mogh1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MogholiSentenceSplittingProcess,
            MogholiOpenAIMorphosyntaxProcess,
            MogholiOpenAIDependencyProcess,
        ]
    )


class BagriOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Bagri (Rajasthani)."""

    description: Optional[str] = "Pipeline for the Bagri (Rajasthani) language"
    glottolog_id: Optional[str] = "bagr1243"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BagriSentenceSplittingProcess,
            BagriOpenAIMorphosyntaxProcess,
            BagriOpenAIDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        plog(self).debug(
            f"Initializing BagriOpenAIPipeline with language: {self.language}"
        )
        plog(self).info("BagriOpenAIPipeline created.")


# Additional Afroasiatic, Altaic-adjacent, Uralic, Turkic, Dravidian pipelines
class NumidianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Numidian (Ancient Berber)."""

    description: Optional[str] = "Pipeline for the Numidian (Ancient Berber) language"
    glottolog_id: Optional[str] = "numi1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            NumidianSentenceSplittingProcess,
            NumidianOpenAIMorphosyntaxProcess,
            NumidianOpenAIDependencyProcess,
        ]
    )


class TaitaOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Taita (Cushitic)."""

    description: Optional[str] = "Pipeline for the Cushitic Taita language"
    glottolog_id: Optional[str] = "tait1247"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TaitaSentenceSplittingProcess,
            TaitaOpenAIMorphosyntaxProcess,
            TaitaOpenAIDependencyProcess,
        ]
    )


class HausaOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Hausa."""

    description: Optional[str] = "Pipeline for the Hausa language"
    glottolog_id: Optional[str] = "haus1257"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HausaSentenceSplittingProcess,
            HausaOpenAIMorphosyntaxProcess,
            HausaOpenAIDependencyProcess,
        ]
    )


class OldJurchenOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Jurchen."""

    description: Optional[str] = "Pipeline for the Old Jurchen language"
    glottolog_id: Optional[str] = "jurc1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldJurchenSentenceSplittingProcess,
            OldJurchenOpenAIMorphosyntaxProcess,
            OldJurchenOpenAIDependencyProcess,
        ]
    )


class OldJapaneseOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Japanese."""

    description: Optional[str] = "Pipeline for the Old Japanese language"
    glottolog_id: Optional[str] = "japo1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldJapaneseSentenceSplittingProcess,
            OldJapaneseOpenAIMorphosyntaxProcess,
            OldJapaneseOpenAIDependencyProcess,
        ]
    )


class OldHungarianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Hungarian."""

    description: Optional[str] = "Pipeline for the Old Hungarian language"
    glottolog_id: Optional[str] = "oldh1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldHungarianSentenceSplittingProcess,
            OldHungarianOpenAIMorphosyntaxProcess,
            OldHungarianOpenAIDependencyProcess,
        ]
    )


class ChagataiOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Chagatai."""

    description: Optional[str] = "Pipeline for the Chagatai language"
    glottolog_id: Optional[str] = "chag1247"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ChagataiSentenceSplittingProcess,
            ChagataiOpenAIMorphosyntaxProcess,
            ChagataiOpenAIDependencyProcess,
        ]
    )


class OldTurkicOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Turkic."""

    description: Optional[str] = "Pipeline for the Old Turkic language"
    glottolog_id: Optional[str] = "oldu1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldTurkicSentenceSplittingProcess,
            OldTurkicOpenAIMorphosyntaxProcess,
            OldTurkicOpenAIDependencyProcess,
        ]
    )


class OldTamilOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Tamil."""

    description: Optional[str] = "Pipeline for the Old Tamil language"
    glottolog_id: Optional[str] = "oldt1248"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldTamilSentenceSplittingProcess,
            OldTamilOpenAIMorphosyntaxProcess,
            OldTamilOpenAIDependencyProcess,
        ]
    )


# Northwest Semitic and Aramaic additions
class MoabiteOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Moabite."""

    description: Optional[str] = "Pipeline for the Moabite language"
    glottolog_id: Optional[str] = "moab1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MoabiteSentenceSplittingProcess,
            MoabiteOpenAIMorphosyntaxProcess,
            MoabiteOpenAIDependencyProcess,
        ]
    )


class AmmoniteOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Ammonite."""

    description: Optional[str] = "Pipeline for the Ammonite language"
    glottolog_id: Optional[str] = "ammo1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AmmoniteSentenceSplittingProcess,
            AmmoniteOpenAIMorphosyntaxProcess,
            AmmoniteOpenAIDependencyProcess,
        ]
    )


class EdomiteOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Edomite."""

    description: Optional[str] = "Pipeline for the Edomite language"
    glottolog_id: Optional[str] = "edom1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            EdomiteSentenceSplittingProcess,
            EdomiteOpenAIMorphosyntaxProcess,
            EdomiteOpenAIDependencyProcess,
        ]
    )


class OldAramaicOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Aramaic (up to 700 BCE)."""

    description: Optional[str] = "Pipeline for Old Aramaic (up to 700 BCE)"
    glottolog_id: Optional[str] = "olda1246"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldAramaicSentenceSplittingProcess,
            OldAramaicOpenAIMorphosyntaxProcess,
            OldAramaicOpenAIDependencyProcess,
        ]
    )


class OldAramaicSamalianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Old Aramaic–Samʾalian."""

    description: Optional[str] = "Pipeline for Old Aramaic–Samʾalian"
    glottolog_id: Optional[str] = "olda1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldAramaicSamalianSentenceSplittingProcess,
            OldAramaicSamalianOpenAIMorphosyntaxProcess,
            OldAramaicSamalianOpenAIDependencyProcess,
        ]
    )


class MiddleAramaicOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Aramaic."""

    description: Optional[str] = "Pipeline for Middle Aramaic"
    glottolog_id: Optional[str] = "midd1366"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleAramaicSentenceSplittingProcess,
            MiddleAramaicOpenAIMorphosyntaxProcess,
            MiddleAramaicOpenAIDependencyProcess,
        ]
    )


class ClassicalMandaicOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Mandaic."""

    description: Optional[str] = "Pipeline for Classical Mandaic"
    glottolog_id: Optional[str] = "clas1253"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalMandaicSentenceSplittingProcess,
            ClassicalMandaicOpenAIMorphosyntaxProcess,
            ClassicalMandaicOpenAIDependencyProcess,
        ]
    )


class HatranOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Hatran."""

    description: Optional[str] = "Pipeline for Hatran"
    glottolog_id: Optional[str] = "hatr1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HatranSentenceSplittingProcess,
            HatranOpenAIMorphosyntaxProcess,
            HatranOpenAIDependencyProcess,
        ]
    )


class JewishBabylonianAramaicOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Jewish Babylonian Aramaic."""

    description: Optional[str] = "Pipeline for Jewish Babylonian Aramaic"
    glottolog_id: Optional[str] = "jewi1240"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            JewishBabylonianAramaicSentenceSplittingProcess,
            JewishBabylonianAramaicOpenAIMorphosyntaxProcess,
            JewishBabylonianAramaicOpenAIDependencyProcess,
        ]
    )


class SamalianOpenAIPipeline(Pipeline):
    """Default ``Pipeline`` for Samʾalian."""

    description: Optional[str] = "Pipeline for Samʾalian"
    glottolog_id: Optional[str] = "sama1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SamalianSentenceSplittingProcess,
            SamalianOpenAIMorphosyntaxProcess,
            SamalianOpenAIDependencyProcess,
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
    "lati1261": LatinOpenAIPipeline,
    "oldf1239": OldFrenchOpenAIPipeline,
    "midd1316": MiddleFrenchOpenAIPipeline,
    # Other Romance languages
    ## Hellenic
    "anci1242": AncientGreekOpenAIPipeline,
    # Mycenaean Greek (Linear B tablets, ca. 1400–1200 BCE).
    # Medieval/Byzantine Greek
    "oldi1245": EarlyIrishOpenAIPipeline,
    "oldw1239": OldMiddleWelshOpenAIPipeline,
    "bret1244": MiddleBretonOpenAIPipeline,
    "corn1251": CornishOpenAIPipeline,
    ## Germanic
    # Proto-Norse
    "goth1244": GothicOpenAIPipeline,
    "oldh1241": OldHighGermanOpenAIPipeline,
    "midd1343": MiddleHighGermanOpenAIPipeline,
    "oldn1244": OldNorseOpenAIPipeline,
    "olde1238": OldEnglishOpenAIPipeline,
    "midd1317": MiddleEnglishOpenAIPipeline,
    ## Balto-Slavic
    "chur1257": ChurchSlavonicOpenAIPipeline,
    "prus1238": OldPrussianOpenAIPipeline,
    "lith1251": LithuanianOpenAIPipeline,
    "latv1249": LatvianOpenAIPipeline,
    "gheg1238": AlbanianOpenAIPipeline,
    ## Armenian, Earliest texts: 5th c. CE (Bible translation by Mesrop Mashtots, who created the script)
    "clas1256": ClassicalArmenianOpenAIPipeline,
    "midd1364": MiddleArmenianOpenAIPipeline,
    # Note this is only a parent, not true languoid
    ## Anatolian
    "hitt1242": HittiteOpenAIPipeline,
    "cune1239": CuneiformLuwianOpenAIPipeline,
    "hier1240": HieroglyphicLuwianOpenAIPipeline,
    "lyci1241": LycianAOpenAIPipeline,
    "lydi1241": LydianOpenAIPipeline,
    "pala1331": PalaicOpenAIPipeline,
    "cari1274": CarianOpenAIPipeline,
    ## Tocharian
    "tokh1242": TocharianAOpenAIPipeline,
    "tokh1243": TocharianBOpenAIPipeline,
    ## Indo-Iranian
    ## Iranian languages
    ### SW Iranian
    "oldp1254": OldPersianOpenAIPipeline,
    "pahl1241": MiddlePersianOpenAIPipeline,
    ### NW Iranian
    "part1239": ParthianOpenAIPipeline,
    ### E Iranian
    "aves1237": AvestanOpenAIPipeline,
    "bact1239": BactrianOpenAIPipeline,
    "sogd1245": SogdianOpenAIPipeline,
    "khot1251": KhotaneseOpenAIPipeline,
    "tums1237": TumshuqeseOpenAIPipeline,
    # Indo-Aryan (Indic): Sanskrit (Vedic & Classical), Prakrits, Pali, later medieval languages (Hindi, Bengali, etc.)
    ## Old Indo-Aryan
    "vedi1234": VedicSanskritOpenAIPipeline,
    "clas1258": ClassicalSanskritOpenAIPipeline,
    # Prakrits (Middle Indo-Aryan, ca. 500 BCE–500 CE)
    "pali1273": PaliOpenAIPipeline,
    # Ardhamāgadhī, Śaurasenī, Mahārāṣṭrī, etc. — languages of Jain/Buddhist texts and early drama.
    # ? Glotto says alt_name for Pali; Ardhamāgadhī, literary language associated with Magadha (eastern India); Jain canonical texts (the Āgamas) are written primarily in Ardhamāgadhī
    "saur1252": SauraseniPrakritOpenAIPipeline,
    "maha1305": MaharastriPrakritOpenAIPipeline,
    "maga1260": MagadhiPrakritOpenAIPipeline,
    "gand1259": GandhariOpenAIPipeline,  ## Middle Indo-Aryan
    # "Maithili": "mait1250"; Apabhraṃśa; "Apabhramsa" is alt_name; (500–1200 CE); Bridges Prakrits → New Indo-Aryan
    ## New Indo-Aryan
    ## Medieval languages (~1200 CE onward):
    # Early forms of Hindi, Bengali, Gujarati, Marathi, Punjabi, Oriya, Sinhala, etc
    # North-Western / Hindi Belt
    "hind1269": HindiOpenAIPipeline,
    "khad1239": KhariBoliOpenAIPipeline,
    "braj1242": BrajOpenAIPipeline,
    "awad1243": AwadhiOpenAIPipeline,
    "urdu1245": UrduOpenAIPipeline,
    # Eastern Indo-Aryan
    "beng1280": BengaliOpenAIPipeline,
    "oriy1255": OdiaOpenAIPipeline,
    "assa1263": AssameseOpenAIPipeline,
    # Western Indo-Aryan
    "guja1252": GujaratiOpenAIPipeline,
    "mara1378": MarathiOpenAIPipeline,
    # Southern Indo-Aryan / adjacency
    "sinh1246": SinhalaOpenAIPipeline,
    # Northwestern frontier
    "panj1256": EasternPanjabiOpenAIPipeline,
    "sind1272": SindhiOpenAIPipeline,
    "kash1277": KashmiriOpenAIPipeline,
    "bagr1243": BagriOpenAIPipeline,
    # Afroasiatic family
    ## Semitic languages
    ### East Semitic
    "akka1240": AkkadianOpenAIPipeline,
    # Eblaite
    ### West Semitic
    "ugar1238": UgariticOpenAIPipeline,
    "phoe1239": PhoenicianOpenAIPipeline,
    "moab1234": MoabiteOpenAIPipeline,
    "ammo1234": AmmoniteOpenAIPipeline,
    "edom1234": EdomiteOpenAIPipeline,
    "anci1244": BiblicalHebrewOpenAIPipeline,
    # Medieval Hebrew: No Glottolog
    # "moab1234": Moabite
    # "ammo1234": Ammonite
    # "edom1234": Edomite
    # Old Aramaic (ca. 1000–700 BCE, inscriptions).
    # "olda1246": "Old Aramaic (up to 700 BCE)",
    # "Old Aramaic-Sam'alian": "olda1245"
    "impe1235": ImperialAramaicOpenAIPipeline,
    "olda1246": OldAramaicOpenAIPipeline,
    "olda1245": OldAramaicSamalianOpenAIPipeline,
    "midd1366": MiddleAramaicOpenAIPipeline,
    "clas1253": ClassicalMandaicOpenAIPipeline,
    "hatr1234": HatranOpenAIPipeline,
    "jewi1240": JewishBabylonianAramaicOpenAIPipeline,
    "sama1234": SamalianOpenAIPipeline,
    # "midd1366": Middle Aramaic (200 BCE – 700 CE), includes Biblical Aramaic, Palmyrene, Nabataean, Targumic Aramaic.
    # Eastern Middle Aramaic
    ##  Classical Mandaic, Hatran, Jewish Babylonian Aramaic dialects, and Classical Syriac
    "clas1252": ClassicalSyriacOpenAIPipeline,
    ### NW Semitic
    ## South Semitic
    # Old South Arabian (OSA)
    "geez1241": GeezOpenAIPipeline,
    ### Central Semitic (bridge between NW and South)
    # Pre-Islamic Arabic
    "clas1259": ClassicalArabicOpenAIPipeline,  # Dialect
    # Glotto doesn't have medieval arabic; Medieval Arabic: scientific, philosophical, historical works dominate much of the Islamic Golden Age corpus.
    ## Egyptian languages
    "olde1242": OldEgyptianOpenAIPipeline,
    "midd1369": MiddleEgyptianOpenAIPipeline,
    "late1256": LateEgyptianOpenAIPipeline,
    "demo1234": DemoticOpenAIPipeline,
    "copt1239": CopticOpenAIPipeline,
    ## Berber
    "numi1241": NumidianOpenAIPipeline,
    "tait1247": TaitaOpenAIPipeline,
    ## Chadic
    # ; "haus1257": "Hausa"; Hausa; Essentially oral until medieval period, when Hausa is written in Ajami (Arabic script).
    "haus1257": HausaOpenAIPipeline,
    "lite1248": LiteraryChineseOpenAIPipeline,
    "clas1254": ClassicalTibetanPipeline,
    # Sino-Tibetan family
    # | **Early Vernacular Chinese (Baihua)**   | ca. 10th – 18th c. CE | *(under `clas1255`)* |
    # | **Old Tibetan**                         | 7th – 10th c. CE     | *(not separately coded)* |
    "oldc1244": OldChineseOpenAIPipeline,
    "midd1344": MiddleChineseOpenAIPipeline,
    "clas1255": BaihuaChineseOpenAIPipeline,
    "oldb1235": OldBurmeseOpenAIPipeline,
    "nucl1310": ClassicalBurmeseOpenAIPipeline,
    "tang1334": TangutOpenAIPipeline,
    "newa1246": NewarOpenAIPipeline,
    "mani1292": MeiteiOpenAIPipeline,
    "sgaw1245": SgawKarenOpenAIPipeline,
    # Mongolic family
    "mong1329": MiddleMongolOpenAIPipeline,
    "mong1331": ClassicalMongolianOpenAIPipeline,  #  TODO: No glottolog broken
    "mogh1245": MogholiOpenAIPipeline,
    # Altaic-Adj.
    "jurc1239": OldJurchenOpenAIPipeline,
    # Japonic
    "japo1237": OldJapaneseOpenAIPipeline,
    # Uralic
    "oldh1242": OldHungarianOpenAIPipeline,
    # Turkic
    "chag1247": ChagataiOpenAIPipeline,
    "oldu1238": OldTurkicOpenAIPipeline,
    # TODO: Make pipeline for Ottoman Turkish
    # "otto1234": OttomanTurkishOpenAIPipeline,
    # Dravidian
    "oldt1248": OldTamilOpenAIPipeline,
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
