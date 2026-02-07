"""Tests for UD feature normalization helpers."""

from cltk.core.data_types import UDFeatureTag
from cltk.morphosyntax.normalization import (
    UDFeatureRemapReport,
    convert_pos_features_to_ud,
    normalize_ud_feature_pair,
)


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


def test_convert_pos_features_to_ud_populates_remap_report() -> None:
    report = UDFeatureRemapReport()
    tag_set = convert_pos_features_to_ud(
        "Case=Nom|PronType=Con|Form=Emp|PronType=Con",
        remap_report=report,
        source_word="ipsorum",
    )

    assert tag_set is not None
    assert len(tag_set.features) == 4
    assert tag_set.features[0].key == "Case"
    assert tag_set.features[0].value == "Nom"
    assert report.total_count == 0
    assert report.unique_count == 0
    assert report.unmapped_pairs[("PronType", "Con")] == 0
    assert report.unmapped_pairs[("Form", "Emp")] == 0
    assert report.pair_word_counts[("PronType", "Con")]["ipsorum"] == 0
    assert report.pair_word_counts[("Form", "Emp")]["ipsorum"] == 0


def test_ud_feature_remap_report_renders_suggestions_sorted() -> None:
    report = UDFeatureRemapReport()
    report.record("PronType", "Con", source_word="quod")
    report.record("Form", "Emp", source_word="ipsorum")
    report.record("PronType", "Con", source_word="qui")
    report.record("NumValue", "1", source_word="unum")

    suggestions = report.as_mapping_suggestions()

    assert "ud_feature_pair_remap" in suggestions
    assert (
        "('PronType', 'Con'): ('<UD_KEY>', '<UD_VALUE>'),  # seen 2x; words:"
        in suggestions
    )
    assert "'quod'(1x)" in suggestions
    assert "'qui'(1x)" in suggestions
    assert (
        "('Form', 'Emp'): ('<UD_KEY>', '<UD_VALUE>'),  # seen 1x; words: 'ipsorum'(1x)"
    ) in suggestions
    lines = suggestions.splitlines()
    pron_idx = next(i for i, line in enumerate(lines) if "('PronType', 'Con')" in line)
    form_idx = next(i for i, line in enumerate(lines) if "('Form', 'Emp')" in line)
    num_idx = next(i for i, line in enumerate(lines) if "('NumValue', '1')" in line)
    assert pron_idx < form_idx
    assert pron_idx < num_idx
