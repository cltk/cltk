"""Process downloaded or local corpora from one format into another.
Some formatting can happen here, or invoke language-specific formatters in
other files.
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import os
import re
import sys

from cltk.corpus.greek.tlg_indices import TLG_INDEX
from cltk.utils.cltk_logger import logger


def remove_non_ascii(input_string):
    """remove non-ascii: http://stackoverflow.com/a/1342373"""
    no_ascii = "".join(i for i in input_string if ord(i) < 128)
    return no_ascii

