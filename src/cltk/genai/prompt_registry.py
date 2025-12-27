"""Prompt profile registry for GenAI processes."""

from __future__ import annotations

import hashlib
import json
from typing import Any, ClassVar

from pydantic import BaseModel, Field

from cltk.genai.prompts import PromptInfo


class PromptTemplate(BaseModel):
    """Immutable prompt template with versioned metadata."""

    profile: str
    process_id: str
    version: str
    text: str | dict[str, str]
    digest: str
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


def _canonicalize_text(text: str | dict[str, str]) -> str:
    """Return a stable string representation for hashing."""
    if isinstance(text, str):
        return text
    return json.dumps(text, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256_hex(text: str) -> str:
    """Return a SHA256 hex digest for the provided text."""
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def build_prompt_info(
    template: PromptTemplate, *, variant: str | None = None, **kwargs: Any
) -> PromptInfo:
    """Render a PromptTemplate into a PromptInfo payload."""
    text = template.text
    if isinstance(text, dict):
        if not variant:
            raise ValueError(
                f"Template for {template.process_id} requires variant selection."
            )
        if variant not in text:
            available = ", ".join(sorted(text))
            raise KeyError(
                f"Unknown variant '{variant}' for {template.process_id}. Available: {available}"
            )
        text = text[variant]
    rendered = str(text).format(**kwargs)
    kind = f"{template.process_id}:{variant}" if variant else template.process_id
    return PromptInfo(
        kind=kind,
        version=template.version,
        text=rendered,
        digest=template.digest,
    )


class PromptProfileRegistry:
    """Registry of prompt bundles by profile and version."""

    _templates: ClassVar[dict[str, dict[str, dict[str, PromptTemplate]]]] = {}
    _defaults: ClassVar[dict[str, str]] = {}

    @classmethod
    def register_bundle(
        cls,
        profile: str,
        version: str,
        templates: dict[str, str | dict[str, str]],
        *,
        metadata: dict[str, Any] | None = None,
        set_default: bool = False,
    ) -> None:
        """Register a prompt bundle for a profile/version pair."""
        for process_id, text in templates.items():
            canonical = _canonicalize_text(text)
            digest = _sha256_hex(canonical)
            tpl = PromptTemplate(
                profile=profile,
                process_id=process_id,
                version=version,
                text=text,
                digest=digest,
                metadata=metadata or {},
            )
            cls._templates.setdefault(profile, {}).setdefault(version, {})[
                process_id
            ] = tpl
        if set_default or profile not in cls._defaults:
            cls._defaults[profile] = version

    @classmethod
    def get_prompt(
        cls, profile: str, process_id: str, version: str | None = None
    ) -> PromptTemplate:
        """Return the prompt template for a profile/process/version."""
        if profile not in cls._templates:
            available = ", ".join(sorted(cls._templates))
            raise KeyError(
                f"Unknown prompt profile '{profile}'. Available: {available}"
            )
        ver = version or cls._defaults.get(profile)
        if not ver:
            raise KeyError(f"No default version for profile '{profile}'.")
        if ver not in cls._templates[profile]:
            available = ", ".join(sorted(cls._templates[profile]))
            raise KeyError(
                f"Unknown version '{ver}' for profile '{profile}'. Available: {available}"
            )
        template = cls._templates[profile][ver].get(process_id)
        if not template:
            available = ", ".join(sorted(cls._templates[profile][ver]))
            raise KeyError(
                f"No template for process_id '{process_id}' in profile '{profile}' version '{ver}'. Available: {available}"
            )
        return template

    @classmethod
    def list_profiles(cls) -> list[str]:
        """Return available prompt profile names."""
        return sorted(cls._templates)

    @classmethod
    def list_versions(cls, profile: str) -> list[str]:
        """Return available versions for a profile."""
        return sorted(cls._templates.get(profile, {}))


_MORPH_TEMPLATE = (
    "For the following {lang_or_dialect_name} text, tokenize the text and return one line per token. "
    "For each token, provide the FORM, LEMMA, UPOS, and FEATS fields following Universal Dependencies (UD) guidelines.\n\n"
    "Rules:\n"
    "- Always use strict UD morphological tags.\n"
    "- Split off enclitics and contractions as separate tokens.\n"
    "- Always include punctuation as separate tokens with UPOS=PUNCT and FEATS=_.\n"
    "- Preserve the spelling of the text exactly as given. Do not normalize.\n"
    "- Always output all fields: FORM, LEMMA, UPOS, FEATS, LEMMA_CONF, UPOS_CONF, FEATS_CONF.\n"
    "- Confidence fields must be floats in [0,1] or '_' if unknown.\n"
    "- Output must be a markdown code block containing only a tab-delimited table with the header row:\n\n"
    "FORM\tLEMMA\tUPOS\tFEATS\tLEMMA_CONF\tUPOS_CONF\tFEATS_CONF\n\n"
    "Text:\n\n{text}\n"
)

_MORPH_EPIGRAPHY = (
    _MORPH_TEMPLATE
    + "\nEpigraphy note: preserve abbreviations and damaged forms as written; do not expand.\n"
)

_DEP_TOKENS_TEMPLATE = (
    "Using the following tokens with UPOS and FEATS, produce a dependency parse as TSV with exactly three columns: FORM, HEAD, DEPREL.\n\n"
    "Rules:\n"
    "- Use strict UD dependency relations only.\n"
    "- Do not change, split, merge, or reorder tokens. Use the tokens as given.\n"
    "- HEAD refers to the 1-based index of the head token in the given token order (0 for root).\n"
    "- Include HEAD_CONF and DEPREL_CONF as floats in [0,1] or '_' if unknown.\n"
    "- Output must be a markdown code block containing only a tab-delimited table with the header: FORM\tHEAD\tDEPREL\tHEAD_CONF\tDEPREL_CONF.\n\n"
    "Tokens:\n\n{token_table}\n\n"
    "Output only the dependency table."
)

_DEP_TEXT_TEMPLATE = (
    "For the following {lang_or_dialect_name} text, tokenize the sentence and output a TSV table with FORM, HEAD, DEPREL.\n\n"
    "Rules:\n"
    "- Use strict UD dependency relations only.\n"
    "- HEAD is 1-based index of the token's head in this sentence (0 for root).\n"
    "- Include HEAD_CONF and DEPREL_CONF as floats in [0,1] or '_' if unknown.\n"
    "- Output must be a markdown code block with the header: FORM\tHEAD\tDEPREL\tHEAD_CONF\tDEPREL_CONF.\n\n"
    "Text:\n\n{sentence}\n"
)

_DEP_TOKENS_EPIGRAPHY = (
    _DEP_TOKENS_TEMPLATE
    + "\nEpigraphy note: preserve abbreviations and damaged forms as written; do not expand.\n"
)

_DEP_TEXT_EPIGRAPHY = (
    _DEP_TEXT_TEMPLATE
    + "\nEpigraphy note: preserve abbreviations and damaged forms as written; do not expand.\n"
)

_ENRICHMENT_TEMPLATE = (
    "Using the following {lang_or_dialect_name} tokens (with lemma, UPOS, FEATS, HEAD, DEPREL), add enrichment fields without changing the tokens.\n\n"
    "Return a single JSON object inside a markdown code block with keys `tokens` and `idioms`.\n"
    "- Each entry in `tokens` must include: index (1-based, matching the table), gloss, lemma_translations, ipa (use pronunciation mode {ipa_mode}), orthography, idiom_span_ids, and pedagogy.\n"
    "- Do not re-tokenize or change morphological or dependency decisions.\n\n"
    "Tokens:\n\n{token_table}\n\n"
    "Output only the JSON payload."
)

_TRANSLATION_TEMPLATE = (
    "Translate the following {lang_or_dialect_name} sentence into {target_language}. "
    "Use the provided morphosyntax, dependency relations, glosses, lemma translations, idiom hints, and pedagogy notes instead of translating from scratch.\n\n"
    "Return a JSON object inside a markdown code block with:\n"
    "- `translation`: the final fluent translation.\n"
    "- `notes`: 1-3 sentences highlighting non-obvious decisions.\n"
    "- `confidence`: float in [0,1] for overall translation confidence (or null if unknown).\n\n"
    "Context:\n\n{context}\n"
)

_TRANSLATION_STUDENT = (
    _TRANSLATION_TEMPLATE + "\nUse clear, student-friendly language and short notes.\n"
)

_TRANSLATION_EPIGRAPHY = (
    _TRANSLATION_TEMPLATE
    + "\nPrefer a conservative, literal translation and note uncertain restorations.\n"
)


PromptProfileRegistry.register_bundle(
    "latin_ud_strict",
    "1.0",
    {
        "morphosyntax.genai": _MORPH_TEMPLATE,
        "dependency.genai": {
            "tokens": _DEP_TOKENS_TEMPLATE,
            "text": _DEP_TEXT_TEMPLATE,
        },
        "enrichment.genai": _ENRICHMENT_TEMPLATE,
        "translation.genai": _TRANSLATION_TEMPLATE,
    },
    set_default=True,
)

PromptProfileRegistry.register_bundle(
    "student_friendly",
    "1.0",
    {
        "morphosyntax.genai": _MORPH_TEMPLATE,
        "dependency.genai": {
            "tokens": _DEP_TOKENS_TEMPLATE,
            "text": _DEP_TEXT_TEMPLATE,
        },
        "enrichment.genai": _ENRICHMENT_TEMPLATE,
        "translation.genai": _TRANSLATION_STUDENT,
    },
    set_default=True,
)

PromptProfileRegistry.register_bundle(
    "epigraphy_conservative",
    "1.0",
    {
        "morphosyntax.genai": _MORPH_EPIGRAPHY,
        "dependency.genai": {
            "tokens": _DEP_TOKENS_EPIGRAPHY,
            "text": _DEP_TEXT_EPIGRAPHY,
        },
        "enrichment.genai": _ENRICHMENT_TEMPLATE,
        "translation.genai": _TRANSLATION_EPIGRAPHY,
    },
    set_default=True,
)
