"""Default processing pipelines for languages. The purpose of
these dataclasses is to represent:

1. the types of NLP processes that the CLTK can do
2. the order in which processes are to be executed
3. specifying what downstream features a particular implemented process requires
"""

from dataclasses import dataclass, field
from typing import Optional, Type

from cltk.alphabet.processes import AncientGreekNormalizeProcess, LatinNormalizeProcess
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
    AncientGreekChatGPTProcess,
    LatinChatGPTProcess,
    PaliChatGPTProcess,
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


class ArabicPipeline(Pipeline):
    """Default ``Pipeline`` for Arabic."""

    description: Optional[str] = "Pipeline for the Arabic language"
    language: Optional[Language] = get_lang("arb")
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
            AncientGreekNormalizeProcess,
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

    def __post_init__(self):
        logger.debug(f"Initializing LatinPipeline with language: {self.language}")
        logger.info("LatinPipeline created.")


class LatinChatGPTPipeline(Pipeline):
    """Default ``Pipeline`` for Latin."""

    description: Optional[str] = "ChatGPT Pipeline for the Latin language."
    language: Optional[Language] = get_lang("lat")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            LatinNormalizeProcess,
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
        default_factory=lambda: [PaliChatGPTProcess]
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
