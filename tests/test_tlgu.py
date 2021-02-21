"""Test TLGU installation."""

import os
import unittest

from cltk.corpora.grc.tlg.tlgu import TLGU
from cltk.utils.file_operations import make_cltk_path

__license__ = "MIT License. See LICENSE."


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    @classmethod
    def setUpClass(self):
        pass

    def test_tlgu_init(self):
        """Test constructors of TLGU module for check, import, and install."""
        TLGU(interactive=False)
        header_file = make_cltk_path("grc/software/grc_software_tlgu/README.md")
        self.assertTrue(os.path.isfile(header_file))


if __name__ == "__main__":
    unittest.main()
