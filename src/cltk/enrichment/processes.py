"""Process for GenAI-driven enrichment (glosses, IPA, idioms, pedagogy)."""

from collections.abc import Callable
from copy import copy
from functools import cached_property
from typing import ClassVar, Optional

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import IPA_PRONUNCIATION_MODE, Doc, Process
from cltk.core.logging_utils import bind_from_doc
from cltk.core.process_registry import register_process
from cltk.enrichment.utils import generate_gpt_enrichment_concurrent
from cltk.genai.prompt_registry import (
    PromptProfileRegistry,
    PromptTemplate,
    build_prompt_info,
)
from cltk.genai.prompts import PromptInfo

# Prompt override type: callable, PromptInfo, or literal string.
# Callable receives (lang_or_dialect_name, token_table, ipa_mode)
EnrichmentPromptBuilder = (
    Callable[[str, str, IPA_PRONUNCIATION_MODE], PromptInfo] | PromptInfo | str
)


@register_process
class GenAIEnrichmentProcess(Process):
    """Language-agnostic enrichment process using a generative GPT model (legacy)."""

    process_id: ClassVar[str] = "enrichment.genai"
    enrichment_fields: ClassVar[Optional[set[str]]] = None
    prompt_template_id: ClassVar[Optional[str]] = None
    prompt_builder: Optional[EnrichmentPromptBuilder] = None
    ipa_mode: IPA_PRONUNCIATION_MODE = "attic_5c_bce"
    prompt_profile: Optional[str] = None
    prompt_version: Optional[str] = None

    @cached_property
    def algorithm(self) -> Callable[..., Doc]:
        """Return the enrichment generation function for this process."""
        if not self.glottolog_id:
            msg = "glottolog_id must be set for EnrichmentProcess"
            bind_context(glottolog_id=self.glottolog_id).error(msg)
            raise ValueError(msg)
        return generate_gpt_enrichment_concurrent

    def run(self, input_doc: Doc) -> Doc:
        """Run the configured GPT enrichment workflow."""
        output_doc: Doc = copy(input_doc)
        if not output_doc.normalized_text:
            msg = "Doc must have `normalized_text`."
            bind_from_doc(output_doc).error(msg)
            raise ValueError(msg)
        if self.glottolog_id is None:
            raise ValueError("glottolog_id must be set for enrichment.")
        prompt_builder = self.prompt_builder
        prompt_digest = None
        if prompt_builder is None and self.prompt_profile:
            template_id = self.prompt_template_id or self.process_id
            template = PromptProfileRegistry.get_prompt(
                self.prompt_profile, template_id, self.prompt_version
            )
            prompt_digest = template.digest

            def _builder(
                lang: str,
                table: str,
                ipa_mode: IPA_PRONUNCIATION_MODE,
                _template: PromptTemplate = template,
            ) -> PromptInfo:
                """Build prompt info from template and parameters."""
                return build_prompt_info(
                    _template,
                    lang_or_dialect_name=lang,
                    token_table=table,
                    ipa_mode=ipa_mode,
                )

            prompt_builder = _builder
        output_doc = self.algorithm(
            output_doc,
            ipa_mode=self.ipa_mode,
            prompt_builder=prompt_builder,
            prompt_profile=self.prompt_profile,
            prompt_digest=prompt_digest,
            fields=self.enrichment_fields,
            provenance_process=f"{self.process_id}:{self.__class__.__name__}",
        )
        return output_doc


@register_process
class LexiconEnrichmentProcess(GenAIEnrichmentProcess):
    """Lexicon-focused enrichment step (glosses, lemma translations)."""

    process_id: ClassVar[str] = "enrichment.lexicon"
    enrichment_fields: ClassVar[set[str]] = {"lexicon"}
    prompt_template_id: ClassVar[str] = "enrichment.genai"
    source: Optional[str] = None


@register_process
class PhonologyEnrichmentProcess(GenAIEnrichmentProcess):
    """Phonology-focused enrichment step (IPA and orthography)."""

    process_id: ClassVar[str] = "enrichment.phonology"
    enrichment_fields: ClassVar[set[str]] = {"phonology"}
    prompt_template_id: ClassVar[str] = "enrichment.genai"
    mode: Optional[str] = None


@register_process
class IdiomsEnrichmentProcess(GenAIEnrichmentProcess):
    """Idiom/MWE-focused enrichment step."""

    process_id: ClassVar[str] = "enrichment.idioms"
    enrichment_fields: ClassVar[set[str]] = {"idioms"}
    prompt_template_id: ClassVar[str] = "enrichment.genai"


@register_process
class PedagogyEnrichmentProcess(GenAIEnrichmentProcess):
    """Pedagogy-focused enrichment step (learner-facing notes)."""

    process_id: ClassVar[str] = "enrichment.pedagogy"
    enrichment_fields: ClassVar[set[str]] = {"pedagogy"}
    prompt_template_id: ClassVar[str] = "enrichment.genai"


class CuneiformLuwianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "cune1239"
    description: str = "Default textual enrichment process using a generative GPT model for the Cuneiform Luwian language."
    authorship_info: str = "CLTK"


class HieroglyphicLuwianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "hier1240"
    description: str = "Default textual enrichment process using a generative GPT model for the Hieroglyphic Luwian language."
    authorship_info: str = "CLTK"


class OldPrussianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "prus1238"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Prussian language."
    authorship_info: str = "CLTK"


class LithuanianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "lith1251"
    description: str = "Default textual enrichment process using a generative GPT model for the Lithuanian language."
    authorship_info: str = "CLTK"


class LatvianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "latv1249"
    description: str = "Default textual enrichment process using a generative GPT model for the Latvian language."
    authorship_info: str = "CLTK"


class AlbanianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "gheg1238"
    description: str = "Default textual enrichment process using a generative GPT model for the Albanian language."
    authorship_info: str = "CLTK"


class AkkadianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "akka1240"
    description: str = "Default textual enrichment process using a generative GPT model for the Akkadian language."
    authorship_info: str = "CLTK"


class AncientGreekGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "anci1242"
    description: str = "Default textual enrichment process using a generative GPT model for the Ancient Greek language."
    authorship_info: str = "CLTK"


class BiblicalHebrewGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "anci1244"
    description: str = "Default textual enrichment process using a generative GPT model for the Biblical Hebrew language."
    authorship_info: str = "CLTK"


class ClassicalArabicGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1259"
    description: str = "Default textual enrichment process using a generative GPT model for the Classical Arabic language."
    authorship_info: str = "CLTK"


class AvestanGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "aves1237"
    description: str = "Default textual enrichment process using a generative GPT model for the Avestan language."
    authorship_info: str = "CLTK"


class BactrianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "bact1239"
    description: str = "Default textual enrichment process using a generative GPT model for the Bactrian language."
    authorship_info: str = "CLTK"


class SogdianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "sogd1245"
    description: str = "Default textual enrichment process using a generative GPT model for the Sogdian language."
    authorship_info: str = "CLTK"


class BengaliGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "beng1280"
    description: str = "Default textual enrichment process using a generative GPT model for the Bengali language."
    authorship_info: str = "CLTK"


class CarianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "cari1274"
    description: str = "Default textual enrichment process using a generative GPT model for the Carian language."
    authorship_info: str = "CLTK"


class ChurchSlavicGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "chur1257"
    description: str = "Default textual enrichment process using a generative GPT model for the Church Slavic language."
    authorship_info: str = "CLTK"


class ClassicalArmenianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1256"
    description: str = "Default textual enrichment process using a generative GPT model for the Classical Armenian language."
    authorship_info: str = "CLTK"


class ClassicalMandaicGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1253"
    description: str = "Default textual enrichment process using a generative GPT model for the Classical Mandaic language."
    authorship_info: str = "CLTK"


class ClassicalMongolianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "mong1331"
    description: str = "Default textual enrichment process using a generative GPT model for the Classical Mongolian language."
    authorship_info: str = "CLTK"


class ClassicalSyriacGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1252"
    description: str = "Default textual enrichment process using a generative GPT model for the Classical Syriac language."
    authorship_info: str = "CLTK"


class ClassicalTibetanGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1254"
    description: str = "Default textual enrichment process using a generative GPT model for the Classical Tibetan language."
    authorship_info: str = "CLTK"


class CopticGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "copt1239"
    description: str = "Default textual enrichment process using a generative GPT model for the Coptic language."
    authorship_info: str = "CLTK"


class DemoticGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "demo1234"
    description: str = "Default textual enrichment process using a generative GPT model for the Demotic language."
    authorship_info: str = "CLTK"


class EasternPanjabiGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default textual enrichment process using a generative GPT model for the Eastern Panjabi language."
    authorship_info: str = "CLTK"


class EdomiteGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "edom1234"
    description: str = "Default textual enrichment process using a generative GPT model for the Edomite language."
    authorship_info: str = "CLTK"


class GeezGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "geez1241"
    description: str = "Default textual enrichment process using a generative GPT model for the Geez language."
    authorship_info: str = "CLTK"


class GothicGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "goth1244"
    description: str = "Default textual enrichment process using a generative GPT model for the Gothic language."
    authorship_info: str = "CLTK"


class GujaratiGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "guja1252"
    description: str = "Default textual enrichment process using a generative GPT model for the Gujarati language."
    authorship_info: str = "CLTK"


class HindiGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "hind1269"
    description: str = "Default textual enrichment process using a generative GPT model for the Hindi language."
    authorship_info: str = "CLTK"


class KhariBoliGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "khad1239"
    description: str = "Default textual enrichment process using a generative GPT model for the Khari Boli dialect of Hindi."
    authorship_info: str = "CLTK"


class BrajGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "braj1242"
    description: str = "Default textual enrichment process using a generative GPT model for the Braj Bhasha language."
    authorship_info: str = "CLTK"


class AwadhiGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "awad1243"
    description: str = "Default textual enrichment process using a generative GPT model for the Awadhi language."
    authorship_info: str = "CLTK"


class HittiteGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "hitt1242"
    description: str = "Default textual enrichment process using a generative GPT model for the Hittite language."
    authorship_info: str = "CLTK"


class KhotaneseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "khot1251"
    description: str = "Default textual enrichment process using a generative GPT model for the Khotanese language."
    authorship_info: str = "CLTK"


class TumshuqeseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "tums1237"
    description: str = "Default textual enrichment process using a generative GPT model for the Tumshuqese language."
    authorship_info: str = "CLTK"


class LateEgyptianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "late1256"
    description: str = "Default textual enrichment process using a generative GPT model for the Late Egyptian language."
    authorship_info: str = "CLTK"


class LatinGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "lati1261"
    description: str = "Default textual enrichment process using a generative GPT model for the Latin language."
    authorship_info: str = "CLTK"


class LiteraryChineseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "lite1248"
    description: str = "Default textual enrichment process using a generative GPT model for the Literary Chinese language."
    authorship_info: str = "CLTK"


class LycianAGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "lyci1241"
    description: str = "Default textual enrichment process using a generative GPT model for the Lycian A language."
    authorship_info: str = "CLTK"


class LydianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "lydi1241"
    description: str = "Default textual enrichment process using a generative GPT model for the Lydian language."
    authorship_info: str = "CLTK"


class MaharastriPrakritGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "maha1305"
    description: str = "Default textual enrichment process using a generative GPT model for the Maharastri Prakrit language."
    authorship_info: str = "CLTK"


class MiddleArmenianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1364"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle Armenian language."
    authorship_info: str = "CLTK"


class MiddleBretonGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldb1244"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle Breton language."
    authorship_info: str = "CLTK"


class MiddleChineseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1344"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle Chinese language."
    authorship_info: str = "CLTK"


class MiddleCornishGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "corn1251"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle Cornish language."
    authorship_info: str = "CLTK"


class MiddleEgyptianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1369"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle Egyptian language."
    authorship_info: str = "CLTK"


class MiddleEnglishGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1317"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle English language."
    authorship_info: str = "CLTK"


class MiddleFrenchGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1316"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle French language."
    authorship_info: str = "CLTK"


class MiddleHighGermanGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1343"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle High German language."
    authorship_info: str = "CLTK"


class MiddleMongolGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "mong1329"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle Mongol language."
    authorship_info: str = "CLTK"


class MoabiteGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "moab1234"
    description: str = "Default textual enrichment process using a generative GPT model for the Moabite language."
    authorship_info: str = "CLTK"


class OdiaGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oriy1255"
    description: str = "Default textual enrichment process using a generative GPT model for the Odia language."
    authorship_info: str = "CLTK"


class OfficialAramaicGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "impe1235"
    description: str = "Default textual enrichment process using a generative GPT model for the Official Aramaic (700-300 BCE) language."
    authorship_info: str = "CLTK"


class OldBurmeseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldb1235"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Burmese language."
    authorship_info: str = "CLTK"


class OldChineseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldc1244"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Chinese language."
    authorship_info: str = "CLTK"


class BaihuaChineseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1255"
    description: str = "Default textual enrichment process using a generative GPT model for Early Vernacular Chinese (Baihua)."
    authorship_info: str = "CLTK"


class ClassicalBurmeseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "nucl1310"
    description: str = "Default textual enrichment process using a generative GPT model for the Classical Burmese language."
    authorship_info: str = "CLTK"


class TangutGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "tang1334"
    description: str = "Default textual enrichment process using a generative GPT model for the Tangut (Xixia) language."
    authorship_info: str = "CLTK"


class NewarGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "newa1246"
    description: str = "Default textual enrichment process using a generative GPT model for the Newar (Classical Nepal Bhasa) language."
    authorship_info: str = "CLTK"


class MeiteiGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "mani1292"
    description: str = "Default textual enrichment process using a generative GPT model for the Meitei (Classical Manipuri) language."
    authorship_info: str = "CLTK"


class SgawKarenGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "sgaw1245"
    description: str = "Default textual enrichment process using a generative GPT model for the Sgaw Karen language."
    authorship_info: str = "CLTK"


class MogholiGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "mogh1245"
    description: str = "Default textual enrichment process using a generative GPT model for the Mogholi (Moghol) language."
    authorship_info: str = "CLTK"


class NumidianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "numi1241"
    description: str = "Default textual enrichment process using a generative GPT model for the Numidian (Ancient Berber) language."
    authorship_info: str = "CLTK"


class TaitaGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "tait1247"
    description: str = "Default textual enrichment process using a generative GPT model for the Cushitic Taita language."
    authorship_info: str = "CLTK"


class HausaGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "haus1257"
    description: str = "Default textual enrichment process using a generative GPT model for the Hausa language."
    authorship_info: str = "CLTK"


class OldJurchenGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "jurc1239"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Jurchen language."
    authorship_info: str = "CLTK"


class OldJapaneseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "japo1237"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Japanese language."
    authorship_info: str = "CLTK"


class OldHungarianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldh1242"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Hungarian language."
    authorship_info: str = "CLTK"


class ChagataiGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "chag1247"
    description: str = "Default textual enrichment process using a generative GPT model for the Chagatai language."
    authorship_info: str = "CLTK"


class OldTurkicGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldu1238"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Turkic language."
    authorship_info: str = "CLTK"


class OldTamilGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldt1248"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Tamil language."
    authorship_info: str = "CLTK"


class AmmoniteGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "ammo1234"
    description: str = "Default textual enrichment process using a generative GPT model for the Ammonite language."
    authorship_info: str = "CLTK"


class OldAramaicGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "olda1246"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Aramaic (up to 700 BCE) language."
    authorship_info: str = "CLTK"


class OldAramaicSamalianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "olda1245"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Aramaic–Samʾalian language."
    authorship_info: str = "CLTK"


class MiddleAramaicGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "midd1366"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle Aramaic language."
    authorship_info: str = "CLTK"


class HatranGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "hatr1234"
    description: str = "Default textual enrichment process using a generative GPT model for the Hatran language."
    authorship_info: str = "CLTK"


class JewishBabylonianAramaicGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "jewi1240"
    description: str = "Default textual enrichment process using a generative GPT model for the Jewish Babylonian Aramaic language."
    authorship_info: str = "CLTK"


class SamalianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "sama1234"
    description: str = "Default textual enrichment process using a generative GPT model for the Samʾalian language."
    authorship_info: str = "CLTK"


class OldEgyptianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "olde1242"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Egyptian language."
    authorship_info: str = "CLTK"


class OldEnglishGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "olde1238"
    description: str = "Default textual enrichment process using a generative GPT model for the Old English (ca. 450-1100) language."
    authorship_info: str = "CLTK"


class OldFrenchGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldf1239"
    description: str = "Default textual enrichment process using a generative GPT model for the Old French (842-ca. 1400) language."
    authorship_info: str = "CLTK"


class OldHighGermanGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldh1241"
    description: str = "Default textual enrichment process using a generative GPT model for the Old High German (ca. 750-1050) language."
    authorship_info: str = "CLTK"


class EarlyIrishGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldi1245"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Irish language."
    authorship_info: str = "CLTK"


class MarathiGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "mara1378"
    description: str = "Default textual enrichment process using a generative GPT model for the Marathi language."
    authorship_info: str = "CLTK"


class OldNorseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldn1244"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Norse language."
    authorship_info: str = "CLTK"


class OldPersianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldp1254"
    description: str = "Default textual enrichment process using a generative GPT model for the Old Persian (ca. 600-400 B.C.) language."
    authorship_info: str = "CLTK"


class OldMiddleWelshGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "oldw1239"
    description: str = "Default textual enrichment process using a generative GPT model for the Old-Middle Welsh language."
    authorship_info: str = "CLTK"


class ParthianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "part1239"
    description: str = "Default textual enrichment process using a generative GPT model for the Parthian language."
    authorship_info: str = "CLTK"


class MiddlePersianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "pahl1241"
    description: str = "Default textual enrichment process using a generative GPT model for the Middle Persian language."
    authorship_info: str = "CLTK"


class PalaicGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "pala1331"
    description: str = "Default textual enrichment process using a generative GPT model for the Palaic language."
    authorship_info: str = "CLTK"


class PaliGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "pali1273"
    description: str = "Default textual enrichment process using a generative GPT model for the Pali language."
    authorship_info: str = "CLTK"


class PhoenicianGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "phoe1239"
    description: str = "Default textual enrichment process using a generative GPT model for the Phoenician language."
    authorship_info: str = "CLTK"


class PunjabiGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default textual enrichment process using a generative GPT model for the Punjabi language."
    authorship_info: str = "CLTK"


class AssameseGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "assa1263"
    description: str = "Default textual enrichment process using a generative GPT model for the Assamese language."
    authorship_info: str = "CLTK"


class SinhalaGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "sinh1246"
    description: str = "Default textual enrichment process using a generative GPT model for the Sinhala language."
    authorship_info: str = "CLTK"


class SindhiGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "sind1272"
    description: str = "Default textual enrichment process using a generative GPT model for the Sindhi language."
    authorship_info: str = "CLTK"


class KashmiriGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "kash1277"
    description: str = "Default textual enrichment process using a generative GPT model for the Kashmiri language."
    authorship_info: str = "CLTK"


class BagriGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "bagr1243"
    description: str = "Default textual enrichment process using a generative GPT model for the Bagri (Rajasthani) language."
    authorship_info: str = "CLTK"


class ClassicalSanskritGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "clas1258"
    description: str = "Default textual enrichment process using a generative GPT model for the Classical Sanskrit language."
    authorship_info: str = "CLTK"


class VedicSanskritGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "vedi1234"
    description: str = "Default textual enrichment process using a generative GPT model for the Vedic Sanskrit language."
    authorship_info: str = "CLTK"


class TokharianAGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "toch1238"
    description: str = "Default textual enrichment process using a generative GPT model for the Tokharian A language."
    authorship_info: str = "CLTK"


class TokharianBGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "toch1237"
    description: str = "Default textual enrichment process using a generative GPT model for the Tokharian B language."
    authorship_info: str = "CLTK"


class UgariticGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "ugar1238"
    description: str = "Default textual enrichment process using a generative GPT model for the Ugaritic language."
    authorship_info: str = "CLTK"


class UrduGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "urdu1245"
    description: str = "Default textual enrichment process using a generative GPT model for the Urdu language."
    authorship_info: str = "CLTK"


class SauraseniPrakritGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "saur1252"
    description: str = "Default textual enrichment process using a generative GPT model for the Sauraseni Prakrit language."
    authorship_info: str = "CLTK"


class MagadhiPrakritGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "maga1260"
    description: str = "Default textual enrichment process using a generative GPT model for the Magadhi Prakrit language."
    authorship_info: str = "CLTK"


class GandhariGenAIEnrichmentProcess(GenAIEnrichmentProcess):
    """Language-specific dependency process using a generative GPT model."""

    glottolog_id: Optional[str] = "gand1259"
    description: str = "Default textual enrichment process using a generative GPT model for the Gandhari language."
    authorship_info: str = "CLTK"
