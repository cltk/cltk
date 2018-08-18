"""Test for Middle English, based on Clément Besnier's test for Old Norse."""

import os
import unittest

from cltk.corpus.middle_english.alphabet import normalize_middle_english
from cltk.phonology.middle_english.transcription import Word as word_me
from cltk.stem.middle_english.stem import affix_stemmer as MiddleEnglishAffixStemmer
from cltk.tokenize.word import WordTokenizer


__author__ = ["John Stewart <johnstewart@aya.yale.edu>", ]


class TestMiddleEnglish(unittest.TestCase):
    def test_normalize_middle_english(self):
        """Tests Middle English normalizer"""
        in_test = "'Madame,' quod he, 'reule me As ȝ,e ly:k?eþ best.'"
        target = "'madame' quod he 'reule me as ye lyketh best'"
        test = normalize_middle_english(in_test)
        self.assertEqual(target, test)

    def test_middle_english_syllabify(self):
        """Test syllabification of Middle English"""

        words = ['marchall', 'content', 'thyne', 'greef', 'commaundyd']

        syllabified = [word_me(w).syllabify() for w in words]
        target_syllabified = [['mar', 'chall'], ['con', 'tent'], ['thyne'], ['greef'], ['com', 'mau', 'ndyd']]

        assert syllabified == target_syllabified

        syllabified_str = [word_me(w).syllabified_str() for w in words]
        target_syllabified_str = ['mar.chall', 'con.tent', 'thyne', 'greef', 'com.mau.ndyd']

        assert syllabified_str == target_syllabified_str

    def test_middle_english_stemmer(self):
        """Test stemming of Middle English"""
        sentence = ['the', 'speke', 'the', 'henmest', 'kyng', 'in', 'the', 'hillis', 'he', 'beholdis','he', 'lokis', 'vnder',
                    'his', 'hondis', 'and', 'his', 'hed', 'heldis']
        stemmed = MiddleEnglishAffixStemmer(sentence)
        target = 'the spek the henm kyng in the hill he behold he lok vnd his hond and his hed held'
        self.assertEqual(stemmed, target)

    def test_middle_english_tokenizer(self):
        text = "    Fers am I ferd of oure fare;\n Fle we ful fast þer-fore. \n Can Y no cownsel bot care.\n\n"
        target = ['Fers', 'am', 'I', 'ferd', 'of', 'oure', 'fare', ';', 'Fle', 'we', 'ful', 'fast', 'þer', '-', 'fore', '.',
                  'Can', 'Y', 'no', 'cownsel', 'bot', 'care', '.']
        tokenizer = WordTokenizer('middle_english')
        tokenized = tokenizer.tokenize(text)
        self.assertTrue(tokenized == target)


if __name__ == '__main__':
    unittest.main()
