"""Test cltk.stem."""

import unittest

from cltk.core.exceptions import CLTKException
from cltk.data.fetch import FetchCorpus
from cltk.stem.latin.stem import Stemmer
from cltk.stem.middle_english.stem import affix_stemmer as MiddleEnglishAffixStemmer
from cltk.stem.sanskrit.indian_syllabifier import Syllabifier as IndianSyllabifier


class TestStemmingFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    # def setUp(self):
    #     """Import sanskrit models first, some CSV files necessary for the
    #     Indian lang tokenizers.
    #     """
    #     corpus_importer = FetchCorpus('sanskrit')
    #     corpus_importer.import_corpus('sanskrit_models_cltk')
    #     file_rel = os.path.join(get_cltk_data_dir() + '/sanskrit/model/sanskrit_models_cltk/README.md')
    #     file = os.path.expanduser(file_rel)
    #     file_exists = os.path.isfile(file)
    #     self.assertTrue(file_exists)

    @classmethod
    def setUpClass(self):
        try:
            corpus_importer = FetchCorpus("san")
            corpus_importer.import_corpus("san_models_cltk")
            corpus_importer = FetchCorpus("grc")
            corpus_importer.import_corpus("grc_models_cltk")
        except:
            raise Exception("Failure to download test corpus")

    """
    def test_latin_stemmer(self):
        """Test Latin stemmer."""
        sentence = "Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum."  # pylint: disable=line-too-long
        stemmer = Stemmer()
        stemmed_text = stemmer.stem(sentence.lower())
        target = "est interd praestar mercatur r quaerere, nisi tam periculos sit, et it foenerari, si tam honestum. "  # pylint: disable=line-too-long
        self.assertEqual(stemmed_text, target)
    """



    def test_syllabify(self):
        """Test Indic Syllabifier method"""
        correct = ["न", "म", "स्ते"]
        syllabifier = IndianSyllabifier("hindi")
        current = syllabifier.orthographic_syllabify("नमस्ते")
        self.assertEqual(current, correct)

    def test_get_offset(self):
        """Test Indic Syllabifier get_offset method"""
        correct = 40
        syllabifier = IndianSyllabifier("hindi")
        current = syllabifier.get_offset("न", "hi")
        self.assertEqual(current, correct)

    def test_coordinated_range(self):
        """Test Indic Syllabifier in_coordinated_range method"""
        syllabifier = IndianSyllabifier("hindi")
        current = syllabifier.get_offset("न", "hi")
        current1 = syllabifier.in_coordinated_range_offset(current)
        self.assertTrue(current1)

    """
    #? Someone fix this; assertTrue() doesn't make sense here
    def test_phonetic_vector(self):
        cor = [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0]
        correct = bytearray(cor)
        syllabifier = IndianSyllabifier('hindi')
        current = syllabifier.get_phonetic_feature_vector('न', 'hi')
        # self.assertTrue(current, correct)
    """

    def test_is_misc(self):
        """Test Indic Syllabifier is_misc method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertFalse(syllabifier.is_misc(v))

    def test_is_consonant(self):
        """Test Indic Syllabifier is_consonant method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertTrue(syllabifier.is_consonant(v))

    def test_is_vowel(self):
        """Test Indic Syllabifier is_vowel method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertFalse(syllabifier.is_vowel(v))

    def test_is_anusvaar(self):
        """Test Indic Syllabifier is_anusvaar method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertFalse(syllabifier.is_anusvaar(v))

    def test_is_plosive(self):
        """Test Indic Syllabifier is_plosive method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertTrue(syllabifier.is_plosive(v))

    def test_is_nukta(self):
        """Test Indic Syllabifier is_nukta method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertFalse(syllabifier.is_nukta(v))

    def test_is_valid(self):
        """Test Indic Syllabifier is_valid method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertTrue(syllabifier.is_valid(v))

    def test_is_dependent_vowel(self):
        """Test Indic Syllabifier is_dependent_vowel method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertFalse(syllabifier.is_dependent_vowel(v))

    
    """
    def french_stemmer_test(self):
        sentence = (
            "ja departissent a itant quant par la vile vint errant tut a cheval "
            "une pucele en tut le siecle n'ot si bele un blanc palefrei chevalchot"
        )
        stemmed_text = stem(sentence)
        target = (
            "j depart a it quant par la vil v err tut a cheval un pucel en tut le siecl n' o si bel un blanc palefre"
            " chevalcho "
        )
        self.assertEqual(stemmed_text, target)
    """

    def test_middle_english_stemmer(self):
        sentence = [
            "the",
            "speke",
            "the",
            "henmest",
            "kyng",
            "in",
            "the",
            "hillis",
            "he",
            "beholdis",
            "he",
            "lokis",
            "vnder",
            "his",
            "hondis",
            "and",
            "his",
            "hed",
            "heldis",
        ]
        stemmed = MiddleEnglishAffixStemmer(sentence)
        target = "the spek the henm kyng in the hill he behold he lok vnd his hond and his hed held"
        self.assertEqual(stemmed, target)

    


if __name__ == "__main__":
    unittest.main()
