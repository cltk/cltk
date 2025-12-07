"""High-level NLP entry point for CLTK pipelines."""

import os
import shutil
from typing import Optional, Union, cast

from colorama import Fore, Style

import cltk
from cltk.core.cltk_logger import bind_context, logger
from cltk.core.data_types import (
    AVAILABLE_OPENAI_MODELS,
    BACKEND_TYPES,
    CLTKConfig,
    Dialect,
    Doc,
    Language,
    ModelConfig,
    Pipeline,
    Process,
    StanzaBackendConfig,
)
from cltk.core.exceptions import UnimplementedAlgorithmError
from cltk.core.logging_utils import bind_from_doc
from cltk.languages.glottolog import resolve_languoid
from cltk.languages.pipelines import (  # MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE_LOCAL,
    MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE,
    MAP_LANGUAGE_CODE_TO_SPACY_PIPELINE,
    MAP_LANGUAGE_CODE_TO_STANZA_PIPELINE,
    ensure_stanza_available,
)
from cltk.utils.utils import load_env_file

# from cltk.languages.utils import get_lang


class NLP:
    """Convenience facade for running CLTK pipelines.

    Args:
      language_code: Language key (Glottolog code, ISO code, or exact name).
        Required unless ``cltk_config`` is provided.
      backend: One of ``"stanza"`` (default), ``"openai"``, ``"ollama"``,
        ``"ollama-cloud"``, or ``mistral``. The ``"spacy"`` backend is not
        yet implemented and will raise ``NotImplementedError``.
      model: Optional model name when using generative backends
        (``"openai"``, ``"ollama"``, ``"ollama-cloud"``, ``mistral``). Ignored for
        ``"stanza"``.
      custom_pipeline: Optional pipeline to use instead of the default mapping.
      suppress_banner: If true, suppresses informational console output.
      cltk_config: Optional :class:`~cltk.core.data_types.CLTKConfig` bundle.
        When provided, its values override the other constructor arguments.

    Notes:
      - When ``backend == "openai"`` and no ``model`` is provided, defaults to
        ``"gpt-5-mini"``. Requires ``OPENAI_API_KEY`` in the environment.
      - When ``backend`` is ``"ollama"`` or ``"ollama-cloud"`` and no ``model``
        is provided, defaults to ``"llama3.1:8b"``. ``"ollama-cloud"`` requires
        ``OLLAMA_CLOUD_API_KEY`` in the environment.
      - The ``"stanza"`` backend does not accept a ``model`` parameter; language
        models are bound to the pipeline for each language.

    """

    def __init__(
        self,
        language_code: Optional[str] = None,
        backend: BACKEND_TYPES = "stanza",
        model: Optional[Union[str, AVAILABLE_OPENAI_MODELS]] = None,
        custom_pipeline: Optional[Pipeline] = None,
        suppress_banner: bool = False,
        cltk_config: Optional["CLTKConfig"] = None,
    ) -> None:
        self.cltk_config: Optional[CLTKConfig] = cltk_config
        backend_config: Optional[ModelConfig] = (
            cltk_config.active_backend_config if cltk_config else None
        )
        stanza_model_override: Optional[str] = None
        if cltk_config:
            language_code = cltk_config.language_code
            backend = cltk_config.backend
            suppress_banner = cltk_config.suppress_banner
            if cltk_config.custom_pipeline is not None:
                custom_pipeline = cltk_config.custom_pipeline
            config_model_value = cltk_config.model
            if config_model_value is not None:
                model = config_model_value
            if model is None and backend_config is not None:
                model = getattr(backend_config, "model", None)
            if isinstance(backend_config, StanzaBackendConfig):
                stanza_model_override = backend_config.model
                # Preserve stanza restriction against explicit model arg
                model = None

        if language_code is None:
            raise ValueError(
                "language_code is required when no CLTKConfig is provided."
            )

        bind_context(glottolog_id=language_code).info(
            f"Initializing NLP for language: {language_code}"
        )
        # self.language: Language = get_language(key=language_code)
        self.language: Language
        self.dialect: Optional[Dialect]
        self.language, self.dialect = resolve_languoid(key=language_code)
        self.language_code: str
        if self.dialect:
            self.language_code = self.dialect.glottolog_id
        else:
            self.language_code = self.language.glottolog_id
        self.backend: BACKEND_TYPES = backend
        self.model: Optional[str] = model
        self._backend_config: Optional[ModelConfig] = backend_config
        self._stanza_model_override: Optional[str] = stanza_model_override
        self._ollama_cloud_api_key: Optional[str] = None
        self.api_key: Optional[str] = None
        if self.backend == "openai":
            # Prefer API key from config when provided
            self.api_key = getattr(backend_config, "api_key", None)
            if not self.api_key:
                load_env_file()
                self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                openai_msg: str = "API key for OpenAI not found."
                logger.error(openai_msg)
                raise ValueError(openai_msg)
            # Default model if none provided
            self.model = self.model or getattr(backend_config, "model", None)
            self.model = self.model or "gpt-5-mini"
        elif self.backend in ("ollama", "ollama-cloud"):
            if self.backend == "ollama-cloud":
                # Prefer API key from config when provided
                self._ollama_cloud_api_key = getattr(backend_config, "api_key", None)
                if not self._ollama_cloud_api_key:
                    load_env_file()
                    self._ollama_cloud_api_key = os.getenv("OLLAMA_CLOUD_API_KEY")
                if not self._ollama_cloud_api_key:
                    msg = "API key for Ollama Cloud not found."
                    logger.error(msg)
                    raise ValueError(msg)
            # Default model if none provided
            self.model = self.model or getattr(backend_config, "model", None)
            self.model = self.model or "llama3.1:8b"
        elif self.backend == "stanza":
            try:
                ensure_stanza_available()
            except ImportError as e:
                logger.error(str(e))
                raise
            # Stanza models are bound to language pipelines; reject explicit model
            if self.model is not None:
                raise ValueError(
                    "The 'stanza' backend does not accept a model parameter; models are hardcoded per language."
                )
        elif self.backend == "mistral":
            # Prefer API key from config when provided
            self.api_key = getattr(backend_config, "api_key", None)
            if not self.api_key:
                load_env_file()
                self.api_key = os.getenv("MISTRAL_API_KEY")
            if not self.api_key:
                mistral_msg: str = "API key for Mistral not found."
                logger.error(mistral_msg)
                raise ValueError(mistral_msg)
            # Default model if none provided
            self.model = self.model or getattr(backend_config, "model", None)
            self.model = self.model or "mistral-medium-latest"
        self.pipeline: Pipeline = (
            custom_pipeline if custom_pipeline else self._get_pipeline()
        )
        bind_context(
            glottolog_id=self.language_code,
            model=str(self.model) if getattr(self, "model", None) else None,
        ).debug(f"Pipeline selected: {self.pipeline}")
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
        doc.backend = self.backend
        doc.model = getattr(self, "model", None)
        # Expose backend config to downstream processes (LLM options, stanza package)
        if self._backend_config:
            doc.metadata["backend_config"] = self._backend_config
        if self._stanza_model_override:
            doc.metadata["stanza_package"] = self._stanza_model_override
        log = bind_from_doc(doc)

        processes: list[type[Process]] = cast(
            list[type[Process]],
            self.pipeline.processes if self.pipeline.processes is not None else [],
        )
        if not processes:
            msg: str = "No processes found in pipeline."
            log.error(msg)
            raise RuntimeError(msg)
        for process in processes:
            process_obj: Process = self._get_process_object(process_object=process)
            try:
                log.debug(f"Running process: {process_obj.__class__.__name__}")
                doc = process_obj.run(doc)
            except Exception as e:
                log.error(f"Process '{process_obj.__class__.__name__}' failed: {e}")
                raise RuntimeError(
                    f"Process '{process_obj.__class__.__name__}' failed: {e}"
                ) from e
        if doc.words is None or not isinstance(doc.words, list):
            msg = "Pipeline did not produce any words. Check your pipeline configuration and input text."
            log.warning(msg)
        log.info("NLP analysis complete.")
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
        processes: list[type[Process]] = cast(
            list[type[Process]],
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
            + f'Pipeline for `NLP("{self.language_code}", backend="{self.backend}")`:'
            + Fore.GREEN
            + f" {[process.__name__ for process in processes]}"
            + Style.RESET_ALL
        )
        logger.debug(f"Processes in pipeline: {processes_name}")
        for process_class in processes:
            process_instance: Process = self._get_process_object(process_class)
            print(
                Fore.CYAN
                + f"⸖ Process name: {process_instance.__class__.__name__}"
                + Style.RESET_ALL
            )
            authorship_info = getattr(process_instance, "authorship_info", None)
            description = getattr(process_instance, "description", None)
            if authorship_info:
                print(
                    Fore.CYAN
                    + f"    Process author: {authorship_info}"
                    + Style.RESET_ALL
                )
            if description:
                print(Fore.CYAN + f"    Description: {description}" + Style.RESET_ALL)

    def _print_special_authorship_messages_for_current_lang(self) -> None:
        """Print any special authorship messages exposed by processes."""
        logger.info("Printing special authorship messages for current language.")
        processes: list[type[Process]] = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        for process_class in processes:
            process_instance: Process = self._get_process_object(process_class)
            special_message: Optional[str] = getattr(
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

    def _get_process_object(self, process_object: type[Process]) -> Process:
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

    def _has_local_gen(self) -> bool:
        """Return true if an Ollama server/binary appears available locally."""
        return bool(os.getenv("OLLAMA_HOST") or shutil.which("ollama"))

    def _get_pipeline(self) -> Pipeline:
        """Select the default pipeline for the resolved language.

        If a custom pipeline was not provided, this looks up the mapping for
        the chosen backend and glottolog code and returns an instance. The
        ``"stanza"`` backend uses ``MAP_LANGUAGE_CODE_TO_STANZA_PIPELINE``.
        The generative backends (``"openai"``, ``"ollama"``, ``"ollama-cloud"``)
        use ``MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE``; the underlying client
        is selected later based on ``doc.backend``. The ``"spacy"`` backend is
        currently not implemented and raises ``NotImplementedError``.

        Examples:
            ```python
            from cltk.core.data_types import Pipeline

            cltk_nlp = NLP(language_code="lat", suppress_banner=True)
            lat_pipeline = cltk_nlp._get_pipeline()
            assert isinstance(cltk_nlp.pipeline, Pipeline)
            assert isinstance(lat_pipeline, Pipeline)

            cltk_nlp = NLP(language_code="axm", suppress_banner=True)
            # Raises cltk.core.exceptions.UnimplementedAlgorithmError for missing pipeline
            cltk_nlp._get_pipeline()
            ```

        """
        if self.backend == "stanza":
            mapping = MAP_LANGUAGE_CODE_TO_STANZA_PIPELINE
        elif self.backend == "spacy":
            mapping = MAP_LANGUAGE_CODE_TO_SPACY_PIPELINE
            raise NotImplementedError(
                f"Discriminative backend '{self.backend}' not yet reimplemented."
            )
        elif self.backend == "openai":
            mapping = MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE
        elif self.backend in ("ollama", "ollama-cloud"):
            # Reuse the same generative pipelines; lower layers pick the client by backend
            mapping = MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE
        elif self.backend == "mistral":
            mapping = MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE
        else:
            raise NotImplementedError(f"Backend '{self.backend}' not available.")
        try:
            pipeline_cls = mapping[self.language_code]
        except KeyError as e:
            raise UnimplementedAlgorithmError(
                f"Valid Glottolog code but no pipeline for '{self.language_code}' with backend '{self.backend}'."
            ) from e
        bind_context(
            glottolog_id=self.language_code,
            model=str(self.model) if getattr(self, "model", None) else None,
        ).info(f"Using backend '{self.backend}' with pipeline {pipeline_cls.__name__}")
        return pipeline_cls()
