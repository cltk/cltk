"""Tests for prompt profile registry behavior."""

from cltk.genai.prompt_registry import PromptProfileRegistry, build_prompt_info


def test_prompt_profile_registry_returns_template() -> None:
    """Return prompt templates and render PromptInfo."""
    template = PromptProfileRegistry.get_prompt("latin_ud_strict", "morphosyntax.genai")
    assert template.version == "1.0"
    assert len(template.digest) == 64

    info = build_prompt_info(template, lang_or_dialect_name="Latin", text="Salve")
    assert "Salve" in info.text
    assert info.digest == template.digest


def test_prompt_profile_registry_dependency_variant() -> None:
    """Resolve dependency prompt variants from a template."""
    template = PromptProfileRegistry.get_prompt("latin_ud_strict", "dependency.genai")
    info = build_prompt_info(
        template,
        variant="tokens",
        lang_or_dialect_name="Latin",
        token_table="INDEX\tFORM\tUPOS\tFEATS",
        sentence="Salve",
        text="Salve",
    )
    assert "INDEX" in info.text
    assert info.digest == template.digest
