"""Misc helper functions for extracting dependency
info from CLTK data structures.
"""

from typing import Any, Optional

from cltk.core.data_types import Word


def get_governor_word(word: Word, sentence: list[Word]) -> Optional[Word]:
    """Submit a ``Word`` and a sentence (being a list of ``Word``)
    and then return the governing word.
    """
    governor: int = word.governor
    if governor == -1:
        return None
    # Note: We need to remove 1 to get the 0-based index of `sentence.words`
    try:
        return sentence[word.governor]
    except IndexError:
        print(word)


def get_governor_word2(word: Word, sentence_words: list[Word]) -> Optional[Word]:
    """Submit a ``Word`` and a sentence (being a list of ``Word``)
    and then return the governing word.
    """
    for sentence_word in sentence_words:
        if sentence_word.index_token == word.index_token:
            return sentence_word
    return None
    # governor: int = word.governor
    # if governor == -1:
    #     return None
    # # Note: We need to remove 1 to get the 0-based index of `sentence.words`
    # try:
    #     return sentence[word.governor]
    # except IndexError:
    #     print(word)


def get_governor_relationship(word: Word, sentence: list[Word]) -> Optional[Any]:
    """Get the dependency relationship of a dependent to its governor."""
    pass
