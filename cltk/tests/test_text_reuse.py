"""Test cltk.text_reuse."""

__author__ = 'Luke Hollis <lukehollis@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import unittest
from cltk.text_reuse.levenshtein import Levenshtein
from cltk.text_reuse.text_reuse import TextReuse


demo_verg = """
tuque o, cui prima frementem
fudit equum magno tellus percussa tridenti,
Neptune; et cultor nemorum, cui pinguia Ceae
ter centum niuei tondent dumeta iuuenci;
ipse nemus linquens patrium saltusque Lycaei
Pan, ouium custos, tua si tibi Maenala curae,
adsis, o Tegeaee, fauens, oleaeque Minerua
inuentrix, uncique puer monstrator aratri,
et teneram ab radice ferens, Siluane, cupressum:
dique deaeque omnes, studium quibus arua tueri,
munera vestra cano. et vos o agrestum praesentia
quique nouas alitis non ullo semine fruges
quique satis largum caelo demittitis imbrem.
"""

demo_prop = """
corniger Arcadii vacuam pastoris in aulam
dux aries saturas ipse reduxit oves;
dique deaeque omnes, quibus est tutela per agros,
praebebant vestri verba benigna foci:
'et leporem, quicumque venis, venaberis, hospes,
et si forte meo tramite quaeris avem:
et me Pana tibi comitem de rupe vocato,
sive petes calamo praemia, sive cane.'
at nunc desertis cessant sacraria lucis:
aurum omnes victa iam pietate colunt.
auro pulsa fides, auro venalia iura,
aurum lex sequitur, mox sine lege pudor.
"""

class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_distance_ratio(self):
        """Test returning simple Levenshtein distance calculation ratio between two strings"""
        l = Levenshtein()
        ratio = l.ratio("dique deaeque omnes, studium quibus arua tueri,", "dique deaeque omnes, quibus est tutela per agros,")
        self.assertEqual(ratio, 0.71)

    def test_distance_sentences(self):
        """Test comparing two passages tokenized at the sentence level"""
        t = TextReuse()
        comparisons = t.compare_sentences(demo_verg, demo_prop)
        self.assertEqual(comparisons[1][0]['ratio'], 0.39)

    def test_distance_sliding_window(self):
        """Test comparing two passages with the sliding window strategy"""
        t = TextReuse()
        comparisons = t.compare_sliding_window(demo_verg, demo_prop)
        self.assertEqual(comparisons[19][3]['ratio'], 0.64)
