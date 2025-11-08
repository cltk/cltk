"""Mistral integration for CLTK.

Based on https://docs.mistral.ai/capabilities/completion/.

# Internal; no stability guarantees

This module provides a small wrapper class (:class:`MistralConnection`) around the
Mistral client and high‑level helpers to generate linguistic annotations from
LLMs for a given language (resolved by Glottolog ID).
"""

__license__ = "MIT License. See LICENSE."

import os
import re
from typing import Any, Optional, cast

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import AVAILABLE_MISTRAL_MODELS, CLTKGenAIResponse
from cltk.core.exceptions import CLTKException, MistralInferenceError
from cltk.text.utils import cltk_normalize
from cltk.utils.utils import load_env_file


class _MistralErrorFallback(Exception):
    """Fallback error raised when the Mistral SDK is unavailable."""


def _resolve_mistral_classes() -> tuple[Optional[Any], Optional[Any]]:
    try:
        from mistralai import Mistral as imported_mistral
    except Exception:
        used_mistral = None
    else:
        used_mistral = imported_mistral
    try:
        from mistralai import SDKError as imported_sdk_error
    except Exception:
        sdk_error = None
    else:
        sdk_error = imported_sdk_error
    return used_mistral, sdk_error


Mistral, SDKError = _resolve_mistral_classes()


class MistralConnection:
    """Thin wrapper around the Mistral client for CLTK use cases.

    Args:
      api_key: Mistral API key.
      model: Small set of supported model aliases.
      temperature: Sampling temperature (default 1.0).

    Attributes:
      client: Mistral client instance.

    """

    def __init__(
        self,
        model: AVAILABLE_MISTRAL_MODELS,
        api_key: Optional[str] = None,
        temperature: float = 1.0,
    ):
        """Initialize the client and resolve language/dialect metadata."""
        self.api_key = api_key
        self.model: str = model
        self.temperature: float = temperature
        if not self.api_key:
            load_env_file()
            self.api_key = os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            msg: str = "MISTRAL_API_KEY not found. Please set it in your environment or in a .env file."
            # Bind with model context even before self.log is available
            bind_context(model=str(model)).error(msg)
            raise ValueError(msg)
        # Use patched Mistral if provided by tests; else import lazily
        mistral_cls = Mistral
        if mistral_cls is None:  # pragma: no cover - import only if needed
            try:
                from mistralai import Mistral as runtime_mistral
            except Exception as e:
                raise ImportError(
                    "Mistral client not installed. Install with: pip install 'cltk[mistral]'"
                ) from e
            mistral_cls = runtime_mistral
        self.client = mistral_cls(api_key=self.api_key)
        # Structured logger bound with model identifier
        self.log = bind_context(model=str(self.model))

    def generate(
        self,
        prompt: str,
        max_retries: int = 2,
    ) -> CLTKGenAIResponse:
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
        mistral_response: Optional[Any] = None
        attempt: Optional[int] = None
        # Accumulate tokens across attempts (including failed ones)
        agg_tokens: dict[str, int] = {"input": 0, "output": 0, "total": 0}
        for attempt in range(1, max_retries + 1):
            self.log.debug(f"Attempt {attempt} of {max_retries}")
            try:
                mistral_response = self.client.chat.complete(
                    model=self.model,
                    messages=cast(Any, [dict(role="user", content=prompt)]),
                )
            except Exception as mistral_error:
                # Some runtimes may not provide SDKError at import time; catch generic
                # exceptions and re-raise as MistralInferenceError for uniform handling.
                raise MistralInferenceError(
                    f"An error from Mistral occurred: {mistral_error}"
                )
            if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
                "1",
                "true",
                "yes",
                "on",
            }:
                # Safely handle cases where mistral_response may be None or missing the attribute
                out_text = getattr(mistral_response, "output_text", "")
                if out_text is None:
                    out_text = ""
                self.log.debug(f"Raw response from Mistral: {out_text}")
            # Add usage from this attempt even if parsing fails
            try:
                tok = self._mistral_response_tokens(mistral_response)
                for k in ("input", "output", "total"):
                    agg_tokens[k] += tok.get(k, 0)
            except Exception:
                pass
            try:
                out_text = getattr(mistral_response, "output_text", "") or ""
                code_block = self._extract_code_blocks(text=out_text)
            except Exception as e:
                # TODO: Count tokens used for failed attempts, too
                self.log.error(f"Error extracting code block: {e}")
                continue
            if code_block:
                break  # Success, exit retry loop
            else:
                self.log.warning(
                    f"Attempt {attempt}: No code block found in Mistral response. Retrying..."
                )
                if attempt == max_retries:
                    final_err = (
                        "No code blocks found in Mistral response after retries."
                    )
                    self.log.error(final_err)
                    # logger.error(raw_mistral_response_normalized)
                    raise CLTKException(final_err)
                    # return doc
                # Optionally, you could modify the prompt or add a delay here
        assert mistral_response
        # Use the accumulated usage across all attempts
        mistral_usage: dict[str, int] = agg_tokens
        # Normalize the same response_text as used for code extraction/logging
        raw_mistral_response_normalized: str = cltk_normalize(
            text=mistral_response.output_text
        )
        if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug(
                f"raw_mistral_response_normalized:\n{raw_mistral_response_normalized}"
            )
        self.log.debug(f"Completed generation() after {attempt} attempts")
        # return {"response": raw_mistral_response_normalized, "usage": mistral_usage}
        return CLTKGenAIResponse(
            response=raw_mistral_response_normalized, usage=mistral_usage
        )
        # logger.error(f"Exceeded maximum retries: {max_retries}")
        # raise RuntimeError("Failed to generate response after multiple attempts.")

    def _mistral_response_tokens(self, response: Any) -> dict[str, int]:
        """Extract token usage information from a Mistral response.

        Args:
          model: Model alias used for the call.
          response: Mistral response object.

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
            self.log.info(f"Mistral usage: {tokens}")
            return tokens

        # Normalize key names across Mistral endpoints
        def _get(u: object, *names: str) -> int:
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
        self.log.info(f"Mistral usage: {tokens}")
        return tokens

    def _extract_code_blocks(self, text: str) -> str:
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


#
class AsyncMistralConnection:
    """Asynchronous variant of :class:`MistralConnection`.

    Provides an ``async`` ``generate_async()`` method and uses the
    ``chat.stream`` client under the hood. Mirrors the behavior and logging of
    the synchronous client while enabling concurrent requests.

    Args:
      model: Model alias to use (see ``AVAILABLE_MISTRAL_MODELS``).
      api_key: Optional Mistral API key. Falls back to ``MISTAL_API_KEY``.
      temperature: Sampling temperature for generation.

    """

    def __init__(
        self,
        model: AVAILABLE_MISTRAL_MODELS,
        api_key: Optional[str] = None,
        temperature: float = 1.0,
    ) -> None:
        self.api_key = api_key
        self.model: str = model
        self.temperature: float = temperature
        if not self.api_key:
            load_env_file()
            self.api_key = os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            msg: str = "MISTRAL_API_KEY not found. Please set it in your environment or in a .env file."
            bind_context(model=str(model)).error(msg)
            raise ValueError(msg)
        async_mistral_cls = Mistral
        if async_mistral_cls is None:  # pragma: no cover - import only if needed
            try:
                from mistralai import Mistral as runtime_async_mistral
            except Exception as e:
                raise ImportError(
                    "Mistral client not installed. Install with: pip install 'cltk[mistral]'"
                ) from e
            async_mistral_cls = runtime_async_mistral
        self.client = async_mistral_cls(api_key=self.api_key)
        # Structured logger bound with model identifier
        self.log = bind_context(model=str(self.model))

    async def generate_async(
        self,
        prompt: str,
        max_retries: int = 2,
    ) -> CLTKGenAIResponse:
        import os as _os

        if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug("[async] Prompt being sent to Mistral:\n%s", prompt)
        code_block: Optional[str] = None
        mistral_response: Optional[Any] = None
        agg_tokens: dict[str, int] = {"input": 0, "output": 0, "total": 0}
        for attempt in range(1, max_retries + 1):
            try:
                mistral_response = await self.client.chat.complete_async(
                    model=self.model,
                    messages=cast(Any, [dict(role="user", content=prompt)]),
                )
            except Exception as mistral_error:
                # Some runtimes may not provide SDKError at import time; log and
                # treat any exception as a MistralInferenceError when retries are exhausted.
                self.log.error(
                    "[async] Mistral error on attempt %s: %s", attempt, mistral_error
                )
                if attempt == max_retries:
                    raise MistralInferenceError(
                        f"An error from Mistral occurred: {mistral_error}"
                    )
                continue
            if not mistral_response:
                self.log.error("[async] No response received from Mistral.")
                if attempt == max_retries:
                    raise MistralInferenceError("No response received from Mistral.")
                continue
            try:
                mistral_content: str = str(mistral_response.choices[0].message.content)
            except Exception:
                self.log.error("Mistral response missing expected content.")
                raise MistralInferenceError(
                    "Mistral response missing expected content."
                )
            self.log.debug("[async] Raw response from Mistral: %s", mistral_content)
            # Track usage for this attempt (even if parsing fails)
            try:
                tok = self._mistral_response_tokens(mistral_response)
                for k in ("input", "output", "total"):
                    agg_tokens[k] += tok.get(k, 0)
            except Exception:
                pass
            try:
                code_block = self._extract_code_blocks(mistral_content)
            except Exception as e:  # pragma: no cover - defensive
                self.log.error("[async] Error extracting code block: %s", e)
                code_block = None
            if code_block:
                break
            self.log.warning(
                "[async] Attempt %s: No code block found in response. Retrying...",
                attempt,
            )

        assert mistral_response is not None
        usage = agg_tokens
        raw_normalized: str = cltk_normalize(
            text=mistral_response.choices[0].message.content
        )
        if _os.getenv("CLTK_LOG_CONTENT", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.log.debug("[async] Normalized output text:\n%s", raw_normalized)
        return CLTKGenAIResponse(response=raw_normalized, usage=usage)

    def _mistral_response_tokens(self, response: Any) -> dict[str, int]:
        usage = getattr(response, "usage", None)
        tokens: dict[str, int] = {"input": 0, "output": 0, "total": 0}
        if not usage:
            self.log.info("[async] No usage info present; returning zeros")
            return tokens

        def _get(u: object, *names: str) -> int:
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
        self.log.info("[async] Mistral usage: %s", tokens)
        return tokens

    def _extract_code_blocks(self, text: str) -> str:
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
