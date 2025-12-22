Contributing to CLTK
====================

Thank you for your interest in contributing to CLTK! This document outlines how
we organize the codebase, what we consider the public API, and our approach to
compatibility and deprecations.

Public vs. Internal API
-----------------------

Most users should interact with CLTK only through the top‑level NLP interface:

```
from cltk import NLP

nlp = NLP("lat")
doc = nlp.analyze("…")
word = doc.words[0]
```

Public API (compatibility guaranteed across minor releases):
- `cltk.NLP`
- `cltk.__version__`
- Data models returned by `NLP` (e.g., `Doc`, `Word`) are stable in behavior;
  we avoid breaking field names without a deprecation period.

Internal API (no stability guarantees):
- All subpackages such as `cltk.morphosyntax`, `cltk.dependency`, `cltk.genai`,
  and `cltk.languages` are considered internal implementation details, unless
  explicitly documented otherwise.
- Internal modules include an inline header comment: “Internal; no stability
  guarantees”. These modules may change at any time.

Versioning and Deprecations
---------------------------

We follow SemVer for the public API surface:
- Patch: bug fixes and internal changes.
- Minor: new functionality that is backwards‑compatible for the public API.
- Major: breaking changes to the public API.

Deprecations:
- Public changes include a deprecation period (documented in the changelog and
  release notes). Deprecations emit warnings when used.
- Internal modules may change without deprecation.

Public Manifest
---------------

The file `api/public_manifest.json` enumerates what we export publicly at the
top level. Tests verify that the `cltk` module exports exactly this surface.

Development Guidelines
----------------------

- Tests: add unit tests for new behavior and regression tests for bug fixes.
- Type hints: we use Python 3.11+ type hints with `mypy` for static checking.
- GenAI changes: follow `LLM_DEV_GUIDE.md` for prompts, model usage, safety, and testing requirements before modifying any LLM-backed code.
- Linting/formatting: `ruff` is used for lint and format; run pre‑commit hooks.
- Docs: keep docstrings updated; user‑facing changes should be documented.

Getting Started
---------------

1. Fork the repository and create a feature branch.
2. Install dev deps and pre‑commit hooks.
3. Run the test suite (`pytest`), lint (`ruff`), and type checks (`mypy`).
4. Open a pull request describing your change and how it was tested.

Thank you for helping improve CLTK!
