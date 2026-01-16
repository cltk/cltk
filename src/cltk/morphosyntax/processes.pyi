"""Type stubs for dynamically generated morphosyntax processes."""

from collections.abc import Callable
from typing import ClassVar, Optional

from cltk.core.data_types import Doc, Process
from cltk.genai.prompts import PromptInfo

PromptBuilder = Callable[[str, str], PromptInfo] | PromptInfo | str

class MorphosyntaxProcess(Process):
    def run(self, input_doc: Doc) -> Doc: ...

class GenAIMorphosyntaxProcess(MorphosyntaxProcess):
    process_id: ClassVar[str]
    prompt_builder: Optional[PromptBuilder]
    prompt_profile: Optional[str]
    prompt_version: Optional[str]
    def run(self, input_doc: Doc) -> Doc: ...

class AkkadianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AlbanianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AmmoniteGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AncientGreekGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AssameseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AvestanGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class AwadhiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BactrianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BagriGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BaihuaChineseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BengaliGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BiblicalHebrewGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class BrajGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class CarianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ChagataiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ChurchSlavicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalArabicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalArmenianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalBurmeseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalMandaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalMongolianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalSanskritGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalSyriacGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ClassicalTibetanGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class CopticGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class CuneiformLuwianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class DemoticGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class EarlyIrishGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class EasternPanjabiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class EdomiteGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class GandhariGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class GeezGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class GothicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class GujaratiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class HatranGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class HausaGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class HieroglyphicLuwianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class HindiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class HittiteGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class JewishBabylonianAramaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class KashmiriGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class KhariBoliGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class KhotaneseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LateEgyptianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LatinGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LatvianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LiteraryChineseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LithuanianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LycianAGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class LydianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MagadhiPrakritGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MaharastriPrakritGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MarathiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MeiteiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleAramaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleArmenianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleBretonGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleChineseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleCornishGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleEgyptianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleEnglishGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleFrenchGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleHighGermanGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddleMongolGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MiddlePersianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MoabiteGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class MogholiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class NewarGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class NumidianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OdiaGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OfficialAramaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldAramaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldAramaicSamalianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldBurmeseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldChineseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldEgyptianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldEnglishGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldFrenchGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldHighGermanGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldHungarianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldJapaneseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldJurchenGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldMiddleWelshGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldNorseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldPersianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldPrussianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldTamilGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class OldTurkicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class PalaicGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class PaliGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class ParthianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class PhoenicianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class PunjabiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SamalianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SauraseniPrakritGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SgawKarenGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SindhiGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SinhalaGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class SogdianGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class TaitaGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class TangutGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class TokharianAGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class TokharianBGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class TumshuqeseGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class UgariticGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class UrduGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

class VedicSanskritGenAIMorphosyntaxProcess(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str]
    description: str
    authorship_info: str

