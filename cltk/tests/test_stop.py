"""Test cltk.stop."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.utils.importer import CorpusImporter
from cltk.stop.greek.stops import STOPS_LIST as greek_stops
from cltk.stop.latin.stops import STOPS_LIST as latin_stops
from nltk.tokenize.punkt import PunktLanguageVars
import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        """Clone Greek models in order to test pull function and other model
        tests later.
        """
        corpus_importer = CorpusImporter('greek')
        corpus_importer.import_corpus('greek_models_cltk')
        file_rel = os.path.join('~/cltk_data/greek/model/greek_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_models_cltk')
        file_rel = os.path.join('~/cltk_data/latin/model/latin_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)


if __name__ == '__main__':
    unittest.main()
