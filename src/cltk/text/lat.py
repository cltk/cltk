"""Functions for replacing j/J and v/V to i/I and u/U"""

__author__ = ["Kyle P. Johnson <kyle@kyle-p-johnson.com>"]
__license__ = "MIT License. See LICENSE."

import re
from re import Pattern

from cltk.core.exceptions import CLTKException

raw_patterns: list[tuple[str, str]] = [
    (r"j", "i"),
    (r"v", "u"),
    (r"J", "I"),
    (r"V", "U"),
]
patterns: list[tuple[Pattern[str], str]] = [
    (re.compile(regex), repl) for (regex, repl) in raw_patterns
]


def replace_jv(text: str) -> str:
    """
    Do j/v replacement.

    >>> replace_jv("vem jam VEL JAM")
    'uem iam UEL IAM'
    """
    if not isinstance(text, str):
        raise CLTKException("Input to replace_jv() must be a string.")
    if not text:
        raise CLTKException("Input string to replace_jv() must not be empty.")
    try:
        for pattern, repl in patterns:
            text = re.subn(pattern, repl, text)[0]
    except Exception as e:
        raise CLTKException(f"Error during j/v replacement: {e}")
    return text
