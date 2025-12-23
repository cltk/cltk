## Translation with CLTK

This document describes how to obtain machine translations from CLTK’s GenAI pipelines, how translations are represented in the data model, and how to request non‑English targets.

### Quick start

```python
from cltk.nlp import NLP

# Language with a GenAI pipeline, using OpenAI as backend
nlp = NLP(language_code="lati1261", backend="openai", model="gpt-5-mini")

doc = nlp.analyze("Gallia est omnis divisa in partes tres.")

# Access translations
print(doc.translation)                      # document-level string
print(doc.translations)                     # list[Translation] (per sentence)
print(doc.sentences[0].translation.text)    # first sentence translation
print(doc.sentences[0].translation.notes)   # notes on difficult decisions
```

Outputs:
- `doc.translation`: concatenated translation text (when sentences were translated)
- `doc.translations`: list of `Translation` objects (`text`, `notes`, `source_lang_id`, `target_lang_id`)
- `sentence.translation`: structured translation for that sentence

Translations run after morphosyntax, dependency, and enrichment steps so the model can use glosses, lemma translations, idiom spans, and pedagogy notes rather than translating from scratch.

### Requesting a non‑English target (first pass)

Set a different target before translation runs by overriding the translation process defaults inside a custom pipeline. For Latin, the default GenAI pipeline is:

1. `MultilingualNormalizeProcess`
2. `LatinSentenceSplittingProcess`
3. `LatinGenAIMorphosyntaxProcess`
4. `LatinGenAIDependencyProcess`
5. `LatinGenAIEnrichmentProcess`
6. `LatinGenAITranslationProcess`

You can subclass `LatinGenAITranslationProcess` and adjust the target language by changing `target_language` and `target_language_id`.

```python
"""End-to-end example of translating into a non-English language."""
from typing import Any, Optional

from pydantic import Field

from cltk.core.data_types import Pipeline
from cltk.languages.pipelines import (
    LatinGenAIDependencyProcess,
    LatinGenAIEnrichmentProcess,
    LatinGenAIMorphosyntaxProcess,
    LatinGenAIPipeline,
    LatinSentenceSplittingProcess,
    MultilingualNormalizeProcess,
)
from cltk.nlp import NLP
from cltk.translation.processes import LatinGenAITranslationProcess


class LatinToFrenchTranslation(LatinGenAITranslationProcess):
    target_language: str = "Modern French"
    target_language_id = "fr-FR"

class LatinFrenchPipeline(Pipeline):
    glottolog_id = "lati1261"
    processes: Optional[list[type]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LatinSentenceSplittingProcess,
            LatinGenAIMorphosyntaxProcess,
            LatinGenAIDependencyProcess,
            LatinGenAIEnrichmentProcess,
            LatinToFrenchTranslation,
        ]
    )

nlp = NLP(language_code="lati1261", backend="openai", model="gpt-5-mini",
          custom_pipeline=LatinFrenchPipeline())
doc = nlp.analyze("Gallia est omnis divisa in partes tres.")

print(doc.translation)
print(doc.sentences[0].translation.text)
print(doc.sentences[0].translation.notes)
```

If you save the above to `non_en_translation.py`, it will output:

```bash
% python non_en_translation.py
𐤀 CLTK version '2.2.0'. When using the CLTK in research, please cite: https://aclanthology.org/2021.acl-demo.3/
Selected language "Latin" ("lati1261") without dialect.
Pipeline for `NLP("lati1261", backend="openai")`: ['MultilingualNormalizeProcess', 'LatinSentenceSplittingProcess', 'LatinGenAIMorphosyntaxProcess', 'LatinGenAIDependencyProcess', 'LatinGenAIEnrichmentProcess', 'LatinToFrenchTranslation']
⸖ Process name: MultilingualNormalizeProcess
⸖ Process name: LatinSentenceSplittingProcess
⸖ Process name: LatinGenAIMorphosyntaxProcess
    Process author: CLTK
    Description: Default morphology tagging process using a generative GPT model for the Latin language.
⸖ Process name: LatinGenAIDependencyProcess
    Process author: CLTK
    Description: Default dependency syntax parsing process using a generative GPT model for the Latin language.
⸖ Process name: LatinGenAIEnrichmentProcess
    Process author: CLTK
    Description: Default textual enrichment process using a generative GPT model for the Latin language.
⸖ Process name: LatinToFrenchTranslation
    Process author: CLTK
    Description: Default textual translation process using a generative GPT model for the Latin language.
Toute la Gaule est divisée en trois parties.
Toute la Gaule est divisée en trois parties.
«Gallia omnis» rendu par «Toute la Gaule» (could also be «La Gaule tout entière»). Verbe parfait passif «divisa» → «est divisée»; «partes tres» → «trois parties». Agreement respects feminine singular «Gaule».
```


### Reader’s guide rendering

`format_readers_guide(doc)` will display, per sentence:
- original sentence text
- translation (with target language identifier when present)
- translation notes summarizing ambiguous or idiomatic choices

### Troubleshooting

- Use a GenAI pipeline (`backend` of `openai`, `ollama`, `ollama-cloud`, or `mistral`) so translation runs after enrichment.
- If no translation appears, verify that tokens, dependencies, and enrichment are present; translation depends on them.
