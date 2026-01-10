## Translation with CLTK

This document describes how to obtain machine translations from CLTK’s GenAI pipelines, how translations are represented in the data model, and how to request non‑English targets.

Translations run after morphosyntax, dependency, and enrichment steps so the model can use glosses, lemma translations, idiom spans, and pedagogy notes rather than translating from scratch.

### Example

```python
from cltk import NLP

# Language with a GenAI pipeline, using OpenAI as backend
nlp = NLP(language_code="lati1261", backend="openai", model="gpt-5-mini", suppress_banner=True)

doc = nlp.analyze("Gallia est omnis divisa in partes tres.")

# Access translations
# print(doc.translation)                      # document-level string
# print(doc.translations)                     # list[Translation] (per sentence)
print("Translation:", doc.sentences[0].translation.text)    # first sentence translation
print("Notes:", doc.sentences[0].translation.notes)   # notes on difficult decisions
```

The above outputs:

```
Translation: All of Gaul is divided into three parts.
Notes: The participle divisa (perfect passive) with est yields a present-state reading—'is divided'—rather than a simple past. omnis modifies Gallia ('all of Gaul').
```

Outputs:

- `doc.translation`: concatenated translation text (when sentences were translated)
- `doc.translations`: list of `Translation` objects (`text`, `notes`, `source_lang_id`, `target_lang_id`)
- `sentence.translation`: structured translation for that sentence

### Requesting a non‑English target

The default target language is U.S. English (`"en-US"`), but this may be changed. First, subclass `LatinGenAITranslationProcess` and adjust the target language by changing `target_language` and `target_language_id`.

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
from cltk import NLP
from cltk.translation.processes import LatinGenAITranslationProcess


class LatinToFrenchTranslation(LatinGenAITranslationProcess):
    target_language: str = "Modern French"
    target_language_id: str = "fr-FR"

class LatinFrenchPipeline(Pipeline):
    glottolog_id: str = "lati1261"
    processes: Optional[list[Any]] = Field(
        default_factory=lambda: [
            MultilingualNormalizeProcess,
            LatinSentenceSplittingProcess,
            LatinGenAIMorphosyntaxProcess,
            LatinGenAIDependencyProcess,
            LatinGenAIEnrichmentProcess,
            LatinToFrenchTranslation,
        ]
    )

nlp = NLP(
    language_code="lati1261",
    backend="openai",
    model="gpt-5-mini",
    custom_pipeline=LatinFrenchPipeline(),
    suppress_banner=True
)
doc = nlp.analyze("Gallia est omnis divisa in partes tres.")

# print(doc.translation)
print("Translation:", doc.sentences[0].translation.text)
print("Notes:", doc.sentences[0].translation.notes)
```

The above outputs:

```
Translation: Toute la Gaule est divisée en trois parties.
Notes: J'ai rendu 'Gallia omnis' par «Toute la Gaule» (on pourrait aussi dire «La Gaule tout entière»). Le participe passif 'divisa ... est' devient «est divisée» et 'partes tres' = «trois parties».
```


### Reader’s guide rendering

`format_readers_guide(doc)` will display, per sentence:

- original sentence text
- translation (with target language identifier when present)
- translation notes summarizing ambiguous or idiomatic choices

### Troubleshooting

- Use a GenAI pipeline (`backend` of `openai`, `ollama`, `ollama-cloud`, or `mistral`) so translation runs after enrichment.
- If no translation appears, verify that tokens, dependencies, and enrichment are present; translation depends on them.
