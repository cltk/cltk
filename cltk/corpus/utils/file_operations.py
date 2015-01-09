"""Miscellaneous file operations used by various parts of the CLTK."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import os
import pickle
from pickle import PickleError
import shutil
import sys


def open_pickle(path: str):
    """Open a pickle and return loaded pickle object.
    :type path: str
    :param : path: File path to pickle file to be opened.
    :rtype : object
    """
    try:
        with open(path, 'rb') as opened_pickle:
            try:
                return pickle.load(opened_pickle)
            except PickleError as pickle_error:
                print(pickle_error)
                sys.exit(1)
    except IOError as io_err:
        print(io_err)
        sys.exit(1)
