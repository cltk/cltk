"""Test cltk.ir."""

import os
import unittest

from cltk.ir.query import _regex_span

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_regex_span(self):
        """Test _regex_span()."""
        text = 'ὅτι μὲν ὑμεῖς, ὦ ἄνδρες Ἀθηναῖοι, πεπόνθατε ὑπὸ τῶν ἐμῶν κατηγόρων, οὐκ οἶδα:'
        _matches = _regex_span(r'ς', text)
        matches_list = []
        for match in _matches:
            matches_list.append(match.span())
        self.assertEqual(matches_list, [(12, 13), (22, 23)])

if __name__ == '__main__':
    unittest.main()