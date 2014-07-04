"""Unit tests for CLTK
"""

from cltk.corpus.classical_greek.beta_to_unicode import Replacer
from cltk.stem.classical_latin.j_and_v_converter import JVReplacer
from cltk.stop.classical_greek.stops_unicode import GREEK_STOPS_LIST
from cltk.stop.classical_latin.stops import LATIN_STOPS_LIST
from nltk.tokenize.punkt import PunktWordTokenizer
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def test_latin_i_u_transform(self):
        """Test conversion of j to i and v to u"""
        j = JVReplacer()
        trans = j.replace('vem jam VEL JAM')
        self.assertEqual(trans, 'uem iam UEL IAM')

    def test_latin_stopwords(self):
        """Filter Latin stopwords"""
        SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'
        lowered = SENTENCE.lower()
        tokens = PunktWordTokenizer().tokenize(lowered)
        no_stops = [w for w in tokens if not w in LATIN_STOPS_LIST]
        target_list = ['usque', 'tandem', 'abutere', ',', 'catilina', ',', 'patientia', 'nostra', '?']
        self.assertEqual(no_stops, target_list)

    def test_greek_stopwords(self):
        """Filter Greek stopwords"""
        sentence = """Ἅρπαγος δὲ καταστρεψάμενος Ἰωνίην ἐποιέετο στρατηίην ἐπὶ Κᾶρας καὶ Καυνίους καὶ Λυκίους, ἅμα ἀγόμενος καὶ Ἴωνας καὶ Αἰολέας."""
        lowered = sentence.lower()
        tokens = PunktWordTokenizer().tokenize(lowered)
        no_stops = [w for w in tokens if not w in GREEK_STOPS_LIST]
        target_list = ['ἅρπαγος', 'καταστρεψάμενος', 'ἰωνίην', 'ἐποιέετο', 'στρατηίην', 'κᾶρας', 'καυνίους', 'λυκίους', ',', 'ἅμα', 'ἀγόμενος', 'ἴωνας', 'αἰολέας.']
        self.assertEqual(no_stops, target_list)

    def test_greek_betacode_to_unicode(self):
        """Test conversion of betacode to unicode
        note: assertEqual appears to not be correctly comparing certain characters (ά and ί, at least)
        """
        BETA_EXAMPLE = r"""O(/PWS OU)=N MH\ TAU)TO\ """
        r = Replacer()
        unicode = r.beta_code(BETA_EXAMPLE)
        target_unicode = 'ὅπωσ οὖν μὴ ταὐτὸ '
        self.assertEqual(unicode, target_unicode)

if __name__ == '__main__':
    unittest.main()
