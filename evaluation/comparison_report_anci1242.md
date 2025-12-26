# Compare Backends Report

## Metadata

- Language: anci1242
- Backends: stanza, openai
- Base backend: stanza
- Timestamp: 2025-12-25T23:06:51.295215+00:00
- Text hash: 52401ede26
- CLTK version: 2.3.1

## Agreement Rates

| Field | Backend Pair | Agree | Total | Rate |
| --- | --- | --- | --- | --- |
| tokenization | stanza vs openai | 15 | 47 | 0.319 |
| lemma | stanza vs openai | 14 | 15 | 0.933 |
| upos | stanza vs openai | 7 | 15 | 0.467 |
| feats | stanza vs openai | 11 | 15 | 0.733 |
| head | stanza vs openai | 4 | 15 | 0.267 |
| deprel | stanza vs openai | 8 | 15 | 0.533 |

## Top Disagreements

| Sentence | Row | Fields | Tokenization |
| --- | --- | --- | --- |
| 0 | 17 | tokenization, lemma, upos, feats, head, deprel | stanza=ἠσθένει; openai=None |
| 0 | 18 | tokenization, lemma, upos, feats, head, deprel | stanza=Δαρεῖος; openai=None |
| 0 | 20 | tokenization, lemma, upos, feats, head, deprel | stanza=ὑπώπτευε; openai=None |
| 0 | 21 | tokenization, lemma, upos, feats, head, deprel | stanza=τελευτὴν; openai=None |
| 0 | 22 | tokenization, lemma, upos, feats, head, deprel | stanza=τοῦ; openai=None |
| 0 | 23 | tokenization, lemma, upos, feats, head, deprel | stanza=βίου; openai=None |
| 0 | 25 | tokenization, lemma, upos, feats, head, deprel | stanza=ἐβούλετο; openai=None |
| 0 | 26 | tokenization, lemma, upos, feats, head, deprel | stanza=τὼ; openai=None |
| 0 | 27 | tokenization, lemma, upos, feats, head, deprel | stanza=παῖδε; openai=None |
| 0 | 28 | tokenization, lemma, upos, feats, head, deprel | stanza=ἀμφοτέρω; openai=None |

## Per-Sentence Details

### Sentence 0

Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι.

| Row | Tokenization |
| --- | --- |
| 0 | stanza=Δαρείου; openai=Δαρείου |
| 1 | stanza=καὶ; openai=καὶ |
| 2 | stanza=Παρυσάτιδος; openai=Παρυσάτιδος |
| 3 | stanza=γίγνονται; openai=γίγνονται |
| 5 | stanza=δύο; openai=δύο |
| 6 | stanza=,; openai=, |
| 7 | stanza=πρεσβύτερος; openai=πρεσβύτερος |
| 8 | stanza=μὲν; openai=μὲν |
| 9 | stanza=Ἀρταξέρξης; openai=Ἀρταξέρξης |
| 10 | stanza=,; openai=, |
| 11 | stanza=νεώτερος; openai=νεώτερος |
| 12 | stanza=δὲ; openai=δὲ |
| 13 | stanza=Κῦρος; openai=Κῦρος |
| 14 | stanza=:; openai=: |
| 15 | stanza=ἐπεὶ; openai=None |
| 16 | stanza=δὲ; openai=None |
| 17 | stanza=ἠσθένει; openai=None |
| 18 | stanza=Δαρεῖος; openai=None |
| 19 | stanza=καὶ; openai=None |
| 20 | stanza=ὑπώπτευε; openai=None |

Truncated 10 additional rows.

### Sentence 1

ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι.

| Row | Tokenization |
| --- | --- |
| 0 | stanza=None; openai=ἐπεὶ |
| 1 | stanza=None; openai=δὲ |
| 2 | stanza=None; openai=ἠσθένει |
| 3 | stanza=None; openai=Δαρεῖος |
| 4 | stanza=None; openai=καὶ |
| 5 | stanza=None; openai=ὑπώπτευε |
| 6 | stanza=None; openai=τελευτὴν |
| 7 | stanza=None; openai=τοῦ |
| 8 | stanza=None; openai=βίου |
| 9 | stanza=None; openai=, |
| 10 | stanza=None; openai=ἐβούλετο |
| 11 | stanza=None; openai=τὼ |
| 12 | stanza=None; openai=παῖδε |
| 13 | stanza=None; openai=ἀμφοτέρω |
| 14 | stanza=None; openai=παρεῖναι |
| 15 | stanza=None; openai=. |
