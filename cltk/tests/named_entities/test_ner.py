import os
import shutil
import unittest

from cltk.corpus.utils.importer import CorpusImporter
from cltk.tag import ner

class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_tag_ner_str_list_french(self):
        """Test make_ner(), str, list."""
        text_str = """Berte fu mere Charlemaine, qui pukis tint France et tot le Maine."""

        tokens = ner.tag_ner('french', input_text=text_str, output_type=list)
        target = [('Berte', 'Entity'), ('fu',), ('mere',), ('Charlemaine', 'Entity'), (',',), ('qui',), ('pukis',),
                  ('tint',), ('France', 'Entity'), ('et',), ('tot',), ('le',), ('Maine', 'Entity'), ('.',)]
        self.assertEqual(tokens, target)


    def test_tag_ner_list_list_french(self):
        """Test make_ner(), list, list."""
        text_list = ['Berte', 'fu', 'mere', 'Charlemaine']
        tokens = ner.tag_ner('french', input_text=text_list, output_type=list)
        target = [('Berte', 'Entity'), ('fu',), ('mere',), ('Charlemaine', 'Entity')]
        self.assertEqual(tokens, target)


    def test_tag_ner_list_str_french(self):
        """Test make_ner(), list, str."""
        text_list = ['Berte', 'fu', 'mere', 'Charlemaine']
        text = ner.tag_ner('french', input_text=text_list, output_type=str)
        target = ' Berte/Entity fu mere Charlemaine/Entity'
        self.assertEqual(text, target)


    def test_tag_ner_str_str_french(self):
        """Test make_ner(), str, str."""
        text_str = """Berte fu mere Charlemaine, qui pukis tint France et tot le Maine."""
        text = ner.tag_ner('french', input_text=text_str, output_type=str)
        target = ' Berte/Entity fu mere Charlemaine/Entity, qui pukis tint France/Entity et tot le Maine/Entity.'
        self.assertEqual(text, target)

if __name__ == '__main__':
    unittest.main()