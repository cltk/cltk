# Provenance and Confidence

CLTK stores provenance records on the document and lightweight references on
sentences/tokens so analysis can be audited and reproduced.

## What is stored

- `Doc.provenance`: map of provenance id to `ProvenanceRecord`
- `Doc.default_provenance_id`: the primary run record for the document
- `Sentence.annotation_sources`: map of field name to provenance id
- `Word.annotation_sources`: map of field name to provenance id
- `Word.confidence`: map of field name to confidence value (0..1)

Provenance records include backend/model identifiers, prompt/config digests,
and runtime metadata (CLTK/Python/platform versions). Prompt digests use
SHA-256 of the canonical prompt text; config digests use SHA-256 of a
canonicalized config snapshot.

Confidence values are only populated when a backend returns them (for example,
LLM prompts that emit `*_CONF` fields or JSON `confidence` fields).

## How to cite a run

Use the default provenance id plus the key digests and versions:

```
CLTK run: <prov_id> (backend=<backend>, model=<model>,
prompt_digest=<sha256>, config_digest=<sha256>, cltk_version=<version>)
```

## Exporting provenance

All exporters keep default behavior unless you opt in:

```python
from cltk.utils.file_outputs import (
    doc_to_conllu,
    doc_to_feature_table,
    format_readers_guide,
)

doc_to_conllu(doc, include_provenance=True, include_confidence=True)
doc_to_feature_table(doc, include_provenance=True, include_confidence=True)
format_readers_guide(doc, include_provenance=True, include_confidence=True)
```
