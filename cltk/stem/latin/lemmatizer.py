"""Lemmatize Latin words with a replacement list."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import re
from cltk.stem.latin.lemmata_list import REPLACEMENT_PATTERNS


class LemmaReplacer(object):
    """Lemmatizing class"""

    def __init__(self, patterns=REPLACEMENT_PATTERNS):
        """Initializer for lemmatizer, imports replacement dict."""
        self.patterns = \
            [(re.compile(regex), repl) for (regex, repl) in patterns]

    def lemmatize(self, text):
        """Replacer of text via the dict."""
        for (pattern, repl) in self.patterns:
            text = re.subn(pattern, repl, text)[0]
        return text
