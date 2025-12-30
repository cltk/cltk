# CLTK data types

This page summarizes the core data structures you will work with when using CLTK. The first section covers objects returned by `NLP().analyze()`. The second section covers internal types that can be used to override defaults.

## Objects returned by `NLP().analyze()`

### `Doc`

The `Doc` object is the top-level container returned by `NLP().analyze()`.

Key attributes:

- `language`: Resolved `Language` metadata.
- `words`: List of `Word` objects (token-level annotations).
- `raw`: Original input text.
- `normalized_text`: Normalized version of `raw` when a normalizer runs.
- `sentence_boundaries`: List of `(start, stop)` character offsets.
- `sentence_embeddings`: Optional embeddings keyed by sentence index.
- `sentence_translations`: `dict[int, Translation]` keyed by sentence index.
- `translation`: Optional aggregated translation string.
- `translations`: List of `Translation` objects (usually per sentence).
- `pipeline`: The `Pipeline` instance that produced the doc.
- `backend` and `model`: Backend/model identifiers used for processing.
- `metadata`: Free-form metadata populated by processes.

Helper properties:

- `sentence_strings`: Returns sentence substrings computed from `normalized_text` and `sentence_boundaries`.
- `sentences`: Returns `Sentence` objects grouped by `Word.index_sentence` and ordered by `Word.index_token`. Each `Sentence` includes the per-sentence translation and embedding when present.

Notes:

- The `translation` field is an optional string. Structured translations live in `sentence_translations` and `translations`.

### `Word`

The `Word` object contains per-token annotations.

Key attributes:

- `index_char_start`, `index_char_stop`: Character offsets.
- `index_token`: Token index within its sentence.
- `index_sentence`: Sentence index within the doc.
- `string`: Token surface form.
- `lemma`, `stem`: Lemma/stem if produced.
- `upos`: Holds `UDPartOfSpeechTag` for a POS tag (e.g., noun, verb) conformant to the Universal Dependencies standard.
- `features`: Holds `UDFeatureTagSet` Full morphosynatic tags conformant to the Universal Dependencies standard.
- `dependency_relation`: For `UDDeprelTag`, a dependency relation label conformant to the Universal Dependencies standard.
- `governor`: An `int` pointing to the dependency head of the parse tree.
- `embedding`: Optional vector embedding.
- `stop`: Stopword flag.
- `named_entity`: Named entity tag if available.
- `enrichment`: `WordEnrichment` bundle (glosses, translations, IPA, etc.).
- `annotation_sources`: Provenance per annotation type.
- `confidence`: Confidence scores per annotation type.

Notes:

- Internal `_doc` reference may be attached to allow back-references to the parent `Doc`.

### `UDPartOfSpeechTag`

Universal Dependencies part-of-speech tag enum used for `Word.upos`.

Notes:

- Values follow the UD POS tagset; see `src/cltk/morphosyntax/ud_pos.py` for the full list.
- See the UD website for full definitions: <https://universaldependencies.org/u/pos/index.html>

### `UDFeatureTagSet`

Bundle of Universal Dependencies morphosyntactic features used for `Word.features`. Consists of one or more `UDDeprelTag`. Example:

```python
>>> nlp = NLP("lat", suppress_banner=True)
>>> doc = nlp.analyze("accipe")
>>> doc.words[0].features
UDFeatureTagSet([UDFeatureTag(Aspect=Imperfective), UDFeatureTag(Mood=Imperative), UDFeatureTag(Number=Singular), UDFeatureTag(Person=Second person), UDFeatureTag(Tense=Present), UDFeatureTag(VerbForm=Finite), UDFeatureTag(Voice=Active)])
```

Notes:

- Exposes UD feature keys and values as a structured tag set; see `src/cltk/morphosyntax/ud_features.py`.

### `UDDeprelTag`

Universal Dependencies dependency relation tag used for `Word.dependency_relation`.

Notes:

- Values follow the UD dependency relation set; see `src/cltk/morphosyntax/ud_deprels.py`.
- See the UD website for full definitions: <https://universaldependencies.org/u/feat/all.html>

### `Sentence`

The `Sentence` object groups words and optional metadata for a sentence.

Key attributes:

- `words`: List of `Word` objects for the sentence.
- `index`: Sentence index.
- `embedding`: Optional sentence embedding.
- `translation`: Optional `Translation` for the sentence.
- `annotation_sources`: Provenance for sentence-level annotations.

Notes:

- `Sentence` objects are produced by `Doc.sentences` and are derived from `Word.index_sentence` and `Word.index_token`.

### `Translation`

Structured translation metadata.

Key attributes:

- `source_lang_id`: Optional source language ID.
- `target_lang_id`: Optional target language ID.
- `text`: Translation text.
- `notes`: Optional notes from the translation process.
- `confidence`: Optional confidence value in `[0, 1]`.

### `Gloss`

Contextual and dictionary gloss information.

Key attributes:

- `dictionary`: Dictionary gloss (if provided).
- `context`: Contextual gloss (if provided).
- `alternatives`: List of `ScoredText` alternatives with optional probabilities.

## Internal types

These may be used to override the CLTK's defaults.

### `Language`

Language metadata used for resolution and display.

Key attributes:

- `name`: Human-readable language name.
- `glottolog_id`: Glottolog ID (used for pipeline selection).
- `identifiers`, `iso`, `iso_set`: Identifier metadata.
- `classification`, `family_id`, `parent_id`: Family and lineage info.
- `scripts`, `orthographies`, `alt_names`: Orthography and naming data.
- `dialects`: List of `Dialect` records.

Notes:

- For user-defined languages, supply a `glottolog_id` and `name` at minimum.

### `Dialect`

`Dialect` metadata associated with a parent `Language`.

Key attributes:

- `glottolog_id`: Dialect Glottolog ID.
- `language_code`: Optional dialect code alias.
- `name`: Dialect name.
- `status`, `alt_names`, `scripts`, `orthographies`: Descriptive metadata.

### `Pipeline`

A pipeline is an ordered set of processes that transforms a `Doc`.

Key attributes:

- `processes`: List of `Process` classes or instances (order matters).
- `description`: Human-readable description.
- `language`, `dialect`, `glottolog_id`: Optional language metadata.
- `spec`: Optional declarative pipeline spec.

Helper methods:

- `add_process(process)`: Append a process to the pipeline.
- `describe()`: Return a human-friendly process list (uses registry for `spec`).

Notes:

- If `glottolog_id` is set, the pipeline can auto-resolve `language`/`dialect`.

### `Process`

Base class for a pipeline step. Each process accepts, transforms, and finally returns a `Doc`.

Key attributes:

- `process_id`: Stable identifier used by registries/specs.
- `glottolog_id`: Optional language code for language-specific logic.

Required method:

- `run(input_doc) -> Doc`: Apply the process and return the modified doc.

### `CLTKConfig`

Bundled configuration for initializing `NLP()`.

Key attributes:

- `language_code`: Language identifier string (Glottolog, ISO, or name).
- `language`: Optional `Language` object (used when defining custom languages).
- `backend`: Backend selection (`stanza`, `openai`, `ollama`, etc.).
- `model`: Optional model name.
- `custom_pipeline`: Optional `Pipeline` instance to override defaults.
- `suppress_banner`: Toggle console banner output.

Backend-specific config blocks:

- `stanza`, `openai`, `mistral`, `ollama`: Optional backend config blocks.
- `active_backend_config`: Returns the config block for the selected backend.

Notes:

- Provide either `language_code` or `language`. If only `language` is supplied, its `glottolog_id` is used as the language code.
- Only one backend config block can be provided at a time.
