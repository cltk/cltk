from __future__ import annotations

from pathlib import Path

import mkdocs_gen_files

LANGUAGES_PATH = Path("src/cltk/languages/languages.py")
DOCS_PATH = Path("docs/languages.md")

START_MARKER = "<!-- LANGUAGES:START -->"
END_MARKER = "<!-- LANGUAGES:END -->"


def _extract_languages_block(text: str) -> str:
    lines = text.splitlines()
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.startswith("LANGUAGES:"):
            start = i
            continue
        if start is not None and line.startswith("__all__"):
            end = i
            break
    if start is None or end is None:
        raise ValueError("Could not find LANGUAGES block boundaries.")
    return "\n".join(lines[start:end]).rstrip()


def _build_insert(block: str) -> str:
    return "\n".join(
        [
            START_MARKER,
            "<details>",
            "<summary>Current curated list (generated from `src/cltk/languages/languages.py`)</summary>",
            "",
            "```python",
            block,
            "```",
            "",
            "</details>",
            END_MARKER,
        ]
    )


lang_text = LANGUAGES_PATH.read_text()
block = _extract_languages_block(lang_text)
insert = _build_insert(block)

doc_text = DOCS_PATH.read_text()
if START_MARKER not in doc_text or END_MARKER not in doc_text:
    raise ValueError("Missing LANGUAGES markers in docs/languages.md.")

before, rest = doc_text.split(START_MARKER, 1)
_, after = rest.split(END_MARKER, 1)
new_text = before + insert + after

with mkdocs_gen_files.open("languages.md", "w") as fd:
    fd.write(new_text)

mkdocs_gen_files.set_edit_path("languages.md", DOCS_PATH)
