"""Preset declarative pipelines."""

from __future__ import annotations

from cltk.pipeline.specs import PipelineSpec, StepSpec


def _profile_config(profile: str | None) -> dict[str, str]:
    """Return a config dict for a prompt profile, if provided."""
    return {"prompt_profile": profile} if profile else {}


def _latin_steps(
    *, morph_profile: str | None, dep_profile: str | None, trans_profile: str | None
) -> list[StepSpec]:
    """Build ordered Latin GenAI steps with optional prompt profiles."""
    return [
        StepSpec(id="normalize"),
        StepSpec(id="sentence_split"),
        StepSpec(id="morphosyntax.genai", config=_profile_config(morph_profile)),
        StepSpec(id="dependency.genai", config=_profile_config(dep_profile)),
        StepSpec(id="enrichment.lexicon"),
        StepSpec(id="enrichment.phonology"),
        StepSpec(id="enrichment.idioms"),
        StepSpec(id="enrichment.pedagogy"),
        StepSpec(id="translation.genai", config=_profile_config(trans_profile)),
    ]


_PRESETS: dict[str, PipelineSpec] = {
    "latin.genai.default": PipelineSpec(
        preset="latin.genai.default",
        language="lati1261",
        steps=_latin_steps(
            morph_profile="latin_ud_strict",
            dep_profile="latin_ud_strict",
            trans_profile=None,
        ),
    ),
    "latin.genai.student_friendly": PipelineSpec(
        preset="latin.genai.student_friendly",
        language="lati1261",
        steps=_latin_steps(
            morph_profile="latin_ud_strict",
            dep_profile="latin_ud_strict",
            trans_profile="student_friendly",
        ),
    ),
    "latin.genai.epigraphy_conservative": PipelineSpec(
        preset="latin.genai.epigraphy_conservative",
        language="lati1261",
        steps=_latin_steps(
            morph_profile="epigraphy_conservative",
            dep_profile="epigraphy_conservative",
            trans_profile="epigraphy_conservative",
        ),
    ),
}


def list_presets() -> list[str]:
    """Return available preset names."""
    return sorted(_PRESETS)


def get_preset(name: str) -> PipelineSpec:
    """Return a deep copy of the named preset."""
    try:
        preset = _PRESETS[name]
    except KeyError as exc:
        available = ", ".join(sorted(_PRESETS))
        raise KeyError(f"Unknown preset '{name}'. Available: {available}") from exc
    return preset.model_copy(deep=True)
