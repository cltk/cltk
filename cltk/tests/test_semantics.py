"""Test cltk.lemmatize."""

import unittest

from cltk.semantics.latin.semantics import Lemmatize
#from cltk.lemmatize.latin.regexp_patterns import rn_patterns
from cltk.stem.latin.j_v import JVReplacer
from cltk.tokenize.word import WordTokenizer
from cltk.corpus.utils.importer import CorpusImporter
from cltk.lemmatize.french.lemma import LemmaReplacer
import os

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>', 'Natasha Voake <natashavoake@gmail.com>', 'James Gawley <james.gawley@gmail.com']
__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):
    """Class for unittest"""

    def test_lemmatize(self):
        """Test Lemmatizer()"""
        lemmatizer = Lemmatize('multiple_lemmata')
        test_str = 'Ceterum antequam destinata componam'
        target = [('ceterum', [('ceterus', 1.0)]), ('antequam', [('antequam', 1.0)]), ('destinata', [('destinatus', 0.25), ('destinatum', 0.25), ('destinata', 0.25), ('destino', 0.25)]), ('componam', [('compono', 1.0)])]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)


if __name__ == '__main__':
    unittest.main()
