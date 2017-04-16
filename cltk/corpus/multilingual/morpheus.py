"""Wrapper for Johan Winge's modified `morpheus` command line utility.

Original software at: ``orig. software url``
TODO: Find original software url
TODO: Add Morpheus to cltk Corpus Importer?
"""

from cltk.utils.cltk_logger import logger
import os
import subprocess

class Morpheus(object):
    """Check, install, and call Morpheus"""
    def __init__(self, testing=False):
        """Check whether morpheus is installed, if not, import and install"""
        self.testing = testing
        self._check_import_source()
        self._check_install()

    @staticmethod
    def _check_import_source():
        """Check if Morpheus is installed, if not, install it"""