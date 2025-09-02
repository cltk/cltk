"""ChatGPT-backed process classes for CLTK.

This module defines :class:`ChatGPTProcess`, a generic :class:`~cltk.core.data_types.Process`
that initializes a :class:`~cltk.genai.chatgpt.ChatGPT` client for a given
language (Glottolog code) and enriches a document with LLM‑produced
annotations. It also exposes many thin per‑language subclasses that set
``glottolog_id`` and human‑readable descriptions.

TODO: Consider adding the following:
- OttomanTurkishChatGPTProcess
- OscanChatGPTProcess
- OldTibetanChatGPTProcess: otb
- OldTurkishChatGPTProcess
- OldAvarChatGPTProcess: oav
- OldBretonChatGPTProcess: obt
- OldCornishChatGPTProcess: oco
- OldDutchOldFrankishChatGPTProcess: odt
- OldFrankishChatGPTProcess: frk
- OldFrisianChatGPTProcess: ofs
- OldGeorgianChatGPTProcess: oge
- OldHittiteChatGPTProcess: oht
- OldKoreanChatGPTProcess: oko
- OldLithuanianChatGPTProcess: olt
- OldManipuriChatGPTProcess: omp
- OldMarathiChatGPTProcess: omr
- OldMonChatGPTProcess: omx
- OldNubianChatGPTProcess: onw
- OldOsseticChatGPTProcess: oos
- OldProvençalChatGPTProcess: pro
- OldRussianChatGPTProcess: orv
- OldSaxonChatGPTProcess: osx
- OldSpanishChatGPTProcess: osp
- MycenaeanGreekChatGPTProcess: gmy
MiddleDutchChatGPTProcess: dum
MiddleHittiteChatGPTProcess: htx
MiddleIrishChatGPTProcess: mga
MiddleKoreanChatGPTProcess: okm
MiddleLowGermanChatGPTProcess: gml
MiddleNewarChatGPTProcess: nwx
- KhazarChatGPTProcess: zkz
- IllyrianChatGPTProcess: xil
HunnicChatGPTProcess: xhc
HibernoScottishGaelicChatGPTProcess: ghc
EtruscanChatGPTProcess: ett
FaliscanChatGPTProcess: xfa
- ElamiteChatGPTProcess: elx
AncientLigurianChatGPTProcess: xlg
AncientMacedonianChatGPTProcess: xmk
AncientNorthArabianChatGPTProcess: xna
AncientZapotecChatGPTProcess: xzp
AndalusianArabicChatGPTProcess: xaa
AngloNormanChatGPTProcess: xno
"""

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
    """ChatGPT-backed linguistic annotation process.

    This process initializes a ChatGPT client for a given language (by
    Glottolog ID) and enriches a CLTK ``Doc`` with token-level and document-level
    metadata produced by the model.

    Attributes:
      glottolog_id: Target language Glottolog code (e.g., ``lati1261``).
      api_key: OpenAI API key. Loaded from ``OPENAI_API_KEY`` if not provided.
      model: Model alias to use (see ``AVAILABILE_MODELS``).
      temperature: Sampling temperature for generation.
      description: Human-friendly description of the process.
      authorship_info: Short attribution string for provenance.
      chatgpt: Initialized ChatGPT client instance, or ``None`` if not ready.

    """

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
        """Finalize initialization and configure the ChatGPT client.

        Loads environment variables (including ``OPENAI_API_KEY`` if not
        explicitly set), validates that both ``glottolog_id`` and ``api_key``
        are present, and constructs the ``chatgpt`` client. When required
        configuration is missing, leaves ``chatgpt`` as ``None`` and logs an
        appropriate warning. Finally, invokes ``on_initialized()`` as a
        subclass hook.

        Args:
            __context: Pydantic post-init context (unused).

        Returns:
            None

        """
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
        """Return a copy of ``input_doc`` enriched with ChatGPT annotations.

        Args:
          input_doc: Document with ``normalized_text`` (and sentence boundaries
            for token-level annotation) to be enriched.

        Returns:
          A ``Doc`` containing the original fields plus ChatGPT-produced
          annotations (e.g., tokens with UD features) and usage metadata.

        Raises:
          ValueError: If the process is not initialized (missing API key or
            language), or if the input document lacks usable text.
          CLTKException: If the document does not contain text in the expected
            fields.

        """
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


class AkkadianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "akka1240"
    description: str = "Default process for ChatGPT for the Akkadian language."
    authorship_info: str = "AkkadianChatGPTProcess using OpenAI GPT models."


class AncientGreekChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "anci1242"
    description: str = "Default process for ChatGPT for the Ancient Greek language."
    authorship_info: str = "Ancient GreekChatGPTProcess using OpenAI GPT models."


class BiblicalHebrewChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "anci1244"
    description: str = "Default process for ChatGPT for the Biblical Hebrew language."
    authorship_info: str = "Biblical HebrewChatGPTProcess using OpenAI GPT models."


class ClassicalArabicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "clas1259"
    description: str = "Default process for ChatGPT for the Classical Arabic language."
    authorship_info: str = "ClassicalArabicChatGPTProcess using OpenAI GPT models."


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


class CarianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "cari1274"
    description: str = "Default process for ChatGPT for the Carian language."
    authorship_info: str = "CarianChatGPTProcess using OpenAI GPT models."


class ChurchSlavicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "chur1257"
    description: str = "Default process for ChatGPT for the Church Slavic language."
    authorship_info: str = "Church SlavicChatGPTProcess using OpenAI GPT models."


class ClassicalArmenianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "clas1256"
    description: str = (
        "Default process for ChatGPT for the Classical Armenian language."
    )
    authorship_info: str = "Classical ArmenianChatGPTProcess using OpenAI GPT models."


class ClassicalMandaicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "clas1253"
    description: str = "Default process for ChatGPT for the Classical Mandaic language."
    authorship_info: str = "Classical MandaicChatGPTProcess using OpenAI GPT models."


class ClassicalMongolianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "mong1331"
    description: str = (
        "Default process for ChatGPT for the Classical Mongolian language."
    )
    authorship_info: str = "Classical MongolianChatGPTProcess using OpenAI GPT models."


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


class DemoticChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "demo1234"
    description: str = "Default process for ChatGPT for the Demotic language."
    authorship_info: str = "DemoticChatGPTProcess using OpenAI GPT models."


class EasternPanjabiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default process for ChatGPT for the Eastern Panjabi language."
    authorship_info: str = "Eastern PanjabiChatGPTProcess using OpenAI GPT models."


class EdomiteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "edom1234"
    description: str = "Default process for ChatGPT for the Edomite language."
    authorship_info: str = "EdomiteChatGPTProcess using OpenAI GPT models."


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
    glottolog_id: Optional[str] = "hitt1242"
    description: str = "Default process for ChatGPT for the Hittite language."
    authorship_info: str = "HittiteChatGPTProcess using OpenAI GPT models."


class KhotaneseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "khot1251"
    description: str = "Default process for ChatGPT for the Khotanese language."
    authorship_info: str = "KhotaneseChatGPTProcess using OpenAI GPT models."


class TumshuqeseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "tums1237"
    description: str = "Default process for ChatGPT for the Tumshuqese language."
    authorship_info: str = "TumshuqeseChatGPTProcess using OpenAI GPT models."


class LateEgyptianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "late1256"
    description: str = "Default process for ChatGPT for the Late Egyptian language."
    authorship_info: str = "Late Egyptian ChatGPTProcess using OpenAI GPT models."


class LatinChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lati1261"
    description: str = "Default process for ChatGPT for the Latin language."
    authorship_info: str = "LatinChatGPTProcess using OpenAI GPT models."


class LiteraryChineseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lite1248"
    description: str = "Default process for ChatGPT for the Literary Chinese language."
    authorship_info: str = "Literary ChineseChatGPTProcess using OpenAI GPT models."


class LycianAChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lyci1241"
    description: str = "Default process for ChatGPT for the Lycian A language."
    authorship_info: str = "Lycian AChatGPTProcess using OpenAI GPT models."


class LydianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "lydi1241"
    description: str = "Default process for ChatGPT for the Lydian language."
    authorship_info: str = "LydianChatGPTProcess using OpenAI GPT models."


class MaharastriPrakritChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "maha1305"
    description: str = (
        "Default process for ChatGPT for the Maharastri Prakrit language."
    )
    authorship_info: str = "MaharastriPrakritChatGPTProcess using OpenAI GPT models."


class MiddleArmenianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "midd1364"
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


class MiddleMongolChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "mong1329"
    description: str = "Default process for ChatGPT for the Middle Mongol language."
    authorship_info: str = "Middle MongolChatGPTProcess using OpenAI GPT models."


class MoabiteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "moab1234"
    description: str = "Default process for ChatGPT for the Moabite language."
    authorship_info: str = "MoabiteChatGPTProcess using OpenAI GPT models."


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


class NumidianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "numi1241"
    description: str = (
        "Default process for ChatGPT for the Numidian (Ancient Berber) language."
    )
    authorship_info: str = "NumidianChatGPTProcess using OpenAI GPT models."


class TaitaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "tait1247"
    description: str = "Default process for ChatGPT for the Cushitic Taita language."
    authorship_info: str = "TaitaChatGPTProcess using OpenAI GPT models."


class HausaChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "haus1257"
    description: str = "Default process for ChatGPT for the Hausa language."
    authorship_info: str = "HausaChatGPTProcess using OpenAI GPT models."


class OldJurchenChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "jurc1239"
    description: str = "Default process for ChatGPT for the Old Jurchen language."
    authorship_info: str = "OldJurchenChatGPTProcess using OpenAI GPT models."


class OldJapaneseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "japo1237"
    description: str = "Default process for ChatGPT for the Old Japanese language."
    authorship_info: str = "OldJapaneseChatGPTProcess using OpenAI GPT models."


class OldHungarianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldh1242"
    description: str = "Default process for ChatGPT for the Old Hungarian language."
    authorship_info: str = "OldHungarianChatGPTProcess using OpenAI GPT models."


class ChagataiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "chag1247"
    description: str = "Default process for ChatGPT for the Chagatai language."
    authorship_info: str = "ChagataiChatGPTProcess using OpenAI GPT models."


class OldTurkicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldu1238"
    description: str = "Default process for ChatGPT for the Old Turkic language."
    authorship_info: str = "OldTurkicChatGPTProcess using OpenAI GPT models."


class OldTamilChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldt1248"
    description: str = "Default process for ChatGPT for the Old Tamil language."
    authorship_info: str = "OldTamilChatGPTProcess using OpenAI GPT models."


class AmmoniteChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ammo1234"
    description: str = "Default process for ChatGPT for the Ammonite language."
    authorship_info: str = "AmmoniteChatGPTProcess using OpenAI GPT models."


class OldAramaicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "olda1246"
    description: str = (
        "Default process for ChatGPT for the Old Aramaic (up to 700 BCE) language."
    )
    authorship_info: str = "OldAramaicChatGPTProcess using OpenAI GPT models."


class OldAramaicSamalianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "olda1245"
    description: str = (
        "Default process for ChatGPT for the Old Aramaic–Samʾalian language."
    )
    authorship_info: str = "OldAramaicSamalianChatGPTProcess using OpenAI GPT models."


class MiddleAramaicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "midd1366"
    description: str = "Default process for ChatGPT for the Middle Aramaic language."
    authorship_info: str = "MiddleAramaicChatGPTProcess using OpenAI GPT models."


class HatranChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "hatr1234"
    description: str = "Default process for ChatGPT for the Hatran language."
    authorship_info: str = "HatranChatGPTProcess using OpenAI GPT models."


class JewishBabylonianAramaicChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "jewi1240"
    description: str = (
        "Default process for ChatGPT for the Jewish Babylonian Aramaic language."
    )
    authorship_info: str = (
        "JewishBabylonianAramaicChatGPTProcess using OpenAI GPT models."
    )


class SamalianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "sama1234"
    description: str = "Default process for ChatGPT for the Samʾalian language."
    authorship_info: str = "SamalianChatGPTProcess using OpenAI GPT models."


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


class OldFrenchChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldf1239"
    description: str = (
        "Default process for ChatGPT for the Old French (842-ca. 1400) language."
    )
    authorship_info: str = (
        "Old French (842-ca. 1400)ChatGPTProcess using OpenAI GPT models."
    )


class OldHighGermanChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldh1241"
    description: str = (
        "Default process for ChatGPT for the Old High German (ca. 750-1050) language."
    )
    authorship_info: str = (
        "Old High German (ca. 750-1050)ChatGPTProcess using OpenAI GPT models."
    )


class EarlyIrishChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldi1245"
    description: str = "Default process for ChatGPT for the Old Irish language."
    authorship_info: str = "Old IrishChatGPTProcess using OpenAI GPT models."


class MarathiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "mara1378"
    description: str = "Default process for ChatGPT for the Marathi language."
    authorship_info: str = "MarathiChatGPTProcess using OpenAI GPT models."


class OldNorseChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldn1244"
    description: str = "Default process for ChatGPT for the Old Norse language."
    authorship_info: str = "Old NorseChatGPTProcess using OpenAI GPT models."


class OldPersianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldp1254"
    description: str = (
        "Default process for ChatGPT for the Old Persian (ca. 600-400 B.C.) language."
    )
    authorship_info: str = (
        "Old Persian (ca. 600-400 B.C.)ChatGPTProcess using OpenAI GPT models."
    )


class OldMiddleWelshChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "oldw1239"
    description: str = "Default process for ChatGPT for the Old-Middle Welsh language."
    authorship_info: str = "Old-Middle WelshChatGPTProcess using OpenAI GPT models."


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


class PaliChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "pali1273"
    description: str = "Default process for ChatGPT for the Pali language."
    authorship_info: str = "PaliChatGPTProcess using OpenAI GPT models."


class PhoenicianChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "phoe1239"
    description: str = "Default process for ChatGPT for the Phoenician language."
    authorship_info: str = "PhoenicianChatGPTProcess using OpenAI GPT models."


class PunjabiChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "panj1256"
    description: str = "Default process for ChatGPT for the Punjabi language."
    authorship_info: str = "PunjabiChatGPTProcess using OpenAI GPT models."


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


class TokharianAChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "toch1238"
    description: str = "Default process for ChatGPT for the Tokharian A language."
    authorship_info: str = "Tokharian AChatGPTProcess using OpenAI GPT models."


class TokharianBChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "toch1237"
    description: str = "Default process for ChatGPT for the Tokharian B language."
    authorship_info: str = "Tokharian BChatGPTProcess using OpenAI GPT models."


class UgariticChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "ugar1238"
    description: str = "Default process for ChatGPT for the Ugaritic language."
    authorship_info: str = "UgariticChatGPTProcess using OpenAI GPT models."


class UrduChatGPTProcess(ChatGPTProcess):
    glottolog_id: Optional[str] = "urdu1245"
    description: str = "Default process for ChatGPT for the Urdu language."
    authorship_info: str = "UrduChatGPTProcess using OpenAI GPT models."


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
