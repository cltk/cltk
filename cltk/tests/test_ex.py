"""unit tests for CLTK
"""

from cltk.stop.classical_latin.stops import STOPS_LIST
from cltk.stem.classical_latin.j_and_v_converter import JVReplacer
import nltk.tokenize
import random
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, list(range(10)))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

    def test_latin_i_u_transform(self):
        """Test conversion of j to i and v to u"""
        j = JVReplacer()
        trans = j.replace('vem jam VEL JAM')
        self.assertEqual(trans, 'uem iam UEL IAM')

    def test_latin_stopwords(self):
        """filter Latin stopwords"""
        SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'
        lowered = SENTENCE.lower()
        tokens = nltk.word_tokenize(lowered)
        no_stops = [w for w in tokens if not w in STOPS_LIST]
        target_list = ['usque', 'tandem', 'abutere', ',', 'catilina', ',', 'patientia', 'nostra', '?']
        self.assertEqual(no_stops, target_list)


if __name__ == '__main__':
    unittest.main()
