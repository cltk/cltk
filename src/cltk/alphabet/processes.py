"""This module holds the ``Process`` for normalizing text strings, usually
before the text is sent to other processes.
"""

from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.alphabet.grc.grc import normalize_grc
from cltk.alphabet.lat import normalize_lat
from cltk.core.data_types import Doc, Process


@dataclass
class NormalizeProcess(Process):
    """Generic process for text normalization."""

    language: str = None

    @cachedproperty
    def algorithm(self):
        if self.language == "grc":
            return normalize_grc
        elif self.language == "lat":
            return normalize_lat

    def run(self, input_doc: Doc) -> Doc:
        """This ideally returns an algorithm that takes and returns a string."""
        normalized_text = self.algorithm(input_doc.raw)
        input_doc.normalized_text = normalized_text
        return input_doc


@dataclass
class GreekNormalizeProcess(NormalizeProcess):
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
