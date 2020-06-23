"""The full unit test suite, testing every available model for every language."""

import unittest

import numpy

from cltkv1 import NLP
from cltkv1.languages.example_texts import get_example_text
from cltkv1.core.data_types import Doc, Word


class TestStringMethods(unittest.TestCase):

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_main_analyze(self):
        """Testing methods from ``cltkv1/nlp.py``. Note that we
        change ``first_word.embedding`` into an empty list because
        otherwise we would have to add a long vector into our tests.
        """
        lang = "grc"
        cltk_nlp = NLP(language=lang)
        cltk_doc = cltk_nlp.analyze(text=get_example_text(lang))
        first_word = cltk_doc.words[0]
        self.assertIsInstance(first_word.embedding, numpy.ndarray)
        first_word.embedding = list()
        target = Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='ὅτι', pos='ADV', lemma='ὅτι',
             scansion=None, xpos='Df', upos='ADV', dependency_relation='advmod', governor=6, features={}, embedding=[],
             stop=True, named_entity=False)
        self.assertEqual(first_word, target)

        lang = "chu"
        cltk_nlp = NLP(language=lang)
        cltk_doc = cltk_nlp.analyze(text=get_example_text(lang))
        first_word = cltk_doc.words[0]
        target = Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='отьчє', pos='NOUN',
             lemma='отьць', scansion=None, xpos='Nb', upos='NOUN', dependency_relation='vocative', governor=7,
             features={'Case': 'Voc', 'Gender': 'Masc', 'Number': 'Sing'}, embedding=None, stop=None, named_entity=None)
        self.assertEqual(first_word, target)

        lang = "fro"
        cltk_nlp = NLP(language=lang)
        cltk_doc = cltk_nlp.analyze(text=get_example_text(lang))
        first_word = cltk_doc.words[0]
        target = Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='Une', pos='DET', lemma=None,
             scansion=None, xpos='DETndf', upos='DET', dependency_relation=None, governor=-1,
             features={'Definite': 'Ind', 'PronType': 'Art'}, embedding=None, stop=False, named_entity=False)
        self.assertEqual(first_word, target)

        lang = "got"
        cltk_nlp = NLP(language=lang)
        cltk_doc = cltk_nlp.analyze(text=get_example_text(lang))
        first_word = cltk_doc.words[0]
        self.assertIsInstance(first_word.embedding, numpy.ndarray)
        first_word.embedding = list()
        target = Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='swa', pos='ADV', lemma='swa',
             scansion=None, xpos='Df', upos='ADV', dependency_relation='advmod', governor=1, features={}, embedding=[],
             stop=None, named_entity=None)
        self.assertEqual(first_word, target)
        self.assertEqual(len(cltk_doc.sentences), 3)

        lang = "cop"
        cltk_nlp = NLP(language=lang)
        cltk_doc = cltk_nlp.analyze(text=get_example_text(lang))
        first_word = cltk_doc.words[0]
        target = Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='ⲧⲏⲛ', pos='VERB', lemma='ⲧⲏⲛ', scansion=None, xpos='VSTAT', upos='VERB', dependency_relation='root', governor=-1, features={'VerbForm': 'Fin'}, embedding=None, stop=None, named_entity=None)
        self.assertEqual(first_word, target)

        lang = "lzh"
        cltk_nlp = NLP(language=lang)
        cltk_doc = cltk_nlp.analyze(text=get_example_text(lang))
        first_word = cltk_doc.words[0]
        target = Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='黃', pos='NOUN', lemma='黃',
             scansion=None, xpos='n,名詞,描写,形質', upos='NOUN', dependency_relation='nmod', governor=1, features={}, embedding=None,
             stop=None, named_entity=None)
        self.assertEqual(first_word, target)


if __name__ == "__main__":
    unittest.main()
