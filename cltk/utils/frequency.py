"""This module's main class reads a text corpus and assembles a list of n
most common words."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'


from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths
from cltk.corpus.utils.formatter import assemble_phi5_author_filepaths
from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
from cltk.corpus.utils.formatter import phi5_plaintext_cleanup
from cltk.utils.cltk_logger import logger
from collections import Counter
from nltk.tokenize.punkt import PunktLanguageVars
import os
from time import strftime


class Frequency:
    """Methods for making word frequency lists."""

    def __init__(self):
        """Language taken as argument, necessary used when saving word frequencies to
        ``cltk_data/user_data``."""
        self.punkt = PunktLanguageVars()
        self.punctuation = [',', '.', ';', ':', '"', "'", '?', '-', '!', '*', '[', ']', '{', '}']

    def counter_from_str(self, string):
        """Build word frequency list from incoming string."""
        string_list = [chars for chars in string if chars not in self.punctuation]
        string_joined = ''.join(string_list)
        tokens = self.punkt.word_tokenize(string_joined)
        return Counter(tokens)


    def counter_from_corpus(self, corpus):
        """Build word frequency list from one of several available corpora.
        TODO: Make this count iteratively, not all at once
        """
        assert corpus in ['phi5', 'tlg'], \
            "Corpus '{0}' not available. Choose from 'phi5' or 'tlg'.".format(corpus)

        all_strings = self._assemble_corpus_string(corpus=corpus)
        return self.counter_from_str(all_strings)

    def _assemble_corpus_string(self, corpus):
        """Takes a list of filepaths, returns a string containing contents of
        all files."""

        if corpus == 'phi5':
            filepaths = assemble_phi5_author_filepaths()
            file_cleaner = phi5_plaintext_cleanup
        elif corpus == 'tlg':
            filepaths = assemble_tlg_author_filepaths()
            file_cleaner = tlg_plaintext_cleanup

        for filepath in filepaths:
            with open(filepath) as file_open:
                file_read = file_open.read().lower()
            file_clean = file_cleaner(file_read)
            yield file_clean
