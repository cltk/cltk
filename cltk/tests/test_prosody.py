"""Test cltk.prosody."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.prosody.latin.scanner import Scansion as ScansionLatin
from cltk.prosody.greek.scanner import Scansion as ScansionGreek
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_scanner_latin(self):
        """Test Latin prosody scanner."""
        scan = ScansionLatin()
        meter = scan.scan_text('quō usque tandem abūtēre, Catilīna, patientiā nostrā. quam diū etiam furor iste tuus nōs ēlūdet.')
        self.assertEqual(meter, ['¯˘¯˘¯¯˘˘˘¯˘˘˘¯˘¯¯x', '¯˘¯˘¯˘˘¯˘˘¯¯¯¯x'])

    def test_long_by_nature_latin(self):
        """Test Latin prosody scanner's `_long_by_nature` method."""
        scansion = ScansionLatin()
        long_by_nat = scansion._long_by_nature('aet')
        self.assertTrue(long_by_nat)

    def test_long_by_position_latin(self):
        """Test Latin prosody scanner's `_long_by_position` method."""
        scansion = ScansionLatin()
        long_by_pos = scansion._long_by_position('am', ['quam', 'di', 'ūe', 'ti', 'am', 'fu', 'ror', 'i', 'ste', 'tu', 'us', 'nōs', 'ē', 'lū', 'det'])
        self.assertTrue(long_by_pos)

    def test_syllabify_latin(self):
        """Test syllabifier for Latin scanner code."""
        scansion = ScansionLatin()
        syllables = [['quō', 'usque', 'tandem', 'abūtēre', ',', 'catilīna', ',', 'patientiā', 'nostrā.'], ['quam', 'diū', 'etiam', 'furor', 'iste', 'tuus', 'nōs', 'ēlūdet.']]
        elided_target = [[[], ['quōu', 'sque'], ['ta'], ['ndema', 'bū', 'tē', 're'], ['ca', 'ti', 'lī', 'na'], ['pa', 'ti', 'e', 'nti', 'ā'], ['no', 'strā']], [['quam'], ['di'], ['ūe', 'ti', 'am'], ['fu', 'ror'], ['i', 'ste'], ['tu', 'us'], ['nōs'], ['ē', 'lū', 'det']]]
        elided = scansion.syllabify(syllables)
        self.assertEqual(elided, elided_target)

    def test_elidable_begin_latin(self):
        """Test elidable word beginnings for Latin."""
        scansion = ScansionLatin()
        elidable_begin = scansion._elidable_begin(['hae', 're', 'na'])
        self.assertTrue(elidable_begin)

    def test_elidable_end_latin(self):
        """Test elidable word endings for Latin."""
        scansion = ScansionLatin()
        elidable_end = scansion._elidable_end(['fi', 'li', 'ae'])
        self.assertTrue(elidable_end)

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

if __name__ == '__main__':
    unittest.main()
