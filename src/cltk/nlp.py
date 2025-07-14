"""Primary module for CLTK pipeline."""

import inspect
import os
from threading import Lock
from typing import Any, Dict, List, Optional, Type

from dotenv import load_dotenv

import cltk
from cltk.core.cltk_logger import logger
from cltk.core.data_types import Doc, Language, Pipeline, Process
from cltk.core.exceptions import UnimplementedAlgorithmError
from cltk.languages.pipelines import (
    AkkadianPipeline,
    ArabicPipeline,
    AramaicPipeline,
    ChinesePipeline,
    CopticPipeline,
    GothicPipeline,
    GreekPipeline,
    HindiPipeline,
    LatinPipeline,
    MiddleEnglishPipeline,
    MiddleFrenchPipeline,
    MiddleHighGermanPipeline,
    OCSPipeline,
    OldEnglishPipeline,
    OldFrenchPipeline,
    OldNorsePipeline,
    PaliPipeline,
    PanjabiPipeline,
    SanskritPipeline,
)
from cltk.languages.utils import get_lang

iso_to_pipeline = {
    "akk": AkkadianPipeline,
    "ang": OldEnglishPipeline,
    "arb": ArabicPipeline,
    "arc": AramaicPipeline,
    "chu": OCSPipeline,
    "cop": CopticPipeline,
    "enm": MiddleEnglishPipeline,
    "frm": MiddleFrenchPipeline,
    "fro": OldFrenchPipeline,
    "gmh": MiddleHighGermanPipeline,
    "got": GothicPipeline,
    "grc": GreekPipeline,
    "hin": HindiPipeline,
    "lat": LatinPipeline,
    "lzh": ChinesePipeline,
    "non": OldNorsePipeline,
    "pan": PanjabiPipeline,
    "pli": PaliPipeline,
    "san": SanskritPipeline,
}


class NLP:
    """NLP class for default processing."""

    process_objects: Dict[Type[Process], Process] = dict()
    process_lock: Lock = Lock()
    language: Language
    pipeline: Pipeline
    api_key: Optional[str]

    def __init__(
        self,
        language: str,
        custom_pipeline: Optional[Pipeline] = None,
        suppress_banner: bool = False,
    ) -> None:
        logger.info(f"Initializing NLP for language: {language}")
        self.language: Language = get_lang(language)
        self.pipeline = custom_pipeline if custom_pipeline else self._get_pipeline()
        logger.debug(f"Pipeline selected: {self.pipeline}")
        # Load OpenAI API key from environment or .env
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key is None or self.api_key == "":
            logger.warning(
                "OPENAI_API_KEY is missing. ChatGPT-based processes will fail unless an API key is provided."
            )
        if not suppress_banner:
            self._print_cltk_info()
            self._print_pipelines_for_current_lang()
            self._print_special_authorship_messages_for_current_lang()
            self._print_suppress_reminder()

    def _print_cltk_info(self) -> None:
        logger.info("Printing CLTK citation info.")
        ltr_mark: str = "\u200E"
        alep: str = "\U00010900"
        print(
            f"{ltr_mark + alep} CLTK version '{cltk.__version__}'. When using the CLTK in research, please cite: https://aclanthology.org/2021.acl-demo.3/"
        )
        print("")

    def _print_pipelines_for_current_lang(self) -> None:
        logger.info(f"Printing pipeline for language: {self.language.name}")
        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        processes_name: list[str] = [process.__name__ for process in processes]
        processes_name_str: str = "`, `".join(processes_name)
        print(
            f"Pipeline for language '{self.language.name}' (ISO: '{self.language.iso_639_3_code}'): `{processes_name_str}`."
        )
        print("")
        logger.debug(f"Processes in pipeline: {processes_name}")
        print(f"Processes in pipeline: {[process.__name__ for process in processes]}")
        for process_class in processes:
            process_instance = self._get_process_object(process_class)
            authorship_info = getattr(process_instance, "authorship_info", None)
            if authorship_info:
                print(f"⸖ {authorship_info}")

    def _print_special_authorship_messages_for_current_lang(self) -> None:
        logger.info("Printing special authorship messages for current language.")
        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        for process_class in processes:
            process_instance = self._get_process_object(process_class)
            special_message = getattr(
                process_instance, "special_authorship_message", None
            )
            if special_message:
                print(special_message)

    def _print_suppress_reminder(self) -> None:
        logger.info("Printing suppress banner reminder.")
        print("")
        print(
            "⸎ To suppress these messages, instantiate ``NLP()`` with ``suppress_banner=True``."
        )

    def _get_process_object(self, process_object: Type[Process]) -> Process:
        logger.debug(f"Getting process object for: {process_object.__name__}")
        with NLP.process_lock:
            a_process: Optional[Process] = NLP.process_objects.get(process_object, None)
            if a_process:
                logger.debug(
                    f"Process object found in cache: {process_object.__name__}"
                )
                return a_process
            else:
                try:
                    new_process: Process = process_object(
                        self.language.iso_639_3_code, api_key=self.api_key  # type: ignore introspection
                    )
                except TypeError:
                    new_process: Process = process_object(self.language.iso_639_3_code)
                except Exception as e:
                    logger.error(
                        f"Failed to instantiate process {process_object.__name__}: {e}"
                    )
                    raise RuntimeError(
                        f"Failed to instantiate process {process_object.__name__}: {e}"
                    )
                NLP.process_objects[process_object] = new_process
                logger.debug(
                    f"Process object instantiated and cached: {process_object.__name__}"
                )
                return new_process

    def analyze(self, text: str) -> Doc:
        logger.info("Analyzing text with NLP pipeline.")
        if not text or not isinstance(text, str):
            logger.error("Input text must be a non-empty string.")
            raise ValueError("Input text must be a non-empty string.")
        doc = Doc(language=self.language.iso_639_3_code, raw=text)
        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        for process in processes:
            a_process: Process = self._get_process_object(process_object=process)
            try:
                logger.debug(f"Running process: {a_process.__class__.__name__}")
                doc = a_process.run(doc)
            except Exception as e:
                logger.error(f"Process '{a_process.__class__.__name__}' failed: {e}")
                raise RuntimeError(
                    f"Process '{a_process.__class__.__name__}' failed: {e}"
                )
        if doc.words is None or not isinstance(doc.words, list):
            logger.error(
                "Pipeline did not produce any words. Check your pipeline configuration and input text."
            )
            raise RuntimeError(
                "Pipeline did not produce any words. Check your pipeline configuration and input text."
            )
        logger.info("NLP analysis complete.")
        return doc

    def _get_pipeline(self) -> Pipeline:
        """Select appropriate pipeline for given language. If custom
        processing is requested, ensure that user-selected choices
        are valid, both in themselves and in unison.

        >>> from cltk.core.data_types import Pipeline
        >>> cltk_nlp = NLP(language="lat", suppress_banner=True)
        >>> lat_pipeline = cltk_nlp._get_pipeline()
        >>> isinstance(cltk_nlp.pipeline, Pipeline)
        True
        >>> isinstance(lat_pipeline, Pipeline)
        True
        >>> cltk_nlp = NLP(language="axm", suppress_banner=True)
        Traceback (most recent call last):
          ...
        cltk.core.exceptions.UnimplementedAlgorithmError: Valid ISO language code, however this algorithm is not available for ``axm``.
        """
        try:
            return iso_to_pipeline[self.language.iso_639_3_code]()
        except KeyError:
            raise UnimplementedAlgorithmError(
                f"Valid ISO language code, however this algorithm is not available for ``{self.language.iso_639_3_code}``."
            )


if __name__ == "__main__":
    from cltk.languages.example_texts import get_example_text
    from cltk.languages.pipelines import GreekChatGPTPipeline

    logger.info("Running NLP main block for GreekChatGPTPipeline example.")
    example_text = get_example_text("grc")
    pipeline = GreekChatGPTPipeline()
    nlp = NLP(language="grc", custom_pipeline=pipeline, suppress_banner=False)
    doc = nlp.analyze(example_text)
    logger.info(f"Doc output: {doc}")
    # logger.info(f"Words: {[w.string for w in doc.words] if doc.words is not None else []}")
    # logger.info(f"ChatGPT metadata: {doc.chatgpt}")
