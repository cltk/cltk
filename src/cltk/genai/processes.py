"""ChatGPT-backed process classes for CLTK.

This module defines :class:`ChatGPTProcess`, a generic :class:`~cltk.core.data_types.Process`
that initializes a :class:`~cltk.genai.chatgpt.ChatGPT` client.
"""

__license__ = "MIT License. See LICENSE."


# from cltk.alphabet.text_normalization import cltk_normalize
from cltk.core.data_types import Process


class GPTProcess(Process):
    """Base class for GPT-backed processes."""


class LocalGPTProcess(GPTProcess):
    """Base class for locally running GPT-backed processes."""
