"""Test cltk.book"""
from unicodedata import normalize
import os
import unittest
from cltk.corpus.utils.importer import CorpusImporter
from cltk.utils.file_operations import make_cltk_path
import importlib

__author__ = 'Patrick J. Burns <patrick@diyclassics.org>'
__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        """Clone Latin Library in order to test pull function and other model
        tests later.
        """
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_text_latin_library')
        from cltk.book.latin import Latin
        self.text1 = Latin.text1
        
        
    def test_book_latin(self):
        """Test importing Latin Book code""" 
        test_name = self.text1.name
        match_name = 'Cicero, In Catilinam'
        self.assertEqual(test_name, match_name)
        

if __name__ == '__main__':
    unittest.main()
