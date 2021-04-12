"""CLTK's logging module."""


import logging.config
import os

from cltk.utils.utils import CLTK_DATA_DIR

__author__ = [
    "Kyle P. Johnson <kyle@kyle-p-johnson.com>",
    "Stephen Margheim <stephen.margheim@gmail.com>",
]

log_path = os.path.join(CLTK_DATA_DIR, "cltk.log")  # pylint: disable=invalid-name

if not os.path.isdir(CLTK_DATA_DIR):
    os.mkdir(CLTK_DATA_DIR)

logger = logging.getLogger("CLTK")  # pylint: disable=invalid-name
handler = logging.FileHandler(log_path)  # pylint: disable=invalid-name
formatter = logging.Formatter(  # pylint: disable=invalid-name
    "%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
