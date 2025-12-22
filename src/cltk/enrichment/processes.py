"""Process for GenAI-driven enrichment (glosses, IPA, idioms, pedagogy)."""

from collections.abc import Callable
from copy import copy
from functools import cached_property
from typing import Optional

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import IPA_PRONUNCIATION_MODE, Doc, Process
from cltk.core.logging_utils import bind_from_doc
from cltk.enrichment.utils import generate_gpt_enrichment_concurrent
from cltk.genai.prompts import PromptInfo

# Prompt override type: callable, PromptInfo, or literal string.
# Callable receives (lang_or_dialect_name, token_table, ipa_mode)
EnrichmentPromptBuilder = (
    Callable[[str, str, IPA_PRONUNCIATION_MODE], PromptInfo] | PromptInfo | str
)


class GenAIEnrichmentProcess(Process):
    """Language-agnostic enrichment process using a generative GPT model."""

    prompt_builder: Optional[EnrichmentPromptBuilder] = None
    ipa_mode: IPA_PRONUNCIATION_MODE = "attic_5c_bce"

    @cached_property
    def algorithm(self) -> Callable[..., Doc]:
        if not self.glottolog_id:
            msg = "glottolog_id must be set for EnrichmentProcess"
            bind_context(glottolog_id=self.glottolog_id).error(msg)
            raise ValueError(msg)
        return generate_gpt_enrichment_concurrent

    def run(self, input_doc: Doc) -> Doc:
        output_doc: Doc = copy(input_doc)
        if not output_doc.normalized_text:
            msg = "Doc must have `normalized_text`."
            bind_from_doc(output_doc).error(msg)
            raise ValueError(msg)
        if self.glottolog_id is None:
            raise ValueError("glottolog_id must be set for enrichment.")
        output_doc = self.algorithm(
            output_doc,
            ipa_mode=self.ipa_mode,
            prompt_builder=self.prompt_builder,
        )
        return output_doc
