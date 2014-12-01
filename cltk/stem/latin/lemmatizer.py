"""Lemmatize Latin words."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import re
from cltk.stem.latin.lemmata_list import REPLACEMENT_PATTERNS


class LemmaReplacer(object):
    """Lemmatize Latin words by replacing input words with corresponding
    values from a replacement list.
    """

    def __init__(self, patterns=REPLACEMENT_PATTERNS):
        """Import replacement patterns into a list."""
        self._patterns = \
            [(re.compile(regex), repl) for (regex, repl) in patterns]

    def lemmatize(self, text):
        """Replacer of text via the dict."""
        for (pattern, repl) in self._patterns:
            text = re.subn(pattern, repl, text)[0]
        return text
