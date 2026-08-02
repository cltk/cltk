"""OpenAI integration for CLTK.

# Internal; no stability guarantees

This module provides a small wrapper class (:class:`OpenAIConnection`) around the
OpenAI client and high‑level helpers to generate linguistic annotations from
LLMs for a given language (resolved by Glottolog ID).
"""

__license__ = "MIT License. See LICENSE."

# NOTE: Keep OpenAI/LLM behavior aligned with LLM_DEV_GUIDE.md (prompts,
# logging, retries, and safety).

import os
import re
from types import SimpleNamespace
from typing import Any, Optional, cast

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import AVAILABLE_OPENAI_MODELS, CLTKGenAIResponse
from cltk.core.exceptions import CLTKException, OpenAIInferenceError
from cltk.text.utils import cltk_normalize
from cltk.utils.utils import load_env_file


class _OpenAIErrorFallback(Exception):
    """Fallback error raised when the OpenAI SDK is unavailable."""


def _resolve_openai_classes() -> (
    tuple[Optional[type[Any]], Optional[type[Any]], type[BaseException]]
):
    """Import OpenAI client classes lazily, tolerating missing optional deps."""
    sync_cls: Optional[type[Any]]
    async_cls: Optional[type[Any]]
    error_cls: type[BaseException]

    try:
        from openai import OpenAI as imported_sync
    except Exception:  # pragma: no cover - optional dependency
        sync_cls = None
    else:
        sync_cls = imported_sync

    try:
        from openai import AsyncOpenAI as imported_async
    except Exception:  # pragma: no cover - optional dependency
        async_cls = None
    else:
        async_cls = imported_async

    try:
        from openai import OpenAIError as imported_error
    except Exception:  # pragma: no cover - optional dependency
        error_cls = _OpenAIErrorFallback
    else:
        error_cls = imported_error

    return sync_cls, async_cls, error_cls


OpenAI, AsyncOpenAI, OpenAIError = _resolve_openai_classes()


def _litellm_output_text(response: Any) -> str:
    """Extract non-empty text from an OpenAI-compatible chat response."""
    try:
        content = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError) as error:
        raise CLTKException(
            "LiteLLM returned an empty or malformed response."
        ) from error
    if not isinstance(content, str) or not content.strip():
        raise CLTKException("LiteLLM returned an empty or malformed response.")
    return content


class OpenAIConnection:
    """Thin wrapper around the OpenAI client for CLTK use cases.

    Args:
      api_key: OpenAI API key.
      model: Small set of supported model aliases.
      temperature: Sampling temperature (default 1.0).

    Attributes:
      client: OpenAI client instance.

    """

    def __init__(
        self,
        model: AVAILABLE_OPENAI_MODELS,
        api_key: Optional[str] = None,
        temperature: float = 1.0,
        _base_url: Optional[str] = None,
    ):
        """Initialize the client and resolve language/dialect metadata."""
        self.api_key = api_key
        self.model: str = model
        self.temperature: float = temperature
        if not self.api_key:
            load_env_file()
            self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            msg: str = "OPENAI_API_KEY not found. Please set it in your environment or in a .env file."
            # Bind with model context even before self.log is available
            bind_context(model=str(model)).error(msg)
            raise ValueError(msg)
        # Use patched OpenAI if provided by tests; else import lazily
        openai_cls = OpenAI
        if openai_cls is None:  # pragma: no cover - import only if needed
            try:
                from openai import OpenAI as runtime_openai
            except Exception as e:
                raise ImportError(
                    "OpenAI client not installed. Install with: pip install 'cltk[openai]'"
                ) from e
            openai_cls = runtime_openai
        client_kwargs: dict[str, Any] = {"api_key": self.api_key}
        if _base_url:
            client_kwargs["base_url"] = _base_url.rstrip("/")
        self.client = openai_cls(**client_kwargs)
        self._is_litellm = _base_url is not None
        # Structured logger bound with model identifier
        self.log = bind_context(model=str(self.model))

    def generate(
        self,
        prompt: str,
        max_retries: int = 2,
    ) -> CLTKGenAIResponse:
        """Generate text through OpenAI Responses or LiteLLM Chat Completions."""
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1")
        # Avoid logging full prompt contents unless explicitly enabled
        import os as _os

        if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug(prompt)
        code_block: Optional[str] = None
        openai_response: Optional[Any] = None
        attempt: Optional[int] = None
        # Accumulate tokens across attempts (including failed ones)
        agg_tokens: dict[str, int] = {"input": 0, "output": 0, "total": 0}
        for attempt in range(1, max_retries + 1):
            self.log.debug(f"Attempt {attempt} of {max_retries}")
            try:
                # TODO: Disable 4.1
                if self._is_litellm:
                    chat_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=self.temperature,
                    )
                    content = _litellm_output_text(chat_response)
                    openai_response = SimpleNamespace(
                        output_text=content, usage=chat_response.usage
                    )
                elif "4.1" in self.model:
                    openai_response = self.client.responses.create(
                        model=self.model, input=prompt, temperature=self.temperature
                    )
                elif "-5" in self.model:
                    openai_response = self.client.responses.create(
                        model=self.model,
                        input=prompt,
                        # TODO: Add params for these
                        reasoning={"effort": "low"},
                        text={"verbosity": "low"},
                    )
                else:
                    raise ValueError(f"Unsupported model: {self.model}.")
            except OpenAIError as openai_error:
                raise OpenAIInferenceError(
                    f"An error from OpenAI occurred: {openai_error}"
                )
            if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
                "1",
                "true",
                "yes",
                "on",
            }:
                self.log.debug(
                    f"Raw response from OpenAI: {openai_response.output_text}"
                )
            # Add usage from this attempt even if parsing fails
            try:
                tok = self._openai_response_tokens(openai_response)
                for k in ("input", "output", "total"):
                    agg_tokens[k] += tok.get(k, 0)
            except Exception:
                pass
            try:
                code_block = self._extract_code_blocks(text=openai_response.output_text)
            except Exception as e:
                # TODO: Count tokens used for failed attempts, too
                self.log.error(f"Error extracting code block: {e}")
                continue
            if code_block:
                break  # Success, exit retry loop
            else:
                self.log.warning(
                    f"Attempt {attempt}: No code block found in OpenAI response. Retrying..."
                )
                if attempt == max_retries:
                    final_err = "No code blocks found in OpenAI response after retries."
                    self.log.error(final_err)
                    # logger.error(raw_openai_response_normalized)
                    raise CLTKException(final_err)
                    # return doc
                # Optionally, you could modify the prompt or add a delay here

        if not code_block:
            raise CLTKException("No code blocks found in response after retries.")
        assert openai_response
        # Use the accumulated usage across all attempts
        openai_usage: dict[str, int] = agg_tokens
        raw_openai_response_normalized: str = cltk_normalize(
            text=openai_response.output_text
        )
        if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug(
                f"raw_openai_response_normalized:\n{raw_openai_response_normalized}"
            )
        self.log.debug(f"Completed generation() after {attempt} attempts")
        # return {"response": raw_openai_response_normalized, "usage": openai_usage}
        return CLTKGenAIResponse(
            response=raw_openai_response_normalized, usage=openai_usage
        )
        # logger.error(f"Exceeded maximum retries: {max_retries}")
        # raise RuntimeError("Failed to generate response after multiple attempts.")

    def _openai_response_tokens(self, response: Any) -> dict[str, int]:
        """Extract token usage information from an OpenAI response.

        Args:
          model: Model alias used for the call.
          response: OpenAI response object.

        Returns:
          A dict with ``input``, ``output``, and ``total`` token counts (0 if
          unavailable).

        """
        usage = getattr(response, "usage", None)
        tokens: dict[str, int] = {"input": 0, "output": 0, "total": 0}
        if not usage:
            self.log.warning(
                "No usage information found in response. Tokens used may not be available."
            )
            self.log.info(f"OpenAI usage: {tokens}")
            return tokens

        # Normalize key names across OpenAI endpoints
        def _get(u: object, *names: str) -> int:
            """Attempt to read an integer field from a response usage object."""
            for nm in names:
                if hasattr(u, nm):
                    try:
                        return int(getattr(u, nm) or 0)
                    except Exception:
                        pass
                if isinstance(u, dict):
                    ud = cast(dict[str, Any], u)
                    if nm in ud:
                        try:
                            return int(ud.get(nm) or 0)
                        except Exception:
                            pass
            return 0

        tokens["input"] = _get(
            usage, "input_tokens", "prompt_tokens", "prompt_token_count"
        )
        tokens["output"] = _get(
            usage, "output_tokens", "completion_tokens", "completion_token_count"
        )
        tokens["total"] = _get(usage, "total_tokens", "total_token_count")

        if tokens["total"] == 0:
            self.log.warning(
                "No tokens used reported in response. This may indicate an issue with the API call."
            )
        self.log.info(f"OpenAI usage: {tokens}")
        return tokens

    def _extract_code_blocks(self, text: str) -> str:
        """Return the first fenced code block from an OpenAI response string."""
        # This regex finds all text between triple backticks
        code_blocks: list[str] = re.findall(
            r"```(?:[a-zA-Z]*\n)?(.*?)```", text, re.DOTALL
        )
        code_block: str = code_blocks[0].strip()
        import os as _os

        if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug(f"Extracted code block:\n{code_block}")
        return code_block


class AsyncOpenAIConnection:
    """Asynchronous variant of :class:`OpenAIConnection`.

    Provides an ``async`` ``generate_async()`` method and uses the
    ``AsyncOpenAI`` client under the hood. Mirrors the behavior and logging of
    the synchronous client while enabling concurrent requests.

    Args:
      model: Model alias to use (see ``AVAILABLE_OPENAI_MODELS``).
      api_key: Optional OpenAI API key. Falls back to ``OPENAI_API_KEY``.
      temperature: Sampling temperature for generation.

    """

    def __init__(
        self,
        model: AVAILABLE_OPENAI_MODELS,
        api_key: Optional[str] = None,
        temperature: float = 1.0,
        _base_url: Optional[str] = None,
    ) -> None:
        self.api_key = api_key
        self.model: str = model
        self.temperature: float = temperature
        if not self.api_key:
            load_env_file()
            self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            msg: str = "OPENAI_API_KEY not found. Please set it in your environment or in a .env file."
            bind_context(model=str(model)).error(msg)
            raise ValueError(msg)
        async_openai_cls = AsyncOpenAI
        if async_openai_cls is None:  # pragma: no cover - import only if needed
            try:
                from openai import AsyncOpenAI as runtime_async_openai
            except Exception as e:
                raise ImportError(
                    "OpenAI client not installed. Install with: pip install 'cltk[openai]'"
                ) from e
            async_openai_cls = runtime_async_openai
        client_kwargs: dict[str, Any] = {"api_key": self.api_key}
        if _base_url:
            client_kwargs["base_url"] = _base_url.rstrip("/")
        self.client = async_openai_cls(**client_kwargs)
        self._is_litellm = _base_url is not None
        # Structured logger bound with model identifier
        self.log = bind_context(model=str(self.model))

    async def generate_async(
        self,
        prompt: str,
        max_retries: int = 2,
    ) -> CLTKGenAIResponse:
        """Generate text asynchronously through OpenAI or LiteLLM."""
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1")
        import os as _os

        if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug("[async] Prompt being sent to OpenAI:\n%s", prompt)
        code_block: Optional[str] = None
        openai_response: Optional[Any] = None
        agg_tokens: dict[str, int] = {"input": 0, "output": 0, "total": 0}
        for attempt in range(1, max_retries + 1):
            self.log.debug("[async] Attempt %s of %s", attempt, max_retries)
            try:
                if self._is_litellm:
                    chat_response = await self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=self.temperature,
                    )
                    content = _litellm_output_text(chat_response)
                    openai_response = SimpleNamespace(
                        output_text=content, usage=chat_response.usage
                    )
                elif "4.1" in self.model:
                    openai_response = await self.client.responses.create(
                        model=self.model,
                        input=prompt,
                        temperature=self.temperature,
                    )
                elif "-5" in self.model:
                    openai_response = await self.client.responses.create(
                        model=self.model,
                        input=prompt,
                        reasoning={"effort": "low"},
                        text={"verbosity": "low"},
                    )
                else:
                    raise ValueError(f"Unsupported model: {self.model}.")
            except OpenAIError as openai_error:
                self.log.error(
                    "[async] OpenAI error on attempt %s: %s", attempt, openai_error
                )
                if attempt == max_retries:
                    raise OpenAIInferenceError(
                        f"An error from OpenAI occurred: {openai_error}"
                    )
                continue

            self.log.debug(
                "[async] Raw response from OpenAI: %s", openai_response.output_text
            )
            # Track usage for this attempt (even if parsing fails)
            try:
                tok = self._openai_response_tokens(openai_response)
                for k in ("input", "output", "total"):
                    agg_tokens[k] += tok.get(k, 0)
            except Exception:
                pass
            try:
                code_block = self._extract_code_blocks(openai_response.output_text)
            except Exception as e:  # pragma: no cover - defensive
                self.log.error("[async] Error extracting code block: %s", e)
                code_block = None
            if code_block:
                break
            self.log.warning(
                "[async] Attempt %s: No code block found in response. Retrying...",
                attempt,
            )

        if not code_block:
            raise CLTKException("No code blocks found in response after retries.")

        assert openai_response is not None
        usage = agg_tokens
        raw_normalized: str = cltk_normalize(text=openai_response.output_text)
        if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug("[async] Normalized output text:\n%s", raw_normalized)
        return CLTKGenAIResponse(response=raw_normalized, usage=usage)

    def _openai_response_tokens(self, response: Any) -> dict[str, int]:
        """Extract token usage fields from an async OpenAI response."""
        usage = getattr(response, "usage", None)
        tokens: dict[str, int] = {"input": 0, "output": 0, "total": 0}
        if not usage:
            self.log.info("[async] No usage info present; returning zeros")
            return tokens

        def _get(u: object, *names: str) -> int:
            """Attempt to read an integer field from an async response usage object."""
            for nm in names:
                if hasattr(u, nm):
                    try:
                        return int(getattr(u, nm) or 0)
                    except Exception:
                        pass
                if isinstance(u, dict):
                    ud = cast(dict[str, Any], u)
                    if nm in ud:
                        try:
                            return int(ud.get(nm) or 0)
                        except Exception:
                            pass
            return 0

        tokens["input"] = _get(
            usage, "input_tokens", "prompt_tokens", "prompt_token_count"
        )
        tokens["output"] = _get(
            usage, "output_tokens", "completion_tokens", "completion_token_count"
        )
        tokens["total"] = _get(usage, "total_tokens", "total_token_count")
        self.log.info("[async] OpenAI usage: %s", tokens)
        return tokens

    def _extract_code_blocks(self, text: str) -> str:
        """Return the first fenced code block from an async OpenAI response string."""
        code_blocks: list[str] = re.findall(
            r"```(?:[a-zA-Z]*\n)?(.*?)```", text, re.DOTALL
        )
        code_block: str = code_blocks[0].strip()
        import os as _os

        if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug("[async] Extracted code block:\n%s", code_block)
        return code_block


class LiteLLMConnection(OpenAIConnection):
    """Synchronous connection to models exposed by a LiteLLM proxy.

    Uses ``LITELLM_API_KEY`` and defaults ``LITELLM_BASE_URL`` to the local
    LiteLLM proxy. Requests use the provider-neutral Chat Completions endpoint;
    model names are proxy aliases and are not restricted to OpenAI identifiers.
    """

    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 1.0,
    ) -> None:
        model = model.strip()
        if not model:
            raise ValueError("LiteLLM model alias cannot be empty.")
        resolved_key = api_key or os.environ.get("LITELLM_API_KEY")
        if not resolved_key:
            raise ValueError(
                "LiteLLM API key required. Set LITELLM_API_KEY or pass api_key."
            )
        resolved_url = base_url or os.environ.get(
            "LITELLM_BASE_URL", "http://localhost:4000/v1"
        )
        super().__init__(
            model=cast(AVAILABLE_OPENAI_MODELS, model),
            api_key=resolved_key,
            temperature=temperature,
            _base_url=resolved_url,
        )


class AsyncLiteLLMConnection(AsyncOpenAIConnection):
    """Asynchronous connection to models exposed by a LiteLLM proxy."""

    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 1.0,
    ) -> None:
        model = model.strip()
        if not model:
            raise ValueError("LiteLLM model alias cannot be empty.")
        resolved_key = api_key or os.environ.get("LITELLM_API_KEY")
        if not resolved_key:
            raise ValueError(
                "LiteLLM API key required. Set LITELLM_API_KEY or pass api_key."
            )
        resolved_url = base_url or os.environ.get(
            "LITELLM_BASE_URL", "http://localhost:4000/v1"
        )
        super().__init__(
            model=cast(AVAILABLE_OPENAI_MODELS, model),
            api_key=resolved_key,
            temperature=temperature,
            _base_url=resolved_url,
        )
