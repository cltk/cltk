from __future__ import annotations

import os
import re
from copy import copy
from typing import ClassVar

from cltk import NLP
from cltk.core.data_types import Doc, Language, Pipeline, Process
from cltk.dependency.processes import GenAIDependencyProcess
from cltk.enrichment.processes import GenAIEnrichmentProcess
from cltk.languages.languages import LANGUAGES
from cltk.morphosyntax.processes import GenAIMorphosyntaxProcess
from cltk.text.processes import MultilingualNormalizeProcess
from cltk.translation.processes import GenAITranslationProcess

CUSTOM_GLOTTOLOG_ID = "ocat1234"
_SENTENCE_END_RE = re.compile(r"[.!?]+")


class BasicSentenceSplitProcess(Process):
    """Lightweight sentence splitter for user-defined languages."""

    process_id: ClassVar[str] = "sentence_split.basic"

    def run(self, input_doc: Doc) -> Doc:
        output_doc = copy(input_doc)
        text = output_doc.normalized_text or output_doc.raw
        if not text:
            raise ValueError("Doc must have `raw` or `normalized_text` to split.")
        output_doc.sentence_boundaries = _split_basic(text)
        return output_doc


def _split_basic(text: str) -> list[tuple[int, int]]:
    boundaries: list[tuple[int, int]] = []
    start = 0
    for match in _SENTENCE_END_RE.finditer(text):
        end = match.end()
        while start < len(text) and text[start].isspace():
            start += 1
        if text[start:end].strip():
            boundaries.append((start, end))
        start = end
    if start < len(text):
        while start < len(text) and text[start].isspace():
            start += 1
        if start < len(text):
            boundaries.append((start, len(text)))
    return boundaries


def _register_language() -> Language:
    language = Language(name="Old Catalan")
    # NLP requires a glottolog_id for pipeline resolution; use a local code.
    language.glottolog_id = CUSTOM_GLOTTOLOG_ID
    LANGUAGES[CUSTOM_GLOTTOLOG_ID] = language
    return language


def _build_pipeline() -> Pipeline:
    return Pipeline(
        description="User-defined GenAI pipeline for Old Catalan.",
        glottolog_id=CUSTOM_GLOTTOLOG_ID,
        processes=[
            MultilingualNormalizeProcess,
            BasicSentenceSplitProcess,
            GenAIMorphosyntaxProcess,
            GenAIDependencyProcess,
            GenAIEnrichmentProcess,
            GenAITranslationProcess,
        ],
    )


TEXT = (
    "Et si Guilelm Arnal me facia tal cosa que dreçar no·m volgués ho no poqués, "
    "ho ssi·s partia de mi, che Mir Arnall me romasés aisí com lo·m avia al dia "
    "che ad él lo commanné."
)


def main() -> Doc:
    language = _register_language()
    pipeline = _build_pipeline()
    backend = os.getenv("CLTK_BACKEND", "openai")
    if backend not in {"openai", "mistral", "ollama", "ollama-cloud"}:
        raise ValueError(
            "CLTK_BACKEND must be one of: openai, mistral, ollama, ollama-cloud."
        )
    model = os.getenv("CLTK_MODEL")
    nlp = NLP(
        language_code=language.name,
        backend=backend,
        model=model,
        custom_pipeline=pipeline,
        suppress_banner=True,
    )
    return nlp.analyze(TEXT)


if __name__ == "__main__":
    doc = main()
    print(doc.translation or "(no translation returned)")
