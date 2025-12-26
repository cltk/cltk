import importlib.util
import os
from typing import Callable

import pytest

from cltk import NLP
from cltk.core.data_types import BACKEND_TYPES, CLTKGenAIResponse
from cltk.utils.utils import load_env_file

load_env_file()

pytestmark = pytest.mark.integration

PROMPT = "Return ONLY a fenced code block containing the exact text: Amor Vincit Omnia."
TEXT = "amor vincit omnia"


def _require_env(var_name: str | None) -> None:
    if not var_name:
        return
    if not os.getenv(var_name):
        pytest.skip(f"Missing {var_name}; skipping live API test.")


def _require_module(module_name: str) -> None:
    if importlib.util.find_spec(module_name) is None:
        pytest.skip(f"Missing optional dependency {module_name}.")


def _run_openai() -> CLTKGenAIResponse:
    from cltk.genai.openai import OpenAIConnection

    conn = OpenAIConnection(model="gpt-5-mini")
    return conn.generate(prompt=PROMPT, max_retries=1)


def _run_mistral() -> CLTKGenAIResponse:
    from cltk.genai.mistral import MistralConnection

    conn = MistralConnection(model="mistral-medium-latest")
    return conn.generate(prompt=PROMPT, max_retries=1)


# def _run_ollama_cloud() -> CLTKGenAIResponse:
#     from cltk.genai.ollama import OllamaConnection

#     conn = OllamaConnection(model="llama3.1:8b", use_cloud=True)
#     return conn.generate(prompt=PROMPT, max_retries=1)


def _run_ollama_local() -> CLTKGenAIResponse:
    from cltk.genai.ollama import OllamaConnection

    conn = OllamaConnection(model="llama3.1:8b")
    return conn.generate(prompt=PROMPT, max_retries=1)


@pytest.mark.parametrize(
    ("name", "env_var", "module_name", "runner"),
    [
        ("openai", "OPENAI_API_KEY", "openai", _run_openai),
        ("mistral", "MISTRAL_API_KEY", "mistralai", _run_mistral),
        # ("ollama-cloud", "OLLAMA_CLOUD_API_KEY", "ollama", _run_ollama_cloud),
        ("ollama-local", None, "ollama", _run_ollama_local),
    ],
)
def test_live_api_tokens(
    name: str,
    env_var: str | None,
    module_name: str,
    runner: Callable[[], CLTKGenAIResponse],
) -> None:
    _require_env(env_var)
    _require_module(module_name)
    response = runner()
    assert "amor vincit omnia" in response.response.lower(), f"{name} missing phrase"


def _run_nlp_backend(backend: BACKEND_TYPES) -> None:
    nlp = NLP(language_code="lati1261", backend=backend, suppress_banner=True)
    doc = nlp.analyze(TEXT)
    assert doc.words, f"{backend} returned no tokens"
    assert any(w.string for w in doc.words), f"{backend} returned empty tokens"


@pytest.mark.parametrize(
    ("name", "env_var", "module_name", "backend"),
    [
        ("openai", "OPENAI_API_KEY", "openai", "openai"),
        ("mistral", "MISTRAL_API_KEY", "mistralai", "mistral"),
        # ("ollama-cloud", "OLLAMA_CLOUD_API_KEY", "ollama", "ollama-cloud"),
        ("ollama-local", None, "ollama", "ollama"),
    ],
)
def test_live_nlp_backends(
    name: str,
    env_var: str | None,
    module_name: str,
    backend: BACKEND_TYPES,
) -> None:
    _require_env(env_var)
    _require_module(module_name)
    _run_nlp_backend(backend)
