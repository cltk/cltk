"""Test cltk.ner."""

from cltk.ner import ner
from cltk.stem.latin.j_v import JVReplacer
import os
import unittest

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_check_latest_latin(self):
        """Test _check_latest_data()"""
        ner._check_latest_data('latin')
        names_path = os.path.expanduser('~/cltk_data/latin/model/latin_models_cltk/ner/proper_names.txt')
        self.assertTrue(os.path.isfile(names_path))

    def test_tag_ner_str_list_latin(self):
        """Test make_ner(), str, list."""
        text_str = """ut Venus, ut Sirius, ut Spica, ut aliae quae primae dicuntur esse mangitudinis."""
        jv_replacer = JVReplacer()
        text_str_iu = jv_replacer.replace(text_str)
        tokens = ner.tag_ner('latin', input_text=text_str_iu, output_type=list)
        target = [('ut',), ('Uenus', 'Entity'), (',',), ('ut',), ('Sirius', 'Entity'), (',',), ('ut',), ('Spica', 'Entity'), (',',), ('ut',), ('aliae',), ('quae',), ('primae',), ('dicuntur',), ('esse',), ('mangitudinis',), ('.',)]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_list_latin(self):
        """Test make_ner(), list, list."""
        text_list = ['ut', 'Venus', 'Sirius']
        jv_replacer = JVReplacer()
        text_list_iu = [jv_replacer.replace(x) for x in text_list]
        tokens = ner.tag_ner('latin', input_text=text_list_iu, output_type=list)
        target = [('ut',), ('Uenus', 'Entity'), ('Sirius', 'Entity')]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_str_latin(self):
        """Test make_ner(), list, str."""
        text_list = ['ut', 'Venus', 'Sirius']
        jv_replacer = JVReplacer()
        text_list_iu = [jv_replacer.replace(x) for x in text_list]
        text = ner.tag_ner('latin', input_text=text_list_iu, output_type=str)
        target = ' ut Uenus/Entity Sirius/Entity'
        self.assertEqual(text, target)

    def test_tag_ner_str_str_latin(self):
        """Test make_ner(), str, str."""
        jv_replacer = JVReplacer()
        text_str = """ut Venus, ut Sirius, ut Spica, ut aliae quae primae dicuntur esse mangitudinis."""
        jv_replacer = JVReplacer()
        text_str_iu = jv_replacer.replace(text_str)
        text = ner.tag_ner('latin', input_text=text_str_iu, output_type=str)
        target = ' ut Uenus/Entity, ut Sirius/Entity, ut Spica/Entity, ut aliae quae primae dicuntur esse mangitudinis.'
        self.assertEqual(text, target)

    def test_tag_ner_str_list_greek(self):
        """Test make_ner(), str, list."""
        text_str = 'τὰ Σίλαριν Σιννᾶν Κάππαρος Πρωτογενείας Διονυσιάδες τὴν'
        tokens = ner.tag_ner('greek', input_text=text_str, output_type=list)
        target = [('τὰ',), ('Σίλαριν', 'Entity'), ('Σιννᾶν', 'Entity'), ('Κάππαρος', 'Entity'), ('Πρωτογενείας', 'Entity'), ('Διονυσιάδες', 'Entity'), ('τὴν',)]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_list_greek(self):
        """Test make_ner(), list, list."""
        text_list = ['τὰ', 'Σίλαριν', 'Σιννᾶν']
        tokens = ner.tag_ner('greek', input_text=text_list, output_type=list)
        target = [('τὰ',), ('Σίλαριν', 'Entity'), ('Σιννᾶν', 'Entity')]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_str_greek(self):
        """Test make_ner(), list, str."""
        text_list = ['τὰ', 'Σίλαριν', 'Σιννᾶν']
        text = ner.tag_ner('greek', input_text=text_list, output_type=str)
        target = ' τὰ Σίλαριν/Entity Σιννᾶν/Entity'
        self.assertEqual(text, target)

    def test_tag_ner_str_str_greek(self):
        """Test make_ner(), str, str."""
        text_str = 'τὰ Σίλαριν Σιννᾶν Κάππαρος Πρωτογενείας Διονυσιάδες τὴν'
        text = ner.tag_ner('greek', input_text=text_str, output_type=str)
        target = ' τὰ Σίλαριν/Entity Σιννᾶν/Entity Κάππαρος/Entity Πρωτογενείας/Entity Διονυσιάδες/Entity τὴν'
        self.assertEqual(text, target)

if __name__ == '__main__':
    unittest.main()
