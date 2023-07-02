
import logging
import os.path
import subprocess
import sys

import spacy
from spacy.tokens import Doc

from cltk.core.exceptions import (
    CLTKException,
    UnimplementedAlgorithmError,
    UnknownLanguageError,
)
from cltk.utils import suppress_stdout


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

MAP_LANGS_CLTK_SPACY = {
    "lat": "Latin",
    # "grc": "Ancient_Greek",
    # "sa": "Sanskrit"
}


class SpacyWrapper:

    nlps = {}

    def __init__(self,
                 language: str,
                 interactive: bool = True,
                 silent: bool = False):
        """

        :param language:
        :param interactive:
        :param silent:
        """
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
            self.nlp = self._load_pipeline()
            self.nlps[self.language] = self.nlp

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

        models_dir = os.path.expanduser("~/")

        nlp = spacy.load(self.model)
        return nlp

    def parse(self, text: str) -> Doc:
        """
        >>> from cltk.languages.example_texts import get_example_text
        >>> spacy_wrapper = SpacyWrapper(language="lat")
        >>> latin_nlp = spacy_wrapper.parse(get_example_text("lat"))

        >>> latin_nlp.sents[0]


        :param text:
        :return:
        """
        return self.nlp(text)

    def _download_model(self):
        models_dir = os.path.expanduser("~/")
        if self.language in ["la", "lat"]:
            package = "https://huggingface.co/latincy/la_core_web_md/resolve/main/la_core_web_md-3.5.1/dist/la_core_web_md-3.5.1.tar.gz"
            # package = "https://huggingface.co/latincy/la_core_web_md/blob/main/la_core_web_md-any-py3-none-any.whl"
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        # elif self.language == "sa":
        #     package = ""
            # https://huggingface.co/Jacobo/grc_ud_proiel_trf/resolve/main/grc_ud_proiel_trf-any-py3-none-any.whl
        # elif self.language == "grc":
        #     TODO change it?
            # package = "grc_ud_proiel_sm"
        else:
            raise CLTKException(f"No spaCy model found for language {self.language}")
        spacy.cli.download(self.model)

    @property
    def _is_model_present(self):
        return spacy.util.is_package(self.model)

    @classmethod
    def get_nlp(cls, language: str):
        if language in cls.nlps:
            return cls.nlps[language]
        else:
            nlp = cls(language)
            cls.nlps[language] = nlp
            return nlp




