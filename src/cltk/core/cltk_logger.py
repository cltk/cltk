"""CLTK logging utilities.

Provides a colorized console formatter and a helper to configure a module
logger suitable for libraries and CLI output.
"""

__license__ = "MIT License. See LICENSE."

import logging
import os
import sys

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


def setup_cltk_logger(
    name: str = "CLTK",
    log_to_file: bool = True,
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
        "%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s"
    )
    formatter_console = ColorFormatter("%(levelname)s: %(message)s")

    if log_to_file:
        file_handler = logging.FileHandler("cltk.log")
        file_handler.setFormatter(formatter_file)
        logger.addHandler(file_handler)

    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter_console)
        logger.addHandler(console_handler)

    return logger


# Usage:
logger = setup_cltk_logger(level="WARNING")
logger.debug("CLTK logger initialized.")
