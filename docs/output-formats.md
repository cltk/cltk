# Output Documents

This page documents the helper functions that turn a processed `Doc` into human‑readable or machine‑readable output. Each function is pure (no file I/O) and returns a string; the caller decides how to persist it.

## `format_readers_guide(doc: Doc) -> str`

Render a Markdown “reader’s guide” aimed at students and scholars. The output is UTF‑8 Markdown with headings, blockquotes, and details blocks.

**Structure**

- A
- H1 title from `doc.metadata["title"]` or `doc.metadata["reference"]`, else “Reader’s Guide”.
- Optional pronunciation line when all enriched words share the same IPA mode.
- Per sentence:
  - `## Sentence N`
  - Blockquote of the sentence surface text (tokens joined with spaces).
  - `### Word-by-word`
  - For each word:
    - `### <surface>`
    - Italic POS name and bold gloss when available.
    - Bullets: Lemma, Gloss, Dictionary Gloss (if distinct), Dependency Role (name + code), Governor (1-based index), IPA (with mode), Syllables.
    - Optional `<details>` blocks for phonology trace and pedagogical notes.

**Example (truncated)**

````markdown
# Reader's Guide
**Pronunciation mode:** attic_5c_bce

## Sentence 1
> ὅτι δὲ τὸν τρόπον τοῦτον

### Word-by-word

### ὅτι
*subordinating conjunction* · **that / because (subordinating conjunction)**
- **Lemma:** ὅτι
- **Gloss:** that / because (subordinating conjunction)
- **Dependency Role:** marker (`mark`)
- **Governor:** token 8
- **IPA (attic_5c_bce):** `/ˈho.ti/`
- **Syllables:** ὅ-τι
<details>
<summary>Phonology</summary>
- initial rough breathing realised as /h-/ in Attic
- vowel qualities preserved; no contraction
- stress on first syllable (acute)
</details>
````

Use this when you need a study‑friendly breakdown with enrichment fields (gloss, IPA, orthography, pedagogy).

## `doc_to_feature_table(doc: Doc) -> pa.Table`

Convert a `Doc` into a tidy `pyarrow.Table` with one row per token, combining morphosyntax, dependencies, UD features, and selected metadata.

**Columns**

- Sentence index, global token index, token index in sentence
- `FORM`, `LEMMA`, `UPOS`, `HEAD`, `DEPREL`
- Metadata columns (if present on words): e.g., translation, definitions
- UD feature columns: each UD feature key becomes its own column
- Dependency extras (if present): governor sentence index, etc.

**Example**

```python
from cltk.utils.file_outputs import doc_to_feature_table
table = doc_to_feature_table(doc)
print(table.schema)
print(table.to_pandas().head())
```

Useful for analytics, export to Parquet/CSV, or downstream ML pipelines.

## `doc_to_conllu(doc: Doc) -> str`

Render a `Doc` as CoNLL‑U v2 text. One sentence per block, 10 tab‑separated fields per token.

**Behavior**

- Uses `doc.sentences` ordering; falls back to `doc.words` if sentences are absent.
- Writes `ID`, `FORM`, `LEMMA`, `UPOS`, `XPOS`, `FEATS`, `HEAD`, `DEPREL`, `DEPS`, `MISC`.
- Preserves existing lemmas/UPOS/FEATS/DEPREL/governor; leaves blanks (`_`) when data is missing.
- `HEAD` is 1‑based; 0 for roots.

**Example**

```
# sent_id = 1
# text = ὅτι δὲ τὸν τρόπον τοῦτον
1	ὅτι	ὅτι	SCONJ	_	_	8	mark	_	_
2	δὲ	δέ	PART	_	_	8	discourse	_	_
...
```

Use this to round‑trip with UD tools, validators, or treebanks. The function is deterministic and does no I/O; write the returned string to disk if needed.
