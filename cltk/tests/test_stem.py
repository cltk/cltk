"""Test cltk.stem."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.utils.importer import CorpusImporter
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.latin.stem import Stemmer
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.syllabifier import Syllabifier as IndianSyllabifier
from cltk.stem.sanskrit.indian_syllabifier import Syllabifier

import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        """Import sanskrit models first, some CSV files necessary for the
        Indian lang tokenizers.
        """
        corpus_importer = CorpusImporter('sanskrit')
        corpus_importer.import_corpus('sanskrit_models_cltk')
        file_rel = os.path.join('~/cltk_data/sanskrit/model/sanskrit_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_latin_i_u_transform(self):
        """Test converting ``j`` to ``i`` and ``v`` to ``u``."""
        jv_replacer = JVReplacer()
        trans = jv_replacer.replace('vem jam VEL JAM')
        self.assertEqual(trans, 'uem iam UEL IAM')

    def test_latin_stemmer(self):
        """Test Latin stemmer."""
        sentence = 'Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum.'  # pylint: disable=line-too-long
        stemmer = Stemmer()
        stemmed_text = stemmer.stem(sentence.lower())
        target = 'est interd praestar mercatur r quaerere, nisi tam periculos sit, et it foenerari, si tam honestum. '  # pylint: disable=line-too-long
        self.assertEqual(stemmed_text, target)

    def test_lemmatizer_inlist_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=False)
        target = ['homo', 'divus', 'voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=False)
        target = ['hominum/homo', 'divomque/divus', 'voluptas/voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=True)
        target = 'homo divus voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=True)
        target = 'hominum/homo divomque/divus voluptas/voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=False)
        target = ['homo', 'divus', 'voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=False)
        target = ['hominum/homo', 'divomque/divus', 'voluptas/voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=True)
        target = 'homo divus voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=True)
        target = 'hominum/homo divomque/divus voluptas/voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=False)
        target = ['τὴν', 'διάγνωσις', 'ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=False)
        target = ['τὴν/τὴν', 'διάγνωσιν/διάγνωσις', 'ἔρχεσθαι/ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=True)
        target = 'τὴν διάγνωσις ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=True)
        target = 'τὴν/τὴν διάγνωσιν/διάγνωσις ἔρχεσθαι/ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=False)
        target = ['τὴν', 'διάγνωσις', 'ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=False)
        target = ['τὴν/τὴν', 'διάγνωσιν/διάγνωσις', 'ἔρχεσθαι/ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=True)
        target = 'τὴν διάγνωσις ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=True)
        target = 'τὴν/τὴν διάγνωσιν/διάγνωσις ἔρχεσθαι/ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_latin_syllabifier(self):
        """Test Latin syllabifier."""
        word = 'sidere'
        syllabifier = Syllabifier()
        syllables = syllabifier.syllabify(word)
        target = ['si', 'de', 're']
        self.assertEqual(syllables, target)

    def test_syllabify(self):
        """Test Indic Syllabifier method"""
        correct = ['न', 'म', 'स्ते']
        syllabifier = IndianSyllabifier('hindi')
        current = syllabifier.orthographic_syllabify('नमस्ते')
        self.assertEqual(current, correct)

    def test_get_offset(self):
        """Test Indic Syllabifier get_offset method"""
        correct = 40
        syllabifier = IndianSyllabifier('hindi')
        current = syllabifier.get_offset('न', 'hi')
        self.assertEqual(current, correct)

    def test_coordinated_range(self):
        """Test Indic Syllabifier in_coordinated_range method"""
        syllabifier = IndianSyllabifier('hindi')
        current = syllabifier.get_offset('न', 'hi')
        current1 = syllabifier.in_coordinated_range_offset(current)
        self.assertTrue(current1)

    '''
    #? Someone fix this; assertTrue() doesn't make sense here
    def test_phonetic_vector(self):
        cor = [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0]
        correct = bytearray(cor)
        syllabifier = IndianSyllabifier('hindi')
        current = syllabifier.get_phonetic_feature_vector('न', 'hi')
        # self.assertTrue(current, correct)
    '''

    def test_is_misc(self):
        """Test Indic Syllabifier is_misc method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_misc(v))

    def test_is_consonant(self):
        """Test Indic Syllabifier is_consonant method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertTrue(syllabifier.is_consonant(v))

    def test_is_vowel(self):
        """Test Indic Syllabifier is_vowel method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_vowel(v))

    def test_is_anusvaar(self):
        """Test Indic Syllabifier is_anusvaar method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_anusvaar(v))

    def test_is_plosive(self):
        """Test Indic Syllabifier is_plosive method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertTrue(syllabifier.is_plosive(v))

    def test_is_nukta(self):
        """Test Indic Syllabifier is_nukta method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_nukta(v))

    def test_is_valid(self):
        """Test Indic Syllabifier is_valid method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertTrue(syllabifier.is_valid(v))

    def test_is_dependent_vowel(self):
        """Test Indic Syllabifier is_dependent_vowel method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_dependent_vowel(v))


if __name__ == '__main__':
    unittest.main()
