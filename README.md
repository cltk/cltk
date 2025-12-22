The Classical Language Toolkit (CLTK) is a Python library offering natural language processing (NLP) for pre-modern languages.

## Installation

For the CLTK's latest version:

```bash
pip install cltk
```

Optional extras

- GenAI (OpenAI-backed annotation):

```bash
pip install "cltk[openai]"
```

- Stanza (discriminative NLP backends powered by Stanford Stanza):

```bash
pip install "cltk[stanza]"
```

You can combine extras, for example:

```bash
pip install "cltk[openai,stanza]"

# or include local LLM support as well
pip install "cltk[openai,stanza,ollama]"
```

- Local LLMs via Ollama:

Install the optional extra and ensure an Ollama server is running locally:

```bash
pip install "cltk[ollama]"
```

By default, when using `backend='ollama'`, CLTK uses the model `llama3.1:8b`. To choose a different local model, pass the `model` parameter to `NLP(...)`, e.g. `qwen2.5:14b`, `gemma2:27b`, `llama3.1:70b`, or any Ollama model string.

### Choosing a model

- OpenAI backend (GenAI in the cloud):

```python
from cltk.nlp import NLP

# Default model is "gpt-5-mini" when backend='openai'
nlp = NLP('lati1261', backend='openai')

# Choose a specific model
nlp_big = NLP('lati1261', backend='openai', model='gpt-5')

# Requires OPENAI_API_KEY to be set in the environment
# (e.g., via a .env file or shell env var)
```

- Ollama backend (local LLMs):

```python
from cltk.nlp import NLP

# Default model is "llama3.1:8b" when backend='ollama'
nlp_local = NLP('lati1261', backend='ollama')

# Choose a specific local model (any installed/pullable Ollama model)
nlp_qwen = NLP('lati1261', backend='ollama', model='qwen2.5:14b')

# To use the hosted Ollama Cloud, set OLLAMA_CLOUD_API_KEY
# and choose backend='ollama-cloud'. The same model strings apply.
```

For more information, see [Installation docs](https://docs.cltk.org/en/latest/installation.html) or, to install from source, [Development](https://docs.cltk.org/en/latest/development.html).

Pre-1.0 software remains available on the [branch v0.1.x](https://github.com/cltk/cltk/tree/v0.1.x) and docs at <https://legacy.cltk.org>. Install it with `pip install "cltk<1.0"`.

## LLM development guide

If you are changing CLTK's GenAI code, prompts, or pipelines, read the [LLM development guide](LLM_DEV_GUIDE.md) first.

## Documentation

Documentation at <https://docs.cltk.org>.

## Citation

When using the CLTK, please cite [the following publication](https://aclanthology.org/2021.acl-demo.3), including the DOI:

Johnson, Kyle P., Patrick J. Burns, John Stewart, Todd Cook, Clément Besnier, and William J. B. Mattingly. "The Classical Language Toolkit: An NLP Framework for Pre-Modern Languages." In *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations*, pp. 20-29. 2021. 10.18653/v1/2021.acl-demo.3

The complete BibTeX entry:

```bibtex
@inproceedings{johnson-etal-2021-classical,
    title = "The {C}lassical {L}anguage {T}oolkit: {A}n {NLP} Framework for Pre-Modern Languages",
    author = "Johnson, Kyle P.  and
      Burns, Patrick J.  and
      Stewart, John  and
      Cook, Todd  and
      Besnier, Cl{\'e}ment  and
      Mattingly, William J. B.",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-demo.3",
    doi = "10.18653/v1/2021.acl-demo.3",
    pages = "20--29",
    abstract = "This paper announces version 1.0 of the Classical Language Toolkit (CLTK), an NLP framework for pre-modern languages. The vast majority of NLP, its algorithms and software, is created with assumptions particular to living languages, thus neglecting certain important characteristics of largely non-spoken historical languages. Further, scholars of pre-modern languages often have different goals than those of living-language researchers. To fill this void, the CLTK adapts ideas from several leading NLP frameworks to create a novel software architecture that satisfies the unique needs of pre-modern languages and their researchers. Its centerpiece is a modular processing pipeline that balances the competing demands of algorithmic diversity with pre-configured defaults. The CLTK currently provides pipelines, including models, for almost 20 languages.",
}
```

## License

Copyright (c) 2014–present Kyle P. Johnson under the [MIT License](https://github.com/cltk/cltk/blob/master/LICENSE).
