"""Test cltk.tag."""

import os
import shutil
import unittest

from cltk.tokenize.word import WordTokenizer
from cltk.stem.latin.j_v import JVReplacer


    
from cltk.lemmatize.latin.backoff import DefaultLemmatizer, IdentityLemmatizer

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
        
        test_str = """Ceterum antequam destinata componam, repetendum uidetur qualis status urbis, quae mens exercituum, quis habitus prouinciarum, quid in toto terrarum orbe ualidum, quid aegrum fuerit, ut non modo casus euentusque rerum, qui plerumque fortuiti sunt, sed ratio etiam causaeque noscantur."""
        
        target = [('ceterum', 'UNK'), ('antequam', 'UNK'), ('destinata', 'UNK'), ('componam', 'UNK'), (',', 'UNK'), ('repetendum', 'UNK'), ('uidetur', 'UNK'), ('qualis', 'UNK'), ('status', 'UNK'), ('urbis', 'UNK'), (',', 'UNK'), ('quae', 'UNK'), ('mens', 'UNK'), ('exercituum', 'UNK'), (',', 'UNK'), ('quis', 'UNK'), ('habitus', 'UNK'), ('prouinciarum', 'UNK'), (',', 'UNK'), ('quid', 'UNK'), ('in', 'UNK'), ('toto', 'UNK'), ('terrarum', 'UNK'), ('orbe', 'UNK'), ('ualidum', 'UNK'), (',', 'UNK'), ('quid', 'UNK'), ('aegrum', 'UNK'), ('fuerit', 'UNK'), (',', 'UNK'), ('ut', 'UNK'), ('non', 'UNK'), ('modo', 'UNK'), ('casus', 'UNK'), ('euentus', 'UNK'), ('-que', 'UNK'), ('rerum', 'UNK'), (',', 'UNK'), ('qui', 'UNK'), ('plerumque', 'UNK'), ('fortuiti', 'UNK'), ('sunt', 'UNK'), (',', 'UNK'), ('sed', 'UNK'), ('ratio', 'UNK'), ('etiam', 'UNK'), ('causae', 'UNK'), ('-que', 'UNK'), ('noscantur', 'UNK'), ('.', 'UNK')]

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
        
        test_str = """Ceterum antequam destinata componam, repetendum uidetur qualis status urbis, quae mens exercituum, quis habitus prouinciarum, quid in toto terrarum orbe ualidum, quid aegrum fuerit, ut non modo casus euentusque rerum, qui plerumque fortuiti sunt, sed ratio etiam causaeque noscantur."""
        
        target = [('ceterum', 'ceterum'), ('antequam', 'antequam'), ('destinata', 'destinata'), ('componam', 'componam'), (',', ','), ('repetendum', 'repetendum'), ('uidetur', 'uidetur'), ('qualis', 'qualis'), ('status', 'status'), ('urbis', 'urbis'), (',', ','), ('quae', 'quae'), ('mens', 'mens'), ('exercituum', 'exercituum'), (',', ','), ('quis', 'quis'), ('habitus', 'habitus'), ('prouinciarum', 'prouinciarum'), (',', ','), ('quid', 'quid'), ('in', 'in'), ('toto', 'toto'), ('terrarum', 'terrarum'), ('orbe', 'orbe'), ('ualidum', 'ualidum'), (',', ','), ('quid', 'quid'), ('aegrum', 'aegrum'), ('fuerit', 'fuerit'), (',', ','), ('ut', 'ut'), ('non', 'non'), ('modo', 'modo'), ('casus', 'casus'), ('euentus', 'euentus'), ('-que', '-que'), ('rerum', 'rerum'), (',', ','), ('qui', 'qui'), ('plerumque', 'plerumque'), ('fortuiti', 'fortuiti'), ('sunt', 'sunt'), (',', ','), ('sed', 'sed'), ('ratio', 'ratio'), ('etiam', 'etiam'), ('causae', 'causae'), ('-que', '-que'), ('noscantur', 'noscantur'), ('.', '.')]

        jv = JVReplacer()
        
        tokenizer = WordTokenizer('latin')
        
        test_str = test_str.lower()
        test_str = jv.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        
        self.assertEqual(lemmas, target)

if __name__ == '__main__':
    unittest.main()