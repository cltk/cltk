from dataclasses import dataclass, field
from typing import Optional

from cltk.core.cltk_logger import logger
from cltk.core.data_types import Doc, Process
from cltk.core.exceptions import CLTKException
from cltk.genai.chatgpt import ChatGPT
from cltk.languages.glottolog import LANGUAGES


@dataclass
class ChatGPTProcess(Process):
    """A Process type to capture everything that ChatGPT can do for a given language."""

    language: Optional[str] = None
    api_key: Optional[str] = None
    model: str = "gpt-4.1"
    temperature: float = 1.0
    description: str = "Process for ChatGPT for linguistic annotation."
    authorship_info: str = "ChatGPTProcess using OpenAI GPT models."
    chatgpt: Optional[ChatGPT] = field(init=False, default=None)

    def __post_init__(self):
        if self.language and self.api_key:
            self.chatgpt = ChatGPT(
                language=self.language,
                api_key=self.api_key,
                model=self.model,
                temperature=self.temperature,
            )
        else:
            self.chatgpt = None

    def run(self, input_doc: Doc) -> Doc:
        """Run ChatGPT inferencing and enrich the Doc with linguistic metadata."""
        if not self.chatgpt:
            raise ValueError("ChatGPTProcess requires language and api_key to be set.")
        # Use normalized_text if available, else raw
        input_text = (
            input_doc.normalized_text if input_doc.normalized_text else input_doc.raw
        )
        if not input_text:
            raise CLTKException(
                "Input document must have either normalized_text or raw text."
            )
        enriched_doc = self._enrich_doc(input_doc)
        logger.info(f"Enriched doc words: {enriched_doc.words}")
        logger.info(f"Enriched doc chatgpt: {enriched_doc.chatgpt}")
        return enriched_doc

    def _enrich_doc(self, input_doc: Doc) -> Doc:
        """Enrich the document with metadata using ChatGPT."""
        if not self.chatgpt:
            raise ValueError("ChatGPTProcess requires language and api_key to be set.")
        # Use normalized_text if available, else raw
        input_text = (
            input_doc.normalized_text if input_doc.normalized_text else input_doc.raw
        )
        if not input_text:
            raise CLTKException(
                "Input document must have either normalized_text or raw text."
            )
        enriched_doc = self.chatgpt.generate_all(input_text=input_text)
        # Only overwrite fields if not None in input_doc
        if input_doc.language is not None:
            enriched_doc.language = input_doc.language
        if input_doc.normalized_text is not None:
            enriched_doc.normalized_text = input_doc.normalized_text
        if input_doc.raw is not None:
            enriched_doc.raw = input_doc.raw
        if input_doc.pipeline is not None:
            enriched_doc.pipeline = input_doc.pipeline
        return enriched_doc


# @dataclass
# class AkkadianChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "akk"
#     description: str = "Default process for ChatGPT for the Akkadian language."
#     authorship_info: str = "AkkadianChatGPTProcess using OpenAI GPT models."


# @dataclass
# class AncientGreekChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "akk"
#     description: str = "Default process for ChatGPT for the Ancient Greek language."
#     authorship_info: str = "AncientGreekChatGPTProcess using OpenAI GPT models."


# @dataclass
# class OldEnglishChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "ang"
#     description: str = "Default process for ChatGPT for the Old English (ca. 450-1100) language."
#     authorship_info: str = "OldEnglishChatGPTProcess using OpenAI GPT models."

# @dataclass
# class OfficialAramaicChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "arc"
#     description: str = "Default process for ChatGPT for the Official Aramaic (700-300 BCE) language."
#     authorship_info: str = "OfficialAramaicChatGPTProcess using OpenAI GPT models."

# @dataclass
# class AvestanChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "ave"
#     description: str = "Default process for ChatGPT for the Avestan language."
#     authorship_info: str = "AvestanChatGPTProcess using OpenAI GPT models."

# @dataclass
# class MiddleArmenianChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "axm"
#     description: str = "Default process for ChatGPT for the Middle Armenian language."
#     authorship_info: str = "MiddleArmenianChatGPTProcess using OpenAI GPT models."

# @dataclass
# class ChurchSlavicChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "chu"
#     description: str = "Default process for ChatGPT for the Church Slavic language."
#     authorship_info: str = "ChurchSlavicChatGPTProcess using OpenAI GPT models."

# @dataclass
# class ClassicalMongolianChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "cmg"
#     description: str = "Default process for ChatGPT for the Classical Mongolian language."
#     authorship_info: str = "ClassicalMongolianChatGPTProcess using OpenAI GPT models."

# @dataclass
# class MessapicChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "cms"
#     description: str = "Default process for ChatGPT for the Messapic language."
#     authorship_info: str = "MessapicChatGPTProcess using OpenAI GPT models."

# @dataclass
# class MiddleCornishChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "cnx"
#     description: str = "Default process for ChatGPT for the Middle Cornish language."
#     authorship_info: str = "MiddleCornishChatGPTProcess using OpenAI GPT models."

# @dataclass
# class MiddleDutchChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "dum"
#     description: str = "Default process for ChatGPT for the Middle Dutch language."
#     authorship_info: str = "MiddleDutchChatGPTProcess using OpenAI GPT models."

# @dataclass
# class EarlyNewHighGermanChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "goh"
#     description: str = "Default process for ChatGPT for the Early New High German language."
#     authorship_info: str = "EarlyNewHighGermanChatGPTProcess using OpenAI GPT models."

# @dataclass
# class GothicChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "got"
#     description: str = "Default process for ChatGPT for the Gothic language."
#     authorship_info: str = "GothicChatGPTProcess using OpenAI GPT models."

# @dataclass
# class HebrewBiblicalChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "heb"
#     description: str = "Default process for ChatGPT for the Biblical Hebrew language."
#     authorship_info: str = "HebrewBiblicalChatGPTProcess using OpenAI GPT models."

# @dataclass
# class OldIrishChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "sga"
#     description: str = "Default process for ChatGPT for the Old Irish (ca. 600-900) language."
#     authorship_info: str = "OldIrishChatGPTProcess using OpenAI GPT models."

# @dataclass
# class SanskritChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "san"
#     description: str = "Default process for ChatGPT for the Sanskrit language."
#     authorship_info: str = "SanskritChatGPTProcess using OpenAI GPT models."

# @dataclass
# class SerboCroatianChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "shs"
#     description: str = "Default process for ChatGPT for the Serbo-Croatian language."
#     authorship_info: str = "SerboCroatianChatGPTProcess using OpenAI GPT models."

# @dataclass
# class MiddleWelshChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "cyw"
#     description: str = "Default process for ChatGPT for the Middle Welsh language."
#     authorship_info: str = "MiddleWelshChatGPTProcess using OpenAI GPT models."

# @dataclass
# class LatinChatGPTProcess(ChatGPTProcess):
#     language: Optional[str] = "lat"
#     description: str = "Default process for ChatGPT for the Latin language."
#     authorship_info: str = "LatinChatGPTProcess using OpenAI GPT models."


@dataclass
class AequianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xae"
    description: str = "Default process for ChatGPT for the Aequian language."
    authorship_info: str = "AequianChatGPTProcess using OpenAI GPT models."


@dataclass
class AghwanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xag"
    description: str = "Default process for ChatGPT for the Aghwan language."
    authorship_info: str = "AghwanChatGPTProcess using OpenAI GPT models."


@dataclass
class AkkadianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "akk"
    description: str = "Default process for ChatGPT for the Akkadian language."
    authorship_info: str = "AkkadianChatGPTProcess using OpenAI GPT models."


@dataclass
class AlanicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xln"
    description: str = "Default process for ChatGPT for the Alanic language."
    authorship_info: str = "AlanicChatGPTProcess using OpenAI GPT models."


@dataclass
class AncientGreekChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "grc"
    description: str = "Default process for ChatGPT for the Ancient Greek language."
    authorship_info: str = "Ancient GreekChatGPTProcess using OpenAI GPT models."


@dataclass
class AncientHebrewChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "hbo"
    description: str = "Default process for ChatGPT for the Ancient Hebrew language."
    authorship_info: str = "Ancient HebrewChatGPTProcess using OpenAI GPT models."


@dataclass
class AncientLigurianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xlg"
    description: str = "Default process for ChatGPT for the Ancient Ligurian language."
    authorship_info: str = "Ancient LigurianChatGPTProcess using OpenAI GPT models."


@dataclass
class AncientMacedonianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xmk"
    description: str = (
        "Default process for ChatGPT for the Ancient Macedonian language."
    )
    authorship_info: str = "Ancient MacedonianChatGPTProcess using OpenAI GPT models."


@dataclass
class AncientNorthArabianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xna"
    description: str = (
        "Default process for ChatGPT for the Ancient North Arabian language."
    )
    authorship_info: str = (
        "Ancient North ArabianChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class AncientZapotecChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xzp"
    description: str = "Default process for ChatGPT for the Ancient Zapotec language."
    authorship_info: str = "Ancient ZapotecChatGPTProcess using OpenAI GPT models."


@dataclass
class AndalusianArabicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xaa"
    description: str = "Default process for ChatGPT for the Andalusian Arabic language."
    authorship_info: str = "Andalusian ArabicChatGPTProcess using OpenAI GPT models."


@dataclass
class AngloNormanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xno"
    description: str = "Default process for ChatGPT for the Anglo-Norman language."
    authorship_info: str = "Anglo-NormanChatGPTProcess using OpenAI GPT models."


@dataclass
class AquitanianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xaq"
    description: str = "Default process for ChatGPT for the Aquitanian language."
    authorship_info: str = "AquitanianChatGPTProcess using OpenAI GPT models."


@dataclass
class ArdhamāgadhīPrākritChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pka"
    description: str = (
        "Default process for ChatGPT for the Ardhamāgadhī Prākrit language."
    )
    authorship_info: str = "Ardhamāgadhī PrākritChatGPTProcess using OpenAI GPT models."


@dataclass
class ArmazicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xrm"
    description: str = "Default process for ChatGPT for the Armazic language."
    authorship_info: str = "ArmazicChatGPTProcess using OpenAI GPT models."


@dataclass
class AvestanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ave"
    description: str = "Default process for ChatGPT for the Avestan language."
    authorship_info: str = "AvestanChatGPTProcess using OpenAI GPT models."


@dataclass
class BactrianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xbc"
    description: str = "Default process for ChatGPT for the Bactrian language."
    authorship_info: str = "BactrianChatGPTProcess using OpenAI GPT models."


@dataclass
class BengaliChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ben"
    description: str = "Default process for ChatGPT for the Bengali language."
    authorship_info: str = "BengaliChatGPTProcess using OpenAI GPT models."


@dataclass
class BolgarianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xbo"
    description: str = "Default process for ChatGPT for the Bolgarian language."
    authorship_info: str = "BolgarianChatGPTProcess using OpenAI GPT models."


@dataclass
class BurmaPyuChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pyx"
    description: str = "Default process for ChatGPT for the Burma Pyu language."
    authorship_info: str = "Burma PyuChatGPTProcess using OpenAI GPT models."


@dataclass
class CamunicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xcc"
    description: str = "Default process for ChatGPT for the Camunic language."
    authorship_info: str = "CamunicChatGPTProcess using OpenAI GPT models."


@dataclass
class CarianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xcr"
    description: str = "Default process for ChatGPT for the Carian language."
    authorship_info: str = "CarianChatGPTProcess using OpenAI GPT models."


@dataclass
class CeltiberianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xce"
    description: str = "Default process for ChatGPT for the Celtiberian language."
    authorship_info: str = "CeltiberianChatGPTProcess using OpenAI GPT models."


@dataclass
class ChurchSlavicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "chu"
    description: str = "Default process for ChatGPT for the Church Slavic language."
    authorship_info: str = "Church SlavicChatGPTProcess using OpenAI GPT models."


@dataclass
class CisalpineGaulishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xcg"
    description: str = "Default process for ChatGPT for the Cisalpine Gaulish language."
    authorship_info: str = "Cisalpine GaulishChatGPTProcess using OpenAI GPT models."


@dataclass
class ClassicalArmenianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xcl"
    description: str = (
        "Default process for ChatGPT for the Classical Armenian language."
    )
    authorship_info: str = "Classical ArmenianChatGPTProcess using OpenAI GPT models."


@dataclass
class ClassicalMandaicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "myz"
    description: str = "Default process for ChatGPT for the Classical Mandaic language."
    authorship_info: str = "Classical MandaicChatGPTProcess using OpenAI GPT models."


@dataclass
class ClassicalMongolianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "cmg"
    description: str = (
        "Default process for ChatGPT for the Classical Mongolian language."
    )
    authorship_info: str = "Classical MongolianChatGPTProcess using OpenAI GPT models."


@dataclass
class ClassicalNahuatlChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "nci"
    description: str = "Default process for ChatGPT for the Classical Nahuatl language."
    authorship_info: str = "Classical NahuatlChatGPTProcess using OpenAI GPT models."


@dataclass
class ClassicalNewariChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "nwc"
    description: str = "Default process for ChatGPT for the Classical Newari language."
    authorship_info: str = "Classical NewariChatGPTProcess using OpenAI GPT models."


@dataclass
class ClassicalQuechuaChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "qwc"
    description: str = "Default process for ChatGPT for the Classical Quechua language."
    authorship_info: str = "Classical QuechuaChatGPTProcess using OpenAI GPT models."


@dataclass
class ClassicalSyriacChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "syc"
    description: str = "Default process for ChatGPT for the Classical Syriac language."
    authorship_info: str = "Classical SyriacChatGPTProcess using OpenAI GPT models."


@dataclass
class ClassicalTibetanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xct"
    description: str = "Default process for ChatGPT for the Classical Tibetan language."
    authorship_info: str = "Classical TibetanChatGPTProcess using OpenAI GPT models."


@dataclass
class CopticChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "cop"
    description: str = "Default process for ChatGPT for the Coptic language."
    authorship_info: str = "CopticChatGPTProcess using OpenAI GPT models."


@dataclass
class CumbricChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xcb"
    description: str = "Default process for ChatGPT for the Cumbric language."
    authorship_info: str = "CumbricChatGPTProcess using OpenAI GPT models."


@dataclass
class CuneiformLuwianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xlu"
    description: str = "Default process for ChatGPT for the Cuneiform Luwian language."
    authorship_info: str = "Cuneiform LuwianChatGPTProcess using OpenAI GPT models."


@dataclass
class CuronianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xcu"
    description: str = "Default process for ChatGPT for the Curonian language."
    authorship_info: str = "CuronianChatGPTProcess using OpenAI GPT models."


@dataclass
class DacianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xdc"
    description: str = "Default process for ChatGPT for the Dacian language."
    authorship_info: str = "DacianChatGPTProcess using OpenAI GPT models."


@dataclass
class EarlyIrishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "sga"
    description: str = "Default process for ChatGPT for the Early Irish language."
    authorship_info: str = "Early IrishChatGPTProcess using OpenAI GPT models."


@dataclass
class EarlyTripuriChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xtr"
    description: str = "Default process for ChatGPT for the Early Tripuri language."
    authorship_info: str = "Early TripuriChatGPTProcess using OpenAI GPT models."


@dataclass
class EasternPanjabiChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pan"
    description: str = "Default process for ChatGPT for the Eastern Panjabi language."
    authorship_info: str = "Eastern PanjabiChatGPTProcess using OpenAI GPT models."


@dataclass
class EblaiteChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xeb"
    description: str = "Default process for ChatGPT for the Eblaite language."
    authorship_info: str = "EblaiteChatGPTProcess using OpenAI GPT models."


@dataclass
class EdomiteChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xdm"
    description: str = "Default process for ChatGPT for the Edomite language."
    authorship_info: str = "EdomiteChatGPTProcess using OpenAI GPT models."


@dataclass
class EgyptianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "egy"
    description: str = (
        "Default process for ChatGPT for the Egyptian (Ancient) language."
    )
    authorship_info: str = "Egyptian (Ancient)ChatGPTProcess using OpenAI GPT models."


@dataclass
class ElamiteChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "elx"
    description: str = "Default process for ChatGPT for the Elamite language."
    authorship_info: str = "ElamiteChatGPTProcess using OpenAI GPT models."


@dataclass
class ElymianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xly"
    description: str = "Default process for ChatGPT for the Elymian language."
    authorship_info: str = "ElymianChatGPTProcess using OpenAI GPT models."


@dataclass
class EpiOlmecChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xep"
    description: str = "Default process for ChatGPT for the Epi-Olmec language."
    authorship_info: str = "Epi-OlmecChatGPTProcess using OpenAI GPT models."


@dataclass
class EpigraphicMayanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "emy"
    description: str = "Default process for ChatGPT for the Epigraphic Mayan language."
    authorship_info: str = "Epigraphic MayanChatGPTProcess using OpenAI GPT models."


@dataclass
class EteocretanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ecr"
    description: str = "Default process for ChatGPT for the Eteocretan language."
    authorship_info: str = "EteocretanChatGPTProcess using OpenAI GPT models."


@dataclass
class EteocypriotChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ecy"
    description: str = "Default process for ChatGPT for the Eteocypriot language."
    authorship_info: str = "EteocypriotChatGPTProcess using OpenAI GPT models."


@dataclass
class EtruscanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ett"
    description: str = "Default process for ChatGPT for the Etruscan language."
    authorship_info: str = "EtruscanChatGPTProcess using OpenAI GPT models."


@dataclass
class FaliscanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xfa"
    description: str = "Default process for ChatGPT for the Faliscan language."
    authorship_info: str = "FaliscanChatGPTProcess using OpenAI GPT models."


@dataclass
class GalatianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xga"
    description: str = "Default process for ChatGPT for the Galatian language."
    authorship_info: str = "GalatianChatGPTProcess using OpenAI GPT models."


@dataclass
class GalindanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xgl"
    description: str = "Default process for ChatGPT for the Galindan language."
    authorship_info: str = "GalindanChatGPTProcess using OpenAI GPT models."


@dataclass
class GeezChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "gez"
    description: str = "Default process for ChatGPT for the Geez language."
    authorship_info: str = "GeezChatGPTProcess using OpenAI GPT models."


@dataclass
class GothicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "got"
    description: str = "Default process for ChatGPT for the Gothic language."
    authorship_info: str = "GothicChatGPTProcess using OpenAI GPT models."


@dataclass
class GujaratiChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "guj"
    description: str = "Default process for ChatGPT for the Gujarati language."
    authorship_info: str = "GujaratiChatGPTProcess using OpenAI GPT models."


@dataclass
class GāndhārīChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pgd"
    description: str = "Default process for ChatGPT for the Gāndhārī language."
    authorship_info: str = "GāndhārīChatGPTProcess using OpenAI GPT models."


@dataclass
class HadramiChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xhd"
    description: str = "Default process for ChatGPT for the Hadrami language."
    authorship_info: str = "HadramiChatGPTProcess using OpenAI GPT models."


@dataclass
class HaramiChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xha"
    description: str = "Default process for ChatGPT for the Harami language."
    authorship_info: str = "HaramiChatGPTProcess using OpenAI GPT models."


@dataclass
class HarappanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xiv"
    description: str = "Default process for ChatGPT for the Harappan language."
    authorship_info: str = "HarappanChatGPTProcess using OpenAI GPT models."


@dataclass
class HatticChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xht"
    description: str = "Default process for ChatGPT for the Hattic language."
    authorship_info: str = "HatticChatGPTProcess using OpenAI GPT models."


@dataclass
class HernicanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xhr"
    description: str = "Default process for ChatGPT for the Hernican language."
    authorship_info: str = "HernicanChatGPTProcess using OpenAI GPT models."


@dataclass
class HibernoScottishGaelicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ghc"
    description: str = (
        "Default process for ChatGPT for the Hiberno-Scottish Gaelic language."
    )
    authorship_info: str = (
        "Hiberno-Scottish GaelicChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class HieroglyphicLuwianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "hlu"
    description: str = (
        "Default process for ChatGPT for the Hieroglyphic Luwian language."
    )
    authorship_info: str = "Hieroglyphic LuwianChatGPTProcess using OpenAI GPT models."


@dataclass
class HindiChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "hin"
    description: str = "Default process for ChatGPT for the Hindi language."
    authorship_info: str = "HindiChatGPTProcess using OpenAI GPT models."


@dataclass
class HittiteChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "hit"
    description: str = "Default process for ChatGPT for the Hittite language."
    authorship_info: str = "HittiteChatGPTProcess using OpenAI GPT models."


@dataclass
class HunnicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xhc"
    description: str = "Default process for ChatGPT for the Hunnic language."
    authorship_info: str = "HunnicChatGPTProcess using OpenAI GPT models."


@dataclass
class HurrianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xhu"
    description: str = "Default process for ChatGPT for the Hurrian language."
    authorship_info: str = "HurrianChatGPTProcess using OpenAI GPT models."


@dataclass
class IberianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xib"
    description: str = "Default process for ChatGPT for the Iberian language."
    authorship_info: str = "IberianChatGPTProcess using OpenAI GPT models."


@dataclass
class IllyrianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xil"
    description: str = "Default process for ChatGPT for the Illyrian language."
    authorship_info: str = "IllyrianChatGPTProcess using OpenAI GPT models."


@dataclass
class JutishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "jut"
    description: str = "Default process for ChatGPT for the Jutish language."
    authorship_info: str = "JutishChatGPTProcess using OpenAI GPT models."


@dataclass
class KajkavianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "kjv"
    description: str = "Default process for ChatGPT for the Kajkavian language."
    authorship_info: str = "KajkavianChatGPTProcess using OpenAI GPT models."


@dataclass
class KannadaChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "kan"
    description: str = "Default process for ChatGPT for the Kannada language."
    authorship_info: str = "KannadaChatGPTProcess using OpenAI GPT models."


@dataclass
class KaraChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "zra"
    description: str = "Default process for ChatGPT for the Kara (Korea) language."
    authorship_info: str = "Kara (Korea)ChatGPTProcess using OpenAI GPT models."


@dataclass
class KarakhanidChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xqa"
    description: str = "Default process for ChatGPT for the Karakhanid language."
    authorship_info: str = "KarakhanidChatGPTProcess using OpenAI GPT models."


@dataclass
class KaskeanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "zsk"
    description: str = "Default process for ChatGPT for the Kaskean language."
    authorship_info: str = "KaskeanChatGPTProcess using OpenAI GPT models."


@dataclass
class KawiChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "kaw"
    description: str = "Default process for ChatGPT for the Kawi language."
    authorship_info: str = "KawiChatGPTProcess using OpenAI GPT models."


@dataclass
class KhazarChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "zkz"
    description: str = "Default process for ChatGPT for the Khazar language."
    authorship_info: str = "KhazarChatGPTProcess using OpenAI GPT models."


@dataclass
class KhorezmianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "zkh"
    description: str = "Default process for ChatGPT for the Khorezmian language."
    authorship_info: str = "KhorezmianChatGPTProcess using OpenAI GPT models."


@dataclass
class KhotaneseChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "kho"
    description: str = "Default process for ChatGPT for the Khotanese language."
    authorship_info: str = "KhotaneseChatGPTProcess using OpenAI GPT models."


@dataclass
class KhwarezmianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xco"
    description: str = "Default process for ChatGPT for the Khwarezmian language."
    authorship_info: str = "KhwarezmianChatGPTProcess using OpenAI GPT models."


@dataclass
class KitanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "zkt"
    description: str = "Default process for ChatGPT for the Kitan language."
    authorship_info: str = "KitanChatGPTProcess using OpenAI GPT models."


@dataclass
class KoguryoChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "zkg"
    description: str = "Default process for ChatGPT for the Koguryo language."
    authorship_info: str = "KoguryoChatGPTProcess using OpenAI GPT models."


@dataclass
class LangobardicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "lng"
    description: str = "Default process for ChatGPT for the Langobardic language."
    authorship_info: str = "LangobardicChatGPTProcess using OpenAI GPT models."


@dataclass
class LatinChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "lat"
    description: str = "Default process for ChatGPT for the Latin language."
    authorship_info: str = "LatinChatGPTProcess using OpenAI GPT models."


@dataclass
class LemnianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xle"
    description: str = "Default process for ChatGPT for the Lemnian language."
    authorship_info: str = "LemnianChatGPTProcess using OpenAI GPT models."


@dataclass
class LeponticChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xlp"
    description: str = "Default process for ChatGPT for the Lepontic language."
    authorship_info: str = "LeponticChatGPTProcess using OpenAI GPT models."


@dataclass
class LiburnianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xli"
    description: str = "Default process for ChatGPT for the Liburnian language."
    authorship_info: str = "LiburnianChatGPTProcess using OpenAI GPT models."


@dataclass
class LinearAChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "lab"
    description: str = "Default process for ChatGPT for the Linear A language."
    authorship_info: str = "Linear AChatGPTProcess using OpenAI GPT models."


@dataclass
class LiteraryChineseChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "lzh"
    description: str = "Default process for ChatGPT for the Literary Chinese language."
    authorship_info: str = "Literary ChineseChatGPTProcess using OpenAI GPT models."


@dataclass
class LusitanianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xls"
    description: str = "Default process for ChatGPT for the Lusitanian language."
    authorship_info: str = "LusitanianChatGPTProcess using OpenAI GPT models."


@dataclass
class LycianAChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xlc"
    description: str = "Default process for ChatGPT for the Lycian A language."
    authorship_info: str = "Lycian AChatGPTProcess using OpenAI GPT models."


@dataclass
class LydianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xld"
    description: str = "Default process for ChatGPT for the Lydian language."
    authorship_info: str = "LydianChatGPTProcess using OpenAI GPT models."


@dataclass
class MaekChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "hmk"
    description: str = "Default process for ChatGPT for the Maek language."
    authorship_info: str = "MaekChatGPTProcess using OpenAI GPT models."


@dataclass
class MaharastriPrakritChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pmh"
    description: str = (
        "Default process for ChatGPT for the Maharastri Prakrit language."
    )
    authorship_info: str = "Maharastri PrakritChatGPTProcess using OpenAI GPT models."


@dataclass
class MalayalamChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "mal"
    description: str = "Default process for ChatGPT for the Malayalam language."
    authorship_info: str = "MalayalamChatGPTProcess using OpenAI GPT models."


@dataclass
class ManichaeanMiddlePersianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xmn"
    description: str = (
        "Default process for ChatGPT for the Manichaean Middle Persian language."
    )
    authorship_info: str = (
        "Manichaean Middle PersianChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class MarrucinianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "umc"
    description: str = "Default process for ChatGPT for the Marrucinian language."
    authorship_info: str = "MarrucinianChatGPTProcess using OpenAI GPT models."


@dataclass
class MarsianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ims"
    description: str = "Default process for ChatGPT for the Marsian language."
    authorship_info: str = "MarsianChatGPTProcess using OpenAI GPT models."


@dataclass
class MedianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xme"
    description: str = "Default process for ChatGPT for the Median language."
    authorship_info: str = "MedianChatGPTProcess using OpenAI GPT models."


@dataclass
class MeroiticChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xmr"
    description: str = "Default process for ChatGPT for the Meroitic language."
    authorship_info: str = "MeroiticChatGPTProcess using OpenAI GPT models."


@dataclass
class MessapicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "cms"
    description: str = "Default process for ChatGPT for the Messapic language."
    authorship_info: str = "MessapicChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleArmenianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "axm"
    description: str = "Default process for ChatGPT for the Middle Armenian language."
    authorship_info: str = "Middle ArmenianChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleBretonChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xbm"
    description: str = "Default process for ChatGPT for the Middle Breton language."
    authorship_info: str = "Middle BretonChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleChineseChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ltc"
    description: str = "Default process for ChatGPT for the Middle Chinese language."
    authorship_info: str = "Middle ChineseChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleCornishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "cnx"
    description: str = "Default process for ChatGPT for the Middle Cornish language."
    authorship_info: str = "Middle CornishChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleDutchChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "dum"
    description: str = "Default process for ChatGPT for the Middle Dutch language."
    authorship_info: str = "Middle DutchChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleEnglishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "enm"
    description: str = "Default process for ChatGPT for the Middle English language."
    authorship_info: str = "Middle EnglishChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleFrenchChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "frm"
    description: str = "Default process for ChatGPT for the Middle French language."
    authorship_info: str = "Middle FrenchChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleHighGermanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "gmh"
    description: str = (
        "Default process for ChatGPT for the Middle High German language."
    )
    authorship_info: str = "Middle High GermanChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleHittiteChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "htx"
    description: str = "Default process for ChatGPT for the Middle Hittite language."
    authorship_info: str = "Middle HittiteChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleIrishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "mga"
    description: str = (
        "Default process for ChatGPT for the Middle Irish (10-12th century) language."
    )
    authorship_info: str = (
        "Middle Irish (10-12th century)ChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class MiddleKoreanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "okm"
    description: str = (
        "Default process for ChatGPT for the Middle Korean (10th-16th cent.) language."
    )
    authorship_info: str = (
        "Middle Korean (10th-16th cent.)ChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class MiddleLowGermanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "gml"
    description: str = "Default process for ChatGPT for the Middle Low German language."
    authorship_info: str = "Middle Low GermanChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleMongolChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xng"
    description: str = "Default process for ChatGPT for the Middle Mongol language."
    authorship_info: str = "Middle MongolChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleNewarChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "nwx"
    description: str = "Default process for ChatGPT for the Middle Newar language."
    authorship_info: str = "Middle NewarChatGPTProcess using OpenAI GPT models."


@dataclass
class MiddleWelshChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "wlm"
    description: str = "Default process for ChatGPT for the Middle Welsh language."
    authorship_info: str = "Middle WelshChatGPTProcess using OpenAI GPT models."


@dataclass
class MilyanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "imy"
    description: str = "Default process for ChatGPT for the Milyan language."
    authorship_info: str = "MilyanChatGPTProcess using OpenAI GPT models."


@dataclass
class MinaeanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "inm"
    description: str = "Default process for ChatGPT for the Minaean language."
    authorship_info: str = "MinaeanChatGPTProcess using OpenAI GPT models."


@dataclass
class MinoanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "omn"
    description: str = "Default process for ChatGPT for the Minoan language."
    authorship_info: str = "MinoanChatGPTProcess using OpenAI GPT models."


@dataclass
class MoabiteChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "obm"
    description: str = "Default process for ChatGPT for the Moabite language."
    authorship_info: str = "MoabiteChatGPTProcess using OpenAI GPT models."


@dataclass
class MozarabicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "mxi"
    description: str = "Default process for ChatGPT for the Mozarabic language."
    authorship_info: str = "MozarabicChatGPTProcess using OpenAI GPT models."


@dataclass
class MycenaeanGreekChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "gmy"
    description: str = "Default process for ChatGPT for the Mycenaean Greek language."
    authorship_info: str = "Mycenaean GreekChatGPTProcess using OpenAI GPT models."


@dataclass
class MysianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "yms"
    description: str = "Default process for ChatGPT for the Mysian language."
    authorship_info: str = "MysianChatGPTProcess using OpenAI GPT models."


@dataclass
class NadruvianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ndf"
    description: str = "Default process for ChatGPT for the Nadruvian language."
    authorship_info: str = "NadruvianChatGPTProcess using OpenAI GPT models."


@dataclass
class NeoHittiteChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "nei"
    description: str = "Default process for ChatGPT for the Neo-Hittite language."
    authorship_info: str = "Neo-HittiteChatGPTProcess using OpenAI GPT models."


@dataclass
class NoricChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "nrc"
    description: str = "Default process for ChatGPT for the Noric language."
    authorship_info: str = "NoricChatGPTProcess using OpenAI GPT models."


@dataclass
class NorthPiceneChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "nrp"
    description: str = "Default process for ChatGPT for the North Picene language."
    authorship_info: str = "North PiceneChatGPTProcess using OpenAI GPT models."


@dataclass
class NumidianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "nxm"
    description: str = "Default process for ChatGPT for the Numidian language."
    authorship_info: str = "NumidianChatGPTProcess using OpenAI GPT models."


@dataclass
class OdiaChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ory"
    description: str = "Default process for ChatGPT for the Odia language."
    authorship_info: str = "OdiaChatGPTProcess using OpenAI GPT models."


@dataclass
class OfficialAramaicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "arc"
    description: str = (
        "Default process for ChatGPT for the Official Aramaic (700-300 BCE) language."
    )
    authorship_info: str = (
        "Official Aramaic (700-300 BCE)ChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class OldAramaicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "oar"
    description: str = (
        "Default process for ChatGPT for the Old Aramaic (up to 700 BCE) language."
    )
    authorship_info: str = (
        "Old Aramaic (up to 700 BCE)ChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class OldAvarChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "oav"
    description: str = "Default process for ChatGPT for the Old Avar language."
    authorship_info: str = "Old AvarChatGPTProcess using OpenAI GPT models."


@dataclass
class OldBretonChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "obt"
    description: str = "Default process for ChatGPT for the Old Breton language."
    authorship_info: str = "Old BretonChatGPTProcess using OpenAI GPT models."


@dataclass
class OldBurmeseChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "obr"
    description: str = "Default process for ChatGPT for the Old Burmese language."
    authorship_info: str = "Old BurmeseChatGPTProcess using OpenAI GPT models."


@dataclass
class OldChineseChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "och"
    description: str = "Default process for ChatGPT for the Old Chinese language."
    authorship_info: str = "Old ChineseChatGPTProcess using OpenAI GPT models."


@dataclass
class OldCornishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "oco"
    description: str = "Default process for ChatGPT for the Old Cornish language."
    authorship_info: str = "Old CornishChatGPTProcess using OpenAI GPT models."


@dataclass
class OldDutchOldFrankishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "odt"
    description: str = (
        "Default process for ChatGPT for the Old Dutch-Old Frankish language."
    )
    authorship_info: str = (
        "Old Dutch-Old FrankishChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class OldEnglishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ang"
    description: str = (
        "Default process for ChatGPT for the Old English (ca. 450-1100) language."
    )
    authorship_info: str = (
        "Old English (ca. 450-1100)ChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class OldFrankishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "frk"
    description: str = "Default process for ChatGPT for the Old Frankish language."
    authorship_info: str = "Old FrankishChatGPTProcess using OpenAI GPT models."


@dataclass
class OldFrenchChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "fro"
    description: str = (
        "Default process for ChatGPT for the Old French (842-ca. 1400) language."
    )
    authorship_info: str = (
        "Old French (842-ca. 1400)ChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class OldFrisianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ofs"
    description: str = "Default process for ChatGPT for the Old Frisian language."
    authorship_info: str = "Old FrisianChatGPTProcess using OpenAI GPT models."


@dataclass
class OldGeorgianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "oge"
    description: str = "Default process for ChatGPT for the Old Georgian language."
    authorship_info: str = "Old GeorgianChatGPTProcess using OpenAI GPT models."


@dataclass
class OldHighGermanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "goh"
    description: str = (
        "Default process for ChatGPT for the Old High German (ca. 750-1050) language."
    )
    authorship_info: str = (
        "Old High German (ca. 750-1050)ChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class OldHittiteChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "oht"
    description: str = "Default process for ChatGPT for the Old Hittite language."
    authorship_info: str = "Old HittiteChatGPTProcess using OpenAI GPT models."


@dataclass
class OldHungarianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ohu"
    description: str = "Default process for ChatGPT for the Old Hungarian language."
    authorship_info: str = "Old HungarianChatGPTProcess using OpenAI GPT models."


@dataclass
class OldJapaneseChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ojp"
    description: str = "Default process for ChatGPT for the Old Japanese language."
    authorship_info: str = "Old JapaneseChatGPTProcess using OpenAI GPT models."


@dataclass
class OldKoreanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "oko"
    description: str = (
        "Default process for ChatGPT for the Old Korean (3rd-9th cent.) language."
    )
    authorship_info: str = (
        "Old Korean (3rd-9th cent.)ChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class OldLithuanianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "olt"
    description: str = "Default process for ChatGPT for the Old Lithuanian language."
    authorship_info: str = "Old LithuanianChatGPTProcess using OpenAI GPT models."


@dataclass
class OldManipuriChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "omp"
    description: str = "Default process for ChatGPT for the Old Manipuri language."
    authorship_info: str = "Old ManipuriChatGPTProcess using OpenAI GPT models."


@dataclass
class OldMarathiChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "omr"
    description: str = "Default process for ChatGPT for the Old Marathi language."
    authorship_info: str = "Old MarathiChatGPTProcess using OpenAI GPT models."


@dataclass
class OldMonChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "omx"
    description: str = "Default process for ChatGPT for the Old Mon language."
    authorship_info: str = "Old MonChatGPTProcess using OpenAI GPT models."


@dataclass
class OldNorseChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "non"
    description: str = "Default process for ChatGPT for the Old Norse language."
    authorship_info: str = "Old NorseChatGPTProcess using OpenAI GPT models."


@dataclass
class OldNubianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "onw"
    description: str = "Default process for ChatGPT for the Old Nubian language."
    authorship_info: str = "Old NubianChatGPTProcess using OpenAI GPT models."


@dataclass
class OldOsseticChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "oos"
    description: str = "Default process for ChatGPT for the Old Ossetic language."
    authorship_info: str = "Old OsseticChatGPTProcess using OpenAI GPT models."


@dataclass
class OldPersianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "peo"
    description: str = (
        "Default process for ChatGPT for the Old Persian (ca. 600-400 B.C.) language."
    )
    authorship_info: str = (
        "Old Persian (ca. 600-400 B.C.)ChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class OldProvençalChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pro"
    description: str = "Default process for ChatGPT for the Old Provençal language."
    authorship_info: str = "Old ProvençalChatGPTProcess using OpenAI GPT models."


@dataclass
class OldRussianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "orv"
    description: str = "Default process for ChatGPT for the Old Russian language."
    authorship_info: str = "Old RussianChatGPTProcess using OpenAI GPT models."


@dataclass
class OldSaxonChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "osx"
    description: str = "Default process for ChatGPT for the Old Saxon language."
    authorship_info: str = "Old SaxonChatGPTProcess using OpenAI GPT models."


@dataclass
class OldSpanishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "osp"
    description: str = "Default process for ChatGPT for the Old Spanish language."
    authorship_info: str = "Old SpanishChatGPTProcess using OpenAI GPT models."


@dataclass
class OldTamilChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "oty"
    description: str = "Default process for ChatGPT for the Old Tamil language."
    authorship_info: str = "Old TamilChatGPTProcess using OpenAI GPT models."


@dataclass
class OldTibetanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "otb"
    description: str = "Default process for ChatGPT for the Old Tibetan language."
    authorship_info: str = "Old TibetanChatGPTProcess using OpenAI GPT models."


@dataclass
class OldTurkicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "oui"
    description: str = "Default process for ChatGPT for the Old Turkic language."
    authorship_info: str = "Old TurkicChatGPTProcess using OpenAI GPT models."


@dataclass
class OldTurkishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "otk"
    description: str = "Default process for ChatGPT for the Old Turkish language."
    authorship_info: str = "Old TurkishChatGPTProcess using OpenAI GPT models."


@dataclass
class OldMiddleWelshChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "owl"
    description: str = "Default process for ChatGPT for the Old-Middle Welsh language."
    authorship_info: str = "Old-Middle WelshChatGPTProcess using OpenAI GPT models."


@dataclass
class OscanChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "osc"
    description: str = "Default process for ChatGPT for the Oscan language."
    authorship_info: str = "OscanChatGPTProcess using OpenAI GPT models."


@dataclass
class OttomanTurkishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "ota"
    description: str = (
        "Default process for ChatGPT for the Ottoman Turkish (1500-1928) language."
    )
    authorship_info: str = (
        "Ottoman Turkish (1500-1928)ChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class PaekcheChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pkc"
    description: str = "Default process for ChatGPT for the Paekche language."
    authorship_info: str = "PaekcheChatGPTProcess using OpenAI GPT models."


@dataclass
class PaelignianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pgn"
    description: str = "Default process for ChatGPT for the Paelignian language."
    authorship_info: str = "PaelignianChatGPTProcess using OpenAI GPT models."


@dataclass
class PahlaviChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pal"
    description: str = "Default process for ChatGPT for the Pahlavi language."
    authorship_info: str = "PahlaviChatGPTProcess using OpenAI GPT models."


@dataclass
class PalaicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "plq"
    description: str = "Default process for ChatGPT for the Palaic language."
    authorship_info: str = "PalaicChatGPTProcess using OpenAI GPT models."


@dataclass
class PalestinianJewishAramaicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "jpa"
    description: str = (
        "Default process for ChatGPT for the Palestinian Jewish Aramaic language."
    )
    authorship_info: str = (
        "Palestinian Jewish AramaicChatGPTProcess using OpenAI GPT models."
    )


@dataclass
class PaliChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pli"
    description: str = "Default process for ChatGPT for the Pali language."
    authorship_info: str = "PaliChatGPTProcess using OpenAI GPT models."


@dataclass
class ParthianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xpr"
    description: str = "Default process for ChatGPT for the Parthian language."
    authorship_info: str = "ParthianChatGPTProcess using OpenAI GPT models."


@dataclass
class PechenegChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xpc"
    description: str = "Default process for ChatGPT for the Pecheneg language."
    authorship_info: str = "PechenegChatGPTProcess using OpenAI GPT models."


@dataclass
class PhoenicianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "phn"
    description: str = "Default process for ChatGPT for the Phoenician language."
    authorship_info: str = "PhoenicianChatGPTProcess using OpenAI GPT models."


@dataclass
class PhrygianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xpg"
    description: str = "Default process for ChatGPT for the Phrygian language."
    authorship_info: str = "PhrygianChatGPTProcess using OpenAI GPT models."


@dataclass
class PictishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xpi"
    description: str = "Default process for ChatGPT for the Pictish language."
    authorship_info: str = "PictishChatGPTProcess using OpenAI GPT models."


@dataclass
class PisidianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xps"
    description: str = "Default process for ChatGPT for the Pisidian language."
    authorship_info: str = "PisidianChatGPTProcess using OpenAI GPT models."


@dataclass
class PrimitiveIrishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pgl"
    description: str = "Default process for ChatGPT for the Primitive Irish language."
    authorship_info: str = "Primitive IrishChatGPTProcess using OpenAI GPT models."


@dataclass
class PunicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xpu"
    description: str = "Default process for ChatGPT for the Punic language."
    authorship_info: str = "PunicChatGPTProcess using OpenAI GPT models."


@dataclass
class PuyoChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xpy"
    description: str = "Default process for ChatGPT for the Puyo language."
    authorship_info: str = "PuyoChatGPTProcess using OpenAI GPT models."


@dataclass
class PuyoPaekcheChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xpp"
    description: str = "Default process for ChatGPT for the Puyo-Paekche language."
    authorship_info: str = "Puyo-PaekcheChatGPTProcess using OpenAI GPT models."


@dataclass
class QatabanianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xqt"
    description: str = "Default process for ChatGPT for the Qatabanian language."
    authorship_info: str = "QatabanianChatGPTProcess using OpenAI GPT models."


@dataclass
class RaeticChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xrr"
    description: str = "Default process for ChatGPT for the Raetic language."
    authorship_info: str = "RaeticChatGPTProcess using OpenAI GPT models."


@dataclass
class SabaicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xsa"
    description: str = "Default process for ChatGPT for the Sabaic language."
    authorship_info: str = "SabaicChatGPTProcess using OpenAI GPT models."


@dataclass
class SabineChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "sbv"
    description: str = "Default process for ChatGPT for the Sabine language."
    authorship_info: str = "SabineChatGPTProcess using OpenAI GPT models."


@dataclass
class SanskritChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "san"
    description: str = "Default process for ChatGPT for the Sanskrit language."
    authorship_info: str = "SanskritChatGPTProcess using OpenAI GPT models."


@dataclass
class SauraseniPrakritChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "psu"
    description: str = "Default process for ChatGPT for the Sauraseni Prakrit language."
    authorship_info: str = "Sauraseni PrakritChatGPTProcess using OpenAI GPT models."


@dataclass
class ScythianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xsc"
    description: str = "Default process for ChatGPT for the Scythian language."
    authorship_info: str = "ScythianChatGPTProcess using OpenAI GPT models."


@dataclass
class SicanaChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "sxc"
    description: str = "Default process for ChatGPT for the Sicana language."
    authorship_info: str = "SicanaChatGPTProcess using OpenAI GPT models."


@dataclass
class SiculaChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "scx"
    description: str = "Default process for ChatGPT for the Sicula language."
    authorship_info: str = "SiculaChatGPTProcess using OpenAI GPT models."


@dataclass
class SiculoArabicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "sqr"
    description: str = "Default process for ChatGPT for the Siculo Arabic language."
    authorship_info: str = "Siculo ArabicChatGPTProcess using OpenAI GPT models."


@dataclass
class SideticChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xsd"
    description: str = "Default process for ChatGPT for the Sidetic language."
    authorship_info: str = "SideticChatGPTProcess using OpenAI GPT models."


@dataclass
class SkalvianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "svx"
    description: str = "Default process for ChatGPT for the Skalvian language."
    authorship_info: str = "SkalvianChatGPTProcess using OpenAI GPT models."


@dataclass
class SogdianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "sog"
    description: str = "Default process for ChatGPT for the Sogdian language."
    authorship_info: str = "SogdianChatGPTProcess using OpenAI GPT models."


@dataclass
class SorothapticChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "sxo"
    description: str = "Default process for ChatGPT for the Sorothaptic language."
    authorship_info: str = "SorothapticChatGPTProcess using OpenAI GPT models."


@dataclass
class SouthPiceneChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "spx"
    description: str = "Default process for ChatGPT for the South Picene language."
    authorship_info: str = "South PiceneChatGPTProcess using OpenAI GPT models."


@dataclass
class StandardArabicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "arb"
    description: str = "Default process for ChatGPT for the Standard Arabic language."
    authorship_info: str = "Standard ArabicChatGPTProcess using OpenAI GPT models."


@dataclass
class SumerianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "sux"
    description: str = "Default process for ChatGPT for the Sumerian language."
    authorship_info: str = "SumerianChatGPTProcess using OpenAI GPT models."


@dataclass
class TangutChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "txg"
    description: str = "Default process for ChatGPT for the Tangut language."
    authorship_info: str = "TangutChatGPTProcess using OpenAI GPT models."


@dataclass
class TartessianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "txr"
    description: str = "Default process for ChatGPT for the Tartessian language."
    authorship_info: str = "TartessianChatGPTProcess using OpenAI GPT models."


@dataclass
class TeluguChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "tel"
    description: str = "Default process for ChatGPT for the Telugu language."
    authorship_info: str = "TeluguChatGPTProcess using OpenAI GPT models."


@dataclass
class ThracianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "txh"
    description: str = "Default process for ChatGPT for the Thracian language."
    authorship_info: str = "ThracianChatGPTProcess using OpenAI GPT models."


@dataclass
class TokharianAChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xto"
    description: str = "Default process for ChatGPT for the Tokharian A language."
    authorship_info: str = "Tokharian AChatGPTProcess using OpenAI GPT models."


@dataclass
class TokharianBChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "txb"
    description: str = "Default process for ChatGPT for the Tokharian B language."
    authorship_info: str = "Tokharian BChatGPTProcess using OpenAI GPT models."


@dataclass
class TransalpineGaulishChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xtg"
    description: str = (
        "Default process for ChatGPT for the Transalpine Gaulish language."
    )
    authorship_info: str = "Transalpine GaulishChatGPTProcess using OpenAI GPT models."


@dataclass
class TumshuqeseChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xtq"
    description: str = "Default process for ChatGPT for the Tumshuqese language."
    authorship_info: str = "TumshuqeseChatGPTProcess using OpenAI GPT models."


@dataclass
class UgariticChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "uga"
    description: str = "Default process for ChatGPT for the Ugaritic language."
    authorship_info: str = "UgariticChatGPTProcess using OpenAI GPT models."


@dataclass
class UmbrianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xum"
    description: str = "Default process for ChatGPT for the Umbrian language."
    authorship_info: str = "UmbrianChatGPTProcess using OpenAI GPT models."


@dataclass
class UrartianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xur"
    description: str = "Default process for ChatGPT for the Urartian language."
    authorship_info: str = "UrartianChatGPTProcess using OpenAI GPT models."


@dataclass
class UrduChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "urd"
    description: str = "Default process for ChatGPT for the Urdu language."
    authorship_info: str = "UrduChatGPTProcess using OpenAI GPT models."


@dataclass
class VandalicChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xvn"
    description: str = "Default process for ChatGPT for the Vandalic language."
    authorship_info: str = "VandalicChatGPTProcess using OpenAI GPT models."


@dataclass
class VeneticChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xve"
    description: str = "Default process for ChatGPT for the Venetic language."
    authorship_info: str = "VeneticChatGPTProcess using OpenAI GPT models."


@dataclass
class VestinianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xvs"
    description: str = "Default process for ChatGPT for the Vestinian language."
    authorship_info: str = "VestinianChatGPTProcess using OpenAI GPT models."


@dataclass
class VolscianChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xvo"
    description: str = "Default process for ChatGPT for the Volscian language."
    authorship_info: str = "VolscianChatGPTProcess using OpenAI GPT models."


@dataclass
class WesternFarsiChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "pes"
    description: str = "Default process for ChatGPT for the Western Farsi language."
    authorship_info: str = "Western FarsiChatGPTProcess using OpenAI GPT models."


@dataclass
class ZhangzhungChatGPTProcess(ChatGPTProcess):
    language: Optional[str] = "xzh"
    description: str = "Default process for ChatGPT for the Zhangzhung language."
    authorship_info: str = "ZhangzhungChatGPTProcess using OpenAI GPT models."


if __name__ == "__main__":
    import os

    from cltk.languages.example_texts import get_example_text
    from cltk.utils.utils import load_env_file

    load_env_file()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise CLTKException("Please set the OPENAI_API_KEY environment variable.")
    LANG_CODE: str = "lat"
    EXAMPLE_LAT = get_example_text(LANG_CODE)
    doc = Doc(language=LANG_CODE, raw=EXAMPLE_LAT)
    process = ChatGPTProcess(
        language=LANG_CODE, api_key=OPENAI_API_KEY, model="gpt-4.1", temperature=1.0
    )
    # process = AncientGreekChatGPTProcess(
    #     language="grc", api_key=OPENAI_API_KEY, model="gpt-4.1", temperature=1.0
    # )
    enriched_doc = process.run(doc)
    print(enriched_doc.words)
    print(enriched_doc.chatgpt)
