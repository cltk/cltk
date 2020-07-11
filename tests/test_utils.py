"""Uit tests for cltk.utils."""

import unittest
from unittest.mock import patch

from cltk.utils.utils import query_yes_no
from cltk.utils.akk import ATFConverter


class TestUtils(unittest.TestCase):
    """Test utils."""

    @patch("builtins.input", lambda *args: "yes")
    def test_query_yes(self):
        """Test question function with I/O."""
        self.assertEqual(query_yes_no(question="Is anyone wiser than Socrates?"), True)

    @patch("builtins.input", lambda *args: "no")
    def test_query_no(self):
        """Test question function with I/O."""
        self.assertEqual(query_yes_no(question="Is anyone wiser than Socrates?"), False)

    @patch("builtins.input", lambda *args: "no")
    def test_query_no_def_none(self):
        """Test question function with I/O."""
        self.assertEqual(
            query_yes_no(question="Is anyone wiser than Socrates?", default=None), False
        )

    @patch("builtins.input", lambda *args: "no")
    def test_query_no_def_no(self):
        """Test question function with I/O."""
        self.assertEqual(
            query_yes_no(question="Is anyone wiser than Socrates?", default="no"), False
        )

    @patch("builtins.input", lambda *args: "no")
    def test_query_no_def_invalid(self):
        """Test question function with I/O."""
        with self.assertRaises(ValueError) as context:
            query_yes_no(question="Is anyone wiser than Socrates?", default="xxx")

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
