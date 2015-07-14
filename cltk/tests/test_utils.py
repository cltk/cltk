"""Test cltk.utils."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.utils.build_contribs_index import build_contribs_file
from cltk.utils.file_operations import open_pickle
from cltk.utils.philology import Philology
from nltk.tokenize.punkt import PunktLanguageVars
import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
