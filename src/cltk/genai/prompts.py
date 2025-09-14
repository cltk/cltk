"""Centralized prompt templates for GenAI calls.

# Internal; no stability guarantees

Each builder returns a PromptInfo with the prompt text, a semantic version, and
an opaque content hash to aid logging and reproducibility.
"""

import hashlib

from pydantic import BaseModel


class PromptInfo(BaseModel):
    """Structured metadata for a prompt template.

    Frozen/immutable to ensure prompts are treated as value objects and can be
    safely logged and hashed without mutation.
    """

    kind: str
    version: str
    text: str
    digest: str

    model_config = {"frozen": True}


def _hash_prompt(kind: str, version: str, text: str) -> str:
    h = hashlib.sha1()
    h.update(kind.encode("utf-8"))
    h.update(version.encode("utf-8"))
    h.update(text.encode("utf-8"))
    return h.hexdigest()[:12]


def morphosyntax_prompt(lang_or_dialect_name: str, normalized_text: str) -> PromptInfo:
    """Build the morphosyntax prompt.

    Rules emphasize strict UD tags, no commentary, and TSV in a code block.
    """
    kind: str = "morphosyntax"
    version: str = "1.0"
    text: str = (
        f"For the following {lang_or_dialect_name} text, tokenize the text and return one line per token. "
        "For each token, provide the FORM, LEMMA, UPOS, and FEATS fields following Universal Dependencies (UD) guidelines.\n\n"
        "Rules:\n"
        "- Always use strict UD morphological tags (not a simplified system).\n"
        "- Split off enclitics and contractions as separate tokens.\n"
        "- Always include punctuation as separate tokens with UPOS=PUNCT and FEATS=_.\n"
        "- For uncertain, rare, or dialectal forms, always provide the most standard dictionary lemma and supply a best‑effort UD tag. Do not skip any tokens.\n"
        '- Separate UD features with a pipe ("|"). Do not use a semi‑colon or other characters.\n'
        "- Preserve the spelling of the text exactly as given (including diacritics, breathings, and subscripts). Do not normalize.\n"
        "- If a lemma or feature is uncertain, still provide the closest standard form and UD features. Never leave fields blank and never ask for clarification.\n"
        "- If full accuracy is not possible, always provide a best‑effort output without asking for clarification.\n"
        "- Never request to perform the task in multiple stages; always deliver the final TSV in one step.\n"
        "- Do not ask for confirmation, do not explain your reasoning, and do not include any commentary. Output only the TSV table.\n"
        "- Always output all four fields: FORM, LEMMA, UPOS, FEATS.\n"
        "- The result must be a markdown code block containing only a tab‑delimited table (TSV) with the header row:\n\n"
        "FORM\tLEMMA\tUPOS\tFEATS\n\n"
        f"Text:\n\n{normalized_text}\n"
    )
    return PromptInfo(
        kind=kind, version=version, text=text, digest=_hash_prompt(kind, version, text)
    )


def dependency_prompt_from_tokens(token_table: str) -> PromptInfo:
    """Build a dependency prompt using an existing token table.

    The table must be TSV with header: INDEX, FORM, UPOS, FEATS.
    """
    kind: str = "dependency-tokens"
    version: str = "1.0"
    text: str = (
        "Using the following tokens with UPOS and FEATS, produce a dependency parse as TSV with exactly three columns: FORM, HEAD, DEPREL.\n\n"
        "Rules:\n"
        "- Use strict UD dependency relations only (e.g., nsubj, obj, obl:tmod, root).\n"
        "- Do not change, split, merge, or reorder tokens. Use the tokens as given.\n"
        "- HEAD refers to the 1-based index of the head token in the given token order (0 for root).\n"
        "- Output must be a Markdown code block containing only a tab‑delimited table with the header: FORM\tHEAD\tDEPREL.\n\n"
        f"Tokens:\n\n{token_table}\n\n"
        "Output only the dependency table."
    )
    return PromptInfo(
        kind=kind, version=version, text=text, digest=_hash_prompt(kind, version, text)
    )


def dependency_prompt_from_text(lang_or_dialect_name: str, sentence: str) -> PromptInfo:
    """Build a dependency prompt when no token table is available."""
    kind: str = "dependency-text"
    version: str = "1.0"
    text: str = (
        f"For the following {lang_or_dialect_name} text, first tokenize the sentence. "
        "For each token, output a TSV row with exactly three columns: FORM, HEAD, DEPREL.\n\n"
        "Rules:\n"
        "- Use strict UD dependency relations only (e.g., nsubj, obj, obl:tmod, root).\n"
        "- HEAD is 1‑based index of the token's head in this sentence (0 for root).\n"
        "- Output must be a Markdown code block with the header: FORM\tHEAD\tDEPREL.\n\n"
        f"Text:\n\n{sentence}\n"
    )
    return PromptInfo(
        kind=kind, version=version, text=text, digest=_hash_prompt(kind, version, text)
    )
