# Advanced Prompting and Custom Pipelines

> Warning: This is an alpha feature. APIs and behaviors may change; use in production with care.

You can swap the default GenAI prompts without forking CLTK by providing custom prompt builders on your own `Process` subclasses and wiring them into a `Pipeline`.

## How prompt overrides work
- `GenAIMorphosyntaxProcess` accepts `prompt_builder` which can be a callable, a `PromptInfo`, or a string. Callables get `(lang_or_dialect_name, text)` and must return `PromptInfo`. Strings are formatted with `{lang_or_dialect_name}` and `{text}` and wrapped into `PromptInfo`.
- `GenAIDependencyProcess` accepts two optional builders that each can be callable, `PromptInfo`, or string:
  - `prompt_builder_from_tokens(lang_or_dialect_name: str, token_table: str) -> PromptInfo`
  - `prompt_builder_from_text(lang_or_dialect_name: str, sentence: str) -> PromptInfo`
- Builders should return `PromptInfo(kind, version, text, digest)`; reuse `cltk.genai.prompts._hash_prompt` or `PromptInfo` directly to keep logging/versioning meaningful.
- If no builder is provided, the built-in prompts are used.

## Example: custom morphosyntax prompt
```python
from typing import Optional

from cltk.core.data_types import Pipeline
from cltk.genai.prompts import PromptInfo, _hash_prompt
from cltk.morphosyntax.processes import (
    GenAIMorphosyntaxProcess,
    PromptBuilder as MorphPromptBuilder,
)
from cltk.text.processes import MultilingualNormalizeProcess
from cltk.sentence.processes import SentenceSplittingProcess
from cltk.nlp import NLP

def custom_morph_prompt(lang: str, text: str) -> PromptInfo:
    kind = "morphosyntax"
    version = "custom-1"
    prompt_text = (
        f"Tokenize the following {lang} text and output FORM, LEMMA, UPOS, FEATS as TSV.\n"
        "Rules:\n"
        "- Use strict UD tags and keep original diacritics.\n"
        "- Include punctuation with UPOS=PUNCT and FEATS=_.\n"
        "- Output only a Markdown code block with header: FORM\\tLEMMA\\tUPOS\\tFEATS.\n\n"
        f"Text:\n\n{text}\n"
    )
    digest = _hash_prompt(kind, version, prompt_text)
    return PromptInfo(kind=kind, version=version, text=prompt_text, digest=digest)

class LatinCustomMorph(GenAIMorphosyntaxProcess):
    glottolog_id: Optional[str] = "lati1261"
    prompt_builder: MorphPromptBuilder = custom_morph_prompt  # callable OK; strings or PromptInfo also allowed
    description = "Latin morphosyntax with a custom prompt"

pipeline = Pipeline(
    glottolog_id="lati1261",
    processes=[
        MultilingualNormalizeProcess,
        SentenceSplittingProcess,
        LatinCustomMorph,
    ],
)
nlp = NLP(language_code="lati1261", backend="openai", model="gpt-5-mini", custom_pipeline=pipeline)
doc = nlp.analyze("arma virumque cano")
print(doc.words)
```

## Example: custom dependency prompts
```python
from typing import Optional

from cltk.core.data_types import Pipeline
from cltk.genai.prompts import PromptInfo, _hash_prompt
from cltk.dependency.processes import (
    GenAIDependencyProcess,
    PromptBuilder as DepPromptBuilder,
)
from cltk.text.processes import MultilingualNormalizeProcess
from cltk.sentence.processes import SentenceSplittingProcess
from cltk.nlp import NLP

def dep_from_tokens(lang: str, table: str) -> PromptInfo:
    kind = "dependency-tokens"
    version = "custom-1"
    text = (
        "Use the tokens below to produce a dependency table with FORM, HEAD, DEPREL.\n"
        "HEAD is 1-based (0 for root). Output TSV in a code block with header FORM\\tHEAD\\tDEPREL.\n\n"
        f"Tokens:\n\n{table}\n"
    )
    return PromptInfo(kind=kind, version=version, text=text, digest=_hash_prompt(kind, version, text))

def dep_from_text(lang: str, sentence: str) -> PromptInfo:
    kind = "dependency-text"
    version = "custom-1"
    text = (
        f"For the following {lang} sentence, tokenize it and output FORM, HEAD, DEPREL as TSV in a code block.\n\n"
        f"Text:\n\n{sentence}\n"
    )
    return PromptInfo(kind=kind, version=version, text=text, digest=_hash_prompt(kind, version, text))

class LatinCustomDep(GenAIDependencyProcess):
    glottolog_id: Optional[str] = "lati1261"
    prompt_builder_from_tokens: DepPromptBuilder = dep_from_tokens  # callable OK; strings or PromptInfo also allowed
    prompt_builder_from_text: DepPromptBuilder = dep_from_text
    description = "Latin dependency parsing with custom prompts"

pipeline = Pipeline(
    glottolog_id="lati1261",
    processes=[
        MultilingualNormalizeProcess,
        SentenceSplittingProcess,
        LatinCustomDep,
    ],
)
nlp = NLP(language_code="lati1261", backend="openai", model="gpt-5-mini", custom_pipeline=pipeline)
doc = nlp.analyze("arma virumque cano")
print(doc.words)
```

## Tips
- Keep output schemas identical to the defaults so downstream parsing still works.
- Use low temperatures and deterministic settings when adjusting prompts.
- Log prompt versions/digests to trace which prompt produced a result (`CLTK_LOG_CONTENT=1` logs full prompts/responses).
