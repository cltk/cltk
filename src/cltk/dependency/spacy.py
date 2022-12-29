
import logging
import os.path
from typing import Union, Optional

import spacy
from cltk.utils import suppress_stdout
from spacy.tokens import Doc

from cltk.core.exceptions import (
    CLTKException,
    UnimplementedAlgorithmError,
    UnknownLanguageError,
)

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

        if not self._is_model_present:
            self._download_model()

        with suppress_stdout():
            self.nlp = self._load_pipeline()
            self.nlps[self.language] = self.nlp

    @property
    def is_wrapper_available(self) -> bool:
        return self.language in MAP_LANGS_CLTK_SPACY

    def _load_pipeline(self) -> Optional[spacy.Language]:

        models_dir = os.path.expanduser("~/")
        if self.language in ["la", "lat"]:
            self.model = "la_core_cltk_sm"
        elif self.language == "sa":
            self.model = ""
            # https://huggingface.co/Jacobo/grc_ud_proiel_trf/resolve/main/grc_ud_proiel_trf-any-py3-none-any.whl
        elif self.language == "grc":
            self.model = "grc_ud_proiel_sm"
        else:
            raise CLTKException(f"No spaCy model found for language {self.language}")
        nlp = spacy.load(self.model)
        return nlp

    def parse(self, text: str) -> Optional[Doc]:
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
        os.system(f"python -m spacy download {self.model}")

    @property
    def _is_model_present(self):
        return True

    @classmethod
    def get_nlp(cls, language: str):
        if language in cls.nlps:
            return cls.nlps[language]
        else:
            nlp = cls(language)
            cls.nlps[language] = nlp
            return nlp




