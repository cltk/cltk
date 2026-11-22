import importlib
from typing import Any


def test_openai_connection_requires_api_key(monkeypatch):  # type: ignore[no-untyped-def]
    # Ensure no ambient API key
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    openai_mod = importlib.import_module("cltk.genai.openai")
    # Prevent reading from a local .env during the test
    monkeypatch.setattr(openai_mod, "load_env_file", lambda: None)

    # Provide a benign OpenAI stub so import doesn't error when constructing
    class _OpenAIStub:  # noqa: D401 - trivial stub
        def __init__(self, **_: Any) -> None:
            """No-op OpenAI client stub."""
            pass

    monkeypatch.setattr(openai_mod, "OpenAI", _OpenAIStub)

    try:
        openai_mod.OpenAIConnection(model="gpt-5-mini")
        assert False, "Expected ValueError without API key"
    except ValueError:
        pass


def test_openai_connection_uses_env_api_key(monkeypatch):  # type: ignore[no-untyped-def]
    # Supply API key via environment
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    openai_mod = importlib.import_module("cltk.genai.openai")

    created = {}

    class _OpenAIRecorder:
        def __init__(self, **kwargs: Any) -> None:  # noqa: D401 - trivial stub
            created.update(kwargs)

    monkeypatch.setattr(openai_mod, "OpenAI", _OpenAIRecorder)
    conn = openai_mod.OpenAIConnection(model="gpt-5-mini")
    assert conn is not None
    assert created.get("api_key") == "test-key"


def test_extract_code_blocks(monkeypatch):  # type: ignore[no-untyped-def]
    openai_mod = importlib.import_module("cltk.genai.openai")

    class _OpenAIStub:
        def __init__(self, **_: Any) -> None:  # noqa: D401 - trivial stub
            pass

    monkeypatch.setattr(openai_mod, "OpenAI", _OpenAIStub)
    conn = openai_mod.OpenAIConnection(model="gpt-5-mini", api_key="dummy")

    text = """
Here is some response.

```tsv
FORM	LEMMA	UPOS	FEATS
Lorem	lorem	NOUN	Case=Nom|Number=Sing
```

Some trailing commentary.
"""
    block = conn._extract_code_blocks(text)
    assert block.startswith("FORM\tLEMMA\tUPOS\tFEATS")


def test_openai_default_and_explicit_model(monkeypatch):  # type: ignore[no-untyped-def]
    """Use the supported default without overriding callers' explicit models."""
    from cltk import NLP

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    default = NLP("lati1261", backend="openai", suppress_banner=True)
    explicit = NLP(
        "lati1261", backend="openai", model="gpt-5-mini", suppress_banner=True
    )

    assert default.model == "gpt-6.1-terra"
    assert explicit.model == "gpt-5-mini"


def test_openai_reasoning_models_use_responses(monkeypatch):  # type: ignore[no-untyped-def]
    """Keep the same request options in sync and async for GPT-5 and GPT-6."""
    import asyncio
    from types import SimpleNamespace
    from unittest.mock import AsyncMock, Mock

    openai_mod = importlib.import_module("cltk.genai.openai")
    fake_response = SimpleNamespace(
        output_text="```tsv\nFORM\tLEMMA\namō\tamō\n```", usage=None
    )
    for model in ("gpt-5-mini", "gpt-6.1-terra", "gpt-6.1-sol"):
        create = Mock(return_value=fake_response)
        create_async = AsyncMock(return_value=fake_response)
        monkeypatch.setattr(
            openai_mod,
            "OpenAI",
            lambda **_: SimpleNamespace(responses=SimpleNamespace(create=create)),
        )
        monkeypatch.setattr(
            openai_mod,
            "AsyncOpenAI",
            lambda **_: SimpleNamespace(responses=SimpleNamespace(create=create_async)),
        )
        prompt = "Annotate the Latin form amō."
        sync = openai_mod.OpenAIConnection(model=model, api_key="test-key")
        async_conn = openai_mod.AsyncOpenAIConnection(model=model, api_key="test-key")

        assert sync.generate(prompt).response == fake_response.output_text
        assert (
            asyncio.run(async_conn.generate_async(prompt)).response
            == fake_response.output_text
        )
        request = {
            "model": model,
            "input": prompt,
            "reasoning": {"effort": "low"},
            "text": {"verbosity": "low"},
        }
        create.assert_called_once_with(**request)
        create_async.assert_awaited_once_with(**request)
