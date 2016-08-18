"""Test cltk.tag."""

import os
import shutil
import unittest

from cltk.tokenize.word import WordTokenizer
from cltk.stem.latin.j_v import JVReplacer


    
from cltk.lemmatize.latin.backoff import DefaultLemmatizer, IdentityLemmatizer, ModelLemmatizer, UnigramLemmatizer, RegexpLemmatizer, PPLemmatizer, RomanNumeralLemmatizer

__author__ = 'Patrick J. Burns <patrick@diyclassics.org>'
__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):
    """Class for unittest"""

    def setUp(self):
        pass
        
        
    def test_default_lemmatizer(self):
        """
        """
        lemmatizer = DefaultLemmatizer('UNK')
        
        test_str = """Ceterum antequam destinata componam"""
        
        target = [('ceterum', 'UNK'), ('antequam', 'UNK'), ('destinata', 'UNK'), ('componam', 'UNK')]

        jv = JVReplacer()        
        tokenizer = WordTokenizer('latin')
        
        test_str = test_str.lower()
        test_str = jv.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        
        self.assertEqual(lemmas, target)
        
    def test_identity_lemmatizer(self):
        """
        """
        lemmatizer = IdentityLemmatizer()
        
        test_str = """Ceterum antequam destinata componam"""
        
        target = [('ceterum', 'ceterum'), ('antequam', 'antequam'), ('destinata', 'destinata'), ('componam', 'componam')]

        jv = JVReplacer()
        
        tokenizer = WordTokenizer('latin')
        
        test_str = test_str.lower()
        test_str = jv.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        
        self.assertEqual(lemmas, target)

    def test_model_lemmatizer(self):
        """
        """
        model = {'ceterum': 'ceterus', 'antequam': 'antequam', 'destinata': 'destino', 'componam': 'compono'}

        lemmatizer = ModelLemmatizer(model=model)

        test_str = """Ceterum antequam destinata componam"""
        
        target = [('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]

        jv = JVReplacer()
        
        tokenizer = WordTokenizer('latin')
        
        test_str = test_str.lower()
        test_str = jv.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        
        self.assertEqual(lemmas, target)

    def test_unigram_lemmatizer(self):
        """
        """
        train = [[('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]]

        lemmatizer = UnigramLemmatizer(train=train)

        test_str = """Ceterum antequam destinata componam"""
        
        target = [('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]

        jv = JVReplacer()
        
        tokenizer = WordTokenizer('latin')
        
        test_str = test_str.lower()
        test_str = jv.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        
        self.assertEqual(lemmas, target)

    def test_regex_lemmatizer(self):
        """
        """
        pattern = [(r'(\w*)abimus', 'o')]

        lemmatizer = RegexpLemmatizer(pattern)

        test_str = """amabimus"""
        
        target = [('amabimus', 'amo')]

        jv = JVReplacer()
        
        tokenizer = WordTokenizer('latin')
        
        test_str = test_str.lower()
        test_str = jv.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        
        self.assertEqual(lemmas, target)
    
    def test_latin_pp_lemmatizer(self):
        """
        """
        from cltk.lemmatize.latin.latin_regexp_patterns import latin_pps
        pattern = [(r'(\w*)[a|ie]bimus\b', 1)]

        lemmatizer = PPLemmatizer(pattern)

        test_str = """amabimus"""
        
        target = [('amabimus', 'amo')]

        jv = JVReplacer()
        
        tokenizer = WordTokenizer('latin')
        
        test_str = test_str.lower()
        test_str = jv.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        
        self.assertEqual(lemmas, target)
        
    def test_roman_numeral_lemmatizer(self):
        """
        """
        from cltk.lemmatize.latin.latin_regexp_patterns import rn_patterns
        
        lemmatizer = RomanNumeralLemmatizer(rn_patterns)

        test_str = """i ii iii iv v vi vii vii ix x xx xxx xl l lx c cc"""
        
        target = [('i', 'NUM'), ('ii', 'NUM'), ('iii', 'NUM'), ('iu', 'NUM'), ('u', 'NUM'), ('ui', 'NUM'), ('uii', 'NUM'), ('uii', 'NUM'), ('ix', 'NUM'), ('x', 'NUM'), ('xx', 'NUM'), ('xxx', 'NUM'), ('xl', 'NUM'), ('l', 'NUM'), ('lx', 'NUM'), ('c', 'NUM'), ('cc', 'NUM')]

        jv = JVReplacer()
        
        tokenizer = WordTokenizer('latin')

        test_str = test_str.lower()
        test_str = jv.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        
        self.assertEqual(lemmas, target)

if __name__ == '__main__':
    unittest.main()