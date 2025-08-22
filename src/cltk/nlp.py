"""Primary module for CLTK pipeline."""

import inspect
import os
from threading import Lock
from typing import Any, Dict, List, Optional, Type

from colorama import Fore, Style

import cltk
from cltk.core.cltk_logger import logger
from cltk.core.data_types_v2 import Doc, Language, Pipeline, Process
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

# TODO: Revisit this and add GPT/genai routing
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

    process_objects: dict[Type[Process], Process] = dict()
    process_lock: Lock = Lock()
    language: Language
    # language_code: str
    pipeline: Pipeline
    api_key: Optional[str]

    def __init__(
        self,
        language_code: str,  # Called `language` for end user; elsewhere what codebase calls `language_code` (ISO or Glottolog)
        custom_pipeline: Optional[Pipeline] = None,
        suppress_banner: bool = False,
    ) -> None:
        logger.info(f"Initializing NLP for language: {language_code}")
        self.language: Language = get_lang(language_code=language_code)
        self.language_code: str = language_code
        self.pipeline: Pipeline = (
            custom_pipeline if custom_pipeline else self._get_pipeline()
        )
        logger.debug(f"Pipeline selected: {self.pipeline}")
        if not suppress_banner:
            self._print_cltk_info()
            self._print_pipelines_for_current_lang()
            self._print_special_authorship_messages_for_current_lang()
            self._print_suppress_reminder()

    def analyze(self, text: str) -> Doc:
        logger.info("Analyzing text with NLP pipeline.")
        if not text or not isinstance(text, str):
            logger.error("Input text must be a non-empty string.")
            raise ValueError("Input text must be a non-empty string.")
        doc: Doc = Doc(language=self.language, raw=text)
        processes: list[Type[Process]] = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        for process in processes:
            process_obj: Process = self._get_process_object(process_object=process)
            try:
                logger.debug(f"Running process: {process_obj.__class__.__name__}")
                doc = process_obj.run(doc)
            except Exception as e:
                logger.error(f"Process '{process_obj.__class__.__name__}' failed: {e}")
                raise RuntimeError(
                    f"Process '{process_obj.__class__.__name__}' failed: {e}"
                )
        if doc.words is None or not isinstance(doc.words, list):
            msg: str = (
                "Pipeline did not produce any words. Check your pipeline configuration and input text."
            )
            logger.warning(msg)
            # raise RuntimeError(msg)
        logger.info("NLP analysis complete.")
        return doc

    def _print_cltk_info(self) -> None:
        logger.info("Printing CLTK citation info.")
        ltr_mark: str = "\u200e"
        alep: str = "\U00010900"
        print(
            Fore.CYAN
            + Style.BRIGHT
            + f"{ltr_mark + alep} CLTK version '{cltk.__version__}'. When using the CLTK in research, please cite: "
            # + Fore.BLUE
            # + Style.BRIGHT
            + "https://aclanthology.org/2021.acl-demo.3/"
            + Style.RESET_ALL
            # + "\n"
        )

    def _print_pipelines_for_current_lang(self) -> None:
        logger.info(f"Printing pipeline for language: {self.language.name}")
        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        processes_name: list[str] = [process.__name__ for process in processes]
        lang_or_dialect_name: str
        if self.language.selected_dialect_name:
            lang_or_dialect_name = self.language.selected_dialect_name
        else:
            lang_or_dialect_name = self.language.name
        print(
            Fore.CYAN
            + f"Pipeline for {lang_or_dialect_name} ('{self.language_code}'):"
            + Fore.GREEN
            + f" {[process.__name__ for process in processes]}"
            + Style.RESET_ALL
        )
        logger.debug(f"Processes in pipeline: {processes_name}")
        for process_class in processes:
            process_instance = self._get_process_object(process_class)
            authorship_info = getattr(process_instance, "authorship_info", None)
            if authorship_info:
                print(
                    # "\n" +
                    Fore.CYAN
                    + f"⸖ {authorship_info}"
                    + Style.RESET_ALL
                )

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
        print(
            # "\n" +
            Fore.CYAN
            + "⸎ To suppress these messages, instantiate `NLP()` with `suppress_banner=True`"
            # + "\n"
            + Style.RESET_ALL
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
                        language_code=self.language_code
                    )
                # except TypeError:
                #     # TODO: Revisit this and standardize passing Language object to all Processes
                #     new_process: Process = process_object(language=self.language.iso)
                except Exception as e:
                    msg: str = (
                        f"Failed to instantiate process {process_object.__name__}: {e}"
                    )
                    logger.error(msg)
                    raise RuntimeError(msg)
                NLP.process_objects[process_object] = new_process
                logger.debug(
                    f"Process object instantiated and cached: {process_object.__name__}"
                )
                return new_process

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
            return iso_to_pipeline[self.language_code]()
        except KeyError:
            raise UnimplementedAlgorithmError(
                f"Valid ISO or Glottolog language code, however this algorithm is not available for ``{self.language_code}``."
            )
