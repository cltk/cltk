"""Factory for generating language-specific process classes.

This module eliminates boilerplate by dynamically creating language-specific
subclasses of GenAI process base classes. The generated classes are fully
compatible with Pydantic and maintain backward compatibility with existing
import patterns.
"""

from typing import Any, Optional

from cltk.languages.definitions import LANGUAGE_DEFINITIONS, LanguageDef


def make_genai_morphosyntax_process(
    base_class: type,
    class_prefix: str,
    glottolog_id: str,
    display_name: str,
) -> type:
    """Create a language-specific morphosyntax process class.

    Args:
        base_class: The GenAIMorphosyntaxProcess base class.
        class_prefix: Prefix for the class name (e.g., "Latin").
        glottolog_id: Glottolog identifier (e.g., "lati1261").
        display_name: Human-readable language name for descriptions.

    Returns:
        A new class like LatinGenAIMorphosyntaxProcess.

    """
    class_name = f"{class_prefix}GenAIMorphosyntaxProcess"

    # For Pydantic models, we need to define class attributes properly
    # The base class is a Pydantic model, so we create a proper subclass
    namespace: dict[str, Any] = {
        "__module__": "cltk.morphosyntax.processes",
        "__doc__": "Language-specific morphosyntax process using a generative GPT model.",
        "__annotations__": {
            "glottolog_id": Optional[str],
            "description": str,
            "authorship_info": str,
        },
        "glottolog_id": glottolog_id,
        "description": f"Default morphology tagging process using a generative GPT model for the {display_name} language.",
        "authorship_info": "CLTK",
    }

    return type(class_name, (base_class,), namespace)


def make_genai_dependency_process(
    base_class: type,
    class_prefix: str,
    glottolog_id: str,
    display_name: str,
) -> type:
    """Create a language-specific dependency process class.

    Args:
        base_class: The GenAIDependencyProcess base class.
        class_prefix: Prefix for the class name (e.g., "Latin").
        glottolog_id: Glottolog identifier (e.g., "lati1261").
        display_name: Human-readable language name for descriptions.

    Returns:
        A new class like LatinGenAIDependencyProcess.

    """
    class_name = f"{class_prefix}GenAIDependencyProcess"

    namespace: dict[str, Any] = {
        "__module__": "cltk.dependency.processes",
        "__doc__": "Language-specific dependency process using a generative GPT model.",
        "__annotations__": {
            "glottolog_id": Optional[str],
            "description": str,
            "authorship_info": str,
        },
        "glottolog_id": glottolog_id,
        "description": f"Default dependency syntax parsing process using a generative GPT model for the {display_name} language.",
        "authorship_info": "CLTK",
    }

    return type(class_name, (base_class,), namespace)


def generate_language_processes(
    module_globals: dict[str, Any],
    base_class: type,
    factory_func: Any,
    language_definitions: tuple[LanguageDef, ...] = LANGUAGE_DEFINITIONS,
) -> list[str]:
    """Generate all language-specific process classes and inject into module.

    Args:
        module_globals: The module's globals() dict to inject classes into.
        base_class: The base process class.
        factory_func: Factory function (make_genai_morphosyntax_process or
            make_genai_dependency_process).
        language_definitions: Tuple of LanguageDef namedtuples.

    Returns:
        List of generated class names for __all__.

    """
    generated_names: list[str] = []

    for lang_def in language_definitions:
        cls = factory_func(
            base_class=base_class,
            class_prefix=lang_def.class_prefix,
            glottolog_id=lang_def.glottolog_id,
            display_name=lang_def.display_name,
        )
        module_globals[cls.__name__] = cls
        generated_names.append(cls.__name__)

    return generated_names
