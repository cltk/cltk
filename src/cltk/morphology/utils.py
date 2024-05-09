"""Misc helper functions for extracting morphological
info from CLTK data structures.
"""

from typing import Optional, Union

from cltk.core.data_types import Word
from cltk.core.exceptions import CLTKException
from cltk.morphology.universal_dependencies_features import (
    NOMINAL_FEATURES,
    VERBAL_FEATURES,
    MorphosyntacticFeature,
)

ALL_POSSIBLE_FEATURES = NOMINAL_FEATURES + VERBAL_FEATURES


def get_pos(word: Optional[Word]) -> Optional[str]:
    """Take word, return structured info."""
    if not word:
        return None
    # Note: SpaCy word.pos.name for stanza, word.pos for spacy
    # TODO: Write this properly upstream!
    if hasattr(word.pos, "name"):
        return word.pos.name
    else:
        return word.pos


def get_features(
    word: Optional[Word],
    prepend_to_label: str = None,
) -> tuple[list[str], list[Union[str, int, float, None]]]:
    """Take a word, return a list of feature labels."""

    features_present: list[Union[str, None]] = list()
    feature_variables: list[str] = list()
    for possible_feature in ALL_POSSIBLE_FEATURES:
        feature_variables.append(str(possible_feature).lower())
        if not word:
            features_present.append(None)
            continue
        try:
            feat: MorphosyntacticFeature = word.__getattr__(possible_feature)[0]
            features_present.append(str(feat.name))
        except CLTKException:
            features_present.append(None)
    if prepend_to_label:
        feature_variables = [prepend_to_label + name for name in feature_variables]
    return feature_variables, features_present
