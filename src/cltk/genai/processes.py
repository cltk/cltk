"""Processes for ChatGPT."""

__license__ = "MIT License. See LICENSE."

import os
from dataclasses import field
from typing import Any, Optional

# from cltk.alphabet.text_normalization import cltk_normalize
from cltk.core.cltk_logger import logger
from cltk.core.data_types import Doc, Process
from cltk.core.exceptions import CLTKException
from cltk.genai.chatgpt import AVAILABILE_MODELS, ChatGPT
from cltk.utils.utils import load_env_file


class ChatGPTProcess(Process):
    """A Process type to capture everything that ChatGPT can do for a given language."""

    # For the type `ChatGPT`
    model_config = {"arbitrary_types_allowed": True}
    glottolog_id: Optional[str] = None
    api_key: Optional[str] = None
    model: AVAILABILE_MODELS = "gpt-5-mini"
    temperature: float = 0.2
    description: str = "Process for ChatGPT for linguistic annotation."
    authorship_info: str = "ChatGPTProcess using OpenAI GPT models."
    chatgpt: Optional[ChatGPT] = field(init=False, default=None)

    def model_post_init(self, __context: Any) -> None:
        load_env_file()
        logger.debug(f"Initializing ChatGPTProcess for language: {self.glottolog_id}")
        if not self.api_key:
            self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logger.error(
                "OPENAI_API_KEY not found. Please set it in your environment or in a .env file."
            )
        if self.glottolog_id and self.api_key:
            self.chatgpt = ChatGPT(
                glottolog_id=self.glottolog_id,
                api_key=self.api_key,
                model=self.model,
                temperature=self.temperature,
            )
            logger.info(
                f"ChatGPT instance created for language: {self.glottolog_id}, model: {self.model}, temperature: {self.temperature}"
            )
        else:
            self.chatgpt = None
            logger.warning(
                "ChatGPTProcess initialized without language or api_key. chatgpt set to None."
            )

        # Allow subclasses to hook into initialization without overriding this method
        try:
            self.on_initialized()
        except Exception as exc:  # defensive: keep initialization resilient
            logger.exception("on_initialized hook raised an exception: %s", exc)

        # Uniform final debug for all subclasses (replaces per-class loggers)
        logger.debug(f"{self.__class__.__name__} initialized.")

    def on_initialized(self) -> None:
        """Subclass hook called at the end of model_post_init.

        Override in subclasses that need extra setup without replacing
        the core initialization logic above.
        """
        return None

    def run(self, input_doc: Doc) -> Doc:
        """Run ChatGPT inferencing and enrich the Doc with linguistic metadata."""
        logger.debug(f"Running ChatGPTProcess for language: {self.glottolog_id}")
        if not self.chatgpt:
            logger.error("ChatGPTProcess requires language and api_key to be set.")
            raise ValueError("ChatGPTProcess requires language and api_key to be set.")
        if not input_doc.raw and not input_doc.normalized_text:
            logger.error(
                "Input document must have either `.normalized_text` or `raw` text."
            )
            raise CLTKException(
                "Input document must have either `.normalized_text` or `.raw` text."
            )
        input_text = (
            input_doc.normalized_text if input_doc.normalized_text else input_doc.raw
        )
        if not input_text:
            logger.error(
                "Input document must have either `.normalized_text` or `raw` text."
            )
            raise CLTKException(
                "Input document must have either `.normalized_text` or `.raw` text."
            )
        logger.info(
            f"Input text for ChatGPT: {input_text[:50]}..."
            if input_text
            else "Input text is empty."
        )
        enriched_doc = self.chatgpt.generate_all(input_doc=input_doc)
        # enriched_doc = self._enrich_doc(input_doc)
        # logger.info(f"Enriched doc words: {enriched_doc.words}")
        # logger.info(f"Enriched doc chatgpt: {enriched_doc.chatgpt}")
        return enriched_doc

    # def _enrich_doc(self, input_doc: Doc) -> Doc:
    #     """Enrich the document with metadata using ChatGPT."""
    #     logger.debug("Enriching document with ChatGPT metadata.")
    #     if not self.chatgpt:
    #         logger.error("ChatGPTProcess requires language and api_key to be set.")
    #         raise ValueError("ChatGPTProcess requires language and api_key to be set.")
    #     input_text = (
    #         input_doc.normalized_text if input_doc.normalized_text else input_doc.raw
    #     )
    #     if not input_text:
    #         logger.error("Input document must have either `.normalized_text` or `.raw` text.")
    #         raise CLTKException(
    #             "Input document must have either `.normalized_text` or `.raw` text."
    #         )
    #     logger.debug(f"Calling chatgpt.generate_all for language: {self.language}")
    #     enriched_doc = self.chatgpt.generate_all(input_text=input_text)
    #     # Only overwrite fields if not None in input_doc
    #     if input_doc.language is not None:
    #         enriched_doc.language = input_doc.language
    #     if input_doc.normalized_text is not None:
    #         enriched_doc.normalized_text = input_doc.normalized_text
    #     if input_doc.raw is not None:
    #         enriched_doc.raw = input_doc.raw
    #     if input_doc.pipeline is not None:
    #         enriched_doc.pipeline = input_doc.pipeline
    #     logger.debug("Document enrichment complete.")
    #     return enriched_doc


class CuneiformLuwianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "cune1239"
    description: str = "Default process for ChatGPT for the Cuneiform Luwian language."
    authorship_info: str = "CuneiformLuwianChatGPTProcess using OpenAI GPT models."


class HieroglyphicLuwianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "hier1240"
    description: str = (
        "Default process for ChatGPT for the Hieroglyphic Luwian language."
    )
    authorship_info: str = "HieroglyphicLuwianChatGPTProcess using OpenAI GPT models."


class OldPrussianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "prus1238"
    description: str = "Default process for ChatGPT for the Old Prussian language."
    authorship_info: str = "OldPrussianChatGPTProcess using OpenAI GPT models."


class LithuanianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lith1251"
    description: str = "Default process for ChatGPT for the Lithuanian language."
    authorship_info: str = "LithuanianChatGPTProcess using OpenAI GPT models."


class LatvianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "latv1249"
    description: str = "Default process for ChatGPT for the Latvian language."
    authorship_info: str = "LatvianChatGPTProcess using OpenAI GPT models."


class AlbanianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "gheg1238"
    description: str = "Default process for ChatGPT for the Albanian language."
    authorship_info: str = "AlbanianChatGPTProcess using OpenAI GPT models."


class AequianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xae"
    description: str = "Default process for ChatGPT for the Aequian language."
    authorship_info: str = "AequianChatGPTProcess using OpenAI GPT models."


class AghwanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xag"
    description: str = "Default process for ChatGPT for the Aghwan language."
    authorship_info: str = "AghwanChatGPTProcess using OpenAI GPT models."


class AkkadianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "akka1240"
    description: str = "Default process for ChatGPT for the Akkadian language."
    authorship_info: str = "AkkadianChatGPTProcess using OpenAI GPT models."


class AlanicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xln"
    description: str = "Default process for ChatGPT for the Alanic language."
    authorship_info: str = "AlanicChatGPTProcess using OpenAI GPT models."


class AncientGreekChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "anci1242"
    description: str = "Default process for ChatGPT for the Ancient Greek language."
    authorship_info: str = "Ancient GreekChatGPTProcess using OpenAI GPT models."


class BiblicalHebrewChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "anci1244"
    description: str = "Default process for ChatGPT for the Biblical Hebrew language."
    authorship_info: str = "Biblical HebrewChatGPTProcess using OpenAI GPT models."


class AncientLigurianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xlg"
    description: str = "Default process for ChatGPT for the Ancient Ligurian language."
    authorship_info: str = "Ancient LigurianChatGPTProcess using OpenAI GPT models."


class AncientMacedonianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xmk"
    description: str = (
        "Default process for ChatGPT for the Ancient Macedonian language."
    )
    authorship_info: str = "Ancient MacedonianChatGPTProcess using OpenAI GPT models."


class AncientNorthArabianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xna"
    description: str = (
        "Default process for ChatGPT for the Ancient North Arabian language."
    )
    authorship_info: str = (
        "Ancient North ArabianChatGPTProcess using OpenAI GPT models."
    )


class AncientZapotecChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xzp"
    description: str = "Default process for ChatGPT for the Ancient Zapotec language."
    authorship_info: str = "Ancient ZapotecChatGPTProcess using OpenAI GPT models."


class AndalusianArabicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xaa"
    description: str = "Default process for ChatGPT for the Andalusian Arabic language."
    authorship_info: str = "Andalusian ArabicChatGPTProcess using OpenAI GPT models."


class AngloNormanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xno"
    description: str = "Default process for ChatGPT for the Anglo-Norman language."
    authorship_info: str = "Anglo-NormanChatGPTProcess using OpenAI GPT models."


class AquitanianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xaq"
    description: str = "Default process for ChatGPT for the Aquitanian language."
    authorship_info: str = "AquitanianChatGPTProcess using OpenAI GPT models."


class ClassicalArabicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "arb-cla"
    description: str = "Default process for ChatGPT for the Classical Arabic language."
    authorship_info: str = "ClassicalArabicChatGPTProcess using OpenAI GPT models."


class ArdhamāgadhīPrākritChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pka"
    description: str = (
        "Default process for ChatGPT for the Ardhamāgadhī Prākrit language."
    )
    authorship_info: str = "Ardhamāgadhī PrākritChatGPTProcess using OpenAI GPT models."


class ArmazicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xrm"
    description: str = "Default process for ChatGPT for the Armazic language."
    authorship_info: str = "ArmazicChatGPTProcess using OpenAI GPT models."


class AvestanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "aves1237"
    description: str = "Default process for ChatGPT for the Avestan language."
    authorship_info: str = "AvestanChatGPTProcess using OpenAI GPT models."


class BactrianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "bact1239"
    description: str = "Default process for ChatGPT for the Bactrian language."
    authorship_info: str = "BactrianChatGPTProcess using OpenAI GPT models."


class SogdianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "sogd1245"
    description: str = "Default process for ChatGPT for the Sogdian language."
    authorship_info: str = "SogdianChatGPTProcess using OpenAI GPT models."


class BengaliChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "beng1280"
    description: str = "Default process for ChatGPT for the Bengali language."
    authorship_info: str = "BengaliChatGPTProcess using OpenAI GPT models."


class BolgarianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xbo"
    description: str = "Default process for ChatGPT for the Bolgarian language."
    authorship_info: str = "BolgarianChatGPTProcess using OpenAI GPT models."


class BurmaPyuChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pyx"
    description: str = "Default process for ChatGPT for the Burma Pyu language."
    authorship_info: str = "Burma PyuChatGPTProcess using OpenAI GPT models."


class CamunicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xcc"
    description: str = "Default process for ChatGPT for the Camunic language."
    authorship_info: str = "CamunicChatGPTProcess using OpenAI GPT models."


class CarianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "cari1274"
    description: str = "Default process for ChatGPT for the Carian language."
    authorship_info: str = "CarianChatGPTProcess using OpenAI GPT models."


class CeltiberianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xce"
    description: str = "Default process for ChatGPT for the Celtiberian language."
    authorship_info: str = "CeltiberianChatGPTProcess using OpenAI GPT models."


class ChurchSlavicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "chur1257"
    description: str = "Default process for ChatGPT for the Church Slavic language."
    authorship_info: str = "Church SlavicChatGPTProcess using OpenAI GPT models."


class CisalpineGaulishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xcg"
    description: str = "Default process for ChatGPT for the Cisalpine Gaulish language."
    authorship_info: str = "Cisalpine GaulishChatGPTProcess using OpenAI GPT models."


class ClassicalArmenianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xcl"
    description: str = (
        "Default process for ChatGPT for the Classical Armenian language."
    )
    authorship_info: str = "Classical ArmenianChatGPTProcess using OpenAI GPT models."


class ClassicalMandaicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "myz"
    description: str = "Default process for ChatGPT for the Classical Mandaic language."
    authorship_info: str = "Classical MandaicChatGPTProcess using OpenAI GPT models."


class ClassicalMongolianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "mong1331"
    description: str = (
        "Default process for ChatGPT for the Classical Mongolian language."
    )
    authorship_info: str = "Classical MongolianChatGPTProcess using OpenAI GPT models."


class ClassicalNahuatlChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "nci"
    description: str = "Default process for ChatGPT for the Classical Nahuatl language."
    authorship_info: str = "Classical NahuatlChatGPTProcess using OpenAI GPT models."


class ClassicalNewariChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "nwc"
    description: str = "Default process for ChatGPT for the Classical Newari language."
    authorship_info: str = "Classical NewariChatGPTProcess using OpenAI GPT models."


class ClassicalQuechuaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "qwc"
    description: str = "Default process for ChatGPT for the Classical Quechua language."
    authorship_info: str = "Classical QuechuaChatGPTProcess using OpenAI GPT models."


class ClassicalSyriacChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "clas1252"
    description: str = "Default process for ChatGPT for the Classical Syriac language."
    authorship_info: str = "Classical SyriacChatGPTProcess using OpenAI GPT models."


class ClassicalTibetanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "clas1254"
    description: str = "Default process for ChatGPT for the Classical Tibetan language."
    authorship_info: str = "Classical TibetanChatGPTProcess using OpenAI GPT models."


class CopticChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "copt1239"
    description: str = "Default process for ChatGPT for the Coptic language."
    authorship_info: str = "CopticChatGPTProcess using OpenAI GPT models."


class CumbricChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xcb"
    description: str = "Default process for ChatGPT for the Cumbric language."
    authorship_info: str = "CumbricChatGPTProcess using OpenAI GPT models."


class CuronianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xcu"
    description: str = "Default process for ChatGPT for the Curonian language."
    authorship_info: str = "CuronianChatGPTProcess using OpenAI GPT models."


class DacianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xdc"
    description: str = "Default process for ChatGPT for the Dacian language."
    authorship_info: str = "DacianChatGPTProcess using OpenAI GPT models."


class DemoticChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "demo1234"
    description: str = "Default process for ChatGPT for the Demotic language."
    authorship_info: str = "DemoticChatGPTProcess using OpenAI GPT models."


class EarlyTripuriChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xtr"
    description: str = "Default process for ChatGPT for the Early Tripuri language."
    authorship_info: str = "Early TripuriChatGPTProcess using OpenAI GPT models."


class EasternPanjabiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default process for ChatGPT for the Eastern Panjabi language."
    authorship_info: str = "Eastern PanjabiChatGPTProcess using OpenAI GPT models."


class EblaiteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xeb"
    description: str = "Default process for ChatGPT for the Eblaite language."
    authorship_info: str = "EblaiteChatGPTProcess using OpenAI GPT models."


class EdomiteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xdm"
    description: str = "Default process for ChatGPT for the Edomite language."
    authorship_info: str = "EdomiteChatGPTProcess using OpenAI GPT models."


class ElamiteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "elx"
    description: str = "Default process for ChatGPT for the Elamite language."
    authorship_info: str = "ElamiteChatGPTProcess using OpenAI GPT models."


class ElymianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xly"
    description: str = "Default process for ChatGPT for the Elymian language."
    authorship_info: str = "ElymianChatGPTProcess using OpenAI GPT models."


class EpiOlmecChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xep"
    description: str = "Default process for ChatGPT for the Epi-Olmec language."
    authorship_info: str = "Epi-OlmecChatGPTProcess using OpenAI GPT models."


class EpigraphicMayanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "emy"
    description: str = "Default process for ChatGPT for the Epigraphic Mayan language."
    authorship_info: str = "Epigraphic MayanChatGPTProcess using OpenAI GPT models."


class EteocretanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ecr"
    description: str = "Default process for ChatGPT for the Eteocretan language."
    authorship_info: str = "EteocretanChatGPTProcess using OpenAI GPT models."


class EteocypriotChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ecy"
    description: str = "Default process for ChatGPT for the Eteocypriot language."
    authorship_info: str = "EteocypriotChatGPTProcess using OpenAI GPT models."


class EtruscanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ett"
    description: str = "Default process for ChatGPT for the Etruscan language."
    authorship_info: str = "EtruscanChatGPTProcess using OpenAI GPT models."


class FaliscanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xfa"
    description: str = "Default process for ChatGPT for the Faliscan language."
    authorship_info: str = "FaliscanChatGPTProcess using OpenAI GPT models."


class GalatianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xga"
    description: str = "Default process for ChatGPT for the Galatian language."
    authorship_info: str = "GalatianChatGPTProcess using OpenAI GPT models."


class GalindanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xgl"
    description: str = "Default process for ChatGPT for the Galindan language."
    authorship_info: str = "GalindanChatGPTProcess using OpenAI GPT models."


class GeezChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "geez1241"
    description: str = "Default process for ChatGPT for the Geez language."
    authorship_info: str = "GeezChatGPTProcess using OpenAI GPT models."


class GothicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "goth1244"
    description: str = "Default process for ChatGPT for the Gothic language."
    authorship_info: str = "GothicChatGPTProcess using OpenAI GPT models."


class GujaratiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "guja1252"
    description: str = "Default process for ChatGPT for the Gujarati language."
    authorship_info: str = "GujaratiChatGPTProcess using OpenAI GPT models."


class GāndhārīChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pgd"
    description: str = "Default process for ChatGPT for the Gāndhārī language."
    authorship_info: str = "GāndhārīChatGPTProcess using OpenAI GPT models."


class HadramiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xhd"
    description: str = "Default process for ChatGPT for the Hadrami language."
    authorship_info: str = "HadramiChatGPTProcess using OpenAI GPT models."


class HaramiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xha"
    description: str = "Default process for ChatGPT for the Harami language."
    authorship_info: str = "HaramiChatGPTProcess using OpenAI GPT models."


class HarappanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xiv"
    description: str = "Default process for ChatGPT for the Harappan language."
    authorship_info: str = "HarappanChatGPTProcess using OpenAI GPT models."


class HatticChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xht"
    description: str = "Default process for ChatGPT for the Hattic language."
    authorship_info: str = "HatticChatGPTProcess using OpenAI GPT models."


class HernicanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xhr"
    description: str = "Default process for ChatGPT for the Hernican language."
    authorship_info: str = "HernicanChatGPTProcess using OpenAI GPT models."


class HibernoScottishGaelicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ghc"
    description: str = (
        "Default process for ChatGPT for the Hiberno-Scottish Gaelic language."
    )
    authorship_info: str = (
        "Hiberno-Scottish GaelicChatGPTProcess using OpenAI GPT models."
    )


class HindiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "hind1269"
    description: str = "Default process for ChatGPT for the Hindi language."
    authorship_info: str = "HindiChatGPTProcess using OpenAI GPT models."


class KhariBoliChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "khad1239"
    description: str = (
        "Default process for ChatGPT for the Khari Boli dialect of Hindi."
    )
    authorship_info: str = "KhariBoliChatGPTProcess using OpenAI GPT models."


class BrajChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "braj1242"
    description: str = "Default process for ChatGPT for the Braj Bhasha language."
    authorship_info: str = "BrajChatGPTProcess using OpenAI GPT models."


class AwadhiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "awad1243"
    description: str = "Default process for ChatGPT for the Awadhi language."
    authorship_info: str = "AwadhiChatGPTProcess using OpenAI GPT models."


class HittiteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "hit1242"
    description: str = "Default process for ChatGPT for the Hittite language."
    authorship_info: str = "HittiteChatGPTProcess using OpenAI GPT models."


class HunnicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xhc"
    description: str = "Default process for ChatGPT for the Hunnic language."
    authorship_info: str = "HunnicChatGPTProcess using OpenAI GPT models."


class HurrianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xhu"
    description: str = "Default process for ChatGPT for the Hurrian language."
    authorship_info: str = "HurrianChatGPTProcess using OpenAI GPT models."


class IberianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xib"
    description: str = "Default process for ChatGPT for the Iberian language."
    authorship_info: str = "IberianChatGPTProcess using OpenAI GPT models."


class IllyrianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xil"
    description: str = "Default process for ChatGPT for the Illyrian language."
    authorship_info: str = "IllyrianChatGPTProcess using OpenAI GPT models."


class JutishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "jut"
    description: str = "Default process for ChatGPT for the Jutish language."
    authorship_info: str = "JutishChatGPTProcess using OpenAI GPT models."


class KajkavianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "kjv"
    description: str = "Default process for ChatGPT for the Kajkavian language."
    authorship_info: str = "KajkavianChatGPTProcess using OpenAI GPT models."


class KannadaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "kan"
    description: str = "Default process for ChatGPT for the Kannada language."
    authorship_info: str = "KannadaChatGPTProcess using OpenAI GPT models."


class KaraChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "zra"
    description: str = "Default process for ChatGPT for the Kara (Korea) language."
    authorship_info: str = "Kara (Korea)ChatGPTProcess using OpenAI GPT models."


class KarakhanidChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xqa"
    description: str = "Default process for ChatGPT for the Karakhanid language."
    authorship_info: str = "KarakhanidChatGPTProcess using OpenAI GPT models."


class KaskeanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "zsk"
    description: str = "Default process for ChatGPT for the Kaskean language."
    authorship_info: str = "KaskeanChatGPTProcess using OpenAI GPT models."


class KawiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "kaw"
    description: str = "Default process for ChatGPT for the Kawi language."
    authorship_info: str = "KawiChatGPTProcess using OpenAI GPT models."


class KhazarChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "zkz"
    description: str = "Default process for ChatGPT for the Khazar language."
    authorship_info: str = "KhazarChatGPTProcess using OpenAI GPT models."


class KhorezmianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "zkh"
    description: str = "Default process for ChatGPT for the Khorezmian language."
    authorship_info: str = "KhorezmianChatGPTProcess using OpenAI GPT models."


class KhotaneseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "khot1251"
    description: str = "Default process for ChatGPT for the Khotanese language."
    authorship_info: str = "KhotaneseChatGPTProcess using OpenAI GPT models."


class TumshuqeseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "tums1237"
    description: str = "Default process for ChatGPT for the Tumshuqese language."
    authorship_info: str = "TumshuqeseChatGPTProcess using OpenAI GPT models."


class KhwarezmianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xco"
    description: str = "Default process for ChatGPT for the Khwarezmian language."
    authorship_info: str = "KhwarezmianChatGPTProcess using OpenAI GPT models."


class KitanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "zkt"
    description: str = "Default process for ChatGPT for the Kitan language."
    authorship_info: str = "KitanChatGPTProcess using OpenAI GPT models."


class KoguryoChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "zkg"
    description: str = "Default process for ChatGPT for the Koguryo language."
    authorship_info: str = "KoguryoChatGPTProcess using OpenAI GPT models."


class LangobardicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lng"
    description: str = "Default process for ChatGPT for the Langobardic language."
    authorship_info: str = "LangobardicChatGPTProcess using OpenAI GPT models."


class LateEgyptianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "late1256"
    description: str = "Default process for ChatGPT for the Late Egyptian language."
    authorship_info: str = "Late Egyptian ChatGPTProcess using OpenAI GPT models."


class LatinChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lati1261"
    description: str = "Default process for ChatGPT for the Latin language."
    authorship_info: str = "LatinChatGPTProcess using OpenAI GPT models."


class LemnianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xle"
    description: str = "Default process for ChatGPT for the Lemnian language."
    authorship_info: str = "LemnianChatGPTProcess using OpenAI GPT models."


class LeponticChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xlp"
    description: str = "Default process for ChatGPT for the Lepontic language."
    authorship_info: str = "LeponticChatGPTProcess using OpenAI GPT models."


class LiburnianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xli"
    description: str = "Default process for ChatGPT for the Liburnian language."
    authorship_info: str = "LiburnianChatGPTProcess using OpenAI GPT models."


class LinearAChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lab"
    description: str = "Default process for ChatGPT for the Linear A language."
    authorship_info: str = "Linear AChatGPTProcess using OpenAI GPT models."


class LiteraryChineseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lite1248"
    description: str = "Default process for ChatGPT for the Literary Chinese language."
    authorship_info: str = "Literary ChineseChatGPTProcess using OpenAI GPT models."


class LusitanianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xls"
    description: str = "Default process for ChatGPT for the Lusitanian language."
    authorship_info: str = "LusitanianChatGPTProcess using OpenAI GPT models."


class LycianAChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lyci1241"
    description: str = "Default process for ChatGPT for the Lycian A language."
    authorship_info: str = "Lycian AChatGPTProcess using OpenAI GPT models."


class LydianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lydi1241"
    description: str = "Default process for ChatGPT for the Lydian language."
    authorship_info: str = "LydianChatGPTProcess using OpenAI GPT models."


class MaekChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "hmk"
    description: str = "Default process for ChatGPT for the Maek language."
    authorship_info: str = "MaekChatGPTProcess using OpenAI GPT models."


class MaharastriPrakritChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "maha1305"
    description: str = (
        "Default process for ChatGPT for the Maharastri Prakrit language."
    )
    authorship_info: str = "MaharastriPrakritChatGPTProcess using OpenAI GPT models."


class MalayalamChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "mal"
    description: str = "Default process for ChatGPT for the Malayalam language."
    authorship_info: str = "MalayalamChatGPTProcess using OpenAI GPT models."


class ManichaeanMiddlePersianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xmn"
    description: str = (
        "Default process for ChatGPT for the Manichaean Middle Persian language."
    )
    authorship_info: str = (
        "Manichaean Middle PersianChatGPTProcess using OpenAI GPT models."
    )


class MarrucinianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "umc"
    description: str = "Default process for ChatGPT for the Marrucinian language."
    authorship_info: str = "MarrucinianChatGPTProcess using OpenAI GPT models."


class MarsianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ims"
    description: str = "Default process for ChatGPT for the Marsian language."
    authorship_info: str = "MarsianChatGPTProcess using OpenAI GPT models."


class MedianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xme"
    description: str = "Default process for ChatGPT for the Median language."
    authorship_info: str = "MedianChatGPTProcess using OpenAI GPT models."


class MeroiticChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xmr"
    description: str = "Default process for ChatGPT for the Meroitic language."
    authorship_info: str = "MeroiticChatGPTProcess using OpenAI GPT models."


class MessapicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "cms"
    description: str = "Default process for ChatGPT for the Messapic language."
    authorship_info: str = "MessapicChatGPTProcess using OpenAI GPT models."


class MiddleArmenianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "axm"
    description: str = "Default process for ChatGPT for the Middle Armenian language."
    authorship_info: str = "Middle ArmenianChatGPTProcess using OpenAI GPT models."


class MiddleBretonChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldb1244"
    description: str = "Default process for ChatGPT for the Middle Breton language."
    authorship_info: str = "Middle BretonChatGPTProcess using OpenAI GPT models."


class MiddleChineseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "midd1344"
    description: str = "Default process for ChatGPT for the Middle Chinese language."
    authorship_info: str = "Middle ChineseChatGPTProcess using OpenAI GPT models."


class MiddleCornishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "corn1251"
    description: str = "Default process for ChatGPT for the Middle Cornish language."
    authorship_info: str = "Middle CornishChatGPTProcess using OpenAI GPT models."


class MiddleDutchChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "dum"
    description: str = "Default process for ChatGPT for the Middle Dutch language."
    authorship_info: str = "Middle DutchChatGPTProcess using OpenAI GPT models."


class MiddleEgyptianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "midd1369"
    description: str = "Default process for ChatGPT for the Middle Egyptian language."
    authorship_info: str = "Middle Egyptian ChatGPTProcess using OpenAI GPT models."


class MiddleEnglishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "midd1317"
    description: str = "Default process for ChatGPT for the Middle English language."
    authorship_info: str = "Middle EnglishChatGPTProcess using OpenAI GPT models."


class MiddleFrenchChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "midd1316"
    description: str = "Default process for ChatGPT for the Middle French language."
    authorship_info: str = "Middle FrenchChatGPTProcess using OpenAI GPT models."


class MiddleHighGermanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "midd1343"
    description: str = (
        "Default process for ChatGPT for the Middle High German language."
    )
    authorship_info: str = "Middle High GermanChatGPTProcess using OpenAI GPT models."


class MiddleHittiteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "htx"
    description: str = "Default process for ChatGPT for the Middle Hittite language."
    authorship_info: str = "Middle HittiteChatGPTProcess using OpenAI GPT models."


class MiddleIrishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "mga"
    description: str = (
        "Default process for ChatGPT for the Middle Irish (10-12th century) language."
    )
    authorship_info: str = (
        "Middle Irish (10-12th century)ChatGPTProcess using OpenAI GPT models."
    )


class MiddleKoreanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "okm"
    description: str = (
        "Default process for ChatGPT for the Middle Korean (10th-16th cent.) language."
    )
    authorship_info: str = (
        "Middle Korean (10th-16th cent.)ChatGPTProcess using OpenAI GPT models."
    )


class MiddleLowGermanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "gml"
    description: str = "Default process for ChatGPT for the Middle Low German language."
    authorship_info: str = "Middle Low GermanChatGPTProcess using OpenAI GPT models."


class MiddleMongolChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "midd1351"
    description: str = "Default process for ChatGPT for the Middle Mongol language."
    authorship_info: str = "Middle MongolChatGPTProcess using OpenAI GPT models."


class MiddleNewarChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "nwx"
    description: str = "Default process for ChatGPT for the Middle Newar language."
    authorship_info: str = "Middle NewarChatGPTProcess using OpenAI GPT models."


class MilyanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "imy"
    description: str = "Default process for ChatGPT for the Milyan language."
    authorship_info: str = "MilyanChatGPTProcess using OpenAI GPT models."


class MinaeanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "inm"
    description: str = "Default process for ChatGPT for the Minaean language."
    authorship_info: str = "MinaeanChatGPTProcess using OpenAI GPT models."


class MinoanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "omn"
    description: str = "Default process for ChatGPT for the Minoan language."
    authorship_info: str = "MinoanChatGPTProcess using OpenAI GPT models."


class MoabiteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "obm"
    description: str = "Default process for ChatGPT for the Moabite language."
    authorship_info: str = "MoabiteChatGPTProcess using OpenAI GPT models."


class MozarabicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "mxi"
    description: str = "Default process for ChatGPT for the Mozarabic language."
    authorship_info: str = "MozarabicChatGPTProcess using OpenAI GPT models."


class MycenaeanGreekChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "gmy"
    description: str = "Default process for ChatGPT for the Mycenaean Greek language."
    authorship_info: str = "Mycenaean GreekChatGPTProcess using OpenAI GPT models."


class MysianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "yms"
    description: str = "Default process for ChatGPT for the Mysian language."
    authorship_info: str = "MysianChatGPTProcess using OpenAI GPT models."


class NadruvianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ndf"
    description: str = "Default process for ChatGPT for the Nadruvian language."
    authorship_info: str = "NadruvianChatGPTProcess using OpenAI GPT models."


class NeoHittiteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "nei"
    description: str = "Default process for ChatGPT for the Neo-Hittite language."
    authorship_info: str = "Neo-HittiteChatGPTProcess using OpenAI GPT models."


class NoricChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "nrc"
    description: str = "Default process for ChatGPT for the Noric language."
    authorship_info: str = "NoricChatGPTProcess using OpenAI GPT models."


class NorthPiceneChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "nrp"
    description: str = "Default process for ChatGPT for the North Picene language."
    authorship_info: str = "North PiceneChatGPTProcess using OpenAI GPT models."


class NumidianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "nxm"
    description: str = "Default process for ChatGPT for the Numidian language."
    authorship_info: str = "NumidianChatGPTProcess using OpenAI GPT models."


class OdiaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oriy1255"
    description: str = "Default process for ChatGPT for the Odia language."
    authorship_info: str = "OdiaChatGPTProcess using OpenAI GPT models."


class OfficialAramaicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "impe1235"
    description: str = (
        "Default process for ChatGPT for the Official Aramaic (700-300 BCE) language."
    )
    authorship_info: str = (
        "Official Aramaic (700-300 BCE) ChatGPTProcess using OpenAI GPT models."
    )


class OldAramaicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oar"
    description: str = (
        "Default process for ChatGPT for the Old Aramaic (up to 700 BCE) language."
    )
    authorship_info: str = (
        "Old Aramaic (up to 700 BCE)ChatGPTProcess using OpenAI GPT models."
    )


class OldAvarChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oav"
    description: str = "Default process for ChatGPT for the Old Avar language."
    authorship_info: str = "Old AvarChatGPTProcess using OpenAI GPT models."


class OldBretonChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "obt"
    description: str = "Default process for ChatGPT for the Old Breton language."
    authorship_info: str = "Old BretonChatGPTProcess using OpenAI GPT models."


class OldBurmeseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldb1235"
    description: str = "Default process for ChatGPT for the Old Burmese language."
    authorship_info: str = "Old BurmeseChatGPTProcess using OpenAI GPT models."


class OldChineseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldc1244"
    description: str = "Default process for ChatGPT for the Old Chinese language."
    authorship_info: str = "Old ChineseChatGPTProcess using OpenAI GPT models."


class BaihuaChineseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "clas1255"
    description: str = (
        "Default process for ChatGPT for Early Vernacular Chinese (Baihua)."
    )
    authorship_info: str = "BaihuaChineseChatGPTProcess using OpenAI GPT models."


class ClassicalBurmeseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "nucl1310"
    description: str = "Default process for ChatGPT for the Classical Burmese language."
    authorship_info: str = "ClassicalBurmeseChatGPTProcess using OpenAI GPT models."


class TangutChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "tang1334"
    description: str = "Default process for ChatGPT for the Tangut (Xixia) language."
    authorship_info: str = "TangutChatGPTProcess using OpenAI GPT models."


class NewarChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "newa1246"
    description: str = (
        "Default process for ChatGPT for the Newar (Classical Nepal Bhasa) language."
    )
    authorship_info: str = "NewarChatGPTProcess using OpenAI GPT models."


class MeiteiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "mani1292"
    description: str = (
        "Default process for ChatGPT for the Meitei (Classical Manipuri) language."
    )
    authorship_info: str = "MeiteiChatGPTProcess using OpenAI GPT models."


class SgawKarenChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "sgaw1245"
    description: str = "Default process for ChatGPT for the Sgaw Karen language."
    authorship_info: str = "SgawKarenChatGPTProcess using OpenAI GPT models."


class MogholiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "mogh1245"
    description: str = "Default process for ChatGPT for the Mogholi (Moghol) language."
    authorship_info: str = "MogholiChatGPTProcess using OpenAI GPT models."


class OldCornishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oco"
    description: str = "Default process for ChatGPT for the Old Cornish language."
    authorship_info: str = "Old CornishChatGPTProcess using OpenAI GPT models."


class OldDutchOldFrankishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "odt"
    description: str = (
        "Default process for ChatGPT for the Old Dutch-Old Frankish language."
    )
    authorship_info: str = (
        "Old Dutch-Old FrankishChatGPTProcess using OpenAI GPT models."
    )


class OldEgyptianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "olde1242"
    description: str = "Default process for ChatGPT for the Old Egyptian language."
    authorship_info: str = "Old Egyptian ChatGPTProcess using OpenAI GPT models."


class OldEnglishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "olde1238"
    description: str = (
        "Default process for ChatGPT for the Old English (ca. 450-1100) language."
    )
    authorship_info: str = (
        "Old English (ca. 450-1100)ChatGPTProcess using OpenAI GPT models."
    )


class OldFrankishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "frk"
    description: str = "Default process for ChatGPT for the Old Frankish language."
    authorship_info: str = "Old FrankishChatGPTProcess using OpenAI GPT models."


class OldFrenchChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldf1239"
    description: str = (
        "Default process for ChatGPT for the Old French (842-ca. 1400) language."
    )
    authorship_info: str = (
        "Old French (842-ca. 1400)ChatGPTProcess using OpenAI GPT models."
    )


class OldFrisianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ofs"
    description: str = "Default process for ChatGPT for the Old Frisian language."
    authorship_info: str = "Old FrisianChatGPTProcess using OpenAI GPT models."


class OldGeorgianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oge"
    description: str = "Default process for ChatGPT for the Old Georgian language."
    authorship_info: str = "Old GeorgianChatGPTProcess using OpenAI GPT models."


class OldHighGermanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "goh"
    description: str = (
        "Default process for ChatGPT for the Old High German (ca. 750-1050) language."
    )
    authorship_info: str = (
        "Old High German (ca. 750-1050)ChatGPTProcess using OpenAI GPT models."
    )


class OldHittiteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oht"
    description: str = "Default process for ChatGPT for the Old Hittite language."
    authorship_info: str = "Old HittiteChatGPTProcess using OpenAI GPT models."


class OldHungarianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ohu"
    description: str = "Default process for ChatGPT for the Old Hungarian language."
    authorship_info: str = "Old HungarianChatGPTProcess using OpenAI GPT models."


class EarlyIrishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldi1245"
    description: str = "Default process for ChatGPT for the Old Irish language."
    authorship_info: str = "Old IrishChatGPTProcess using OpenAI GPT models."


class OldJapaneseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ojp"
    description: str = "Default process for ChatGPT for the Old Japanese language."
    authorship_info: str = "Old JapaneseChatGPTProcess using OpenAI GPT models."


class OldKoreanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oko"
    description: str = (
        "Default process for ChatGPT for the Old Korean (3rd-9th cent.) language."
    )
    authorship_info: str = (
        "Old Korean (3rd-9th cent.)ChatGPTProcess using OpenAI GPT models."
    )


class OldLithuanianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "olt"
    description: str = "Default process for ChatGPT for the Old Lithuanian language."
    authorship_info: str = "Old LithuanianChatGPTProcess using OpenAI GPT models."


class OldManipuriChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "omp"
    description: str = "Default process for ChatGPT for the Old Manipuri language."
    authorship_info: str = "Old ManipuriChatGPTProcess using OpenAI GPT models."


class OldMarathiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "omr"
    description: str = "Default process for ChatGPT for the Old Marathi language."
    authorship_info: str = "Old MarathiChatGPTProcess using OpenAI GPT models."


class MarathiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "mara1378"
    description: str = "Default process for ChatGPT for the Marathi language."
    authorship_info: str = "MarathiChatGPTProcess using OpenAI GPT models."


class OldMonChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "omx"
    description: str = "Default process for ChatGPT for the Old Mon language."
    authorship_info: str = "Old MonChatGPTProcess using OpenAI GPT models."


class OldNorseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "non"
    description: str = "Default process for ChatGPT for the Old Norse language."
    authorship_info: str = "Old NorseChatGPTProcess using OpenAI GPT models."


class OldNubianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "onw"
    description: str = "Default process for ChatGPT for the Old Nubian language."
    authorship_info: str = "Old NubianChatGPTProcess using OpenAI GPT models."


class OldOsseticChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oos"
    description: str = "Default process for ChatGPT for the Old Ossetic language."
    authorship_info: str = "Old OsseticChatGPTProcess using OpenAI GPT models."


class OldPersianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldp1254"
    description: str = (
        "Default process for ChatGPT for the Old Persian (ca. 600-400 B.C.) language."
    )
    authorship_info: str = (
        "Old Persian (ca. 600-400 B.C.)ChatGPTProcess using OpenAI GPT models."
    )


class OldProvençalChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pro"
    description: str = "Default process for ChatGPT for the Old Provençal language."
    authorship_info: str = "Old ProvençalChatGPTProcess using OpenAI GPT models."


class OldRussianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "orv"
    description: str = "Default process for ChatGPT for the Old Russian language."
    authorship_info: str = "Old RussianChatGPTProcess using OpenAI GPT models."


class OldSaxonChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "osx"
    description: str = "Default process for ChatGPT for the Old Saxon language."
    authorship_info: str = "Old SaxonChatGPTProcess using OpenAI GPT models."


class OldSpanishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "osp"
    description: str = "Default process for ChatGPT for the Old Spanish language."
    authorship_info: str = "Old SpanishChatGPTProcess using OpenAI GPT models."


class OldTamilChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oty"
    description: str = "Default process for ChatGPT for the Old Tamil language."
    authorship_info: str = "Old TamilChatGPTProcess using OpenAI GPT models."


class OldTibetanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "otb"
    description: str = "Default process for ChatGPT for the Old Tibetan language."
    authorship_info: str = "Old TibetanChatGPTProcess using OpenAI GPT models."


class OldTurkicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oui"
    description: str = "Default process for ChatGPT for the Old Turkic language."
    authorship_info: str = "Old TurkicChatGPTProcess using OpenAI GPT models."


class OldTurkishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "otk"
    description: str = "Default process for ChatGPT for the Old Turkish language."
    authorship_info: str = "Old TurkishChatGPTProcess using OpenAI GPT models."


class OldMiddleWelshChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldw1239"
    description: str = "Default process for ChatGPT for the Old-Middle Welsh language."
    authorship_info: str = "Old-Middle WelshChatGPTProcess using OpenAI GPT models."


class OscanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "osc"
    description: str = "Default process for ChatGPT for the Oscan language."
    authorship_info: str = "OscanChatGPTProcess using OpenAI GPT models."


class OttomanTurkishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ota"
    description: str = (
        "Default process for ChatGPT for the Ottoman Turkish (1500-1928) language."
    )
    authorship_info: str = (
        "Ottoman Turkish (1500-1928)ChatGPTProcess using OpenAI GPT models."
    )


class PaekcheChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pkc"
    description: str = "Default process for ChatGPT for the Paekche language."
    authorship_info: str = "PaekcheChatGPTProcess using OpenAI GPT models."


class PaelignianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pgn"
    description: str = "Default process for ChatGPT for the Paelignian language."
    authorship_info: str = "PaelignianChatGPTProcess using OpenAI GPT models."


class ParthianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "part1239"
    description: str = "Default process for ChatGPT for the Parthian language."
    authorship_info: str = "ParthianChatGPTProcess using OpenAI GPT models."


class MiddlePersianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pahl1241"
    description: str = "Default process for ChatGPT for the Middle Persian language."
    authorship_info: str = "MiddlePersianChatGPTProcess using OpenAI GPT models."


class PalaicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pala1331"
    description: str = "Default process for ChatGPT for the Palaic language."
    authorship_info: str = "PalaicChatGPTProcess using OpenAI GPT models."


class PalauanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pau"
    description: str = "Default process for ChatGPT for the Palauan language."
    authorship_info: str = "PalauanChatGPTProcess using OpenAI GPT models."


class PaliChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pali1273"
    description: str = "Default process for ChatGPT for the Pali language."
    authorship_info: str = "PaliChatGPTProcess using OpenAI GPT models."


class PampangaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pam"
    description: str = "Default process for ChatGPT for the Pampanga language."
    authorship_info: str = "PampangaChatGPTProcess using OpenAI GPT models."


class PashtoChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pus"
    description: str = "Default process for ChatGPT for the Pashto language."
    authorship_info: str = "PashtoChatGPTProcess using OpenAI GPT models."


class PersianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pes"
    description: str = "Default process for ChatGPT for the Persian language."
    authorship_info: str = "PersianChatGPTProcess using OpenAI GPT models."


class PhoenicianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "phoe1239"
    description: str = "Default process for ChatGPT for the Phoenician language."
    authorship_info: str = "PhoenicianChatGPTProcess using OpenAI GPT models."


class PicardChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pic"
    description: str = "Default process for ChatGPT for the Picard language."
    authorship_info: str = "PicardChatGPTProcess using OpenAI GPT models."


class PolishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pol"
    description: str = "Default process for ChatGPT for the Polish language."
    authorship_info: str = "PolishChatGPTProcess using OpenAI GPT models."


class PortugueseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "por"
    description: str = "Default process for ChatGPT for the Portuguese language."
    authorship_info: str = "PortugueseChatGPTProcess using OpenAI GPT models."


class ProvençalChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pro"
    description: str = "Default process for ChatGPT for the Provençal language."
    authorship_info: str = "ProvençalChatGPTProcess using OpenAI GPT models."


class PunjabiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default process for ChatGPT for the Punjabi language."
    authorship_info: str = "PunjabiChatGPTProcess using OpenAI GPT models."


class QashqaiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xqs"
    description: str = "Default process for ChatGPT for the Qashqai language."
    authorship_info: str = "QashqaiChatGPTProcess using OpenAI GPT models."


class QuechuaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "que"
    description: str = "Default process for ChatGPT for the Quechua language."
    authorship_info: str = "QuechuaChatGPTProcess using OpenAI GPT models."


class RarotonganChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "rar"
    description: str = "Default process for ChatGPT for the Rarotongan language."
    authorship_info: str = "RarotonganChatGPTProcess using OpenAI GPT models."


class RomanianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ron"
    description: str = "Default process for ChatGPT for the Romanian language."
    authorship_info: str = "RomanianChatGPTProcess using OpenAI GPT models."


class AssameseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "assa1263"
    description: str = "Default process for ChatGPT for the Assamese language."
    authorship_info: str = "AssameseChatGPTProcess using OpenAI GPT models."


class SinhalaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "sinh1246"
    description: str = "Default process for ChatGPT for the Sinhala language."
    authorship_info: str = "SinhalaChatGPTProcess using OpenAI GPT models."


class SindhiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "sind1272"
    description: str = "Default process for ChatGPT for the Sindhi language."
    authorship_info: str = "SindhiChatGPTProcess using OpenAI GPT models."


class KashmiriChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "kash1277"
    description: str = "Default process for ChatGPT for the Kashmiri language."
    authorship_info: str = "KashmiriChatGPTProcess using OpenAI GPT models."


class BagriChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "bagr1243"
    description: str = (
        "Default process for ChatGPT for the Bagri (Rajasthani) language."
    )
    authorship_info: str = "BagriChatGPTProcess using OpenAI GPT models."


class RussianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "rus"
    description: str = "Default process for ChatGPT for the Russian language."
    authorship_info: str = "RussianChatGPTProcess using OpenAI GPT models."


class SardinianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "srd"
    description: str = "Default process for ChatGPT for the Sardinian language."
    authorship_info: str = "SardinianChatGPTProcess using OpenAI GPT models."


class ClassicalSanskritChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "clas1258"
    description: str = (
        "Default process for ChatGPT for the Classical Sanskrit language."
    )
    authorship_info: str = "ClassicalSanskritChatGPTProcess using OpenAI GPT models."


class VedicSanskritChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "vedi1234"
    description: str = "Default process for ChatGPT for the Vedic Sanskrit language."
    authorship_info: str = "VedicSanskritChatGPTProcess using OpenAI GPT models."


class ScottishGaelicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "gla"
    description: str = "Default process for ChatGPT for the Scottish Gaelic language."
    authorship_info: str = "Scottish GaelicChatGPTProcess using OpenAI GPT models."


class SerbianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "srp"
    description: str = "Default process for ChatGPT for the Serbian language."
    authorship_info: str = "SerbianChatGPTProcess using OpenAI GPT models."


class SicilianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "scn"
    description: str = "Default process for ChatGPT for the Sicilian language."
    authorship_info: str = "SicilianChatGPTProcess using OpenAI GPT models."


class SilesianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "szl"
    description: str = "Default process for ChatGPT for the Silesian language."
    authorship_info: str = "SilesianChatGPTProcess using OpenAI GPT models."


class SlovakChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "slk"
    description: str = "Default process for ChatGPT for the Slovak language."
    authorship_info: str = "SlovakChatGPTProcess using OpenAI GPT models."


class SlovenianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "slv"
    description: str = "Default process for ChatGPT for the Slovenian language."
    authorship_info: str = "SlovenianChatGPTProcess using OpenAI GPT models."


class SomaliChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "som"
    description: str = "Default process for ChatGPT for the Somali language."
    authorship_info: str = "SomaliChatGPTProcess using OpenAI GPT models."


class SorbianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "wen"
    description: str = "Default process for ChatGPT for the Sorbian language."
    authorship_info: str = "SorbianChatGPTProcess using OpenAI GPT models."


class SpanishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "spa"
    description: str = "Default process for ChatGPT for the Spanish language."
    authorship_info: str = "SpanishChatGPTProcess using OpenAI GPT models."


class SumerianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "sux"
    description: str = "Default process for ChatGPT for the Sumerian language."
    authorship_info: str = "SumerianChatGPTProcess using OpenAI GPT models."


class SwedishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "swe"
    description: str = "Default process for ChatGPT for the Swedish language."
    authorship_info: str = "SwedishChatGPTProcess using OpenAI GPT models."


class SyriacChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "syc"
    description: str = "Default process for ChatGPT for the Syriac language."
    authorship_info: str = "SyriacChatGPTProcess using OpenAI GPT models."


class TahitianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "tah"
    description: str = "Default process for ChatGPT for the Tahitian language."
    authorship_info: str = "TahitianChatGPTProcess using OpenAI GPT models."


class TigrinyaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "tir"
    description: str = "Default process for ChatGPT for the Tigrinya language."
    authorship_info: str = "TigrinyaChatGPTProcess using OpenAI GPT models."


class TibetanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "bod"
    description: str = "Default process for ChatGPT for the Tibetan language."
    authorship_info: str = "TibetanChatGPTProcess using OpenAI GPT models."


class TigréChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "tig"
    description: str = "Default process for ChatGPT for the Tigré language."
    authorship_info: str = "TigréChatGPTProcess using OpenAI GPT models."


class TokharianAChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "toch1238"
    description: str = "Default process for ChatGPT for the Tokharian A language."
    authorship_info: str = "Tokharian AChatGPTProcess using OpenAI GPT models."


class TokharianBChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "toch1237"
    description: str = "Default process for ChatGPT for the Tokharian B language."
    authorship_info: str = "Tokharian BChatGPTProcess using OpenAI GPT models."


class TurkishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "tur"
    description: str = "Default process for ChatGPT for the Turkish language."
    authorship_info: str = "TurkishChatGPTProcess using OpenAI GPT models."


class UgariticChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ugar1238"
    description: str = "Default process for ChatGPT for the Ugaritic language."
    authorship_info: str = "UgariticChatGPTProcess using OpenAI GPT models."


class UighurChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "uig"
    description: str = "Default process for ChatGPT for the Uighur language."
    authorship_info: str = "UighurChatGPTProcess using OpenAI GPT models."


class UkrainianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ukr"
    description: str = "Default process for ChatGPT for the Ukrainian language."
    authorship_info: str = "UkrainianChatGPTProcess using OpenAI GPT models."


class UrduChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "urdu1245"
    description: str = "Default process for ChatGPT for the Urdu language."
    authorship_info: str = "UrduChatGPTProcess using OpenAI GPT models."


class UzbekChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "uz"
    description: str = "Default process for ChatGPT for the Uzbek language."
    authorship_info: str = "UzbekChatGPTProcess using OpenAI GPT models."


class VietnameseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "vie"
    description: str = "Default process for ChatGPT for the Vietnamese language."
    authorship_info: str = "VietnameseChatGPTProcess using OpenAI GPT models."


class WelshChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "cy"
    description: str = "Default process for ChatGPT for the Welsh language."
    authorship_info: str = "WelshChatGPTProcess using OpenAI GPT models."


class WolofChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "wo"
    description: str = "Default process for ChatGPT for the Wolof language."
    authorship_info: str = "WolofChatGPTProcess using OpenAI GPT models."


class XhosaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "xh"
    description: str = "Default process for ChatGPT for the Xhosa language."
    authorship_info: str = "XhosaChatGPTProcess using OpenAI GPT models."


class YorubaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "yo"
    description: str = "Default process for ChatGPT for the Yoruba language."
    authorship_info: str = "YorubaChatGPTProcess using OpenAI GPT models."


class ZazaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "zza"
    description: str = "Default process for ChatGPT for the Zaza language."
    authorship_info: str = "ZazaChatGPTProcess using OpenAI GPT models."


class ZenagaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "zen"
    description: str = "Default process for ChatGPT for the Zenaga language."
    authorship_info: str = "ZenagaChatGPTProcess using OpenAI GPT models."


class ZuluChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "zu"
    description: str = "Default process for ChatGPT for the Zulu language."
    authorship_info: str = "ZuluChatGPTProcess using OpenAI GPT models."


class SauraseniPrakritChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "saur1252"
    description: str = "Default process for ChatGPT for the Sauraseni Prakrit language."
    authorship_info: str = "SauraseniPrakritChatGPTProcess using OpenAI GPT models."


## Duplicate of MaharastriPrakritChatGPTProcess; removing to avoid redefinition


class MagadhiPrakritChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "maga1260"
    description: str = "Default process for ChatGPT for the Magadhi Prakrit language."
    authorship_info: str = "MagadhiPrakritChatGPTProcess using OpenAI GPT models."


class GandhariChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "gand1259"
    description: str = "Default process for ChatGPT for the Gandhari language."
    authorship_info: str = "GandhariChatGPTProcess using OpenAI GPT models."
