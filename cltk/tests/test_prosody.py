"""Test cltk.prosody."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.utils.importer import CorpusImporter
from cltk.prosody.latin.scanner import Scansion
import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_scanner_latin(self):
        """Test Latin prosody scanner."""
        scan = Scansion()
        meter = scan.scan_text('quō usque tandem abūtēre, Catilīna, patientiā nostrā. quam diū etiam furor iste tuus nōs ēlūdet.')
        self.assertEqual(meter, ['¯˘¯˘¯¯˘˘˘¯˘˘˘¯˘¯¯¯', '¯˘¯˘¯˘˘¯˘˘¯¯¯¯˘'])

    def test_long_by_nature(self):
        """Test Latin prosody scanner's `_long_by_nature` method."""
        scansion = Scansion()
        long_by_nat = scansion._long_by_nature('aet')
        self.assertTrue(long_by_nat)

    def test_long_by_position(self):
        """Test Latin prosody scanner's `_long_by_position` method."""
        scansion = Scansion()
        long_by_pos = scansion._long_by_position('am', ['quam', 'di', 'ūe', 'ti', 'am', 'fu', 'ror', 'i', 'ste', 'tu', 'us', 'nōs', 'ē', 'lū', 'det'])
        self.assertTrue(long_by_pos)

    def test_syllabify_latin(self):
        """Test syllabifier for Latin scanner code."""
        scansion = Scansion()
        syllables = [['quō', 'usque', 'tandem', 'abūtēre', ',', 'catilīna', ',', 'patientiā', 'nostrā.'], ['quam', 'diū', 'etiam', 'furor', 'iste', 'tuus', 'nōs', 'ēlūdet.']]
        elided_target = [[[], ['quōu', 'sque'], ['ta'], ['ndema', 'bū', 'tē', 're'], ['ca', 'ti', 'lī', 'na'], ['pa', 'ti', 'e', 'nti', 'ā'], ['no', 'strā']], [['quam'], ['di'], ['ūe', 'ti', 'am'], ['fu', 'ror'], ['i', 'ste'], ['tu', 'us'], ['nōs'], ['ē', 'lū', 'det']]]
        elided = scansion.syllabify(syllables)
        self.assertEqual(elided, elided_target)

    def test_elidable_begin_latin(self):
        """Test elidable word beginnings for Latin."""
        scansion = Scansion()
        elidable_begin = scansion._elidable_begin(['hae', 're', 'na'])
        self.assertTrue(elidable_begin)

    def test_elidable_end_latin(self):
        """Test elidable word endings for Latin."""
        scansion = Scansion()
        elidable_end = scansion._elidable_end(['fi', 'li', 'ae'])
        self.assertTrue(elidable_end)

if __name__ == '__main__':
    unittest.main()
