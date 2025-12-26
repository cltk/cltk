# Compare Backends Report

## Metadata

- Language: anci1242
- Backends: stanza, openai, mistral, ollama
- Base backend: stanza
- Timestamp: 2025-12-26T04:32:01.821739+00:00
- Text hash: 52401ede26
- CLTK version: 2.3.1

## Agreement Rates

| Field | Backend Pair | Agree | Total | Rate |
| --- | --- | --- | --- | --- |
| tokenization | stanza vs openai | 15 | 47 | 0.319 |
| tokenization | stanza vs mistral | 15 | 47 | 0.319 |
| tokenization | stanza vs ollama | 13 | 45 | 0.289 |
| tokenization | openai vs mistral | 15 | 47 | 0.319 |
| tokenization | openai vs ollama | 13 | 45 | 0.289 |
| tokenization | mistral vs ollama | 13 | 45 | 0.289 |
| lemma | stanza vs openai | 14 | 15 | 0.933 |
| lemma | stanza vs mistral | 14 | 15 | 0.933 |
| lemma | stanza vs ollama | 3 | 13 | 0.231 |
| lemma | openai vs mistral | 15 | 15 | 1.000 |
| lemma | openai vs ollama | 3 | 13 | 0.231 |
| lemma | mistral vs ollama | 3 | 13 | 0.231 |
| upos | stanza vs openai | 7 | 15 | 0.467 |
| upos | stanza vs mistral | 7 | 15 | 0.467 |
| upos | stanza vs ollama | 7 | 13 | 0.538 |
| upos | openai vs mistral | 14 | 15 | 0.933 |
| upos | openai vs ollama | 8 | 13 | 0.615 |
| upos | mistral vs ollama | 7 | 13 | 0.538 |
| feats | stanza vs openai | 12 | 15 | 0.800 |
| feats | stanza vs mistral | 10 | 15 | 0.667 |
| feats | stanza vs ollama | 4 | 13 | 0.308 |
| feats | openai vs mistral | 12 | 15 | 0.800 |
| feats | openai vs ollama | 4 | 13 | 0.308 |
| feats | mistral vs ollama | 4 | 13 | 0.308 |
| head | stanza vs openai | 6 | 15 | 0.400 |
| head | stanza vs mistral | 4 | 15 | 0.267 |
| head | stanza vs ollama | 2 | 13 | 0.154 |
| head | openai vs mistral | 9 | 15 | 0.600 |
| head | openai vs ollama | 1 | 13 | 0.077 |
| head | mistral vs ollama | 1 | 13 | 0.077 |
| deprel | stanza vs openai | 8 | 15 | 0.533 |
| deprel | stanza vs mistral | 7 | 15 | 0.467 |
| deprel | stanza vs ollama | 6 | 13 | 0.462 |
| deprel | openai vs mistral | 10 | 15 | 0.667 |
| deprel | openai vs ollama | 3 | 13 | 0.231 |
| deprel | mistral vs ollama | 2 | 13 | 0.154 |

## Top Disagreements

| Sentence | Row | Fields | Tokenization |
| --- | --- | --- | --- |
| 0 | 9 | lemma, upos, feats, head, deprel | stanza=Ἀρταξέρξης; openai=Ἀρταξέρξης; mistral=Ἀρταξέρξης; ollama=Ἀρταξέρξης |
| 0 | 12 | lemma, upos, head, deprel | stanza=δὲ; openai=δὲ; mistral=δὲ; ollama=δὲ |
| 0 | 0 | lemma, upos, feats, head, deprel | stanza=Δαρείου; openai=Δαρείου; mistral=Δαρείου; ollama=Δαρείου |
| 0 | 2 | lemma, upos, feats, head, deprel | stanza=Παρυσάτιδος; openai=Παρυσάτιδος; mistral=Παρυσάτιδος; ollama=Παρυσάτιδος |
| 0 | 7 | lemma, feats, head, deprel | stanza=πρεσβύτερος; openai=πρεσβύτερος; mistral=πρεσβύτερος; ollama=πρεσβύτερος |
| 0 | 10 | tokenization, lemma, upos, head, deprel | stanza=,; openai=,; mistral=,; ollama=None |
| 0 | 1 | upos, head, deprel | stanza=καὶ; openai=καὶ; mistral=καὶ; ollama=καὶ |
| 0 | 6 | tokenization, lemma, upos, head, deprel | stanza=,; openai=,; mistral=,; ollama=None |
| 0 | 11 | lemma, feats, head, deprel | stanza=νεώτερος; openai=νεώτερος; mistral=νεώτερος; ollama=νεώτερος |
| 0 | 13 | lemma, upos, feats, head, deprel | stanza=Κῦρος; openai=Κῦρος; mistral=Κῦρος; ollama=Κῦρος |

## Per-Sentence Details

### Sentence 0

Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι.

| Row | Tokenization |
| --- | --- |
| 0 | stanza=Δαρείου; openai=Δαρείου; mistral=Δαρείου; ollama=Δαρείου |
| 1 | stanza=καὶ; openai=καὶ; mistral=καὶ; ollama=καὶ |
| 2 | stanza=Παρυσάτιδος; openai=Παρυσάτιδος; mistral=Παρυσάτιδος; ollama=Παρυσάτιδος |
| 3 | stanza=γίγνονται; openai=γίγνονται; mistral=γίγνονται; ollama=γίγνονται |
| 4 | stanza=παῖδες; openai=παῖδες; mistral=παῖδες; ollama=παῖδες |
| 5 | stanza=δύο; openai=δύο; mistral=δύο; ollama=δύο |
| 6 | stanza=,; openai=,; mistral=,; ollama=None |
| 7 | stanza=πρεσβύτερος; openai=πρεσβύτερος; mistral=πρεσβύτερος; ollama=πρεσβύτερος |
| 8 | stanza=μὲν; openai=μὲν; mistral=μὲν; ollama=μὲν |
| 9 | stanza=Ἀρταξέρξης; openai=Ἀρταξέρξης; mistral=Ἀρταξέρξης; ollama=Ἀρταξέρξης |
| 10 | stanza=,; openai=,; mistral=,; ollama=None |
| 11 | stanza=νεώτερος; openai=νεώτερος; mistral=νεώτερος; ollama=νεώτερος |
| 12 | stanza=δὲ; openai=δὲ; mistral=δὲ; ollama=δὲ |
| 13 | stanza=Κῦρος; openai=Κῦρος; mistral=Κῦρος; ollama=Κῦρος |
| 14 | stanza=:; openai=:; mistral=:; ollama=: |
| 15 | stanza=ἐπεὶ; openai=None; mistral=None; ollama=None |
| 16 | stanza=δὲ; openai=None; mistral=None; ollama=None |
| 17 | stanza=ἠσθένει; openai=None; mistral=None; ollama=None |
| 18 | stanza=Δαρεῖος; openai=None; mistral=None; ollama=None |
| 19 | stanza=καὶ; openai=None; mistral=None; ollama=None |

Truncated 11 additional rows.

### Sentence 1

ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι.

| Row | Tokenization |
| --- | --- |
| 0 | stanza=None; openai=ἐπεὶ; mistral=None; ollama=None |
| 1 | stanza=None; openai=δὲ; mistral=None; ollama=None |
| 2 | stanza=None; openai=ἠσθένει; mistral=None; ollama=None |
| 3 | stanza=None; openai=Δαρεῖος; mistral=None; ollama=None |
| 4 | stanza=None; openai=καὶ; mistral=None; ollama=None |
| 5 | stanza=None; openai=ὑπώπτευε; mistral=None; ollama=None |
| 6 | stanza=None; openai=τελευτὴν; mistral=None; ollama=None |
| 7 | stanza=None; openai=τοῦ; mistral=None; ollama=None |
| 8 | stanza=None; openai=βίου; mistral=None; ollama=None |
| 9 | stanza=None; openai=,; mistral=None; ollama=None |
| 10 | stanza=None; openai=ἐβούλετο; mistral=None; ollama=None |
| 11 | stanza=None; openai=τὼ; mistral=None; ollama=None |
| 12 | stanza=None; openai=παῖδε; mistral=None; ollama=None |
| 13 | stanza=None; openai=ἀμφοτέρω; mistral=None; ollama=None |
| 14 | stanza=None; openai=παρεῖναι; mistral=None; ollama=None |
| 15 | stanza=None; openai=.; mistral=None; ollama=None |
| 16 | stanza=None; openai=None; mistral=ἐπεὶ; ollama=None |
| 17 | stanza=None; openai=None; mistral=δὲ; ollama=None |
| 18 | stanza=None; openai=None; mistral=ἠσθένει; ollama=None |
| 19 | stanza=None; openai=None; mistral=Δαρεῖος; ollama=None |

Truncated 26 additional rows.
