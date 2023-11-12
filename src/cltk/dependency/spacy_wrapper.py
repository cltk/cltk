import logging
import subprocess
import sys
from typing import Any, Optional

import spacy
from spacy.tokens import Doc

from cltk.core.exceptions import CLTKException, UnknownLanguageError
from cltk.utils import suppress_stdout
from cltk.utils.utils import query_yes_no

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

MAP_LANGS_CLTK_SPACY = {
    "lat": "la",
}

MAP_LANG_TO_SPACY_MODEL_NAME: dict[str, str] = {
    "lat": "la_core_web_lg",
}

MAP_LANG_TO_SPACY_MODEL_URL: dict[str, str] = {
    "lat": "https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl",
}


class SpacyWrapper:
    """`SpacyWrapper` has been made to be an interface
    between spaCy and CLTK.
    """

    nlps = {}

    def __init__(
        self,
        language: str,
        nlp: Optional[spacy.Language] = None,
        interactive: bool = True,
        silent: bool = False,
        # spacy_model_name: Optional[str] = None
    ):
        """

        :param language: One of the officially supported languages by CLTK. It selects a default model for
        :param nlp: A `Language` instance from spaCy (not used by default).
        :param interactive: Are downloads interactive?
        :param silent: Is it verbose?
        """
        self.language = language
        self.nlp = nlp
        self.interactive = interactive
        self.silent = silent
        self.spacy_model: Optional[Any] = None
        # self.spacy_debug_level = spacy_debug_level

        if self.interactive and self.silent:
            raise ValueError(
                "``interactive`` and ``silent`` options are not compatible with each other."
            )

        self.wrapper_available: bool = self.is_wrapper_available()
        if not self.wrapper_available:
            raise UnknownLanguageError(
                f"Language '{self.language}' either not in scope for CLTK or the project does know about it. If you know of a publicly available spaCy model for '{self._language}', please open a pull request (with this message) at `https://github.com/cltk/cltk/issues`."
            )
        self.spacy_code: str = self._get_spacy_code()
        self.spacy_model_name: str = self._get_spacy_model_name()
        self.spacy_model_url: str = self._get_spacy_model_url()

        if not self._is_model_present():
            self._download_model()

        if not self.spacy_model:
            self.nlp = self._load_model()

        # def is_wrapper_available(self) -> bool:
        #     """Maps an ISO 639-3 language id (e.g., ``lat`` for Latin) to
        #     that used by ``spacy`` (``la``); confirms that this is
        #     a language the CLTK supports (i.e., is it pre-modern or not).
        #
        #     >>> spacy_wrapper = SpacyWrapper(language='lat', interactive=False, silent=True)
        #     >>> spacy_wrapper.is_wrapper_available()
        #     True
        #     """
        #     return self.language in MAP_LANGS_CLTK_SPACY

        # self.nlp = nlp
        # if self.nlp:
        #     self._language = self.nlp.lang
        #     self.nlps[self._language] = self
        # else:
        #     self._language = language
        #     self._interactive = interactive
        #     self._silent = silent
        #
        #     if self._interactive and self._silent:
        #         raise ValueError(
        #             "``interactive`` and ``silent`` options are not compatible with each other."
        #         )
        #
        #     if not self.is_wrapper_available:
        #         raise UnknownLanguageError(
        #             f"Language {self._language} is not supported by CLTK wrapper of SpaCy."
        #         )
        #
        #     self._select_model()
        #
        #
        #
        #     if not self._is_model_present:
        #         query_yes_no(
        #             question="This part of the CLTK requires a spaCy model downloaded from 'https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl'. Do you want to download this?",
        #             default="yes"
        #         )
        #         self._download_model()
        #
        #     with suppress_stdout():
        #         self.nlp = self._load_pipeline()
        #         self.nlps[self._language] = self

    # @property
    # def language(self) -> str:
    #     return self._language
    #
    # @property
    # def silent(self) -> bool:
    #     return self._silent
    #
    # @property
    # def interactive(self) -> bool:
    #     return self._interactive

    # @property
    # def is_wrapper_available(self) -> bool:
    #     return self._language in MAP_LANGS_CLTK_SPACY

    # def _select_model(self):
    #     if self._language == "lat":
    #         self.spacy_model_name: str = "la_core_web_la"
    #     else:
    #         raise CLTKException(f"No spaCy model found for language {self._language}")
    #
    # def _load_pipeline(self) -> spacy.Language:
    #     nlp = spacy.load(self.spacy_model_name)
    #     return nlp
    #
    def parse(self, text: str) -> spacy.tokens.doc.Doc:
        """
        >>> from cltk.languages.example_texts import get_example_text
        >>> spacy_wrapper = SpacyWrapper(language="lat")
        >>> latin_nlp = spacy_wrapper.parse(get_example_text("lat"))

        ???

        :param text: Text to analyze.
        :return:
        """
        if isinstance(self.nlp, spacy.Language):
            return self.nlp(text)
        raise CLTKException(
            "No spaCy model has been loaded. Is the language supported? "
            "Otherwise try to provide a spaCy model with `nlp`argument."
        )
        # Note: spacy's `nlp` object is called directly, not with eg `nlp.process()`
        # parsed_text: spacy.tokens.doc.Doc = self.spacy_model(text=text)
        # return parsed_text

    def _download_model(self):
        if self.language == "lat":
            # Use Patrick Burns's Spacy models, hosted on HuggingFace
            subprocess.check_call([
                "pip",
                "install",
                "https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl"
            ])
        else:
            raise CLTKException(f"No spaCy model found for language '{self.language}'. If you know of a publicly available spaCy model for '{self._language}', please open a pull request (with this message) at `https://github.com/cltk/cltk/issues`.")

    def _is_model_present(self):
        return spacy.util.is_package(self.spacy_model_name)

    @classmethod
    def get_nlp(cls, language: str):
        """

        :param language: Language parameter to retrieve an already-loaded model or the default model.
        :return: A saved instance of `SpacyWrapper`.
        """
        if language in cls.nlps:
            return cls.nlps[language]
        else:
            nlp = cls(language)
            cls.nlps[language] = nlp
            return nlp

    def is_wrapper_available(self) -> bool:
        """Maps an ISO 639-3 language id (e.g., ``lat`` for Latin) to
        that used by ``spacy`` (``la``); confirms that this is
        a language the CLTK supports (i.e., is it pre-modern or not).

        >>> spacy_wrapper = SpacyWrapper(language='lat', interactive=False, silent=True)
        >>> spacy_wrapper.is_wrapper_available()
        True
        """
        return self.language in MAP_LANGS_CLTK_SPACY

    def _get_spacy_code(self) -> str:
        """Get Spacy abbreviation from the ISO standard name."""
        return MAP_LANGS_CLTK_SPACY[self.language]

    def _get_spacy_model_name(self) -> str:
        return MAP_LANG_TO_SPACY_MODEL_NAME[self.language]

    def _get_spacy_model_url(self) -> str:
        return MAP_LANG_TO_SPACY_MODEL_URL[self.language]

    def _load_model(self):
        """Load model into memory."""

        return spacy.load(self.spacy_model_name)
