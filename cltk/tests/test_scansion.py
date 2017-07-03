"""Test cltk.prosody scansion modules using the existing doctest methods."""

__license__ = 'MIT License. See LICENSE.'

import unittest
import doctest
from cltk.prosody.latin.HexameterScanner import HexameterScanner
import cltk.prosody.latin.Hexameter


class TestScansionFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_hexameter(self):
        scanner = HexameterScanner()
        my_hex = scanner.scan("impulerit. Tantaene animis caelestibus irae?")
        self.assertEqual(my_hex.scansion, '-  U U -    -   -   U U -    - -  U U  -  - ')
