"""Test ``cltk.alphabet``."""

__license__ = "MIT License. See LICENSE."

import unicodedata
import unittest

from cltk.alphabet.grc.grc import normalize_grc


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_normalize_grc(self):
        """Test for normalizing grc input"""
        source = "Ἡροδότου Ἁλικαρνησσέος ἱστορίης ἀπόδεξις ἥδε"
        source_nfd = unicodedata.normalize("NFD", source)
        target = normalize_grc(source_nfd)
        self.assertEqual(source, target)


if __name__ == "__main__":
    unittest.main()
