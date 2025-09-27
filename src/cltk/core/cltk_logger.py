"""CLTK logging utilities.

Provides a colorized console formatter and a helper to configure a module
logger suitable for libraries and CLI output.

Adds lightweight "structured" fields (doc_id, sentence_idx, model,
glottolog_id, prompt_version) to each log record so they can be grepped or
filtered in the file logs. Use ``bind_context(...)`` to attach values for a
code path; otherwise, defaults are injected so formatting never fails.
"""

__license__ = "MIT License. See LICENSE."

import logging
import os
import sys
from typing import Any, MutableMapping, Optional

from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)  # for Windows


class ColorFormatter(logging.Formatter):
    """Console color formatter using Colorama styles."""

    COLORS = {
        logging.DEBUG: Fore.CYAN + Style.DIM,
        logging.INFO: Fore.CYAN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Return a colorized log line for console output."""
        color = self.COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL
        # record.msg = f"{color}{record.msg}{reset}"
        # return super().format(record)
        message = super().format(record)
        return f"{color}{message}{reset}"


class _CLTKContextFilter(logging.Filter):
    """Ensure structured fields exist on every log record.

    Injects default values for structured context keys so formatters can
    safely reference them even when a handler or call site did not bind
    explicit context.
    """

    KEYS = (
        "doc_id",
        "sentence_idx",
        "model",
        "glottolog_id",
        "prompt_version",
    )

    def filter(self, record: logging.LogRecord) -> bool:
        for k in self.KEYS:
            if not hasattr(record, k):
                setattr(record, k, "-")
        return True


class _ContextAdapter(logging.LoggerAdapter):
    """LoggerAdapter that attaches structured context into ``extra``."""

    def process(
        self, msg: Any, kwargs: MutableMapping[str, Any]
    ) -> tuple[Any, MutableMapping[str, Any]]:
        extra: dict[str, Any] = kwargs.get("extra", {}) or {}
        # Existing adapter.extra should take precedence over call-time extras
        merged = (
            {**kwargs.get("extra", {}), **self.extra}
            if isinstance(self.extra, dict)
            else extra
        )
        if merged:
            kwargs["extra"] = merged
        return msg, kwargs


def setup_cltk_logger(
    name: str = "CLTK",
    log_to_file: bool | None = None,
    log_to_console: bool = True,
    level: str | None = None,
) -> logging.Logger:
    """Configure and return a library logger.

    Args:
      name: Logger name.
      log_to_file: If true, add a file handler writing to ``cltk.log``.
      log_to_console: If true, add a colorized console handler.
      level: Optional log level name (e.g., ``"INFO"``). If ``None``, uses
        ``CLTK_LOG_LEVEL`` environment variable or defaults to ``INFO``.

    Returns:
      A configured ``logging.Logger`` instance.

    """
    logger = logging.getLogger(name)
    logger.handlers.clear()  # Remove any existing handlers

    log_level = level or os.getenv("CLTK_LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    formatter_file = logging.Formatter(
        (
            "%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(levelname)s"
            " - doc_id=%(doc_id)s sentence_idx=%(sentence_idx)s"
            " model=%(model)s glottolog_id=%(glottolog_id)s"
            " prompt_version=%(prompt_version)s - %(message)s"
        )
    )
    formatter_console = ColorFormatter("%(levelname)s: %(message)s")

    # Determine file logging from explicit arg or env var (default: off)
    if log_to_file is None:
        env_val = os.getenv("CLTK_LOG_TO_FILE", "").strip().lower()
        log_to_file = env_val in {"1", "true", "yes", "on"}

    if log_to_file:
        file_handler = logging.FileHandler("cltk.log")
        file_handler.setFormatter(formatter_file)
        file_handler.addFilter(_CLTKContextFilter())
        logger.addHandler(file_handler)

    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter_console)
        console_handler.addFilter(_CLTKContextFilter())
        logger.addHandler(console_handler)

    return logger


# Usage:
logger = setup_cltk_logger(level="WARNING")
logger.debug("CLTK logger initialized.")


def bind_context(
    *,
    doc_id: Optional[str] = None,
    sentence_idx: Optional[int] = None,
    model: Optional[str] = None,
    glottolog_id: Optional[str] = None,
    prompt_version: Optional[str] = None,
    base_logger: Optional[logging.Logger] = None,
) -> logging.LoggerAdapter:
    """Return a LoggerAdapter that carries structured CLTK context.

    Example:
        ```python
        log = bind_context(doc_id="abc123", sentence_idx=0, model="gpt-5-mini")
        log.info("Generating POS tags")
        ```

    Args:
      doc_id: Stable document identifier for correlating events.
      sentence_idx: Sentence index within the document (if applicable).
      model: Backend model identifier (e.g., LLM model name).
      glottolog_id: Language or dialect identifier.
      prompt_version: Semantic version of the prompt used for a call.
      base_logger: Optional base logger to adapt; defaults to module ``logger``.

    """
    base = base_logger or logger
    extra: dict[str, Any] = {
        "doc_id": doc_id if doc_id is not None else "-",
        "sentence_idx": sentence_idx if sentence_idx is not None else "-",
        "model": model if model is not None else "-",
        "glottolog_id": glottolog_id if glottolog_id is not None else "-",
        "prompt_version": prompt_version if prompt_version is not None else "-",
    }
    return _ContextAdapter(base, extra)
