# text encoded in following encoding: utf-8

"""Test cltk.tokenize.

TODO: Add tests for the Indian lang tokenizers: from cltk.tokenize.indian_tokenizer import indian_punctuation_tokenize_regex
"""

from cltk.corpus.utils.importer import CorpusImporter
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import nltk_tokenize_words
from cltk.tokenize.word import WordTokenizer
from cltk.tokenize.line import LineTokenizer
import os
import unittest

__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""


    #def test_sentence_tokenizer_french(self):
    #    """Test tokenizing French sentences."""
    #    text = "S'a table te veulz maintenir, Honnestement te dois tenir Et garder les enseignemens Dont cilz " \
    #           "vers sont commancemens. Chacun doit estre coutumiers De penser des povres premiers, Car li saoul " \
    #           "si ne scet mie Com le jeun a dure vie. A viande nulz main ne mette Jusques la beneisson soit faitte. " \
    #           "Ne t'assiez pas, je te conseille, Se bien ne sces que l'en le vueille. Ne mangue mie, je te commande," \
    #           " Avant que on serve de vïande, Car il sembleroit que tu feusses Trop glout, ou que trop fain eusses. " \
    #           "Du pain que mis as en ta bouche, A ton escuelle point n'atouche. Ongles polis et nais les dois Ayes, " \
    #           "ainsi tenir te dois Qu'aux compaignons ne soit grevance, Ne autres ne facent nuissance. Vïande au" \
    #           " sel de la salliere N'atouche, c'est laide manière. Tes narilles fourgier ne vueilles De tes doies, " \
    #           "ne tes oreilles."
    #    target = [
    #        "S'a table te veulz maintenir, Honnestement te dois tenir Et garder les enseignemens Dont cilz vers sont commancemens.",
    #        "Chacun doit estre coutumiers De penser des povres premiers, Car li saoul si ne scet mie Com le jeun a dure vie.",
    #        "A viande nulz main ne mette Jusques la beneisson soit faitte.",
    #        "Ne t'assiez pas, je te conseille, Se bien ne sces que l'en le vueille.",
    #        "Ne mangue mie, je te commande, Avant que on serve de vïande, Car il sembleroit que tu feusses Trop glout, ou que trop fain eusses.",
    #        "Du pain que mis as en ta bouche, A ton escuelle point n'atouche.",
    #        "Ongles polis et nais les dois Ayes, ainsi tenir te dois Qu\'aux compaignons ne soit grevance, Ne autres ne facent nuissance.",
    #        "Vïande au sel de la salliere N'atouche, c'est laide manière.",
    #        "Tes narilles fourgier ne vueilles De tes doies, ne tes oreilles."]
    #    tokenizer = TokenizeSentence('french')
    #    tokenized_sentences = tokenizer.tokenize_sentences(text)
    #    self.MaxDiff = none
    #    assert_equal.__self__.maxDiff = None
    #    self.assertEqual(tokenized_sentences, target)


    def test_french_word_tokenizer(self):
        """Test French-specific word tokenizer."""
        word_tokenizer = WordTokenizer('french')

        # Test sources:
        # - Wace - St George
        # - Marie de France - Guigemar
        #

        tests = ["S'a table te veulz maintenir, Honnestement te dois tenir Et garder les enseignemens Dont cilz vers sont commancemens."]

        results = []

        for test in tests:
            result = word_tokenizer.tokenize(test)
            results.append(result)

        target = [["S'", 'a', 'table', 'te', 'veulz', 'maintenir', ',', 'Honnestement', 'te', 'dois', 'tenir', 'Et', 'garder', 'les', 'enseignemens', 'Dont', 'cilz', 'vers', 'sont', 'commancemens', '.']]

        self.assertEqual(results, target)

    def test_nltk_tokenize_words(self):
        """Test wrapper for NLTK's PunktLanguageVars()"""
        tokens = nltk_tokenize_words("Sentence 1. Sentence 2.", attached_period=False)
        target = ['Sentence', '1', '.', 'Sentence', '2', '.']
        self.assertEqual(tokens, target)

    def test_nltk_tokenize_words_attached(self):
        """Test wrapper for NLTK's PunktLanguageVars(), returning unaltered output."""
        tokens = nltk_tokenize_words("Sentence 1. Sentence 2.", attached_period=True)
        target = ['Sentence', '1.', 'Sentence', '2.']
        self.assertEqual(tokens, target)

    def test_sanskrit_nltk_tokenize_words(self):
        """Test wrapper for NLTK's PunktLanguageVars()"""
        tokens = nltk_tokenize_words("कृपया।", attached_period=False, language='sanskrit')
        target = ['कृपया', '।']
        self.assertEqual(tokens, target)

    def test_sanskrit_nltk_tokenize_words_attached(self):
        """Test wrapper for NLTK's PunktLanguageVars(), returning unaltered output."""
        tokens = nltk_tokenize_words("कृपया।", attached_period=True, language='sanskrit')
        target = ['कृपया।']
        self.assertEqual(tokens, target)

    def test_nltk_tokenize_words_assert(self):
        """Test assert error for CLTK's word tokenizer."""
        with self.assertRaises(AssertionError):
            nltk_tokenize_words(['Sentence', '1.'])


    def test_line_tokenizer(self):
        """Test LineTokenizer"""
        text = """Ki de bone matire traite,\nmult li peise, se bien n’est faite.\nOëz, seignur, que dit Marie,\nki en sun tens pas ne s’oblie. """
        target = ['Ki de bone matire traite,', 'mult li peise, se bien n’est faite.','Oëz, seignur, que dit Marie,', 'ki en sun tens pas ne s’oblie. ']
        tokenizer = LineTokenizer('french')
        tokenized_lines = tokenizer.tokenize(text)
        self.assertTrue(tokenized_lines == target)

    def test_line_tokenizer_include_blanks(self):
        """Test LineTokenizer"""
        text = """Ki de bone matire traite,\nmult li peise, se bien n’est faite.\nOëz, seignur, que dit Marie,\nki en sun tens pas ne s’oblie.\n\nLes contes que jo sai verais,\ndunt li Bretun unt fait les lais,\nvos conterai assez briefment."""
        target = ['Ki de bone matire traite,', 'mult li peise, se bien n’est faite.','Oëz, seignur, que dit Marie,', 'ki en sun tens pas ne s’oblie.','','Les contes que jo sai verais,','dunt li Bretun unt fait les lais,','vos conterai assez briefment.']
        tokenizer = LineTokenizer('french')
        tokenized_lines = tokenizer.tokenize(text, include_blanks=True)
        self.assertTrue(tokenized_lines == target)


if __name__ == '__main__':
    unittest.main()
