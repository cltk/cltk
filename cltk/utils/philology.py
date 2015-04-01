"""Miscellaneous operations for traditional philology and simple
statistics."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.utils.cltk_logger import logger
from nltk.text import ConcordanceIndex
from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.text import Text
import os



# AVAILABLE_LANGUAGES = ['latin']


class Philology:
    """Class for Philological and simple statistics."""

    def __init__(self):
        """Misc. contructors."""
        pass

    def _read_file(self, filepath):
        """Read a file and return it as a string"""
        filepath = os.path.expanduser(filepath)  #? Check this is ok if absolute paths passed in
        with open(filepath) as opened_file:
            read_file = opened_file.read()
            return read_file

    def _build_concordance(self, text_string):
        """
        Inherit or mimic the logic of ConcordanceIndex() at http://www.nltk.org/_modules/nltk/text.html
        and/or ConcordanceSearchView() & SearchCorpus() at https://github.com/nltk/nltk/blob/develop/nltk/app/concordance_app.py
        :param text_string: Text to be turned into a concordance
        :type text_string: str
        :return: str
        """
        tokens = PunktWordTokenizer().tokenize(text_str.lower())  # mk lower() an option later
        #concordance = ConcordanceIndex(tokens) # this returns just one word
        #c.print_concordance('ut')  # this returns just one word

        t = Text(tokens)
        #t.concordance('ut')  # this has better formatting than c.print_concordance('ut')
        tokens_read = t.tokens
        for token in tokens_read:
            print(t.concordance(token))  # the original object prints a lot of junk; figure how to stop this
        #! from here, add lines to memory, then return

    def concordance(self, filepaths):
        """Replacer of text via the dict.
        :type filepaths: str or list
        :param filepaths: Filepath of text(s) to be used in concordance.
        :rtype : str
        """
        assert isinstance(filepaths, (str, list))
        if isinstance(filepaths, str):
            filepath = filepaths
            text = self._read_file(filepath)
        elif isinstance(filepaths, list):
            text = ''
            for filepath in filepaths:
                text += self._read_file(filepath)
        concordance = self._build_concordance(text)
        return concordance
