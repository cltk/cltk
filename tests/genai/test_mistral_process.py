from __future__ import annotations

import importlib
from typing import Any


def test_mistral_connection_requires_api_key(monkeypatch):  # type: ignore[no-untyped-def]
    # Ensure no ambient API key
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)

    mistral_module = importlib.import_module("cltk.genai.mistral")
    # Prevent reading from a local .env during the test
    monkeypatch.setattr(mistral_module, "load_env_file", lambda: None)
    # Provide a benign Mistral stub so import doesn't error when constructing
    class _MistralStub:  # noqa: D401 - trivial stub
        def __init__(self, **_: Any) -> None:
            """No-op Mistral client stub."""
            pass

    monkeypatch.setattr(mistral_module, "Mistral", _MistralStub)

    try:
        mistral_module.MistralConnection(model="")
        assert False, "Expected ValueError without API key"
    except ValueError:
        pass


def test_mistral_connection_uses_env_api_key(monkeypatch):  # type: ignore[no-untyped-def]
    # Supply API key via environment
    monkeypatch.setenv("MISTRAL_API_KEY", "test-key")

    mistral_module = importlib.import_module("cltk.genai.mistral")

    created = {}

    class _MistralRecorder:
        def __init__(self, **kwargs: Any) -> None:  # noqa: D401 - trivial stub
            created.update(kwargs)

    monkeypatch.setattr(mistral_module, "Mistral", _MistralRecorder)
    conn = mistral_module.MistralConnection(model="")
    assert conn is not None
    assert created.get("api_key") == "test-key"


def test_extract_code_blocks(monkeypatch):  # type: ignore[no-untyped-def]
    mistral_module = importlib.import_module("cltk.genai.mistral")

    class _MistralStub:
        def __init__(self, **_: Any) -> None:  # noqa: D401 - trivial stub
            pass

    monkeypatch.setattr(mistral_module, "Mistral", _MistralStub)
    conn = mistral_module.MistralConnection(model="", api_key="dummy")

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
