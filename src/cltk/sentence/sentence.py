"""Tokenize sentences."""

__author__ = [
    "Patrick J. Burns <patrick@diyclassics.org>",
    "Kyle P. Johnson <kyle@kyle-p-johnson.com>",
    "Anoop Kunchukuttan <anoop.kunchukuttan@gmail.com>",
]
__license__ = "MIT License. See LICENSE."

import os
import re
from abc import ABC, abstractmethod
from typing import List

from nltk.tokenize.punkt import PunktSentenceTokenizer as NLTKPunktSentenceTokenizer

from cltk.core import CLTKException
from cltk.utils import CLTK_DATA_DIR
from cltk.utils.file_operations import open_pickle


class SentenceTokenizer(ABC):
    """Base class for sentences tokenization"""

    @abstractmethod
    def __init__(self, language: str = None):
        """Initialize stoplist builder with option for language specific parameters.

        :param language : language for sentences tokenization
        :type language: str
        """
        if language:
            self.language = language.lower()
        self.model = None
        self.lang_vars = None

    def tokenize(self, text: str, model: object = None) -> List[str]:
        """Method for tokenizing sentences with pretrained punkt models; can
        be overridden by language-specific tokenizers.

        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        if not hasattr(self, "model") or not self.model:
            self.model = model

        tokenizer = self.model
        if not hasattr(tokenizer, "tokenize"):
            raise CLTKException("model does not have 'tokenize' method.")
        if self.lang_vars:
            tokenizer._lang_vars = self.lang_vars
        return tokenizer.tokenize(text)

    def _get_models_path(self, language):  # pragma: no cover
        return (
            CLTK_DATA_DIR
            + f"/{language}/model/{language}_models_cltk/tokenizers/sentence"
        )


class PunktSentenceTokenizer(SentenceTokenizer):
    """Base class for punkt sentences tokenization."""

    missing_models_message = "PunktSentenceTokenizer requires a language model."

    def __init__(self, language: str = None, lang_vars: object = None):
        """Constructor.

        :param language : language for sentences tokenization
        :type language: str
        """
        super().__init__(language=language)
        if self.language == "lat":
            self.language_old = "lat"
        self.lang_vars = lang_vars
        if self.language:
            self.models_path = self._get_models_path(self.language)
            try:
                self.model = open_pickle(
                    os.path.join(
                        os.path.expanduser(self.models_path),
                        f"{self.language_old}_punkt.pickle",
                    )
                )
            except FileNotFoundError as err:
                raise type(err)(PunktSentenceTokenizer.missing_models_message)


class RegexSentenceTokenizer(SentenceTokenizer):
    """Base class for regex sentences tokenization."""

    def __init__(self, language: str = None, sent_end_chars: List[str] = None):
        """Constructor.

        :param language: language for sentences tokenization
        :type language: str
        :param sent_end_chars: list of sentences-ending punctuation marks
        :type sent_end_chars: list
        """
        super().__init__(language)
        if sent_end_chars:
            self.sent_end_chars = sent_end_chars
            self.sent_end_chars_regex = "|".join(self.sent_end_chars)
            self.pattern = rf"(?<=[{self.sent_end_chars_regex}])\s"
        else:
            raise Exception("Must specify sent_end_chars")

    def tokenize(self, text: str, model: object = None) -> List[str]:
        """Method for tokenizing sentences with regular expressions.

        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        """
        sentences = re.split(self.pattern, text)
        return sentences
