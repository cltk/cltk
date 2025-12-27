"""Tests for pipeline spec TOML loading."""

from pathlib import Path

import pytest

from cltk.pipeline.spec_io import load_pipeline_spec


def _write(tmp_path: Path, text: str) -> Path:
    """Write a temporary pipeline TOML file."""
    path = tmp_path / "pipeline.toml"
    path.write_text(text, encoding="utf-8")
    return path


def test_load_pipeline_spec_nested_steps(tmp_path: Path) -> None:
    """Load nested [step.*] tables and apply to preset ordering."""
    toml = """
    preset = "latin.genai.default"

    [step.dependency.genai]
    enabled = false
    """
    path = _write(tmp_path, toml)
    spec = load_pipeline_spec(path)
    assert spec.steps is not None
    dep = next(step for step in spec.steps if step.id == "dependency.genai")
    assert dep.enabled is False
    assert spec.steps[0].id == "normalize"


def test_load_pipeline_spec_quoted_steps(tmp_path: Path) -> None:
    """Load quoted step keys and inline config."""
    toml = """
    steps = ["dependency.genai"]

    [step."dependency.genai"]
    prompt_profile = "latin_ud_strict"
    """
    path = _write(tmp_path, toml)
    spec = load_pipeline_spec(path)
    assert spec.steps is not None
    step = spec.steps[0]
    assert step.id == "dependency.genai"
    assert step.config["prompt_profile"] == "latin_ud_strict"


def test_step_overrides_merge(tmp_path: Path) -> None:
    """Merge step_overrides into per-step config."""
    toml = """
    steps = ["morphosyntax.genai"]

    [step.morphosyntax.genai]
    prompt_profile = "latin_ud_strict"

    [step_overrides.morphosyntax.genai]
    prompt_version = "1.0"
    """
    path = _write(tmp_path, toml)
    spec = load_pipeline_spec(path)
    assert spec.steps is not None
    step = spec.steps[0]
    assert step.config["prompt_profile"] == "latin_ud_strict"
    assert step.config["prompt_version"] == "1.0"


def test_missing_steps_requires_preset(tmp_path: Path) -> None:
    """Raise when neither steps nor preset is provided."""
    toml = """
    language = "lati1261"
    """
    path = _write(tmp_path, toml)
    with pytest.raises(ValueError, match="Available presets"):
        load_pipeline_spec(path)
