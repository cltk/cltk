"""This module holds the ``Process`` for normalizing text strings, usually
before the text is sent to other processes.
"""

from dataclasses import dataclass
from typing import Optional

from boltons.cacheutils import cachedproperty  # type: ignore

from cltk.alphabet.grc.grc import normalize_grc
from cltk.alphabet.lat import normalize_lat
from cltk.core.cltk_logger import logger
from cltk.core.data_types import Doc, Process


@dataclass
class NormalizeProcess(Process):
    """Generic process for text normalization."""

    language: Optional[str] = None

    @cachedproperty
    def algorithm(self):
        logger.debug(f"Selecting normalization algorithm for language: {self.language}")
        if self.language == "grc":
            logger.info("Using Ancient Greek normalization algorithm.")
            return normalize_grc
        elif self.language == "lat":
            logger.info("Using Latin normalization algorithm.")
            return normalize_lat
        logger.warning(
            f"No normalization algorithm found for language: {self.language}"
        )
        return None

    def run(self, input_doc: Doc) -> Doc:
        """This ideally returns an algorithm that takes and returns a string."""
        logger.debug(f"Running normalization for language: {self.language}")
        if self.algorithm is None:
            logger.error(
                f"No normalization algorithm found for language '{self.language}'"
            )
            raise ValueError(
                f"No normalization algorithm found for language '{self.language}'"
            )
        if input_doc.raw is None:
            logger.error("input_doc.raw must not be None")
            raise ValueError("input_doc.raw must not be None")
        normalized_text = self.algorithm(input_doc.raw)
        input_doc.normalized_text = normalized_text
        logger.info(
            f"Normalized text: {input_doc.normalized_text[:50]}..."
            if input_doc.normalized_text
            else "Normalized text is empty."
        )
        return input_doc


@dataclass
class AncientGreekNormalizeProcess(NormalizeProcess):
    """Text normalization for Ancient Greek.

    >>> from cltk.core.data_types import Doc, Word
    >>> from cltk.languages.example_texts import get_example_text
    >>> from boltons.strutils import split_punct_ws
    >>> lang = "grc"
    >>> orig_text = get_example_text(lang)
    >>> non_normed_doc = Doc(raw=orig_text)
    >>> normalize_proc = GreekNormalizeProcess(language=lang)
    >>> normalized_text = normalize_proc.run(input_doc=non_normed_doc)
    >>> normalized_text == orig_text
    False
    """

    language = "grc"

    def __post_init__(self):
        logger.debug("AncientGreekNormalizeProcess initialized.")


@dataclass
class LatinNormalizeProcess(NormalizeProcess):
    """Text normalization for Latin.

    >>> from cltk.core.data_types import Doc, Word
    >>> from cltk.languages.example_texts import get_example_text
    >>> from boltons.strutils import split_punct_ws
    >>> lang = "lat"
    >>> orig_text = get_example_text(lang)
    >>> non_normed_doc = Doc(raw=orig_text)
    >>> normalize_proc = LatinNormalizeProcess(language=lang)
    >>> normalized_text = normalize_proc.run(input_doc=non_normed_doc)
    >>> normalized_text == orig_text
    False
    """

    language = "lat"

    def __post_init__(self):
        logger.debug("LatinNormalizeProcess initialized.")
