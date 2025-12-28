from __future__ import annotations

from pathlib import Path

import mkdocs_gen_files

PIPELINES_PATH = Path("src/cltk/languages/pipelines.py")
DOCS_PATH = Path("docs/pipelines.md")

STANZA_START = "<!-- PIPELINES:STANZA:START -->"
STANZA_END = "<!-- PIPELINES:STANZA:END -->"
GENAI_START = "<!-- PIPELINES:GENAI:START -->"
GENAI_END = "<!-- PIPELINES:GENAI:END -->"


def _extract_block(text: str, start_prefix: str, end_prefixes: tuple[str, ...]) -> str:
    lines = text.splitlines()
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.startswith(start_prefix):
            start = i
            continue
        if start is not None and line.startswith(end_prefixes):
            end = i
            break
    if start is None:
        raise ValueError(f"Could not find block start: {start_prefix}")
    if end is None:
        end = len(lines)
    return "\n".join(lines[start:end]).rstrip()


def _build_insert(start_marker: str, end_marker: str, summary: str, block: str) -> str:
    return "\n".join(
        [
            start_marker,
            "<details>",
            f"<summary>{summary}</summary>",
            "",
            "```python",
            block,
            "```",
            "",
            "</details>",
            end_marker,
        ]
    )


pipelines_text = PIPELINES_PATH.read_text()

stanza_block = _extract_block(
    pipelines_text,
    "MAP_LANGUAGE_CODE_TO_STANZA_PIPELINE:",
    ("MAP_LANGUAGE_CODE_TO_SPACY_PIPELINE:",),
)
genai_block = _extract_block(
    pipelines_text,
    "MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE:",
    (),
)

stanza_insert = _build_insert(
    STANZA_START,
    STANZA_END,
    "Current Stanza pipeline map (generated from `src/cltk/languages/pipelines.py`)",
    stanza_block,
)
genai_insert = _build_insert(
    GENAI_START,
    GENAI_END,
    "Current generative pipeline map (generated from `src/cltk/languages/pipelines.py`)",
    genai_block,
)

doc_text = DOCS_PATH.read_text()
if STANZA_START not in doc_text or STANZA_END not in doc_text:
    raise ValueError("Missing Stanza pipeline markers in docs/pipelines.md.")
if GENAI_START not in doc_text or GENAI_END not in doc_text:
    raise ValueError("Missing Generative pipeline markers in docs/pipelines.md.")

before_stanza, stanza_rest = doc_text.split(STANZA_START, 1)
_, stanza_tail = stanza_rest.split(STANZA_END, 1)
stanza_updated = before_stanza + stanza_insert + stanza_tail

before_genai, genai_rest = stanza_updated.split(GENAI_START, 1)
_, genai_tail = genai_rest.split(GENAI_END, 1)
new_text = before_genai + genai_insert + genai_tail

with mkdocs_gen_files.open("pipelines.md", "w") as fd:
    fd.write(new_text)

mkdocs_gen_files.set_edit_path("pipelines.md", DOCS_PATH)
