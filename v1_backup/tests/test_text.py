"""Uit tests for cltk.text."""

import unittest

from cltk.text.akk import ATFConverter


class TestAkkadianUtils(unittest.TestCase):
    def test_single_sign(self):
        """
        Tests process with two_three as active.
        """
        atf = ATFConverter(two_three=True)
        signs = ["a", "a1", "a2", "a3", "be2", "be3", "bad2", "bad3"]
        target = ["a", "a₁", "a₂", "a₃", "be₂", "be₃", "bad₂", "bad₃"]
        output = atf.process(signs)
        self.assertEqual(output, target)

    def test_accents(self):
        """
        Tests process with two_three as inactive.
        """
        atf = ATFConverter(two_three=False)
        signs = ["a", "a2", "a3", "be2", "bad3", "buru14"]
        target = ["a", "á", "à", "bé", "bàd", "buru₁₄"]
        output = atf.process(signs)
        self.assertEqual(output, target)

    def test_unknown_token(self):
        """
        Tests process with unrecognizable tokens.
        """
        atf = ATFConverter(two_three=True)
        signs = ["a2", "☉", "be3"]
        target = ["a₂", "☉", "be₃"]
        output = atf.process(signs)
        self.assertEqual(output, target)
