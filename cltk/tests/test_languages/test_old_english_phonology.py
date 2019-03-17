"""Test for Old English, based on Clément Besnier's test for Old Norse."""

import os
import unittest

from cltk.phonology.old_english.orthophonology import oe

__author__ = ["John Stewart <johnstewart@aya.yale.edu>", ]


class TestOldEnglish(unittest.TestCase):
    """Class for unittest"""

    def test_transcriber_æċed(self):
        self.assertEqual(oe.transcribe('æċed'), 'æt͡ʃed')

    def test_transcriber_ic(self):
        self.assertEqual(oe.transcribe('ic'), 'it͡ʃ')

    def test_transcriber_scip(self):
        self.assertEqual(oe.transcribe('scip'), 'ʃip')

    def test_transcriber_ascian(self):
        self.assertEqual(oe.transcribe('ascian'), 'ɑskiɑn')

    def test_transcriber_þurhbregdan(self):
        self.assertEqual(oe.transcribe('þurhbregdan'), 'θurxbrejdɑn')

    def test_transcriber_hamsteall(self):
        self.assertEqual(oe.transcribe('hamsteall'), 'hɑmstæɑll')




if __name__ == '__main__':
    unittest.main()
