"""Process for GenAI-driven translation."""

from collections.abc import Callable
from copy import copy
from functools import cached_property
from typing import Optional

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import Doc, Process
from cltk.core.logging_utils import bind_from_doc
from cltk.translation.utils import (
    TranslationPromptBuilder,
    generate_gpt_translation_concurrent,
)


class GenAITranslationProcess(Process):
    """Language-agnostic translation process using a generative GPT model."""

    prompt_builder: Optional[TranslationPromptBuilder] = None
    target_language: str = "Modern US English"
    target_language_id: Optional[str] = "en-US"

    @cached_property
    def algorithm(self) -> Callable[..., Doc]:
        """Return the translation generation function for this process."""
        if not self.glottolog_id:
            msg = "glottolog_id must be set for TranslationProcess"
            bind_context(glottolog_id=self.glottolog_id).error(msg)
            raise ValueError(msg)
        return generate_gpt_translation_concurrent

    def run(self, input_doc: Doc) -> Doc:
        """Run the configured GPT translation workflow."""
        output_doc: Doc = copy(input_doc)
        if not output_doc.words:
            msg = "Doc must have `words` with prior annotations before translation."
            bind_from_doc(output_doc).error(msg)
            raise ValueError(msg)
        target_language = self.target_language
        target_language_id = self.target_language_id
        try:
            meta = output_doc.metadata
            if isinstance(meta, dict):
                target_language = meta.get(
                    "translation_target_language", target_language
                )
                target_language_id = meta.get(
                    "translation_target_language_id", target_language_id
                )
        except Exception:
            pass
        output_doc = self.algorithm(
            output_doc,
            target_language=target_language,
            target_language_id=target_language_id,
            prompt_builder=self.prompt_builder,
            provenance_process=self.__class__.__name__,
        )
        return output_doc


class CuneiformLuwianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "cune1239"
    description: str = "Default textual translation process using a generative GPT model for the Cuneiform Luwian language."
    authorship_info: str = "CLTK"


class HieroglyphicLuwianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "hier1240"
    description: str = "Default textual translation process using a generative GPT model for the Hieroglyphic Luwian language."
    authorship_info: str = "CLTK"


class OldPrussianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "prus1238"
    description: str = "Default textual translation process using a generative GPT model for the Old Prussian language."
    authorship_info: str = "CLTK"


class LithuanianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "lith1251"
    description: str = "Default textual translation process using a generative GPT model for the Lithuanian language."
    authorship_info: str = "CLTK"


class LatvianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "latv1249"
    description: str = "Default textual translation process using a generative GPT model for the Latvian language."
    authorship_info: str = "CLTK"


class AlbanianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "gheg1238"
    description: str = "Default textual translation process using a generative GPT model for the Albanian language."
    authorship_info: str = "CLTK"


class AkkadianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "akka1240"
    description: str = "Default textual translation process using a generative GPT model for the Akkadian language."
    authorship_info: str = "CLTK"


class AncientGreekGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "anci1242"
    description: str = "Default textual translation process using a generative GPT model for the Ancient Greek language."
    authorship_info: str = "CLTK"


class BiblicalHebrewGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "anci1244"
    description: str = "Default textual translation process using a generative GPT model for the Biblical Hebrew language."
    authorship_info: str = "CLTK"


class ClassicalArabicGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1259"
    description: str = "Default textual translation process using a generative GPT model for the Classical Arabic language."
    authorship_info: str = "CLTK"


class AvestanGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "aves1237"
    description: str = "Default textual translation process using a generative GPT model for the Avestan language."
    authorship_info: str = "CLTK"


class BactrianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "bact1239"
    description: str = "Default textual translation process using a generative GPT model for the Bactrian language."
    authorship_info: str = "CLTK"


class SogdianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "sogd1245"
    description: str = "Default textual translation process using a generative GPT model for the Sogdian language."
    authorship_info: str = "CLTK"


class BengaliGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "beng1280"
    description: str = "Default textual translation process using a generative GPT model for the Bengali language."
    authorship_info: str = "CLTK"


class CarianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "cari1274"
    description: str = "Default textual translation process using a generative GPT model for the Carian language."
    authorship_info: str = "CLTK"


class ChurchSlavicGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "chur1257"
    description: str = "Default textual translation process using a generative GPT model for the Church Slavic language."
    authorship_info: str = "CLTK"


class ClassicalArmenianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1256"
    description: str = "Default textual translation process using a generative GPT model for the Classical Armenian language."
    authorship_info: str = "CLTK"


class ClassicalMandaicGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1253"
    description: str = "Default textual translation process using a generative GPT model for the Classical Mandaic language."
    authorship_info: str = "CLTK"


class ClassicalMongolianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "mong1331"
    description: str = "Default textual translation process using a generative GPT model for the Classical Mongolian language."
    authorship_info: str = "CLTK"


class ClassicalSyriacGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1252"
    description: str = "Default textual translation process using a generative GPT model for the Classical Syriac language."
    authorship_info: str = "CLTK"


class ClassicalTibetanGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1254"
    description: str = "Default textual translation process using a generative GPT model for the Classical Tibetan language."
    authorship_info: str = "CLTK"


class CopticGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "copt1239"
    description: str = "Default textual translation process using a generative GPT model for the Coptic language."
    authorship_info: str = "CLTK"


class DemoticGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "demo1234"
    description: str = "Default textual translation process using a generative GPT model for the Demotic language."
    authorship_info: str = "CLTK"


class EasternPanjabiGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default textual translation process using a generative GPT model for the Eastern Panjabi language."
    authorship_info: str = "CLTK"


class EdomiteGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "edom1234"
    description: str = "Default textual translation process using a generative GPT model for the Edomite language."
    authorship_info: str = "CLTK"


class GeezGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "geez1241"
    description: str = "Default textual translation process using a generative GPT model for the Geez language."
    authorship_info: str = "CLTK"


class GothicGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "goth1244"
    description: str = "Default textual translation process using a generative GPT model for the Gothic language."
    authorship_info: str = "CLTK"


class GujaratiGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "guja1252"
    description: str = "Default textual translation process using a generative GPT model for the Gujarati language."
    authorship_info: str = "CLTK"


class HindiGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "hind1269"
    description: str = "Default textual translation process using a generative GPT model for the Hindi language."
    authorship_info: str = "CLTK"


class KhariBoliGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "khad1239"
    description: str = "Default textual translation process using a generative GPT model for the Khari Boli dialect of Hindi."
    authorship_info: str = "CLTK"


class BrajGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "braj1242"
    description: str = "Default textual translation process using a generative GPT model for the Braj Bhasha language."
    authorship_info: str = "CLTK"


class AwadhiGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "awad1243"
    description: str = "Default textual translation process using a generative GPT model for the Awadhi language."
    authorship_info: str = "CLTK"


class HittiteGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "hitt1242"
    description: str = "Default textual translation process using a generative GPT model for the Hittite language."
    authorship_info: str = "CLTK"


class KhotaneseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "khot1251"
    description: str = "Default textual translation process using a generative GPT model for the Khotanese language."
    authorship_info: str = "CLTK"


class TumshuqeseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "tums1237"
    description: str = "Default textual translation process using a generative GPT model for the Tumshuqese language."
    authorship_info: str = "CLTK"


class LateEgyptianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "late1256"
    description: str = "Default textual translation process using a generative GPT model for the Late Egyptian language."
    authorship_info: str = "CLTK"


class LatinGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "lati1261"
    description: str = "Default textual translation process using a generative GPT model for the Latin language."
    authorship_info: str = "CLTK"


class LiteraryChineseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "lite1248"
    description: str = "Default textual translation process using a generative GPT model for the Literary Chinese language."
    authorship_info: str = "CLTK"


class LycianAGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "lyci1241"
    description: str = "Default textual translation process using a generative GPT model for the Lycian A language."
    authorship_info: str = "CLTK"


class LydianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "lydi1241"
    description: str = "Default textual translation process using a generative GPT model for the Lydian language."
    authorship_info: str = "CLTK"


class MaharastriPrakritGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "maha1305"
    description: str = "Default textual translation process using a generative GPT model for the Maharastri Prakrit language."
    authorship_info: str = "CLTK"


class MiddleArmenianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1364"
    description: str = "Default textual translation process using a generative GPT model for the Middle Armenian language."
    authorship_info: str = "CLTK"


class MiddleBretonGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldb1244"
    description: str = "Default textual translation process using a generative GPT model for the Middle Breton language."
    authorship_info: str = "CLTK"


class MiddleChineseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1344"
    description: str = "Default textual translation process using a generative GPT model for the Middle Chinese language."
    authorship_info: str = "CLTK"


class MiddleCornishGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "corn1251"
    description: str = "Default textual translation process using a generative GPT model for the Middle Cornish language."
    authorship_info: str = "CLTK"


class MiddleEgyptianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1369"
    description: str = "Default textual translation process using a generative GPT model for the Middle Egyptian language."
    authorship_info: str = "CLTK"


class MiddleEnglishGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1317"
    description: str = "Default textual translation process using a generative GPT model for the Middle English language."
    authorship_info: str = "CLTK"


class MiddleFrenchGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1316"
    description: str = "Default textual translation process using a generative GPT model for the Middle French language."
    authorship_info: str = "CLTK"


class MiddleHighGermanGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1343"
    description: str = "Default textual translation process using a generative GPT model for the Middle High German language."
    authorship_info: str = "CLTK"


class MiddleMongolGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "mong1329"
    description: str = "Default textual translation process using a generative GPT model for the Middle Mongol language."
    authorship_info: str = "CLTK"


class MoabiteGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "moab1234"
    description: str = "Default textual translation process using a generative GPT model for the Moabite language."
    authorship_info: str = "CLTK"


class OdiaGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oriy1255"
    description: str = "Default textual translation process using a generative GPT model for the Odia language."
    authorship_info: str = "CLTK"


class OfficialAramaicGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "impe1235"
    description: str = "Default textual translation process using a generative GPT model for the Official Aramaic (700-300 BCE) language."
    authorship_info: str = "CLTK"


class OldBurmeseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldb1235"
    description: str = "Default textual translation process using a generative GPT model for the Old Burmese language."
    authorship_info: str = "CLTK"


class OldChineseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldc1244"
    description: str = "Default textual translation process using a generative GPT model for the Old Chinese language."
    authorship_info: str = "CLTK"


class BaihuaChineseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1255"
    description: str = "Default textual translation process using a generative GPT model for Early Vernacular Chinese (Baihua)."
    authorship_info: str = "CLTK"


class ClassicalBurmeseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "nucl1310"
    description: str = "Default textual translation process using a generative GPT model for the Classical Burmese language."
    authorship_info: str = "CLTK"


class TangutGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "tang1334"
    description: str = "Default textual translation process using a generative GPT model for the Tangut (Xixia) language."
    authorship_info: str = "CLTK"


class NewarGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "newa1246"
    description: str = "Default textual translation process using a generative GPT model for the Newar (Classical Nepal Bhasa) language."
    authorship_info: str = "CLTK"


class MeiteiGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "mani1292"
    description: str = "Default textual translation process using a generative GPT model for the Meitei (Classical Manipuri) language."
    authorship_info: str = "CLTK"


class SgawKarenGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "sgaw1245"
    description: str = "Default textual translation process using a generative GPT model for the Sgaw Karen language."
    authorship_info: str = "CLTK"


class MogholiGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "mogh1245"
    description: str = "Default textual translation process using a generative GPT model for the Mogholi (Moghol) language."
    authorship_info: str = "CLTK"


class NumidianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "numi1241"
    description: str = "Default textual translation process using a generative GPT model for the Numidian (Ancient Berber) language."
    authorship_info: str = "CLTK"


class TaitaGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "tait1247"
    description: str = "Default textual translation process using a generative GPT model for the Cushitic Taita language."
    authorship_info: str = "CLTK"


class HausaGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "haus1257"
    description: str = "Default textual translation process using a generative GPT model for the Hausa language."
    authorship_info: str = "CLTK"


class OldJurchenGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "jurc1239"
    description: str = "Default textual translation process using a generative GPT model for the Old Jurchen language."
    authorship_info: str = "CLTK"


class OldJapaneseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "japo1237"
    description: str = "Default textual translation process using a generative GPT model for the Old Japanese language."
    authorship_info: str = "CLTK"


class OldHungarianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldh1242"
    description: str = "Default textual translation process using a generative GPT model for the Old Hungarian language."
    authorship_info: str = "CLTK"


class ChagataiGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "chag1247"
    description: str = "Default textual translation process using a generative GPT model for the Chagatai language."
    authorship_info: str = "CLTK"


class OldTurkicGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldu1238"
    description: str = "Default textual translation process using a generative GPT model for the Old Turkic language."
    authorship_info: str = "CLTK"


class OldTamilGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldt1248"
    description: str = "Default textual translation process using a generative GPT model for the Old Tamil language."
    authorship_info: str = "CLTK"


class AmmoniteGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "ammo1234"
    description: str = "Default textual translation process using a generative GPT model for the Ammonite language."
    authorship_info: str = "CLTK"


class OldAramaicGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "olda1246"
    description: str = "Default textual translation process using a generative GPT model for the Old Aramaic (up to 700 BCE) language."
    authorship_info: str = "CLTK"


class OldAramaicSamalianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "olda1245"
    description: str = "Default textual translation process using a generative GPT model for the Old Aramaic–Samʾalian language."
    authorship_info: str = "CLTK"


class MiddleAramaicGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1366"
    description: str = "Default textual translation process using a generative GPT model for the Middle Aramaic language."
    authorship_info: str = "CLTK"


class HatranGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "hatr1234"
    description: str = "Default textual translation process using a generative GPT model for the Hatran language."
    authorship_info: str = "CLTK"


class JewishBabylonianAramaicGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "jewi1240"
    description: str = "Default textual translation process using a generative GPT model for the Jewish Babylonian Aramaic language."
    authorship_info: str = "CLTK"


class SamalianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "sama1234"
    description: str = "Default textual translation process using a generative GPT model for the Samʾalian language."
    authorship_info: str = "CLTK"


class OldEgyptianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "olde1242"
    description: str = "Default textual translation process using a generative GPT model for the Old Egyptian language."
    authorship_info: str = "CLTK"


class OldEnglishGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "olde1238"
    description: str = "Default textual translation process using a generative GPT model for the Old English (ca. 450-1100) language."
    authorship_info: str = "CLTK"


class OldFrenchGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldf1239"
    description: str = "Default textual translation process using a generative GPT model for the Old French (842-ca. 1400) language."
    authorship_info: str = "CLTK"


class OldHighGermanGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldh1241"
    description: str = "Default textual translation process using a generative GPT model for the Old High German (ca. 750-1050) language."
    authorship_info: str = "CLTK"


class EarlyIrishGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldi1245"
    description: str = "Default textual translation process using a generative GPT model for the Old Irish language."
    authorship_info: str = "CLTK"


class MarathiGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "mara1378"
    description: str = "Default textual translation process using a generative GPT model for the Marathi language."
    authorship_info: str = "CLTK"


class OldNorseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldn1244"
    description: str = "Default textual translation process using a generative GPT model for the Old Norse language."
    authorship_info: str = "CLTK"


class OldPersianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldp1254"
    description: str = "Default textual translation process using a generative GPT model for the Old Persian (ca. 600-400 B.C.) language."
    authorship_info: str = "CLTK"


class OldMiddleWelshGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldw1239"
    description: str = "Default textual translation process using a generative GPT model for the Old-Middle Welsh language."
    authorship_info: str = "CLTK"


class ParthianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "part1239"
    description: str = "Default textual translation process using a generative GPT model for the Parthian language."
    authorship_info: str = "CLTK"


class MiddlePersianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "pahl1241"
    description: str = "Default textual translation process using a generative GPT model for the Middle Persian language."
    authorship_info: str = "CLTK"


class PalaicGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "pala1331"
    description: str = "Default textual translation process using a generative GPT model for the Palaic language."
    authorship_info: str = "CLTK"


class PaliGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "pali1273"
    description: str = "Default textual translation process using a generative GPT model for the Pali language."
    authorship_info: str = "CLTK"


class PhoenicianGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "phoe1239"
    description: str = "Default textual translation process using a generative GPT model for the Phoenician language."
    authorship_info: str = "CLTK"


class AssameseGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "assa1263"
    description: str = "Default textual translation process using a generative GPT model for the Assamese language."
    authorship_info: str = "CLTK"


class SinhalaGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "sinh1246"
    description: str = "Default textual translation process using a generative GPT model for the Sinhala language."
    authorship_info: str = "CLTK"


class SindhiGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "sind1272"
    description: str = "Default textual translation process using a generative GPT model for the Sindhi language."
    authorship_info: str = "CLTK"


class KashmiriGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "kash1277"
    description: str = "Default textual translation process using a generative GPT model for the Kashmiri language."
    authorship_info: str = "CLTK"


class BagriGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "bagr1243"
    description: str = "Default textual translation process using a generative GPT model for the Bagri (Rajasthani) language."
    authorship_info: str = "CLTK"


class ClassicalSanskritGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1258"
    description: str = "Default textual translation process using a generative GPT model for the Classical Sanskrit language."
    authorship_info: str = "CLTK"


class VedicSanskritGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "vedi1234"
    description: str = "Default textual translation process using a generative GPT model for the Vedic Sanskrit language."
    authorship_info: str = "CLTK"


class TokharianAGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "toch1238"
    description: str = "Default textual translation process using a generative GPT model for the Tokharian A language."
    authorship_info: str = "CLTK"


class TokharianBGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "toch1237"
    description: str = "Default textual translation process using a generative GPT model for the Tokharian B language."
    authorship_info: str = "CLTK"


class UgariticGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "ugar1238"
    description: str = "Default textual translation process using a generative GPT model for the Ugaritic language."
    authorship_info: str = "CLTK"


class UrduGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "urdu1245"
    description: str = "Default textual translation process using a generative GPT model for the Urdu language."
    authorship_info: str = "CLTK"


class SauraseniPrakritGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "saur1252"
    description: str = "Default textual translation process using a generative GPT model for the Sauraseni Prakrit language."
    authorship_info: str = "CLTK"


class MagadhiPrakritGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "maga1260"
    description: str = "Default textual translation process using a generative GPT model for the Magadhi Prakrit language."
    authorship_info: str = "CLTK"


class GandhariGenAITranslationProcess(GenAITranslationProcess):
    """Language-specific translation process using a generative GPT model."""

    glottolog_id: Optional[str] = "gand1259"
    description: str = "Default textual translation process using a generative GPT model for the Gandhari language."
    authorship_info: str = "CLTK"
