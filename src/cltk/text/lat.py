"""Functions for replacing j/J and v/V to i/I and u/U"""

__author__ = ["Kyle P. Johnson <kyle@kyle-p-johnson.com>"]
__license__ = "MIT License. See LICENSE."

import re
from re import Pattern

patterns: list[tuple[str, str]] = [(r"j", "i"), (r"v", "u"), (r"J", "I"), (r"V", "U")]
patterns: list[tuple[Pattern[str], str]] = [
    (re.compile(regex), repl) for (regex, repl) in patterns
]


def replace_jv(text: str) -> str:
    """
    Do j/v replacement.

    >>> replace_jv("vem jam VEL JAM")
    'uem iam UEL IAM'
    """

    for pattern, repl in patterns:
        text = re.subn(pattern, repl, text)[0]
    return text
