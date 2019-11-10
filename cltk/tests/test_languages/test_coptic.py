"""Test for Coptic, based on John Stewart's tests for Old English"""

import os
import unittest

from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.swadesh import Swadesh

__author__ = ["Edward Nolan <nolanee@umich.edu>", ]


class TestCoptic(unittest.TestCase):
    """Class for unittest"""
    def setUp(self):
        corpus_importer = CorpusImporter("coptic")
        corpus_importer.import_corpus("coptic_text_scriptorium")
        file_rel = os.path.join(get_cltk_data_dir() + '/coptic/text/coptic_text_scriptorium/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    # Swadesh list
    def test_swadesh_coptic(self):
        swadesh = Swadesh('cop')
        first_word = 'ⲁⲛⲟⲕ'
        match = swadesh.words()[0]
        self.assertEqual(first_word, match)


if __name__ == '__main__':
    unittest.main()