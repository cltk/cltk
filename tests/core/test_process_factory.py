"""Tests for the language process factory."""

import re

from cltk.core.process_factory import (
    generate_language_processes,
    make_genai_dependency_process,
    make_genai_morphosyntax_process,
)
from cltk.dependency.processes import GenAIDependencyProcess
from cltk.languages.definitions import LANGUAGE_DEFINITIONS, LanguageDef
from cltk.morphosyntax.processes import GenAIMorphosyntaxProcess


def test_make_genai_morphosyntax_process_creates_valid_class() -> None:
    """Factory should create a proper subclass with correct attributes."""
    cls = make_genai_morphosyntax_process(
        base_class=GenAIMorphosyntaxProcess,
        class_prefix="TestLang",
        glottolog_id="test1234",
        display_name="Test Language",
    )

    assert cls.__name__ == "TestLangGenAIMorphosyntaxProcess"
    assert issubclass(cls, GenAIMorphosyntaxProcess)

    instance = cls()
    assert instance.glottolog_id == "test1234"
    assert "Test Language" in instance.description
    assert instance.authorship_info == "CLTK"


def test_make_genai_dependency_process_creates_valid_class() -> None:
    """Factory should create a proper subclass with correct attributes."""
    cls = make_genai_dependency_process(
        base_class=GenAIDependencyProcess,
        class_prefix="TestLang",
        glottolog_id="test1234",
        display_name="Test Language",
    )

    assert cls.__name__ == "TestLangGenAIDependencyProcess"
    assert issubclass(cls, GenAIDependencyProcess)

    instance = cls()
    assert instance.glottolog_id == "test1234"
    assert "Test Language" in instance.description
    assert instance.authorship_info == "CLTK"


def test_generate_language_processes_populates_module_namespace() -> None:
    """Factory should inject generated classes into module globals."""
    test_globals: dict[str, object] = {}
    test_definitions = (
        LanguageDef("Alpha", "alph1234", "Alpha"),
        LanguageDef("Beta", "beta5678", "Beta"),
    )

    names = generate_language_processes(
        module_globals=test_globals,
        base_class=GenAIMorphosyntaxProcess,
        factory_func=make_genai_morphosyntax_process,
        language_definitions=test_definitions,
    )

    assert "AlphaGenAIMorphosyntaxProcess" in test_globals
    assert "BetaGenAIMorphosyntaxProcess" in test_globals
    assert names == ["AlphaGenAIMorphosyntaxProcess", "BetaGenAIMorphosyntaxProcess"]


def test_language_definitions_have_valid_glottolog_ids() -> None:
    """All language definitions must have valid Glottolog ID format."""
    pattern = re.compile(r"^[a-z]{4}\d{4}$")

    for lang in LANGUAGE_DEFINITIONS:
        assert pattern.match(lang.glottolog_id), (
            f"{lang.class_prefix} has invalid glottolog_id: {lang.glottolog_id}"
        )


def test_language_definitions_count() -> None:
    """Ensure we have the expected number of language definitions."""
    # This acts as a regression test - if languages are added/removed,
    # this test will need to be updated intentionally.
    assert len(LANGUAGE_DEFINITIONS) == 107
