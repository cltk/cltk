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
    """Language-specific dependency process using OpenAI."""

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
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "cune1239"
    description: str = "Default process for OpenAI for the Cuneiform Luwian language."
    authorship_info: str = "CuneiformLuwianOpenAIProcess using OpenAI GPT models."


class HieroglyphicLuwianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "hier1240"
    description: str = (
        "Default process for OpenAI for the Hieroglyphic Luwian language."
    )
    authorship_info: str = "HieroglyphicLuwianOpenAIProcess using OpenAI GPT models."


class OldPrussianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "prus1238"
    description: str = "Default process for OpenAI for the Old Prussian language."
    authorship_info: str = "OldPrussianOpenAIProcess using OpenAI GPT models."


class LithuanianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "lith1251"
    description: str = "Default process for OpenAI for the Lithuanian language."
    authorship_info: str = "LithuanianOpenAIProcess using OpenAI GPT models."


class LatvianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "latv1249"
    description: str = "Default process for OpenAI for the Latvian language."
    authorship_info: str = "LatvianOpenAIProcess using OpenAI GPT models."


class AlbanianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "gheg1238"
    description: str = "Default process for OpenAI for the Albanian language."
    authorship_info: str = "AlbanianOpenAIProcess using OpenAI GPT models."


class AkkadianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "akka1240"
    description: str = "Default process for OpenAI for the Akkadian language."
    authorship_info: str = "AkkadianOpenAIProcess using OpenAI GPT models."


class AncientGreekGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "anci1242"
    description: str = "Default process for OpenAI for the Ancient Greek language."
    authorship_info: str = "Ancient GreekOpenAIProcess using OpenAI GPT models."


class BiblicalHebrewGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "anci1244"
    description: str = "Default process for OpenAI for the Biblical Hebrew language."
    authorship_info: str = "Biblical HebrewOpenAIProcess using OpenAI GPT models."


class ClassicalArabicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1259"
    description: str = "Default process for OpenAI for the Classical Arabic language."
    authorship_info: str = "ClassicalArabicOpenAIProcess using OpenAI GPT models."


class AvestanGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "aves1237"
    description: str = "Default process for OpenAI for the Avestan language."
    authorship_info: str = "AvestanOpenAIProcess using OpenAI GPT models."


class BactrianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "bact1239"
    description: str = "Default process for OpenAI for the Bactrian language."
    authorship_info: str = "BactrianOpenAIProcess using OpenAI GPT models."


class SogdianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "sogd1245"
    description: str = "Default process for OpenAI for the Sogdian language."
    authorship_info: str = "SogdianOpenAIProcess using OpenAI GPT models."


class BengaliGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "beng1280"
    description: str = "Default process for OpenAI for the Bengali language."
    authorship_info: str = "BengaliOpenAIProcess using OpenAI GPT models."


class CarianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "cari1274"
    description: str = "Default process for OpenAI for the Carian language."
    authorship_info: str = "CarianOpenAIProcess using OpenAI GPT models."


class ChurchSlavicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "chur1257"
    description: str = "Default process for OpenAI for the Church Slavic language."
    authorship_info: str = "Church SlavicOpenAIProcess using OpenAI GPT models."


class ClassicalArmenianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1256"
    description: str = "Default process for OpenAI for the Classical Armenian language."
    authorship_info: str = "Classical ArmenianOpenAIProcess using OpenAI GPT models."


class ClassicalMandaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1253"
    description: str = "Default process for OpenAI for the Classical Mandaic language."
    authorship_info: str = "Classical MandaicOpenAIProcess using OpenAI GPT models."


class ClassicalMongolianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "mong1331"
    description: str = (
        "Default process for OpenAI for the Classical Mongolian language."
    )
    authorship_info: str = "Classical MongolianOpenAIProcess using OpenAI GPT models."


class ClassicalSyriacGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1252"
    description: str = "Default process for OpenAI for the Classical Syriac language."
    authorship_info: str = "Classical SyriacOpenAIProcess using OpenAI GPT models."


class ClassicalTibetanGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1254"
    description: str = "Default process for OpenAI for the Classical Tibetan language."
    authorship_info: str = "Classical TibetanOpenAIProcess using OpenAI GPT models."


class CopticGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "copt1239"
    description: str = "Default process for OpenAI for the Coptic language."
    authorship_info: str = "CopticOpenAIProcess using OpenAI GPT models."


class DemoticGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "demo1234"
    description: str = "Default process for OpenAI for the Demotic language."
    authorship_info: str = "DemoticOpenAIProcess using OpenAI GPT models."


class EasternPanjabiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default process for OpenAI for the Eastern Panjabi language."
    authorship_info: str = "Eastern PanjabiOpenAIProcess using OpenAI GPT models."


class EdomiteGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "edom1234"
    description: str = "Default process for OpenAI for the Edomite language."
    authorship_info: str = "EdomiteOpenAIProcess using OpenAI GPT models."


class GeezGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "geez1241"
    description: str = "Default process for OpenAI for the Geez language."
    authorship_info: str = "GeezOpenAIProcess using OpenAI GPT models."


class GothicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "goth1244"
    description: str = "Default process for OpenAI for the Gothic language."
    authorship_info: str = "GothicOpenAIProcess using OpenAI GPT models."


class GujaratiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "guja1252"
    description: str = "Default process for OpenAI for the Gujarati language."
    authorship_info: str = "GujaratiOpenAIProcess using OpenAI GPT models."


class HindiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "hind1269"
    description: str = "Default process for OpenAI for the Hindi language."
    authorship_info: str = "HindiOpenAIProcess using OpenAI GPT models."


class KhariBoliGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "khad1239"
    description: str = "Default process for OpenAI for the Khari Boli dialect of Hindi."
    authorship_info: str = "KhariBoliOpenAIProcess using OpenAI GPT models."


class BrajGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "braj1242"
    description: str = "Default process for OpenAI for the Braj Bhasha language."
    authorship_info: str = "BrajOpenAIProcess using OpenAI GPT models."


class AwadhiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "awad1243"
    description: str = "Default process for OpenAI for the Awadhi language."
    authorship_info: str = "AwadhiOpenAIProcess using OpenAI GPT models."


class HittiteGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "hitt1242"
    description: str = "Default process for OpenAI for the Hittite language."
    authorship_info: str = "HittiteOpenAIProcess using OpenAI GPT models."


class KhotaneseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "khot1251"
    description: str = "Default process for OpenAI for the Khotanese language."
    authorship_info: str = "KhotaneseOpenAIProcess using OpenAI GPT models."


class TumshuqeseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "tums1237"
    description: str = "Default process for OpenAI for the Tumshuqese language."
    authorship_info: str = "TumshuqeseOpenAIProcess using OpenAI GPT models."


class LateEgyptianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "late1256"
    description: str = "Default process for OpenAI for the Late Egyptian language."
    authorship_info: str = "Late Egyptian OpenAIProcess using OpenAI GPT models."


class LatinGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "lati1261"
    description: str = "Default process for OpenAI for the Latin language."
    authorship_info: str = "LatinOpenAIProcess using OpenAI GPT models."


class LiteraryChineseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "lite1248"
    description: str = "Default process for OpenAI for the Literary Chinese language."
    authorship_info: str = "Literary ChineseOpenAIProcess using OpenAI GPT models."


class LycianAGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "lyci1241"
    description: str = "Default process for OpenAI for the Lycian A language."
    authorship_info: str = "Lycian AOpenAIProcess using OpenAI GPT models."


class LydianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "lydi1241"
    description: str = "Default process for OpenAI for the Lydian language."
    authorship_info: str = "LydianOpenAIProcess using OpenAI GPT models."


class MaharastriPrakritGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "maha1305"
    description: str = "Default process for OpenAI for the Maharastri Prakrit language."
    authorship_info: str = "MaharastriPrakritOpenAIProcess using OpenAI GPT models."


class MiddleArmenianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1364"
    description: str = "Default process for OpenAI for the Middle Armenian language."
    authorship_info: str = "Middle ArmenianOpenAIProcess using OpenAI GPT models."


class MiddleBretonGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldb1244"
    description: str = "Default process for OpenAI for the Middle Breton language."
    authorship_info: str = "Middle BretonOpenAIProcess using OpenAI GPT models."


class MiddleChineseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1344"
    description: str = "Default process for OpenAI for the Middle Chinese language."
    authorship_info: str = "Middle ChineseOpenAIProcess using OpenAI GPT models."


class MiddleCornishGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "corn1251"
    description: str = "Default process for OpenAI for the Middle Cornish language."
    authorship_info: str = "Middle CornishOpenAIProcess using OpenAI GPT models."


class MiddleEgyptianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1369"
    description: str = "Default process for OpenAI for the Middle Egyptian language."
    authorship_info: str = "Middle Egyptian OpenAIProcess using OpenAI GPT models."


class MiddleEnglishGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1317"
    description: str = "Default process for OpenAI for the Middle English language."
    authorship_info: str = "Middle EnglishOpenAIProcess using OpenAI GPT models."


class MiddleFrenchGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1316"
    description: str = "Default process for OpenAI for the Middle French language."
    authorship_info: str = "Middle FrenchOpenAIProcess using OpenAI GPT models."


class MiddleHighGermanGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1343"
    description: str = "Default process for OpenAI for the Middle High German language."
    authorship_info: str = "Middle High GermanOpenAIProcess using OpenAI GPT models."


class MiddleMongolGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "mong1329"
    description: str = "Default process for OpenAI for the Middle Mongol language."
    authorship_info: str = "Middle MongolOpenAIProcess using OpenAI GPT models."


class MoabiteGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "moab1234"
    description: str = "Default process for OpenAI for the Moabite language."
    authorship_info: str = "MoabiteOpenAIProcess using OpenAI GPT models."


class OdiaGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oriy1255"
    description: str = "Default process for OpenAI for the Odia language."
    authorship_info: str = "OdiaOpenAIProcess using OpenAI GPT models."


class OfficialAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "impe1235"
    description: str = (
        "Default process for OpenAI for the Official Aramaic (700-300 BCE) language."
    )
    authorship_info: str = (
        "Official Aramaic (700-300 BCE) OpenAIProcess using OpenAI GPT models."
    )


class OldBurmeseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldb1235"
    description: str = "Default process for OpenAI for the Old Burmese language."
    authorship_info: str = "Old BurmeseOpenAIProcess using OpenAI GPT models."


class OldChineseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldc1244"
    description: str = "Default process for OpenAI for the Old Chinese language."
    authorship_info: str = "Old ChineseOpenAIProcess using OpenAI GPT models."


class BaihuaChineseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1255"
    description: str = (
        "Default process for OpenAI for Early Vernacular Chinese (Baihua)."
    )
    authorship_info: str = "BaihuaChineseOpenAIProcess using OpenAI GPT models."


class ClassicalBurmeseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "nucl1310"
    description: str = "Default process for OpenAI for the Classical Burmese language."
    authorship_info: str = "ClassicalBurmeseOpenAIProcess using OpenAI GPT models."


class TangutGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "tang1334"
    description: str = "Default process for OpenAI for the Tangut (Xixia) language."
    authorship_info: str = "TangutOpenAIProcess using OpenAI GPT models."


class NewarGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "newa1246"
    description: str = (
        "Default process for OpenAI for the Newar (Classical Nepal Bhasa) language."
    )
    authorship_info: str = "NewarOpenAIProcess using OpenAI GPT models."


class MeiteiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "mani1292"
    description: str = (
        "Default process for OpenAI for the Meitei (Classical Manipuri) language."
    )
    authorship_info: str = "MeiteiOpenAIProcess using OpenAI GPT models."


class SgawKarenGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "sgaw1245"
    description: str = "Default process for OpenAI for the Sgaw Karen language."
    authorship_info: str = "SgawKarenOpenAIProcess using OpenAI GPT models."


class MogholiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "mogh1245"
    description: str = "Default process for OpenAI for the Mogholi (Moghol) language."
    authorship_info: str = "MogholiOpenAIProcess using OpenAI GPT models."


class NumidianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "numi1241"
    description: str = (
        "Default process for OpenAI for the Numidian (Ancient Berber) language."
    )
    authorship_info: str = "NumidianOpenAIProcess using OpenAI GPT models."


class TaitaGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "tait1247"
    description: str = "Default process for OpenAI for the Cushitic Taita language."
    authorship_info: str = "TaitaOpenAIProcess using OpenAI GPT models."


class HausaGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "haus1257"
    description: str = "Default process for OpenAI for the Hausa language."
    authorship_info: str = "HausaOpenAIProcess using OpenAI GPT models."


class OldJurchenGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "jurc1239"
    description: str = "Default process for OpenAI for the Old Jurchen language."
    authorship_info: str = "OldJurchenOpenAIProcess using OpenAI GPT models."


class OldJapaneseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "japo1237"
    description: str = "Default process for OpenAI for the Old Japanese language."
    authorship_info: str = "OldJapaneseOpenAIProcess using OpenAI GPT models."


class OldHungarianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldh1242"
    description: str = "Default process for OpenAI for the Old Hungarian language."
    authorship_info: str = "OldHungarianOpenAIProcess using OpenAI GPT models."


class ChagataiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "chag1247"
    description: str = "Default process for OpenAI for the Chagatai language."
    authorship_info: str = "ChagataiOpenAIProcess using OpenAI GPT models."


class OldTurkicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldu1238"
    description: str = "Default process for OpenAI for the Old Turkic language."
    authorship_info: str = "OldTurkicOpenAIProcess using OpenAI GPT models."


class OldTamilGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldt1248"
    description: str = "Default process for OpenAI for the Old Tamil language."
    authorship_info: str = "OldTamilOpenAIProcess using OpenAI GPT models."


class AmmoniteGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "ammo1234"
    description: str = "Default process for OpenAI for the Ammonite language."
    authorship_info: str = "AmmoniteOpenAIProcess using OpenAI GPT models."


class OldAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "olda1246"
    description: str = (
        "Default process for OpenAI for the Old Aramaic (up to 700 BCE) language."
    )
    authorship_info: str = "OldAramaicOpenAIProcess using OpenAI GPT models."


class OldAramaicSamalianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "olda1245"
    description: str = (
        "Default process for OpenAI for the Old Aramaic–Samʾalian language."
    )
    authorship_info: str = "OldAramaicSamalianOpenAIProcess using OpenAI GPT models."


class MiddleAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1366"
    description: str = "Default process for OpenAI for the Middle Aramaic language."
    authorship_info: str = "MiddleAramaicOpenAIProcess using OpenAI GPT models."


class HatranGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "hatr1234"
    description: str = "Default process for OpenAI for the Hatran language."
    authorship_info: str = "HatranOpenAIProcess using OpenAI GPT models."


class JewishBabylonianAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "jewi1240"
    description: str = (
        "Default process for OpenAI for the Jewish Babylonian Aramaic language."
    )
    authorship_info: str = (
        "JewishBabylonianAramaicOpenAIProcess using OpenAI GPT models."
    )


class SamalianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "sama1234"
    description: str = "Default process for OpenAI for the Samʾalian language."
    authorship_info: str = "SamalianOpenAIProcess using OpenAI GPT models."


class OldEgyptianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "olde1242"
    description: str = "Default process for OpenAI for the Old Egyptian language."
    authorship_info: str = "Old Egyptian OpenAIProcess using OpenAI GPT models."


class OldEnglishGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "olde1238"
    description: str = (
        "Default process for OpenAI for the Old English (ca. 450-1100) language."
    )
    authorship_info: str = (
        "Old English (ca. 450-1100)OpenAIProcess using OpenAI GPT models."
    )


class OldFrenchGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldf1239"
    description: str = (
        "Default process for OpenAI for the Old French (842-ca. 1400) language."
    )
    authorship_info: str = (
        "Old French (842-ca. 1400)OpenAIProcess using OpenAI GPT models."
    )


class OldHighGermanGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldh1241"
    description: str = (
        "Default process for OpenAI for the Old High German (ca. 750-1050) language."
    )
    authorship_info: str = (
        "Old High German (ca. 750-1050)OpenAIProcess using OpenAI GPT models."
    )


class EarlyIrishGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldi1245"
    description: str = "Default process for OpenAI for the Old Irish language."
    authorship_info: str = "Old IrishOpenAIProcess using OpenAI GPT models."


class MarathiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "mara1378"
    description: str = "Default process for OpenAI for the Marathi language."
    authorship_info: str = "MarathiOpenAIProcess using OpenAI GPT models."


class OldNorseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldn1244"
    description: str = "Default process for OpenAI for the Old Norse language."
    authorship_info: str = "Old NorseOpenAIProcess using OpenAI GPT models."


class OldPersianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldp1254"
    description: str = (
        "Default process for OpenAI for the Old Persian (ca. 600-400 B.C.) language."
    )
    authorship_info: str = (
        "Old Persian (ca. 600-400 B.C.)OpenAIProcess using OpenAI GPT models."
    )


class OldMiddleWelshGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldw1239"
    description: str = "Default process for OpenAI for the Old-Middle Welsh language."
    authorship_info: str = "Old-Middle WelshOpenAIProcess using OpenAI GPT models."


class ParthianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "part1239"
    description: str = "Default process for OpenAI for the Parthian language."
    authorship_info: str = "ParthianOpenAIProcess using OpenAI GPT models."


class MiddlePersianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "pahl1241"
    description: str = "Default process for OpenAI for the Middle Persian language."
    authorship_info: str = "MiddlePersianOpenAIProcess using OpenAI GPT models."


class PalaicGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "pala1331"
    description: str = "Default process for OpenAI for the Palaic language."
    authorship_info: str = "PalaicOpenAIProcess using OpenAI GPT models."


class PaliGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "pali1273"
    description: str = "Default process for OpenAI for the Pali language."
    authorship_info: str = "PaliOpenAIProcess using OpenAI GPT models."


class PhoenicianGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "phoe1239"
    description: str = "Default process for OpenAI for the Phoenician language."
    authorship_info: str = "PhoenicianOpenAIProcess using OpenAI GPT models."


class PunjabiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default process for OpenAI for the Punjabi language."
    authorship_info: str = "PunjabiOpenAIProcess using OpenAI GPT models."


class AssameseGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "assa1263"
    description: str = "Default process for OpenAI for the Assamese language."
    authorship_info: str = "AssameseOpenAIProcess using OpenAI GPT models."


class SinhalaGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "sinh1246"
    description: str = "Default process for OpenAI for the Sinhala language."
    authorship_info: str = "SinhalaOpenAIProcess using OpenAI GPT models."


class SindhiGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "sind1272"
    description: str = "Default process for OpenAI for the Sindhi language."
    authorship_info: str = "SindhiOpenAIProcess using OpenAI GPT models."


class KashmiriGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "kash1277"
    description: str = "Default process for OpenAI for the Kashmiri language."
    authorship_info: str = "KashmiriOpenAIProcess using OpenAI GPT models."


class BagriGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "bagr1243"
    description: str = "Default process for OpenAI for the Bagri (Rajasthani) language."
    authorship_info: str = "BagriOpenAIProcess using OpenAI GPT models."


class ClassicalSanskritGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1258"
    description: str = "Default process for OpenAI for the Classical Sanskrit language."
    authorship_info: str = "ClassicalSanskritOpenAIProcess using OpenAI GPT models."


class VedicSanskritGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "vedi1234"
    description: str = "Default process for OpenAI for the Vedic Sanskrit language."
    authorship_info: str = "VedicSanskritOpenAIProcess using OpenAI GPT models."


class TokharianAGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "toch1238"
    description: str = "Default process for OpenAI for the Tokharian A language."
    authorship_info: str = "Tokharian AOpenAIProcess using OpenAI GPT models."


class TokharianBGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "toch1237"
    description: str = "Default process for OpenAI for the Tokharian B language."
    authorship_info: str = "Tokharian BOpenAIProcess using OpenAI GPT models."


class UgariticGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "ugar1238"
    description: str = "Default process for OpenAI for the Ugaritic language."
    authorship_info: str = "UgariticOpenAIProcess using OpenAI GPT models."


class UrduGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "urdu1245"
    description: str = "Default process for OpenAI for the Urdu language."
    authorship_info: str = "UrduOpenAIProcess using OpenAI GPT models."


class SauraseniPrakritGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "saur1252"
    description: str = "Default process for OpenAI for the Sauraseni Prakrit language."
    authorship_info: str = "SauraseniPrakritOpenAIProcess using OpenAI GPT models."


class MagadhiPrakritGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "maga1260"
    description: str = "Default process for OpenAI for the Magadhi Prakrit language."
    authorship_info: str = "MagadhiPrakritOpenAIProcess using OpenAI GPT models."


class GandhariGenAIDependencyProcess(GenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "gand1259"
    description: str = "Default process for OpenAI for the Gandhari language."
    authorship_info: str = "GandhariOpenAIProcess using OpenAI GPT models."
