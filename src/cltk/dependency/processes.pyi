"""Type stubs for dynamically generated dependency processes."""

from collections.abc import Callable
from typing import ClassVar, Optional

from cltk.core.data_types import Doc, Process
from cltk.genai.prompts import PromptInfo

PromptBuilder = Callable[[str, str], PromptInfo] | PromptInfo | str

class DependencyProcess(Process):
    def run(self, input_doc: Doc) -> Doc: ...

class GenAIDependencyProcess(DependencyProcess):
    process_id: ClassVar[str]
    prompt_builder_from_tokens: Optional[PromptBuilder]
    prompt_builder_from_text: Optional[PromptBuilder]
    prompt_profile: Optional[str]
    prompt_version: Optional[str]
    def run(self, input_doc: Doc) -> Doc: ...

class AkkadianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AlbanianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AmmoniteGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AncientGreekGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AssameseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AvestanGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AwadhiGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BactrianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BagriGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BaihuaChineseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BengaliGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BiblicalHebrewGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BrajGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class CarianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ChagataiGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ChurchSlavicGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalArabicGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalArmenianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalBurmeseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalMandaicGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalMongolianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalSanskritGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalSyriacGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalTibetanGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class CopticGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class CuneiformLuwianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class DemoticGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class EarlyIrishGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class EasternPanjabiGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class EdomiteGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class GandhariGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class GeezGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class GothicGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class GujaratiGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class HatranGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class HausaGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class HieroglyphicLuwianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class HindiGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class HittiteGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class JewishBabylonianAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class KashmiriGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class KhariBoliGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class KhotaneseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LateEgyptianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LatinGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LatvianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LiteraryChineseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LithuanianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LycianAGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LydianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MagadhiPrakritGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MaharastriPrakritGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MarathiGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MeiteiGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleArmenianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleBretonGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleChineseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleCornishGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleEgyptianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleEnglishGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleFrenchGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleHighGermanGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleMongolGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddlePersianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MoabiteGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MogholiGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class NewarGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class NumidianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OdiaGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OfficialAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldAramaicGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldAramaicSamalianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldBurmeseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldChineseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldEgyptianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldEnglishGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldFrenchGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldHighGermanGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldHungarianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldJapaneseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldJurchenGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldMiddleWelshGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldNorseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldPersianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldPrussianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldTamilGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldTurkicGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class PalaicGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class PaliGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ParthianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class PhoenicianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class PunjabiGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SamalianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SauraseniPrakritGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SgawKarenGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SindhiGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SinhalaGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SogdianGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class TaitaGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class TangutGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class TokharianAGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class TokharianBGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class TumshuqeseGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class UgariticGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class UrduGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class VedicSanskritGenAIDependencyProcess(GenAIDependencyProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

