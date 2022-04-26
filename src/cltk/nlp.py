"""Primary module for CLTK pipeline."""

from threading import Lock
from typing import Type

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

    process_objects = dict()
    process_lock = Lock()

    def __init__(
        self,
        language: str,
        custom_pipeline: Pipeline = None,
        suppress_banner: bool = False,
    ) -> None:
        """Constructor for CLTK class.

        Args:
            language: ISO code
            custom_pipeline: Optional ``Pipeline`` for processing text.


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
        self.language = get_lang(language)  # type: Language
        self.pipeline = custom_pipeline if custom_pipeline else self._get_pipeline()
        if not suppress_banner:
            self._print_pipelines_for_current_lang()

    def _print_pipelines_for_current_lang(self):
        """Print to screen the ``Process``es invoked upon invocation
        of ``NLP()``.
        """
        processes_name = [
            process.__name__ for process in self.pipeline.processes
        ]  # type: List[str]
        processes_name_str = "`, `".join(processes_name)  # type: str
        ltr_mark = "\u200E"
        alep = "𐤀"
        print(f"{ltr_mark + alep} CLTK version '{cltk.__version__.version}'.")
        print(
            f"Pipeline for language '{self.language.name}' (ISO: '{self.language.iso_639_3_code}'): `{processes_name_str}`."
        )

    def _get_process_object(self, process_object: Type[Process]) -> Process:
        """
        Returns an instance of a process from a memoized hash.
        An un-instantiated process is created and stashed in the cache.
        """
        with NLP.process_lock:
            a_process = NLP.process_objects.get(process_object, None)
            if a_process:
                return a_process
            else:
                a_process = process_object(self.language.iso_639_3_code)
                NLP.process_objects[process_object] = a_process
                return a_process

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
        for process in self.pipeline.processes:
            a_process = self._get_process_object(process)
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

    def __call__(self, text: str) -> Doc:
        return self.analyze(text)
