# CLTK LLM Development Guide

This guide tells humans and LLM-based helpers how to extend or modify CLTK's GenAI features without breaking the rest of the toolkit. Read it before touching any code that calls hosted models, builds prompts, or parses LLM output.

## Scope and expectations
- Applies to all GenAI-backed code under `src/cltk/genai/`, the GenAI processes in `src/cltk/morphosyntax/` and `src/cltk/dependency/`, any new pipelines that rely on hosted or local LLMs, **and** any regular Python code generated or proposed by an LLM (even if it is not directly calling a model).
- Prefer minimal, explicit changes: small functions, clear typing, and deterministic defaults. Keep classical-language constraints in mind (diacritics, RTL scripts, mixed encodings).
- Avoid introducing new dependencies unless strictly necessary. Use the existing wrappers instead of one-off SDK calls.

## Architecture quick map
- Entry points: `OpenAIConnection`, `AsyncOpenAIConnection` (`src/cltk/genai/openai.py`); `OllamaConnection`, `AsyncOllamaConnection` (`src/cltk/genai/ollama.py`); `MistralConnection` (`src/cltk/genai/mistral.py`).
- Prompt builders live in `src/cltk/genai/prompts.py`; extend these instead of inlining prompts.
- GenAI processes plug into pipelines via `GenAIMorphosyntaxProcess` and `GenAIDependencyProcess` in `src/cltk/morphosyntax/processes.py` and `src/cltk/dependency/processes.py`.
- Responses are normalized to `CLTKGenAIResponse` (`src/cltk/core/data_types.py`); keep that shape stable.

## Runtime, configuration, dependencies
- Supported extras: `cltk[openai]` and `cltk[ollama]`. Env vars: `OPENAI_API_KEY`, `OLLAMA_CLOUD_API_KEY`. Use `.env` loading via `load_env_file()` when needed.
- Default models: OpenAI backend uses `gpt-5-mini` by default; Ollama backend uses `llama3.1:8b`. Override via the `model` parameter; document any non-default you hardcode.
- Keep temperature, top_p, and timeouts explicit; set conservative defaults (e.g., low temperature) for reproducibility.
- Do not add new network calls outside the existing clients; prefer dependency-free utilities from `src/cltk/utils/` and `src/cltk/text/`.

## Coding style
- Use modern typing directly (PEP 604 unions, standard generics); do not add `from __future__ import annotations` or other “old-style” typing shims.

## Prompt and model usage
- Build prompts through `PromptInfo` helpers in `src/cltk/genai/prompts.py`. If you need a new task, add a new builder with versioned text and a digest; do not embed raw prompts in call sites.
- Custom pipelines can override prompts by subclassing `GenAIMorphosyntaxProcess` or `GenAIDependencyProcess` and setting their prompt fields to a callable, `PromptInfo`, or string. Strings are formatted with `{lang_or_dialect_name}` plus `{text}`/`{token_table}`/`{sentence}` as applicable and wrapped into `PromptInfo`. Keep versions/digests meaningful and reuse shared parsing rules.
- Structure: system/context (if required), short instruction, rules, and an explicit output schema. Favor TSV or JSON inside fenced code blocks for easy parsing.
- Preserve the original text spelling, including diacritics and breathings; do not auto-normalize unless a caller explicitly requests it.
- Keep prompts concise and avoid meta-conversation. Make the model return final answers in one shot (no "let's think step by step" unless the output requires it and you validate the result).
- Document any language-specific quirks you encode (e.g., tokenization expectations for enclitics).

## Output parsing and validation
- Always expect fenced code blocks and validate that the first block matches the requested schema. Fail fast with clear errors (`CLTKException` subclasses) when parsing fails.
- Normalize text with `cltk_normalize` where appropriate, but keep a traceable path back to the raw response when logging is enabled.
- Track token usage by aggregating attempts; keep retry counts bounded and deterministic.

## Logging, telemetry, and retries
- Respect `CLTK_LOG_CONTENT` for logging full prompts/responses; default to redacting contents.
- Log model name, temperature, prompt digest/version, and attempt counts. Avoid logging user text unless explicitly enabled.
- Use bounded retries with backoff when needed; never loop indefinitely. Keep retry logic centralized in the connection classes.

## Testing and CI
- Add unit tests for new prompt builders and parsers. Use small, realistic classical-language fixtures (Latin, Greek, Hebrew, etc.) with diacritics preserved.
- Integration tests that hit external APIs must be skipped when keys are absent (e.g., check `OPENAI_API_KEY`) and should prefer recorded or stubbed responses. Do not make live calls in default CI.
- Ensure pre-commit hooks stay green (ruff, mypy, tests). Favor deterministic assertions; avoid brittle string matches on full model prose.

## Checklist for GenAI pull requests
- [ ] Prompt text lives in `src/cltk/genai/prompts.py` with a version and digest.
- [ ] Outputs are validated and parsed with clear errors; retries are bounded.
- [ ] Logging respects `CLTK_LOG_CONTENT`; sensitive text is not logged by default.
- [ ] Tests cover new prompts/parsers; integration tests are opt-in behind env keys.
- [ ] README/CONTRIBUTING references remain accurate if behavior changed.
- [ ] New dependencies are justified and minimal; defaults remain deterministic.
