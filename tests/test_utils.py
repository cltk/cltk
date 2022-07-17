"""Uit tests for cltk.utils."""

import unittest
from unittest.mock import patch

from cltk.utils.utils import query_yes_no, str_to_bool


class TestUtils(unittest.TestCase):
    """Test utils."""

    def test_str_to_bool_yes(self):
        """Test that "yes" returns True."""
        self.assertEqual(str_to_bool("yes"), True)

    def test_str_to_bool_no(self):
        """Test that "no" returns False."""
        self.assertEqual(str_to_bool("no"), False)

    def test_str_to_bool_case_insensitivity(self):
        """Test that the function is case insensitive."""
        self.assertEqual(str_to_bool("yES"), True)

    def test_str_to_bool_custom_truths_true(self):
        """Test that we can pass a custom list of true values and get True."""
        self.assertEqual(str_to_bool("hello", truths=["Hello", "World"]), True)

    def test_str_to_bool_custom_truths_false(self):
        """Test that we can pass a custom list of true values and get False."""
        self.assertEqual(str_to_bool("yes", truths=["Hello", "World"]), False)

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
