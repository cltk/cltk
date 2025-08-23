"""Default processing pipelines for languages. The purpose of
these dataclasses is to represent:

1. the types of NLP processes that the CLTK can do
2. the order in which processes are to be executed
3. specifying what downstream features a particular implemented process requires
"""

from dataclasses import dataclass, field
from typing import Optional, Type

from cltk.alphabet.processes import (
    AncientGreekNormalizeProcess,
    LatinNormalizeProcess,
    MultilingualNormalizeProcess,
)
from cltk.core.cltk_logger import logger
from cltk.core.data_types_v2 import Language, Pipeline, Process
from cltk.dependency.processes import (
    ChineseStanzaProcess,
    CopticStanzaProcess,
    GothicStanzaProcess,
    GreekSpacyProcess,
    GreekStanzaProcess,
    LatinSpacyProcess,
    LatinStanzaProcess,
    OCSStanzaProcess,
    OldFrenchStanzaProcess,
)
from cltk.embeddings.processes import (
    ArabicEmbeddingsProcess,
    AramaicEmbeddingsProcess,
    GothicEmbeddingsProcess,
    GreekEmbeddingsProcess,
    LatinEmbeddingsProcess,
    MiddleEnglishEmbeddingsProcess,
    OldEnglishEmbeddingsProcess,
    PaliEmbeddingsProcess,
    SanskritEmbeddingsProcess,
)
from cltk.genai.processes import (
    AkkadianChatGPTProcess,
    AncientGreekChatGPTProcess,
    AncientHebrewChatGPTProcess,
    ChurchSlavicChatGPTProcess,
    ClassicalArabicChatGPTProcess,
    CopticChatGPTProcess,
    DemoticChatGPTProcess,
    GothicChatGPTProcess,
    HindiChatGPTProcess,
    LatinChatGPTProcess,
    LiteraryChineseChatGPTProcess,
    MiddleEnglishChatGPTProcess,
    MiddleFrenchChatGPTProcess,
    MiddleHighGermanChatGPTProcess,
    OfficialAramaicChatGPTProcess,
    OldEnglishChatGPTProcess,
    OldFrenchChatGPTProcess,
    OldHighGermanChatGPTProcess,
    OldNorseChatGPTProcess,
    PaliChatGPTProcess,
    PunjabiChatGPTProcess,
    SanskritChatGPTProcess,
)
from cltk.languages.utils import get_lang
from cltk.lemmatize.processes import (
    GreekLemmatizationProcess,
    LatinLemmatizationProcess,
    OldEnglishLemmatizationProcess,
    OldFrenchLemmatizationProcess,
)
from cltk.lexicon.processes import LatinLexiconProcess, OldNorseLexiconProcess
from cltk.ner.processes import (  # GreekNERProcess,; LatinNERProcess,; OldEnglishNERProcess,
    OldFrenchNERProcess,
)
from cltk.sentence.processes import (
    AkkadianSentenceSplittingProcess,
    AncientGreekSentenceSplittingProcess,
    AncientHebrewSentenceSplittingProcess,
    ChurchSlavonicSentenceSplittingProcess,
    ClassicalArabicSentenceSplittingProcess,
    CopticSentenceSplittingProcess,
    DemoticSentenceSplittingProcess,
    GothicSentenceSplittingProcess,
    HindiSentenceSplittingProcess,
    LatinSentenceSplittingProcess,
    LiteraryChineseSentenceSplittingProcess,
    MiddleEnglishSentenceSplittingProcess,
    MiddleFrenchSentenceSplittingProcess,
    MiddleHighGermanSentenceSplittingProcess,
    OfficialAramaicSentenceSplittingProcess,
    OldEnglishSentenceSplittingProcess,
    OldFrenchSentenceSplittingProcess,
    OldHighGermanSentenceSplittingProcess,
    OldNorseSentenceSplittingProcess,
    PaliSentenceSplittingProcess,
    PanjabiSentenceSplittingProcess,
    SanskritSentenceSplittingProcess,
)
from cltk.stops.processes import StopsProcess
from cltk.tokenizers.processes import (
    AkkadianTokenizationProcess,
    ArabicTokenizationProcess,
    GreekTokenizationProcess,
    LatinTokenizationProcess,
    MiddleEnglishTokenizationProcess,
    MiddleFrenchTokenizationProcess,
    MiddleHighGermanTokenizationProcess,
    MultilingualTokenizationProcess,
    OldFrenchTokenizationProcess,
    OldNorseTokenizationProcess,
)


class AkkadianPipeline(Pipeline):
    """Default ``Pipeline`` for Akkadian."""

    description: Optional[str] = "Pipeline for the Akkadian language."
    language: Optional[Language] = get_lang("akk")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [AkkadianTokenizationProcess, StopsProcess]
    )

    def __post_init__(self):
        logger.debug(f"Initializing AkkadianPipeline with language: {self.language}")
        logger.info("AkkadianPipeline created.")


class AkkadianChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Akkadian."""

    description: Optional[str] = "Pipeline for the Akkadian language"
    language: Optional[Language] = get_lang("akk")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AkkadianSentenceSplittingProcess,
            AkkadianChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing AkkadianChatGPTPipeline with language: {self.language}"
        )
        logger.info("AkkadianChatGPTPipeline created.")


class ArabicPipeline(Pipeline):
    """Default ``Pipeline`` for Arabic."""

    description: Optional[str] = "Pipeline for the Arabic language"
    language: Optional[Language] = get_lang("arb-cla")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            ArabicTokenizationProcess,
            ArabicEmbeddingsProcess,
            StopsProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing ArabicPipeline with language: {self.language}")
        logger.info("ArabicPipeline created.")


class ClassicalArabicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Arabic."""

    description: Optional[str] = "Pipeline for the Arabic language"
    language: Optional[Language] = get_lang("arb-cla")
    processes: Optional[list[Type[Process]]] = field(
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


class AramaicPipeline(Pipeline):
    """Default ``Pipeline`` for Aramaic."""

    description: Optional[str] = "Pipeline for the Aramaic language"
    language: Optional[Language] = get_lang("arc")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            ArabicTokenizationProcess,  # Note: Using Arabic tokenizer for Aramaic. Is this OK?
            AramaicEmbeddingsProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing AramaicPipeline with language: {self.language}")
        logger.info("AramaicPipeline created.")
        logger.warning("Using Arabic tokenizer for Aramaic. Is this OK?")


class ChinesePipeline(Pipeline):
    """Default ``Pipeline`` for Classical Chinese."""

    description: Optional[str] = "Pipeline for the Classical Chinese language"
    language: Optional[Language] = get_lang("lzh")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [ChineseStanzaProcess]
    )

    def __post_init__(self):
        logger.debug(f"Initializing ChinesePipeline with language: {self.language}")
        logger.info("ChinesePipeline created.")


class CopticPipeline(Pipeline):
    """Default ``Pipeline`` for Coptic."""

    description: Optional[str] = "Pipeline for the Coptic language"
    language: Optional[Language] = get_lang("cop")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [CopticStanzaProcess, StopsProcess]
    )

    def __post_init__(self):
        logger.debug(f"Initializing CopticPipeline with language: {self.language}")
        logger.info("CopticPipeline created.")


class CopticChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Coptic."""

    description: Optional[str] = "ChatGPT Pipeline for the Coptic language."
    language: Optional[Language] = get_lang("cop")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            CopticSentenceSplittingProcess,
            CopticChatGPTProcess,
        ]
    )


class GothicPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic."""

    description: Optional[str] = "Pipeline for the Gothic language"
    language: Optional[Language] = get_lang("got")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [GothicStanzaProcess, GothicEmbeddingsProcess]
    )

    def __post_init__(self):
        logger.debug(f"Initializing GothicPipeline with language: {self.language}")
        logger.info("GothicPipeline created.")


class GothicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic."""

    description: Optional[str] = "Pipeline for the Gothic language"
    language: Optional[Language] = get_lang("got")
    processes: Optional[list[Type[Process]]] = field(
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


class GreekPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Greek."""

    description: Optional[str] = "Pipeline for the Greek language"
    language: Optional[Language] = get_lang("grc")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            AncientGreekNormalizeProcess,
            GreekSpacyProcess,
            GreekEmbeddingsProcess,
            StopsProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing GreekPipeline with language: {self.language}")
        logger.info("GreekPipeline created.")


class GreekChatGPTPipeline(Pipeline):
    """Pipeline for Ancient Greek using normalization and ChatGPT annotation only."""

    description: Optional[str] = "Pipeline for Ancient Greek with ChatGPT annotation"
    language: Optional[Language] = get_lang("grc")
    processes: Optional[list[Type[Process]]] = field(
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


class HindiPipeline(Pipeline):
    """Default ``Pipeline`` for Hindi."""

    description: Optional[str] = "Pipeline for the Hindi language."
    language: Optional[Language] = get_lang("hin")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [MultilingualTokenizationProcess, StopsProcess]
    )

    def __post_init__(self):
        logger.debug(f"Initializing HindiPipeline with language: {self.language}")
        logger.info("HindiPipeline created.")


class AncientHebrewChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Hebrew."""

    description: Optional[str] = "Pipeline for the Ancient Hebrew language."
    language: Optional[Language] = get_lang("hbo")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            AncientHebrewSentenceSplittingProcess,
            AncientHebrewChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing LatinPipeline with language: {self.language}")
        logger.info("LatinPipeline created.")


class LatinPipeline(Pipeline):
    """Default ``Pipeline`` for Latin."""

    description: Optional[str] = "Pipeline for the Latin language."
    language: Optional[Language] = get_lang("lat")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            LatinNormalizeProcess,
            LatinStanzaProcess,
            LatinEmbeddingsProcess,
            StopsProcess,
            LatinLexiconProcess,
        ]
    )


class LatinChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Latin."""

    description: Optional[str] = "ChatGPT Pipeline for the Latin language."
    language: Optional[Language] = get_lang("lat")
    processes: Optional[list[Type[Process]]] = field(
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


class MiddleHighGermanPipeline(Pipeline):
    """Default ``Pipeline`` for Middle High German."""

    description: Optional[str] = "Pipeline for the Middle High German language."
    language: Optional[Language] = get_lang("gmh")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [MiddleHighGermanTokenizationProcess, StopsProcess]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddleHighGermanPipeline with language: {self.language}"
        )
        logger.info("MiddleHighGermanPipeline created.")


class MiddleEnglishPipeline(Pipeline):
    """Default ``Pipeline`` for Middle English."""

    description: Optional[str] = "Pipeline for the Middle English language"
    language: Optional[Language] = get_lang("enm")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MiddleEnglishTokenizationProcess,
            StopsProcess,
            MiddleEnglishEmbeddingsProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddleEnglishPipeline with language: {self.language}"
        )
        logger.info("MiddleEnglishPipeline created.")


class MiddleEnglishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle English."""

    description: Optional[str] = "Pipeline for the Middle English language"
    language: Optional[Language] = get_lang("enm")
    processes: Optional[list[Type[Process]]] = field(
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


class MiddleFrenchPipeline(Pipeline):
    """Default ``Pipeline`` for Middle French."""

    description: Optional[str] = "Pipeline for the Middle French language"
    language: Optional[Language] = get_lang("frm")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [MiddleFrenchTokenizationProcess]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing MiddleFrenchPipeline with language: {self.language}"
        )
        logger.info("MiddleFrenchPipeline created.")


class MiddleFrenchChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Middle French."""

    description: Optional[str] = "Pipeline for the Middle French language"
    language: Optional[Language] = get_lang("frm")
    processes: Optional[list[Type[Process]]] = field(
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


class OCSPipeline(Pipeline):
    """Default ``Pipeline`` for Old Church Slavonic."""

    description: Optional[str] = "Pipeline for the Old Church Slavonic language"
    language: Optional[Language] = get_lang("chu")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [OCSStanzaProcess]
    )

    def __post_init__(self):
        logger.debug(f"Initializing OCSPipeline with language: {self.language}")
        logger.info("OCSPipeline created.")


class OfficialAramaicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Official Aramaic."""

    description: Optional[str] = "ChatGPT Pipeline for the Official Aramaic language."
    language: Optional[Language] = get_lang("arc")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OfficialAramaicSentenceSplittingProcess,
            OfficialAramaicChatGPTProcess,
        ]
    )


class ChurchSlavonicChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for (Old) Church Slavonic."""

    description: Optional[str] = "Pipeline for the Church Slavonic language"
    language: Optional[Language] = get_lang("chu")
    processes: Optional[list[Type[Process]]] = field(
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


class OldEnglishPipeline(Pipeline):
    """Default ``Pipeline`` for Old English."""

    description: Optional[str] = "Pipeline for the Old English language"
    language: Optional[Language] = get_lang("ang")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualTokenizationProcess,
            OldEnglishLemmatizationProcess,
            OldEnglishEmbeddingsProcess,
            StopsProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing OldEnglishPipeline with language: {self.language}")
        logger.info("OldEnglishPipeline created.")


class OldEnglishChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old English."""

    description: Optional[str] = "Pipeline for the Old English language"
    language: Optional[Language] = get_lang("ang")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            OldEnglishSentenceSplittingProcess,
            OldEnglishChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing OldEnglishChatGPTPipeline with language: {self.language}"
        )
        logger.info("OldEnglishChatGPTPipeline created.")


class OldFrenchPipeline(Pipeline):
    """Default ``Pipeline`` for Old French."""

    description: Optional[str] = "Pipeline for the Old French language"
    language: Optional[Language] = get_lang("fro")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            OldFrenchStanzaProcess,
            StopsProcess,
            OldFrenchNERProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing OldFrenchPipeline with language: {self.language}")
        logger.info("OldFrenchPipeline created.")


class OldFrenchChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old French."""

    description: Optional[str] = "Pipeline for the Old French language"
    language: Optional[Language] = get_lang("fro")
    processes: Optional[list[Type[Process]]] = field(
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


# TODO: Add Old Marathi ("omr")
# logger.critical("Old Marathi pipeline is not yet implemented.")


class OldNorsePipeline(Pipeline):
    """Default ``Pipeline`` for Old Norse."""

    description: Optional[str] = "Pipeline for the Old Norse language"
    language: Optional[Language] = get_lang("non")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            OldNorseTokenizationProcess,
            StopsProcess,
            OldNorseLexiconProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing OldNorsePipeline with language: {self.language}")
        logger.info("OldNorsePipeline created.")


class OldNorseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Old Norse."""

    description: Optional[str] = "Pipeline for the Old Norse language"
    language: Optional[Language] = get_lang("non")
    processes: Optional[list[Type[Process]]] = field(
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


class PaliPipeline(Pipeline):
    """Default ``Pipeline`` for Pali."""

    description: Optional[str] = "Pipeline for the Pali language"
    language: Optional[Language] = get_lang("pli")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [MultilingualTokenizationProcess, PaliEmbeddingsProcess]
    )

    def __post_init__(self):
        logger.debug(f"Initializing PaliPipeline with language: {self.language}")
        logger.info("PaliPipeline created.")


class PaliChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Pali."""

    description: Optional[str] = "Pipeline for the Pali language"
    language: Optional[Language] = get_lang("pli")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PaliSentenceSplittingProcess,
            PaliChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing PaliPipeline with language: {self.language}")
        logger.info("PaliPipeline created.")


class PanjabiPipeline(Pipeline):
    """Default ``Pipeline`` for Panjabi."""

    description: Optional[str] = "Pipeline for the Panjabi language."
    language: Optional[Language] = get_lang("pan")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [MultilingualTokenizationProcess, StopsProcess]
    )

    def __post_init__(self):
        logger.debug(f"Initializing PanjabiPipeline with language: {self.language}")
        logger.info("PanjabiPipeline created.")


class SanskritPipeline(Pipeline):
    """Default ``Pipeline`` for Sanskrit."""

    description: Optional[str] = "Pipeline for the Sanskrit language."
    language: Optional[Language] = get_lang("san")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualTokenizationProcess,
            SanskritEmbeddingsProcess,
            StopsProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(f"Initializing SanskritPipeline with language: {self.language}")
        logger.info("SanskritPipeline created.")


class SanskritChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Sanskrit."""

    description: Optional[str] = "Pipeline for the Sanskrit language"
    language: Optional[Language] = get_lang("san")
    processes: Optional[list[Type[Process]]] = field(
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
    language: Optional[Language] = get_lang("goh")
    processes: Optional[list[Type[Process]]] = field(
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
    language: Optional[Language] = get_lang("gmh")
    processes: Optional[list[Type[Process]]] = field(
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


class HindiChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Hindi."""

    description: Optional[str] = "Pipeline for the Hindi language"
    language: Optional[Language] = get_lang("hin")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            HindiSentenceSplittingProcess,
            HindiChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing HindiChatGPTPipeline with language: {self.language}"
        )
        logger.info("HindiChatGPTPipeline created.")


class LiteraryChineseChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Literary (or Classical) Chinese."""

    description: Optional[str] = (
        "Pipeline for the Literary (or Classical) Chinese language"
    )
    language: Optional[Language] = get_lang("lzh")
    processes: Optional[list[Type[Process]]] = field(
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


class PanjabiChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Panjabi."""

    description: Optional[str] = "Pipeline for the Panjabi language"
    language: Optional[Language] = get_lang("pan")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            PanjabiSentenceSplittingProcess,
            PunjabiChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing PanjabiChatGPTPipeline with language: {self.language}"
        )
        logger.info("PanjabiChatGPTPipeline created.")


class DemoticChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Egyptian."""

    description: Optional[str] = "Pipeline for the Egyptian language"
    language: Optional[Language] = get_lang("egy-dem")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            DemoticSentenceSplittingProcess,
            DemoticChatGPTProcess,
        ]
    )

    def __post_init__(self):
        logger.debug(
            f"Initializing EgyptianChatGPTPipeline with language: {self.language}"
        )
        logger.info("EgyptianChatGPTPipeline created.")
