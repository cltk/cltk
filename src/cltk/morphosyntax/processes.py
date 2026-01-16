"""Processes of POS and feature tagging."""

from collections.abc import Callable
from copy import copy
from functools import cached_property
from typing import ClassVar, Optional

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import Doc, Process
from cltk.core.logging_utils import bind_from_doc
from cltk.core.process_factory import (
    generate_language_processes,
    make_genai_morphosyntax_process,
)
from cltk.core.process_registry import register_process
from cltk.genai.prompt_registry import (
    PromptProfileRegistry,
    PromptTemplate,
    build_prompt_info,
)
from cltk.genai.prompts import PromptInfo
from cltk.languages.definitions import LANGUAGE_DEFINITIONS
from cltk.morphosyntax.utils import generate_gpt_morphosyntax_concurrent

# A prompt override can be a callable, a PromptInfo, or a literal string.
PromptBuilder = Callable[[str, str], PromptInfo] | PromptInfo | str


class MorphosyntaxProcess(Process):
    """Base class for morphosyntactic processes."""


@register_process
class GenAIMorphosyntaxProcess(MorphosyntaxProcess):
    """Language-specific morphosyntax process using a generative GPT model."""

    process_id: ClassVar[str] = "morphosyntax.genai"
    # Optional prompt builder override for custom pipelines
    prompt_builder: Optional[PromptBuilder] = None
    prompt_profile: Optional[str] = None
    prompt_version: Optional[str] = None

    @cached_property
    def algorithm(self) -> Callable[..., Doc]:
        """Return the morphosyntax generation function for this process."""
        if not self.glottolog_id:
            msg: str = "glottolog_id must be set for MorphosyntaxProcess"
            bind_context(glottolog_id=self.glottolog_id).error(msg)
            raise ValueError(msg)
        # Prefer the safe concurrent wrapper (async under the hood, sync surface)
        return generate_gpt_morphosyntax_concurrent

    def run(self, input_doc: Doc) -> Doc:
        """Run the configured GPT morphosyntax tagging workflow."""
        output_doc = copy(input_doc)
        if not output_doc.normalized_text:
            msg: str = "Doc must have `normalized_text`."
            bind_from_doc(output_doc).error(msg)
            raise ValueError(msg)
        # Ensure required attributes are present
        if self.glottolog_id is None:
            raise ValueError("glottolog_id must be set for sentence splitting")
        prompt_builder = self.prompt_builder
        prompt_digest = None
        if prompt_builder is None and self.prompt_profile:
            template = PromptProfileRegistry.get_prompt(
                self.prompt_profile, self.process_id, self.prompt_version
            )
            prompt_digest = template.digest

            def _builder(
                lang: str, text: str, _template: PromptTemplate = template
            ) -> PromptInfo:
                """Build a morphosyntax prompt from a profile template."""
                return build_prompt_info(
                    _template, lang_or_dialect_name=lang, text=text
                )

            prompt_builder = _builder
        # Callable typing does not retain keyword names; pass positionally
        output_doc = self.algorithm(
            output_doc,
            prompt_builder=prompt_builder,
            prompt_profile=self.prompt_profile,
            prompt_digest=prompt_digest,
            provenance_process=f"{self.process_id}:{self.__class__.__name__}",
        )
        return output_doc


# -----------------------------------------------------------------------------
# Generate all language-specific process classes dynamically
# -----------------------------------------------------------------------------
# This replaces 107 nearly-identical class definitions with a single factory call.
# Each generated class (e.g., LatinGenAIMorphosyntaxProcess) is injected into this
# module's namespace and behaves identically to the previously hand-written classes.

_generated_names = generate_language_processes(
    module_globals=globals(),
    base_class=GenAIMorphosyntaxProcess,
    factory_func=make_genai_morphosyntax_process,
    language_definitions=LANGUAGE_DEFINITIONS,
)

# Export base classes + all generated language-specific classes
__all__ = [
    "MorphosyntaxProcess",
    "GenAIMorphosyntaxProcess",
    *_generated_names,
]
