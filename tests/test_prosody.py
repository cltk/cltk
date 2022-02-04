"""Test cltk.prosody."""

__license__ = "MIT License. See LICENSE."

import unittest

from cltk.prosody.lat.clausulae_analysis import Clausulae
from cltk.prosody.lat.macronizer import Macronizer
from cltk.prosody.lat.scanner import Scansion as ScansionLatin


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    # lat/macronizer.py
    def test_retrieve_morpheus_entry(self):
        """Text Macronizer()._retrieve_morpheus_tag()"""
        correct = [
            ("n-s---fb-", "puella", "puellā"),
            ("n-s---fn-", "puella", "puella"),
            ("n-s---fv-", "puella", "puella"),
        ]
        current = Macronizer("tag_ngram_123_backoff")._retrieve_morpheus_entry("puella")
        self.assertEqual(current, correct)

    def test_macronize_word(self):
        """Test Macronizer()._macronize_word()"""
        correct = ("flumine", "n-s---nb-", "flūmine")
        current = Macronizer("tag_ngram_123_backoff")._macronize_word(
            ("flumine", "n-s---nb-")
        )
        self.assertEqual(current, correct)

    def test_macronize_tags(self):
        """Test Macronizer().macronize_tags()"""
        text = "Quo usque tandem, O Catilina, abutere nostra patientia?"
        correct = [
            ("quo", "d--------", "quō"),
            ("usque", "d--------", "usque"),
            ("tandem", "d--------", "tandem"),
            (",", "u--------", ","),
            ("o", "e--------", "ō"),
            ("catilina", "n-s---mb-", "catilīnā"),
            (",", "u--------", ","),
            ("abutere", "v2sfip---", "abūtēre"),
            ("nostra", "a-s---fb-", "nostrā"),
            ("patientia", "n-s---fn-", "patientia"),
            ("?", None, "?"),
        ]
        current = Macronizer("tag_ngram_123_backoff").macronize_tags(text)
        self.assertEqual(current, correct)

    def test_macronize_text(self):
        """Test Macronizer().macronize_text()"""
        text = "Quo usque tandem, O Catilina, abutere nostra patientia?"
        correct = "quō usque tandem , ō catilīnā , abūtēre nostrā patientia ?"
        current = Macronizer("tag_ngram_123_backoff").macronize_text(text)
        self.assertEqual(current, correct)


if __name__ == "__main__":
    unittest.main()
