
import logging
import subprocess
import sys

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

    nlps = {}

    def __init__(self,
                 language: str,
                 spacy_language: spacy.Language = None,
                 interactive: bool = True,
                 silent: bool = False):
        """

        :param language: One of the officially supported languages by CLTK. It selects a default model for
        :param spacy_language: A `Language` instance from spaCy (not used by default).
        :param interactive: Are downloads interactive?
        :param silent: Is it verbose?
        """
        self.spacy_language = spacy_language
        if self.spacy_language:
            self.language = self.spacy_language.lang
            self.nlps[self.language] = self
        else:

            self.language = language
            self._interactive = interactive
            self._silent = silent

            if self._interactive and self._silent:
                raise ValueError(
                    "``interactive`` and ``silent`` options are not compatible with each other."
                )

            if not self.is_wrapper_available:
                raise UnknownLanguageError(f"Language {self.language} is not supported by CLTK wrapper of SpaCy.")

            self._select_model()

            if not self._is_model_present:
                self._download_model()

            with suppress_stdout():
                self.spacy_language = self._load_pipeline()
                self.nlps[self.language] = self

    @property
    def is_wrapper_available(self) -> bool:
        return self.language in MAP_LANGS_CLTK_SPACY

    def _select_model(self):
        if self.language in ["la", "lat"]:
            self.model = "la_core_web_md"
        # elif self.language == "sa":
        #     self.model = ""
        # elif self.language == "grc":
        #     self.model = ""
        else:
            raise CLTKException(f"No spaCy model found for language {self.language}")

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
        return self.spacy_language(text)

    def _download_model(self):
        if self.language in ["la", "lat"]:
            package = "https://huggingface.co/latincy/la_core_web_md/resolve/main/la_core_web_md-3.5.1/dist/la_core_web_md-3.5.1.tar.gz"
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        else:
            raise CLTKException(f"No spaCy model found for language '{self.language}'")
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




