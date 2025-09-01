from __future__ import annotations

import importlib
from typing import Any

from cltk.core.data_types import Language
from cltk.languages.glottolog import get_language


class _StubChatGPT:
    def __init__(self, **_: Any) -> None:
        pass

    def generate_all(self, input_doc):  # type: ignore[no-untyped-def]
        return input_doc


def test_chatgpt_process_run_success(monkeypatch):  # type: ignore[no-untyped-def]
    processes = importlib.import_module("cltk.genai.processes")

    # Ensure no ambient API key sneaks in from env unless provided
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(processes, "ChatGPT", _StubChatGPT)

    Doc = importlib.import_module("cltk.core.data_types").Doc
    glottolog_id = "lati1261"
    proc = processes.ChatGPTProcess(glottolog_id=glottolog_id, api_key="test-key")

    lat: Language = get_language(key=glottolog_id)
    doc_in = Doc(raw="Lorem ipsum", language=lat)
    doc_out = proc.run(doc_in)

    assert doc_out is doc_in


def test_chatgpt_process_requires_config(monkeypatch):  # type: ignore[no-untyped-def]
    processes = importlib.import_module("cltk.genai.processes")

    # No API key configured anywhere
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    Doc = importlib.import_module("cltk.core.data_types").Doc
    glottolog_id = "lati1261"
    proc = processes.ChatGPTProcess(glottolog_id=glottolog_id)

    lat: Language = get_language(key=glottolog_id)
    doc_in = Doc(raw="Lorem ipsum", language=lat)

    try:
        proc.run(doc_in)
        assert False, "Expected ValueError when chatgpt is not initialized"
    except ValueError:
        pass
