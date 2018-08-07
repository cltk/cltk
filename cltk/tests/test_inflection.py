"""Test for inflections: declension, conjugation, etc"""

import unittest
from cltk.inflection.old_norse import pronouns as decl_utils


__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


class TestInflection(unittest.TestCase):
    """Class for unittest"""
    def test_declensions(self):
        thessi_declension = [
            [["þessi", "þenna", "þessum", "þessa"], ["þessir", "þessa", "þessum", "þessa"]],
            [["þessi", "þessa", "þessi", "þessar"], ["þessar", "þessar", "þessum", "þessa"]],
            [["þetta", "þetta", "þessu", "þessa"], ["þessi", "þessi", "þessum", "þessa"]]
        ]
        self.assertListEqual(decl_utils.pro_demonstrative_pronouns_this.declension, thessi_declension)


if __name__ == '__main__':
    unittest.main()
