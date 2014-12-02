"""Lemmatize Latin words."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import re
from cltk.stem.latin.lemma_list import REPLACEMENT_PATTERNS

AVAILABLE_LANGUAGES = ['latin']


class LemmaReplacer(object):
    """Lemmatize Latin words by replacing input words with corresponding
    values from a replacement list.
    """

    def __init__(self, language):
        """Import replacement patterns into a list."""
        self.language = language
        self._patterns = self._setup_language_variables()

    def _setup_language_variables(self):
        """Check for availability of lemmatizer for a language.
        TODO: Move ``lemma_list.py`` to CLTK linguistic DL.
        """
        assert self.language in AVAILABLE_LANGUAGES, \
            'Corpora not available for %s language.' % self.language
        if self.language == 'latin':
            patterns = REPLACEMENT_PATTERNS
        print('Loading lemmata. This may take a minute.')
        return [(re.compile(regex), repl) for (regex, repl) in patterns]

    def lemmatize(self, text):
        """Replacer of text via the dict.
        :type text: str
        :param text: Input text to be lemmatized.
        :rtype : str
        """
        for (pattern, repl) in self._patterns:
            text = re.subn(pattern, repl, text)[0]
        return text
