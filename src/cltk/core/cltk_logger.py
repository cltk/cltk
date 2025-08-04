"""CLTK's logging module."""

__license__ = "MIT License. See LICENSE."

import logging
import os
import sys

from cltk.utils.utils import CLTK_DATA_DIR


def setup_cltk_logger(name="CLTK", log_to_file=True, log_to_console=True, level=None):
    logger = logging.getLogger(name)
    logger.handlers.clear()  # Remove any existing handlers

    log_level = level or os.getenv("CLTK_LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    formatter_file = logging.Formatter(
        "%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s"
    )
    formatter_console = logging.Formatter("%(levelname)s: %(message)s")

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
