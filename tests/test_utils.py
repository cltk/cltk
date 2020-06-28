"""Uit tests for cltkv1.utils."""

import unittest
from unittest.mock import patch

from cltkv1.utils.utils import query_yes_no


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
