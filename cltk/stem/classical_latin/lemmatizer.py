"""Lemmatize Latin words with a replacement list."""

import re
from cltk.stem.classical_latin.lemmata_list import REPLACEMENT_PATTERNS


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
