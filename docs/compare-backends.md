# Compare Backends

The compare backends feature runs the same input through multiple CLTK NLP
backends and produces a structured diff report. Use it to spot disagreements
in tokenization, lemma, UPOS, features, head, and dependency relations.

## Python API

```python
from cltk.evaluation.compare_backends import compare_backends, report_to_markdown

report = compare_backends(
    "lati1261",
    "Gallia est omnis divisa in partes tres.",
    ["stanza", "openai"],
)
print(report_to_markdown(report))
```

## CLI

```bash
python -m cltk.compare_backends \
  --language lati1261 \
  --text "Gallia est omnis divisa in partes tres." \
  --backends stanza,openai \
  --out report.md
```

To write JSON, Markdown, and CSV outputs in a directory:

```bash
python -m cltk.compare_backends \
  --language lati1261 \
  --text "Gallia est omnis divisa in partes tres." \
  --backends stanza,openai \
  --out-dir ./reports
```
