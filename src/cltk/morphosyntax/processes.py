"""Processes of POS and feature tagging."""

from collections.abc import Callable
from copy import copy
from functools import cached_property
from typing import Optional

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import Doc, Process
from cltk.core.logging_utils import bind_from_doc
from cltk.morphosyntax.utils import (
    generate_gpt_morphosyntax_concurrent,
)


class MorphosyntaxProcess(Process):
    """Base class for morphosyntactic processes."""


class GenAIMorphosyntaxProcess(MorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    @cached_property
    def algorithm(self) -> Callable[[Doc], Doc]:
        if not self.glottolog_id:
            msg: str = "glottolog_id must be set for MorphosyntaxProcess"
            bind_context(glottolog_id=self.glottolog_id).error(msg)
            raise ValueError(msg)
        # Prefer the safe concurrent wrapper (async under the hood, sync surface)
        return generate_gpt_morphosyntax_concurrent

    def run(self, input_doc: Doc) -> Doc:
        output_doc = copy(input_doc)
        if not output_doc.normalized_text:
            msg: str = "Doc must have `normalized_text`."
            bind_from_doc(output_doc).error(msg)
            raise ValueError(msg)
        # Ensure required attributes are present
        if self.glottolog_id is None:
            raise ValueError("glottolog_id must be set for sentence splitting")
        # Callable typing does not retain keyword names; pass positionally
        output_doc = self.algorithm(
            output_doc,
        )
        return output_doc


class CuneiformLuwianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "cune1239"
    description: str = "Default process using a generative GPT model for the Cuneiform Luwian language."
    authorship_info: str = "CuneiformLuwianGenAIProcess a generative GPT model."


class HieroglyphicLuwianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "hier1240"
    description: str = "Default process using a generative GPT model for the Hieroglyphic Luwian language."
    authorship_info: str = "HieroglyphicLuwianGenAIProcess a generative GPT model."


class OldPrussianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "prus1238"
    description: str = (
        "Default process using a generative GPT model for the Old Prussian language."
    )
    authorship_info: str = "OldPrussianGenAIProcess a generative GPT model."


class LithuanianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "lith1251"
    description: str = (
        "Default process using a generative GPT model for the Lithuanian language."
    )
    authorship_info: str = "LithuanianGenAIProcess a generative GPT model."


class LatvianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "latv1249"
    description: str = (
        "Default process using a generative GPT model for the Latvian language."
    )
    authorship_info: str = "LatvianGenAIProcess a generative GPT model."


class AlbanianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "gheg1238"
    description: str = (
        "Default process using a generative GPT model for the Albanian language."
    )
    authorship_info: str = "AlbanianGenAIProcess a generative GPT model."


class AkkadianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "akka1240"
    description: str = (
        "Default process using a generative GPT model for the Akkadian language."
    )
    authorship_info: str = "AkkadianGenAIProcess a generative GPT model."


class AncientGreekGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "anci1242"
    description: str = (
        "Default process using a generative GPT model for the Ancient Greek language."
    )
    authorship_info: str = "Ancient GreekGenAIProcess a generative GPT model."


class BiblicalHebrewGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "anci1244"
    description: str = (
        "Default process using a generative GPT model for the Biblical Hebrew language."
    )
    authorship_info: str = "Biblical HebrewGenAIProcess a generative GPT model."


class ClassicalArabicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1259"
    description: str = "Default process using a generative GPT model for the Classical Arabic language."
    authorship_info: str = "ClassicalArabicGenAIProcess a generative GPT model."


class AvestanGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "aves1237"
    description: str = (
        "Default process using a generative GPT model for the Avestan language."
    )
    authorship_info: str = "AvestanGenAIProcess a generative GPT model."


class BactrianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "bact1239"
    description: str = (
        "Default process using a generative GPT model for the Bactrian language."
    )
    authorship_info: str = "BactrianGenAIProcess a generative GPT model."


class SogdianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "sogd1245"
    description: str = (
        "Default process using a generative GPT model for the Sogdian language."
    )
    authorship_info: str = "SogdianGenAIProcess a generative GPT model."


class BengaliGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "beng1280"
    description: str = (
        "Default process using a generative GPT model for the Bengali language."
    )
    authorship_info: str = "BengaliGenAIProcess a generative GPT model."


class CarianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "cari1274"
    description: str = (
        "Default process using a generative GPT model for the Carian language."
    )
    authorship_info: str = "CarianGenAIProcess a generative GPT model."


class ChurchSlavicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "chur1257"
    description: str = (
        "Default process using a generative GPT model for the Church Slavic language."
    )
    authorship_info: str = "Church SlavicGenAIProcess a generative GPT model."


class ClassicalArmenianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1256"
    description: str = "Default process using a generative GPT model for the Classical Armenian language."
    authorship_info: str = "Classical ArmenianGenAIProcess a generative GPT model."


class ClassicalMandaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1253"
    description: str = "Default process using a generative GPT model for the Classical Mandaic language."
    authorship_info: str = "Classical MandaicGenAIProcess a generative GPT model."


class ClassicalMongolianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "mong1331"
    description: str = "Default process using a generative GPT model for the Classical Mongolian language."
    authorship_info: str = "Classical MongolianGenAIProcess a generative GPT model."


class ClassicalSyriacGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1252"
    description: str = "Default process using a generative GPT model for the Classical Syriac language."
    authorship_info: str = "Classical SyriacGenAIProcess a generative GPT model."


class ClassicalTibetanGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1254"
    description: str = "Default process using a generative GPT model for the Classical Tibetan language."
    authorship_info: str = "Classical TibetanGenAIProcess a generative GPT model."


class CopticGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "copt1239"
    description: str = (
        "Default process using a generative GPT model for the Coptic language."
    )
    authorship_info: str = "CopticGenAIProcess a generative GPT model."


class DemoticGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "demo1234"
    description: str = (
        "Default process using a generative GPT model for the Demotic language."
    )
    authorship_info: str = "DemoticGenAIProcess a generative GPT model."


class EasternPanjabiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = (
        "Default process using a generative GPT model for the Eastern Panjabi language."
    )
    authorship_info: str = "Eastern PanjabiGenAIProcess a generative GPT model."


class EdomiteGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "edom1234"
    description: str = (
        "Default process using a generative GPT model for the Edomite language."
    )
    authorship_info: str = "EdomiteGenAIProcess a generative GPT model."


class GeezGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "geez1241"
    description: str = (
        "Default process using a generative GPT model for the Geez language."
    )
    authorship_info: str = "GeezGenAIProcess a generative GPT model."


class GothicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "goth1244"
    description: str = (
        "Default process using a generative GPT model for the Gothic language."
    )
    authorship_info: str = "GothicGenAIProcess a generative GPT model."


class GujaratiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "guja1252"
    description: str = (
        "Default process using a generative GPT model for the Gujarati language."
    )
    authorship_info: str = "GujaratiGenAIProcess a generative GPT model."


class HindiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "hind1269"
    description: str = (
        "Default process using a generative GPT model for the Hindi language."
    )
    authorship_info: str = "HindiGenAIProcess a generative GPT model."


class KhariBoliGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "khad1239"
    description: str = "Default process using a generative GPT model for the Khari Boli dialect of Hindi."
    authorship_info: str = "KhariBoliGenAIProcess a generative GPT model."


class BrajGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "braj1242"
    description: str = (
        "Default process using a generative GPT model for the Braj Bhasha language."
    )
    authorship_info: str = "BrajGenAIProcess a generative GPT model."


class AwadhiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "awad1243"
    description: str = (
        "Default process using a generative GPT model for the Awadhi language."
    )
    authorship_info: str = "AwadhiGenAIProcess a generative GPT model."


class HittiteGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "hitt1242"
    description: str = (
        "Default process using a generative GPT model for the Hittite language."
    )
    authorship_info: str = "HittiteGenAIProcess a generative GPT model."


class KhotaneseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "khot1251"
    description: str = (
        "Default process using a generative GPT model for the Khotanese language."
    )
    authorship_info: str = "KhotaneseGenAIProcess a generative GPT model."


class TumshuqeseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "tums1237"
    description: str = (
        "Default process using a generative GPT model for the Tumshuqese language."
    )
    authorship_info: str = "TumshuqeseGenAIProcess a generative GPT model."


class LateEgyptianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "late1256"
    description: str = (
        "Default process using a generative GPT model for the Late Egyptian language."
    )
    authorship_info: str = "Late Egyptian GenAIProcess a generative GPT model."


class LatinGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "lati1261"
    description: str = (
        "Default process using a generative GPT model for the Latin language."
    )
    authorship_info: str = "LatinGenAIProcess a generative GPT model."


class LiteraryChineseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "lite1248"
    description: str = "Default process using a generative GPT model for the Literary Chinese language."
    authorship_info: str = "Literary ChineseGenAIProcess a generative GPT model."


class LycianAGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "lyci1241"
    description: str = (
        "Default process using a generative GPT model for the Lycian A language."
    )
    authorship_info: str = "Lycian AGenAIProcess a generative GPT model."


class LydianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "lydi1241"
    description: str = (
        "Default process using a generative GPT model for the Lydian language."
    )
    authorship_info: str = "LydianGenAIProcess a generative GPT model."


class MaharastriPrakritGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "maha1305"
    description: str = "Default process using a generative GPT model for the Maharastri Prakrit language."
    authorship_info: str = "MaharastriPrakritGenAIProcess a generative GPT model."


class MiddleArmenianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1364"
    description: str = (
        "Default process using a generative GPT model for the Middle Armenian language."
    )
    authorship_info: str = "Middle ArmenianGenAIProcess a generative GPT model."


class MiddleBretonGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldb1244"
    description: str = (
        "Default process using a generative GPT model for the Middle Breton language."
    )
    authorship_info: str = "Middle BretonGenAIProcess a generative GPT model."


class MiddleChineseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1344"
    description: str = (
        "Default process using a generative GPT model for the Middle Chinese language."
    )
    authorship_info: str = "Middle ChineseGenAIProcess a generative GPT model."


class MiddleCornishGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "corn1251"
    description: str = (
        "Default process using a generative GPT model for the Middle Cornish language."
    )
    authorship_info: str = "Middle CornishGenAIProcess a generative GPT model."


class MiddleEgyptianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1369"
    description: str = (
        "Default process using a generative GPT model for the Middle Egyptian language."
    )
    authorship_info: str = "Middle Egyptian GenAIProcess a generative GPT model."


class MiddleEnglishGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1317"
    description: str = (
        "Default process using a generative GPT model for the Middle English language."
    )
    authorship_info: str = "Middle EnglishGenAIProcess a generative GPT model."


class MiddleFrenchGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1316"
    description: str = (
        "Default process using a generative GPT model for the Middle French language."
    )
    authorship_info: str = "Middle FrenchGenAIProcess a generative GPT model."


class MiddleHighGermanGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1343"
    description: str = "Default process using a generative GPT model for the Middle High German language."
    authorship_info: str = "Middle High GermanGenAIProcess a generative GPT model."


class MiddleMongolGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "mong1329"
    description: str = (
        "Default process using a generative GPT model for the Middle Mongol language."
    )
    authorship_info: str = "Middle MongolGenAIProcess a generative GPT model."


class MoabiteGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "moab1234"
    description: str = (
        "Default process using a generative GPT model for the Moabite language."
    )
    authorship_info: str = "MoabiteGenAIProcess a generative GPT model."


class OdiaGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oriy1255"
    description: str = (
        "Default process using a generative GPT model for the Odia language."
    )
    authorship_info: str = "OdiaGenAIProcess a generative GPT model."


class OfficialAramaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "impe1235"
    description: str = "Default process using a generative GPT model for the Official Aramaic (700-300 BCE) language."
    authorship_info: str = (
        "Official Aramaic (700-300 BCE) GenAIProcess a generative GPT model."
    )


class OldBurmeseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldb1235"
    description: str = (
        "Default process using a generative GPT model for the Old Burmese language."
    )
    authorship_info: str = "Old BurmeseGenAIProcess a generative GPT model."


class OldChineseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldc1244"
    description: str = (
        "Default process using a generative GPT model for the Old Chinese language."
    )
    authorship_info: str = "Old ChineseGenAIProcess a generative GPT model."


class BaihuaChineseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1255"
    description: str = "Default process using a generative GPT model for Early Vernacular Chinese (Baihua)."
    authorship_info: str = "BaihuaChineseGenAIProcess a generative GPT model."


class ClassicalBurmeseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "nucl1310"
    description: str = "Default process using a generative GPT model for the Classical Burmese language."
    authorship_info: str = "ClassicalBurmeseGenAIProcess a generative GPT model."


class TangutGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "tang1334"
    description: str = (
        "Default process using a generative GPT model for the Tangut (Xixia) language."
    )
    authorship_info: str = "TangutGenAIProcess a generative GPT model."


class NewarGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "newa1246"
    description: str = "Default process using a generative GPT model for the Newar (Classical Nepal Bhasa) language."
    authorship_info: str = "NewarGenAIProcess a generative GPT model."


class MeiteiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "mani1292"
    description: str = "Default process using a generative GPT model for the Meitei (Classical Manipuri) language."
    authorship_info: str = "MeiteiGenAIProcess a generative GPT model."


class SgawKarenGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "sgaw1245"
    description: str = (
        "Default process using a generative GPT model for the Sgaw Karen language."
    )
    authorship_info: str = "SgawKarenGenAIProcess a generative GPT model."


class MogholiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "mogh1245"
    description: str = "Default process using a generative GPT model for the Mogholi (Moghol) language."
    authorship_info: str = "MogholiGenAIProcess a generative GPT model."


class NumidianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "numi1241"
    description: str = "Default process using a generative GPT model for the Numidian (Ancient Berber) language."
    authorship_info: str = "NumidianGenAIProcess a generative GPT model."


class TaitaGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "tait1247"
    description: str = (
        "Default process using a generative GPT model for the Cushitic Taita language."
    )
    authorship_info: str = "TaitaGenAIProcess a generative GPT model."


class HausaGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "haus1257"
    description: str = (
        "Default process using a generative GPT model for the Hausa language."
    )
    authorship_info: str = "HausaGenAIProcess a generative GPT model."


class OldJurchenGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "jurc1239"
    description: str = (
        "Default process using a generative GPT model for the Old Jurchen language."
    )
    authorship_info: str = "OldJurchenGenAIProcess a generative GPT model."


class OldJapaneseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "japo1237"
    description: str = (
        "Default process using a generative GPT model for the Old Japanese language."
    )
    authorship_info: str = "OldJapaneseGenAIProcess a generative GPT model."


class OldHungarianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldh1242"
    description: str = (
        "Default process using a generative GPT model for the Old Hungarian language."
    )
    authorship_info: str = "OldHungarianGenAIProcess a generative GPT model."


class ChagataiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "chag1247"
    description: str = (
        "Default process using a generative GPT model for the Chagatai language."
    )
    authorship_info: str = "ChagataiGenAIProcess a generative GPT model."


class OldTurkicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldu1238"
    description: str = (
        "Default process using a generative GPT model for the Old Turkic language."
    )
    authorship_info: str = "OldTurkicGenAIProcess a generative GPT model."


class OldTamilGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldt1248"
    description: str = (
        "Default process using a generative GPT model for the Old Tamil language."
    )
    authorship_info: str = "OldTamilGenAIProcess a generative GPT model."


class AmmoniteGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "ammo1234"
    description: str = (
        "Default process using a generative GPT model for the Ammonite language."
    )
    authorship_info: str = "AmmoniteGenAIProcess a generative GPT model."


class OldAramaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "olda1246"
    description: str = "Default process using a generative GPT model for the Old Aramaic (up to 700 BCE) language."
    authorship_info: str = "OldAramaicGenAIProcess a generative GPT model."


class OldAramaicSamalianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "olda1245"
    description: str = "Default process using a generative GPT model for the Old Aramaic–Samʾalian language."
    authorship_info: str = "OldAramaicSamalianGenAIProcess a generative GPT model."


class MiddleAramaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1366"
    description: str = (
        "Default process using a generative GPT model for the Middle Aramaic language."
    )
    authorship_info: str = "MiddleAramaicGenAIProcess a generative GPT model."


class HatranGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "hatr1234"
    description: str = (
        "Default process using a generative GPT model for the Hatran language."
    )
    authorship_info: str = "HatranGenAIProcess a generative GPT model."


class JewishBabylonianAramaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "jewi1240"
    description: str = "Default process using a generative GPT model for the Jewish Babylonian Aramaic language."
    authorship_info: str = "JewishBabylonianAramaicGenAIProcess a generative GPT model."


class SamalianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "sama1234"
    description: str = (
        "Default process using a generative GPT model for the Samʾalian language."
    )
    authorship_info: str = "SamalianGenAIProcess a generative GPT model."


class OldEgyptianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "olde1242"
    description: str = (
        "Default process using a generative GPT model for the Old Egyptian language."
    )
    authorship_info: str = "Old Egyptian GenAIProcess a generative GPT model."


class OldEnglishGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "olde1238"
    description: str = "Default process using a generative GPT model for the Old English (ca. 450-1100) language."
    authorship_info: str = (
        "Old English (ca. 450-1100)GenAIProcess a generative GPT model."
    )


class OldFrenchGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldf1239"
    description: str = "Default process using a generative GPT model for the Old French (842-ca. 1400) language."
    authorship_info: str = (
        "Old French (842-ca. 1400)GenAIProcess a generative GPT model."
    )


class OldHighGermanGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldh1241"
    description: str = "Default process using a generative GPT model for the Old High German (ca. 750-1050) language."
    authorship_info: str = (
        "Old High German (ca. 750-1050)GenAIProcess a generative GPT model."
    )


class EarlyIrishGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldi1245"
    description: str = (
        "Default process using a generative GPT model for the Old Irish language."
    )
    authorship_info: str = "Old IrishGenAIProcess a generative GPT model."


class MarathiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "mara1378"
    description: str = (
        "Default process using a generative GPT model for the Marathi language."
    )
    authorship_info: str = "MarathiGenAIProcess a generative GPT model."


class OldNorseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldn1244"
    description: str = (
        "Default process using a generative GPT model for the Old Norse language."
    )
    authorship_info: str = "Old NorseGenAIProcess a generative GPT model."


class OldPersianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldp1254"
    description: str = "Default process using a generative GPT model for the Old Persian (ca. 600-400 B.C.) language."
    authorship_info: str = (
        "Old Persian (ca. 600-400 B.C.)GenAIProcess a generative GPT model."
    )


class OldMiddleWelshGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldw1239"
    description: str = "Default process using a generative GPT model for the Old-Middle Welsh language."
    authorship_info: str = "Old-Middle WelshGenAIProcess a generative GPT model."


class ParthianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "part1239"
    description: str = (
        "Default process using a generative GPT model for the Parthian language."
    )
    authorship_info: str = "ParthianGenAIProcess a generative GPT model."


class MiddlePersianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "pahl1241"
    description: str = (
        "Default process using a generative GPT model for the Middle Persian language."
    )
    authorship_info: str = "MiddlePersianGenAIProcess a generative GPT model."


class PalaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "pala1331"
    description: str = (
        "Default process using a generative GPT model for the Palaic language."
    )
    authorship_info: str = "PalaicGenAIProcess a generative GPT model."


class PaliGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "pali1273"
    description: str = (
        "Default process using a generative GPT model for the Pali language."
    )
    authorship_info: str = "PaliGenAIProcess a generative GPT model."


class PhoenicianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "phoe1239"
    description: str = (
        "Default process using a generative GPT model for the Phoenician language."
    )
    authorship_info: str = "PhoenicianGenAIProcess a generative GPT model."


class PunjabiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = (
        "Default process using a generative GPT model for the Punjabi language."
    )
    authorship_info: str = "PunjabiGenAIProcess a generative GPT model."


class AssameseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "assa1263"
    description: str = (
        "Default process using a generative GPT model for the Assamese language."
    )
    authorship_info: str = "AssameseGenAIProcess a generative GPT model."


class SinhalaGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "sinh1246"
    description: str = (
        "Default process using a generative GPT model for the Sinhala language."
    )
    authorship_info: str = "SinhalaGenAIProcess a generative GPT model."


class SindhiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "sind1272"
    description: str = (
        "Default process using a generative GPT model for the Sindhi language."
    )
    authorship_info: str = "SindhiGenAIProcess a generative GPT model."


class KashmiriGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "kash1277"
    description: str = (
        "Default process using a generative GPT model for the Kashmiri language."
    )
    authorship_info: str = "KashmiriGenAIProcess a generative GPT model."


class BagriGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "bagr1243"
    description: str = "Default process using a generative GPT model for the Bagri (Rajasthani) language."
    authorship_info: str = "BagriGenAIProcess a generative GPT model."


class ClassicalSanskritGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1258"
    description: str = "Default process using a generative GPT model for the Classical Sanskrit language."
    authorship_info: str = "ClassicalSanskritGenAIProcess a generative GPT model."


class VedicSanskritGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "vedi1234"
    description: str = (
        "Default process using a generative GPT model for the Vedic Sanskrit language."
    )
    authorship_info: str = "VedicSanskritGenAIProcess a generative GPT model."


class TokharianAGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "toch1238"
    description: str = (
        "Default process using a generative GPT model for the Tokharian A language."
    )
    authorship_info: str = "Tokharian AGenAIProcess a generative GPT model."


class TokharianBGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "toch1237"
    description: str = (
        "Default process using a generative GPT model for the Tokharian B language."
    )
    authorship_info: str = "Tokharian BGenAIProcess a generative GPT model."


class UgariticGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "ugar1238"
    description: str = (
        "Default process using a generative GPT model for the Ugaritic language."
    )
    authorship_info: str = "UgariticGenAIProcess a generative GPT model."


class UrduGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "urdu1245"
    description: str = (
        "Default process using a generative GPT model for the Urdu language."
    )
    authorship_info: str = "UrduGenAIProcess a generative GPT model."


class SauraseniPrakritGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "saur1252"
    description: str = "Default process using a generative GPT model for the Sauraseni Prakrit language."
    authorship_info: str = "SauraseniPrakritGenAIProcess a generative GPT model."


class MagadhiPrakritGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "maga1260"
    description: str = (
        "Default process using a generative GPT model for the Magadhi Prakrit language."
    )
    authorship_info: str = "MagadhiPrakritGenAIProcess a generative GPT model."


class GandhariGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    glottolog_id: Optional[str] = "gand1259"
    description: str = (
        "Default process using a generative GPT model for the Gandhari language."
    )
    authorship_info: str = "GandhariGenAIProcess a generative GPT model."
