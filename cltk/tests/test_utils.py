"""Test cltk.utils."""

from collections import Counter
import os
from pickle import UnpicklingError
import unittest

from cltk.corpus.utils.importer import CorpusImporter
from cltk.utils.cltk_logger import logger
from cltk.utils.contributors import Contributors
from cltk.utils.file_operations import make_cltk_path
from cltk.utils.file_operations import open_pickle
from cltk.utils.frequency import Frequency
from cltk.utils.philology import Philology


__license__ = 'MIT License. See LICENSE.'


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

    def test_open_pickle_fail_missing(self):
        """Test failure to unpickle a file that doesn't exist"""
        bad_file = 'cltk/tests/doesnt_exist.pickle'
        with self.assertRaises(FileNotFoundError):
            open_pickle(bad_file)

    def test_open_pickle_fail_corrupt(self):
        """Test failure to open corrupted pickle."""
        bad_file = 'cltk/tests/bad_pickle.pickle'
        with self.assertRaises(UnpicklingError):
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
        frequencies = Frequency()
        text = 'Quo Quo Quo Quo usque tandem abutere, Catilina Catilina Catilina, patientia nostra nostra ?'.lower()
        count = frequencies.counter_from_str(text)
        target = Counter({'quo': 4, 'catilina': 3, 'nostra': 2, 'patientia': 1, 'abutere': 1, 'usque': 1, 'tandem': 1})
        self.assertEqual(count, target)

    def test_make_list_from_corpus_assert(self):
        """Test frequency builder for corpus, if present."""
        frequencies = Frequency()
        with self.assertRaises(AssertionError):
            frequencies.counter_from_corpus('xxx')

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

    def test_concordance_from_file_ioerror(self):
        """Test ``write_concordance_from_file()`` for file writing completion
        of concordance builder, with IOError. Doesn't test quality of output."""
        philology = Philology()
        bad_path = '/cltk_data/user_data/concordance_test_file.txt'
        with self.assertRaises(IOError):
            philology.write_concordance_from_file(bad_path, 'test_file')

    def test_contribs_walk_cltk(self):
        """Test recursive fp walk."""
        contribs = Contributors()
        modules_list = contribs.walk_cltk()
        self.assertEqual(type(modules_list), list)

    def test_get_module_authors(self):
        """Test opening contribs file."""
        contribs = Contributors()
        author = contribs.get_module_authors('cltk/corpus/utils/importer.py')[0]
        self.assertEqual(author, 'Kyle P. Johnson <kyle@kyle-p-johnson.com>')

    def test_contribs_make_authors_dict(self):
        """Test making dict for author contrib file."""
        contribs = Contributors()
        authors_dict = contribs._make_authors_dict()
        self.assertGreater(len(authors_dict), 8)

    def test_contribs_write_contribs(self):
        """Test contrib writing function."""
        contribs = Contributors()
        file = 'contributors.md'
        try:
            os.remove(file)
        except FileNotFoundError:
            logger.info("No file to remove at '%s'. Continuing.", file)
        contribs.write_contribs()
        contribs_file = os.path.isfile(file)
        self.assertTrue(contribs_file)


class TestPathCreation(unittest.TestCase):
    """Class for filepath maker."""

    def test_empty_path(self):
        """Test empty empty_path()"""
        self.assertEqual(make_cltk_path(),
                         os.path.expanduser(os.path.join('~', 'cltk_data')))

    def test_path(self):
        """Test empty_path() with argument."""
        self.assertEqual(make_cltk_path('greek', 'perseus_corpus'),
                         os.path.expanduser(os.path.join('~', 'cltk_data', 'greek', 'perseus_corpus')))


if __name__ == '__main__':
    unittest.main()
