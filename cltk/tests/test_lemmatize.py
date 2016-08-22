"""Test cltk.lemmatize."""

import unittest

from cltk.lemmatize.latin.backoff import DefaultLemmatizer
from cltk.lemmatize.latin.backoff import IdentityLemmatizer
from cltk.lemmatize.latin.backoff import ModelLemmatizer
from cltk.lemmatize.latin.backoff import PPLemmatizer
from cltk.lemmatize.latin.backoff import RegexpLemmatizer
from cltk.lemmatize.latin.backoff import RomanNumeralLemmatizer
from cltk.lemmatize.latin.backoff import UnigramLemmatizer
from cltk.lemmatize.latin.regexp_patterns import rn_patterns
from cltk.stem.latin.j_v import JVReplacer
from cltk.tokenize.word import WordTokenizer

__author__ = 'Patrick J. Burns <patrick@diyclassics.org>'
__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):
    """Class for unittest"""

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

    def test_model_lemmatizer(self):
        """Test model_lemmatizer()"""
        model = {'ceterum': 'ceterus', 'antequam': 'antequam', 'destinata': 'destino', 'componam': 'compono'}  # pylint: disable=line-too-long
        lemmatizer = ModelLemmatizer(model=model)
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
        pattern = [(r'(\w*)abimus', 'o')]
        lemmatizer = RegexpLemmatizer(pattern)
        test_str = 'amabimus'
        target = [('amabimus', 'amo')]
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_latin_pp_lemmatizer(self):
        """Test latin_pp_lemmatizer()"""
        pattern = [(r'(\w*)[a|ie]bimus\b', 1)]
        lemmatizer = PPLemmatizer(pattern)
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
        lemmatizer = RomanNumeralLemmatizer(rn_patterns)
        test_str = 'i ii iii iv v vi vii vii ix x xx xxx xl l lx c cc'
        target = [('i', 'NUM'), ('ii', 'NUM'), ('iii', 'NUM'), ('iu', 'NUM'), ('u', 'NUM'), ('ui', 'NUM'), ('uii', 'NUM'), ('uii', 'NUM'), ('ix', 'NUM'), ('x', 'NUM'), ('xx', 'NUM'), ('xxx', 'NUM'), ('xl', 'NUM'), ('l', 'NUM'), ('lx', 'NUM'), ('c', 'NUM'), ('cc', 'NUM')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

if __name__ == '__main__':
    unittest.main()
