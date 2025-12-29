from __future__ import annotations

from pathlib import Path

import mkdocs_gen_files

LANGUAGES_PATH = Path("src/cltk/languages/languages.py")
USER_DEFINED_EXAMPLE_PATH = Path("scripts/example_user_defined_language.py")
DOCS_PATH = Path("docs/languages.md")

START_MARKER = "<!-- LANGUAGES:START -->"
END_MARKER = "<!-- LANGUAGES:END -->"
USER_START_MARKER = "<!-- USER_DEFINED_LANG:START -->"
USER_END_MARKER = "<!-- USER_DEFINED_LANG:END -->"


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


def _build_languages_insert(block: str) -> str:
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


def _build_user_example_insert(block: str) -> str:
    return "\n".join(
        [
            USER_START_MARKER,
            "<details>",
            "<summary>User-defined language example (generated from `scripts/example_user_defined_language.py`)</summary>",
            "",
            "```python",
            block,
            "```",
            "",
            "</details>",
            USER_END_MARKER,
        ]
    )


lang_text = LANGUAGES_PATH.read_text()
lang_block = _extract_languages_block(lang_text)
lang_insert = _build_languages_insert(lang_block)
user_block = USER_DEFINED_EXAMPLE_PATH.read_text().rstrip()
user_insert = _build_user_example_insert(user_block)

doc_text = DOCS_PATH.read_text()
if START_MARKER not in doc_text or END_MARKER not in doc_text:
    raise ValueError("Missing LANGUAGES markers in docs/languages.md.")
if USER_START_MARKER not in doc_text or USER_END_MARKER not in doc_text:
    raise ValueError("Missing user-defined language markers in docs/languages.md.")

before, rest = doc_text.split(START_MARKER, 1)
_, after = rest.split(END_MARKER, 1)
new_text = before + lang_insert + after

before, rest = new_text.split(USER_START_MARKER, 1)
_, after = rest.split(USER_END_MARKER, 1)
new_text = before + user_insert + after

with mkdocs_gen_files.open("languages.md", "w") as fd:
    fd.write(new_text)

mkdocs_gen_files.set_edit_path("languages.md", DOCS_PATH)
