"""ChatGPT integration for CLTK.

This module provides a small wrapper class (:class:`ChatGPT`) around the
OpenAI client and high‑level helpers to generate linguistic annotations from
LLMs for a given language (resolved by Glottolog ID).
"""

__license__ = "MIT License. See LICENSE."

import os
import re
from typing import Optional

from openai import AsyncOpenAI, OpenAI, OpenAIError
from openai.types.responses.response import Response

from cltk.core.cltk_logger import logger
from cltk.core.data_types import AVAILABLE_OPENAI_MODELS, CLTKGenAIResponse
from cltk.core.exceptions import CLTKException, OpenAIInferenceError
from cltk.text.utils import cltk_normalize
from cltk.utils.utils import load_env_file


class ChatGPTConnection:
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
            logger.error(msg)
            raise ValueError(msg)
        self.client: OpenAI = OpenAI(api_key=self.api_key)

    def generate(
        self,
        prompt: str,
        max_retries: int = 2,
    ) -> CLTKGenAIResponse:
        logger.debug(prompt)
        code_block: Optional[str] = None
        chatgpt_response: Optional[Response] = None
        attempt: Optional[int] = None
        for attempt in range(1, max_retries + 1):
            logger.debug(f"Attempt {attempt} of {max_retries}")
            try:
                # TODO: Disable 4.1
                if "4.1" in self.model:
                    chatgpt_response = self.client.responses.create(
                        model=self.model, input=prompt, temperature=self.temperature
                    )
                elif "-5" in self.model:
                    chatgpt_response = self.client.responses.create(
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
            logger.debug(f"Raw response from OpenAI: {chatgpt_response.output_text}")
            try:
                code_block = self._extract_code_blocks(
                    text=chatgpt_response.output_text
                )
            except Exception as e:
                # TODO: Count tokens used for failed attempts, too
                logger.error(f"Error extracting code block: {e}")
                continue
            if code_block:
                break  # Success, exit retry loop
            else:
                logger.warning(
                    f"Attempt {attempt}: No code block found in ChatGPT response. Retrying..."
                )
                if attempt == max_retries:
                    final_err = (
                        "No code blocks found in ChatGPT response after retries."
                    )
                    logger.error(final_err)
                    # logger.error(raw_chatgpt_response_normalized)
                    raise CLTKException(final_err)
                    # return doc
                # Optionally, you could modify the prompt or add a delay here
        assert chatgpt_response
        chatgpt_usage: dict[str, int] = self._chatgpt_response_tokens(
            response=chatgpt_response
        )
        raw_chatgpt_response_normalized: str = cltk_normalize(
            text=chatgpt_response.output_text
        )
        logger.debug(
            f"raw_chatgpt_response_normalized:\n{raw_chatgpt_response_normalized}"
        )
        logger.debug(f"Completed generation() after {attempt} attempts")
        # return {"response": raw_chatgpt_response_normalized, "usage": chatgpt_usage}
        return CLTKGenAIResponse(
            response=raw_chatgpt_response_normalized, usage=chatgpt_usage
        )
        # logger.error(f"Exceeded maximum retries: {max_retries}")
        # raise RuntimeError("Failed to generate response after multiple attempts.")

    def _chatgpt_response_tokens(self, response: Response) -> dict[str, int]:
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
            logger.warning(
                "No usage information found in response. Tokens used may not be available."
            )
            logger.info(f"ChatGPT usage: {tokens}")
            return tokens

        # OpenAI API standardizes these keys:
        # prompt_tokens: tokens in the prompt
        # completion_tokens: tokens in the completion
        # total_tokens: total tokens used
        # TODO: input and output stay 0, fix
        tokens["input"] = int(getattr(usage, "prompt_tokens", 0))
        tokens["output"] = int(getattr(usage, "completion_tokens", 0))
        tokens["total"] = int(getattr(usage, "total_tokens", 0))

        if tokens["total"] == 0:
            logger.warning(
                "No tokens used reported in response. This may indicate an issue with the API call."
            )
        logger.info(f"ChatGPT usage: {tokens}")
        return tokens

    def _extract_code_blocks(self, text: str) -> str:
        # This regex finds all text between triple backticks
        code_blocks: list[str] = re.findall(
            r"```(?:[a-zA-Z]*\n)?(.*?)```", text, re.DOTALL
        )
        code_block: str = code_blocks[0].strip()
        logger.debug(f"Extracted code block:\n{code_block}")
        return code_block


class AsyncChatGPTConnection:
    """Asynchronous variant of :class:`ChatGPTConnection`.

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
    ) -> None:
        self.api_key = api_key
        self.model: str = model
        self.temperature: float = temperature
        if not self.api_key:
            load_env_file()
            self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            msg: str = "OPENAI_API_KEY not found. Please set it in your environment or in a .env file."
            logger.error(msg)
            raise ValueError(msg)
        self.client: AsyncOpenAI = AsyncOpenAI(api_key=self.api_key)

    async def generate_async(
        self,
        prompt: str,
        max_retries: int = 2,
    ) -> CLTKGenAIResponse:
        logger.debug("[async] Prompt being sent to OpenAI:\n%s", prompt)
        code_block: Optional[str] = None
        chatgpt_response: Optional[Response] = None
        for attempt in range(1, max_retries + 1):
            logger.debug("[async] Attempt %s of %s", attempt, max_retries)
            try:
                if "4.1" in self.model:
                    chatgpt_response = await self.client.responses.create(
                        model=self.model,
                        input=prompt,
                        temperature=self.temperature,
                    )
                elif "-5" in self.model:
                    chatgpt_response = await self.client.responses.create(
                        model=self.model,
                        input=prompt,
                        reasoning={"effort": "low"},
                        text={"verbosity": "low"},
                    )
                else:
                    raise ValueError(f"Unsupported model: {self.model}.")
            except OpenAIError as openai_error:
                logger.error(
                    "[async] OpenAI error on attempt %s: %s", attempt, openai_error
                )
                if attempt == max_retries:
                    raise OpenAIInferenceError(
                        f"An error from OpenAI occurred: {openai_error}"
                    )
                continue

            logger.debug(
                "[async] Raw response from OpenAI: %s", chatgpt_response.output_text
            )
            try:
                code_block = self._extract_code_blocks(chatgpt_response.output_text)
            except Exception as e:  # pragma: no cover - defensive
                logger.error("[async] Error extracting code block: %s", e)
                code_block = None
            if code_block:
                break
            logger.warning(
                "[async] Attempt %s: No code block found in response. Retrying...",
                attempt,
            )

        assert chatgpt_response is not None
        usage = self._chatgpt_response_tokens(chatgpt_response)
        raw_normalized: str = cltk_normalize(text=chatgpt_response.output_text)
        logger.debug("[async] Normalized output text:\n%s", raw_normalized)
        return CLTKGenAIResponse(response=raw_normalized, usage=usage)

    def _chatgpt_response_tokens(self, response: Response) -> dict[str, int]:
        usage = getattr(response, "usage", None)
        tokens: dict[str, int] = {"input": 0, "output": 0, "total": 0}
        if not usage:
            logger.info("[async] No usage info present; returning zeros")
            return tokens
        tokens["input"] = int(getattr(usage, "prompt_tokens", 0))
        tokens["output"] = int(getattr(usage, "completion_tokens", 0))
        tokens["total"] = int(getattr(usage, "total_tokens", 0))
        logger.info("[async] ChatGPT usage: %s", tokens)
        return tokens

    def _extract_code_blocks(self, text: str) -> str:
        code_blocks: list[str] = re.findall(
            r"```(?:[a-zA-Z]*\n)?(.*?)```", text, re.DOTALL
        )
        code_block: str = code_blocks[0].strip()
        logger.debug("[async] Extracted code block:\n%s", code_block)
        return code_block
