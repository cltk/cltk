"""Shared helpers for scholar-facing export formats."""

import html
import re
from typing import Iterable, Optional

from cltk.core.data_types import Doc, Sentence, Word

_XML_ID_SAFE = re.compile(r"[^A-Za-z0-9_.:-]")


def iter_sentences(doc: Doc, max_sentences: Optional[int] = None) -> list[Sentence]:
    """Return sentence list with stable ordering and optional slicing."""
    sentences = list(getattr(doc, "sentences", []) or [])
    if not sentences and getattr(doc, "words", None):
        sentences = [Sentence(words=list(doc.words or []), index=0)]
    if max_sentences is not None:
        if max_sentences <= 0:
            raise ValueError("max_sentences must be positive when provided.")
        sentences = sentences[:max_sentences]
    return sentences


def iter_words(sentence: Sentence) -> list[Word]:
    """Return sentence words in stable order."""
    words = list(getattr(sentence, "words", []) or [])
    if not words:
        return []
    if any(getattr(word, "index_token", None) is not None for word in words):
        return sorted(
            words,
            key=lambda word: word.index_token
            if isinstance(getattr(word, "index_token", None), int)
            else 0,
        )
    return words


def get_token_text(word: Word) -> str:
    """Return the surface token string for a word."""
    return str(getattr(word, "string", "") or "")


def get_lemma(word: Word) -> str:
    """Return lemma string when available."""
    return str(getattr(word, "lemma", "") or "")


def get_upos_tag(word: Word) -> str:
    """Return UPOS tag or name in a stable string form."""
    upos = getattr(word, "upos", None)
    if not upos:
        return ""
    tag = getattr(upos, "tag", None)
    if tag:
        return str(tag)
    name = getattr(upos, "name", None)
    return str(name) if name else ""


def get_feature_map(word: Word) -> dict[str, str]:
    """Return a flat feature map from UD features."""
    feats = getattr(word, "features", None)
    feature_list = getattr(feats, "features", None)
    if not feature_list:
        return {}
    output: dict[str, str] = {}
    for feat in feature_list:
        key = getattr(feat, "key", None)
        value = getattr(feat, "value", None)
        if key and value:
            output[str(key)] = str(value)
    return output


def format_features(word: Word) -> str:
    """Serialize UD features into a sorted Key=Val string."""
    items = [f"{key}={val}" for key, val in sorted(get_feature_map(word).items())]
    return "|".join(items)


def format_morph(word: Word) -> str:
    """Return a compact UD-like morph string (UPOS + FEATS)."""
    upos = get_upos_tag(word)
    feats = format_features(word)
    if upos and feats:
        return f"{upos} {feats}"
    if upos:
        return upos
    return feats


def _gloss_from_gloss_field(gloss: object) -> Optional[str]:
    """Extract a gloss string from a Gloss-like object."""
    context = getattr(gloss, "context", None)
    if context:
        return str(context)
    dictionary = getattr(gloss, "dictionary", None)
    if dictionary:
        return str(dictionary)
    alternatives = getattr(gloss, "alternatives", None) or []
    if alternatives:
        alt_text = getattr(alternatives[0], "text", None)
        if alt_text:
            return str(alt_text)
    return None


def get_gloss(word: Word) -> str:
    """Return gloss text using prioritized enrichment fallbacks."""
    enrichment = getattr(word, "enrichment", None)
    if enrichment:
        gloss = getattr(enrichment, "gloss", None)
        if gloss:
            text = _gloss_from_gloss_field(gloss)
            if text:
                return text
        lemma_translations = getattr(enrichment, "lemma_translations", None) or []
        if lemma_translations:
            candidate = getattr(lemma_translations[0], "text", None)
            if candidate:
                return str(candidate)
    lemma = get_lemma(word)
    if lemma:
        return lemma
    return get_token_text(word)


def get_ipa(word: Word) -> tuple[Optional[str], Optional[str]]:
    """Return IPA value and mode when available."""
    enrichment = getattr(word, "enrichment", None)
    if not enrichment:
        return None, None
    ipa = getattr(enrichment, "ipa", None)
    if not ipa:
        return None, None
    value = getattr(ipa, "value", None)
    mode = getattr(ipa, "mode", None)
    return (str(value) if value else None, str(mode) if mode else None)


def sentence_text(doc: Doc, sentence: Sentence, words: Iterable[Word]) -> str:
    """Return sentence surface text with safe fallbacks."""
    idx = getattr(sentence, "index", None)
    if idx is not None:
        sentence_strings = getattr(doc, "sentence_strings", None)
        if sentence_strings and 0 <= idx < len(sentence_strings):
            return str(sentence_strings[idx])
    tokens = [get_token_text(word) for word in words]
    return " ".join(token for token in tokens if token)


def make_sentence_id(sentence_number: int) -> str:
    """Return a stable sentence ID (1-based)."""
    return f"s{sentence_number}"


def make_token_id(sentence_number: int, token_number: int) -> str:
    """Return a stable token ID (1-based)."""
    return f"s{sentence_number}w{token_number}"


def make_root_id(sentence_number: int) -> str:
    """Return a stable sentence root ID."""
    return f"s{sentence_number}root"


def safe_xml_id(value: str) -> str:
    """Normalize a string into a valid XML ID fragment."""
    cleaned = _XML_ID_SAFE.sub("-", value.strip())
    return cleaned.strip("-") or "cltk-doc"


def html_escape(text: str) -> str:
    """Escape text for HTML output."""
    return html.escape(text, quote=True)


def latex_escape(text: str) -> str:
    """Escape LaTeX special characters in a string."""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)
