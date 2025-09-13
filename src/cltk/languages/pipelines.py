"""Language pipelines and mappings.

This module defines many language‑specific pipeline classes (mostly
ChatGPT‑backed) and central mappings from Glottolog codes to default pipelines.
Pipelines are lightweight containers that list a small sequence of processes
such as normalization, sentence splitting, and generative annotation.
"""

from typing import Any, Optional

from pydantic import Field

from cltk.core.cltk_logger import logger
from cltk.core.data_types import Pipeline
from cltk.dependency.processes import (
    AkkadianChatGPTDependencyProcess,
    AlbanianChatGPTDependencyProcess,
    AmmoniteChatGPTDependencyProcess,
    AncientGreekChatGPTDependencyProcess,
    AssameseChatGPTDependencyProcess,
    AvestanChatGPTDependencyProcess,
    AwadhiChatGPTDependencyProcess,
    BactrianChatGPTDependencyProcess,
    BagriChatGPTDependencyProcess,
    BaihuaChineseChatGPTDependencyProcess,
    BengaliChatGPTDependencyProcess,
    BiblicalHebrewChatGPTDependencyProcess,
    BrajChatGPTDependencyProcess,
    CarianChatGPTDependencyProcess,
    ChagataiChatGPTDependencyProcess,
    ChurchSlavicChatGPTDependencyProcess,
    ClassicalArabicChatGPTDependencyProcess,
    ClassicalArmenianChatGPTDependencyProcess,
    ClassicalBurmeseChatGPTDependencyProcess,
    ClassicalMandaicChatGPTDependencyProcess,
    ClassicalMongolianChatGPTDependencyProcess,
    ClassicalSanskritChatGPTDependencyProcess,
    ClassicalSyriacChatGPTDependencyProcess,
    ClassicalTibetanChatGPTDependencyProcess,
    CopticChatGPTDependencyProcess,
    CuneiformLuwianChatGPTDependencyProcess,
    DemoticChatGPTDependencyProcess,
    EarlyIrishChatGPTDependencyProcess,
    EasternPanjabiChatGPTDependencyProcess,
    EdomiteChatGPTDependencyProcess,
    GandhariChatGPTDependencyProcess,
    GeezChatGPTDependencyProcess,
    GothicChatGPTDependencyProcess,
    GujaratiChatGPTDependencyProcess,
    HatranChatGPTDependencyProcess,
    HausaChatGPTDependencyProcess,
    HieroglyphicLuwianChatGPTDependencyProcess,
    HindiChatGPTDependencyProcess,
    HittiteChatGPTDependencyProcess,
    JewishBabylonianAramaicChatGPTDependencyProcess,
    KashmiriChatGPTDependencyProcess,
    KhariBoliChatGPTDependencyProcess,
    KhotaneseChatGPTDependencyProcess,
    LateEgyptianChatGPTDependencyProcess,
    LatinChatGPTDependencyProcess,
    LatvianChatGPTDependencyProcess,
    LiteraryChineseChatGPTDependencyProcess,
    LithuanianChatGPTDependencyProcess,
    LycianAChatGPTDependencyProcess,
    LydianChatGPTDependencyProcess,
    MagadhiPrakritChatGPTDependencyProcess,
    MaharastriPrakritChatGPTDependencyProcess,
    MarathiChatGPTDependencyProcess,
    MeiteiChatGPTDependencyProcess,
    MiddleAramaicChatGPTDependencyProcess,
    MiddleArmenianChatGPTDependencyProcess,
    MiddleBretonChatGPTDependencyProcess,
    MiddleChineseChatGPTDependencyProcess,
    MiddleCornishChatGPTDependencyProcess,
    MiddleEgyptianChatGPTDependencyProcess,
    MiddleEnglishChatGPTDependencyProcess,
    MiddleFrenchChatGPTDependencyProcess,
    MiddleHighGermanChatGPTDependencyProcess,
    MiddleMongolChatGPTDependencyProcess,
    MiddlePersianChatGPTDependencyProcess,
    MoabiteChatGPTDependencyProcess,
    MogholiChatGPTDependencyProcess,
    NewarChatGPTDependencyProcess,
    NumidianChatGPTDependencyProcess,
    OdiaChatGPTDependencyProcess,
    OfficialAramaicChatGPTDependencyProcess,
    OldAramaicChatGPTDependencyProcess,
    OldAramaicSamalianChatGPTDependencyProcess,
    OldBurmeseChatGPTDependencyProcess,
    OldChineseChatGPTDependencyProcess,
    OldEgyptianChatGPTDependencyProcess,
    OldEnglishChatGPTDependencyProcess,
    OldFrenchChatGPTDependencyProcess,
    OldHighGermanChatGPTDependencyProcess,
    OldHungarianChatGPTDependencyProcess,
    OldJapaneseChatGPTDependencyProcess,
    OldJurchenChatGPTDependencyProcess,
    OldMiddleWelshChatGPTDependencyProcess,
    OldNorseChatGPTDependencyProcess,
    OldPersianChatGPTDependencyProcess,
    OldPrussianChatGPTDependencyProcess,
    OldTamilChatGPTDependencyProcess,
    OldTurkicChatGPTDependencyProcess,
    PalaicChatGPTDependencyProcess,
    PaliChatGPTDependencyProcess,
    ParthianChatGPTDependencyProcess,
    PhoenicianChatGPTDependencyProcess,
    SamalianChatGPTDependencyProcess,
    SauraseniPrakritChatGPTDependencyProcess,
    SgawKarenChatGPTDependencyProcess,
    SindhiChatGPTDependencyProcess,
    SinhalaChatGPTDependencyProcess,
    SogdianChatGPTDependencyProcess,
    TaitaChatGPTDependencyProcess,
    TangutChatGPTDependencyProcess,
    TokharianAChatGPTDependencyProcess,
    TokharianBChatGPTDependencyProcess,
    TumshuqeseChatGPTDependencyProcess,
    UgariticChatGPTDependencyProcess,
    UrduChatGPTDependencyProcess,
    VedicSanskritChatGPTDependencyProcess,
)
from cltk.morphosyntax.processes import (
    AkkadianChatGPTMorphosyntaxProcess,
    AlbanianChatGPTMorphosyntaxProcess,
    AmmoniteChatGPTMorphosyntaxProcess,
    AncientGreekChatGPTMorphosyntaxProcess,
    AssameseChatGPTMorphosyntaxProcess,
    AvestanChatGPTMorphosyntaxProcess,
    AwadhiChatGPTMorphosyntaxProcess,
    BactrianChatGPTMorphosyntaxProcess,
    BagriChatGPTMorphosyntaxProcess,
    BaihuaChineseChatGPTMorphosyntaxProcess,
    BengaliChatGPTMorphosyntaxProcess,
    BiblicalHebrewChatGPTMorphosyntaxProcess,
    BrajChatGPTMorphosyntaxProcess,
    CarianChatGPTMorphosyntaxProcess,
    ChagataiChatGPTMorphosyntaxProcess,
    ChurchSlavicChatGPTMorphosyntaxProcess,
    ClassicalArabicChatGPTMorphosyntaxProcess,
    ClassicalArmenianChatGPTMorphosyntaxProcess,
    ClassicalBurmeseChatGPTMorphosyntaxProcess,
    ClassicalMandaicChatGPTMorphosyntaxProcess,
    ClassicalMongolianChatGPTMorphosyntaxProcess,
    ClassicalSanskritChatGPTMorphosyntaxProcess,
    ClassicalSyriacChatGPTMorphosyntaxProcess,
    ClassicalTibetanChatGPTMorphosyntaxProcess,
    CopticChatGPTMorphosyntaxProcess,
    CuneiformLuwianChatGPTMorphosyntaxProcess,
    DemoticChatGPTMorphosyntaxProcess,
    EarlyIrishChatGPTMorphosyntaxProcess,
    EasternPanjabiChatGPTMorphosyntaxProcess,
    EdomiteChatGPTMorphosyntaxProcess,
    GandhariChatGPTMorphosyntaxProcess,
    GeezChatGPTMorphosyntaxProcess,
    GothicChatGPTMorphosyntaxProcess,
    GujaratiChatGPTMorphosyntaxProcess,
    HatranChatGPTMorphosyntaxProcess,
    HausaChatGPTMorphosyntaxProcess,
    HieroglyphicLuwianChatGPTMorphosyntaxProcess,
    HindiChatGPTMorphosyntaxProcess,
    HittiteChatGPTMorphosyntaxProcess,
    JewishBabylonianAramaicChatGPTMorphosyntaxProcess,
    KashmiriChatGPTMorphosyntaxProcess,
    KhariBoliChatGPTMorphosyntaxProcess,
    KhotaneseChatGPTMorphosyntaxProcess,
    LateEgyptianChatGPTMorphosyntaxProcess,
    LatinChatGPTMorphosyntaxProcess,
    LatvianChatGPTMorphosyntaxProcess,
    LiteraryChineseChatGPTMorphosyntaxProcess,
    LithuanianChatGPTMorphosyntaxProcess,
    LycianAChatGPTMorphosyntaxProcess,
    LydianChatGPTMorphosyntaxProcess,
    MagadhiPrakritChatGPTMorphosyntaxProcess,
    MaharastriPrakritChatGPTMorphosyntaxProcess,
    MarathiChatGPTMorphosyntaxProcess,
    MeiteiChatGPTMorphosyntaxProcess,
    MiddleAramaicChatGPTMorphosyntaxProcess,
    MiddleArmenianChatGPTMorphosyntaxProcess,
    MiddleBretonChatGPTMorphosyntaxProcess,
    MiddleChineseChatGPTMorphosyntaxProcess,
    MiddleCornishChatGPTMorphosyntaxProcess,
    MiddleEgyptianChatGPTMorphosyntaxProcess,
    MiddleEnglishChatGPTMorphosyntaxProcess,
    MiddleFrenchChatGPTMorphosyntaxProcess,
    MiddleHighGermanChatGPTMorphosyntaxProcess,
    MiddleMongolChatGPTMorphosyntaxProcess,
    MiddlePersianChatGPTMorphosyntaxProcess,
    MoabiteChatGPTMorphosyntaxProcess,
    MogholiChatGPTMorphosyntaxProcess,
    NewarChatGPTMorphosyntaxProcess,
    NumidianChatGPTMorphosyntaxProcess,
    OdiaChatGPTMorphosyntaxProcess,
    OfficialAramaicChatGPTMorphosyntaxProcess,
    OldAramaicChatGPTMorphosyntaxProcess,
    OldAramaicSamalianChatGPTMorphosyntaxProcess,
    OldBurmeseChatGPTMorphosyntaxProcess,
    OldChineseChatGPTMorphosyntaxProcess,
    OldEgyptianChatGPTMorphosyntaxProcess,
    OldEnglishChatGPTMorphosyntaxProcess,
    OldFrenchChatGPTMorphosyntaxProcess,
    OldHighGermanChatGPTMorphosyntaxProcess,
    OldHungarianChatGPTMorphosyntaxProcess,
    OldJapaneseChatGPTMorphosyntaxProcess,
    OldJurchenChatGPTMorphosyntaxProcess,
    OldMiddleWelshChatGPTMorphosyntaxProcess,
    OldNorseChatGPTMorphosyntaxProcess,
    OldPersianChatGPTMorphosyntaxProcess,
    OldPrussianChatGPTMorphosyntaxProcess,
    OldTamilChatGPTMorphosyntaxProcess,
    OldTurkicChatGPTMorphosyntaxProcess,
    PalaicChatGPTMorphosyntaxProcess,
    PaliChatGPTMorphosyntaxProcess,
    ParthianChatGPTMorphosyntaxProcess,
    PhoenicianChatGPTMorphosyntaxProcess,
    SamalianChatGPTMorphosyntaxProcess,
    SauraseniPrakritChatGPTMorphosyntaxProcess,
    SgawKarenChatGPTMorphosyntaxProcess,
    SindhiChatGPTMorphosyntaxProcess,
    SinhalaChatGPTMorphosyntaxProcess,
    SogdianChatGPTMorphosyntaxProcess,
    TaitaChatGPTMorphosyntaxProcess,
    TangutChatGPTMorphosyntaxProcess,
    TokharianAChatGPTMorphosyntaxProcess,
    TokharianBChatGPTMorphosyntaxProcess,
    TumshuqeseChatGPTMorphosyntaxProcess,
    UgariticChatGPTMorphosyntaxProcess,
    UrduChatGPTMorphosyntaxProcess,
    VedicSanskritChatGPTMorphosyntaxProcess,
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


class AkkadianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Akkadian."""

    description: Optional[str] = "Pipeline for the Akkadian language"
    glottolog_id: Optional[str] = "akka1240"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AkkadianSentenceSplittingProcess,
            AkkadianChatGPTMorphosyntaxProcess,
            AkkadianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        logger.debug(
            f"Initializing AkkadianChatGPTPipeline with language: {self.language.name}"
        )
        logger.info("AkkadianChatGPTPipeline created.")


class ClassicalArabicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Arabic."""

    description: Optional[str] = "Pipeline for the Arabic language"
    glottolog_id: Optional[str] = "clas1259"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalArabicSentenceSplittingProcess,
            ClassicalArabicChatGPTMorphosyntaxProcess,
            ClassicalArabicChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing ArabicChatGPTPipeline with language: {self.language}"
        )
        logger.info("ArabicChatGPTPipeline created.")


#
class ClassicalSyriacChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Syriac."""

    description: Optional[str] = "Pipeline for the Classical Syriac language"
    glottolog_id: Optional[str] = "clas1252"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalSyriacSentenceSplittingProcess,
            ClassicalSyriacChatGPTMorphosyntaxProcess,
            ClassicalSyriacChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        logger.debug(
            f"Initializing ClassicalSyriacChatGPTPipeline with language: {self.language.name}"
        )
        logger.info("ClassicalSyriacChatGPTPipeline created.")


# ClassicalTibetanPipeline
class ClassicalTibetanPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Tibetan."""

    description: Optional[str] = "Pipeline for the Classical Tibetan language"
    glottolog_id: Optional[str] = "clas1254"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalTibetanSentenceSplittingProcess,
            ClassicalTibetanChatGPTMorphosyntaxProcess,
            ClassicalTibetanChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        logger.debug(
            f"Initializing ClassicalTibetanChatGPTPipeline with language: {self.language.name}"
        )
        logger.info("ClassicalTibetanChatGPTPipeline created.")


class CopticChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Coptic."""

    description: Optional[str] = "ChatGPT Pipeline for the Coptic language."
    glottolog_id: Optional[str] = "copt1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CopticSentenceSplittingProcess,
            CopticChatGPTMorphosyntaxProcess,
            CopticChatGPTDependencyProcess,
        ]
    )


class GothicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic."""

    description: Optional[str] = "Pipeline for the Gothic language"
    glottolog_id: Optional[str] = "goth1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GothicSentenceSplittingProcess,
            GothicChatGPTMorphosyntaxProcess,
            GothicChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing GothicChatGPTPipeline with language: {self.language}"
        )
        logger.info("GothicChatGPTPipeline created.")


class AncientGreekChatGPTPipeline(Pipeline):
    """Pipeline for Ancient Greek using normalization and ChatGPT annotation only."""

    description: Optional[str] = "Pipeline for Ancient Greek with ChatGPT annotation"
    glottolog_id: Optional[str] = "anci1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            # AncientGreekNormalizeProcess,
            MultilingualNormalizeProcess,
            AncientGreekSentenceSplittingProcess,
            AncientGreekChatGPTMorphosyntaxProcess,
            AncientGreekChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing GreekChatGPTPipeline with language: {self.language}"
        )
        logger.info("GreekChatGPTPipeline created.")


class BiblicalHebrewChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Hebrew."""

    description: Optional[str] = "Pipeline for the Ancient Hebrew language."
    glottolog_id: Optional[str] = "anci1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AncientHebrewSentenceSplittingProcess,
            BiblicalHebrewChatGPTMorphosyntaxProcess,
            BiblicalHebrewChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(f"Initializing LatinPipeline with language: {self.language}")
        logger.info("LatinPipeline created.")


class LatinChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Latin."""

    description: Optional[str] = "ChatGPT Pipeline for the Latin language."
    glottolog_id: Optional[str] = "lati1261"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            # LatinNormalizeProcess,
            MultilingualNormalizeProcess,
            LatinSentenceSplittingProcess,
            LatinChatGPTMorphosyntaxProcess,
            LatinChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(f"Initializing LatinPipeline with language: {self.language}")
        logger.info("LatinPipeline created.")


class MiddleEnglishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle English."""

    description: Optional[str] = "Pipeline for the Middle English language"
    glottolog_id: Optional[str] = "midd1317"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleEnglishSentenceSplittingProcess,
            MiddleEnglishChatGPTMorphosyntaxProcess,
            MiddleEnglishChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MiddleEnglishChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleEnglishChatGPTPipeline created.")


class MiddleFrenchChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle French."""

    description: Optional[str] = "Pipeline for the Middle French language"
    glottolog_id: Optional[str] = "midd1316"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleFrenchSentenceSplittingProcess,
            MiddleFrenchChatGPTMorphosyntaxProcess,
            MiddleFrenchChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MiddleFrenchChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleFrenchChatGPTPipeline created.")


class MiddlePersianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Persian (Pahlavi)."""

    description: Optional[str] = "Pipeline for the Middle Persian (Pahlavi) language"
    glottolog_id: Optional[str] = "pahl1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddlePersianSentenceSplittingProcess,
            MiddlePersianChatGPTMorphosyntaxProcess,
            MiddlePersianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MiddlePersianChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddlePersianChatGPTPipeline created.")


class ImperialAramaicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Official Aramaic."""

    description: Optional[str] = "ChatGPT Pipeline for the Official Aramaic language."
    glottolog_id: Optional[str] = "impe1235"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OfficialAramaicSentenceSplittingProcess,
            OfficialAramaicChatGPTMorphosyntaxProcess,
            OfficialAramaicChatGPTDependencyProcess,
        ]
    )


class ChurchSlavonicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for (Old) Church Slavonic."""

    description: Optional[str] = "Pipeline for the Church Slavonic language"
    glottolog_id: Optional[str] = "chur1257"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ChurchSlavonicSentenceSplittingProcess,
            ChurchSlavicChatGPTMorphosyntaxProcess,
            ChurchSlavicChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing ChurchSlavonicChatGPTPipeline with language: {self.language}"
        )
        logger.info("ChurchSlavonicChatGPTPipeline")


class OldEnglishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old English."""

    description: Optional[str] = "Pipeline for the Old English language"
    glottolog_id: Optional[str] = "olde1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldEnglishSentenceSplittingProcess,
            OldEnglishChatGPTMorphosyntaxProcess,
            OldEnglishChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        assert self.language, "Language not found"
        logger.debug(
            f"Initializing OldEnglishChatGPTPipeline with language: {self.language.name}"
        )
        logger.info("OldEnglishChatGPTPipeline created.")


class OldFrenchChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old French."""

    description: Optional[str] = "Pipeline for the Old French language"
    glottolog_id: Optional[str] = "oldf1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldFrenchSentenceSplittingProcess,
            OldFrenchChatGPTMorphosyntaxProcess,
            OldFrenchChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing OldFrenchChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldFrenchChatGPTPipeline created.")


class OldNorseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Norse."""

    description: Optional[str] = "Pipeline for the Old Norse language"
    glottolog_id: Optional[str] = "oldn1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldNorseSentenceSplittingProcess,
            OldNorseChatGPTMorphosyntaxProcess,
            OldNorseChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing OldNorseChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldNorseChatGPTPipeline created.")


class PaliChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Pali."""

    description: Optional[str] = "Pipeline for the Pali language"
    glottolog_id: Optional[str] = "pali1273"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PaliSentenceSplittingProcess,
            PaliChatGPTMorphosyntaxProcess,
            PaliChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(f"Initializing PaliPipeline with language: {self.language}")
        logger.info("PaliPipeline created.")


class ClassicalSanskritChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Sanskrit."""

    description: Optional[str] = "Pipeline for the Classical Sanskrit language"
    glottolog_id: Optional[str] = "vedi1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalSanskritSentenceSplittingProcess,
            ClassicalSanskritChatGPTMorphosyntaxProcess,
            ClassicalSanskritChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing ClassicalSanskritChatGPTPipeline with language: {self.language}"
        )
        logger.info("ClassicalSanskritChatGPTPipeline created.")


class VedicSanskritChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Vedic Sanskrit."""

    description: Optional[str] = "Pipeline for the Vedic Sanskrit language"
    glottolog_id: Optional[str] = "clas1258"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            VedicSanskritSentenceSplittingProcess,
            VedicSanskritChatGPTMorphosyntaxProcess,
            VedicSanskritChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing VedicSanskritChatGPTPipeline with language: {self.language}"
        )
        logger.info("VedicSanskritChatGPTPipeline created.")


class OldHighGermanChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old High German."""

    description: Optional[str] = "Pipeline for the Old High German language"
    glottolog_id: Optional[str] = "oldh1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            # MiddleHighGermanTokenizationProcess,  # Substitute with OldHighGermanTokenizationProcess if available
            OldHighGermanSentenceSplittingProcess,
            OldHighGermanChatGPTMorphosyntaxProcess,
            OldHighGermanChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing OldHighGermanChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldHighGermanChatGPTPipeline created.")


class MiddleHighGermanChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle High German."""

    description: Optional[str] = "Pipeline for the Middle High German language"
    glottolog_id: Optional[str] = "midd1343"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleHighGermanSentenceSplittingProcess,
            MiddleHighGermanChatGPTMorphosyntaxProcess,
            MiddleHighGermanChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MiddleHighGermanChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleHighGermanChatGPTPipeline created.")


class LiteraryChineseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Literary (or Classical) Chinese."""

    description: Optional[str] = (
        "Pipeline for the Literary (or Classical) Chinese language"
    )
    glottolog_id: Optional[str] = "lite1248"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LiteraryChineseSentenceSplittingProcess,
            LiteraryChineseChatGPTMorphosyntaxProcess,
            LiteraryChineseChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing LiteraryChineseChatGPTPipeline with language: {self.language}"
        )
        logger.info("LiteraryChineseChatGPTPipeline created.")


class DemoticChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Demotic Egyptian."""

    description: Optional[str] = "Pipeline for the Demotic Egyptian language"
    glottolog_id: Optional[str] = "demo1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            DemoticSentenceSplittingProcess,
            DemoticChatGPTMorphosyntaxProcess,
            DemoticChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing DemoticChatGPTPipeline with language: {self.language}"
        )
        logger.info("DemoticChatGPTPipeline created.")


class HittiteChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Hittite."""

    description: Optional[str] = "Pipeline for the Hittite language"
    glottolog_id: Optional[str] = "hitt1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HittiteSentenceSplittingProcess,
            HittiteChatGPTMorphosyntaxProcess,
            HittiteChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing HittiteChatGPTPipeline with language: {self.language}"
        )
        logger.info("HittiteChatGPTPipeline created.")


class TocharianAChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Tocharian A."""

    description: Optional[str] = "Pipeline for the Tocharian A language"
    glottolog_id: Optional[str] = "toch1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TocharianASentenceSplittingProcess,
            TokharianAChatGPTMorphosyntaxProcess,
            TokharianAChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing TocharianAChatGPTPipeline with language: {self.language}"
        )
        logger.info("TocharianAChatGPTPipeline created.")


class TocharianBChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Tocharian B."""

    description: Optional[str] = "Pipeline for the Tocharian B language"
    glottolog_id: Optional[str] = "toch1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TocharianBSentenceSplittingProcess,
            TokharianBChatGPTMorphosyntaxProcess,
            TokharianBChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing TocharianBChatGPTPipeline with language: {self.language}"
        )
        logger.info("TocharianBChatGPTPipeline created.")


class AvestanChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Avestan."""

    description: Optional[str] = "Pipeline for the Avestan language"
    glottolog_id: Optional[str] = "aves1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AvestanSentenceSplittingProcess,
            AvestanChatGPTMorphosyntaxProcess,
            AvestanChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing AvestanChatGPTPipeline with language: {self.language}"
        )
        logger.info("AvestanChatGPTPipeline created.")


class BactrianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Bactrian."""

    description: Optional[str] = "Pipeline for the Bactrian language"
    glottolog_id: Optional[str] = "bact1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BactrianSentenceSplittingProcess,
            BactrianChatGPTMorphosyntaxProcess,
            BactrianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing BactrianChatGPTPipeline with language: {self.language}"
        )
        logger.info("BactrianChatGPTPipeline created.")


class SogdianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Sogdian."""

    description: Optional[str] = "Pipeline for the Sogdian language"
    glottolog_id: Optional[str] = "sogd1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SogdianSentenceSplittingProcess,
            SogdianChatGPTMorphosyntaxProcess,
            SogdianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing SogdianChatGPTPipeline with language: {self.language}"
        )
        logger.info("SogdianChatGPTPipeline created.")


class KhotaneseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Khotanese."""

    description: Optional[str] = "Pipeline for the Khotanese language"
    glottolog_id: Optional[str] = "khot1251"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            KhotaneseSentenceSplittingProcess,
            KhotaneseChatGPTMorphosyntaxProcess,
            KhotaneseChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing KhotaneseChatGPTPipeline with language: {self.language}"
        )
        logger.info("KhotaneseChatGPTPipeline created.")


class TumshuqeseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Tumshuqese."""

    description: Optional[str] = "Pipeline for the Tumshuqese language"
    glottolog_id: Optional[str] = "tums1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TumshuqeseSentenceSplittingProcess,
            TumshuqeseChatGPTMorphosyntaxProcess,
            TumshuqeseChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing TumshuqeseChatGPTPipeline with language: {self.language}"
        )
        logger.info("TumshuqeseChatGPTPipeline created.")


class OldPersianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Persian."""

    description: Optional[str] = "Pipeline for the Old Persian language"
    glottolog_id: Optional[str] = "oldp1254"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldPersianSentenceSplittingProcess,
            OldPersianChatGPTMorphosyntaxProcess,
            OldPersianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing OldPersianChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldPersianChatGPTPipeline created.")


class EarlyIrishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Irish."""

    description: Optional[str] = "Pipeline for the Old Irish language"
    glottolog_id: Optional[str] = "oldi1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            EarlyIrishSentenceSplittingProcess,
            EarlyIrishChatGPTMorphosyntaxProcess,
            EarlyIrishChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing OldIrishChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldIrishChatGPTPipeline created.")


class UgariticChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Ugaritic."""

    description: Optional[str] = "Pipeline for the Ugaritic language"
    glottolog_id: Optional[str] = "ugar1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            UgariticSentenceSplittingProcess,
            UgariticChatGPTMorphosyntaxProcess,
            UgariticChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing UgariticChatGPTPipeline with language: {self.language}"
        )
        logger.info("UgariticChatGPTPipeline created.")


class PhoenicianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Phoenician (Punic)."""

    description: Optional[str] = "Pipeline for the Phoenician (Punic) language"
    glottolog_id: Optional[str] = "phoe1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PhoenicianSentenceSplittingProcess,
            PhoenicianChatGPTMorphosyntaxProcess,
            PhoenicianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing PhoenicianChatGPTPipeline with language: {self.language}"
        )
        logger.info("PhoenicianChatGPTPipeline created.")


class GeezChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Geʿez (Classical Ethiopic)."""

    description: Optional[str] = "Pipeline for the Geʿez (Classical Ethiopic) language"
    glottolog_id: Optional[str] = "geez1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GeezSentenceSplittingProcess,
            GeezChatGPTMorphosyntaxProcess,
            GeezChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(f"Initializing GeezChatGPTPipeline with language: {self.language}")
        logger.info("GeezChatGPTPipeline created.")


class MiddleEgyptianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Egyptian."""

    description: Optional[str] = "Pipeline for the Middle Egyptian language"
    glottolog_id: Optional[str] = "midd1369"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleEgyptianSentenceSplittingProcess,
            MiddleEgyptianChatGPTMorphosyntaxProcess,
            MiddleEgyptianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MiddleEgyptianChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleEgyptianChatGPTPipeline created.")


class OldEgyptianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Egyptian."""

    description: Optional[str] = "Pipeline for the Old Egyptian language"
    glottolog_id: Optional[str] = "olde1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldEgyptianSentenceSplittingProcess,
            OldEgyptianChatGPTMorphosyntaxProcess,
            OldEgyptianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing OldEgyptianChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldEgyptianChatGPTPipeline created.")


class LateEgyptianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Late Egyptian."""

    description: Optional[str] = "Pipeline for the Late Egyptian language"
    glottolog_id: Optional[str] = "late1256"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LateEgyptianSentenceSplittingProcess,
            LateEgyptianChatGPTMorphosyntaxProcess,
            LateEgyptianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing LateEgyptianChatGPTPipeline with language: {self.language}"
        )
        logger.info("LateEgyptianChatGPTPipeline created.")


class ParthianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Parthian."""

    description: Optional[str] = "Pipeline for the Parthian language"
    glottolog_id: Optional[str] = "part1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ParthianSentenceSplittingProcess,
            ParthianChatGPTMorphosyntaxProcess,
            ParthianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing LateEgyptianChatGPTPipeline with language: {self.language}"
        )
        logger.info("LateEgyptianChatGPTPipeline created.")


class OldMiddleWelshChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Welsh."""

    description: Optional[str] = "Pipeline for the Middle Welsh language"
    glottolog_id: Optional[str] = "oldw1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldMiddleWelshSentenceSplittingProcess,
            OldMiddleWelshChatGPTMorphosyntaxProcess,
            OldMiddleWelshChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MiddleWelshChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleWelshChatGPTPipeline created.")


class MiddleBretonChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Breton."""

    description: Optional[str] = "Pipeline for the Middle Breton language"
    glottolog_id: Optional[str] = "oldb1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleBretonSentenceSplittingProcess,
            MiddleBretonChatGPTMorphosyntaxProcess,
            MiddleBretonChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MiddleBretonChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleBretonChatGPTPipeline created.")


class CornishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Cornish."""

    description: Optional[str] = "Pipeline for the Cornish language"
    glottolog_id: Optional[str] = "corn1251"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleCornishSentenceSplittingProcess,
            MiddleCornishChatGPTMorphosyntaxProcess,
            MiddleCornishChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing CornishChatGPTPipeline with language: {self.language}"
        )
        logger.info("CornishChatGPTPipeline created.")


class OldPrussianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Prussian."""

    description: Optional[str] = "Pipeline for the Old Prussian language"
    glottolog_id: Optional[str] = "prus1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldPrussianSentenceSplittingProcess,
            OldPrussianChatGPTMorphosyntaxProcess,
            OldPrussianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing OldPrussianChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldPrussianChatGPTPipeline created.")


class LithuanianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Lithuanian."""

    description: Optional[str] = "Pipeline for the Lithuanian language"
    glottolog_id: Optional[str] = "lith1251"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LithuanianSentenceSplittingProcess,
            LithuanianChatGPTMorphosyntaxProcess,
            LithuanianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing LithuanianChatGPTPipeline with language: {self.language}"
        )
        logger.info("LithuanianChatGPTPipeline created.")


class LatvianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Latvian."""

    description: Optional[str] = "Pipeline for the Latvian language"
    glottolog_id: Optional[str] = "latv1249"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LatvianSentenceSplittingProcess,
            LatvianChatGPTMorphosyntaxProcess,
            LatvianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing LatvianChatGPTPipeline with language: {self.language}"
        )
        logger.info("LatvianChatGPTPipeline created.")


class AlbanianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Albanian."""

    description: Optional[str] = "Pipeline for the Albanian language"
    glottolog_id: Optional[str] = "gheg1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AlbanianSentenceSplittingProcess,
            AlbanianChatGPTMorphosyntaxProcess,
            AlbanianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing AlbanianChatGPTPipeline with language: {self.language}"
        )
        logger.info("AlbanianChatGPTPipeline created.")


class ClassicalArmenianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Armenian."""

    description: Optional[str] = "Pipeline for the Classical Armenian language"
    glottolog_id: Optional[str] = "clas1256"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalArmenianSentenceSplittingProcess,
            ClassicalArmenianChatGPTMorphosyntaxProcess,
            ClassicalArmenianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing ClassicalArmenianChatGPTPipeline with language: {self.language}"
        )
        logger.info("ClassicalArmenianChatGPTPipeline created.")


class MiddleArmenianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Armenian."""

    description: Optional[str] = "Pipeline for the Middle Armenian language"
    glottolog_id: Optional[str] = "midd1364"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleArmenianSentenceSplittingProcess,
            MiddleArmenianChatGPTMorphosyntaxProcess,
            MiddleArmenianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MiddleArmenianChatGPTPipeline with language: {self.language}"
        )


class CuneiformLuwianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Cuneiform Luwian."""

    description: Optional[str] = "Pipeline for the Cuneiform Luwian language"
    glottolog_id: Optional[str] = "cune1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CuneiformLuwianSentenceSplittingProcess,
            CuneiformLuwianChatGPTMorphosyntaxProcess,
            CuneiformLuwianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing CuneiformLuwianChatGPTPipeline with language: {self.language}"
        )
        logger.info("CuneiformLuwianChatGPTPipeline created.")


class HieroglyphicLuwianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Hieroglyphic Luwian."""

    description: Optional[str] = "Pipeline for the Hieroglyphic Luwian language"
    glottolog_id: Optional[str] = "hier1240"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HieroglyphicLuwianSentenceSplittingProcess,
            HieroglyphicLuwianChatGPTMorphosyntaxProcess,
            HieroglyphicLuwianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing HieroglyphicLuwianChatGPTPipeline with language: {self.language}"
        )
        logger.info("HieroglyphicLuwianChatGPTPipeline created.")


class LycianAChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Lycian."""

    description: Optional[str] = "Pipeline for the Lycian language"
    glottolog_id: Optional[str] = "lyci1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LycianASentenceSplittingProcess,
            LycianAChatGPTMorphosyntaxProcess,
            LycianAChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing LycianChatGPTPipeline with language: {self.language}"
        )
        logger.info("LycianChatGPTPipeline created.")


class LydianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Lydian."""

    description: Optional[str] = "Pipeline for the Lydian language"
    glottolog_id: Optional[str] = "lydi1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LydianSentenceSplittingProcess,
            LydianChatGPTMorphosyntaxProcess,
            LydianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing LydianChatGPTPipeline with language: {self.language}"
        )
        logger.info("LydianChatGPTPipeline created.")


class PalaicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Palaic."""

    description: Optional[str] = "Pipeline for the Palaic language"
    glottolog_id: Optional[str] = "pala1331"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PalaicSentenceSplittingProcess,
            PalaicChatGPTMorphosyntaxProcess,
            PalaicChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing PalaicChatGPTPipeline with language: {self.language}"
        )
        logger.info("PalaicChatGPTPipeline created.")


class CarianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Carian."""

    description: Optional[str] = "Pipeline for the Carian language"
    glottolog_id: Optional[str] = "cari1274"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CarianSentenceSplittingProcess,
            CarianChatGPTMorphosyntaxProcess,
            CarianChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing CarianChatGPTPipeline with language: {self.language}"
        )


class SauraseniPrakritChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Sauraseni Prakrit."""

    description: Optional[str] = "Pipeline for the Sauraseni Prakrit language"
    glottolog_id: Optional[str] = "saur1252"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SauraseniPrakritSentenceSplittingProcess,
            SauraseniPrakritChatGPTMorphosyntaxProcess,
            SauraseniPrakritChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing SauraseniPrakritChatGPTPipeline with language: {self.language}"
        )
        logger.info("SauraseniPrakritChatGPTPipeline created.")


class MaharastriPrakritChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Maharastri Prakrit."""

    description: Optional[str] = "Pipeline for the Maharastri Prakrit language"
    glottolog_id: Optional[str] = "maha1305"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MaharastriPrakritSentenceSplittingProcess,
            MaharastriPrakritChatGPTMorphosyntaxProcess,
            MaharastriPrakritChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MaharastriPrakritChatGPTPipeline with language: {self.language}"
        )
        logger.info("MaharastriPrakritChatGPTPipeline created.")


class MagadhiPrakritChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Magadhi Prakrit."""

    description: Optional[str] = "Pipeline for the Magadhi Prakrit language"
    glottolog_id: Optional[str] = "maga1260"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MagadhiPrakritSentenceSplittingProcess,
            MagadhiPrakritChatGPTMorphosyntaxProcess,
            MagadhiPrakritChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MagadhiPrakritChatGPTPipeline with language: {self.language}"
        )
        logger.info("MagadhiPrakritChatGPTPipeline created.")


class GandhariChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Gandhari."""

    description: Optional[str] = "Pipeline for the Gandhari language"
    glottolog_id: Optional[str] = "gand1259"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GandhariSentenceSplittingProcess,
            GandhariChatGPTMorphosyntaxProcess,
            GandhariChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing GandhariChatGPTPipeline with language: {self.language}"
        )
        logger.info("GandhariChatGPTPipeline created.")


# Hindi and closely related lects
class HindiChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Hindi (glottocode hind1269)."""

    description: Optional[str] = "Pipeline for the Hindi language"
    glottolog_id: Optional[str] = "hind1269"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HindiSentenceSplittingProcess,
            HindiChatGPTMorphosyntaxProcess,
            HindiChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing HindiChatGPTPipeline with language: {self.language}"
        )
        logger.info("HindiChatGPTPipeline created.")


class KhariBoliChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Khari Boli (Hindi dialect)."""

    description: Optional[str] = "Pipeline for the Khari Boli dialect of Hindi"
    glottolog_id: Optional[str] = "khad1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            KhariBoliSentenceSplittingProcess,
            KhariBoliChatGPTMorphosyntaxProcess,
            KhariBoliChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing KhariBoliChatGPTPipeline with language: {self.language}"
        )
        logger.info("KhariBoliChatGPTPipeline created.")


class BrajChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Braj Bhasha."""

    description: Optional[str] = "Pipeline for the Braj Bhasha language"
    glottolog_id: Optional[str] = "braj1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BrajSentenceSplittingProcess,
            BrajChatGPTMorphosyntaxProcess,
            BrajChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(f"Initializing BrajChatGPTPipeline with language: {self.language}")
        logger.info("BrajChatGPTPipeline created.")


class AwadhiChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Awadhi."""

    description: Optional[str] = "Pipeline for the Awadhi language"
    glottolog_id: Optional[str] = "awad1243"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AwadhiSentenceSplittingProcess,
            AwadhiChatGPTMorphosyntaxProcess,
            AwadhiChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing AwadhiChatGPTPipeline with language: {self.language}"
        )
        logger.info("AwadhiChatGPTPipeline created.")


class UrduChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Urdu."""

    description: Optional[str] = "Pipeline for the Urdu language"
    glottolog_id: Optional[str] = "urdu1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            UrduSentenceSplittingProcess,
            UrduChatGPTMorphosyntaxProcess,
            UrduChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(f"Initializing UrduChatGPTPipeline with language: {self.language}")
        logger.info("UrduChatGPTPipeline created.")


# Eastern Indo-Aryan and Western IA additions
class BengaliChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Bengali."""

    description: Optional[str] = "Pipeline for the Bengali language"
    glottolog_id: Optional[str] = "beng1280"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BengaliSentenceSplittingProcess,
            BengaliChatGPTMorphosyntaxProcess,
            BengaliChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing BengaliChatGPTPipeline with language: {self.language}"
        )
        logger.info("BengaliChatGPTPipeline created.")


class OdiaChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Odia (Oriya)."""

    description: Optional[str] = "Pipeline for the Odia language"
    glottolog_id: Optional[str] = "oriy1255"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OdiaSentenceSplittingProcess,
            OdiaChatGPTMorphosyntaxProcess,
            OdiaChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(f"Initializing OdiaChatGPTPipeline with language: {self.language}")
        logger.info("OdiaChatGPTPipeline created.")


class AssameseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Assamese."""

    description: Optional[str] = "Pipeline for the Assamese language"
    glottolog_id: Optional[str] = "assa1263"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AssameseSentenceSplittingProcess,
            AssameseChatGPTMorphosyntaxProcess,
            AssameseChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing AssameseChatGPTPipeline with language: {self.language}"
        )
        logger.info("AssameseChatGPTPipeline created.")


class GujaratiChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Gujarati."""

    description: Optional[str] = "Pipeline for the Gujarati language"
    glottolog_id: Optional[str] = "guja1252"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GujaratiSentenceSplittingProcess,
            GujaratiChatGPTMorphosyntaxProcess,
            GujaratiChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing GujaratiChatGPTPipeline with language: {self.language}"
        )
        logger.info("GujaratiChatGPTPipeline created.")


class MarathiChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Marathi."""

    description: Optional[str] = "Pipeline for the Marathi language"
    glottolog_id: Optional[str] = "mara1378"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MarathiSentenceSplittingProcess,
            MarathiChatGPTMorphosyntaxProcess,
            MarathiChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing MarathiChatGPTPipeline with language: {self.language}"
        )
        logger.info("MarathiChatGPTPipeline created.")


class SinhalaChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Sinhala."""

    description: Optional[str] = "Pipeline for the Sinhala language"
    glottolog_id: Optional[str] = "sinh1246"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SinhalaSentenceSplittingProcess,
            SinhalaChatGPTMorphosyntaxProcess,
            SinhalaChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing SinhalaChatGPTPipeline with language: {self.language}"
        )
        logger.info("SinhalaChatGPTPipeline created.")


class EasternPanjabiChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Eastern Panjabi."""

    description: Optional[str] = "Pipeline for the Eastern Panjabi language"
    glottolog_id: Optional[str] = "panj1256"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PanjabiSentenceSplittingProcess,
            EasternPanjabiChatGPTMorphosyntaxProcess,
            EasternPanjabiChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing EasternPanjabiChatGPTPipeline with language: {self.language}"
        )
        logger.info("EasternPanjabiChatGPTPipeline created.")


class SindhiChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Sindhi."""

    description: Optional[str] = "Pipeline for the Sindhi language"
    glottolog_id: Optional[str] = "sind1272"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SindhiSentenceSplittingProcess,
            SindhiChatGPTMorphosyntaxProcess,
            SindhiChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing SindhiChatGPTPipeline with language: {self.language}"
        )
        logger.info("SindhiChatGPTPipeline created.")


class KashmiriChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Kashmiri."""

    description: Optional[str] = "Pipeline for the Kashmiri language"
    glottolog_id: Optional[str] = "kash1277"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            KashmiriSentenceSplittingProcess,
            KashmiriChatGPTMorphosyntaxProcess,
            KashmiriChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing KashmiriChatGPTPipeline with language: {self.language}"
        )
        logger.info("KashmiriChatGPTPipeline created.")


# Sino-Tibetan additions
class OldChineseChatGPTPipeline(Pipeline):
    """Pipeline for Old Chinese."""

    description: Optional[str] = "Pipeline for Old Chinese"
    glottolog_id: Optional[str] = "oldc1244"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldChineseSentenceSplittingProcess,
            OldChineseChatGPTMorphosyntaxProcess,
            OldChineseChatGPTDependencyProcess,
        ]
    )


class MiddleChineseChatGPTPipeline(Pipeline):
    """Pipeline for Middle Chinese."""

    description: Optional[str] = "Pipeline for Middle Chinese"
    glottolog_id: Optional[str] = "midd1344"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleChineseSentenceSplittingProcess,
            MiddleChineseChatGPTMorphosyntaxProcess,
            MiddleChineseChatGPTDependencyProcess,
        ]
    )


class BaihuaChineseChatGPTPipeline(Pipeline):
    """Pipeline for Early Vernacular Chinese (Baihua)."""

    description: Optional[str] = "Pipeline for Early Vernacular Chinese (Baihua)"
    glottolog_id: Optional[str] = "clas1255"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BaihuaChineseSentenceSplittingProcess,
            BaihuaChineseChatGPTMorphosyntaxProcess,
            BaihuaChineseChatGPTDependencyProcess,
        ]
    )


class OldBurmeseChatGPTPipeline(Pipeline):
    """Pipeline for Old Burmese."""

    description: Optional[str] = "Pipeline for Old Burmese"
    glottolog_id: Optional[str] = "oldb1235"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldBurmeseSentenceSplittingProcess,
            OldBurmeseChatGPTMorphosyntaxProcess,
            OldBurmeseChatGPTDependencyProcess,
        ]
    )


class ClassicalBurmeseChatGPTPipeline(Pipeline):
    """Pipeline for Classical/Nuclear Burmese."""

    description: Optional[str] = "Pipeline for Classical Burmese"
    glottolog_id: Optional[str] = "nucl1310"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalBurmeseSentenceSplittingProcess,
            ClassicalBurmeseChatGPTMorphosyntaxProcess,
            ClassicalBurmeseChatGPTDependencyProcess,
        ]
    )


class TangutChatGPTPipeline(Pipeline):
    """Pipeline for Tangut (Xixia)."""

    description: Optional[str] = "Pipeline for the Tangut language"
    glottolog_id: Optional[str] = "tang1334"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TangutSentenceSplittingProcess,
            TangutChatGPTMorphosyntaxProcess,
            TangutChatGPTDependencyProcess,
        ]
    )


class NewarChatGPTPipeline(Pipeline):
    """Pipeline for Newar (Classical Nepal Bhasa)."""

    description: Optional[str] = "Pipeline for the Newar language"
    glottolog_id: Optional[str] = "newa1246"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            NewarSentenceSplittingProcess,
            NewarChatGPTMorphosyntaxProcess,
            NewarChatGPTDependencyProcess,
        ]
    )


class MeiteiChatGPTPipeline(Pipeline):
    """Pipeline for Meitei (Classical Manipuri)."""

    description: Optional[str] = "Pipeline for the Meitei (Classical Manipuri) language"
    glottolog_id: Optional[str] = "mani1292"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MeiteiSentenceSplittingProcess,
            MeiteiChatGPTMorphosyntaxProcess,
            MeiteiChatGPTDependencyProcess,
        ]
    )


class SgawKarenChatGPTPipeline(Pipeline):
    """Pipeline for Sgaw Karen."""

    description: Optional[str] = "Pipeline for the Sgaw Karen language"
    glottolog_id: Optional[str] = "sgaw1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SgawKarenSentenceSplittingProcess,
            SgawKarenChatGPTMorphosyntaxProcess,
            SgawKarenChatGPTDependencyProcess,
        ]
    )


class MiddleMongolChatGPTPipeline(Pipeline):
    """Pipeline for Middle Mongol."""

    description: Optional[str] = "Pipeline for the Middle Mongol language"
    glottolog_id: Optional[str] = "midd1351"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleMongolSentenceSplittingProcess,
            MiddleMongolChatGPTMorphosyntaxProcess,
            MiddleMongolChatGPTDependencyProcess,
        ]
    )


class ClassicalMongolianChatGPTPipeline(Pipeline):
    """Pipeline for Classical Mongolian."""

    description: Optional[str] = "Pipeline for the Classical Mongolian language"
    glottolog_id: Optional[str] = "mong1331"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalMongolianSentenceSplittingProcess,
            ClassicalMongolianChatGPTMorphosyntaxProcess,
            ClassicalMongolianChatGPTDependencyProcess,
        ]
    )


class MogholiChatGPTPipeline(Pipeline):
    """Pipeline for Mogholi (Moghol)."""

    description: Optional[str] = "Pipeline for the Mogholi (Moghol) language"
    glottolog_id: Optional[str] = "mogh1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MogholiSentenceSplittingProcess,
            MogholiChatGPTMorphosyntaxProcess,
            MogholiChatGPTDependencyProcess,
        ]
    )


class BagriChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Bagri (Rajasthani)."""

    description: Optional[str] = "Pipeline for the Bagri (Rajasthani) language"
    glottolog_id: Optional[str] = "bagr1243"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BagriSentenceSplittingProcess,
            BagriChatGPTMorphosyntaxProcess,
            BagriChatGPTDependencyProcess,
        ]
    )

    def __post_init__(self) -> None:
        logger.debug(
            f"Initializing BagriChatGPTPipeline with language: {self.language}"
        )
        logger.info("BagriChatGPTPipeline created.")


# Additional Afroasiatic, Altaic-adjacent, Uralic, Turkic, Dravidian pipelines
class NumidianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Numidian (Ancient Berber)."""

    description: Optional[str] = "Pipeline for the Numidian (Ancient Berber) language"
    glottolog_id: Optional[str] = "numi1241"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            NumidianSentenceSplittingProcess,
            NumidianChatGPTMorphosyntaxProcess,
            NumidianChatGPTDependencyProcess,
        ]
    )


class TaitaChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Taita (Cushitic)."""

    description: Optional[str] = "Pipeline for the Cushitic Taita language"
    glottolog_id: Optional[str] = "tait1247"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TaitaSentenceSplittingProcess,
            TaitaChatGPTMorphosyntaxProcess,
            TaitaChatGPTDependencyProcess,
        ]
    )


class HausaChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Hausa."""

    description: Optional[str] = "Pipeline for the Hausa language"
    glottolog_id: Optional[str] = "haus1257"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HausaSentenceSplittingProcess,
            HausaChatGPTMorphosyntaxProcess,
            HausaChatGPTDependencyProcess,
        ]
    )


class OldJurchenChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Jurchen."""

    description: Optional[str] = "Pipeline for the Old Jurchen language"
    glottolog_id: Optional[str] = "jurc1239"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldJurchenSentenceSplittingProcess,
            OldJurchenChatGPTMorphosyntaxProcess,
            OldJurchenChatGPTDependencyProcess,
        ]
    )


class OldJapaneseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Japanese."""

    description: Optional[str] = "Pipeline for the Old Japanese language"
    glottolog_id: Optional[str] = "japo1237"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldJapaneseSentenceSplittingProcess,
            OldJapaneseChatGPTMorphosyntaxProcess,
            OldJapaneseChatGPTDependencyProcess,
        ]
    )


class OldHungarianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Hungarian."""

    description: Optional[str] = "Pipeline for the Old Hungarian language"
    glottolog_id: Optional[str] = "oldh1242"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldHungarianSentenceSplittingProcess,
            OldHungarianChatGPTMorphosyntaxProcess,
            OldHungarianChatGPTDependencyProcess,
        ]
    )


class ChagataiChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Chagatai."""

    description: Optional[str] = "Pipeline for the Chagatai language"
    glottolog_id: Optional[str] = "chag1247"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ChagataiSentenceSplittingProcess,
            ChagataiChatGPTMorphosyntaxProcess,
            ChagataiChatGPTDependencyProcess,
        ]
    )


class OldTurkicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Turkic."""

    description: Optional[str] = "Pipeline for the Old Turkic language"
    glottolog_id: Optional[str] = "oldu1238"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldTurkicSentenceSplittingProcess,
            OldTurkicChatGPTMorphosyntaxProcess,
            OldTurkicChatGPTDependencyProcess,
        ]
    )


class OldTamilChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Tamil."""

    description: Optional[str] = "Pipeline for the Old Tamil language"
    glottolog_id: Optional[str] = "oldt1248"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldTamilSentenceSplittingProcess,
            OldTamilChatGPTMorphosyntaxProcess,
            OldTamilChatGPTDependencyProcess,
        ]
    )


# Northwest Semitic and Aramaic additions
class MoabiteChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Moabite."""

    description: Optional[str] = "Pipeline for the Moabite language"
    glottolog_id: Optional[str] = "moab1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MoabiteSentenceSplittingProcess,
            MoabiteChatGPTMorphosyntaxProcess,
            MoabiteChatGPTDependencyProcess,
        ]
    )


class AmmoniteChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Ammonite."""

    description: Optional[str] = "Pipeline for the Ammonite language"
    glottolog_id: Optional[str] = "ammo1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AmmoniteSentenceSplittingProcess,
            AmmoniteChatGPTMorphosyntaxProcess,
            AmmoniteChatGPTDependencyProcess,
        ]
    )


class EdomiteChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Edomite."""

    description: Optional[str] = "Pipeline for the Edomite language"
    glottolog_id: Optional[str] = "edom1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            EdomiteSentenceSplittingProcess,
            EdomiteChatGPTMorphosyntaxProcess,
            EdomiteChatGPTDependencyProcess,
        ]
    )


class OldAramaicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Aramaic (up to 700 BCE)."""

    description: Optional[str] = "Pipeline for Old Aramaic (up to 700 BCE)"
    glottolog_id: Optional[str] = "olda1246"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldAramaicSentenceSplittingProcess,
            OldAramaicChatGPTMorphosyntaxProcess,
            OldAramaicChatGPTDependencyProcess,
        ]
    )


class OldAramaicSamalianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Aramaic–Samʾalian."""

    description: Optional[str] = "Pipeline for Old Aramaic–Samʾalian"
    glottolog_id: Optional[str] = "olda1245"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldAramaicSamalianSentenceSplittingProcess,
            OldAramaicSamalianChatGPTMorphosyntaxProcess,
            OldAramaicSamalianChatGPTDependencyProcess,
        ]
    )


class MiddleAramaicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Aramaic."""

    description: Optional[str] = "Pipeline for Middle Aramaic"
    glottolog_id: Optional[str] = "midd1366"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleAramaicSentenceSplittingProcess,
            MiddleAramaicChatGPTMorphosyntaxProcess,
            MiddleAramaicChatGPTDependencyProcess,
        ]
    )


class ClassicalMandaicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Mandaic."""

    description: Optional[str] = "Pipeline for Classical Mandaic"
    glottolog_id: Optional[str] = "clas1253"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalMandaicSentenceSplittingProcess,
            ClassicalMandaicChatGPTMorphosyntaxProcess,
            ClassicalMandaicChatGPTDependencyProcess,
        ]
    )


class HatranChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Hatran."""

    description: Optional[str] = "Pipeline for Hatran"
    glottolog_id: Optional[str] = "hatr1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HatranSentenceSplittingProcess,
            HatranChatGPTMorphosyntaxProcess,
            HatranChatGPTDependencyProcess,
        ]
    )


class JewishBabylonianAramaicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Jewish Babylonian Aramaic."""

    description: Optional[str] = "Pipeline for Jewish Babylonian Aramaic"
    glottolog_id: Optional[str] = "jewi1240"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            JewishBabylonianAramaicSentenceSplittingProcess,
            JewishBabylonianAramaicChatGPTMorphosyntaxProcess,
            JewishBabylonianAramaicChatGPTDependencyProcess,
        ]
    )


class SamalianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Samʾalian."""

    description: Optional[str] = "Pipeline for Samʾalian"
    glottolog_id: Optional[str] = "sama1234"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SamalianSentenceSplittingProcess,
            SamalianChatGPTMorphosyntaxProcess,
            SamalianChatGPTDependencyProcess,
        ]
    )


MAP_LANGUAGE_CODE_TO_STANZA_PIPELINE: dict[str, type[Pipeline]] = {
    # "akk": AkkadianPipeline,
    # "ang": OldEnglishPipeline,
    # "arb": ArabicPipeline,
    # "arc": AramaicPipeline,
    # "chu": OCSPipeline,
    # "cop": CopticPipeline,
    # "enm": MiddleEnglishPipeline,
    # "frm": MiddleFrenchPipeline,
    # "fro": OldFrenchPipeline,
    # "gmh": MiddleHighGermanPipeline,
    # "got": GothicPipeline,
    # "grc": GreekPipeline,
    # "hin": HindiPipeline,
    # "lat": LatinPipeline,
    # "lzh": ChinesePipeline,
    # "non": OldNorsePipeline,
    # "pan": PanjabiPipeline,
    # "pli": PaliPipeline,
    # "san": SanskritPipeline,
}


MAP_LANGUAGE_CODE_TO_SPACY_PIPELINE: dict[str, type[Pipeline]] = dict()


MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE: dict[str, type[Pipeline]] = {
    # Indo-European family
    ## Italic
    "lati1261": LatinChatGPTPipeline,
    "oldf1239": OldFrenchChatGPTPipeline,
    "midd1316": MiddleFrenchChatGPTPipeline,
    # Other Romance languages
    ## Hellenic
    "anci1242": AncientGreekChatGPTPipeline,
    # Mycenaean Greek (Linear B tablets, ca. 1400–1200 BCE).
    # Medieval/Byzantine Greek
    "oldi1245": EarlyIrishChatGPTPipeline,
    "oldw1239": OldMiddleWelshChatGPTPipeline,
    "bret1244": MiddleBretonChatGPTPipeline,
    "corn1251": CornishChatGPTPipeline,
    ## Germanic
    # Proto-Norse
    "goth1244": GothicChatGPTPipeline,
    "oldh1241": OldHighGermanChatGPTPipeline,
    "midd1343": MiddleHighGermanChatGPTPipeline,
    "oldn1244": OldNorseChatGPTPipeline,
    "olde1238": OldEnglishChatGPTPipeline,
    "midd1317": MiddleEnglishChatGPTPipeline,
    ## Balto-Slavic
    "chur1257": ChurchSlavonicChatGPTPipeline,
    "prus1238": OldPrussianChatGPTPipeline,
    "lith1251": LithuanianChatGPTPipeline,
    "latv1249": LatvianChatGPTPipeline,
    "gheg1238": AlbanianChatGPTPipeline,
    ## Armenian, Earliest texts: 5th c. CE (Bible translation by Mesrop Mashtots, who created the script)
    "clas1256": ClassicalArmenianChatGPTPipeline,
    "midd1364": MiddleArmenianChatGPTPipeline,
    # Note this is only a parent, not true languoid
    ## Anatolian
    "hitt1242": HittiteChatGPTPipeline,
    "cune1239": CuneiformLuwianChatGPTPipeline,
    "hier1240": HieroglyphicLuwianChatGPTPipeline,
    "lyci1241": LycianAChatGPTPipeline,
    "lydi1241": LydianChatGPTPipeline,
    "pala1331": PalaicChatGPTPipeline,
    "cari1274": CarianChatGPTPipeline,
    ## Tocharian
    "tokh1242": TocharianAChatGPTPipeline,
    "tokh1243": TocharianBChatGPTPipeline,
    ## Indo-Iranian
    ## Iranian languages
    ### SW Iranian
    "oldp1254": OldPersianChatGPTPipeline,
    "pahl1241": MiddlePersianChatGPTPipeline,
    ### NW Iranian
    "part1239": ParthianChatGPTPipeline,
    ### E Iranian
    "aves1237": AvestanChatGPTPipeline,
    "bact1239": BactrianChatGPTPipeline,
    "sogd1245": SogdianChatGPTPipeline,
    "khot1251": KhotaneseChatGPTPipeline,
    "tums1237": TumshuqeseChatGPTPipeline,
    # Indo-Aryan (Indic): Sanskrit (Vedic & Classical), Prakrits, Pali, later medieval languages (Hindi, Bengali, etc.)
    ## Old Indo-Aryan
    "vedi1234": VedicSanskritChatGPTPipeline,
    "clas1258": ClassicalSanskritChatGPTPipeline,
    # Prakrits (Middle Indo-Aryan, ca. 500 BCE–500 CE)
    "pali1273": PaliChatGPTPipeline,
    # Ardhamāgadhī, Śaurasenī, Mahārāṣṭrī, etc. — languages of Jain/Buddhist texts and early drama.
    # ? Glotto says alt_name for Pali; Ardhamāgadhī, literary language associated with Magadha (eastern India); Jain canonical texts (the Āgamas) are written primarily in Ardhamāgadhī
    "saur1252": SauraseniPrakritChatGPTPipeline,
    "maha1305": MaharastriPrakritChatGPTPipeline,
    "maga1260": MagadhiPrakritChatGPTPipeline,
    "gand1259": GandhariChatGPTPipeline,  ## Middle Indo-Aryan
    # "Maithili": "mait1250"; Apabhraṃśa; "Apabhramsa" is alt_name; (500–1200 CE); Bridges Prakrits → New Indo-Aryan
    ## New Indo-Aryan
    ## Medieval languages (~1200 CE onward):
    # Early forms of Hindi, Bengali, Gujarati, Marathi, Punjabi, Oriya, Sinhala, etc
    # North-Western / Hindi Belt
    "hind1269": HindiChatGPTPipeline,
    "khad1239": KhariBoliChatGPTPipeline,
    "braj1242": BrajChatGPTPipeline,
    "awad1243": AwadhiChatGPTPipeline,
    "urdu1245": UrduChatGPTPipeline,
    # Eastern Indo-Aryan
    "beng1280": BengaliChatGPTPipeline,
    "oriy1255": OdiaChatGPTPipeline,
    "assa1263": AssameseChatGPTPipeline,
    # Western Indo-Aryan
    "guja1252": GujaratiChatGPTPipeline,
    "mara1378": MarathiChatGPTPipeline,
    # Southern Indo-Aryan / adjacency
    "sinh1246": SinhalaChatGPTPipeline,
    # Northwestern frontier
    "panj1256": EasternPanjabiChatGPTPipeline,
    "sind1272": SindhiChatGPTPipeline,
    "kash1277": KashmiriChatGPTPipeline,
    "bagr1243": BagriChatGPTPipeline,
    # Afroasiatic family
    ## Semitic languages
    ### East Semitic
    "akka1240": AkkadianChatGPTPipeline,
    # Eblaite
    ### West Semitic
    "ugar1238": UgariticChatGPTPipeline,
    "phoe1239": PhoenicianChatGPTPipeline,
    "moab1234": MoabiteChatGPTPipeline,
    "ammo1234": AmmoniteChatGPTPipeline,
    "edom1234": EdomiteChatGPTPipeline,
    "anci1244": BiblicalHebrewChatGPTPipeline,
    # Medieval Hebrew: No Glottolog
    # "moab1234": Moabite
    # "ammo1234": Ammonite
    # "edom1234": Edomite
    # Old Aramaic (ca. 1000–700 BCE, inscriptions).
    # "olda1246": "Old Aramaic (up to 700 BCE)",
    # "Old Aramaic-Sam'alian": "olda1245"
    "impe1235": ImperialAramaicChatGPTPipeline,
    "olda1246": OldAramaicChatGPTPipeline,
    "olda1245": OldAramaicSamalianChatGPTPipeline,
    "midd1366": MiddleAramaicChatGPTPipeline,
    "clas1253": ClassicalMandaicChatGPTPipeline,
    "hatr1234": HatranChatGPTPipeline,
    "jewi1240": JewishBabylonianAramaicChatGPTPipeline,
    "sama1234": SamalianChatGPTPipeline,
    # "midd1366": Middle Aramaic (200 BCE – 700 CE), includes Biblical Aramaic, Palmyrene, Nabataean, Targumic Aramaic.
    # Eastern Middle Aramaic
    ##  Classical Mandaic, Hatran, Jewish Babylonian Aramaic dialects, and Classical Syriac
    "clas1252": ClassicalSyriacChatGPTPipeline,
    ### NW Semitic
    ## South Semitic
    # Old South Arabian (OSA)
    "geez1241": GeezChatGPTPipeline,
    ### Central Semitic (bridge between NW and South)
    # Pre-Islamic Arabic
    "clas1259": ClassicalArabicChatGPTPipeline,  # Dialect
    # Glotto doesn't have medieval arabic; Medieval Arabic: scientific, philosophical, historical works dominate much of the Islamic Golden Age corpus.
    ## Egyptian languages
    "olde1242": OldEgyptianChatGPTPipeline,
    "midd1369": MiddleEgyptianChatGPTPipeline,
    "late1256": LateEgyptianChatGPTPipeline,
    "demo1234": DemoticChatGPTPipeline,
    "copt1239": CopticChatGPTPipeline,
    ## Berber
    "numi1241": NumidianChatGPTPipeline,
    "tait1247": TaitaChatGPTPipeline,
    ## Chadic
    # ; "haus1257": "Hausa"; Hausa; Essentially oral until medieval period, when Hausa is written in Ajami (Arabic script).
    "haus1257": HausaChatGPTPipeline,
    "lite1248": LiteraryChineseChatGPTPipeline,
    "clas1254": ClassicalTibetanPipeline,
    # Sino-Tibetan family
    # | **Early Vernacular Chinese (Baihua)**   | ca. 10th – 18th c. CE | *(under `clas1255`)* |
    # | **Old Tibetan**                         | 7th – 10th c. CE     | *(not separately coded)* |
    "oldc1244": OldChineseChatGPTPipeline,
    "midd1344": MiddleChineseChatGPTPipeline,
    "clas1255": BaihuaChineseChatGPTPipeline,
    "oldb1235": OldBurmeseChatGPTPipeline,
    "nucl1310": ClassicalBurmeseChatGPTPipeline,
    "tang1334": TangutChatGPTPipeline,
    "newa1246": NewarChatGPTPipeline,
    "mani1292": MeiteiChatGPTPipeline,
    "sgaw1245": SgawKarenChatGPTPipeline,
    # Mongolic family
    "mong1329": MiddleMongolChatGPTPipeline,
    "mong1331": ClassicalMongolianChatGPTPipeline,  #  TODO: No glottolog broken
    "mogh1245": MogholiChatGPTPipeline,
    # Altaic-Adj.
    "jurc1239": OldJurchenChatGPTPipeline,
    # Japonic
    "japo1237": OldJapaneseChatGPTPipeline,
    # Uralic
    "oldh1242": OldHungarianChatGPTPipeline,
    # Turkic
    "chag1247": ChagataiChatGPTPipeline,
    "oldu1238": OldTurkicChatGPTPipeline,
    # Dravidian
    "oldt1248": OldTamilChatGPTPipeline,
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
