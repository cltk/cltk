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
    AncientGreekChatGPTProcess,
    AvestanChatGPTProcess,
    BiblicalHebrewChatGPTProcess,
    ChurchSlavicChatGPTProcess,
    ClassicalArabicChatGPTProcess,
    ClassicalSyriacChatGPTProcess,
    CopticChatGPTProcess,
    DemoticChatGPTProcess,
    GothicChatGPTProcess,
    HindiChatGPTProcess,
    HittiteChatGPTProcess,
    LatinChatGPTProcess,
    LiteraryChineseChatGPTProcess,
    MiddleEnglishChatGPTProcess,
    MiddleFrenchChatGPTProcess,
    MiddleHighGermanChatGPTProcess,
    OfficialAramaicChatGPTProcess,
    OldEnglishChatGPTProcess,
    OldFrenchChatGPTProcess,
    OldHighGermanChatGPTProcess,
    OldIrishChatGPTProcess,
    OldNorseChatGPTProcess,
    OldPersianChatGPTProcess,
    PaliChatGPTProcess,
    PunjabiChatGPTProcess,
    SanskritChatGPTProcess,
    TokharianAChatGPTProcess,
    TokharianBChatGPTProcess,
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
    AncientGreekSentenceSplittingProcess,
    AncientHebrewSentenceSplittingProcess,
    AvestanSentenceSplittingProcess,
    ChurchSlavonicSentenceSplittingProcess,
    ClassicalArabicSentenceSplittingProcess,
    ClassicalSyriacSentenceSplittingProcess,
    CopticSentenceSplittingProcess,
    DemoticSentenceSplittingProcess,
    GothicSentenceSplittingProcess,
    HindiSentenceSplittingProcess,
    HittiteSentenceSplittingProcess,
    LatinSentenceSplittingProcess,
    LiteraryChineseSentenceSplittingProcess,
    MiddleEnglishSentenceSplittingProcess,
    MiddleFrenchSentenceSplittingProcess,
    MiddleHighGermanSentenceSplittingProcess,
    OfficialAramaicSentenceSplittingProcess,
    OldEnglishSentenceSplittingProcess,
    OldFrenchSentenceSplittingProcess,
    OldHighGermanSentenceSplittingProcess,
    OldIrishSentenceSplittingProcess,
    OldNorseSentenceSplittingProcess,
    OldPersianSentenceSplittingProcess,
    PaliSentenceSplittingProcess,
    PanjabiSentenceSplittingProcess,
    SanskritSentenceSplittingProcess,
    TocharianASentenceSplittingProcess,
    TocharianBSentenceSplittingProcess,
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


# class GothicChatGPTPipeline(Pipeline):
#     """Default ``Pipeline`` for Gothic."""

#     description: Optional[str] = "Pipeline for the Gothic language"
#     glottolog_id: str = "oldh1241"
#     language: Optional[Language] = get_language("oldh1241")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             MultilingualNormalizeProcess,
#             GothicSentenceSplittingProcess,
#             GothicChatGPTProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(
#             f"Initializing GothicChatGPTPipeline with language: {self.language}"
#         )
#         logger.info("GothicChatGPTPipeline created.")


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


# TODO: Re-enable once Pali is added to the Glottolog export
# class PaliChatGPTPipeline(Pipeline):
#     """Default ``Pipeline`` for Pali."""

#     description: Optional[str] = "Pipeline for the Pali language"
#     language: Optional[Language] = get_language("pli")
#     processes: Optional[list[Type[Process]]] = Field(
#         default_factory=lambda: [
#             MultilingualNormalizeProcess,
#             PaliSentenceSplittingProcess,
#             PaliChatGPTProcess,
#         ]
#     )

#     def __post_init__(self):
#         logger.debug(f"Initializing PaliPipeline with language: {self.language}")
#         logger.info("PaliPipeline created.")


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


class OldPersianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Persian."""

    description: Optional[str] = "Pipeline for the Old Persian language"
    glottolog_id: Optional[str] = "oldp1245"
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


class OldIrishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Irish."""

    description: Optional[str] = "Pipeline for the Old Irish language"
    glottolog_id: Optional[str] = "oldi1245"
    processes: Optional[list[Type[Process]]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldIrishSentenceSplittingProcess,
            OldIrishChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing OldIrishChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldIrishChatGPTPipeline created.")


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

# Indo-European
# Hittite (hit1242) — earliest attested Indo-European language; lots of tablets, strong scholarly interest.
# Tocharian A/B (toch1238, toch1237) — Buddhist texts from the Tarim Basin, unique branch of Indo-European.
# Avestan (aves1237) — sacred Zoroastrian language; close to Old Persian, key for Iranian studies.
# Old Persian (oldp1245) — royal inscriptions, relatively small corpus but important historically.
# Gothic (goth1244) — earliest attested Germanic, crucial for comparative studies.
# Old Irish (oldi1245) — earliest Celtic with substantial corpus, highly inflected.

# Semitic
# Ugaritic (ugar1238) — Northwest Semitic, alphabetic cuneiform corpus, very important for biblical studies.
# Phoenician / Punic (phoe1238) — inscriptions across the Mediterranean, huge for comparative Semitics.
# Geʿez (Classical Ethiopic) (geez1241) — major liturgical language of the Horn of Africa, continuous tradition.
# Egyptian & Related
# Middle Egyptian (midd1330) — the “classical” stage of Egyptian, most of the literary corpus.
# Old Egyptian (olde1246) — Pyramid Texts, earliest stage.
# Late Egyptian (late1246) — administrative/literary texts, Amarna period onward.
# (Demotic and Coptic you already have.)

# East & South Asia
# Pali (pali1273) — canonical Buddhist Prakrit, still central in Buddhist studies.
# Prakrits (esp. Ardhamāgadhī, Māhārāṣṭrī) — Jain and early drama texts.
# Classical Japanese (Bungo) (clas1255) — Heian and medieval prose/poetry, essential for East Asian NLP.
# Classical Tibetan (clas1249) — canonical Buddhist translations, large corpus, lots of digital projects.

MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE: dict[str, Type[Pipeline]] = {
    # TODO: Pali missing from JSON entirely
    # # "pli": PaliChatGPTPipeline,
    # TODO: Re-enable, Gothic the JSON incorrectly puts Gothic as another name for Old High German (oldh1241)
    # "got": GothicChatGPTPipeline,
    "akka1240": AkkadianChatGPTPipeline,
    "olde1238": OldEnglishChatGPTPipeline,
    "impe1235": ImperialAramaicChatGPTPipeline,
    "copt1239": CopticChatGPTPipeline,
    "anci1242": GreekChatGPTPipeline,
    "anci1244": BiblicalHebrewChatGPTPipeline,
    "lati1261": LatinChatGPTPipeline,
    "oldn1244": OldNorseChatGPTPipeline,
    "sans1269": SanskritChatGPTPipeline,
    "clas1259": ClassicalArabicChatGPTPipeline,
    "chur1257": ChurchSlavonicChatGPTPipeline,
    "midd1317": MiddleEnglishChatGPTPipeline,
    "midd1316": MiddleFrenchChatGPTPipeline,
    "oldf1239": OldFrenchChatGPTPipeline,
    "midd1343": MiddleHighGermanChatGPTPipeline,
    "oldh1241": OldHighGermanChatGPTPipeline,
    "demo1234": DemoticChatGPTPipeline,
    "lite1248": LiteraryChineseChatGPTPipeline,
    "clas1252": ClassicalSyriacChatGPTPipeline,
    "hit1242": HittiteChatGPTPipeline,
    "toch1238": TocharianAChatGPTPipeline,
    "toch1237": TocharianBChatGPTPipeline,
    "aves1237": AvestanChatGPTPipeline,
    "oldp1245": OldPersianChatGPTPipeline,
    "oldi1245": OldIrishChatGPTPipeline,
}
