"""Test cltk.reuse."""

__license__ = 'MIT License. See LICENSE.'

import unittest

from cltk.reuse.levenshtein import Levenshtein



class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_levenshtein_sent_latin(self):
        """Test Latin Levenshtein setence comparison."""
        leven = Levenshtein()
        sent_1 = "Duos cum haberet Demea adulescentulos, dat Micioni fratri adoptandum Aeschinum, sed Ctesiphonem retinet. hunc citharistriae lepore captum sub duro ac tristi patre frater celabat Aeschinus; famam rei, amorem in sese transferebat; denique fidicinam lenoni eripit."  # pylint: disable=line-too-long
        sent_2 = "Tres cum haberet Demea adulescentulos, dat Micioni fratri adoptandum Aeschinum, sed Ctesiphonem retinet. hunc citharistriae lepore captum sub duro ac tristi patre frater celabat Aeschinus; famam rei, amorem in sese transferebat; denique fidicinam lenoni eripit."  # pylint: disable=line-too-long
        ratios = leven.distance_sentences('latin', sent_1, sent_2)
        self.assertEqual(ratios, [[0.97, 0.43], [0.42, 1.0]])

    def test_levenshtein_sent_greek(self):
        """Test Greek Levenshtein setence comparison."""
        leven = Levenshtein()
        sent_1 = "ὥστε καὶ δὴ τοὔνομ᾽ αὐτῆς ἐν ἀγορᾷ κυλίνδεται. ἢν μὲν ὠνῆταί τις ὀρφὼς μεμβράδας δὲ μὴ 'θέλῃ, εὐθέως εἴρηχ᾽ ὁ πωλῶν πλησίον τὰς μεμβράδας: οὗτος ὀψωνεῖν ἔοιχ᾽ ἅνθρωπος ἐπὶ τυραννίδι."
        sent_2 = "ὥστε καὶ δὴ τοὔνομ᾽ αὐτῆς ἐν ἀγορᾷ κυλίνδεται. ἢν μὲν ὠνῆταί τις ὀρφὼς μεμβράδας δὲ μὴ 'θέλῃ."
        ratios = leven.distance_sentences('latin', sent_1, sent_2)
        self.assertEqual(ratios, [[1.0, 0.26], [0.26, 0.66], [0.34, 0.29]])


    def test_levenshtein_string(self):
        """Test Levenshtein string comparison."""
        leven = Levenshtein()
        str_1 = 'Duos cum haberet Demea adulescentulos'
        str_2 = 'Tres cum haberet Demea adulescentulos'
        ratio = leven.distance(str_1, str_2)
        self.assertEqual(ratio, 0.92)


if __name__ == '__main__':
    unittest.main()
