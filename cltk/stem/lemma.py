"""Lemmatize Latin words."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.utils.cltk_logger import logger
import importlib.machinery
import os
import re

AVAILABLE_LANGUAGES = ['latin']


class LemmaReplacer(object):  # pylint: disable=R0903
    """Lemmatize Latin words by replacing input words with corresponding
    values from a replacement list.
    """

    def __init__(self, language):
        """Import replacement patterns into a list."""
        self.language = language
        self._patterns = self._setup_language_variables()

    def _setup_language_variables(self):
        """Check for availability of lemmatizer for a language.
        TODO: Turn 'lemma_list' file a simple csv and importing on the fly.
        """
        assert self.language in AVAILABLE_LANGUAGES, \
            'Corpora not available for %s language.' % self.language
        if self.language == 'latin':
            rel_path = os.path.join('~/cltk_data',
                                    self.language,
                                    'trained_model/cltk_linguistic_data/lemmata/lemma_list.py')  # pylint: disable=C0301
            path = os.path.expanduser(rel_path)
            logger.info('Loading lemmata. This may take a minute.')
            loader = importlib.machinery.SourceFileLoader('lemma_list', path)
            module = loader.load_module()
            patterns = module.REPLACEMENT_PATTERNS
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
