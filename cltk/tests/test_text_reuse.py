"""Test cltk.text_reuse."""

__author__ = 'Luke Hollis <lukehollis@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.text_reuse.levenshtein import Levenshtein


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_distance_ratio(self):
        """Test returning simple Levenshtein distance calculation ratio between two strings"""
        l = Levenshtein()
        ratio = l.ratio("dique deaeque omnes, studium quibus arua tueri,", "dique deaeque omnes, quibus est tutela per agros,")
        self.assertEqual(ratio, 0.71)
