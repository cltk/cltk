import os
import shutil
import unittest

from cltk.corpus.utils.importer import CorpusImporter
from cltk.tag import ner_fr

class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_tag_ner_str_list_french(self):
        """Test make_ner(), str, list."""
        text_str = """Berte fu mere Charlemaine, qui pukis tint France et tot le Maine."""

        tokens = ner_fr.tag_ner_fr(input_text=text_str, output_type=list)
        target = [[('Berte', 'entity', 'CHI')], ('fu',), ('mere',), [('Charlemaine', 'entity', 'CHI')], (',',), ('qui',), ('pukis',),
                  ('tint',), [('France', 'entity', 'LOC')], ('et',), ('tot',), ('le',), [('Maine', 'entity', 'LOC')], ('.',)]
        self.assertEqual(tokens, target)

if __name__ == '__main__':
    unittest.main()