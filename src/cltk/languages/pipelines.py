"""Processing pipelines for languages."""

from typing import Optional, Type

from pydantic import Field

from cltk.alphabet.processes import (  # AncientGreekNormalizeProcess,; LatinNormalizeProcess,
    MultilingualNormalizeProcess,
)
from cltk.core.cltk_logger import logger
from cltk.core.data_types_v3 import Dialect, Language, Pipeline, Process

# from cltk.dependency.processes import (
#     ChineseStanzaProcess,
#     CopticStanzaProcess,
#     GothicStanzaProcess,
#     GreekSpacyProcess,
#     GreekStanzaProcess,
#     LatinSpacyProcess,
#     LatinStanzaProcess,
#     OCSStanzaProcess,
#     OldFrenchStanzaProcess,
# )
# from cltk.embeddings.processes import (
#     ArabicEmbeddingsProcess,
#     AramaicEmbeddingsProcess,
#     GothicEmbeddingsProcess,
#     GreekEmbeddingsProcess,
#     LatinEmbeddingsProcess,
#     MiddleEnglishEmbeddingsProcess,
#     OldEnglishEmbeddingsProcess,
#     PaliEmbeddingsProcess,
#     SanskritEmbeddingsProcess,
# )
from cltk.genai.processes import (
    AkkadianChatGPTProcess,
    AlbanianChatGPTProcess,
    AncientGreekChatGPTProcess,
    AvestanChatGPTProcess,
    BactrianChatGPTProcess,
    BiblicalHebrewChatGPTProcess,
    ChurchSlavicChatGPTProcess,
    ClassicalArabicChatGPTProcess,
    ClassicalArmenianChatGPTProcess,
    ClassicalSyriacChatGPTProcess,
    ClassicalTibetanChatGPTProcess,
    CopticChatGPTProcess,
    DemoticChatGPTProcess,
    EarlyIrishChatGPTProcess,
    GeezChatGPTProcess,
    GothicChatGPTProcess,
    HindiChatGPTProcess,
    HittiteChatGPTProcess,
    KhotaneseChatGPTProcess,
    LateEgyptianChatGPTProcess,
    LatinChatGPTProcess,
    LatvianChatGPTProcess,
    LiteraryChineseChatGPTProcess,
    LithuanianChatGPTProcess,
    MiddleArmenianChatGPTProcess,
    MiddleBretonChatGPTProcess,
    MiddleCornishChatGPTProcess,
    MiddleEgyptianChatGPTProcess,
    MiddleEnglishChatGPTProcess,
    MiddleFrenchChatGPTProcess,
    MiddleHighGermanChatGPTProcess,
    MiddlePersianChatGPTProcess,
    OfficialAramaicChatGPTProcess,
    OldEgyptianChatGPTProcess,
    OldEnglishChatGPTProcess,
    OldFrenchChatGPTProcess,
    OldHighGermanChatGPTProcess,
    OldMiddleWelshChatGPTProcess,
    OldNorseChatGPTProcess,
    OldPersianChatGPTProcess,
    OldPrussianChatGPTProcess,
    PaliChatGPTProcess,
    ParthianChatGPTProcess,
    PhoenicianChatGPTProcess,
    PunjabiChatGPTProcess,
    SanskritChatGPTProcess,
    SogdianChatGPTProcess,
    TokharianAChatGPTProcess,
    TokharianBChatGPTProcess,
    TumshuqeseChatGPTProcess,
    UgariticChatGPTProcess,
)

# from cltk.languages.utils import get_lang
from cltk.languages.glottolog_v3 import get_dialect, get_language, resolve_languoid

# from cltk.lemmatize.processes import (
#     GreekLemmatizationProcess,
#     LatinLemmatizationProcess,
#     OldEnglishLemmatizationProcess,
#     OldFrenchLemmatizationProcess,
# )
# from cltk.lexicon.processes import LatinLexiconProcess, OldNorseLexiconProcess
# from cltk.ner.processes import (  # GreekNERProcess,; LatinNERProcess,; OldEnglishNERProcess,
#     OldFrenchNERProcess,
# )
from cltk.sentence.processes import (
    AkkadianSentenceSplittingProcess,
    AlbanianSentenceSplittingProcess,
    AncientGreekSentenceSplittingProcess,
    AncientHebrewSentenceSplittingProcess,
    AvestanSentenceSplittingProcess,
    BactrianSentenceSplittingProcess,
    ChurchSlavonicSentenceSplittingProcess,
    ClassicalArabicSentenceSplittingProcess,
    ClassicalArmenianSentenceSplittingProcess,
    ClassicalSyriacSentenceSplittingProcess,
    ClassicalTibetanSentenceSplittingProcess,
    CopticSentenceSplittingProcess,
    DemoticSentenceSplittingProcess,
    EarlyIrishSentenceSplittingProcess,
    GeezSentenceSplittingProcess,
    GothicSentenceSplittingProcess,
    HindiSentenceSplittingProcess,
    HittiteSentenceSplittingProcess,
    KhotaneseSentenceSplittingProcess,
    LateEgyptianSentenceSplittingProcess,
    LatinSentenceSplittingProcess,
    LatvianSentenceSplittingProcess,
    LiteraryChineseSentenceSplittingProcess,
    LithuanianSentenceSplittingProcess,
    MiddleArmenianSentenceSplittingProcess,
    MiddleBretonSentenceSplittingProcess,
    MiddleCornishSentenceSplittingProcess,
    MiddleEgyptianSentenceSplittingProcess,
    MiddleEnglishSentenceSplittingProcess,
    MiddleFrenchSentenceSplittingProcess,
    MiddleHighGermanSentenceSplittingProcess,
    MiddlePersianSentenceSplittingProcess,
    OfficialAramaicSentenceSplittingProcess,
    OldEgyptianSentenceSplittingProcess,
    OldEnglishSentenceSplittingProcess,
    OldFrenchSentenceSplittingProcess,
    OldHighGermanSentenceSplittingProcess,
    OldMiddleWelshSentenceSplittingProcess,
    OldNorseSentenceSplittingProcess,
    OldPersianSentenceSplittingProcess,
    OldPrussianSentenceSplittingProcess,
    PaliSentenceSplittingProcess,
    PanjabiSentenceSplittingProcess,
    ParthianSentenceSplittingProcess,
    PhoenicianSentenceSplittingProcess,
    SanskritSentenceSplittingProcess,
    SogdianSentenceSplittingProcess,
    TocharianASentenceSplittingProcess,
    TocharianBSentenceSplittingProcess,
    TumshuqeseSentenceSplittingProcess,
    UgariticSentenceSplittingProcess,
)

# from cltk.stops.processes import StopsProcess
# from cltk.tokenizers.processes import (
#     AkkadianTokenizationProcess,
#     ArabicTokenizationProcess,
#     GreekTokenizationProcess,
#     LatinTokenizationProcess,
#     MiddleEnglishTokenizationProcess,
#     MiddleFrenchTokenizationProcess,
#     MiddleHighGermanTokenizationProcess,
#     MultilingualTokenizationProcess,
#     OldFrenchTokenizationProcess,
#     OldNorseTokenizationProcess,
# )


# class AkkadianPipeline(Pipeline):
#     """Default ``Pipeline`` for Akkadian."""

#     description: Optional[str] = "Pipeline for the Akkadian language."
#     language: Optional[Language] = get_language("akk")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [AkkadianTokenizationProcess, StopsProcess]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing AkkadianPipeline with language: {self.language}")
#         logger.info("AkkadianPipeline created.")


class AkkadianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Akkadian."""

    description: Optional[str] = "Pipeline for the Akkadian language"
    glottolog_id: Optional[str] = "akka1240"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AkkadianSentenceSplittingProcess,
            AkkadianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        assert self.language, "Language not found"
        logger.debug(
            f"Initializing AkkadianChatGPTPipeline with language: {self.language.name}"
        )
        logger.info("AkkadianChatGPTPipeline created.")


# class ArabicPipeline(Pipeline):
#     """Default ``Pipeline`` for Arabic."""

#     description: Optional[str] = "Pipeline for the Arabic language"
#     language: Optional[Language] = get_language("arb-cla")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             ArabicTokenizationProcess,
#             ArabicEmbeddingsProcess,
#             StopsProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing ArabicPipeline with language: {self.language}")
#         logger.info("ArabicPipeline created.")


class ClassicalArabicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Arabic."""

    description: Optional[str] = "Pipeline for the Arabic language"
    glottolog_id: Optional[str] = "clas1259"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalArabicSentenceSplittingProcess,
            ClassicalArabicChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing ArabicChatGPTPipeline with language: {self.language}"
        )
        logger.info("ArabicChatGPTPipeline created.")


#
class ClassicalSyriacChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Syriac."""

    description: Optional[str] = "Pipeline for the Classical Syriac language"
    glottolog_id: Optional[str] = "clas1252"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalSyriacSentenceSplittingProcess,
            ClassicalSyriacChatGPTProcess,
        ]
    )

    def __post_init__(self):
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
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalTibetanSentenceSplittingProcess,
            ClassicalTibetanChatGPTProcess,
        ]
    )

    def __post_init__(self):
        assert self.language, "Language not found"
        logger.debug(
            f"Initializing ClassicalTibetanChatGPTPipeline with language: {self.language.name}"
        )
        logger.info("ClassicalTibetanChatGPTPipeline created.")


# class AramaicPipeline(Pipeline):
#     """Default ``Pipeline`` for Aramaic."""

#     description: Optional[str] = "Pipeline for the Aramaic language"
#     language: Optional[Language] = get_language("arc")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             ArabicTokenizationProcess,  # Note: Using Arabic tokenizer for Aramaic. Is this OK?
#             AramaicEmbeddingsProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing AramaicPipeline with language: {self.language}")
#         logger.info("AramaicPipeline created.")
#         logger.warning("Using Arabic tokenizer for Aramaic. Is this OK?")


# class ChinesePipeline(Pipeline):
#     """Default ``Pipeline`` for Classical Chinese."""

#     description: Optional[str] = "Pipeline for the Classical Chinese language"
#     language: Optional[Language] = get_language("lzh")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [ChineseStanzaProcess]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing ChinesePipeline with language: {self.language}")
#         logger.info("ChinesePipeline created.")


# class CopticPipeline(Pipeline):
#     """Default ``Pipeline`` for Coptic."""

#     description: Optional[str] = "Pipeline for the Coptic language"
#     language: Optional[Language] = get_language("cop")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [CopticStanzaProcess, StopsProcess]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing CopticPipeline with language: {self.language}")
#         logger.info("CopticPipeline created.")


class CopticChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Coptic."""

    description: Optional[str] = "ChatGPT Pipeline for the Coptic language."
    glottolog_id: Optional[str] = "copt1239"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CopticSentenceSplittingProcess,
            CopticChatGPTProcess,
        ]
    )


# class GothicPipeline(Pipeline):
#     """Default ``Pipeline`` for Gothic."""

#     description: Optional[str] = "Pipeline for the Gothic language"
#     language: Optional[Language] = get_language("got")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [GothicStanzaProcess, GothicEmbeddingsProcess]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing GothicPipeline with language: {self.language}")
#         logger.info("GothicPipeline created.")


class GothicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic."""

    description: Optional[str] = "Pipeline for the Gothic language"
    glottolog_id: Optional[str] = "goth1244"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GothicSentenceSplittingProcess,
            GothicChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing GothicChatGPTPipeline with language: {self.language}"
        )
        logger.info("GothicChatGPTPipeline created.")


# class GreekPipeline(Pipeline):
#     """Default ``Pipeline`` for Ancient Greek."""

#     description: Optional[str] = "Pipeline for the Greek language"
#     language: Optional[Language] = get_language("grc")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             AncientGreekNormalizeProcess,
#             GreekSpacyProcess,
#             GreekEmbeddingsProcess,
#             StopsProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing GreekPipeline with language: {self.language}")
#         logger.info("GreekPipeline created.")


class GreekChatGPTPipeline(Pipeline):
    """Pipeline for Ancient Greek using normalization and ChatGPT annotation only."""

    description: Optional[str] = "Pipeline for Ancient Greek with ChatGPT annotation"
    glottolog_id: Optional[str] = "anci1242"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            # AncientGreekNormalizeProcess,
            MultilingualNormalizeProcess,
            AncientGreekSentenceSplittingProcess,
            AncientGreekChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing GreekChatGPTPipeline with language: {self.language}"
        )
        logger.info("GreekChatGPTPipeline created.")


# class HindiPipeline(Pipeline):
#     """Default ``Pipeline`` for Hindi."""

#     description: Optional[str] = "Pipeline for the Hindi language."
#     language: Optional[Language] = get_language("hin")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [MultilingualTokenizationProcess, StopsProcess]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing HindiPipeline with language: {self.language}")
#         logger.info("HindiPipeline created.")


class BiblicalHebrewChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Hebrew."""

    description: Optional[str] = "Pipeline for the Ancient Hebrew language."
    glottolog_id: Optional[str] = "anci1244"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AncientHebrewSentenceSplittingProcess,
            BiblicalHebrewChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing LatinPipeline with language: {self.language}")
        logger.info("LatinPipeline created.")


# class LatinPipeline(Pipeline):
#     """Default ``Pipeline`` for Latin."""

#     description: Optional[str] = "Pipeline for the Latin language."
#     language: Optional[Language] = get_language("lat")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             LatinNormalizeProcess,
#             LatinStanzaProcess,
#             LatinEmbeddingsProcess,
#             StopsProcess,
#             LatinLexiconProcess,
#         ]
#     )


class LatinChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Latin."""

    description: Optional[str] = "ChatGPT Pipeline for the Latin language."
    glottolog_id: Optional[str] = "lati1261"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            # LatinNormalizeProcess,
            MultilingualNormalizeProcess,
            LatinSentenceSplittingProcess,
            LatinChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing LatinPipeline with language: {self.language}")
        logger.info("LatinPipeline created.")


# class MiddleHighGermanPipeline(Pipeline):
#     """Default ``Pipeline`` for Middle High German."""

#     description: Optional[str] = "Pipeline for the Middle High German language."
#     language: Optional[Language] = get_language("gmh")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [MiddleHighGermanTokenizationProcess, StopsProcess]
#     )

#     def __post_init__(self):
#         logger.debug(
#             f"Initializing MiddleHighGermanPipeline with language: {self.language}"
#         )
#         logger.info("MiddleHighGermanPipeline created.")


# class MiddleEnglishPipeline(Pipeline):
#     """Default ``Pipeline`` for Middle English."""

#     description: Optional[str] = "Pipeline for the Middle English language"
#     language: Optional[Language] = get_language("enm")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             MiddleEnglishTokenizationProcess,
#             StopsProcess,
#             MiddleEnglishEmbeddingsProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(
#             f"Initializing MiddleEnglishPipeline with language: {self.language}"
#         )
#         logger.info("MiddleEnglishPipeline created.")


class MiddleEnglishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle English."""

    description: Optional[str] = "Pipeline for the Middle English language"
    glottolog_id: Optional[str] = "midd1317"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleEnglishSentenceSplittingProcess,
            MiddleEnglishChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddleEnglishChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleEnglishChatGPTPipeline created.")


# class MiddleFrenchPipeline(Pipeline):
#     """Default ``Pipeline`` for Middle French."""

#     description: Optional[str] = "Pipeline for the Middle French language"
#     language: Optional[Language] = get_language("frm")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [MiddleFrenchTokenizationProcess]
#     )

#     def __post_init__(self):
#         logger.debug(
#             f"Initializing MiddleFrenchPipeline with language: {self.language}"
#         )
#         logger.info("MiddleFrenchPipeline created.")


class MiddleFrenchChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle French."""

    description: Optional[str] = "Pipeline for the Middle French language"
    glottolog_id: Optional[str] = "midd1316"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleFrenchSentenceSplittingProcess,
            MiddleFrenchChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddleFrenchChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleFrenchChatGPTPipeline created.")


# class OCSPipeline(Pipeline):
#     """Default ``Pipeline`` for Old Church Slavonic."""

#     description: Optional[str] = "Pipeline for the Old Church Slavonic language"
#     language: Optional[Language] = get_language("chu")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [OCSStanzaProcess]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing OCSPipeline with language: {self.language}")
#         logger.info("OCSPipeline created.")


class MiddlePersianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Persian (Pahlavi)."""

    description: Optional[str] = "Pipeline for the Middle Persian (Pahlavi) language"
    glottolog_id: Optional[str] = "pahl1241"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddlePersianSentenceSplittingProcess,
            MiddlePersianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddlePersianChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddlePersianChatGPTPipeline created.")


class ImperialAramaicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Official Aramaic."""

    description: Optional[str] = "ChatGPT Pipeline for the Official Aramaic language."
    glottolog_id: Optional[str] = "impe1235"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OfficialAramaicSentenceSplittingProcess,
            OfficialAramaicChatGPTProcess,
        ]
    )


class ChurchSlavonicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for (Old) Church Slavonic."""

    description: Optional[str] = "Pipeline for the Church Slavonic language"
    glottolog_id: Optional[str] = "chur1257"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ChurchSlavonicSentenceSplittingProcess,
            ChurchSlavicChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing ChurchSlavonicChatGPTPipeline with language: {self.language}"
        )
        logger.info("ChurchSlavonicChatGPTPipeline")


# class OldEnglishPipeline(Pipeline):
#     """Default ``Pipeline`` for Old English."""

#     description: Optional[str] = "Pipeline for the Old English language"
#     language: Optional[Language] = get_language("ang")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             MultilingualTokenizationProcess,
#             OldEnglishLemmatizationProcess,
#             OldEnglishEmbeddingsProcess,
#             StopsProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing OldEnglishPipeline with language: {self.language}")
#         logger.info("OldEnglishPipeline created.")


class OldEnglishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old English."""

    description: Optional[str] = "Pipeline for the Old English language"
    glottolog_id: Optional[str] = "olde1238"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldEnglishSentenceSplittingProcess,
            OldEnglishChatGPTProcess,
        ]
    )

    def __post_init__(self):
        assert self.language, "Language not found"
        logger.debug(
            f"Initializing OldEnglishChatGPTPipeline with language: {self.language.name}"
        )
        logger.info("OldEnglishChatGPTPipeline created.")


# class OldFrenchPipeline(Pipeline):
#     """Default ``Pipeline`` for Old French."""

#     description: Optional[str] = "Pipeline for the Old French language"
#     language: Optional[Language] = get_language("fro")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             OldFrenchStanzaProcess,
#             StopsProcess,
#             OldFrenchNERProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing OldFrenchPipeline with language: {self.language}")
#         logger.info("OldFrenchPipeline created.")


class OldFrenchChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old French."""

    description: Optional[str] = "Pipeline for the Old French language"
    glottolog_id: Optional[str] = "oldf1239"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldFrenchSentenceSplittingProcess,
            OldFrenchChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing OldFrenchChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldFrenchChatGPTPipeline created.")


# class OldNorsePipeline(Pipeline):
#     """Default ``Pipeline`` for Old Norse."""

#     description: Optional[str] = "Pipeline for the Old Norse language"
#     language: Optional[Language] = get_language("non")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             OldNorseTokenizationProcess,
#             StopsProcess,
#             OldNorseLexiconProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing OldNorsePipeline with language: {self.language}")
#         logger.info("OldNorsePipeline created.")


class OldNorseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Norse."""

    description: Optional[str] = "Pipeline for the Old Norse language"
    glottolog_id: Optional[str] = "oldn1244"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldNorseSentenceSplittingProcess,
            OldNorseChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing OldNorseChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldNorseChatGPTPipeline created.")


# class PaliPipeline(Pipeline):
#     """Default ``Pipeline`` for Pali."""

#     description: Optional[str] = "Pipeline for the Pali language"
#     language: Optional[Language] = get_language("pli")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [MultilingualTokenizationProcess, PaliEmbeddingsProcess]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing PaliPipeline with language: {self.language}")
#         logger.info("PaliPipeline created.")


class PaliChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Pali."""

    description: Optional[str] = "Pipeline for the Pali language"
    glottolog_id: Optional[str] = "pali1273"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PaliSentenceSplittingProcess,
            PaliChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing PaliPipeline with language: {self.language}")
        logger.info("PaliPipeline created.")


# class PanjabiPipeline(Pipeline):
#     """Default ``Pipeline`` for Panjabi."""

#     description: Optional[str] = "Pipeline for the Panjabi language."
#     language: Optional[Language] = get_language("pan")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [MultilingualTokenizationProcess, StopsProcess]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing PanjabiPipeline with language: {self.language}")
#         logger.info("PanjabiPipeline created.")


# class SanskritPipeline(Pipeline):
#     """Default ``Pipeline`` for Sanskrit."""

#     description: Optional[str] = "Pipeline for the Sanskrit language."
#     language: Optional[Language] = get_language("san")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             MultilingualTokenizationProcess,
#             SanskritEmbeddingsProcess,
#             StopsProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing SanskritPipeline with language: {self.language}")
#         logger.info("SanskritPipeline created.")


class SanskritChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Sanskrit."""

    description: Optional[str] = "Pipeline for the Sanskrit language"
    glottolog_id: Optional[str] = "sans1269"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SanskritSentenceSplittingProcess,
            SanskritChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing SanskritChatGPTPipeline with language: {self.language}"
        )
        logger.info("PaliPipeline created.")


class OldHighGermanChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old High German."""

    description: Optional[str] = "Pipeline for the Old High German language"
    glottolog_id: Optional[str] = "oldh1241"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            # MiddleHighGermanTokenizationProcess,  # Substitute with OldHighGermanTokenizationProcess if available
            OldHighGermanSentenceSplittingProcess,
            OldHighGermanChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing OldHighGermanChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldHighGermanChatGPTPipeline created.")


class MiddleHighGermanChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle High German."""

    description: Optional[str] = "Pipeline for the Middle High German language"
    glottolog_id: Optional[str] = "midd1343"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleHighGermanSentenceSplittingProcess,
            MiddleHighGermanChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddleHighGermanChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleHighGermanChatGPTPipeline created.")


# class HindiChatGPTPipeline(Pipeline):
#     """Default ``Pipeline`` for Hindi."""

#     description: Optional[str] = "Pipeline for the Hindi language"
#     language: Optional[Language] = get_language("hin")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             MultilingualNormalizeProcess,
#             HindiSentenceSplittingProcess,
#             HindiChatGPTProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(
#             f"Initializing HindiChatGPTPipeline with language: {self.language}"
#         )
#         logger.info("HindiChatGPTPipeline created.")


class LiteraryChineseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Literary (or Classical) Chinese."""

    description: Optional[str] = (
        "Pipeline for the Literary (or Classical) Chinese language"
    )
    glottolog_id: Optional[str] = "lite1248"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LiteraryChineseSentenceSplittingProcess,
            LiteraryChineseChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing LiteraryChineseChatGPTPipeline with language: {self.language}"
        )
        logger.info("LiteraryChineseChatGPTPipeline created.")


# class PanjabiChatGPTPipeline(Pipeline):
#     """Default ``Pipeline`` for Panjabi."""

#     description: Optional[str] = "Pipeline for the Panjabi language"
#     language: Optional[Language] = get_language("pan")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             MultilingualNormalizeProcess,
#             PanjabiSentenceSplittingProcess,
#             PunjabiChatGPTProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(
#             f"Initializing PanjabiChatGPTPipeline with language: {self.language}"
#         )
#         logger.info("PanjabiChatGPTPipeline created.")


class DemoticChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Demotic Egyptian."""

    description: Optional[str] = "Pipeline for the Demotic Egyptian language"
    glottolog_id: Optional[str] = "demo1234"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            DemoticSentenceSplittingProcess,
            DemoticChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing DemoticChatGPTPipeline with language: {self.language}"
        )
        logger.info("DemoticChatGPTPipeline created.")


class HittiteChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Hittite."""

    description: Optional[str] = "Pipeline for the Hittite language"
    glottolog_id: Optional[str] = "hit1242"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HittiteSentenceSplittingProcess,
            HittiteChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing HittiteChatGPTPipeline with language: {self.language}"
        )
        logger.info("HittiteChatGPTPipeline created.")


class TocharianAChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Tocharian A."""

    description: Optional[str] = "Pipeline for the Tocharian A language"
    glottolog_id: Optional[str] = "toch1238"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TocharianASentenceSplittingProcess,
            TokharianAChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing TocharianAChatGPTPipeline with language: {self.language}"
        )
        logger.info("TocharianAChatGPTPipeline created.")


class TocharianBChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Tocharian B."""

    description: Optional[str] = "Pipeline for the Tocharian B language"
    glottolog_id: Optional[str] = "toch1237"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TocharianBSentenceSplittingProcess,
            TokharianBChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing TocharianBChatGPTPipeline with language: {self.language}"
        )
        logger.info("TocharianBChatGPTPipeline created.")


class AvestanChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Avestan."""

    description: Optional[str] = "Pipeline for the Avestan language"
    glottolog_id: Optional[str] = "aves1237"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AvestanSentenceSplittingProcess,
            AvestanChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing AvestanChatGPTPipeline with language: {self.language}"
        )
        logger.info("AvestanChatGPTPipeline created.")


class BactrianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Bactrian."""

    description: Optional[str] = "Pipeline for the Bactrian language"
    glottolog_id: Optional[str] = "bact1239"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            BactrianSentenceSplittingProcess,
            BactrianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing BactrianChatGPTPipeline with language: {self.language}"
        )
        logger.info("BactrianChatGPTPipeline created.")


class SogdianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Sogdian."""

    description: Optional[str] = "Pipeline for the Sogdian language"
    glottolog_id: Optional[str] = "sogd1245"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            SogdianSentenceSplittingProcess,
            SogdianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing SogdianChatGPTPipeline with language: {self.language}"
        )
        logger.info("SogdianChatGPTPipeline created.")


class KhotaneseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Khotanese."""

    description: Optional[str] = "Pipeline for the Khotanese language"
    glottolog_id: Optional[str] = "khot1251"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            KhotaneseSentenceSplittingProcess,
            KhotaneseChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing KhotaneseChatGPTPipeline with language: {self.language}"
        )
        logger.info("KhotaneseChatGPTPipeline created.")


class TumshuqeseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Tumshuqese."""

    description: Optional[str] = "Pipeline for the Tumshuqese language"
    glottolog_id: Optional[str] = "tums1237"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            TumshuqeseSentenceSplittingProcess,
            TumshuqeseChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing TumshuqeseChatGPTPipeline with language: {self.language}"
        )
        logger.info("TumshuqeseChatGPTPipeline created.")


class OldPersianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Persian."""

    description: Optional[str] = "Pipeline for the Old Persian language"
    glottolog_id: Optional[str] = "oldp1254"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldPersianSentenceSplittingProcess,
            OldPersianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing OldPersianChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldPersianChatGPTPipeline created.")


class EarlyIrishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Irish."""

    description: Optional[str] = "Pipeline for the Old Irish language"
    glottolog_id: Optional[str] = "oldi1245"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            EarlyIrishSentenceSplittingProcess,
            EarlyIrishChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing OldIrishChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldIrishChatGPTPipeline created.")


class UgariticChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Ugaritic."""

    description: Optional[str] = "Pipeline for the Ugaritic language"
    glottolog_id: Optional[str] = "ugar1238"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            UgariticSentenceSplittingProcess,
            UgariticChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing UgariticChatGPTPipeline with language: {self.language}"
        )
        logger.info("UgariticChatGPTPipeline created.")


class PhoenicianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Phoenician (Punic)."""

    description: Optional[str] = "Pipeline for the Phoenician (Punic) language"
    glottolog_id: Optional[str] = "phoe1239"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PhoenicianSentenceSplittingProcess,
            PhoenicianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing PhoenicianChatGPTPipeline with language: {self.language}"
        )
        logger.info("PhoenicianChatGPTPipeline created.")


class GeezChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Geʿez (Classical Ethiopic)."""

    description: Optional[str] = "Pipeline for the Geʿez (Classical Ethiopic) language"
    glottolog_id: Optional[str] = "geez1241"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            GeezSentenceSplittingProcess,
            GeezChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing GeezChatGPTPipeline with language: {self.language}")
        logger.info("GeezChatGPTPipeline created.")


class MiddleEgyptianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Egyptian."""

    description: Optional[str] = "Pipeline for the Middle Egyptian language"
    glottolog_id: Optional[str] = "midd1369"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleEgyptianSentenceSplittingProcess,
            MiddleEgyptianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddleEgyptianChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleEgyptianChatGPTPipeline created.")


class OldEgyptianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Egyptian."""

    description: Optional[str] = "Pipeline for the Old Egyptian language"
    glottolog_id: Optional[str] = "olde1242"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldEgyptianSentenceSplittingProcess,
            OldEgyptianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing OldEgyptianChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldEgyptianChatGPTPipeline created.")


class LateEgyptianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Late Egyptian."""

    description: Optional[str] = "Pipeline for the Late Egyptian language"
    glottolog_id: Optional[str] = "late1256"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LateEgyptianSentenceSplittingProcess,
            LateEgyptianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing LateEgyptianChatGPTPipeline with language: {self.language}"
        )
        logger.info("LateEgyptianChatGPTPipeline created.")


class ParthianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Parthian."""

    description: Optional[str] = "Pipeline for the Parthian language"
    glottolog_id: Optional[str] = "part1239"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ParthianSentenceSplittingProcess,
            ParthianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing LateEgyptianChatGPTPipeline with language: {self.language}"
        )
        logger.info("LateEgyptianChatGPTPipeline created.")


class OldMiddleWelshChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Welsh."""

    description: Optional[str] = "Pipeline for the Middle Welsh language"
    glottolog_id: Optional[str] = "oldw1239"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldMiddleWelshSentenceSplittingProcess,
            OldMiddleWelshChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddleWelshChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleWelshChatGPTPipeline created.")


class MiddleBretonChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Breton."""

    description: Optional[str] = "Pipeline for the Middle Breton language"
    glottolog_id: Optional[str] = "oldb1244"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleBretonSentenceSplittingProcess,
            MiddleBretonChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddleBretonChatGPTPipeline with language: {self.language}"
        )
        logger.info("MiddleBretonChatGPTPipeline created.")


class CornishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Cornish."""

    description: Optional[str] = "Pipeline for the Cornish language"
    glottolog_id: Optional[str] = "corn1251"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleCornishSentenceSplittingProcess,
            MiddleCornishChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing CornishChatGPTPipeline with language: {self.language}"
        )
        logger.info("CornishChatGPTPipeline created.")


class OldPrussianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Prussian."""

    description: Optional[str] = "Pipeline for the Old Prussian language"
    glottolog_id: Optional[str] = "prus1238"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldPrussianSentenceSplittingProcess,
            OldPrussianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing OldPrussianChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldPrussianChatGPTPipeline created.")


class LithuanianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Lithuanian."""

    description: Optional[str] = "Pipeline for the Lithuanian language"
    glottolog_id: Optional[str] = "lith1251"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LithuanianSentenceSplittingProcess,
            LithuanianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing LithuanianChatGPTPipeline with language: {self.language}"
        )
        logger.info("LithuanianChatGPTPipeline created.")


class LatvianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Latvian."""

    description: Optional[str] = "Pipeline for the Latvian language"
    glottolog_id: Optional[str] = "latv1249"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LatvianSentenceSplittingProcess,
            LatvianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing LatvianChatGPTPipeline with language: {self.language}"
        )
        logger.info("LatvianChatGPTPipeline created.")


class AlbanianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Albanian."""

    description: Optional[str] = "Pipeline for the Albanian language"
    glottolog_id: Optional[str] = "gheg1238"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AlbanianSentenceSplittingProcess,
            AlbanianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing AlbanianChatGPTPipeline with language: {self.language}"
        )
        logger.info("AlbanianChatGPTPipeline created.")


class ClassicalArmenianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Classical Armenian."""

    description: Optional[str] = "Pipeline for the Classical Armenian language"
    glottolog_id: Optional[str] = "clas1256"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            ClassicalArmenianSentenceSplittingProcess,
            ClassicalArmenianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing ClassicalArmenianChatGPTPipeline with language: {self.language}"
        )
        logger.info("ClassicalArmenianChatGPTPipeline created.")


class MiddleArmenianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle Armenian."""

    description: Optional[str] = "Pipeline for the Middle Armenian language"
    glottolog_id: Optional[str] = "midd1364"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            MiddleArmenianSentenceSplittingProcess,
            MiddleArmenianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddleArmenianChatGPTPipeline with language: {self.language}"
        )


MAP_LANGUAGE_CODE_TO_DISCRIMINATIVE_PIPELINE: dict[str, Type[Pipeline]] = {
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


MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE: dict[str, Type[Pipeline]] = {
    # Indo-European family
    ## Italic
    "lati1261": LatinChatGPTPipeline,
    "oldf1239": OldFrenchChatGPTPipeline,
    "midd1316": MiddleFrenchChatGPTPipeline,
    # Other Romance languages
    ## Hellenic
    "anci1242": GreekChatGPTPipeline,
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
    "hit1242": HittiteChatGPTPipeline,
    # Luwian (cuneiform and hieroglyphic inscriptions, 14th–8th c. BCE).
    # Lycian (inscriptions, 6th–4th c. BCE).
    # Lydian (inscriptions, 7th–4th c. BCE).
    # Palaic (inscriptions, 2nd–1st c. BCE).
    # Carian (inscriptions, 6th–4th c. BCE).
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
    # Vedic Sanskrit (c. 1500–500 BCE) "vedi1234"
    # Classical Sanskrit (from ~500 BCE) "clas1258"
    "sans1269": SanskritChatGPTPipeline,
    # Prakrits (Middle Indo-Aryan, ca. 500 BCE–500 CE)
    "pali1273": PaliChatGPTPipeline,
    # Ardhamāgadhī, Śaurasenī, Mahārāṣṭrī, etc. — languages of Jain/Buddhist texts and early drama.
    # ? Glotto says alt_name for Pali; Ardhamāgadhī, literary language associated with Magadha (eastern India); Jain canonical texts (the Āgamas) are written primarily in Ardhamāgadhī
    # "saur1252": "Sauraseni Prakrit"; Śaurasenī, Linked to Śūrasena (region around Mathurā, central north India).
    # "maha1305": "Maharastri Prakrit"; Mahārāṣṭrī, Western Deccan (Maharashtra). Lyric and epic poetry, gatha
    # "maga1260": "Magadhi Prakrit"; Māgadhī, Magadha (Bihar). Buddhist texts (especially in eastern India).
    # "Gandhari": "gand1259"; Gāndhārī, Inscriptions and Buddhist texts. Kharoṣṭhī script
    ## Middle Indo-Aryan
    # "Maithili": "mait1250"; Apabhraṃśa; "Apabhramsa" is alt_name; (500–1200 CE); Bridges Prakrits → New Indo-Aryan
    ## New Indo-Aryan
    ## Medieval languages (~1200 CE onward):
    # Early forms of Hindi, Bengali, Gujarati, Marathi, Punjabi, Oriya, Sinhala, etc
    # North-Western / Hindi Belt
    # "hind1269": "Hindi"; "Old Hindi" is alt_name: ~10th–14th century CE.
    # "hind1269": "Hindi"; Khari Boli is alt name: In the medieval period (before 1700), Khari Boli itself was not a prestigious literary dialect; Braj and Awadhi dominated literary use.; becomes the basis of Standard Hindi and Standard Urdu
    # "braj1242": "Braj" Braj Bhāṣā: Braj area around Mathura, Agra, western Uttar Pradesh, parts of Rajasthan; Flourished 15th–18th centuries as a major literary dialect; language of Krishna bhakti poetry
    # "awad1243": "Awadhi" Awadhi: Awadh region of eastern Uttar Pradesh; Active literary language from 14th century onward; Rāmāyaṇa tradition, Sufi poetry
    # "urdu1245": "Urdu" Urdu: 13th–14th c.: In Delhi Sultanate, Sufi poets (e.g. Amīr Khusro, d. 1325) composed in Hindavī, blending Khari Boli vernacular with Persian/Arabic elements.
    ### Eastern Indo-Aryan
    # "beng1280": "Bengali" Bengali (Bangla): Descends from Magadhi Apabhraṃśa; Caryāpadas (Buddhist, c. 10th–12th c.); Chaitanya, a vast Vaishnava devotional literature
    # "oriy1255": "Odia"; Oriya (Odia): diverging from Bengali/Assamese around 10th–11th c.; Sarala Dāsa (15th c.): Mahābhārata in Odia, Chandī Purāṇa, Vilanka Rāmāyaṇa, and other medieval epics
    # "assa1263": "Assamese" Assamese: the same eastern Apabhraṃśa ancestor as Bengali and Odia; distinct by 12th–13th c.; Śaṅkaradeva (15th–16th c.): central figure, created Vaishnava plays (Ankiyā Nāt), poetry, translations of epics
    ### Western Indo-Aryan
    # "guja1252": "Gujarati" Gujarati: from western Apabhraṃśa by the 12th c.; Jain religious poetry (12th–14th c.).
    # "mara1378": "Marathi" Marathi: Western Apabhraṃśa → Old Marathi attested from 11th–13th c. inscriptions.; Earliest texts: Jñāneśvarī (1275 CE) by Jñāneśvar — Marathi commentary on the Bhagavad Gītā.
    # !? Glottolog calls Rajashani an alternative name for Bagri; investigate "bagr1243": "Bagri"; "Rajasthani" Rajasthani: Old Western Rajasthani (often overlapping with Old Gujarati/Apabhraṃśa). Jain texts in Dingal/Pingal dialects, heroic poetry (12th–13th c.).
    ### Southern Indo-Aryan
    # "sinh1246": "Sinhala" Sinhala (Sinhalese); Earliest texts: Elu Sandēsa poems (13th c.), chronicles (Cūḷavaṃsa continues through medieval period).
    ### North-Western Frontier
    # "panj1256": "Eastern Panjabi" Punjabi: in its Old forms; Baba Farid’s vārs (12th–13th c.)
    # "sind1272": "Sindhi" Sindhi: Northwestern WIA dialect continuum; Sufi poetry from the 14th c.
    # "kash1277": "Kashmiri" Kashmiri: Early poetry of Lal Dēd (14th c.) and Habba Khatoon (16th c.).
    # Afroasiatic family
    ## Semitic languages
    ### East Semitic
    "akka1240": AkkadianChatGPTPipeline,
    # Eblaite
    ### West Semitic
    "ugar1238": UgariticChatGPTPipeline,
    "phoe1239": PhoenicianChatGPTPipeline,
    # Biblical Hebrew
    "anci1244": BiblicalHebrewChatGPTPipeline,
    # Medieval Hebrew
    # Moabite, Ammonite, Edomite
    # Old Aramaic (ca. 1000–700 BCE, inscriptions).
    # Imperial Aramaic (ca. 700–300 BCE), lingua franca of Assyrian, Babylonian, Persian empires.
    "impe1235": ImperialAramaicChatGPTPipeline,
    # Middle Aramaic (200 BCE – 700 CE), includes Biblical Aramaic, Palmyrene, Nabataean, Targumic Aramaic.
    # Syriac (2nd c. CE → medieval period): huge Christian corpus (Bible, hymns, philosophy).
    "clas1252": ClassicalSyriacChatGPTPipeline,
    # Jewish Babylonian Aramaic: Talmud, liturgy.
    # Mandaic: liturgy of the Mandaeans.
    ### NW Semitic
    # Samʾalian (Zincirli) — 1st mill. BCE; NW Semitic variety with its own inscriptional corpus.
    ## South Semitic
    # Old South Arabian (OSA)
    # Geʿez (Classical Ethiopic)
    "geez1241": GeezChatGPTPipeline,
    ### Central Semitic (bridge between NW and South)
    # Pre-Islamic Arabic
    # Classical Arabic (7th c. CE onward): Qurʾān, poetry, early Islamic literature.
    "clas1259": ClassicalArabicChatGPTPipeline,  # Dialect
    # Glotto doesn't have medieval arabic; Medieval Arabic: scientific, philosophical, historical works dominate much of the Islamic Golden Age corpus.
    ## Egyptian languages
    "olde1242": OldEgyptianChatGPTPipeline,
    "midd1369": MiddleEgyptianChatGPTPipeline,
    "late1256": LateEgyptianChatGPTPipeline,
    "demo1234": DemoticChatGPTPipeline,
    "copt1239": CopticChatGPTPipeline,
    ## Berber
    # "numi1241": "Numidian"; "Ancient Berber" and "Lybico-Berber" are alt names; Libyco-Berber inscriptions (1st mill. BCE).
    ## "tait1247": "Cushitic Taita" ; Cushitic
    # earliest written records only medieval, often in Geʿez script or Arabic script (e.g. Beja glosses in Arabic works)
    ## Chadic
    # ; "haus1257": "Hausa"; Hausa; Essentially oral until medieval period, when Hausa is written in Ajami (Arabic script).
    "lite1248": LiteraryChineseChatGPTPipeline,
    "clas1254": ClassicalTibetanPipeline,
    # Sino-Tibetan family
    # Sino-Tibetan (Pre-1800 Attested)
    # | Language / Register                     | Period              | Glottocode    |
    # |----------------------------------------|---------------------|---------------|
    # | **Old Chinese**                         | ca. 1200 BCE – 200 CE | `oldc1244`    |
    # | **Middle Chinese**                      | ca. 3rd – 10th c. CE | `midd1344`    |
    # | **Classical Chinese (Literary Chinese)**| ca. 5th c. BCE – 19th c. | `lite1248` |
    # | **Early Vernacular Chinese (Baihua)**   | ca. 10th – 18th c. CE | *(under `clas1255`)* |
    # | **Old Tibetan**                         | 7th – 10th c. CE     | *(not separately coded)* |
    # | **Classical Tibetan**                   | from 7th c. onward   | `clas1254`    |
    # | **Old Burmese**                         | 11th – 16th c. CE    | `oldb1235`    |
    # | **Classical Burmese**                   | 16th – 18th c. CE    | `nucl1310`    |
    # | **Tangut**                              | 11th – 13th c. CE    | `tang1334`    |
    # | **Newar (Classical Nepal Bhasa)**       | 12th – 18th c. CE    | `newa1246`    |
    # | **Meitei (Classical Manipuri)**         | 15th – 18th c. CE    | `mani1292` |
    # | **Early Sgaw Karen**                    | 18th c. CE           | `sgaw1245` |
    # Mongolic family
    # Mongolic (Pre-1800 Attested)
    # | Language / Period                | Approx. Dates        | Glottocode      |
    # |----------------------------------|----------------------|-----------------|
    # | Middle Mongol                    | 13th–16th centuries  | `mong1329`      |
    # | Classical Mongolian              | ca. 1700–1900        | `mong1331`      |
    # | Mogholi (Moghol language)        | ca. 13th–17th c.     | `mogh1245`      |
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
    # | Altaic-Adj.    | Old Jurchen                 | 12th–13th c. CE      | *(not coded)*  |
    # |                | Manchu                      | 17th–18th c. CE      | *(not coded)*  |
    # | Austroasiatic  | Old Mon                     | from 6th c. CE       | *(not coded)*  |
    # |                | Old Khmer                   | from 7th c. CE       | *(not coded)*  |
    # | Austronesian   | Old Javanese (Kawi)         | from 8th c. CE       | *(not coded)*  |
    # |                | Classical Malay             | from 7th c. CE onward| *(not coded)*  |
    # | Tai–Kadai      | Old Thai                    | from 13th c. CE      | *(not coded)*  |
}
