"""High-level NLP entry point for CLTK pipelines.

The :class:`NLP` class resolves a language (by Glottolog/ISO/name), chooses an
appropriate pipeline (discriminative or generative backends), and runs each
process in order to produce a :class:`cltk.core.data_types.Doc`.
"""

import os
import shutil
from typing import Literal, Optional, Type, cast

from colorama import Fore, Style

import cltk
from cltk.core.cltk_logger import logger
from cltk.core.data_types import Dialect, Doc, Language, Pipeline, Process
from cltk.core.exceptions import UnimplementedAlgorithmError
from cltk.languages.glottolog import resolve_languoid
from cltk.languages.pipelines import (  # MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE_LOCAL,
    MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE,
)

# from cltk.languages.utils import get_lang


class NLP:
    """Convenience facade for running CLTK pipelines.

    Args:
      language_code: Language key (Glottolog code, ISO code, or exact name).
      backend: Backend family: ``"disc"`` (discriminative), ``"gen-cloud"``
        (cloud LLM), ``"gen-local"`` (local LLM), or ``"auto"`` (detect from
        env; default).
      custom_pipeline: Optional pipeline to use instead of the default mapping.
      suppress_banner: If true, suppresses informational console output.

    Notes:
      - ``backend="auto"`` resolves to:
        1) ``gen-cloud`` if an API key is found (``OPENAI_API_KEY`` or
           ``CLTK_GENAI_API_KEY``),
        2) else ``gen-local`` if an Ollama server is detected,
        3) else ``disc``.

    """

    def __init__(
        self,
        language_code: str,
        backend: Literal["disc", "gen-cloud", "gen-local", "auto"] = "auto",
        custom_pipeline: Optional[Pipeline] = None,
        suppress_banner: bool = False,
    ) -> None:
        logger.info(f"Initializing NLP for language: {language_code}")
        # self.language: Language = get_language(key=language_code)
        self.language: Language
        self.dialect: Optional[Dialect]
        self.language, self.dialect = resolve_languoid(key=language_code)
        self.language_code: str
        if self.dialect:
            self.language_code = self.dialect.glottolog_id
        else:
            self.language_code = self.language.glottolog_id
        # Resolve backend (param > env > auto detection)
        env_backend = os.getenv("CLTK_BACKEND")
        self.backend: str = self._normalize_backend(env_backend or backend)
        # API key used for gen-cloud auto detection
        self.api_key: Optional[str] = os.getenv("OPENAI_API_KEY") or os.getenv(
            "CLTK_GENAI_API_KEY"
        )
        self.pipeline: Pipeline = (
            custom_pipeline if custom_pipeline else self._get_pipeline()
        )
        logger.debug(f"Pipeline selected: {self.pipeline}")
        if not suppress_banner:
            self._print_cltk_info()
            self._print_pipelines_for_current_lang()
            self._print_special_authorship_messages_for_current_lang()
            # self._print_suppress_reminder()

    def analyze(self, text: str) -> Doc:
        """Run text through the selected NLP pipeline and return a document.

        Args:
          text: Raw text to analyze.

        Returns:
          A :class:`~cltk.core.data_types.Doc` enriched by each process in the
          pipeline (e.g., sentence boundaries, tokens, features).

        Raises:
          ValueError: If ``text`` is empty or not a string.
          RuntimeError: If any process fails during execution.

        """
        logger.info("Analyzing text with NLP pipeline.")
        if not text or not isinstance(text, str):
            logger.error("Input text must be a non-empty string.")
            raise ValueError("Input text must be a non-empty string.")
        doc: Doc = Doc(language=self.language, raw=text)
        from typing import cast

        processes: list[Type[Process]] = cast(
            list[Type[Process]],
            self.pipeline.processes if self.pipeline.processes is not None else [],
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
                ) from e
        if doc.words is None or not isinstance(doc.words, list):
            msg: str = "Pipeline did not produce any words. Check your pipeline configuration and input text."
            logger.warning(msg)
        logger.info("NLP analysis complete.")
        return doc

    def _print_cltk_info(self) -> None:
        """Print CLTK version and citation information."""
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
        """Print the resolved language/dialect and process list."""
        logger.info(f"Printing pipeline for language: {self.language.name}")
        processes: list[Type[Process]] = cast(
            list[Type[Process]],
            self.pipeline.processes if self.pipeline.processes is not None else [],
        )
        processes_name: list[str] = [process.__name__ for process in processes]
        lang_and_dialect_selected: str = ""
        if self.dialect:
            lang_and_dialect_selected = f'Selected language "{self.language.name}" ("{self.language.glottolog_id}") with dialect "{self.dialect.name}" ("{self.dialect.glottolog_id}").'
        else:
            lang_and_dialect_selected = f'Selected language "{self.language.name}" ("{self.language.glottolog_id}") without dialect.'
        print(
            Fore.CYAN
            + lang_and_dialect_selected
            + "\n"
            + f'Pipeline for `NLP("{self.language_code}", backend="{self._resolved_backend()}")`:'
            + Fore.GREEN
            + f" {[process.__name__ for process in processes]}"
            + Style.RESET_ALL
        )
        logger.debug(f"Processes in pipeline: {processes_name}")
        for process_class in processes:
            process_instance: Process = self._get_process_object(process_class)
            authorship_info = getattr(process_instance, "authorship_info", None)
            if authorship_info:
                print(
                    # "\n" +
                    Fore.CYAN + f"⸖ {authorship_info}" + Style.RESET_ALL
                )

    def _print_special_authorship_messages_for_current_lang(self) -> None:
        """Print any special authorship messages exposed by processes."""
        logger.info("Printing special authorship messages for current language.")
        processes: list[Type[Process]] = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        for process_class in processes:
            process_instance: Process = self._get_process_object(process_class)
            special_message = getattr(
                process_instance, "special_authorship_message", None
            )
            if special_message:
                print(special_message)

    def _print_suppress_reminder(self) -> None:
        """Print reminder for suppressing banner output."""
        logger.info("Printing suppress banner reminder.")
        print(
            # "\n" +
            Fore.CYAN
            + "⸎ To suppress these messages, instantiate `NLP()` with `suppress_banner=True`"
            # + "\n"
            + Style.RESET_ALL
        )

    def _get_process_object(self, process_object: Type[Process]) -> Process:
        """Instantiate a process passing the resolved ``glottolog_id``.

        Args:
          process_object: Process class to instantiate.

        Returns:
          A ``Process`` instance ready to ``run()``.

        Raises:
          RuntimeError: If instantiation fails.

        """
        logger.debug(f"Getting process object for: {process_object.__name__}")
        try:
            return process_object(glottolog_id=self.language_code)
        # except TypeError:
        #     # TODO: Revisit this and standardize passing Language object to all Processes
        #     return process_object(language=self.language.iso)
        except Exception as e:
            msg: str = f"Failed to instantiate process {process_object.__name__}: {e}"
            logger.error(msg)
            raise RuntimeError(msg) from e

    def _normalize_backend(self, value: str) -> str:
        """Map friendly aliases to canonical backends.

        Accepts "local", "cloud", "chatgpt", "openai", "stanza", etc., and
        returns one of: ``disc``, ``gen-cloud``, ``gen-local``, or ``auto``.
        """
        aliases = {
            "local": "disc",
            "discriminative": "disc",
            "spacy": "disc",
            "stanza": "disc",
            "cloud": "gen-cloud",
            "chatgpt": "gen-cloud",
            "openai": "gen-cloud",
            "llama": "gen-local",
            "ollama": "gen-local",
            "local-gen": "gen-local",
        }
        if value in ("disc", "gen-cloud", "gen-local", "auto"):
            return value
        return aliases.get(value, "auto")

    def _has_local_gen(self) -> bool:
        """Return true if an Ollama server/binary appears available locally."""
        return bool(os.getenv("OLLAMA_HOST") or shutil.which("ollama"))

    def _resolved_backend(self) -> str:
        """Resolve backend when ``auto``; otherwise return normalized value."""
        if self.backend != "auto":
            return self.backend
        if self.api_key:
            return "gen-cloud"
        if self._has_local_gen():
            return "gen-local"
        return "disc"

    def _get_pipeline(self) -> Pipeline:
        """Select the default pipeline for the resolved language.

        If a custom pipeline was not provided, this looks up the mapping for
        the chosen backend and glottolog code and returns an instance.

        Examples:
          >>> from cltk.core.data_types import Pipeline
          >>> cltk_nlp = NLP(language_code="lat", suppress_banner=True)
          >>> lat_pipeline = cltk_nlp._get_pipeline()
          >>> isinstance(cltk_nlp.pipeline, Pipeline)
          True
          >>> isinstance(lat_pipeline, Pipeline)
          True
          >>> cltk_nlp = NLP(language_code="axm", suppress_banner=True)
          Traceback (most recent call last):
          ...
          cltk.core.exceptions.UnimplementedAlgorithmError: Valid ISO/Glottolog code but no pipeline for 'axm' with backend 'disc'.

        """
        backend = self._resolved_backend()
        if backend == "disc":
            raise NotImplementedError("Discriminative backend not yet reimplemented.")
            # mapping = MAP_LANGUAGE_CODE_TO_DISCRIMINATIVE_PIPELINE
        elif backend == "gen-cloud":
            mapping = MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE
        else:  # "gen-local"
            raise NotImplementedError("Local generative backend not yet implemented.")
            # mapping = MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE_LOCAL
        try:
            pipeline_cls = mapping[self.language_code]
        except KeyError as e:
            raise UnimplementedAlgorithmError(
                f"Valid ISO/Glottolog code but no pipeline for '{self.language_code}' with backend '{backend}'."
            ) from e
        logger.info(f"Using backend '{backend}' with pipeline {pipeline_cls.__name__}")
        return pipeline_cls()
