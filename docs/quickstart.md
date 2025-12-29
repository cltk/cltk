# Quickstart

This guide helps you install CLTK and run working examples using each backend.

## Requirements

- Python 3.13+

## Install

- Base library:
    - pip: `pip install cltk`
- Optional extras (choose any):
    - Stanza: `pip install "cltk[stanza]"`
    - OpenAI: `pip install "cltk[openai]"`
    - Mistral: `pip install "cltk[mistral]"`
    - Ollama (local or cloud): `pip install "cltk[ollama]"`
- You can combine extras, e.g. `pip install "cltk[openai,stanza,ollama,mistral]"`.

## Environment Variables

Remote LLM require an API key for access. To set an environment variable, do one of the following:

- Set environment variables directly through the shell: `export OPENAI_API_KEY='<YOUR-SECRET-KEY>'`).
- Setting the variable inside your script: `os.environ["OPENAI_API_KEY"] = "<YOUR-SECRET-KEY>"`
  - Important: Do not do this if you need to share your code publicly.
- Putting them in a `.env` file located in the directory from which you run your code:

```bash
OPENAI_API_KEY=<YOUR-SECRET-KEU>
```

## Minimal Examples

### Stanza

- When `NLP()` is called without specifying the `backend` parameter, it defaults to executing Stanza-specific `Pipeline`s.
- Install `cltk[stanza]`.
- Stanza only supports the labeling of morphology, dependency syntax, and lemmatization.
- Language models (which will be installed by as needed).
- See [Languages](languages.md) for languages supported by Stanza models.

``` python
from cltk.nlp import NLP
nlp = NLP("lati1261", backend="stanza", suppress_banner=True)
doc = nlp.analyze("Gallia est omnis divisa in partes tres.")
for w in doc.words[:10]:
    print(w.string, getattr(w.upos, "tag", None), w.lemma)
```

### OpenAI

- Install `cltk[openai]`.
- Requires `OPENAI_API_KEY`.
- Defaults to model `gpt-5-mini` if not specified.

```python
import os
os.environ["OPENAI_API_KEY"] = "..."  # or set in your shell/.env

from cltk.nlp import NLP
nlp = NLP("lati1261", backend="openai", suppress_banner=True)
doc = nlp.analyze("Gallia est omnis divisa in partes tres.")
print("FORM\tLEMMA\tUPOS\tFEATS")
for w in doc.words:
    upos = getattr(w.upos, "tag", "_")
    feats = "_"
    if getattr(w, "features", None) and getattr(w.features, "features", None):
        items = []
        for f in w.features.features:
            if getattr(f, "key", None) and getattr(f, "value", None):
                items.append(f"{f.key}={f.value}")
        feats = "|".join(items) if items else "_"
    print(f"{w.string}\t{w.lemma}\t{upos}\t{feats}")
```

### Ollama

#### Ollama Local
- Install `cltk[ollama]`.
- Install the [Ollama server](https://ollama.com/) and run on `http://127.0.0.1:11434`).
- Defaults to model `llama3.1:8b` if not specified. You can pass any available model string.
- Note: You may override the Ollama host, port, and model. See [Advanced Configuration](advanced-configuration.md)


```python
from cltk.nlp import NLP
nlp = NLP("lati1261", backend="ollama", suppress_banner=True)
doc = nlp.analyze("Gallia est omnis divisa in partes tres.")
print(len(doc.words), "tokens")
```

#### Ollama Cloud

- Install `cltk[ollama]`.
- Set `OLLAMA_CLOUD_API_KEY` and use backend `ollama-cloud`.

```python
import os
os.environ["OLLAMA_CLOUD_API_KEY"] = "oc-..."  # or set in your shell/.env

from cltk.nlp import NLP
nlp = NLP("lati1261", backend="ollama-cloud", suppress_banner=True)
doc = nlp.analyze("Gallia est omnis divisa in partes tres.")
print("usage:", doc.genai_use)
```

<!--
## Dependency parsing (generative backends)

- Many language pipelines include an additional dependency step. If present, the `words` will also carry UD dependency labels and governors.
- Example (printing dependency info if available):

```python
for w in doc.words:
    deprel = getattr(getattr(w, "dependency_relation", None), "tag", None)
    print(w.string, "head=", w.governor, "deprel=", deprel)
``` -->

## Choosing Language Identifiers

- `NLP(language_code=...)` accepts Glottolog IDs (e.g. `"lati1261"`), ISO codes (e.g. `"lat"`), or exact language names (e.g. `"Latin"`). Internally, CLTK resolves to a Glottolog ID. See [languages.md] for more.
