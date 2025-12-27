# Pipelines

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

## Pipeline TOML

A pipeline spec is a TOML file with optional presets and per-step config. Steps can be
listed explicitly or inherited from a preset. Step configuration lives under the
`[step.*]` tables.

Key points:

- If `steps` is present, its order is used.
- If `steps` is omitted, `preset` defines the order.
- You can enable or disable steps with `enabled = true/false`.
- Both `[step.dependency.genai]` (nested) and `[step."dependency.genai"]` (quoted) are supported.

Example (`examples/pipeline_latin_genai.toml`):

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

pipeline = Pipeline.from_toml("examples/pipeline_latin_genai.toml")
nlp = NLP(language_code="lati1261", backend="openai", custom_pipeline=pipeline)
doc = nlp.analyze("Gallia est omnis divisa in partes tres.")
```

This keeps the normal `NLP` flow while letting you control step order, enable/disable steps, and prompt profiles through the TOML.

## CLI

Use the CLI to inspect or validate specs:

```bash
cltk pipeline describe --toml examples/pipeline_latin_genai.toml
cltk pipeline validate --toml examples/pipeline_latin_genai.toml
cltk pipeline presets
```
