"""Default processing pipelines for languages. The purpose of
these dataclasses is to represent:

1. the types of NLP processes that the CLTK can do
2. the order in which processes are to be executed
3. specifying what downstream features a particular implemented process requires
"""

from dataclasses import dataclass, field
from typing import Optional, Type

from cltk.alphabet.processes import GreekNormalizeProcess, LatinNormalizeProcess
from cltk.core.data_types import Language, Pipeline, Process
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
from cltk.genai.processes import AncientGreekChatGPTProcess
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


@dataclass
class AkkadianPipeline(Pipeline):
    """Default ``Pipeline`` for Akkadian."""

    description: Optional[str] = "Pipeline for the Akkadian language."
    language: Optional[Language] = get_lang("akk")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [AkkadianTokenizationProcess, StopsProcess]
    )


@dataclass
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


@dataclass
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


@dataclass
class ChinesePipeline(Pipeline):
    """Default ``Pipeline`` for Classical Chinese."""

    description: Optional[str] = "Pipeline for the Classical Chinese language"
    language: Optional[Language] = get_lang("lzh")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [ChineseStanzaProcess]
    )


@dataclass
class CopticPipeline(Pipeline):
    """Default ``Pipeline`` for Coptic."""

    description: Optional[str] = "Pipeline for the Coptic language"
    language: Optional[Language] = get_lang("cop")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [CopticStanzaProcess, StopsProcess]
    )


@dataclass
class GothicPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic."""

    description: Optional[str] = "Pipeline for the Gothic language"
    language: Optional[Language] = get_lang("got")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [GothicStanzaProcess, GothicEmbeddingsProcess]
    )


@dataclass
class GreekPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Greek."""

    description: Optional[str] = "Pipeline for the Greek language"
    language: Optional[Language] = get_lang("grc")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [
            GreekNormalizeProcess,
            GreekSpacyProcess,
            GreekEmbeddingsProcess,
            StopsProcess,
        ]
    )


@dataclass
class GreekChatGPTPipeline(Pipeline):
    """Pipeline for Ancient Greek using normalization and ChatGPT annotation only."""

    description: Optional[str] = "Pipeline for Ancient Greek with ChatGPT annotation"
    language: Optional[Language] = get_lang("grc")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [GreekNormalizeProcess, AncientGreekChatGPTProcess]
    )


@dataclass
class HindiPipeline(Pipeline):
    """Default ``Pipeline`` for Hindi."""

    description: Optional[str] = "Pipeline for the Hindi language."
    language: Optional[Language] = get_lang("hin")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [MultilingualTokenizationProcess, StopsProcess]
    )


@dataclass
class LatinPipeline(Pipeline):
    """Default ``Pipeline`` for Latin."""

    description: Optional[str] = "Pipeline for the Latin language"
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


@dataclass
class MiddleHighGermanPipeline(Pipeline):
    """Default ``Pipeline`` for Middle High German."""

    description: Optional[str] = "Pipeline for the Middle High German language."
    language: Optional[Language] = get_lang("gmh")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [MiddleHighGermanTokenizationProcess, StopsProcess]
    )


@dataclass
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


@dataclass
class MiddleFrenchPipeline(Pipeline):
    """Default ``Pipeline`` for Middle French."""

    description: Optional[str] = "Pipeline for the Middle French language"
    language: Optional[Language] = get_lang("frm")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [MiddleFrenchTokenizationProcess]
    )


@dataclass
class OCSPipeline(Pipeline):
    """Default ``Pipeline`` for Old Church Slavonic."""

    description: Optional[str] = "Pipeline for the Old Church Slavonic language"
    language: Optional[Language] = get_lang("chu")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [OCSStanzaProcess]
    )


@dataclass
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


@dataclass
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


# TODO: Add Old Marathi ("omr")


@dataclass
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


@dataclass
class PaliPipeline(Pipeline):
    """Default ``Pipeline`` for Pali."""

    description: Optional[str] = "Pipeline for the Pali language"
    language: Optional[Language] = get_lang("pli")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [MultilingualTokenizationProcess, PaliEmbeddingsProcess]
    )


@dataclass
class PanjabiPipeline(Pipeline):
    """Default ``Pipeline`` for Panjabi."""

    description: Optional[str] = "Pipeline for the Panjabi language."
    language: Optional[Language] = get_lang("pan")
    processes: Optional[list[Type[Process]]] = field(
        default_factory=lambda: [MultilingualTokenizationProcess, StopsProcess]
    )


@dataclass
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
