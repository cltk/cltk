__author__ = ['Natasha Voake <natashavoake@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

from cltk.normalize.normalize import normalize
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_normalize(self):
        """Test french normalizer"""
        text = "viw"
        normalized = normalize(text)
        target = ['vieux']
        self.assertEqual(normalized, target)

if __name__ == '__main__':
    unittest.main()