"""Test cltk.lemmatize."""

import unittest

from cltk.semantics.latin.lookup import Lemmata
from cltk.semantics.latin.lookup import Synonyms
#from cltk.lemmatize.latin.regexp_patterns import rn_patterns
from cltk.stem.latin.j_v import JVReplacer
from cltk.tokenize.word import WordTokenizer
from cltk.corpus.utils.importer import CorpusImporter
from cltk.lemmatize.french.lemma import LemmaReplacer
import os

__author__ = ['James Gawley <james.gawley@gmail.com', 'Patrick J. Burns <patrick@diyclassics.org>', 'Natasha Voake <natashavoake@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):
    """Class for unittest"""

    def test_latin_lemmata(self):
        """Test Lemmata class lookup() method"""
        lemmatizer = Lemmata(dictionary = 'lemmata', language = 'latin')
        test_str = 'Ceterum antequam destinata componam'
        target = [('ceterum', [('ceterus', 1.0)]), ('antequam', [('antequam', 1.0)]), ('destinata', [('destinatus', 0.25), ('destinatum', 0.25), ('destinata', 0.25), ('destino', 0.25)]), ('componam', [('compono', 1.0)])]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lookup(tokens)
        self.assertEqual(lemmas, target)

    def test_latin_synonyms(self):
        """Test Synonym class lookup() function and Lemmata class isolate() method"""
        #first build the lemma list as in test_latin_lemmata()
        lemmatizer = Lemmata(dictionary = 'lemmata', language = 'latin')
        test_str = 'Ceterum antequam destinata componam'
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lookup(tokens)
        #now isolate the list of lemmas
        lemmas = lemmatizer.isolate(lemmas)
        synonyms = Synonyms(dictionary = 'synonyms', language = 'latin')
        syns = synonyms.lookup_synonyms(lemmas)
        target = [('ceterus', [('ceteroqui', 0.5), ('perquiesco', 0.5)]), ('compono', [('struo', 0.5), ('condo', 0.5)])]
        self.assertEqual(syns, target)

    def test_latin_translations(self):
        """Test Synonym class lookup() function and Lemmata class isolate() method"""
        #first build the lemma list as in test_latin_lemmata()
        lemmatizer = Lemmata(dictionary = 'lemmata', language = 'latin')
        test_str = 'Ceterum antequam destinata componam'
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lookup(tokens)
        #now isolate the list of lemmas
        lemmas = lemmatizer.isolate(lemmas)
        translations = Synonyms(dictionary = 'translations', language = 'latin')
        translations = translations.lookup_synonyms(lemmas)
        target = [('destino', [('σκοπός', 1.0)]), ('compono', [('συντίθημι', 1.0)])]
        self.assertEqual(translations, target)

if __name__ == '__main__':
    unittest.main()

