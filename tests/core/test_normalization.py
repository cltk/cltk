"""Tests for UD feature normalization helpers."""

from cltk.core.data_types import UDFeatureTag
from cltk.morphosyntax.normalization import normalize_ud_feature_pair


def test_normalize_ud_feature_pair_remaps_key_only() -> None:
    normalized = normalize_ud_feature_pair("InflClass[nominal]", "IndEurA")
    assert normalized == ("InflClass", "IndEurA")


def test_ud_feature_tag_accepts_key_only_remap() -> None:
    feature_tag = UDFeatureTag(key="InflClass[nominal]", value="IndEurA")
    assert feature_tag.key == "InflClass"
    assert feature_tag.value == "IndEurA"


def test_normalize_ud_feature_pair_still_remaps_known_pair() -> None:
    normalized = normalize_ud_feature_pair("Tense", "Perf")
    assert normalized == ("Aspect", "Perf")
