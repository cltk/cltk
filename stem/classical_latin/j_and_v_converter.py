"""Functions for replacing j/J and v/V to i/I and u/U"""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import re


class JVReplacer(object):  # pylint: disable=R0903
    """Replace J/V with I/U."""

    def __init__(self):
        """Initialization for JVReplacer, reads replacement pattern tuple."""
        patterns = [(r'j', 'i'), (r'v', 'u'), (r'J', 'I'), (r'V', 'U')]
        self.patterns = \
            [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        """Do j/v replacement"""
        for (pattern, repl) in self.patterns:
            text = re.subn(pattern, repl, text)[0]
        return text
