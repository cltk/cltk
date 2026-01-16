"""Processes for dependency parsing."""

from collections.abc import Callable
from copy import copy
from functools import cached_property
from typing import ClassVar, Optional

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import Doc, Process
from cltk.core.logging_utils import bind_from_doc
from cltk.core.process_factory import (
    generate_language_processes,
    make_genai_dependency_process,
)
from cltk.core.process_registry import register_process
from cltk.dependency.utils import generate_gpt_dependency_concurrent
from cltk.genai.prompt_registry import (
    PromptProfileRegistry,
    PromptTemplate,
    build_prompt_info,
)
from cltk.genai.prompts import PromptInfo
from cltk.languages.definitions import LANGUAGE_DEFINITIONS

# Prompt overrides can be callables, PromptInfo, or literal strings.
PromptBuilder = Callable[[str, str], PromptInfo] | PromptInfo | str


class DependencyProcess(Process):
    """Base class for dependency parsing processes."""


@register_process
class GenAIDependencyProcess(DependencyProcess):
    """Language-specific dependency process using a generative GPT model."""

    process_id: ClassVar[str] = "dependency.genai"
    # Optional prompt builders for custom pipelines
    prompt_builder_from_tokens: Optional[PromptBuilder] = None
    prompt_builder_from_text: Optional[PromptBuilder] = None
    prompt_profile: Optional[str] = None
    prompt_version: Optional[str] = None

    @cached_property
    def algorithm(self) -> Callable[..., Doc]:
        """Return the dependency generation function for this process."""
        if not self.glottolog_id:
            msg: str = "glottolog_id must be set for DependencyProcess"
            bind_context(glottolog_id=self.glottolog_id).error(msg)
            raise ValueError(msg)
        # Prefer the safe concurrent wrapper (async under the hood, sync surface)
        return generate_gpt_dependency_concurrent

    def run(self, input_doc: Doc) -> Doc:
        """Run the configured GPT dependency parsing workflow."""
        output_doc = copy(input_doc)
        if not output_doc.normalized_text:
            msg: str = "Doc must have `normalized_text`."
            bind_from_doc(output_doc).error(msg)
            raise ValueError(msg)
        # Ensure required attributes are present
        if self.glottolog_id is None:
            raise ValueError("glottolog_id must be set for sentence splitting")
        prompt_builder_from_tokens = self.prompt_builder_from_tokens
        prompt_builder_from_text = self.prompt_builder_from_text
        prompt_digest = None
        if self.prompt_profile and (
            prompt_builder_from_tokens is None or prompt_builder_from_text is None
        ):
            template = PromptProfileRegistry.get_prompt(
                self.prompt_profile, self.process_id, self.prompt_version
            )
            prompt_digest = template.digest
            if prompt_builder_from_tokens is None:

                def _builder_tokens(
                    lang: str, table: str, _template: PromptTemplate = template
                ) -> PromptInfo:
                    """Build a dependency prompt from tokens via a profile template."""
                    return build_prompt_info(
                        _template,
                        variant="tokens",
                        lang_or_dialect_name=lang,
                        token_table=table,
                        text=table,
                        sentence=table,
                    )

                prompt_builder_from_tokens = _builder_tokens
            if prompt_builder_from_text is None:

                def _builder_text(
                    lang: str, sentence: str, _template: PromptTemplate = template
                ) -> PromptInfo:
                    """Build a dependency prompt from text via a profile template."""
                    return build_prompt_info(
                        _template,
                        variant="text",
                        lang_or_dialect_name=lang,
                        sentence=sentence,
                        text=sentence,
                        token_table=sentence,
                    )

                prompt_builder_from_text = _builder_text
        # Callable typing does not retain keyword names; pass positionally
        output_doc = self.algorithm(
            output_doc,
            prompt_builder_from_tokens=prompt_builder_from_tokens,
            prompt_builder_from_text=prompt_builder_from_text,
            prompt_profile=self.prompt_profile,
            prompt_digest=prompt_digest,
            provenance_process=f"{self.process_id}:{self.__class__.__name__}",
        )
        return output_doc


# -----------------------------------------------------------------------------
# Generate all language-specific process classes dynamically
# -----------------------------------------------------------------------------
# This replaces 107 nearly-identical class definitions with a single factory call.
# Each generated class (e.g., LatinGenAIDependencyProcess) is injected into this
# module's namespace and behaves identically to the previously hand-written classes.

_generated_names = generate_language_processes(
    module_globals=globals(),
    base_class=GenAIDependencyProcess,
    factory_func=make_genai_dependency_process,
    language_definitions=LANGUAGE_DEFINITIONS,
)

# Export base classes + all generated language-specific classes
__all__ = [
    "DependencyProcess",
    "GenAIDependencyProcess",
    *_generated_names,
]
