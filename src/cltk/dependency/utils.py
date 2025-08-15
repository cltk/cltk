"""Misc helper functions for extracting dependency
info from CLTK data structures.
"""

from typing import Any, Optional

from cltk.core.cltk_logger import logger
from cltk.core.data_types_v2 import Word
from cltk.morphology.ud_features import UDFeatureTag, UDFeatureTagSet


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


def convert_pos_features_to_ud(feats_raw: str) -> Optional[UDFeatureTagSet]:
    features_tag_set = UDFeatureTagSet()
    # Ensure inner tuple has only 2 elements
    raw_features_pairs: list[tuple[str, str]] = [
        tup
        for tup in (
            tuple(pair.split("=", maxsplit=1))
            for pair in feats_raw.split("|")
            if "=" in pair
        )
        if len(tup) == 2
    ]
    logger.debug(f"raw_features_pairs: {raw_features_pairs}")
    raw_feature_pairs: tuple[str, str]
    for raw_feature_pairs in raw_features_pairs:
        raw_feature_key: str = raw_feature_pairs[0]
        raw_feature_value: str = raw_feature_pairs[1]
        # TODO: Do some validation to ensure the tag value is not multiple (check for commas)
        feature_tag: UDFeatureTag = UDFeatureTag(
            key=raw_feature_key,
            value=raw_feature_value,
        )
        logger.debug(f"feature_tag: {feature_tag}")
        features_tag_set.features.append(feature_tag)
        return features_tag_set
