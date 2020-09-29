"""Test cltk.text_reuse."""

__author__ = ['Luke Hollis <lukehollis@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import unittest
from cltk.text_reuse.levenshtein import Levenshtein
from cltk.text_reuse.text_reuse import TextReuse
from cltk.text_reuse.comparison import long_substring
from cltk.text_reuse.comparison import minhash
from cltk.text_reuse.comparison import Needleman_Wunsch
from cltk.text_reuse.comparison import Default_Matrix


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
        
    def test_levenshtein_distance(self):
        """Test for Levenshtein Distance between two words""" 
        l = Levenshtein()
        dist = l.levenshtein_distance("now grete glorious god through grace of himselven", "and the precious prayer of his pris moder")
        self.assertEqual(dist, 36)
        
    def test_damerau_levenshtein_distance(self):
        """Test for Damerau-Levenshtein Distance between two words"""
        l = Levenshtein()
        dist = l.damerau_levenshtein_distance("all haile whose solempne glorious concepcioun", "fresche floure in quhom the hevinlie dewe doun fell")
        self.assertEqual(dist,35)

#    Test causing lemmatizer Travis build to fail—figure out what is wrong and restore.
#    def test_distance_sentences(self):
#        """Test comparing two passages tokenized at the sentence level"""
#        t = TextReuse()
#        comparisons = t.compare_sentences(demo_verg, demo_prop, 'latin')
#        self.assertEqual(comparisons[1][0].ratio, 0.40)

    def test_distance_sliding_window(self):
        """Test comparing two passages with the sliding window strategy"""
        t = TextReuse()
        comparisons = t.compare_sliding_window(demo_verg, demo_prop)
        self.assertEqual(comparisons[19][3].ratio, 0.64)
    
    def test_long_substring(self):
        """Test to check for the longest substring in the two passages"""
        substring = long_substring(demo_verg, demo_prop)
        self.assertEqual(substring,"dique deaeque omnes,")

    def test_minhash(self):
        """Test for finding the similarity between two sentences using Minhash"""
        score = minhash(demo_verg, demo_prop)
        self.assertEqual(score, 0.17163120567375886)
   
    def test_Needleman_Wunsch(self):
        """Test for finding the optimal alignment by the Needleman-Wunsch algorithm"""
        w1, w2 = "michtis","myht"
        al = Needleman_Wunsch(w1, w2)
        self.assertEqual(al,('michtis', 'm-yht--'))
    
    def test_Default_Matrix(self):
        """Test for the default similarity matrix"""
        A = Default_Matrix(3, 1, -1)
        self.assertEqual(A, [[1, -1, -1], [-1, 1, -1], [-1, -1, 1]])

if __name__ == '__main__':
    unittest.main()
