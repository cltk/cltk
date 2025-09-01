"""This module holds the ``Process`` for normalizing text strings, usually
before the text is sent to other processes.
"""

from functools import cached_property
from types import FunctionType
from typing import Optional

from cltk.alphabet.grc.grc import normalize_grc
from cltk.alphabet.lat import normalize_lat
from cltk.alphabet.text_normalization import cltk_normalize
from cltk.core.cltk_logger import logger
from cltk.core.data_types import Doc, Process


class NormalizeProcess(Process):
    """Generic process for text normalization."""

    language_code: Optional[str] = None

    @cached_property
    def algorithm(self) -> FunctionType:
        # TODO: Decide whether to strip out section numbers with `text = strip_section_numbers(text)`
        logger.debug(
            f"Selecting normalization algorithm for language: {self.language_code}"
        )
        if self.language_code == "grc":
            logger.info("Using Ancient Greek normalization algorithm.")
            return normalize_grc
        elif self.language_code == "lat":
            logger.info("Using Latin normalization algorithm.")
            return normalize_lat
        else:
            logger.debug(
                f"`NormalizeProcess()`: Generic normalization for: {self.language_code}"
            )
            return cltk_normalize

    def run(self, input_doc: Doc) -> Doc:
        """This invokes language-appropriate normalization code for text a given language."""
        logger.debug(f"Running normalization for language: {self.language_code}")
        if self.algorithm is None:
            logger.error(
                f"No normalization algorithm found for language '{self.language_code}'"
            )
            raise ValueError(
                f"No normalization algorithm found for language '{self.language_code}'"
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


# class AncientGreekNormalizeProcess(NormalizeProcess):
#     """Text normalization for Ancient Greek.

#     >>> from cltk.core.data_types import Doc, Word
#     >>> from cltk.languages.example_texts import get_example_text
#     >>> from boltons.strutils import split_punct_ws
#     >>> lang = "grc"
#     >>> orig_text = get_example_text(lang)
#     >>> non_normed_doc = Doc(raw=orig_text)
#     >>> normalize_proc = GreekNormalizeProcess(language=lang)
#     >>> normalized_text = normalize_proc.run(input_doc=non_normed_doc)
#     >>> normalized_text == orig_text
#     False
#     """

#     language_code: Optional[str] = "grc"

#     def __post_init__(self):
#         logger.debug("AncientGreekNormalizeProcess initialized.")


# class LatinNormalizeProcess(NormalizeProcess):
#     """Text normalization for Latin.

#     >>> from cltk.core.data_types import Doc, Word
#     >>> from cltk.languages.example_texts import get_example_text
#     >>> from boltons.strutils import split_punct_ws
#     >>> lang = "lat"
#     >>> orig_text = get_example_text(lang)
#     >>> non_normed_doc = Doc(raw=orig_text)
#     >>> normalize_proc = LatinNormalizeProcess(language=lang)
#     >>> normalized_text = normalize_proc.run(input_doc=non_normed_doc)
#     >>> normalized_text == orig_text
#     False
#     """

#     language_code: Optional[str] = "lat"

#     def __post_init__(self):
#         logger.debug("LatinNormalizeProcess initialized.")


class MultilingualNormalizeProcess(NormalizeProcess):
    """Text normalization for multiple languages."""

    def __post_init__(self):
        logger.debug("MultilingualNormalizeProcess initialized.")
