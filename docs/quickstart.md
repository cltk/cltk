# Quickstart

This guide helps you install CLTK and run minimal, working examples using each backend.

## Requirements

- Python 3.13+

## Install

- Base library:
  - pip: `pip install cltk`
- Optional extras (choose any):
  - OpenAI: `pip install "cltk[openai]"`
  - Stanza: `pip install "cltk[stanza]"`
  - Ollama (local or cloud): `pip install "cltk[ollama]"`
- You can combine extras, e.g. `pip install "cltk[openai,stanza,ollama]"`.

## Environment

- OpenAI: set `OPENAI_API_KEY`.
- Ollama Cloud: set `OLLAMA_CLOUD_API_KEY`.
- Ollama local: ensure the Ollama server is running (defaults to `http://127.0.0.1:11434`).

## Minimal examples

### Stanza (default backend)

- Requires the stanza extra and language models (CLTK will prompt/install as needed).
- Example (Latin):

``` python
from cltk.nlp import NLP
nlp = NLP("lati1261", backend="stanza", suppress_banner=True)
doc = nlp.analyze("Gallia est omnis divisa in partes tres.")
for w in doc.words[:10]:
    print(w.string, getattr(w.upos, "tag", None), w.lemma)
```

### OpenAI (cloud LLM)

- Requires `OPENAI_API_KEY`.
- Defaults to model `gpt-5-mini` if not specified.
- Example (Latin):

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."  # or set in your shell/.env

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

### Ollama (local LLM)

- Ensure the Ollama server is running and the `cltk[ollama]` extra is installed.
- Defaults to model `llama3.1:8b` if not specified. You can pass any available model string.
- Example (Latin):

  ```python
  from cltk.nlp import NLP
  nlp = NLP("lati1261", backend="ollama", suppress_banner=True)
  doc = nlp.analyze("Gallia est omnis divisa in partes tres.")
  print(len(doc.words), "tokens")
  ```

- Ollama Cloud (hosted)
  - Set `OLLAMA_CLOUD_API_KEY` and use backend `ollama-cloud`.
  - Example (Latin):

  ```python
  import os
  os.environ["OLLAMA_CLOUD_API_KEY"] = "oc-..."  # or set in your shell/.env

  from cltk.nlp import NLP
  nlp = NLP("lati1261", backend="ollama-cloud", suppress_banner=True)
  doc = nlp.analyze("Gallia est omnis divisa in partes tres.")
  print("usage:", doc.openai)
  ```

## Dependency parsing (generative backends)

- Many language pipelines include an additional dependency step. If present, the `words` will also carry UD dependency labels and governors.
- Example (printing dependency info if available):

```python
for w in doc.words:
    deprel = getattr(getattr(w, "dependency_relation", None), "tag", None)
    print(w.string, "head=", w.governor, "deprel=", deprel)
```

## Choosing identifiers

- `NLP(language_code=...)` accepts Glottolog IDs (e.g. `"lati1261"`), ISO codes (e.g. `"lat"`), or exact language names (e.g. `"Latin"`). Internally, CLTK resolves to a Glottolog ID.

# Troubleshooting

- Missing API key errors: ensure the relevant environment variable is set.
- Ollama client errors about httpx: the `cltk[ollama]` extra pins a compatible httpx; upgrade with `pip install -U "cltk[ollama]"`.
- To suppress banner output in examples, pass `suppress_banner=True` when creating `NLP`.

# Logging

- To improve logging, optionally enable:
  - Whether the logger writes to a file cltk.log in the current working directory: `CLTK_LOG_TO_FILE=1|true|yes|on`. Default: `off`.
  - Whether sensitive content is emitted to logs at all (prompts, raw responses, extracted TSV rows, etc.): `CLTK_LOG_CONTENT=1|true|yes|on`. Default: `off`.
  - Log level: `CLTK_LOG_LEVEL=DEBUG|INFO|WARNING|ERROR`

Programmatic logging configuration (in code):

- Console debug only (no file):

```python
from cltk.core.cltk_logger import setup_cltk_logger

setup_cltk_logger(level="DEBUG", log_to_console=True, log_to_file=False)
```

- Write logs to a file (no sensitive content):

```python
from cltk.core.cltk_logger import setup_cltk_logger

setup_cltk_logger(level="INFO", log_to_console=True, log_to_file=True)
```

- Enable sensitive content logs (prompts/responses) at runtime:

```python
import os
from cltk.core.cltk_logger import setup_cltk_logger

os.environ["CLTK_LOG_CONTENT"] = "1"  # allow content logs
setup_cltk_logger(level="DEBUG", log_to_console=True, log_to_file=False)
```

- Persist sensitive content to disk (explicit opt‑in):

```python
import os
from cltk.core.cltk_logger import setup_cltk_logger

os.environ["CLTK_LOG_CONTENT"] = "1"
setup_cltk_logger(level="DEBUG", log_to_console=True, log_to_file=True)
# Note: certain rare error details (e.g., feature parse failures) are also
# written to features_err.log only when BOTH content logging and file logging are enabled.
```

- Revert to quiet defaults later in the same process:

```python
from cltk.core.cltk_logger import setup_cltk_logger

setup_cltk_logger(level="INFO", log_to_console=True, log_to_file=False)
```
