from syllabifier import Syllabifier
import unittest


class testing_syl_indic(unittest.TestCase):
    def test_syllabify(self):
        """Test Indic Syllabifier method"""
        correct = ['न', 'म', 'स्ते']
        syllabifier = Syllabifier('hindi')
        current = syllabifier.orthographic_syllabify('नमस्ते')
        self.assertEqual(current, correct)

    def test_get_offset(self):
        """Test Indic Syllabifier get_offset method"""
        correct = 40
        syllabifier = Syllabifier('hindi')
        current = syllabifier.get_offset('न', 'hi')
        self.assertEqual(current, correct)

    def test_coordinated_range(self):
        """Test Indic Syllabifier in_coordinated_range method"""
        syllabifier = Syllabifier('hindi')
        current = syllabifier.get_offset('न', 'hi')
        current1 = syllabifier.in_coordinated_range_offset(current)
        self.assertTrue(current1)

    """
    def test_phonetic_vector(self):
        cor = [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0]
        correct = bytearray(cor)
        syllabifier = Syllabifier('hindi')
        current = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertTrue(current, correct)
    """

    def test_is_misc(self):
        """Test Indic Syllabifier is_misc method"""
        syllabifier = Syllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_misc(v))

    def test_is_consonant(self):
        """Test Indic Syllabifier is_consonant method"""
        syllabifier = Syllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertTrue(syllabifier.is_consonant(v))

    def test_is_vowel(self):
        """Test Indic Syllabifier is_vowel method"""
        syllabifier = Syllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_vowel(v))

    def test_is_anusvaar(self):
        """Test Indic Syllabifier is_anusvaar method"""
        syllabifier = Syllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_anusvaar(v))

    def test_is_plosive(self):
        """Test Indic Syllabifier is_plosive method"""
        syllabifier = Syllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertTrue(syllabifier.is_plosive(v))

    def test_is_nukta(self):
        """Test Indic Syllabifier is_nukta method"""
        syllabifier = Syllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_nukta(v))

    def test_is_valid(self):
        """Test Indic Syllabifier is_valid method"""
        syllabifier = Syllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertTrue(syllabifier.is_valid(v))

    def test_is_dependent_vowel(self):
        """Test Indic Syllabifier is_dependent_vowel method"""
        syllabifier = Syllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_dependent_vowel(v))


if __name__ == '__main__':
    unittest.main()