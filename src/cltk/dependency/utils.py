"""Misc helper functions for extracting dependency
info from CLTK data structures.
"""

from typing import Any, List, Optional

from cltk.core.data_types import Word


def get_governor_word(word: Word, sentence: List[Word]) -> Optional[Word]:
    """Submit a ``Word`` and a sentence (being a list of ``Word``)
    and then return the governing word.
    """
    governor = word.governor
    if governor == -1:
        return None
    return sentence[word.governor]


def get_governor_relationship(word: Word, sentence: List[Word]) -> Optional[Any]:
    """Get the dependency relationship of a dependent to its governor."""
    pass
