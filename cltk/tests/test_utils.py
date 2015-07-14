"""Test cltk.utils."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.utils.importer import CorpusImporter
from cltk.utils.build_contribs_index import build_contribs_file
from cltk.utils.file_operations import open_pickle
from cltk.utils.frequency import Frequency
from cltk.utils.philology import Philology
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

    def test_build_contribs_file(self):
        """Test building of contributors file ``contributors.md`` by
        ``build_contribs_file.py``."""
        string = build_contribs_file(test=True)
        self.assertTrue(string)


    def test_open_pickle_fail_missing(self):
        """Test failure to unpickle a file that doesn't exist"""
        bad_file = 'cltk/tests/doesnt_exist.pickle'
        with self.assertRaises(FileNotFoundError):
            open_pickle(bad_file)

    def test_open_pickle_fail_corrupt(self):
        """Test failure to open corrupted pickle."""
        bad_file = 'cltk/tests/bad_pickle.pickle'
        with self.assertRaises(EOFError):
            open_pickle(bad_file)

    def test_logger(self):
        """Test the CLTK logger."""
        home_dir = os.path.expanduser('~/cltk_data')
        log_path = os.path.join(home_dir, 'cltk.log')
        self.assertTrue(log_path)

    def test_open_pickle(self):
        """Test opening pickle. This requires ``greek_models_cltk``
        to have been run in ``setUp()``.
        """
        pickle_path_rel = '~/cltk_data/greek/model/greek_models_cltk/tokenizers/sentence/greek.pickle'  # pylint: disable=line-too-long
        pickle_path = os.path.expanduser(pickle_path_rel)
        a_pickle = open_pickle(pickle_path)
        self.assertTrue(a_pickle)

    def test_make_frequencies(self):
        """Test frequency builder."""
        frequencies = Frequency('latin')
        text = 'Quo Quo Quo Quo usque tandem abutere, Catilina Catilina Catilina, patientia nostra nostra ?'.lower()
        stops = frequencies.make_list_from_str(text, 3)
        target = ['quo', 'catilina', 'nostra']
        self.assertEqual(stops, target)

    def test_make_frequencies_save(self):
        """Test frequency builder."""
        frequencies = Frequency('latin')
        text = 'Quo Quo Quo Quo usque tandem abutere, Catilina Catilina Catilina, patientia nostra nostra ?'.lower()
        frequencies.make_list_from_str(text, 3, save=True)
        # cltk_data/user_data/stops_latin_*
        user_data_rel = '~/cltk_data/user_data/'
        user_data = os.path.expanduser(user_data_rel)
        list_dir = os.listdir(user_data)
        file_start = 'stops_latin_'
        for file in list_dir:
            if file.startswith(file_start):
                self.assertTrue(file.startswith(file_start))
                os.remove(user_data + file)

    def test_make_list_from_corpus_assert(self):
        """Test frequency builder for corpus, if present."""
        frequencies = Frequency('latin')
        with self.assertRaises(AssertionError):
            frequencies.make_list_from_corpus('xxx')

    def test_saving_frequencies(self):
        """Test frequency saving private module."""
        frequencies = Frequency('latin')
        frequencies._save_frequencies(['word1', 'word2'])
        # cltk_data/user_data/stops_latin_*
        user_data_rel = '~/cltk_data/user_data/'
        user_data = os.path.expanduser(user_data_rel)
        list_dir = os.listdir(user_data)
        file_start = 'frequency_latin_'
        for file in list_dir:
            if file.startswith(file_start):
                self.assertTrue(file.startswith(file_start))
                os.remove(user_data + file)

    def test_concordance_from_string(self):
        """Test ``write_concordance_from_string()`` for file writing completion
        of concordance builder. Doesn't test quality of output."""
        philology = Philology()
        text = 'felices cantus ore sonante dedit'
        philology.write_concordance_from_string(text, 'test_string')
        file = os.path.expanduser('~/cltk_data/user_data/concordance_test_string.txt')
        is_file = os.path.isfile(file)
        self.assertTrue(is_file)

    def test_concordance_from_file(self):
        """Test ``write_concordance_from_file()`` for file writing completion
        of concordance builder. Doesn't test quality of output."""
        philology = Philology()
        file = 'cltk/tests/bad_pickle.pickle'
        philology.write_concordance_from_file(file, 'test_file')
        file = os.path.expanduser('~/cltk_data/user_data/concordance_test_file.txt')
        is_file = os.path.isfile(file)
        self.assertTrue(is_file)

if __name__ == '__main__':
    unittest.main()
