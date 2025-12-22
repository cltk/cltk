# Advanced Configuration

This page shows how to use the `CLTKConfig` model to configure `NLP()` beyond the basic constructor arguments. A `CLTKConfig` instance can be passed to `NLP(cltk_config=...)`, and its values override any other arguments.

For customizing prompts used by GenAI processes (without forking), see [Advanced Prompting](advanced-prompting.md).

## General pattern

```python
from cltk.core.data_types import CLTKConfig
from cltk.nlp import NLP

cltk_config = CLTKConfig(
    language_code="lati1261",
    backend="stanza",
    suppress_banner=True,
)

nlp = NLP(cltk_config=cltk_config)
doc = nlp.analyze("Arma virumque cano...")
```

Each backend has its own config block. Only set the block that matches the `backend` value.

## Stanza: choose a non‑default treebank

```python
from cltk.core.data_types import CLTKConfig, StanzaBackendConfig

cltk_config = CLTKConfig(
    language_code="lati1261",
    backend="stanza",
    stanza=StanzaBackendConfig(model="latin-ittb"),  # override default treebank
)
nlp = NLP(cltk_config=cltk_config)
```

## OpenAI / ChatGPT: temperature and retries

```python
from cltk.core.data_types import CLTKConfig, OpenAIBackendConfig

cltk_config = CLTKConfig(
    language_code="lati1261",
    backend="openai",
    model="gpt-5-mini",  # optional, defaults to gpt-5-mini
    openai=OpenAIBackendConfig(
        temperature=0.4,
        max_retries=1,
        # api_key="sk-...",  # overrides OPENAI_API_KEY if provided
    ),
)
nlp = NLP(cltk_config=cltk_config)
```

## Mistral: model and sampling controls

```python
from cltk.core.data_types import CLTKConfig, MistralBackendConfig

cltk_config = CLTKConfig(
    language_code="lati1261",
    backend="mistral",
    mistral=MistralBackendConfig(
        model="mistral-medium-latest",
        temperature=0.5,
        max_retries=1,
        # api_key="...",  # overrides MISTRAL_API_KEY if provided
    ),
)
nlp = NLP(cltk_config=cltk_config)
```

## Ollama (local): custom host/port and options

```python
from cltk.core.data_types import CLTKConfig, OllamaBackendConfig

cltk_config = CLTKConfig(
    language_code="lati1261",
    backend="ollama",
    ollama=OllamaBackendConfig(
        model="llama3.1:8b",
        host="http://my-ollama.local",
        port=11434,
        temperature=0.7,
        top_p=0.9,
        num_ctx=8192,
        num_predict=256,
        options={"stop": ["\n\n"]},
        max_retries=1,
    ),
)
nlp = NLP(cltk_config=cltk_config)
```

## Ollama (remote / cloud)

```python
from cltk.core.data_types import CLTKConfig, OllamaBackendConfig

cltk_config = CLTKConfig(
    language_code="lati1261",
    backend="ollama-cloud",
    ollama=OllamaBackendConfig(
        model="llama3.1:70b",
        host="https://ollama.example.com",
        port=8000,
        use_cloud=True,
        temperature=0.6,
        top_p=0.95,
        # api_key="...",  # overrides OLLAMA_CLOUD_API_KEY if provided
    ),
)
nlp = NLP(cltk_config=cltk_config)
```

## Notes

- Only one backend config block should be provided at a time; Pydantic validation will raise if more than one is set.
- When `cltk_config` is supplied, its values override the individual `NLP()` arguments (`language_code`, `backend`, `model`, `custom_pipeline`, `suppress_banner`).
- API keys in the config blocks take precedence over environment variables like `OPENAI_API_KEY`, `MISTRAL_API_KEY`, and `OLLAMA_CLOUD_API_KEY`.
- Currently applied knobs per backend:
  - Stanza: `stanza.model` selects the UD package/treebank (`package` in Stanza).
  - OpenAI: `temperature`, `api_key`, `max_retries`.
  - Mistral: `temperature`, `api_key`, `max_retries`.
  - Ollama: `temperature`, `top_p`, `num_ctx`, `num_predict`, `options`, `host`/`port`, `api_key`, `max_retries`.
