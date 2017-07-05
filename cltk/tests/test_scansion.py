"""Test cltk.prosody scansion modules using the existing doctest methods."""

__license__ = 'MIT License. See LICENSE.'

import unittest
import doctest

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite('cltk.prosody.latin.HexameterScanner'))
    tests.addTests(doctest.DocTestSuite('cltk.prosody.latin.Hexameter'))
    tests.addTests(doctest.DocTestSuite('cltk.prosody.latin.MetricalValidator'))
    tests.addTests(doctest.DocTestSuite('cltk.prosody.latin.ScansionConstants'))
    tests.addTests(doctest.DocTestSuite('cltk.prosody.latin.ScansionFormatter'))
    tests.addTests(doctest.DocTestSuite('cltk.prosody.latin.Syllabifier'))
    tests.addTests(doctest.DocTestSuite('cltk.prosody.latin.StringUtils'))
    return tests

class TestScansionFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""
