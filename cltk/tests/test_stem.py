"""Test cltk.stem."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.utils.importer import CorpusImporter
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.latin.stem import Stemmer
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.syllabifier import Syllabifier
import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

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

if __name__ == '__main__':
    unittest.main()
