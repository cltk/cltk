"""Processes of POS and feature tagging."""

from collections.abc import Callable
from copy import copy
from functools import cached_property
from typing import Optional

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import Doc, Process
from cltk.core.logging_utils import bind_from_doc
from cltk.dependency.utils import (
    generate_gpt_dependency_concurrent,
)


class DependencyProcess(Process):
    """Base class for morphosyntactic processes."""


class GenAIDependencyProcess(DependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    @cached_property
    def algorithm(self) -> Callable[[Doc], Doc]:
        if not self.glottolog_id:
            msg: str = "glottolog_id must be set for DependencyProcess"
            bind_context(glottolog_id=self.glottolog_id).error(msg)
            raise ValueError(msg)
        # Prefer the safe concurrent wrapper (async under the hood, sync surface)
        return generate_gpt_dependency_concurrent

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


class CuneiformLuwianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "cune1239"
    description: str = "Default process using a generative GPT model for the Cuneiform Luwian language."
    authorship_info: str = "CuneiformLuwianGenAIProcess using a generative GPT model."


class HieroglyphicLuwianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "hier1240"
    description: str = "Default process using a generative GPT model for the Hieroglyphic Luwian language."
    authorship_info: str = (
        "HieroglyphicLuwianGenAIProcess using a generative GPT model."
    )


class OldPrussianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "prus1238"
    description: str = (
        "Default process using a generative GPT model for the Old Prussian language."
    )
    authorship_info: str = "OldPrussianGenAIProcess using a generative GPT model."


class LithuanianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "lith1251"
    description: str = (
        "Default process using a generative GPT model for the Lithuanian language."
    )
    authorship_info: str = "LithuanianGenAIProcess using a generative GPT model."


class LatvianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "latv1249"
    description: str = (
        "Default process using a generative GPT model for the Latvian language."
    )
    authorship_info: str = "LatvianGenAIProcess using a generative GPT model."


class AlbanianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "gheg1238"
    description: str = (
        "Default process using a generative GPT model for the Albanian language."
    )
    authorship_info: str = "AlbanianGenAIProcess using a generative GPT model."


class AkkadianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "akka1240"
    description: str = (
        "Default process using a generative GPT model for the Akkadian language."
    )
    authorship_info: str = "AkkadianGenAIProcess using a generative GPT model."


class AncientGreekGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "anci1242"
    description: str = (
        "Default process using a generative GPT model for the Ancient Greek language."
    )
    authorship_info: str = "Ancient GreekGenAIProcess using a generative GPT model."


class BiblicalHebrewGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "anci1244"
    description: str = (
        "Default process using a generative GPT model for the Biblical Hebrew language."
    )
    authorship_info: str = "Biblical HebrewGenAIProcess using a generative GPT model."


class ClassicalArabicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1259"
    description: str = "Default process using a generative GPT model for the Classical Arabic language."
    authorship_info: str = "ClassicalArabicGenAIProcess using a generative GPT model."


class AvestanGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "aves1237"
    description: str = (
        "Default process using a generative GPT model for the Avestan language."
    )
    authorship_info: str = "AvestanGenAIProcess using a generative GPT model."


class BactrianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "bact1239"
    description: str = (
        "Default process using a generative GPT model for the Bactrian language."
    )
    authorship_info: str = "BactrianGenAIProcess using a generative GPT model."


class SogdianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "sogd1245"
    description: str = (
        "Default process using a generative GPT model for the Sogdian language."
    )
    authorship_info: str = "SogdianGenAIProcess using a generative GPT model."


class BengaliGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "beng1280"
    description: str = (
        "Default process using a generative GPT model for the Bengali language."
    )
    authorship_info: str = "BengaliGenAIProcess using a generative GPT model."


class CarianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "cari1274"
    description: str = (
        "Default process using a generative GPT model for the Carian language."
    )
    authorship_info: str = "CarianGenAIProcess using a generative GPT model."


class ChurchSlavicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "chur1257"
    description: str = (
        "Default process using a generative GPT model for the Church Slavic language."
    )
    authorship_info: str = "Church SlavicGenAIProcess using a generative GPT model."


class ClassicalArmenianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1256"
    description: str = "Default process using a generative GPT model for the Classical Armenian language."
    authorship_info: str = (
        "Classical ArmenianGenAIProcess using a generative GPT model."
    )


class ClassicalMandaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1253"
    description: str = "Default process using a generative GPT model for the Classical Mandaic language."
    authorship_info: str = "Classical MandaicGenAIProcess using a generative GPT model."


class ClassicalMongolianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "mong1331"
    description: str = "Default process using a generative GPT model for the Classical Mongolian language."
    authorship_info: str = (
        "Classical MongolianGenAIProcess using a generative GPT model."
    )


class ClassicalSyriacGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1252"
    description: str = "Default process using a generative GPT model for the Classical Syriac language."
    authorship_info: str = "Classical SyriacGenAIProcess using a generative GPT model."


class ClassicalTibetanGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1254"
    description: str = "Default process using a generative GPT model for the Classical Tibetan language."
    authorship_info: str = "Classical TibetanGenAIProcess using a generative GPT model."


class CopticGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "copt1239"
    description: str = (
        "Default process using a generative GPT model for the Coptic language."
    )
    authorship_info: str = "CopticGenAIProcess using a generative GPT model."


class DemoticGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "demo1234"
    description: str = (
        "Default process using a generative GPT model for the Demotic language."
    )
    authorship_info: str = "DemoticGenAIProcess using a generative GPT model."


class EasternPanjabiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = (
        "Default process using a generative GPT model for the Eastern Panjabi language."
    )
    authorship_info: str = "Eastern PanjabiGenAIProcess using a generative GPT model."


class EdomiteGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "edom1234"
    description: str = (
        "Default process using a generative GPT model for the Edomite language."
    )
    authorship_info: str = "EdomiteGenAIProcess using a generative GPT model."


class GeezGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "geez1241"
    description: str = (
        "Default process using a generative GPT model for the Geez language."
    )
    authorship_info: str = "GeezGenAIProcess using a generative GPT model."


class GothicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "goth1244"
    description: str = (
        "Default process using a generative GPT model for the Gothic language."
    )
    authorship_info: str = "GothicGenAIProcess using a generative GPT model."


class GujaratiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "guja1252"
    description: str = (
        "Default process using a generative GPT model for the Gujarati language."
    )
    authorship_info: str = "GujaratiGenAIProcess using a generative GPT model."


class HindiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "hind1269"
    description: str = (
        "Default process using a generative GPT model for the Hindi language."
    )
    authorship_info: str = "HindiGenAIProcess using a generative GPT model."


class KhariBoliGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "khad1239"
    description: str = "Default process using a generative GPT model for the Khari Boli dialect of Hindi."
    authorship_info: str = "KhariBoliGenAIProcess using a generative GPT model."


class BrajGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "braj1242"
    description: str = (
        "Default process using a generative GPT model for the Braj Bhasha language."
    )
    authorship_info: str = "BrajGenAIProcess using a generative GPT model."


class AwadhiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "awad1243"
    description: str = (
        "Default process using a generative GPT model for the Awadhi language."
    )
    authorship_info: str = "AwadhiGenAIProcess using a generative GPT model."


class HittiteGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "hitt1242"
    description: str = (
        "Default process using a generative GPT model for the Hittite language."
    )
    authorship_info: str = "HittiteGenAIProcess using a generative GPT model."


class KhotaneseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "khot1251"
    description: str = (
        "Default process using a generative GPT model for the Khotanese language."
    )
    authorship_info: str = "KhotaneseGenAIProcess using a generative GPT model."


class TumshuqeseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "tums1237"
    description: str = (
        "Default process using a generative GPT model for the Tumshuqese language."
    )
    authorship_info: str = "TumshuqeseGenAIProcess using a generative GPT model."


class LateEgyptianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "late1256"
    description: str = (
        "Default process using a generative GPT model for the Late Egyptian language."
    )
    authorship_info: str = "Late Egyptian GenAIProcess using a generative GPT model."


class LatinGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "lati1261"
    description: str = (
        "Default process using a generative GPT model for the Latin language."
    )
    authorship_info: str = "LatinGenAIProcess using a generative GPT model."


class LiteraryChineseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "lite1248"
    description: str = "Default process using a generative GPT model for the Literary Chinese language."
    authorship_info: str = "Literary ChineseGenAIProcess using a generative GPT model."


class LycianAGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "lyci1241"
    description: str = (
        "Default process using a generative GPT model for the Lycian A language."
    )
    authorship_info: str = "Lycian AGenAIProcess using a generative GPT model."


class LydianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "lydi1241"
    description: str = (
        "Default process using a generative GPT model for the Lydian language."
    )
    authorship_info: str = "LydianGenAIProcess using a generative GPT model."


class MaharastriPrakritGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "maha1305"
    description: str = "Default process using a generative GPT model for the Maharastri Prakrit language."
    authorship_info: str = "MaharastriPrakritGenAIProcess using a generative GPT model."


class MiddleArmenianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1364"
    description: str = (
        "Default process using a generative GPT model for the Middle Armenian language."
    )
    authorship_info: str = "Middle ArmenianGenAIProcess using a generative GPT model."


class MiddleBretonGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldb1244"
    description: str = (
        "Default process using a generative GPT model for the Middle Breton language."
    )
    authorship_info: str = "Middle BretonGenAIProcess using a generative GPT model."


class MiddleChineseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1344"
    description: str = (
        "Default process using a generative GPT model for the Middle Chinese language."
    )
    authorship_info: str = "Middle ChineseGenAIProcess using a generative GPT model."


class MiddleCornishGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "corn1251"
    description: str = (
        "Default process using a generative GPT model for the Middle Cornish language."
    )
    authorship_info: str = "Middle CornishGenAIProcess using a generative GPT model."


class MiddleEgyptianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1369"
    description: str = (
        "Default process using a generative GPT model for the Middle Egyptian language."
    )
    authorship_info: str = "Middle Egyptian GenAIProcess using a generative GPT model."


class MiddleEnglishGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1317"
    description: str = (
        "Default process using a generative GPT model for the Middle English language."
    )
    authorship_info: str = "Middle EnglishGenAIProcess using a generative GPT model."


class MiddleFrenchGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1316"
    description: str = (
        "Default process using a generative GPT model for the Middle French language."
    )
    authorship_info: str = "Middle FrenchGenAIProcess using a generative GPT model."


class MiddleHighGermanGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1343"
    description: str = "Default process using a generative GPT model for the Middle High German language."
    authorship_info: str = (
        "Middle High GermanGenAIProcess using a generative GPT model."
    )


class MiddleMongolGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "mong1329"
    description: str = (
        "Default process using a generative GPT model for the Middle Mongol language."
    )
    authorship_info: str = "Middle MongolGenAIProcess using a generative GPT model."


class MoabiteGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "moab1234"
    description: str = (
        "Default process using a generative GPT model for the Moabite language."
    )
    authorship_info: str = "MoabiteGenAIProcess using a generative GPT model."


class OdiaGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oriy1255"
    description: str = (
        "Default process using a generative GPT model for the Odia language."
    )
    authorship_info: str = "OdiaGenAIProcess using a generative GPT model."


class OfficialAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "impe1235"
    description: str = "Default process using a generative GPT model for the Official Aramaic (700-300 BCE) language."
    authorship_info: str = (
        "Official Aramaic (700-300 BCE) GenAIProcess using a generative GPT model."
    )


class OldBurmeseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldb1235"
    description: str = (
        "Default process using a generative GPT model for the Old Burmese language."
    )
    authorship_info: str = "Old BurmeseGenAIProcess using a generative GPT model."


class OldChineseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldc1244"
    description: str = (
        "Default process using a generative GPT model for the Old Chinese language."
    )
    authorship_info: str = "Old ChineseGenAIProcess using a generative GPT model."


class BaihuaChineseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1255"
    description: str = "Default process using a generative GPT model for Early Vernacular Chinese (Baihua)."
    authorship_info: str = "BaihuaChineseGenAIProcess using a generative GPT model."


class ClassicalBurmeseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "nucl1310"
    description: str = "Default process using a generative GPT model for the Classical Burmese language."
    authorship_info: str = "ClassicalBurmeseGenAIProcess using a generative GPT model."


class TangutGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "tang1334"
    description: str = (
        "Default process using a generative GPT model for the Tangut (Xixia) language."
    )
    authorship_info: str = "TangutGenAIProcess using a generative GPT model."


class NewarGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "newa1246"
    description: str = "Default process using a generative GPT model for the Newar (Classical Nepal Bhasa) language."
    authorship_info: str = "NewarGenAIProcess using a generative GPT model."


class MeiteiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "mani1292"
    description: str = "Default process using a generative GPT model for the Meitei (Classical Manipuri) language."
    authorship_info: str = "MeiteiGenAIProcess using a generative GPT model."


class SgawKarenGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "sgaw1245"
    description: str = (
        "Default process using a generative GPT model for the Sgaw Karen language."
    )
    authorship_info: str = "SgawKarenGenAIProcess using a generative GPT model."


class MogholiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "mogh1245"
    description: str = "Default process using a generative GPT model for the Mogholi (Moghol) language."
    authorship_info: str = "MogholiGenAIProcess using a generative GPT model."


class NumidianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "numi1241"
    description: str = "Default process using a generative GPT model for the Numidian (Ancient Berber) language."
    authorship_info: str = "NumidianGenAIProcess using a generative GPT model."


class TaitaGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "tait1247"
    description: str = (
        "Default process using a generative GPT model for the Cushitic Taita language."
    )
    authorship_info: str = "TaitaGenAIProcess using a generative GPT model."


class HausaGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "haus1257"
    description: str = (
        "Default process using a generative GPT model for the Hausa language."
    )
    authorship_info: str = "HausaGenAIProcess using a generative GPT model."


class OldJurchenGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "jurc1239"
    description: str = (
        "Default process using a generative GPT model for the Old Jurchen language."
    )
    authorship_info: str = "OldJurchenGenAIProcess using a generative GPT model."


class OldJapaneseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "japo1237"
    description: str = (
        "Default process using a generative GPT model for the Old Japanese language."
    )
    authorship_info: str = "OldJapaneseGenAIProcess using a generative GPT model."


class OldHungarianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldh1242"
    description: str = (
        "Default process using a generative GPT model for the Old Hungarian language."
    )
    authorship_info: str = "OldHungarianGenAIProcess using a generative GPT model."


class ChagataiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "chag1247"
    description: str = (
        "Default process using a generative GPT model for the Chagatai language."
    )
    authorship_info: str = "ChagataiGenAIProcess using a generative GPT model."


class OldTurkicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldu1238"
    description: str = (
        "Default process using a generative GPT model for the Old Turkic language."
    )
    authorship_info: str = "OldTurkicGenAIProcess using a generative GPT model."


class OldTamilGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldt1248"
    description: str = (
        "Default process using a generative GPT model for the Old Tamil language."
    )
    authorship_info: str = "OldTamilGenAIProcess using a generative GPT model."


class AmmoniteGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "ammo1234"
    description: str = (
        "Default process using a generative GPT model for the Ammonite language."
    )
    authorship_info: str = "AmmoniteGenAIProcess using a generative GPT model."


class OldAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "olda1246"
    description: str = "Default process using a generative GPT model for the Old Aramaic (up to 700 BCE) language."
    authorship_info: str = "OldAramaicGenAIProcess using a generative GPT model."


class OldAramaicSamalianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "olda1245"
    description: str = "Default process using a generative GPT model for the Old Aramaic–Samʾalian language."
    authorship_info: str = (
        "OldAramaicSamalianGenAIProcess using a generative GPT model."
    )


class MiddleAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1366"
    description: str = (
        "Default process using a generative GPT model for the Middle Aramaic language."
    )
    authorship_info: str = "MiddleAramaicGenAIProcess using a generative GPT model."


class HatranGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "hatr1234"
    description: str = (
        "Default process using a generative GPT model for the Hatran language."
    )
    authorship_info: str = "HatranGenAIProcess using a generative GPT model."


class JewishBabylonianAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "jewi1240"
    description: str = "Default process using a generative GPT model for the Jewish Babylonian Aramaic language."
    authorship_info: str = (
        "JewishBabylonianAramaicGenAIProcess using a generative GPT model."
    )


class SamalianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "sama1234"
    description: str = (
        "Default process using a generative GPT model for the Samʾalian language."
    )
    authorship_info: str = "SamalianGenAIProcess using a generative GPT model."


class OldEgyptianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "olde1242"
    description: str = (
        "Default process using a generative GPT model for the Old Egyptian language."
    )
    authorship_info: str = "Old Egyptian GenAIProcess using a generative GPT model."


class OldEnglishGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "olde1238"
    description: str = "Default process using a generative GPT model for the Old English (ca. 450-1100) language."
    authorship_info: str = (
        "Old English (ca. 450-1100)GenAIProcess using a generative GPT model."
    )


class OldFrenchGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldf1239"
    description: str = "Default process using a generative GPT model for the Old French (842-ca. 1400) language."
    authorship_info: str = (
        "Old French (842-ca. 1400)GenAIProcess using a generative GPT model."
    )


class OldHighGermanGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldh1241"
    description: str = "Default process using a generative GPT model for the Old High German (ca. 750-1050) language."
    authorship_info: str = (
        "Old High German (ca. 750-1050)GenAIProcess using a generative GPT model."
    )


class EarlyIrishGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldi1245"
    description: str = (
        "Default process using a generative GPT model for the Old Irish language."
    )
    authorship_info: str = "Old IrishGenAIProcess using a generative GPT model."


class MarathiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "mara1378"
    description: str = (
        "Default process using a generative GPT model for the Marathi language."
    )
    authorship_info: str = "MarathiGenAIProcess using a generative GPT model."


class OldNorseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldn1244"
    description: str = (
        "Default process using a generative GPT model for the Old Norse language."
    )
    authorship_info: str = "Old NorseGenAIProcess using a generative GPT model."


class OldPersianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldp1254"
    description: str = "Default process using a generative GPT model for the Old Persian (ca. 600-400 B.C.) language."
    authorship_info: str = (
        "Old Persian (ca. 600-400 B.C.)GenAIProcess using a generative GPT model."
    )


class OldMiddleWelshGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldw1239"
    description: str = "Default process using a generative GPT model for the Old-Middle Welsh language."
    authorship_info: str = "Old-Middle WelshGenAIProcess using a generative GPT model."


class ParthianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "part1239"
    description: str = (
        "Default process using a generative GPT model for the Parthian language."
    )
    authorship_info: str = "ParthianGenAIProcess using a generative GPT model."


class MiddlePersianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "pahl1241"
    description: str = (
        "Default process using a generative GPT model for the Middle Persian language."
    )
    authorship_info: str = "MiddlePersianGenAIProcess using a generative GPT model."


class PalaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "pala1331"
    description: str = (
        "Default process using a generative GPT model for the Palaic language."
    )
    authorship_info: str = "PalaicGenAIProcess using a generative GPT model."


class PaliGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "pali1273"
    description: str = (
        "Default process using a generative GPT model for the Pali language."
    )
    authorship_info: str = "PaliGenAIProcess using a generative GPT model."


class PhoenicianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "phoe1239"
    description: str = (
        "Default process using a generative GPT model for the Phoenician language."
    )
    authorship_info: str = "PhoenicianGenAIProcess using a generative GPT model."


class PunjabiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = (
        "Default process using a generative GPT model for the Punjabi language."
    )
    authorship_info: str = "PunjabiGenAIProcess using a generative GPT model."


class AssameseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "assa1263"
    description: str = (
        "Default process using a generative GPT model for the Assamese language."
    )
    authorship_info: str = "AssameseGenAIProcess using a generative GPT model."


class SinhalaGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "sinh1246"
    description: str = (
        "Default process using a generative GPT model for the Sinhala language."
    )
    authorship_info: str = "SinhalaGenAIProcess using a generative GPT model."


class SindhiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "sind1272"
    description: str = (
        "Default process using a generative GPT model for the Sindhi language."
    )
    authorship_info: str = "SindhiGenAIProcess using a generative GPT model."


class KashmiriGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "kash1277"
    description: str = (
        "Default process using a generative GPT model for the Kashmiri language."
    )
    authorship_info: str = "KashmiriGenAIProcess using a generative GPT model."


class BagriGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "bagr1243"
    description: str = "Default process using a generative GPT model for the Bagri (Rajasthani) language."
    authorship_info: str = "BagriGenAIProcess using a generative GPT model."


class ClassicalSanskritGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1258"
    description: str = "Default process using a generative GPT model for the Classical Sanskrit language."
    authorship_info: str = "ClassicalSanskritGenAIProcess using a generative GPT model."


class VedicSanskritGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "vedi1234"
    description: str = (
        "Default process using a generative GPT model for the Vedic Sanskrit language."
    )
    authorship_info: str = "VedicSanskritGenAIProcess using a generative GPT model."


class TokharianAGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "toch1238"
    description: str = (
        "Default process using a generative GPT model for the Tokharian A language."
    )
    authorship_info: str = "Tokharian AGenAIProcess using a generative GPT model."


class TokharianBGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "toch1237"
    description: str = (
        "Default process using a generative GPT model for the Tokharian B language."
    )
    authorship_info: str = "Tokharian BGenAIProcess using a generative GPT model."


class UgariticGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "ugar1238"
    description: str = (
        "Default process using a generative GPT model for the Ugaritic language."
    )
    authorship_info: str = "UgariticGenAIProcess using a generative GPT model."


class UrduGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "urdu1245"
    description: str = (
        "Default process using a generative GPT model for the Urdu language."
    )
    authorship_info: str = "UrduGenAIProcess using a generative GPT model."


class SauraseniPrakritGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "saur1252"
    description: str = "Default process using a generative GPT model for the Sauraseni Prakrit language."
    authorship_info: str = "SauraseniPrakritGenAIProcess using a generative GPT model."


class MagadhiPrakritGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "maga1260"
    description: str = (
        "Default process using a generative GPT model for the Magadhi Prakrit language."
    )
    authorship_info: str = "MagadhiPrakritGenAIProcess using a generative GPT model."


class GandhariGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "gand1259"
    description: str = (
        "Default process using a generative GPT model for the Gandhari language."
    )
    authorship_info: str = "GandhariGenAIProcess using a generative GPT model."
