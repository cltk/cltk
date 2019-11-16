"""Test for Coptic, based on John Stewart's tests for Old English"""

import os
import unittest

from cltk.corpus.swadesh import Swadesh

__author__ = ["Edward Nolan <nolanee@umich.edu>", ]


class TestCoptic(unittest.TestCase):
    """Class for unittest"""

    # Swadesh list
    def test_swadesh_coptic(self):
        swadesh = Swadesh('cop')
        first_word = 'ⲁⲛⲟⲕ'
        match = swadesh.words()[0]
        self.assertEqual(first_word, match)
        turn = ['ⲡⲱⲱⲛⲉ', 'ⲕⲧⲟ']
        match = swadesh.words()[125]
        self.assertEqual(turn, match)
        match = len(swadesh.words())
        length = len(Swadesh('la').words())
        self.assertEqual(length, match)


if __name__ == '__main__':
    unittest.main()