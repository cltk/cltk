# Compare Backends Report

## Metadata

- Language: lati1261
- Backends: stanza, openai
- Base backend: stanza
- Timestamp: 2025-12-25T18:03:07.512358+00:00
- Text hash: 3e09219f5a
- CLTK version: 2.3.1

## Agreement Rates

| Field | Backend Pair | Agree | Total | Rate |
| --- | --- | --- | --- | --- |
| tokenization | stanza vs openai | 8 | 8 | 1.000 |
| lemma | stanza vs openai | 7 | 8 | 0.875 |
| upos | stanza vs openai | 5 | 8 | 0.625 |
| feats | stanza vs openai | 5 | 8 | 0.625 |
| head | stanza vs openai | 8 | 8 | 1.000 |
| deprel | stanza vs openai | 6 | 8 | 0.750 |

## Top Disagreements

| Sentence | Row | Fields | Tokenization |
| --- | --- | --- | --- |
| 0 | 1 | upos, feats, deprel | stanza=est; openai=est |
| 0 | 2 | upos, feats, deprel | stanza=omnis; openai=omnis |
| 0 | 3 | lemma, feats | stanza=divisa; openai=divisa |
| 0 | 0 | upos | stanza=Gallia; openai=Gallia |

## Per-Sentence Details

### Sentence 0

Gallia est omnis divisa in partes tres.

| Row | Tokenization |
| --- | --- |
| 0 | stanza=Gallia; openai=Gallia |
| 1 | stanza=est; openai=est |
| 2 | stanza=omnis; openai=omnis |
| 3 | stanza=divisa; openai=divisa |
