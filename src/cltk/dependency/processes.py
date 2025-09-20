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


class OpenAIDependencyProcess(DependencyProcess):
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


class CuneiformLuwianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "cune1239"
    description: str = "Default process for OpenAI for the Cuneiform Luwian language."
    authorship_info: str = "CuneiformLuwianOpenAIProcess using OpenAI GPT models."


class HieroglyphicLuwianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "hier1240"
    description: str = (
        "Default process for OpenAI for the Hieroglyphic Luwian language."
    )
    authorship_info: str = "HieroglyphicLuwianOpenAIProcess using OpenAI GPT models."


class OldPrussianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "prus1238"
    description: str = "Default process for OpenAI for the Old Prussian language."
    authorship_info: str = "OldPrussianOpenAIProcess using OpenAI GPT models."


class LithuanianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "lith1251"
    description: str = "Default process for OpenAI for the Lithuanian language."
    authorship_info: str = "LithuanianOpenAIProcess using OpenAI GPT models."


class LatvianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "latv1249"
    description: str = "Default process for OpenAI for the Latvian language."
    authorship_info: str = "LatvianOpenAIProcess using OpenAI GPT models."


class AlbanianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "gheg1238"
    description: str = "Default process for OpenAI for the Albanian language."
    authorship_info: str = "AlbanianOpenAIProcess using OpenAI GPT models."


class AkkadianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "akka1240"
    description: str = "Default process for OpenAI for the Akkadian language."
    authorship_info: str = "AkkadianOpenAIProcess using OpenAI GPT models."


class AncientGreekOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "anci1242"
    description: str = "Default process for OpenAI for the Ancient Greek language."
    authorship_info: str = "Ancient GreekOpenAIProcess using OpenAI GPT models."


class BiblicalHebrewOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "anci1244"
    description: str = "Default process for OpenAI for the Biblical Hebrew language."
    authorship_info: str = "Biblical HebrewOpenAIProcess using OpenAI GPT models."


class ClassicalArabicOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1259"
    description: str = "Default process for OpenAI for the Classical Arabic language."
    authorship_info: str = "ClassicalArabicOpenAIProcess using OpenAI GPT models."


class AvestanOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "aves1237"
    description: str = "Default process for OpenAI for the Avestan language."
    authorship_info: str = "AvestanOpenAIProcess using OpenAI GPT models."


class BactrianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "bact1239"
    description: str = "Default process for OpenAI for the Bactrian language."
    authorship_info: str = "BactrianOpenAIProcess using OpenAI GPT models."


class SogdianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "sogd1245"
    description: str = "Default process for OpenAI for the Sogdian language."
    authorship_info: str = "SogdianOpenAIProcess using OpenAI GPT models."


class BengaliOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "beng1280"
    description: str = "Default process for OpenAI for the Bengali language."
    authorship_info: str = "BengaliOpenAIProcess using OpenAI GPT models."


class CarianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "cari1274"
    description: str = "Default process for OpenAI for the Carian language."
    authorship_info: str = "CarianOpenAIProcess using OpenAI GPT models."


class ChurchSlavicOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "chur1257"
    description: str = "Default process for OpenAI for the Church Slavic language."
    authorship_info: str = "Church SlavicOpenAIProcess using OpenAI GPT models."


class ClassicalArmenianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1256"
    description: str = "Default process for OpenAI for the Classical Armenian language."
    authorship_info: str = "Classical ArmenianOpenAIProcess using OpenAI GPT models."


class ClassicalMandaicOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1253"
    description: str = "Default process for OpenAI for the Classical Mandaic language."
    authorship_info: str = "Classical MandaicOpenAIProcess using OpenAI GPT models."


class ClassicalMongolianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "mong1331"
    description: str = (
        "Default process for OpenAI for the Classical Mongolian language."
    )
    authorship_info: str = "Classical MongolianOpenAIProcess using OpenAI GPT models."


class ClassicalSyriacOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1252"
    description: str = "Default process for OpenAI for the Classical Syriac language."
    authorship_info: str = "Classical SyriacOpenAIProcess using OpenAI GPT models."


class ClassicalTibetanOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1254"
    description: str = "Default process for OpenAI for the Classical Tibetan language."
    authorship_info: str = "Classical TibetanOpenAIProcess using OpenAI GPT models."


class CopticOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "copt1239"
    description: str = "Default process for OpenAI for the Coptic language."
    authorship_info: str = "CopticOpenAIProcess using OpenAI GPT models."


class DemoticOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "demo1234"
    description: str = "Default process for OpenAI for the Demotic language."
    authorship_info: str = "DemoticOpenAIProcess using OpenAI GPT models."


class EasternPanjabiOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default process for OpenAI for the Eastern Panjabi language."
    authorship_info: str = "Eastern PanjabiOpenAIProcess using OpenAI GPT models."


class EdomiteOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "edom1234"
    description: str = "Default process for OpenAI for the Edomite language."
    authorship_info: str = "EdomiteOpenAIProcess using OpenAI GPT models."


class GeezOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "geez1241"
    description: str = "Default process for OpenAI for the Geez language."
    authorship_info: str = "GeezOpenAIProcess using OpenAI GPT models."


class GothicOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "goth1244"
    description: str = "Default process for OpenAI for the Gothic language."
    authorship_info: str = "GothicOpenAIProcess using OpenAI GPT models."


class GujaratiOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "guja1252"
    description: str = "Default process for OpenAI for the Gujarati language."
    authorship_info: str = "GujaratiOpenAIProcess using OpenAI GPT models."


class HindiOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "hind1269"
    description: str = "Default process for OpenAI for the Hindi language."
    authorship_info: str = "HindiOpenAIProcess using OpenAI GPT models."


class KhariBoliOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "khad1239"
    description: str = "Default process for OpenAI for the Khari Boli dialect of Hindi."
    authorship_info: str = "KhariBoliOpenAIProcess using OpenAI GPT models."


class BrajOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "braj1242"
    description: str = "Default process for OpenAI for the Braj Bhasha language."
    authorship_info: str = "BrajOpenAIProcess using OpenAI GPT models."


class AwadhiOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "awad1243"
    description: str = "Default process for OpenAI for the Awadhi language."
    authorship_info: str = "AwadhiOpenAIProcess using OpenAI GPT models."


class HittiteOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "hitt1242"
    description: str = "Default process for OpenAI for the Hittite language."
    authorship_info: str = "HittiteOpenAIProcess using OpenAI GPT models."


class KhotaneseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "khot1251"
    description: str = "Default process for OpenAI for the Khotanese language."
    authorship_info: str = "KhotaneseOpenAIProcess using OpenAI GPT models."


class TumshuqeseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "tums1237"
    description: str = "Default process for OpenAI for the Tumshuqese language."
    authorship_info: str = "TumshuqeseOpenAIProcess using OpenAI GPT models."


class LateEgyptianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "late1256"
    description: str = "Default process for OpenAI for the Late Egyptian language."
    authorship_info: str = "Late Egyptian OpenAIProcess using OpenAI GPT models."


class LatinOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "lati1261"
    description: str = "Default process for OpenAI for the Latin language."
    authorship_info: str = "LatinOpenAIProcess using OpenAI GPT models."


class LiteraryChineseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "lite1248"
    description: str = "Default process for OpenAI for the Literary Chinese language."
    authorship_info: str = "Literary ChineseOpenAIProcess using OpenAI GPT models."


class LycianAOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "lyci1241"
    description: str = "Default process for OpenAI for the Lycian A language."
    authorship_info: str = "Lycian AOpenAIProcess using OpenAI GPT models."


class LydianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "lydi1241"
    description: str = "Default process for OpenAI for the Lydian language."
    authorship_info: str = "LydianOpenAIProcess using OpenAI GPT models."


class MaharastriPrakritOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "maha1305"
    description: str = "Default process for OpenAI for the Maharastri Prakrit language."
    authorship_info: str = "MaharastriPrakritOpenAIProcess using OpenAI GPT models."


class MiddleArmenianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1364"
    description: str = "Default process for OpenAI for the Middle Armenian language."
    authorship_info: str = "Middle ArmenianOpenAIProcess using OpenAI GPT models."


class MiddleBretonOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldb1244"
    description: str = "Default process for OpenAI for the Middle Breton language."
    authorship_info: str = "Middle BretonOpenAIProcess using OpenAI GPT models."


class MiddleChineseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1344"
    description: str = "Default process for OpenAI for the Middle Chinese language."
    authorship_info: str = "Middle ChineseOpenAIProcess using OpenAI GPT models."


class MiddleCornishOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "corn1251"
    description: str = "Default process for OpenAI for the Middle Cornish language."
    authorship_info: str = "Middle CornishOpenAIProcess using OpenAI GPT models."


class MiddleEgyptianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1369"
    description: str = "Default process for OpenAI for the Middle Egyptian language."
    authorship_info: str = "Middle Egyptian OpenAIProcess using OpenAI GPT models."


class MiddleEnglishOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1317"
    description: str = "Default process for OpenAI for the Middle English language."
    authorship_info: str = "Middle EnglishOpenAIProcess using OpenAI GPT models."


class MiddleFrenchOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1316"
    description: str = "Default process for OpenAI for the Middle French language."
    authorship_info: str = "Middle FrenchOpenAIProcess using OpenAI GPT models."


class MiddleHighGermanOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1343"
    description: str = "Default process for OpenAI for the Middle High German language."
    authorship_info: str = "Middle High GermanOpenAIProcess using OpenAI GPT models."


class MiddleMongolOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "mong1329"
    description: str = "Default process for OpenAI for the Middle Mongol language."
    authorship_info: str = "Middle MongolOpenAIProcess using OpenAI GPT models."


class MoabiteOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "moab1234"
    description: str = "Default process for OpenAI for the Moabite language."
    authorship_info: str = "MoabiteOpenAIProcess using OpenAI GPT models."


class OdiaOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oriy1255"
    description: str = "Default process for OpenAI for the Odia language."
    authorship_info: str = "OdiaOpenAIProcess using OpenAI GPT models."


class OfficialAramaicOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "impe1235"
    description: str = (
        "Default process for OpenAI for the Official Aramaic (700-300 BCE) language."
    )
    authorship_info: str = (
        "Official Aramaic (700-300 BCE) OpenAIProcess using OpenAI GPT models."
    )


class OldBurmeseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldb1235"
    description: str = "Default process for OpenAI for the Old Burmese language."
    authorship_info: str = "Old BurmeseOpenAIProcess using OpenAI GPT models."


class OldChineseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldc1244"
    description: str = "Default process for OpenAI for the Old Chinese language."
    authorship_info: str = "Old ChineseOpenAIProcess using OpenAI GPT models."


class BaihuaChineseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1255"
    description: str = (
        "Default process for OpenAI for Early Vernacular Chinese (Baihua)."
    )
    authorship_info: str = "BaihuaChineseOpenAIProcess using OpenAI GPT models."


class ClassicalBurmeseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "nucl1310"
    description: str = "Default process for OpenAI for the Classical Burmese language."
    authorship_info: str = "ClassicalBurmeseOpenAIProcess using OpenAI GPT models."


class TangutOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "tang1334"
    description: str = "Default process for OpenAI for the Tangut (Xixia) language."
    authorship_info: str = "TangutOpenAIProcess using OpenAI GPT models."


class NewarOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "newa1246"
    description: str = (
        "Default process for OpenAI for the Newar (Classical Nepal Bhasa) language."
    )
    authorship_info: str = "NewarOpenAIProcess using OpenAI GPT models."


class MeiteiOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "mani1292"
    description: str = (
        "Default process for OpenAI for the Meitei (Classical Manipuri) language."
    )
    authorship_info: str = "MeiteiOpenAIProcess using OpenAI GPT models."


class SgawKarenOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "sgaw1245"
    description: str = "Default process for OpenAI for the Sgaw Karen language."
    authorship_info: str = "SgawKarenOpenAIProcess using OpenAI GPT models."


class MogholiOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "mogh1245"
    description: str = "Default process for OpenAI for the Mogholi (Moghol) language."
    authorship_info: str = "MogholiOpenAIProcess using OpenAI GPT models."


class NumidianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "numi1241"
    description: str = (
        "Default process for OpenAI for the Numidian (Ancient Berber) language."
    )
    authorship_info: str = "NumidianOpenAIProcess using OpenAI GPT models."


class TaitaOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "tait1247"
    description: str = "Default process for OpenAI for the Cushitic Taita language."
    authorship_info: str = "TaitaOpenAIProcess using OpenAI GPT models."


class HausaOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "haus1257"
    description: str = "Default process for OpenAI for the Hausa language."
    authorship_info: str = "HausaOpenAIProcess using OpenAI GPT models."


class OldJurchenOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "jurc1239"
    description: str = "Default process for OpenAI for the Old Jurchen language."
    authorship_info: str = "OldJurchenOpenAIProcess using OpenAI GPT models."


class OldJapaneseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "japo1237"
    description: str = "Default process for OpenAI for the Old Japanese language."
    authorship_info: str = "OldJapaneseOpenAIProcess using OpenAI GPT models."


class OldHungarianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldh1242"
    description: str = "Default process for OpenAI for the Old Hungarian language."
    authorship_info: str = "OldHungarianOpenAIProcess using OpenAI GPT models."


class ChagataiOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "chag1247"
    description: str = "Default process for OpenAI for the Chagatai language."
    authorship_info: str = "ChagataiOpenAIProcess using OpenAI GPT models."


class OldTurkicOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldu1238"
    description: str = "Default process for OpenAI for the Old Turkic language."
    authorship_info: str = "OldTurkicOpenAIProcess using OpenAI GPT models."


class OldTamilOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldt1248"
    description: str = "Default process for OpenAI for the Old Tamil language."
    authorship_info: str = "OldTamilOpenAIProcess using OpenAI GPT models."


class AmmoniteOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "ammo1234"
    description: str = "Default process for OpenAI for the Ammonite language."
    authorship_info: str = "AmmoniteOpenAIProcess using OpenAI GPT models."


class OldAramaicOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "olda1246"
    description: str = (
        "Default process for OpenAI for the Old Aramaic (up to 700 BCE) language."
    )
    authorship_info: str = "OldAramaicOpenAIProcess using OpenAI GPT models."


class OldAramaicSamalianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "olda1245"
    description: str = (
        "Default process for OpenAI for the Old Aramaic–Samʾalian language."
    )
    authorship_info: str = "OldAramaicSamalianOpenAIProcess using OpenAI GPT models."


class MiddleAramaicOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "midd1366"
    description: str = "Default process for OpenAI for the Middle Aramaic language."
    authorship_info: str = "MiddleAramaicOpenAIProcess using OpenAI GPT models."


class HatranOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "hatr1234"
    description: str = "Default process for OpenAI for the Hatran language."
    authorship_info: str = "HatranOpenAIProcess using OpenAI GPT models."


class JewishBabylonianAramaicOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "jewi1240"
    description: str = (
        "Default process for OpenAI for the Jewish Babylonian Aramaic language."
    )
    authorship_info: str = (
        "JewishBabylonianAramaicOpenAIProcess using OpenAI GPT models."
    )


class SamalianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "sama1234"
    description: str = "Default process for OpenAI for the Samʾalian language."
    authorship_info: str = "SamalianOpenAIProcess using OpenAI GPT models."


class OldEgyptianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "olde1242"
    description: str = "Default process for OpenAI for the Old Egyptian language."
    authorship_info: str = "Old Egyptian OpenAIProcess using OpenAI GPT models."


class OldEnglishOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "olde1238"
    description: str = (
        "Default process for OpenAI for the Old English (ca. 450-1100) language."
    )
    authorship_info: str = (
        "Old English (ca. 450-1100)OpenAIProcess using OpenAI GPT models."
    )


class OldFrenchOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldf1239"
    description: str = (
        "Default process for OpenAI for the Old French (842-ca. 1400) language."
    )
    authorship_info: str = (
        "Old French (842-ca. 1400)OpenAIProcess using OpenAI GPT models."
    )


class OldHighGermanOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldh1241"
    description: str = (
        "Default process for OpenAI for the Old High German (ca. 750-1050) language."
    )
    authorship_info: str = (
        "Old High German (ca. 750-1050)OpenAIProcess using OpenAI GPT models."
    )


class EarlyIrishOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldi1245"
    description: str = "Default process for OpenAI for the Old Irish language."
    authorship_info: str = "Old IrishOpenAIProcess using OpenAI GPT models."


class MarathiOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "mara1378"
    description: str = "Default process for OpenAI for the Marathi language."
    authorship_info: str = "MarathiOpenAIProcess using OpenAI GPT models."


class OldNorseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldn1244"
    description: str = "Default process for OpenAI for the Old Norse language."
    authorship_info: str = "Old NorseOpenAIProcess using OpenAI GPT models."


class OldPersianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldp1254"
    description: str = (
        "Default process for OpenAI for the Old Persian (ca. 600-400 B.C.) language."
    )
    authorship_info: str = (
        "Old Persian (ca. 600-400 B.C.)OpenAIProcess using OpenAI GPT models."
    )


class OldMiddleWelshOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "oldw1239"
    description: str = "Default process for OpenAI for the Old-Middle Welsh language."
    authorship_info: str = "Old-Middle WelshOpenAIProcess using OpenAI GPT models."


class ParthianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "part1239"
    description: str = "Default process for OpenAI for the Parthian language."
    authorship_info: str = "ParthianOpenAIProcess using OpenAI GPT models."


class MiddlePersianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "pahl1241"
    description: str = "Default process for OpenAI for the Middle Persian language."
    authorship_info: str = "MiddlePersianOpenAIProcess using OpenAI GPT models."


class PalaicOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "pala1331"
    description: str = "Default process for OpenAI for the Palaic language."
    authorship_info: str = "PalaicOpenAIProcess using OpenAI GPT models."


class PaliOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "pali1273"
    description: str = "Default process for OpenAI for the Pali language."
    authorship_info: str = "PaliOpenAIProcess using OpenAI GPT models."


class PhoenicianOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "phoe1239"
    description: str = "Default process for OpenAI for the Phoenician language."
    authorship_info: str = "PhoenicianOpenAIProcess using OpenAI GPT models."


class PunjabiOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default process for OpenAI for the Punjabi language."
    authorship_info: str = "PunjabiOpenAIProcess using OpenAI GPT models."


class AssameseOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "assa1263"
    description: str = "Default process for OpenAI for the Assamese language."
    authorship_info: str = "AssameseOpenAIProcess using OpenAI GPT models."


class SinhalaOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "sinh1246"
    description: str = "Default process for OpenAI for the Sinhala language."
    authorship_info: str = "SinhalaOpenAIProcess using OpenAI GPT models."


class SindhiOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "sind1272"
    description: str = "Default process for OpenAI for the Sindhi language."
    authorship_info: str = "SindhiOpenAIProcess using OpenAI GPT models."


class KashmiriOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "kash1277"
    description: str = "Default process for OpenAI for the Kashmiri language."
    authorship_info: str = "KashmiriOpenAIProcess using OpenAI GPT models."


class BagriOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "bagr1243"
    description: str = "Default process for OpenAI for the Bagri (Rajasthani) language."
    authorship_info: str = "BagriOpenAIProcess using OpenAI GPT models."


class ClassicalSanskritOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "clas1258"
    description: str = "Default process for OpenAI for the Classical Sanskrit language."
    authorship_info: str = "ClassicalSanskritOpenAIProcess using OpenAI GPT models."


class VedicSanskritOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "vedi1234"
    description: str = "Default process for OpenAI for the Vedic Sanskrit language."
    authorship_info: str = "VedicSanskritOpenAIProcess using OpenAI GPT models."


class TokharianAOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "toch1238"
    description: str = "Default process for OpenAI for the Tokharian A language."
    authorship_info: str = "Tokharian AOpenAIProcess using OpenAI GPT models."


class TokharianBOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "toch1237"
    description: str = "Default process for OpenAI for the Tokharian B language."
    authorship_info: str = "Tokharian BOpenAIProcess using OpenAI GPT models."


class UgariticOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "ugar1238"
    description: str = "Default process for OpenAI for the Ugaritic language."
    authorship_info: str = "UgariticOpenAIProcess using OpenAI GPT models."


class UrduOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "urdu1245"
    description: str = "Default process for OpenAI for the Urdu language."
    authorship_info: str = "UrduOpenAIProcess using OpenAI GPT models."


class SauraseniPrakritOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "saur1252"
    description: str = "Default process for OpenAI for the Sauraseni Prakrit language."
    authorship_info: str = "SauraseniPrakritOpenAIProcess using OpenAI GPT models."


class MagadhiPrakritOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "maga1260"
    description: str = "Default process for OpenAI for the Magadhi Prakrit language."
    authorship_info: str = "MagadhiPrakritOpenAIProcess using OpenAI GPT models."


class GandhariOpenAIDependencyProcess(OpenAIDependencyProcess):
    """Language-specific dependency process using OpenAI."""

    glottolog_id: Optional[str] = "gand1259"
    description: str = "Default process for OpenAI for the Gandhari language."
    authorship_info: str = "GandhariOpenAIProcess using OpenAI GPT models."
