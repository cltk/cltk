"""Test cltk.lemmatize."""
import os
import unittest
from unittest.mock import patch

from cltk.data.fetch import FetchCorpus
from cltk.lemmatize.backoff import (
    DefaultLemmatizer,
    DictLemmatizer,
    IdentityLemmatizer,
    RegexpLemmatizer,
    UnigramLemmatizer,
)
from cltk.lemmatize.grc import GreekBackoffLemmatizer, models_path
from cltk.lemmatize.lat import (
    LatinBackoffLemmatizer,
    RomanNumeralLemmatizer,
    models_path,
)
from cltk.text.lat import replace_jv
from cltk.tokenizers.lat.lat import LatinWordTokenizer
from cltk.utils import CLTK_DATA_DIR

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License. See LICENSE."


class TestSequenceFunctions(unittest.TestCase):
    """Class for unittest"""

    def test_dict_lemmatizer(self):
        """Test model_lemmatizer()"""
        lemmas = {
            "ceterum": "ceterus",
            "antequam": "antequam",
            "destinata": "destino",
            "componam": "compono",
        }
        lemmatizer = DictLemmatizer(lemmas=lemmas)
        test_str = "Ceterum antequam destinata componam"
        target = [
            ("ceterum", "ceterus"),
            ("antequam", "antequam"),
            ("destinata", "destino"),
            ("componam", "compono"),
        ]  # pylint: disable=line-too-long
        tokenizer = LatinWordTokenizer()
        test_str = test_str.lower()
        test_str = replace_jv(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_unigram_lemmatizer(self):
        """Test unigram_lemmatizer()"""
        train = [
            [
                ("ceterum", "ceterus"),
                ("antequam", "antequam"),
                ("destinata", "destino"),
                ("componam", "compono"),
            ]
        ]  # pylint: disable=line-too-long
        lemmatizer = UnigramLemmatizer(train=train)
        test_str = """Ceterum antequam destinata componam"""
        target = [
            ("ceterum", "ceterus"),
            ("antequam", "antequam"),
            ("destinata", "destino"),
            ("componam", "compono"),
        ]  # pylint: disable=line-too-long
        tokenizer = LatinWordTokenizer()
        test_str = test_str.lower()
        test_str = replace_jv(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_regex_lemmatizer(self):
        """Test regex_lemmatizer()"""
        sub = [("(.)ab(o|is|it|imus|itis|unt)$", r"\1o")]
        lemmatizer = RegexpLemmatizer(sub)
        test_str = "amabimus"
        target = [("amabimus", "amo")]
        tokenizer = LatinWordTokenizer()
        test_str = test_str.lower()
        test_str = replace_jv(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_backoff_latin_lemmatizer(self):
        """Test LatinBackoffLemmatizer"""
        train = [
            [
                ("ceterum", "ceterus"),
                ("antequam", "antequam"),
                ("destinata", "destino"),
                ("componam", "compono"),
            ]
        ]
        lemmatizer = LatinBackoffLemmatizer()
        test_str = """Ceterum antequam destinata componam"""
        target = [
            ("ceterum", "ceterum"),
            ("antequam", "antequam"),
            ("destinata", "destino"),
            ("componam", "compono"),
        ]
        tokenizer = LatinWordTokenizer()
        test_str = test_str.lower()
        test_str = replace_jv(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_backoff_latin_lemmatizer_verbose(self):
        """Test LatinBackoffLemmatizer"""
        train = [
            [
                ("ceterum", "ceterus"),
                ("antequam", "antequam"),
                ("destinata", "destino"),
                ("componam", "compono"),
            ]
        ]
        lemmatizer = LatinBackoffLemmatizer(verbose=True)
        test_str = """Ceterum antequam destinata componam"""
        target = [
            ("ceterum", "ceterum", "<UnigramLemmatizer: CLTK Sentence Training Data>"),
            (
                "antequam",
                "antequam",
                "<UnigramLemmatizer: CLTK Sentence Training Data>",
            ),
            (
                "destinata",
                "destino",
                "<UnigramLemmatizer: CLTK Sentence Training Data>",
            ),
            ("componam", "compono", "<DictLemmatizer: Morpheus Lemmas>"),
        ]
        tokenizer = LatinWordTokenizer()
        test_str = test_str.lower()
        test_str = replace_jv(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_backoff_latin_lemmatizer_evaluate(self):
        """Test LatinBackoffLemmatizer evaluate method"""
        lemmatizer = LatinBackoffLemmatizer(verbose=False)
        accuracy = lemmatizer.evaluate()
        self.assertTrue(0.85 <= accuracy <= 1)


if __name__ == "__main__":
    unittest.main()
