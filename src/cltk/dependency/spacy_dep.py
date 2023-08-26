
import logging
import subprocess
import sys
from typing import Optional

import spacy
from spacy.tokens import Doc

from cltk.core.exceptions import (
    CLTKException,
    UnknownLanguageError,
)
from cltk.utils import suppress_stdout


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

MAP_LANGS_CLTK_SPACY = {
    "lat": "Latin",
}


class SpacyWrapper:
    """
    `SpacyWrapper` has been made to be an interface between spaCy and CLTK.

    """

    nlps = {}

    def __init__(self,
                 language: str,
                 nlp: Optional[spacy.Language] = None,
                 interactive: bool = True,
                 silent: bool = False):
        """

        :param language: One of the officially supported languages by CLTK. It selects a default model for
        :param nlp: A `Language` instance from spaCy (not used by default).
        :param interactive: Are downloads interactive?
        :param silent: Is it verbose?
        """
        self.nlp = nlp
        if self.nlp:
            self._language = self.nlp.lang
            self.nlps[self._language] = self
        else:

            self._language = language
            self._interactive = interactive
            self._silent = silent

            if self._interactive and self._silent:
                raise ValueError(
                    "``interactive`` and ``silent`` options are not compatible with each other."
                )

            if not self.is_wrapper_available:
                raise UnknownLanguageError(f"Language {self._language} is not supported by CLTK wrapper of SpaCy.")

            self._select_model()

            if not self._is_model_present:
                self._download_model()

            with suppress_stdout():
                self.nlp = self._load_pipeline()
                self.nlps[self._language] = self

    @property
    def language(self) -> str:
        return self._language

    @property
    def silent(self) -> bool:
        return self._silent

    @property
    def interactive(self) -> bool:
        return self._interactive

    @property
    def is_wrapper_available(self) -> bool:
        return self._language in MAP_LANGS_CLTK_SPACY

    def _select_model(self):
        if self._language in ["la", "lat"]:
            self.model = "la_core_web_md"
        else:
            raise CLTKException(f"No spaCy model found for language {self._language}")

    def _load_pipeline(self) -> spacy.Language:
        nlp = spacy.load(self.model)
        return nlp

    def parse(self, text: str) -> Doc:
        """
        >>> from cltk.languages.example_texts import get_example_text
        >>> spacy_wrapper = SpacyWrapper(language="lat")
        >>> latin_nlp = spacy_wrapper.parse(get_example_text("lat"))

        >>> latin_nlp.sents[0]


        :param text: Text to analyze.
        :return:
        """
        if isinstance(self.nlp, spacy.Language):
            return self.nlp(text)
        raise CLTKException("No spaCy model has been loaded. Is the language supported? "
                            "Otherwise try to provide a spaCy model with `nlp`argument.")

    def _download_model(self):
        if self._language in ["la", "lat"]:
            package = "https://huggingface.co/latincy/la_core_web_md/resolve/main/la_core_web_md-3.5.1/dist/la_core_web_md-3.5.1.tar.gz"
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        else:
            raise CLTKException(f"No spaCy model found for language '{self._language}'")
        spacy.cli.download(self.model)

    @property
    def _is_model_present(self):
        return spacy.util.is_package(self.model)

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
