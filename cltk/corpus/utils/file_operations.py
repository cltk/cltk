"""Miscellaneous file operations used by various parts of the CLTK."""

import os
import pickle
from pickle import PickleError
import shutil
import sys


def copy_dir_contents(src_path: str, destination_path: str):
    """Copy contents of one directory to another. ``destination_path`` will
    be the name of the new dir and cannot exist.
    :type src_path: str
    :type destination_path: str
    :param : src_path: Path of dir to be copied.
    :param : destination_path: Path of new dir.
    """
    src_files = os.listdir(src_path)
    for file_name in src_files:
        full_file_name = os.path.join(src_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, destination_path)


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
