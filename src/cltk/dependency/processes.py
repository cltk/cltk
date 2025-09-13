"""Processes of POS and feature tagging."""

from collections.abc import Callable
from copy import copy
from functools import cached_property
from typing import Optional

from cltk.core.cltk_logger import logger
from cltk.core.data_types import Doc, Process
from cltk.dependency.utils import (
    generate_gpt_dependency_concurrent,
)


class DependencyProcess(Process):
    """Base class for morphosyntactic processes."""


class ChatGPTDependencyProcess(DependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    @cached_property
    def algorithm(self) -> Callable[[Doc], Doc]:
        if not self.glottolog_id:
            msg: str = "glottolog_id must be set for DependencyProcess"
            logger.error(msg)
            raise ValueError(msg)
        # Prefer the safe concurrent wrapper (async under the hood, sync surface)
        return generate_gpt_dependency_concurrent

    def run(self, input_doc: Doc) -> Doc:
        output_doc = copy(input_doc)
        if not output_doc.normalized_text:
            msg: str = "Doc must have `normalized_text`."
            logger.error(msg)
            raise ValueError(msg)
        # Ensure required attributes are present
        if self.glottolog_id is None:
            raise ValueError("glottolog_id must be set for sentence splitting")
        # Callable typing does not retain keyword names; pass positionally
        output_doc = self.algorithm(
            output_doc,
        )
        return output_doc


class CuneiformLuwianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "cune1239"
    description: str = "Default process for ChatGPT for the Cuneiform Luwian language."
    authorship_info: str = "CuneiformLuwianChatGPTProcess using OpenAI GPT models."


class HieroglyphicLuwianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "hier1240"
    description: str = (
        "Default process for ChatGPT for the Hieroglyphic Luwian language."
    )
    authorship_info: str = "HieroglyphicLuwianChatGPTProcess using OpenAI GPT models."


class OldPrussianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "prus1238"
    description: str = "Default process for ChatGPT for the Old Prussian language."
    authorship_info: str = "OldPrussianChatGPTProcess using OpenAI GPT models."


class LithuanianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "lith1251"
    description: str = "Default process for ChatGPT for the Lithuanian language."
    authorship_info: str = "LithuanianChatGPTProcess using OpenAI GPT models."


class LatvianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "latv1249"
    description: str = "Default process for ChatGPT for the Latvian language."
    authorship_info: str = "LatvianChatGPTProcess using OpenAI GPT models."


class AlbanianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "gheg1238"
    description: str = "Default process for ChatGPT for the Albanian language."
    authorship_info: str = "AlbanianChatGPTProcess using OpenAI GPT models."


class AkkadianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "akka1240"
    description: str = "Default process for ChatGPT for the Akkadian language."
    authorship_info: str = "AkkadianChatGPTProcess using OpenAI GPT models."


class AncientGreekChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "anci1242"
    description: str = "Default process for ChatGPT for the Ancient Greek language."
    authorship_info: str = "Ancient GreekChatGPTProcess using OpenAI GPT models."


class BiblicalHebrewChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "anci1244"
    description: str = "Default process for ChatGPT for the Biblical Hebrew language."
    authorship_info: str = "Biblical HebrewChatGPTProcess using OpenAI GPT models."


class ClassicalArabicChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "clas1259"
    description: str = "Default process for ChatGPT for the Classical Arabic language."
    authorship_info: str = "ClassicalArabicChatGPTProcess using OpenAI GPT models."


class AvestanChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "aves1237"
    description: str = "Default process for ChatGPT for the Avestan language."
    authorship_info: str = "AvestanChatGPTProcess using OpenAI GPT models."


class BactrianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "bact1239"
    description: str = "Default process for ChatGPT for the Bactrian language."
    authorship_info: str = "BactrianChatGPTProcess using OpenAI GPT models."


class SogdianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "sogd1245"
    description: str = "Default process for ChatGPT for the Sogdian language."
    authorship_info: str = "SogdianChatGPTProcess using OpenAI GPT models."


class BengaliChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "beng1280"
    description: str = "Default process for ChatGPT for the Bengali language."
    authorship_info: str = "BengaliChatGPTProcess using OpenAI GPT models."


class CarianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "cari1274"
    description: str = "Default process for ChatGPT for the Carian language."
    authorship_info: str = "CarianChatGPTProcess using OpenAI GPT models."


class ChurchSlavicChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "chur1257"
    description: str = "Default process for ChatGPT for the Church Slavic language."
    authorship_info: str = "Church SlavicChatGPTProcess using OpenAI GPT models."


class ClassicalArmenianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "clas1256"
    description: str = (
        "Default process for ChatGPT for the Classical Armenian language."
    )
    authorship_info: str = "Classical ArmenianChatGPTProcess using OpenAI GPT models."


class ClassicalMandaicChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "clas1253"
    description: str = "Default process for ChatGPT for the Classical Mandaic language."
    authorship_info: str = "Classical MandaicChatGPTProcess using OpenAI GPT models."


class ClassicalMongolianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "mong1331"
    description: str = (
        "Default process for ChatGPT for the Classical Mongolian language."
    )
    authorship_info: str = "Classical MongolianChatGPTProcess using OpenAI GPT models."


class ClassicalSyriacChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "clas1252"
    description: str = "Default process for ChatGPT for the Classical Syriac language."
    authorship_info: str = "Classical SyriacChatGPTProcess using OpenAI GPT models."


class ClassicalTibetanChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "clas1254"
    description: str = "Default process for ChatGPT for the Classical Tibetan language."
    authorship_info: str = "Classical TibetanChatGPTProcess using OpenAI GPT models."


class CopticChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "copt1239"
    description: str = "Default process for ChatGPT for the Coptic language."
    authorship_info: str = "CopticChatGPTProcess using OpenAI GPT models."


class DemoticChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "demo1234"
    description: str = "Default process for ChatGPT for the Demotic language."
    authorship_info: str = "DemoticChatGPTProcess using OpenAI GPT models."


class EasternPanjabiChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default process for ChatGPT for the Eastern Panjabi language."
    authorship_info: str = "Eastern PanjabiChatGPTProcess using OpenAI GPT models."


class EdomiteChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "edom1234"
    description: str = "Default process for ChatGPT for the Edomite language."
    authorship_info: str = "EdomiteChatGPTProcess using OpenAI GPT models."


class GeezChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "geez1241"
    description: str = "Default process for ChatGPT for the Geez language."
    authorship_info: str = "GeezChatGPTProcess using OpenAI GPT models."


class GothicChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "goth1244"
    description: str = "Default process for ChatGPT for the Gothic language."
    authorship_info: str = "GothicChatGPTProcess using OpenAI GPT models."


class GujaratiChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "guja1252"
    description: str = "Default process for ChatGPT for the Gujarati language."
    authorship_info: str = "GujaratiChatGPTProcess using OpenAI GPT models."


class HindiChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "hind1269"
    description: str = "Default process for ChatGPT for the Hindi language."
    authorship_info: str = "HindiChatGPTProcess using OpenAI GPT models."


class KhariBoliChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "khad1239"
    description: str = (
        "Default process for ChatGPT for the Khari Boli dialect of Hindi."
    )
    authorship_info: str = "KhariBoliChatGPTProcess using OpenAI GPT models."


class BrajChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "braj1242"
    description: str = "Default process for ChatGPT for the Braj Bhasha language."
    authorship_info: str = "BrajChatGPTProcess using OpenAI GPT models."


class AwadhiChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "awad1243"
    description: str = "Default process for ChatGPT for the Awadhi language."
    authorship_info: str = "AwadhiChatGPTProcess using OpenAI GPT models."


class HittiteChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "hitt1242"
    description: str = "Default process for ChatGPT for the Hittite language."
    authorship_info: str = "HittiteChatGPTProcess using OpenAI GPT models."


class KhotaneseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "khot1251"
    description: str = "Default process for ChatGPT for the Khotanese language."
    authorship_info: str = "KhotaneseChatGPTProcess using OpenAI GPT models."


class TumshuqeseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "tums1237"
    description: str = "Default process for ChatGPT for the Tumshuqese language."
    authorship_info: str = "TumshuqeseChatGPTProcess using OpenAI GPT models."


class LateEgyptianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "late1256"
    description: str = "Default process for ChatGPT for the Late Egyptian language."
    authorship_info: str = "Late Egyptian ChatGPTProcess using OpenAI GPT models."


class LatinChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "lati1261"
    description: str = "Default process for ChatGPT for the Latin language."
    authorship_info: str = "LatinChatGPTProcess using OpenAI GPT models."


class LiteraryChineseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "lite1248"
    description: str = "Default process for ChatGPT for the Literary Chinese language."
    authorship_info: str = "Literary ChineseChatGPTProcess using OpenAI GPT models."


class LycianAChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "lyci1241"
    description: str = "Default process for ChatGPT for the Lycian A language."
    authorship_info: str = "Lycian AChatGPTProcess using OpenAI GPT models."


class LydianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "lydi1241"
    description: str = "Default process for ChatGPT for the Lydian language."
    authorship_info: str = "LydianChatGPTProcess using OpenAI GPT models."


class MaharastriPrakritChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "maha1305"
    description: str = (
        "Default process for ChatGPT for the Maharastri Prakrit language."
    )
    authorship_info: str = "MaharastriPrakritChatGPTProcess using OpenAI GPT models."


class MiddleArmenianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "midd1364"
    description: str = "Default process for ChatGPT for the Middle Armenian language."
    authorship_info: str = "Middle ArmenianChatGPTProcess using OpenAI GPT models."


class MiddleBretonChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldb1244"
    description: str = "Default process for ChatGPT for the Middle Breton language."
    authorship_info: str = "Middle BretonChatGPTProcess using OpenAI GPT models."


class MiddleChineseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "midd1344"
    description: str = "Default process for ChatGPT for the Middle Chinese language."
    authorship_info: str = "Middle ChineseChatGPTProcess using OpenAI GPT models."


class MiddleCornishChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "corn1251"
    description: str = "Default process for ChatGPT for the Middle Cornish language."
    authorship_info: str = "Middle CornishChatGPTProcess using OpenAI GPT models."


class MiddleEgyptianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "midd1369"
    description: str = "Default process for ChatGPT for the Middle Egyptian language."
    authorship_info: str = "Middle Egyptian ChatGPTProcess using OpenAI GPT models."


class MiddleEnglishChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "midd1317"
    description: str = "Default process for ChatGPT for the Middle English language."
    authorship_info: str = "Middle EnglishChatGPTProcess using OpenAI GPT models."


class MiddleFrenchChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "midd1316"
    description: str = "Default process for ChatGPT for the Middle French language."
    authorship_info: str = "Middle FrenchChatGPTProcess using OpenAI GPT models."


class MiddleHighGermanChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "midd1343"
    description: str = (
        "Default process for ChatGPT for the Middle High German language."
    )
    authorship_info: str = "Middle High GermanChatGPTProcess using OpenAI GPT models."


class MiddleMongolChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "mong1329"
    description: str = "Default process for ChatGPT for the Middle Mongol language."
    authorship_info: str = "Middle MongolChatGPTProcess using OpenAI GPT models."


class MoabiteChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "moab1234"
    description: str = "Default process for ChatGPT for the Moabite language."
    authorship_info: str = "MoabiteChatGPTProcess using OpenAI GPT models."


class OdiaChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oriy1255"
    description: str = "Default process for ChatGPT for the Odia language."
    authorship_info: str = "OdiaChatGPTProcess using OpenAI GPT models."


class OfficialAramaicChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "impe1235"
    description: str = (
        "Default process for ChatGPT for the Official Aramaic (700-300 BCE) language."
    )
    authorship_info: str = (
        "Official Aramaic (700-300 BCE) ChatGPTProcess using OpenAI GPT models."
    )


class OldBurmeseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldb1235"
    description: str = "Default process for ChatGPT for the Old Burmese language."
    authorship_info: str = "Old BurmeseChatGPTProcess using OpenAI GPT models."


class OldChineseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldc1244"
    description: str = "Default process for ChatGPT for the Old Chinese language."
    authorship_info: str = "Old ChineseChatGPTProcess using OpenAI GPT models."


class BaihuaChineseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "clas1255"
    description: str = (
        "Default process for ChatGPT for Early Vernacular Chinese (Baihua)."
    )
    authorship_info: str = "BaihuaChineseChatGPTProcess using OpenAI GPT models."


class ClassicalBurmeseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "nucl1310"
    description: str = "Default process for ChatGPT for the Classical Burmese language."
    authorship_info: str = "ClassicalBurmeseChatGPTProcess using OpenAI GPT models."


class TangutChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "tang1334"
    description: str = "Default process for ChatGPT for the Tangut (Xixia) language."
    authorship_info: str = "TangutChatGPTProcess using OpenAI GPT models."


class NewarChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "newa1246"
    description: str = (
        "Default process for ChatGPT for the Newar (Classical Nepal Bhasa) language."
    )
    authorship_info: str = "NewarChatGPTProcess using OpenAI GPT models."


class MeiteiChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "mani1292"
    description: str = (
        "Default process for ChatGPT for the Meitei (Classical Manipuri) language."
    )
    authorship_info: str = "MeiteiChatGPTProcess using OpenAI GPT models."


class SgawKarenChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "sgaw1245"
    description: str = "Default process for ChatGPT for the Sgaw Karen language."
    authorship_info: str = "SgawKarenChatGPTProcess using OpenAI GPT models."


class MogholiChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "mogh1245"
    description: str = "Default process for ChatGPT for the Mogholi (Moghol) language."
    authorship_info: str = "MogholiChatGPTProcess using OpenAI GPT models."


class NumidianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "numi1241"
    description: str = (
        "Default process for ChatGPT for the Numidian (Ancient Berber) language."
    )
    authorship_info: str = "NumidianChatGPTProcess using OpenAI GPT models."


class TaitaChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "tait1247"
    description: str = "Default process for ChatGPT for the Cushitic Taita language."
    authorship_info: str = "TaitaChatGPTProcess using OpenAI GPT models."


class HausaChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "haus1257"
    description: str = "Default process for ChatGPT for the Hausa language."
    authorship_info: str = "HausaChatGPTProcess using OpenAI GPT models."


class OldJurchenChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "jurc1239"
    description: str = "Default process for ChatGPT for the Old Jurchen language."
    authorship_info: str = "OldJurchenChatGPTProcess using OpenAI GPT models."


class OldJapaneseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "japo1237"
    description: str = "Default process for ChatGPT for the Old Japanese language."
    authorship_info: str = "OldJapaneseChatGPTProcess using OpenAI GPT models."


class OldHungarianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldh1242"
    description: str = "Default process for ChatGPT for the Old Hungarian language."
    authorship_info: str = "OldHungarianChatGPTProcess using OpenAI GPT models."


class ChagataiChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "chag1247"
    description: str = "Default process for ChatGPT for the Chagatai language."
    authorship_info: str = "ChagataiChatGPTProcess using OpenAI GPT models."


class OldTurkicChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldu1238"
    description: str = "Default process for ChatGPT for the Old Turkic language."
    authorship_info: str = "OldTurkicChatGPTProcess using OpenAI GPT models."


class OldTamilChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldt1248"
    description: str = "Default process for ChatGPT for the Old Tamil language."
    authorship_info: str = "OldTamilChatGPTProcess using OpenAI GPT models."


class AmmoniteChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "ammo1234"
    description: str = "Default process for ChatGPT for the Ammonite language."
    authorship_info: str = "AmmoniteChatGPTProcess using OpenAI GPT models."


class OldAramaicChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "olda1246"
    description: str = (
        "Default process for ChatGPT for the Old Aramaic (up to 700 BCE) language."
    )
    authorship_info: str = "OldAramaicChatGPTProcess using OpenAI GPT models."


class OldAramaicSamalianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "olda1245"
    description: str = (
        "Default process for ChatGPT for the Old Aramaic–Samʾalian language."
    )
    authorship_info: str = "OldAramaicSamalianChatGPTProcess using OpenAI GPT models."


class MiddleAramaicChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "midd1366"
    description: str = "Default process for ChatGPT for the Middle Aramaic language."
    authorship_info: str = "MiddleAramaicChatGPTProcess using OpenAI GPT models."


class HatranChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "hatr1234"
    description: str = "Default process for ChatGPT for the Hatran language."
    authorship_info: str = "HatranChatGPTProcess using OpenAI GPT models."


class JewishBabylonianAramaicChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "jewi1240"
    description: str = (
        "Default process for ChatGPT for the Jewish Babylonian Aramaic language."
    )
    authorship_info: str = (
        "JewishBabylonianAramaicChatGPTProcess using OpenAI GPT models."
    )


class SamalianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "sama1234"
    description: str = "Default process for ChatGPT for the Samʾalian language."
    authorship_info: str = "SamalianChatGPTProcess using OpenAI GPT models."


class OldEgyptianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "olde1242"
    description: str = "Default process for ChatGPT for the Old Egyptian language."
    authorship_info: str = "Old Egyptian ChatGPTProcess using OpenAI GPT models."


class OldEnglishChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "olde1238"
    description: str = (
        "Default process for ChatGPT for the Old English (ca. 450-1100) language."
    )
    authorship_info: str = (
        "Old English (ca. 450-1100)ChatGPTProcess using OpenAI GPT models."
    )


class OldFrenchChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldf1239"
    description: str = (
        "Default process for ChatGPT for the Old French (842-ca. 1400) language."
    )
    authorship_info: str = (
        "Old French (842-ca. 1400)ChatGPTProcess using OpenAI GPT models."
    )


class OldHighGermanChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldh1241"
    description: str = (
        "Default process for ChatGPT for the Old High German (ca. 750-1050) language."
    )
    authorship_info: str = (
        "Old High German (ca. 750-1050)ChatGPTProcess using OpenAI GPT models."
    )


class EarlyIrishChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldi1245"
    description: str = "Default process for ChatGPT for the Old Irish language."
    authorship_info: str = "Old IrishChatGPTProcess using OpenAI GPT models."


class MarathiChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "mara1378"
    description: str = "Default process for ChatGPT for the Marathi language."
    authorship_info: str = "MarathiChatGPTProcess using OpenAI GPT models."


class OldNorseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldn1244"
    description: str = "Default process for ChatGPT for the Old Norse language."
    authorship_info: str = "Old NorseChatGPTProcess using OpenAI GPT models."


class OldPersianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldp1254"
    description: str = (
        "Default process for ChatGPT for the Old Persian (ca. 600-400 B.C.) language."
    )
    authorship_info: str = (
        "Old Persian (ca. 600-400 B.C.)ChatGPTProcess using OpenAI GPT models."
    )


class OldMiddleWelshChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "oldw1239"
    description: str = "Default process for ChatGPT for the Old-Middle Welsh language."
    authorship_info: str = "Old-Middle WelshChatGPTProcess using OpenAI GPT models."


class ParthianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "part1239"
    description: str = "Default process for ChatGPT for the Parthian language."
    authorship_info: str = "ParthianChatGPTProcess using OpenAI GPT models."


class MiddlePersianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "pahl1241"
    description: str = "Default process for ChatGPT for the Middle Persian language."
    authorship_info: str = "MiddlePersianChatGPTProcess using OpenAI GPT models."


class PalaicChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "pala1331"
    description: str = "Default process for ChatGPT for the Palaic language."
    authorship_info: str = "PalaicChatGPTProcess using OpenAI GPT models."


class PaliChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "pali1273"
    description: str = "Default process for ChatGPT for the Pali language."
    authorship_info: str = "PaliChatGPTProcess using OpenAI GPT models."


class PhoenicianChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "phoe1239"
    description: str = "Default process for ChatGPT for the Phoenician language."
    authorship_info: str = "PhoenicianChatGPTProcess using OpenAI GPT models."


class PunjabiChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default process for ChatGPT for the Punjabi language."
    authorship_info: str = "PunjabiChatGPTProcess using OpenAI GPT models."


class AssameseChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "assa1263"
    description: str = "Default process for ChatGPT for the Assamese language."
    authorship_info: str = "AssameseChatGPTProcess using OpenAI GPT models."


class SinhalaChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "sinh1246"
    description: str = "Default process for ChatGPT for the Sinhala language."
    authorship_info: str = "SinhalaChatGPTProcess using OpenAI GPT models."


class SindhiChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "sind1272"
    description: str = "Default process for ChatGPT for the Sindhi language."
    authorship_info: str = "SindhiChatGPTProcess using OpenAI GPT models."


class KashmiriChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "kash1277"
    description: str = "Default process for ChatGPT for the Kashmiri language."
    authorship_info: str = "KashmiriChatGPTProcess using OpenAI GPT models."


class BagriChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "bagr1243"
    description: str = (
        "Default process for ChatGPT for the Bagri (Rajasthani) language."
    )
    authorship_info: str = "BagriChatGPTProcess using OpenAI GPT models."


class ClassicalSanskritChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "clas1258"
    description: str = (
        "Default process for ChatGPT for the Classical Sanskrit language."
    )
    authorship_info: str = "ClassicalSanskritChatGPTProcess using OpenAI GPT models."


class VedicSanskritChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "vedi1234"
    description: str = "Default process for ChatGPT for the Vedic Sanskrit language."
    authorship_info: str = "VedicSanskritChatGPTProcess using OpenAI GPT models."


class TokharianAChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "toch1238"
    description: str = "Default process for ChatGPT for the Tokharian A language."
    authorship_info: str = "Tokharian AChatGPTProcess using OpenAI GPT models."


class TokharianBChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "toch1237"
    description: str = "Default process for ChatGPT for the Tokharian B language."
    authorship_info: str = "Tokharian BChatGPTProcess using OpenAI GPT models."


class UgariticChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "ugar1238"
    description: str = "Default process for ChatGPT for the Ugaritic language."
    authorship_info: str = "UgariticChatGPTProcess using OpenAI GPT models."


class UrduChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "urdu1245"
    description: str = "Default process for ChatGPT for the Urdu language."
    authorship_info: str = "UrduChatGPTProcess using OpenAI GPT models."


class SauraseniPrakritChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "saur1252"
    description: str = "Default process for ChatGPT for the Sauraseni Prakrit language."
    authorship_info: str = "SauraseniPrakritChatGPTProcess using OpenAI GPT models."


class MagadhiPrakritChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "maga1260"
    description: str = "Default process for ChatGPT for the Magadhi Prakrit language."
    authorship_info: str = "MagadhiPrakritChatGPTProcess using OpenAI GPT models."


class GandhariChatGPTDependencyProcess(ChatGPTDependencyProcess):
    """Language-specific dependency process using ChatGPT."""

    glottolog_id: Optional[str] = "gand1259"
    description: str = "Default process for ChatGPT for the Gandhari language."
    authorship_info: str = "GandhariChatGPTProcess using OpenAI GPT models."
