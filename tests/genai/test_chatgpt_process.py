from __future__ import annotations

import importlib
from typing import Any


def test_gpt_process_types_exist() -> None:
    processes = importlib.import_module("cltk.genai.processes")
    assert hasattr(processes, "GPTProcess")
    assert hasattr(processes, "LocalGPTProcess")


def test_chatgpt_connection_requires_api_key(monkeypatch):  # type: ignore[no-untyped-def]
    # Ensure no ambient API key
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    chatgpt_mod = importlib.import_module("cltk.genai.chatgpt")
    # Prevent reading from a local .env during the test
    monkeypatch.setattr(chatgpt_mod, "load_env_file", lambda: None)
    # Provide a benign OpenAI stub so import doesn't error when constructing
    class _OpenAIStub:  # noqa: D401 - trivial stub
        def __init__(self, **_: Any) -> None:
            """No-op OpenAI client stub."""
            pass

    monkeypatch.setattr(chatgpt_mod, "OpenAI", _OpenAIStub)

    try:
        chatgpt_mod.ChatGPTConnection(model="gpt-5-mini")
        assert False, "Expected ValueError without API key"
    except ValueError:
        pass


def test_chatgpt_connection_uses_env_api_key(monkeypatch):  # type: ignore[no-untyped-def]
    # Supply API key via environment
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    chatgpt_mod = importlib.import_module("cltk.genai.chatgpt")

    created = {}

    class _OpenAIRecorder:
        def __init__(self, **kwargs: Any) -> None:  # noqa: D401 - trivial stub
            created.update(kwargs)

    monkeypatch.setattr(chatgpt_mod, "OpenAI", _OpenAIRecorder)
    conn = chatgpt_mod.ChatGPTConnection(model="gpt-5-mini")
    assert conn is not None
    assert created.get("api_key") == "test-key"


def test_extract_code_blocks(monkeypatch):  # type: ignore[no-untyped-def]
    chatgpt_mod = importlib.import_module("cltk.genai.chatgpt")

    class _OpenAIStub:
        def __init__(self, **_: Any) -> None:  # noqa: D401 - trivial stub
            pass

    monkeypatch.setattr(chatgpt_mod, "OpenAI", _OpenAIStub)
    conn = chatgpt_mod.ChatGPTConnection(model="gpt-5-mini", api_key="dummy")

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
