"""Ollama integration for CLTK.

This module provides a thin client around the local Ollama server for
generating text responses used by CLTK's generative pipelines. It mirrors the
shape of the OpenAI integration so higher layers can switch based on
``doc.backend``.

Usage requires the optional dependency group ``cltk[ollama]`` alongside either
a running local Ollama server (default host ``http://127.0.0.1:11434``) or an
Ollama Cloud API key.
"""

from __future__ import annotations

import os
from typing import Any, Optional

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import CLTKGenAIResponse
from cltk.core.exceptions import CLTKException
from cltk.utils.utils import load_env_file

OLLAMA_HOST_ENV = "OLLAMA_HOST"
OLLAMA_INSTALL_HINT = (
    "Ollama client not installed. Install with: pip install 'cltk[ollama]'"
)
HTTPX_INCOMPAT_HINT = "Ollama client is incompatible with httpx>=0.29. Install a supported version via: pip install 'httpx<0.29'."


def _default_host() -> str:
    host = os.environ.get(OLLAMA_HOST_ENV)
    if host:
        return host
    # Fallback to local default
    return "http://127.0.0.1:11434"


def _usage_from_result(res: Any) -> dict[str, int]:
    """Best-effort token usage extraction from Ollama response.

    Ollama responses commonly include ``eval_count`` and ``prompt_eval_count``.
    When absent, zeros are returned.
    """
    usage = {"input": 0, "output": 0, "total": 0}
    try:
        inp = int(
            getattr(res, "prompt_eval_count", 0) or res.get("prompt_eval_count", 0)
        )
    except Exception:
        inp = 0
    try:
        out = int(getattr(res, "eval_count", 0) or res.get("eval_count", 0))
    except Exception:
        out = 0
    usage["input"] = max(inp, 0)
    usage["output"] = max(out, 0)
    usage["total"] = usage["input"] + usage["output"]
    return usage


def _bearer(token: str) -> str:
    t = token.strip()
    return t if t.lower().startswith("bearer ") else f"Bearer {t}"


class OllamaConnection:
    """Thin wrapper around the Ollama client for CLTK use cases (sync).

    Args:
      model: Ollama model name (e.g., ``"llama3.1:8b"``). Any string accepted.
      host: Optional Ollama host URL. Defaults to ``$OLLAMA_HOST`` or
        ``http://127.0.0.1:11434``.
      use_cloud: When true, use the hosted Ollama Cloud endpoint.
      api_key: Optional explicit API key for the hosted endpoint.

    """

    def __init__(
        self,
        model: str,
        host: Optional[str] = None,
        *,
        use_cloud: bool = False,
        api_key: Optional[str] = None,
    ) -> None:
        self.model = model
        self.use_cloud = use_cloud
        self.log = bind_context(model=model)
        self.host = host or ("https://ollama.com" if use_cloud else _default_host())
        self.api_key = api_key
        headers: Optional[dict[str, str]] = None
        if self.use_cloud:
            load_env_file()
            self.api_key = self.api_key or os.environ.get("OLLAMA_CLOUD_API_KEY")
            if not self.api_key:
                raise ImportError(
                    "Ollama Cloud API key not found. Set OLLAMA_CLOUD_API_KEY in your environment."
                )
            headers = {"Authorization": _bearer(self.api_key)}
        self._client: Any
        try:
            from ollama import Client as _Client
        except Exception as e:  # pragma: no cover - optional dep
            raise ImportError(OLLAMA_INSTALL_HINT) from e

        try:
            if headers:
                self._client = _Client(host=self.host, headers=headers)
            else:
                self._client = _Client(host=self.host)
        except TypeError as e:
            if "base_url" in str(e):
                httpx_version = "unknown"
                try:  # pragma: no cover - optional dep
                    import httpx

                    httpx_version = getattr(httpx, "__version__", httpx_version)
                except Exception:
                    pass
                raise ImportError(
                    f"{HTTPX_INCOMPAT_HINT} Detected httpx {httpx_version}."
                ) from e
            raise ImportError(OLLAMA_INSTALL_HINT) from e
        except Exception as e:  # pragma: no cover - optional dep
            raise ImportError(OLLAMA_INSTALL_HINT) from e

    def _pull_if_needed(self) -> None:
        """Attempt to pull model if missing.

        We optimistically try ``show`` to check presence; if unavailable or
        raises, we call ``pull``.
        """
        if self.use_cloud:
            return
        try:
            # Some client versions expose ``show(model=...)``
            show = getattr(self._client, "show", None)
            if callable(show):
                try:
                    show(model=self.model)
                    return
                except Exception:
                    pass
            # Fallback to always pull (idempotent when already present)
            self.log.info("Pulling Ollama model '%s' (if not present)...", self.model)
            self._client.pull(self.model, stream=False)
        except Exception:
            # Do not fail here; generate() will raise if still unavailable
            self.log.warning("Could not verify/pull model '%s' via Ollama.", self.model)

    def generate(self, prompt: str, *, max_retries: int = 2) -> CLTKGenAIResponse:
        # Avoid logging prompt contents unless explicitly enabled
        if os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug("[ollama] Prompt being sent to Ollama:\n%s", prompt)
        # Ensure model is present (best-effort)
        self._pull_if_needed()
        last_err: Optional[Exception] = None
        for attempt in range(1, max_retries + 1):
            self.log.debug("[ollama] Attempt %s of %s", attempt, max_retries)
            try:
                res: dict[str, Any] = self._client.generate(
                    model=self.model, prompt=prompt
                )
                text: str = str(res.get("response", ""))
                usage = _usage_from_result(res)
                if not text.strip():
                    raise CLTKException("Empty response from Ollama.")
                return CLTKGenAIResponse(response=text, usage=usage)
            except Exception as e:
                last_err = e
                self.log.error("[ollama] Error on attempt %s: %s", attempt, e)
        assert last_err is not None
        raise CLTKException(f"Ollama generation failed after retries: {last_err}")


class AsyncOllamaConnection:
    """Async wrapper around the Ollama client for CLTK use cases."""

    def __init__(
        self,
        model: str,
        host: Optional[str] = None,
        *,
        use_cloud: bool = False,
        api_key: Optional[str] = None,
    ) -> None:
        self.model = model
        self.use_cloud = use_cloud
        self.log = bind_context(model=model)
        self.host = host or ("https://ollama.com" if use_cloud else _default_host())
        self.api_key = api_key
        headers: Optional[dict[str, str]] = None
        if self.use_cloud:
            load_env_file()
            self.api_key = self.api_key or os.environ.get("OLLAMA_CLOUD_API_KEY")
            if not self.api_key:
                raise ImportError(
                    "Ollama Cloud API key not found. Set OLLAMA_CLOUD_API_KEY in your environment."
                )
            headers = {"Authorization": _bearer(self.api_key)}
        self._client: Any
        try:
            from ollama import AsyncClient as _AsyncClient
        except Exception as e:  # pragma: no cover - optional dep
            raise ImportError(OLLAMA_INSTALL_HINT) from e

        try:
            if headers:
                self._client = _AsyncClient(host=self.host, headers=headers)
            else:
                self._client = _AsyncClient(host=self.host)
        except TypeError as e:
            if "base_url" in str(e):
                httpx_version = "unknown"
                try:  # pragma: no cover - optional dep
                    import httpx

                    httpx_version = getattr(httpx, "__version__", httpx_version)
                except Exception:
                    pass
                raise ImportError(
                    f"{HTTPX_INCOMPAT_HINT} Detected httpx {httpx_version}."
                ) from e
            raise ImportError(OLLAMA_INSTALL_HINT) from e
        except Exception as e:  # pragma: no cover - optional dep
            raise ImportError(OLLAMA_INSTALL_HINT) from e

    async def _pull_if_needed(self) -> None:
        if self.use_cloud:
            return
        try:
            show = getattr(self._client, "show", None)
            if callable(show):
                try:
                    await show(model=self.model)
                    return
                except Exception:
                    pass
            self.log.info("Pulling Ollama model '%s' (if not present)...", self.model)
            pull = getattr(self._client, "pull", None)
            if callable(pull):
                await pull(self.model, stream=False)
        except Exception:
            self.log.warning("Could not verify/pull model '%s' via Ollama.", self.model)

    async def generate_async(
        self, *, prompt: str, max_retries: int = 2
    ) -> CLTKGenAIResponse:
        if os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug("[async-ollama] Prompt being sent to Ollama:\n%s", prompt)
        await self._pull_if_needed()
        last_err: Optional[Exception] = None
        for attempt in range(1, max_retries + 1):
            self.log.debug("[async-ollama] Attempt %s of %s", attempt, max_retries)
            try:
                res: dict[str, Any] = await self._client.generate(
                    model=self.model, prompt=prompt
                )
                text: str = str(res.get("response", ""))
                usage = _usage_from_result(res)
                if not text.strip():
                    raise CLTKException("Empty response from Ollama.")
                return CLTKGenAIResponse(response=text, usage=usage)
            except Exception as e:
                last_err = e
                self.log.error("[async-ollama] Error on attempt %s: %s", attempt, e)
        assert last_err is not None
        raise CLTKException(
            f"[async-ollama] Ollama generation failed after retries: {last_err}"
        )


# Suggested models (not enforced; any Ollama model string is accepted)
SUGGESTED_OLLAMA_MODELS: list[str] = [
    # Qwen 2.5 family
    "qwen2.5:7b",
    "qwen2.5:14b",
    "qwen2.5:72b",
    # LLaMA 3.1 family
    "llama3.1:8b",
    "llama3.1:70b",
    "llama3.1:405b",
    # Gemma 2 family
    "gemma2:9b",
    "gemma2:27b",
    # OpenAI family
    "gpt-oss:20b",
    "gpt-oss:120b",
    # DeepSeek
    "deepseek-r13:8b",
]
