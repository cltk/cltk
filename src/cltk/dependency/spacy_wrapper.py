"""Wrapper for spaCy NLP software and models."""

import logging
import subprocess
from typing import Any, Optional

import spacy
from spacy import Language as SpacyLanguage
from spacy.tokens import Doc as SpacyDoc

from cltk.core.exceptions import CLTKException, UnknownLanguageError
from cltk.utils.utils import query_yes_no

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

MAP_LANGS_CLTK_SPACY = {
    "grc": "grc",
    "lat": "la",
}

MAP_LANG_TO_SPACY_MODEL_NAME: dict[str, str] = {
    "grc": "grc_odycy_joint_sm",
    "lat": "la_core_web_lg",
}

MAP_LANG_TO_SPACY_MODEL_URL: dict[str, str] = {
    "grc": "https://huggingface.co/chcaa/grc_odycy_joint_sm/resolve/main/grc_odycy_joint_sm-any-py3-none-any.whl",
    "lat": "https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl",
}


class SpacyWrapper:
    """`SpacyWrapper` has been made to be an interface
    between spaCy and CLTK.
    """

    nlps: dict[str, "SpacyWrapper"] = dict()

    def __init__(
        self,
        language: str,
        nlp: Optional[SpacyLanguage] = None,
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
        self.language: str = language
        self.nlp: Optional[SpacyLanguage] = nlp
        self.interactive: bool = interactive
        self.silent: bool = silent
        self.spacy_model: Optional[SpacyLanguage] = None
        # self.spacy_debug_level = spacy_debug_level

        if self.interactive and self.silent:
            raise ValueError(
                "``interactive`` and ``silent`` options are not compatible with each other."
            )

        self.wrapper_available: bool = self.is_wrapper_available()
        if not self.wrapper_available:
            raise UnknownLanguageError(
                f"Language '{self.language}' either not in scope for CLTK or the project does know about it. If you know of a publicly available spaCy model for '{self.language}', please open a pull request (with this message) at `https://github.com/cltk/cltk/issues`."
            )
        self.spacy_code: str = self._get_spacy_code()
        self.spacy_model_name: str = self._get_spacy_model_name()
        self.spacy_model_url: str = self._get_spacy_model_url()

        if not self._is_model_present():
            self._download_model()

        # if not self.spacy_model:
        if not self.nlp:
            self.nlp = self._load_model()

    def parse(self, text: str) -> SpacyDoc:
        """
        >>> from cltk.languages.example_texts import get_example_text
        >>> spacy_wrapper: SpacyWrapper = SpacyWrapper(language="lat")
        >>> latin_spacy_doc: SpacyDoc = spacy_wrapper.parse(get_example_text("lat"))

        :param text: Text to analyze.
        :return:
        """
        if isinstance(self.nlp, SpacyLanguage):
            # Note: spacy's `nlp` object is called directly, not with eg `nlp.process()`
            return self.nlp(text)
        raise CLTKException(
            "No spaCy model has been loaded. Is the language supported? "
            "Otherwise try to provide a spaCy model with `nlp` argument."
        )

    def _download_model(self) -> None:
        if not self.interactive:
            if not self.silent:
                print(
                    f"CLTK message: Going to download required a spaCy model ``{self.spacy_model_name}`` from ``{self.spacy_model_url}`` ..."
                )  # pragma: no cover
        else:
            print(  # pragma: no cover
                "CLTK message: This part of the CLTK depends upon a spaCy NLP mode."
            )  # pragma: no cover
            dl_is_allowed: bool = query_yes_no(
                f"CLTK message: Allow download of spaCy model ``{self.spacy_model_name}`` from ``{self.spacy_model_url}``?"
            )
            if not dl_is_allowed:
                raise CLTKException(
                    f"Download of necessary spaCy model declined for '{self.language}'. Unable to continue with spaCy's processing."
                )
        if self.language == "lat":
            # Use Patrick Burns's Spacy models, hosted on HuggingFace
            subprocess.check_call(
                [
                    "pip",
                    "install",
                    "https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl",
                ]
            )
        elif self.language == "grc":
            # Use OdyCy's Spacy models, hosted on HuggingFace
            subprocess.check_call(
                [
                    "pip",
                    "install",
                    "https://huggingface.co/chcaa/grc_odycy_joint_sm/resolve/main/grc_odycy_joint_sm-any-py3-none-any.whl",
                ]
            )
        else:
            raise CLTKException(
                f"No spaCy model found for language '{self.language}'. If you know of a publicly available spaCy model for '{self.language}', please open a pull request (with this message) at `https://github.com/cltk/cltk/issues`."
            )

    def _is_model_present(self) -> bool:
        return spacy.util.is_package(self.spacy_model_name)

    @classmethod
    def get_nlp(cls, language: str) -> "SpacyWrapper":
        """

        :param language: Language parameter to retrieve an already-loaded model or the default model.
        :return: A saved instance of `SpacyWrapper`.
        """
        if language in cls.nlps:
            return cls.nlps[language]
        nlp: SpacyWrapper = cls(language)
        cls.nlps[language] = nlp
        return nlp

    def is_wrapper_available(self) -> bool:
        """Maps an ISO 639-3 language id (e.g., ``lat`` for Latin) to
        that used by ``spacy`` (``la``); confirms that this is
        a language the CLTK supports (i.e., is it pre-modern or not).

        >>> spacy_wrapper: SpacyWrapper = SpacyWrapper(language='lat', interactive=False, silent=True)
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

    def _load_model(self) -> SpacyLanguage:
        """Load model into memory."""
        return spacy.load(self.spacy_model_name)
