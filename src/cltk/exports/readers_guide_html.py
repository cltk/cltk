"""Reader's guide HTML exporter."""

from typing import Optional

from cltk.core.data_types import Doc
from cltk.exports._helpers import (
    format_features,
    format_morph,
    get_gloss,
    get_ipa,
    get_lemma,
    get_token_text,
    get_upos_tag,
    html_escape,
    iter_sentences,
    iter_words,
    sentence_text,
)


def _sentence_translation(doc: Doc, sentence_index: int) -> Optional[str]:
    """Return the sentence translation text or fallback document translation."""
    translation_map = getattr(doc, "sentence_translations", None) or {}
    translation = translation_map.get(sentence_index)
    if translation is not None:
        return getattr(translation, "text", None)
    return getattr(doc, "translation", None)


def doc_to_readers_guide_html(
    doc: Doc,
    *,
    title: Optional[str] = None,
    include_ipa: bool = True,
    include_gloss: bool = True,
    include_morph: bool = True,
    include_dependencies: bool = True,
    include_translation: bool = True,
    max_sentences: Optional[int] = None,
) -> str:
    """Render a self-contained HTML reader's guide for a ``Doc``."""
    sentences = iter_sentences(doc, max_sentences)
    doc_title = (
        title
        or (getattr(doc, "metadata", None) or {}).get("title")
        or (getattr(doc, "metadata", None) or {}).get("reference")
        or "Reader's Guide"
    )

    toc_items: list[str] = []
    sentence_blocks: list[str] = []
    for sent_idx, sentence in enumerate(sentences, start=1):
        words = iter_words(sentence)
        if not words:
            continue
        anchor = f"sentence-{sent_idx}"
        toc_items.append(f'<li><a href="#{anchor}">Sentence {sent_idx}</a></li>')
        sentence_value = html_escape(sentence_text(doc, sentence, words))
        translation_html = ""
        if include_translation:
            translation = _sentence_translation(doc, sent_idx - 1)
            if translation:
                translation_html = f'<div class="sentence-translation">{html_escape(str(translation))}</div>'

        token_strip_parts: list[str] = []
        for word in words:
            token = html_escape(get_token_text(word))
            gloss = get_gloss(word) if include_gloss else ""
            ipa_value, ipa_mode = get_ipa(word) if include_ipa else (None, None)
            tooltip_parts: list[str] = []
            if gloss:
                tooltip_parts.append(f"Gloss: {gloss}")
            if ipa_value:
                ipa_text = f"IPA: {ipa_value}"
                if ipa_mode:
                    ipa_text += f" ({ipa_mode})"
                tooltip_parts.append(ipa_text)
            tooltip_text = html_escape(" • ".join(tooltip_parts))
            data_attr = f' data-tooltip="{tooltip_text}"' if tooltip_text else ""
            token_strip_parts.append(f'<span class="token"{data_attr}>{token}</span>')
        token_strip = " ".join(token_strip_parts)

        card_blocks: list[str] = []
        for tok_idx, word in enumerate(words, start=1):
            token = html_escape(get_token_text(word))
            lemma = get_lemma(word)
            pos = get_upos_tag(word)
            feats = format_features(word)
            gloss = get_gloss(word) if include_gloss else ""
            ipa_value, ipa_mode = get_ipa(word) if include_ipa else (None, None)
            morph = format_morph(word) if include_morph else ""
            dep = getattr(word, "dependency_relation", None)
            dep_code = getattr(dep, "code", None) or getattr(dep, "tag", None)
            dep_name = getattr(dep, "name", None)
            governor = getattr(word, "governor", None)

            rows: list[str] = []
            if lemma:
                rows.append(
                    "".join(
                        [
                            "<dt>Lemma</dt>",
                            f'<dd>{html_escape(str(lemma))} <button class="copy" data-copy="{html_escape(str(lemma))}">Copy</button></dd>',
                        ]
                    )
                )
            if pos:
                rows.append(f"<dt>POS</dt><dd>{html_escape(str(pos))}</dd>")
            if include_morph and morph:
                rows.append(f"<dt>Morphology</dt><dd>{html_escape(morph)}</dd>")
            if include_gloss and gloss:
                rows.append(
                    "".join(
                        [
                            "<dt>Gloss</dt>",
                            f'<dd>{html_escape(gloss)} <button class="copy" data-copy="{html_escape(gloss)}">Copy</button></dd>',
                        ]
                    )
                )
            if include_ipa and ipa_value:
                ipa_label = html_escape(ipa_value)
                if ipa_mode:
                    ipa_label += (
                        f' <span class="muted">({html_escape(ipa_mode)})</span>'
                    )
                rows.append(f"<dt>IPA</dt><dd>{ipa_label}</dd>")
            if feats:
                rows.append(f"<dt>Features</dt><dd>{html_escape(feats)}</dd>")
            if include_dependencies and (dep_code or governor is not None):
                dep_label = dep_code or ""
                if dep_name and dep_name != dep_code:
                    dep_label = (
                        f"{dep_name} ({dep_code})" if dep_code else str(dep_name)
                    )
                governor_label = ""
                if governor is not None:
                    try:
                        head_index = int(governor)
                    except (TypeError, ValueError):
                        head_index = None
                    if head_index is not None and 0 <= head_index < len(words):
                        head_word = get_token_text(words[head_index])
                        governor_label = f"token {head_index + 1} ({head_word})"
                    elif head_index is not None:
                        governor_label = f"token {head_index + 1}"
                dep_details = " · ".join(
                    part for part in [dep_label, governor_label] if part
                )
                if dep_details:
                    rows.append(
                        f"<dt>Dependencies</dt><dd>{html_escape(dep_details)}</dd>"
                    )

            rows_html = "".join(rows) if rows else "<p>No details available.</p>"
            card_blocks.append(
                "\n".join(
                    [
                        '<details class="token-card">',
                        f"<summary>{token}</summary>",
                        f"<dl>{rows_html}</dl>",
                        "</details>",
                    ]
                )
            )

        sentence_blocks.append(
            "\n".join(
                [
                    f'<section id="{anchor}" class="sentence">',
                    f"<h2>Sentence {sent_idx}</h2>",
                    f'<div class="sentence-text">{sentence_value}</div>',
                    translation_html,
                    f'<div class="token-strip">{token_strip}</div>',
                    '<div class="token-cards">',
                    "\n".join(card_blocks),
                    "</div>",
                    "</section>",
                ]
            )
        )

    toc_html = ""
    if len(toc_items) > 1:
        toc_html = (
            '<nav class="toc"><h2>Contents</h2><ol>'
            + "".join(toc_items)
            + "</ol></nav>"
        )

    body = "\n".join(sentence_blocks)
    return (
        "\n".join(
            [
                "<!doctype html>",
                '<html lang="en">',
                "<head>",
                '<meta charset="utf-8" />',
                f"<title>{html_escape(str(doc_title))}</title>",
                "<style>",
                "body{font-family:Georgia,serif;line-height:1.6;margin:2rem;color:#1f1f1f;}",
                "h1,h2{font-family:'Palatino Linotype',serif;}",
                ".toc{background:#f5f5f5;padding:1rem;border-radius:8px;margin-bottom:1.5rem;}",
                ".sentence{margin:2rem 0;padding-bottom:1.5rem;border-bottom:1px solid #ddd;}",
                ".sentence-text{font-weight:600;margin-bottom:0.25rem;}",
                ".sentence-translation{font-style:italic;margin-bottom:0.75rem;color:#444;}",
                ".token-strip{display:flex;flex-wrap:wrap;gap:0.5rem;margin:0.75rem 0;}",
                ".token{position:relative;padding:0.2rem 0.4rem;border-radius:4px;background:#eef2ff;}",
                ".token[data-tooltip]:hover::after{content:attr(data-tooltip);position:absolute;left:0;top:100%;background:#111;color:#fff;padding:0.4rem;border-radius:4px;white-space:nowrap;font-size:0.8rem;z-index:5;}",
                ".token-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:0.75rem;}",
                ".token-card{background:#fafafa;border:1px solid #e2e2e2;border-radius:8px;padding:0.5rem;}",
                ".token-card summary{cursor:pointer;font-weight:600;margin-bottom:0.4rem;}",
                ".token-card dl{margin:0;}",
                ".token-card dt{font-weight:600;margin-top:0.3rem;}",
                ".token-card dd{margin:0 0 0.3rem 0.5rem;}",
                ".copy{margin-left:0.4rem;font-size:0.75rem;}",
                ".muted{color:#666;font-size:0.85rem;}",
                "</style>",
                "</head>",
                "<body>",
                f"<h1>{html_escape(str(doc_title))}</h1>",
                toc_html,
                body,
                "<script>",
                "document.addEventListener('click', (event) => {",
                "  const target = event.target;",
                "  if (target && target.classList.contains('copy')) {",
                "    const text = target.getAttribute('data-copy') || '';",
                "    if (navigator.clipboard) {",
                "      navigator.clipboard.writeText(text);",
                "    } else {",
                "      const temp = document.createElement('textarea');",
                "      temp.value = text;",
                "      document.body.appendChild(temp);",
                "      temp.select();",
                "      document.execCommand('copy');",
                "      document.body.removeChild(temp);",
                "    }",
                "  }",
                "});",
                "</script>",
                "</body>",
                "</html>",
            ]
        ).strip()
        + "\n"
    )
