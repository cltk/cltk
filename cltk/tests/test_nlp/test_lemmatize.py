"""Test cltk.lemmatize."""
import os
import unittest
from unittest.mock import patch

from cltk.stem.latin.j_v import JVReplacer
from cltk.tokenize.word import WordTokenizer
from cltk.corpus.utils.importer import CorpusImporter

from cltk.lemmatize.backoff import DefaultLemmatizer
from cltk.lemmatize.backoff import IdentityLemmatizer
from cltk.lemmatize.backoff import UnigramLemmatizer
from cltk.lemmatize.backoff import DictLemmatizer
from cltk.lemmatize.backoff import RegexpLemmatizer

from cltk.lemmatize.latin.backoff import BackoffLatinLemmatizer
from cltk.lemmatize.latin.backoff import RomanNumeralLemmatizer # Removed temporarily

from cltk.lemmatize.greek.backoff import BackoffGreekLemmatizer

from cltk.lemmatize.french.lemma import LemmaReplacer

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>', 'Natasha Voake <natashavoake@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):
    """Class for unittest"""

    def setUp(self):
        corpus_importer = CorpusImporter('french')
        corpus_importer.import_corpus('french_data_cltk')
        file_rel = os.path.join('~/cltk_data/french/text/french_data_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_default_lemmatizer(self):
        """Test default_lemmatizer()"""
        lemmatizer = DefaultLemmatizer('UNK')
        test_str = 'Ceterum antequam destinata componam'
        target = [('ceterum', 'UNK'), ('antequam', 'UNK'), ('destinata', 'UNK'), ('componam', 'UNK')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_identity_lemmatizer(self):
        """Test identity_lemmatizer()"""
        lemmatizer = IdentityLemmatizer()
        test_str = 'Ceterum antequam destinata componam'
        target = [('ceterum', 'ceterum'), ('antequam', 'antequam'), ('destinata', 'destinata'), ('componam', 'componam')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_dict_lemmatizer(self):
        """Test model_lemmatizer()"""
        lemmas = {'ceterum': 'ceterus', 'antequam': 'antequam', 'destinata': 'destino', 'componam': 'compono'}  # pylint: disable=line-too-long
        lemmatizer = DictLemmatizer(lemmas=lemmas)
        test_str = 'Ceterum antequam destinata componam'
        target = [('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_unigram_lemmatizer(self):
        """Test unigram_lemmatizer()"""
        train = [[('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]]  # pylint: disable=line-too-long
        lemmatizer = UnigramLemmatizer(train=train)
        test_str = """Ceterum antequam destinata componam"""
        target = [('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_regex_lemmatizer(self):
        """Test regex_lemmatizer()"""
        sub = [('(.)ab(o|is|it|imus|itis|unt)$', r'\1o')]
        lemmatizer = RegexpLemmatizer(sub)
        test_str = 'amabimus'
        target = [('amabimus', 'amo')]
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_roman_numeral_lemmatizer(self):
        """Test roman_numeral_lemmatizer()"""
        lemmatizer = RomanNumeralLemmatizer()
        test_str = 'i ii iii iv v vi vii vii ix x xx xxx xl l lx c cc'
        target = [('i', 'NUM'), ('ii', 'NUM'), ('iii', 'NUM'), ('iu', 'NUM'), ('u', 'NUM'), ('ui', 'NUM'), ('uii', 'NUM'), ('uii', 'NUM'), ('ix', 'NUM'), ('x', 'NUM'), ('xx', 'NUM'), ('xxx', 'NUM'), ('xl', 'NUM'), ('l', 'NUM'), ('lx', 'NUM'), ('c', 'NUM'), ('cc', 'NUM')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = test_str.split()
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_roman_numeral_lemmatizer_default(self):
        """Test roman_numeral_lemmatizer()"""
        lemmatizer = RomanNumeralLemmatizer(default="RN")
        test_str = 'i ii iii'
        target = [('i', 'RN'), ('ii', 'RN'), ('iii', 'RN')]
        tokens = test_str.split()
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_backoff_latin_lemmatizer(self):
        """Test backoffLatinLemmatizer"""
        train = [[('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]]  # pylint: disable=line-too-long
        lemmatizer = BackoffLatinLemmatizer()
        test_str = """Ceterum antequam destinata componam"""
        target = [('ceterum', 'ceterum'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_backoff_latin_lemmatizer_verbose(self):
        """Test backoffLatinLemmatizer"""
        train = [[('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]]  # pylint: disable=line-too-long
        lemmatizer = BackoffLatinLemmatizer(verbose=True)
        test_str = """Ceterum antequam destinata componam"""
        target = [('ceterum', 'ceterum', '<UnigramLemmatizer: CLTK Sentence Training Data>'), ('antequam', 'antequam', '<UnigramLemmatizer: CLTK Sentence Training Data>'), ('destinata', 'destino', '<UnigramLemmatizer: CLTK Sentence Training Data>'), ('componam', 'compono', '<DictLemmatizer: Morpheus Lemmas>')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_backoff_latin_lemmatizer_evaluate(self):
        """Test backoffLatinLemmatizer evaluate method"""
        lemmatizer = BackoffLatinLemmatizer(verbose=False)
        accuracy = lemmatizer.evaluate()
        self.assertTrue(.85 <= accuracy <= 1)

    def test_backoff_latin_lemmatizer_evaluate_verbose(self):
        """Test backoffLatinLemmatizer evaluate method"""
        lemmatizer = BackoffLatinLemmatizer(verbose=True)
        with self.assertRaises(AssertionError):
            accuracy = lemmatizer.evaluate()

    def test_backoff_latin_lemmatizer_models_not_present(self):
        """Test whether models are present for BackoffLatinLemmatizer"""
        with patch.object(BackoffLatinLemmatizer,'models_path',''):
            with self.assertRaises(FileNotFoundError):
                lemmatizer = BackoffLatinLemmatizer()

    def test_backoff_greek_lemmatizer(self):
        """Test backoffLatinLemmatizer"""
        train = [[('χθὲς', 'χθές'), ('εἰς', 'εἰς'), ('μετὰ', 'μετά'), ('τοῦ', 'ὁ')]]  # pylint: disable=line-too-long
        lemmatizer = BackoffGreekLemmatizer()
        test_str = """κατέβην χθὲς εἰς Πειραιᾶ μετὰ Γλαύκωνος τοῦ Ἀρίστωνος"""
        # NB: Look at χθὲς in the training data
        target = [('κατέβην', 'καταβαίνω'), ('χθὲς', 'χθὲς'), ('εἰς', 'εἰς'), ('Πειραιᾶ', 'Πειραιεύς'), ('μετὰ', 'μετά'), ('Γλαύκωνος', 'Γλαύκων'), ('τοῦ', 'ὁ'), ('Ἀρίστωνος', 'Ἀρίστων')]  # pylint: disable=line-too-long
        tokens = test_str.split()
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_backoff_greek_lemmatizer_models_not_present(self):
        """Test whether models are present for BackoffGreekLemmatizer"""
        with patch.object(BackoffGreekLemmatizer,'models_path',''):
            with self.assertRaises(FileNotFoundError):
                lemmatizer = BackoffGreekLemmatizer()

    def test_french_lemmatizer(self):
        text = "Li rois pense que par folie, Sire Tristran, vos aie amé ; Mais Dé plevis ma loiauté, Qui sor mon cors mete flaele, S'onques fors cil qui m’ot pucele Out m'amistié encor nul jor !"
        text = str.lower(text)
        tokenizer = WordTokenizer('french')
        lemmatizer = LemmaReplacer()
        tokens = tokenizer.tokenize(text)
        lemmas = lemmatizer.lemmatize(tokens)
        target = [('li', 'li'), ('rois', 'rois'), ('pense', 'pense'), ('que', 'que'), ('par', 'par'), ('folie', 'folie'), (',', ['PUNK']), ('sire', 'sire'), ('tristran', 'None'), (',', ['PUNK']), ('vos', 'vos'), ('aie', ['avoir']), ('amé', 'amer'), (';', ['PUNK']), ('mais', 'mais'), ('dé', 'dé'), ('plevis', 'plevir'), ('ma', 'ma'), ('loiauté', 'loiauté'), (',', ['PUNK']), ('qui', 'qui'), ('sor', 'sor'), ('mon', 'mon'), ('cors', 'cors'), ('mete', 'mete'), ('flaele', 'flaele'), (',', ['PUNK']), ("s'", "s'"), ('onques', 'onques'), ('fors', 'fors'), ('cil', 'cil'), ('qui', 'qui'), ("m'", "m'"), ('ot', 'ot'), ('pucele', 'pucele'), ('out', ['avoir']), ("m'", "m'"), ('amistié', 'amistié'), ('encor', 'encor'), ('nul', 'nul'), ('jor', 'jor'), ('!', ['PUNK'])]
        self.assertEqual(lemmas, target)

if __name__ == '__main__':
    unittest.main()
