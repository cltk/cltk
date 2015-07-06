import unittest
from cltk.prosody.latin.scanner import Scansion

class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    def test_latin(self):
        s = Scansion()
        m = s.scan_text('quō usque tandem abūtēre, Catilīna, patientiā nostrā. quam diū etiam furor iste tuus nōs ēlūdet.')
        self.assertEqual(m, ['¯˘¯˘¯¯˘˘˘¯˘˘˘¯˘¯¯¯', '¯˘¯˘¯˘˘¯˘˘¯¯¯¯˘'])

if __name__ == '__main__':
    unittest.main()