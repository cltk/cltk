# User-Defined Pipelines

> Warning: This is an alpha feature. APIs and behaviors may change; use in production with care.

This page describes the declarative pipeline system for CLTK.

## Process IDs

Each process has a stable `process_id` used in configs and presets. Examples:

- `normalize`
- `sentence_split`
- `morphosyntax.genai`
- `dependency.genai`
- `translation.genai`
- `enrichment.genai` (legacy)
- `enrichment.lexicon`, `enrichment.phonology`, `enrichment.idioms`, `enrichment.pedagogy`

You can discover registered processes in code via `ProcessRegistry.list_processes()`.

## Example

Below is a minimal, working example that registers a Greek-only process to scan
iambic trimeter and wires it into a TOML pipeline. The scanner is intentionally
naive (syllable counts + basic long-vowel/diphthong heuristics), but it shows
how to add a custom process without changing CLTK code.

`scripts/pipeline_greek_iambic.toml`:

```toml
language = "anci1242"
steps = ["prosody.iambic_trimeter"]

[step.prosody.iambic_trimeter]
enabled = true
output_key = "scansion"
```

`scripts/scan_iambic_trimeter.py`:

```python
import re
import unicodedata
from typing import ClassVar

from cltk import NLP
from cltk.core.data_types import Doc, Pipeline, Process
from cltk.core.process_registry import register_process

_IAMBIC_TEMPLATE = ["x", "-", "u", "-", "x", "-", "u", "-", "x", "-", "u", "-"]
_VOWEL_RE = re.compile(r"[αεηιουω]+")
_DIPHTHONGS = ("αι", "ει", "οι", "υι", "αυ", "ευ", "ου", "ηυ", "ωυ")
_GREEK_GLOTTOLOG_IDS = {"anci1242"}


def _strip_diacritics(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _normalize_greek(text: str) -> str:
    text = _strip_diacritics(text).lower()
    text = re.sub(r"[0-9]", "", text)
    return re.sub(r"[^\w\s]", "", text)


def _scan_line(line: str) -> str:
    cleaned = _normalize_greek(line)
    syllables = _VOWEL_RE.findall(cleaned)
    quantities: list[str] = []
    for syl in syllables:
        long_by_vowel = "η" in syl or "ω" in syl
        long_by_diphthong = any(diph in syl for diph in _DIPHTHONGS)
        quantities.append("-" if long_by_vowel or long_by_diphthong else "u")
    quantities = quantities[: len(_IAMBIC_TEMPLATE)]
    pattern = [
        quantities[i] if i < len(quantities) else _IAMBIC_TEMPLATE[i]
        for i in range(len(_IAMBIC_TEMPLATE))
    ]
    return " ".join(pattern)


@register_process
class GreekIambicTrimeterProcess(Process):
    process_id: ClassVar[str] = "prosody.iambic_trimeter"
    glottolog_id: str | None = None
    output_key: str = "scansion"

    def run(self, input_doc: Doc) -> Doc:
        lang = input_doc.language
        iso = getattr(lang, "iso", None) or getattr(lang, "iso_set", {}).get("639-3")
        if lang.glottolog_id not in _GREEK_GLOTTOLOG_IDS and iso != "grc":
            raise ValueError("Iambic trimeter scanner is Ancient Greek only.")
        lines = [line.strip() for line in (input_doc.raw or "").splitlines() if line]
        scans = [_scan_line(line) for line in lines]
        input_doc.metadata.setdefault(self.output_key, scans)
        return input_doc


TEXT = """Εἴθ᾽ ὤφελ᾽ Ἀργοῦς μὴ διαπτάσθαι σκάφος
Κόλχων ἐς αἶαν κυανέας Συμπληγάδας,
μηδ᾽ ἐν νάπαισι Πηλίου πεσεῖν ποτε
τμηθεῖσα πεύκη, μηδ᾽ ἐρετμῶσαι χέρας
5ἀνδρῶν ἀριστέων οἳ τὸ πάγχρυσον δέρος
Πελίᾳ μετῆλθον."""

pipeline = Pipeline.from_toml("scripts/pipeline_greek_iambic.toml")
nlp = NLP(language_code="anci1242", custom_pipeline=pipeline)
doc = nlp.analyze(TEXT)

for line, scan in zip(TEXT.splitlines(), doc.metadata["scansion"]):
    print(line)
    print(scan)
```

Calling `python scripts/scan_iambic_trimeter.py` returns:

```text
% python scripts/scan_iambic_trimeter.py
𐤀 CLTK version '2.3.10'. When using the CLTK in research, please cite: https://aclanthology.org/2021.acl-demo.3/
Selected language "Ionic-Attic Ancient Greek" ("anci1242") without dialect.
Pipeline for `NLP("anci1242", backend="stanza")`: ['GreekIambicTrimeterProcess']
⸖ Process name: GreekIambicTrimeterProcess
Εἴθ᾽ ὤφελ᾽ Ἀργοῦς μὴ διαπτάσθαι σκάφος
- - u u - - u u - u u -
Κόλχων ἐς αἶαν κυανέας Συμπληγάδας,
u - u - u u u - u u u -
μηδ᾽ ἐν νάπαισι Πηλίου πεσεῖν ποτε
- u u - u - - u - u u -
τμηθεῖσα πεύκη, μηδ᾽ ἐρετμῶσαι χέρας
- - u - - - u u - - u u
5ἀνδρῶν ἀριστέων οἳ τὸ πάγχρυσον δέρος
u - u u - - u u u u u u
Πελίᾳ μετῆλθον.
u u u - u - u - x - u -
```

See these examples in <https://github.com/cltk/cltk/tree/master/examples> of the CLTK's repo.

## Process Registry

`ProcessRegistry` is importable from `cltk.core.process_registry` and lets you
list, fetch, and register pipeline processes at runtime.

```python
from cltk.core.data_types import Classification, Doc, Language, Process
from cltk.core.process_registry import ProcessRegistry, register_process

language = Language(
    name="Latin",
    glottolog_id="lati1261",
    level="language",
    classification=Classification(level="language"),
)
doc = Doc(language=language, raw="Gallia est omnis divisa in partes tres.")

# Discover and run a built-in process.
processes = ProcessRegistry.list_processes()
normalize_cls = ProcessRegistry.get_process("normalize")
normalized_doc = normalize_cls().run(doc)

# Register a custom process and fetch it by ID.
@register_process
class CustomEchoProcess(Process):
    process_id = "custom.echo"

    def run(self, input_doc: Doc) -> Doc:
        input_doc.raw = input_doc.raw or ""
        return input_doc

assert ProcessRegistry.get_process("custom.echo") is CustomEchoProcess
```

## Pipeline TOML

A pipeline spec is a TOML file with optional presets and per-step config. Steps can be
listed explicitly or inherited from a preset. Step configuration lives under the
`[step.*]` tables.

Key points:

- If `steps` is present, its order is used.
- If `steps` is omitted, `preset` defines the order.
- You can enable or disable steps with `enabled = true/false`.
- Both `[step.dependency.genai]` (nested) and `[step."dependency.genai"]` (quoted) are supported.

Example (`scripts/pipeline_latin_genai.toml`):

```toml
language = "lati1261"
preset = "latin.genai.default"

# If steps is omitted, preset provides ordering.
# If steps is provided, it overrides the preset ordering.
# steps = ["normalize", "sentence_split", "morphosyntax.genai", "dependency.genai", "enrichment.lexicon", "enrichment.phonology", "translation.genai"]

[step.normalize]
enabled = true

[step.sentence_split]
enabled = true

[step.morphosyntax.genai]
enabled = true
prompt_profile = "latin_ud_strict"

[step.dependency.genai]
enabled = true
prompt_profile = "latin_ud_strict"

# Phase 4 will replace enrichment.genai with composable enrichers; show future shape now:
[step.enrichment.lexicon]
enabled = true
source = "perseus"

[step.enrichment.phonology]
enabled = false
mode = "rule_trace"

[step.translation.genai]
enabled = true
prompt_profile = "student_friendly"

# Also support quoted keys:
[step."dependency.genai"]
# (same content as above if desired)
```

## Presets

Presets are named pipeline specs that provide an ordered set of steps and default
configuration. Current presets include:

- `latin.genai.default`
- `latin.genai.student_friendly`
- `latin.genai.epigraphy_conservative`

Use them with `preset = "..."` in your TOML.

## Prompt Profiles

Prompt profiles let you select prompt bundles without subclassing processes. A profile
can define templates per process and version.

Example usage in TOML:

```toml
[step.morphosyntax.genai]
prompt_profile = "latin_ud_strict"

[step.translation.genai]
prompt_profile = "student_friendly"
```

## Use A TOML Pipeline With NLP

Load a TOML spec and pass it as the `custom_pipeline` for `NLP().analyze()`:

```python
from cltk import NLP
from cltk.core.data_types import Pipeline

pipeline = Pipeline.from_toml("scripts/pipeline_latin_genai.toml")
nlp = NLP(language_code="lati1261", backend="openai", custom_pipeline=pipeline)
doc = nlp.analyze("Gallia est omnis divisa in partes tres.")
```

This keeps the normal `NLP` flow while letting you control step order, enable/disable steps, and prompt profiles through the TOML.

## CLI

Use the CLI to inspect or validate specs:

```bash
cltk pipeline describe --toml scripts/pipeline_latin_genai.toml
cltk pipeline validate --toml scripts/pipeline_latin_genai.toml
cltk pipeline presets
```
