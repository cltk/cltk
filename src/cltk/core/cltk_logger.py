"""CLTK's logging module."""

__license__ = "MIT License. See LICENSE."

import logging
import os
import sys

from colorama import Fore, Style
from colorama import init as colorama_init

from cltk.utils.utils import CLTK_DATA_DIR

colorama_init(autoreset=True)


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN + Style.DIM,
        logging.INFO: Fore.GREEN + Style.BRIGHT,
        logging.WARNING: Fore.YELLOW + Style.BRIGHT,
        logging.ERROR: Fore.RED + Style.BRIGHT,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL
        record.msg = f"{color}{record.msg}{reset}"
        return super().format(record)


def setup_cltk_logger(name="CLTK", log_to_file=True, log_to_console=True, level=None):
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
