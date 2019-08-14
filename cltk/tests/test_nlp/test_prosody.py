"""Test cltk.prosody."""

__license__ = 'MIT License. See LICENSE.'

from cltk.prosody.latin.scanner import Scansion as ScansionLatin
from cltk.prosody.latin.clausulae_analysis import Clausulae
from cltk.prosody.greek.scanner import Scansion as ScansionGreek
from cltk.prosody.latin.macronizer import Macronizer
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    """greek/scanner.py"""
    # Test string for Greek prosody module unit testing
    test = "νέος μὲν καὶ ἄπειρος, δικῶν ἔγωγε ἔτι. μὲν καὶ ἄπειρος."

    def test_clean_text_greek(self):
        """Test _clean_text method."""
        correct = "νέος μὲν καὶ ἄπειρος δικῶν ἔγωγε ἔτι. μὲν καὶ ἄπειρος."
        current = ScansionGreek()._clean_text(self.test)
        self.assertEqual(current, correct)

    def test_clean_accents_greek(self):
        """Test _clean_accents method."""
        correct = "νεος μεν και απειρος δικων εγωγε ετι. μεν και απειρος."
        current = ScansionGreek()._clean_accents(self.test)
        self.assertEqual(current, correct)

    def test_tokenize_greek(self):
        """Test _tokenize method."""
        correct = [['νεος', 'μεν', 'και', 'απειρος', 'δικων', 'εγωγε', 'ετι.'],
                   ['μεν', 'και', 'απειρος.']]
        current = ScansionGreek()._tokenize(self.test)
        self.assertEqual(current, correct)

    def test_make_syllables_greek(self):
        """Test _make_syllables method."""
        correct = [[['νε', 'ος'], ['μεν'], ['και'], ['α', 'πει', 'ρος'],
                   ['δι', 'κων'], ['ε', 'γω', 'γε'], ['ε', 'τι']], [['μεν'],
                   ['και'], ['α', 'πει', 'ρος']]]
        current = ScansionGreek()._make_syllables(self.test)
        self.assertEqual(current, correct)

    def test_scan_text_greek(self):
        """Test scan_text method."""
        correct = ['˘¯¯¯˘¯¯˘¯˘¯˘˘x', '¯¯˘¯x']
        current = ScansionGreek().scan_text(self.test)
        self.assertEqual(current, correct)

    """latin/macronizer.py"""
    def test_retrieve_morpheus_entry(self):
        """ Text Macronizer()._retrieve_morpheus_tag()"""
        correct = [('n-s---fb-', 'puella', 'puellā'), ('n-s---fn-', 'puella', 'puella'), ('n-s---fv-', 'puella', 'puella')]
        current = Macronizer("tag_ngram_123_backoff")._retrieve_morpheus_entry("puella")
        self.assertEqual(current, correct)

    def test_macronize_word(self):
        """Test Macronizer()._macronize_word()"""
        correct = ('flumine', 'n-s---nb-', 'flūmine')
        current = Macronizer("tag_ngram_123_backoff")._macronize_word(('flumine', 'n-s---nb-'))
        self.assertEqual(current, correct)

    def test_macronize_tags(self):
        """Test Macronizer().macronize_tags()"""
        text = "Quo usque tandem, O Catilina, abutere nostra patientia?"
        correct = [('quo', 'd--------', 'quō'), ('usque', 'd--------', 'usque'), ('tandem', 'd--------', 'tandem'), (',', 'u--------', ','), ('o', 'e--------', 'ō'), ('catilina', 'n-s---mb-', 'catilīnā'), (',', 'u--------', ','), ('abutere', 'v2sfip---', 'abūtēre'), ('nostra', 'a-s---fb-', 'nostrā'), ('patientia', 'n-s---fn-', 'patientia'), ('?', None, '?')]
        current = Macronizer("tag_ngram_123_backoff").macronize_tags(text)
        self.assertEqual(current, correct)

    def test_macronize_text(self):
        """Test Macronizer().macronize_text()"""
        text = "Quo usque tandem, O Catilina, abutere nostra patientia?"
        correct = "quō usque tandem , ō catilīnā , abūtēre nostrā patientia ?"
        current = Macronizer("tag_ngram_123_backoff").macronize_text(text)
        self.assertEqual(current, correct)


if __name__ == '__main__':
    unittest.main()
