"""Test ``cltk.alphabet``."""

__license__ = "MIT License. See LICENSE."

import unicodedata
import unittest

from cltk.alphabet.grc import beta_to_unicode
from cltk.alphabet.grc.grc import normalize_grc


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_normalize_grc(self):
        """Test for normalizing grc input"""
        source = "Ἡροδότου Ἁλικαρνησσέος ἱστορίης ἀπόδεξις ἥδε"
        source_nfd = unicodedata.normalize("NFD", source)
        target = normalize_grc(source_nfd)
        self.assertEqual(source, target)

    def test_beta_to_unicode_grc_reorder(self):
        """Test reordering of diacritics"""
        source = ["w/)", "w/|)", "*w/|)", "*)w"]
        expected = ["w)/", "w)/|", "*w)/|", "*w)"]
        conv = beta_to_unicode.BetaCodeReplacer(pattern=[("", "")])
        target = [conv.replace_beta_code(case) for case in source]
        self.assertEqual(expected, target)

    def test_beta_to_unicode_grc_converter(self):
        """Test full conversion algorithm"""
        source = [
            r"proi+sxome/nwn",
            r"*Xaldai+kh\n",
            r"*xaldai+kh\n",
            r"*XALDAI+KH\N",
            "di' o(/",
            "*)A",
            "*)=A",
            "o(/s3a",
        ]
        expected = [
            "προϊσχομένων",
            "Χαλδαϊκὴν",
            "Χαλδαϊκὴν",
            "Χαλδαϊκὴν",
            "διʼ ὅ",
            "Ἀ",
            "Ἆ",
            "ὅϲα",
        ]
        conv = beta_to_unicode.BetaCodeReplacer()
        target = [conv.replace_beta_code(case) for case in source]
        self.assertEqual(expected, target)


if __name__ == "__main__":
    unittest.main()
