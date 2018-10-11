"""Test for Old English, based on Clément Besnier's test for Old Norse."""

import os
import unittest

from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.swadesh import Swadesh
from cltk.tag.pos import POSTag
from cltk.phonology.syllabify import Syllabifier

__author__ = ["John Stewart <johnstewart@aya.yale.edu>", ]


class TestOldEnglish(unittest.TestCase):
    """Class for unittest"""
    def setUp(self):
        corpus_importer = CorpusImporter("old_english")
        corpus_importer.import_corpus("old_english_models_cltk")
        file_rel = os.path.join('~/cltk_data/old_english/model/old_english_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    # Swadesh list
    def test_swadesh_old_english(self):
        swadesh = Swadesh('eng_old')
        first_word = 'ic, iċċ, ih'
        match = swadesh.words()[0]
        self.assertEqual(first_word, match)

    def test_syllabification_old_english(self):
        s = Syllabifier(language='old_english')
        self.assertEqual(s.syllabify('geardagum'), ['gear', 'da', 'gum'])

    def test_pos_unigram_old_english(self):
        """Test tagging Old English POS with unigram tagger."""
        tagger = POSTag('old_english')
        tagged = tagger.tag_unigram('Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon.')
        self.assertTrue(tagged)

    def test_pos_bigram_old_english(self):
        """Test tagging Old English POS with bigram tagger."""
        tagger = POSTag('old_english')
        tagged = tagger.tag_bigram('Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon.')
        self.assertTrue(tagged)

    def test_pos_trigram_old_english(self):
        """Test tagging old_english POS with trigram tagger."""
        tagger = POSTag('old_english')
        tagged = tagger.tag_trigram('Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon.')
        self.assertTrue(tagged)

    def test_pos_ngram123_tagger_old_english(self):
        """Test tagging Old English POS with a 1-, 2-, and 3-gram backoff tagger."""
        tagger = POSTag('old_english')
        tagged = tagger.tag_ngram_123_backoff('Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon.')  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_crf_tagger_old_english(self):
        """Test tagging Old English POS with CRF tagger."""
        tagger = POSTag('old_english')
        tagged = tagger.tag_crf('Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon.')
        self.assertTrue(tagged)

    def test_pos_perceptron_tagger_old_english(self):
        """Test tagging Old English POS with Perceptron tagger."""
        tagger = POSTag('old_english')
        tagged = tagger.tag_perceptron('Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon.')
        self.assertTrue(tagged)


if __name__ == '__main__':
    unittest.main()
