"""Primary module for CLTK pipeline."""

import inspect
import os
from threading import Lock
from typing import Any, Dict, List, Optional, Type

from dotenv import load_dotenv

import cltk
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
        """Constructor for CLTK class.

        Args:
            language: ISO code
            custom_pipeline: Optional ``Pipeline`` for processing text.
            api_key: Optional OpenAI API key for ChatGPT-based processes.


        >>> from cltk import NLP
        >>> cltk_nlp = NLP(language="lat", suppress_banner=True)
        >>> isinstance(cltk_nlp, NLP)
        True
        >>> from cltk.core.data_types import Pipeline
        >>> from cltk.tokenizers import LatinTokenizationProcess
        >>> from cltk.languages.utils import get_lang
        >>> a_pipeline = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess], language=get_lang("lat"))
        >>> nlp = NLP(language="lat", custom_pipeline=a_pipeline, suppress_banner=True)
        >>> nlp.pipeline is a_pipeline
        True
        """
        self.language: Language = get_lang(language)
        self.pipeline = custom_pipeline if custom_pipeline else self._get_pipeline()
        # Load OpenAI API key from environment or .env
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not suppress_banner:
            self._print_cltk_info()
            self._print_pipelines_for_current_lang()
            self._print_special_authorship_messages_for_current_lang()
            self._print_suppress_reminder()

    def _print_cltk_info(self) -> None:
        """Print to screen about citing CLTK."""
        ltr_mark: str = "\u200E"
        alep: str = "𐤀"
        print(
            f"{ltr_mark + alep} CLTK version '{cltk.__version__}'. When using the CLTK in research, please cite: https://aclanthology.org/2021.acl-demo.3/"
        )
        print("")

    def _print_pipelines_for_current_lang(self) -> None:
        """Print to screen the ``Process``es invoked upon invocation
        of ``NLP()``.
        """
        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        processes_name: list[str] = [process.__name__ for process in processes]
        processes_name_str: str = "`, `".join(processes_name)
        print(
            f"Pipeline for language '{self.language.name}' (ISO: '{self.language.iso_639_3_code}'): `{processes_name_str}`."
        )
        print("")

        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        print(f"Processes in pipeline: {[process.__name__ for process in processes]}")
        for process_class in processes:
            process_instance = self._get_process_object(process_class)
            authorship_info = getattr(process_instance, "authorship_info", None)
            if authorship_info:
                print(f"⸖ {authorship_info}")

    def _print_special_authorship_messages_for_current_lang(self) -> None:
        """Print to screen the authors of particular algorithms."""
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
        """Tell users how to suppress printed messages."""
        # https://en.wikipedia.org/wiki/Coronis_(textual_symbol)
        # U+2E0E ⸎ EDITORIAL CORONIS
        print("")
        print(
            "⸎ To suppress these messages, instantiate ``NLP()`` with ``suppress_banner=True``."
        )

    def _get_process_object(self, process_object: Type[Process]) -> Process:
        """
        Returns an instance of a process from a memoized hash.
        An un-instantiated process is created and stashed in the cache.
        """
        with NLP.process_lock:
            a_process: Optional[Process] = NLP.process_objects.get(process_object, None)
            if a_process:
                return a_process
            else:
                # Try instantiating with api_key, fallback if not accepted
                try:
                    new_process: Process = process_object(
                        self.language.iso_639_3_code, api_key=self.api_key  # type: ignore introspection
                    )
                except TypeError:
                    new_process: Process = process_object(self.language.iso_639_3_code)
                NLP.process_objects[process_object] = new_process
                return new_process

    def analyze(self, text: str) -> Doc:
        """The primary method for the NLP object, to which raw text strings are passed.

        Args:
            text: Input text string.

        Returns:
            CLTK ``Doc`` containing all processed information.

        >>> from cltk.languages.example_texts import get_example_text
        >>> from cltk.core.data_types import Doc
        >>> cltk_nlp = NLP(language="lat", suppress_banner=True)
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lat"))
        >>> isinstance(cltk_doc, Doc)
        True
        >>> cltk_doc.words[0].string
        'Gallia'
        """
        doc = Doc(language=self.language.iso_639_3_code, raw=text)
        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        for process in processes:
            a_process: Process = self._get_process_object(process_object=process)
            doc = a_process.run(doc)
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

    def run_pipeline(self, text: str) -> Doc:
        """Run the entire pipeline on the given text."""
        doc = Doc(language=self.language.iso_639_3_code, raw=text)
        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        for process in processes:
            a_process: Process = self._get_process_object(process_object=process)
            doc = a_process.run(doc)
        return doc

    def __call__(self, text: str) -> Doc:
        return self.analyze(text)


if __name__ == "__main__":
    from cltk.languages.example_texts import get_example_text
    from cltk.languages.pipelines import GreekChatGPTPipeline

    example_text = get_example_text("grc")
    pipeline = GreekChatGPTPipeline()
    nlp = NLP(language="grc", custom_pipeline=pipeline, suppress_banner=True)
    doc = nlp(example_text)
    print(doc)
    print("Words:", [w.string for w in doc.words] if doc.words is not None else [])
    print("ChatGPT metadata:", doc.chatgpt)
