import asyncio
import importlib
import os
from types import SimpleNamespace
from typing import Any

import httpx
import openai
import pytest

from cltk import NLP
from cltk.core.data_types import CLTKConfig, LiteLLMBackendConfig
from cltk.core.exceptions import CLTKException, OpenAIInferenceError


def test_litellm_connection_uses_proxy_configuration(monkeypatch):  # type: ignore[no-untyped-def]
    module = importlib.import_module("cltk.genai.openai")
    created: dict[str, Any] = {}

    class OpenAIRecorder:
        def __init__(self, **kwargs: Any) -> None:
            created.update(kwargs)
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **_: SimpleNamespace(
                        choices=[
                            SimpleNamespace(
                                message=SimpleNamespace(
                                    content="```tsv\nFORM\tLEMMA\namo\tamo\n```"
                                )
                            )
                        ],
                        usage=SimpleNamespace(
                            prompt_tokens=2, completion_tokens=3, total_tokens=5
                        ),
                    )
                )
            )

    monkeypatch.setattr(module, "OpenAI", OpenAIRecorder)
    connection = module.LiteLLMConnection(
        model="proxy-latin", api_key="sk-test", base_url="http://proxy.test/v1/"
    )

    result = connection.generate("annotate amo", max_retries=1)

    assert created == {
        "api_key": "sk-test",
        "base_url": "http://proxy.test/v1",
    }
    assert result.usage == {"input": 2, "output": 3, "total": 5}
    assert "FORM" in result.response


def test_litellm_connection_requires_key(monkeypatch):  # type: ignore[no-untyped-def]
    module = importlib.import_module("cltk.genai.openai")
    monkeypatch.delenv("LITELLM_API_KEY", raising=False)

    with pytest.raises(ValueError, match="LiteLLM API key required"):
        module.LiteLLMConnection(model="proxy-model")


def test_litellm_connection_rejects_empty_model() -> None:
    module = importlib.import_module("cltk.genai.openai")

    with pytest.raises(ValueError, match="model alias cannot be empty"):
        module.LiteLLMConnection(model="  ", api_key="sk-test")


def test_litellm_connection_requires_at_least_one_attempt(monkeypatch):  # type: ignore[no-untyped-def]
    module = importlib.import_module("cltk.genai.openai")

    class OpenAIStub:
        def __init__(self, **_: Any) -> None:
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(create=lambda **_: None)
            )

    monkeypatch.setattr(module, "OpenAI", OpenAIStub)
    connection = module.LiteLLMConnection(model="proxy-model", api_key="sk-test")

    with pytest.raises(ValueError, match="max_retries must be at least 1"):
        connection.generate("annotate amo", max_retries=0)


def test_litellm_connection_retries_malformed_responses(monkeypatch):  # type: ignore[no-untyped-def]
    module = importlib.import_module("cltk.genai.openai")
    calls = 0

    class OpenAIStub:
        def __init__(self, **_: Any) -> None:
            def create(**_: Any) -> SimpleNamespace:
                nonlocal calls
                calls += 1
                return SimpleNamespace(
                    choices=[
                        SimpleNamespace(message=SimpleNamespace(content="not fenced"))
                    ],
                    usage=None,
                )

            self.chat = SimpleNamespace(completions=SimpleNamespace(create=create))

    monkeypatch.setattr(module, "OpenAI", OpenAIStub)
    connection = module.LiteLLMConnection(model="proxy-model", api_key="sk-test")

    with pytest.raises(CLTKException, match="No code blocks found"):
        connection.generate("annotate amo", max_retries=2)
    assert calls == 2


@pytest.mark.parametrize(
    "response",
    [
        SimpleNamespace(choices=[]),
        SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=None))]
        ),
    ],
    ids=["missing-choice", "null-content"],
)
def test_litellm_connection_rejects_empty_responses(monkeypatch, response):  # type: ignore[no-untyped-def]
    module = importlib.import_module("cltk.genai.openai")

    class OpenAIStub:
        def __init__(self, **_: Any) -> None:
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(create=lambda **_: response)
            )

    monkeypatch.setattr(module, "OpenAI", OpenAIStub)
    connection = module.LiteLLMConnection(model="proxy-model", api_key="sk-test")

    with pytest.raises(CLTKException, match="empty or malformed response"):
        connection.generate("annotate amo", max_retries=1)


def test_async_litellm_connection_retries_malformed_responses(monkeypatch):  # type: ignore[no-untyped-def]
    module = importlib.import_module("cltk.genai.openai")
    calls = 0

    class AsyncOpenAIStub:
        def __init__(self, **_: Any) -> None:
            async def create(**_: Any) -> SimpleNamespace:
                nonlocal calls
                calls += 1
                return SimpleNamespace(
                    choices=[
                        SimpleNamespace(message=SimpleNamespace(content="not fenced"))
                    ],
                    usage=None,
                )

            self.chat = SimpleNamespace(completions=SimpleNamespace(create=create))

    monkeypatch.setattr(module, "AsyncOpenAI", AsyncOpenAIStub)
    connection = module.AsyncLiteLLMConnection(model="proxy-model", api_key="sk-test")

    async def run() -> None:
        with pytest.raises(CLTKException, match="No code blocks found"):
            await connection.generate_async("annotate amo", max_retries=2)

    asyncio.run(run())
    assert calls == 2


def _status_error(
    error_type: type[openai.APIStatusError], status: int
) -> openai.APIStatusError:
    request = httpx.Request("POST", "http://proxy.test/v1/responses")
    response = httpx.Response(status, request=request)
    return error_type(
        "gateway rejected request",
        response=response,
        body={"error": {"message": "gateway rejected request"}},
    )


@pytest.mark.parametrize(
    "sdk_error",
    [
        pytest.param(
            _status_error(openai.AuthenticationError, 401), id="invalid-api-key"
        ),
        pytest.param(_status_error(openai.NotFoundError, 404), id="model-not-found"),
        pytest.param(_status_error(openai.RateLimitError, 429), id="rate-limit"),
        pytest.param(
            _status_error(openai.BadRequestError, 400), id="context-window-exceeded"
        ),
        pytest.param(
            openai.APITimeoutError(
                request=httpx.Request("POST", "http://proxy.test/v1/responses")
            ),
            id="timeout",
        ),
    ],
)
def test_litellm_connection_wraps_sdk_errors(monkeypatch, sdk_error):  # type: ignore[no-untyped-def]
    module = importlib.import_module("cltk.genai.openai")

    class OpenAIStub:
        def __init__(self, **_: Any) -> None:
            def create(**_: Any) -> None:
                raise sdk_error

            self.chat = SimpleNamespace(completions=SimpleNamespace(create=create))

    monkeypatch.setattr(module, "OpenAI", OpenAIStub)
    connection = module.LiteLLMConnection(model="proxy-model", api_key="sk-test")

    with pytest.raises(OpenAIInferenceError, match="An error from OpenAI occurred"):
        connection.generate("annotate amo", max_retries=1)


def test_litellm_backend_config_is_selected() -> None:
    config = CLTKConfig(
        language_code="lati1261",
        backend="litellm",
        litellm=LiteLLMBackendConfig(
            model="proxy-latin",
            api_key="sk-test",
            base_url="https://proxy.test/v1",
        ),
    )

    assert config.active_backend_config is config.litellm
    assert config.litellm is not None
    assert config.litellm.model == "proxy-latin"


def test_nlp_initializes_litellm_backend() -> None:
    config = CLTKConfig(
        language_code="lati1261",
        backend="litellm",
        suppress_banner=True,
        litellm=LiteLLMBackendConfig(model="proxy-latin", api_key="sk-test"),
    )

    nlp = NLP(cltk_config=config)

    assert nlp.backend == "litellm"
    assert nlp.model == "proxy-latin"
    assert nlp.pipeline is not None


@pytest.mark.skipif(
    not all(
        os.environ.get(name)
        for name in (
            "LITELLM_E2E_BASE_URL",
            "LITELLM_E2E_API_KEY",
            "LITELLM_E2E_MODEL",
        )
    ),
    reason="LiteLLM live E2E environment is not configured",
)
def test_litellm_live_e2e() -> None:
    module = importlib.import_module("cltk.genai.openai")
    connection = module.LiteLLMConnection(
        model=os.environ["LITELLM_E2E_MODEL"],
        api_key=os.environ["LITELLM_E2E_API_KEY"],
        base_url=os.environ["LITELLM_E2E_BASE_URL"],
        temperature=0,
    )

    result = connection.generate(
        "Return exactly this fenced block: ```text\nOK\n```", max_retries=1
    )

    assert "OK" in result.response
