"""Hold the ``Process`` for normalizing text strings.

Usually used before the text is sent to other processes.
"""

from functools import cached_property
from typing import Callable, Optional

from cltk.core.cltk_logger import logger
from cltk.core.data_types import Doc, Process
from cltk.text.utils import cltk_normalize


class NormalizeProcess(Process):
    """Generic process for text normalization."""

    language_code: Optional[str] = None

    @cached_property
    def algorithm(self) -> Callable[[str], str]:
        # TODO: Decide whether to strip out section numbers with `text = strip_section_numbers(text)`
        logger.debug(
            f"`NormalizeProcess()`: Generic normalization for: {self.language_code}"
        )
        return cltk_normalize

    def run(self, input_doc: Doc) -> Doc:
        """Invoke language-appropriate normalization code for text a given language."""
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


class MultilingualNormalizeProcess(NormalizeProcess):
    """Text normalization for multiple languages."""

    def __post_init__(self) -> None:
        logger.debug("MultilingualNormalizeProcess initialized.")
