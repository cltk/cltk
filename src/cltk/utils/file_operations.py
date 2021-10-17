"""Miscellaneous file operations used by various parts of the CLTK."""

import hashlib
import os.path
import pickle
from typing import Any

from cltk.core.cltk_logger import logger
from cltk.utils import CLTK_DATA_DIR

__author__ = [
    "Andreas Grivas <andreasgrv@gmail.com>",
    "Kyle P. Johnson <kyle@kyle-p-johnson.com>",
    "Todd Cook <todd.g.cook@gmail.com>",
]
__license__ = "MIT License. See LICENSE."


CLTK_DATA_DIR_PRIVATE = os.path.expanduser("~/cltk_data/private/")


def make_cltk_path(*fp_list):
    """Take arbitrary number of str arguments (not list) and return expanded,
    absolute path to a user's (or user-defined) cltk_data dir.

    Example:
    In [8]: make_cltk_path('greek', 'model', 'greek_models_cltk')
    Out[8]: '/Users/kyle/cltk_data/greek/model/greek_models_cltk'

    :type fp_list: str positional arguments
    :param: : fp_list tokens to join together beginning from cltk_root folder
    :rtype: str
    """

    return os.path.join(CLTK_DATA_DIR, *fp_list)


def open_pickle(path: str) -> Any:
    """Open a pickle and return loaded pickle object.
    :type path: str
    :param : path: File path to pickle file to be opened.
    :rtype : object
    """
    try:
        with open(path, "rb") as opened_pickle:
            try:
                return pickle.load(opened_pickle)
            except Exception as pickle_error:
                logger.error(pickle_error)
                raise
    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)
        raise
    except IOError as io_err:
        logger.error(io_err)
        raise
    except EOFError as eof_error:
        logger.error(eof_error)
        raise
    except pickle.UnpicklingError as unp_error:
        logger.error(unp_error)
        raise


def md5(filename: str) -> str:
    """
    Given a filename produce an md5 hash of the contents.
    >>> import tempfile, os
    >>> f = tempfile.NamedTemporaryFile(delete=False)
    >>> f.write(b'Hello Wirld!')
    12
    >>> f.close()
    >>> md5(f.name)
    '997c62b6afe9712cad3baffb49cb8c8a'
    >>> os.unlink(f.name)
    """
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
