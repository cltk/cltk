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

    def test_transcriber_fricativization(self):
        self.assertEqual(oe.transcribe('arstafas'), 'ɑrstɑvɑs')
        self.assertEqual(oe.transcribe('sceaft'), 'ʃæɑft')

    def test_trascriber_g(self):
        self.assertEqual(oe.transcribe('ige'), 'ije')
        self.assertEqual(oe.transcribe('itgu'), 'itgu')
        self.assertEqual(oe.transcribe('igu'), 'iɣu')
        self.assertEqual(oe('dagas'), 'dɑɣɑs')

    def test_transcriber_cæg(self):
        self.assertEqual(oe.transcribe('cæg'), 'kæj')

    def test_wynn(self):
        self.assertEqual(oe('tƿirædness'), 'twirædness')

    def test_ng(self):
        self.assertEqual(oe('singan'), 'siŋgɑn')
        self.assertEqual(oe('panc'), 'pɑŋk')

    def test_cyrice(self):
        self.assertEqual(oe('cyrice'), 't͡ʃyrit͡ʃe')

    def test_ecg(self):
        self.assertEqual(oe('ecg'), 'ed͡ʒ')


if __name__ == '__main__':
    unittest.main()
