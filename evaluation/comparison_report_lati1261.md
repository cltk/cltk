# Compare Backends Report

## Metadata

- Language: lati1261
- Backends: stanza, openai, mistral, ollama
- Base backend: stanza
- Timestamp: 2025-12-26T04:24:29.896853+00:00
- Text hash: 3e09219f5a
- CLTK version: 2.3.1

## Agreement Rates

| Field | Backend Pair | Agree | Total | Rate |
| --- | --- | --- | --- | --- |
| tokenization | stanza vs openai | 8 | 8 | 1.000 |
| tokenization | stanza vs mistral | 8 | 8 | 1.000 |
| tokenization | stanza vs ollama | 8 | 8 | 1.000 |
| tokenization | openai vs mistral | 8 | 8 | 1.000 |
| tokenization | openai vs ollama | 8 | 8 | 1.000 |
| tokenization | mistral vs ollama | 8 | 8 | 1.000 |
| lemma | stanza vs openai | 7 | 8 | 0.875 |
| lemma | stanza vs mistral | 7 | 8 | 0.875 |
| lemma | stanza vs ollama | 0 | 8 | 0.000 |
| lemma | openai vs mistral | 7 | 8 | 0.875 |
| lemma | openai vs ollama | 0 | 8 | 0.000 |
| lemma | mistral vs ollama | 0 | 8 | 0.000 |
| upos | stanza vs openai | 5 | 8 | 0.625 |
| upos | stanza vs mistral | 6 | 8 | 0.750 |
| upos | stanza vs ollama | 7 | 8 | 0.875 |
| upos | openai vs mistral | 7 | 8 | 0.875 |
| upos | openai vs ollama | 6 | 8 | 0.750 |
| upos | mistral vs ollama | 7 | 8 | 0.875 |
| feats | stanza vs openai | 6 | 8 | 0.750 |
| feats | stanza vs mistral | 4 | 8 | 0.500 |
| feats | stanza vs ollama | 1 | 8 | 0.125 |
| feats | openai vs mistral | 5 | 8 | 0.625 |
| feats | openai vs ollama | 1 | 8 | 0.125 |
| feats | mistral vs ollama | 1 | 8 | 0.125 |
| head | stanza vs openai | 8 | 8 | 1.000 |
| head | stanza vs mistral | 2 | 8 | 0.250 |
| head | stanza vs ollama | 0 | 8 | 0.000 |
| head | openai vs mistral | 2 | 8 | 0.250 |
| head | openai vs ollama | 0 | 8 | 0.000 |
| head | mistral vs ollama | 0 | 8 | 0.000 |
| deprel | stanza vs openai | 6 | 8 | 0.750 |
| deprel | stanza vs mistral | 5 | 8 | 0.625 |
| deprel | stanza vs ollama | 2 | 8 | 0.250 |
| deprel | openai vs mistral | 6 | 8 | 0.750 |
| deprel | openai vs ollama | 2 | 8 | 0.250 |
| deprel | mistral vs ollama | 2 | 8 | 0.250 |

## Top Disagreements

| Sentence | Row | Fields | Tokenization |
| --- | --- | --- | --- |
| 0 | 1 | lemma, upos, feats, head, deprel | stanza=est; openai=est; mistral=est; ollama=est |
| 0 | 3 | lemma, feats, head, deprel | stanza=divisa; openai=divisa; mistral=divisa; ollama=divisa |
| 0 | 2 | lemma, upos, feats, head, deprel | stanza=omnis; openai=omnis; mistral=omnis; ollama=omnis |
| 0 | 0 | lemma, upos, feats, head, deprel | stanza=Gallia; openai=Gallia; mistral=Gallia; ollama=Gallia |
| 0 | 4 | lemma, feats, head, deprel | stanza=in; openai=in; mistral=in; ollama=in |
| 0 | 5 | lemma, feats, head, deprel | stanza=partes; openai=partes; mistral=partes; ollama=partes |
| 0 | 6 | lemma, feats, head | stanza=tres; openai=tres; mistral=tres; ollama=tres |
| 0 | 7 | lemma, head | stanza=.; openai=.; mistral=.; ollama=. |

## Per-Sentence Details

### Sentence 0

Gallia est omnis divisa in partes tres.

| Row | Tokenization |
| --- | --- |
| 0 | stanza=Gallia; openai=Gallia; mistral=Gallia; ollama=Gallia |
| 1 | stanza=est; openai=est; mistral=est; ollama=est |
| 2 | stanza=omnis; openai=omnis; mistral=omnis; ollama=omnis |
| 3 | stanza=divisa; openai=divisa; mistral=divisa; ollama=divisa |
| 4 | stanza=in; openai=in; mistral=in; ollama=in |
| 5 | stanza=partes; openai=partes; mistral=partes; ollama=partes |
| 6 | stanza=tres; openai=tres; mistral=tres; ollama=tres |
| 7 | stanza=.; openai=.; mistral=.; ollama=. |
