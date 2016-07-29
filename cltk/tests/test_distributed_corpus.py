
from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.utils.importer import CorpusImportError

import os
import sys
import unittest

DISTRIBUTED_CORPUS_PATH_REL = '~/cltk_data/test_distributed_corpora.yaml'
DISTRIBUTED_CORPUS_PATH = os.path.expanduser(DISTRIBUTED_CORPUS_PATH_REL)


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904

    def test_corpora_import_list_greek(self):
        """Test listing of available corpora."""
        corpus_importer = CorpusImporter('greek', testing=True)
        available_corpora = corpus_importer.list_corpora
        self.assertTrue(available_corpora)

    def make_distributed_corpora_testing_file(self):
        """Setup for some cloning tests, make file at
        '~/cltk_data/test_distributed_corpora.yaml'.
        """
        #! Don't format this literal string, must be YAML-ish
        yaml_str_to_write = """example_distributed_latin_corpus:
        git_remote: git@github.com:kylepjohnson/latin_corpus_newton_example.git
        language: latin
        type: text

example_distributed_fake_language_corpus:
        git_remote: git@github.com:kylepjohnson/doesntexistyet.git
        language: fake_language
        type: treebank
    """
        cltk_data_dir = os.path.expanduser('~/cltk_data')
        if not os.path.isdir(cltk_data_dir):
            os.mkdir(cltk_data_dir)
        with open(DISTRIBUTED_CORPUS_PATH, 'w') as file_open:
            file_open.write(yaml_str_to_write)

    def remove_distributed_corpora_testing_file(self):
        """Remove ~/cltk_data/test_distributed_corpora.yaml."""
        os.remove(DISTRIBUTED_CORPUS_PATH)

    def test_setup_language_variables_no_user_but_in_core(self):
        """Test function which checks for presence of
        ~/cltk_data/distributed_corpora.yaml. Look for a language
        not in core repos but not in user-defined.
        """
        self.make_distributed_corpora_testing_file()
        corpus_importer = CorpusImporter('sanskrit', testing=True)
        self.assertIn('sanskrit_models_cltk', corpus_importer.list_corpora)
        self.remove_distributed_corpora_testing_file()

    def test_setup_language_variables_user_but_not_core(self):
        """Test function which checks for presence of
        `~/cltk_data/distributed_corpora.yaml`. Look for a language
        not in the core but in the user's custom file.
        """
        self.make_distributed_corpora_testing_file()
        corpus_importer = CorpusImporter('fake_language', testing=True)
        corpus_name = corpus_importer.list_corpora
        target_name = 'example_distributed_fake_language_corpus'
        self.assertEqual(corpus_name[0], target_name)
        self.remove_distributed_corpora_testing_file()

    def test_setup_language_variables_no_user_but_yes_core(self):
        """Test function which checks for presence of
        `~/cltk_data/distributed_corpora.yaml`. Look for a language
        in the core but not in the user's custom file.
        """
        self.make_distributed_corpora_testing_file()
        corpus_importer = CorpusImporter('pali', testing=True)
        corpora = corpus_importer.list_corpora
        self.assertIn('pali_text_ptr_tipitaka', corpora)
        self.remove_distributed_corpora_testing_file()

    def test_setup_language_variables_no_user_no_core(self):
        """Test function which checks for presence of
        `~/cltk_data/distributed_corpora.yaml`. Look for a language
        neither in the core or in the user's custom file.
        """
        self.make_distributed_corpora_testing_file()
        with self.assertRaises(CorpusImportError):
            CorpusImporter('fake_language_nowhere')
        self.remove_distributed_corpora_testing_file()


if __name__ == '__main__':
    unittest.main()
