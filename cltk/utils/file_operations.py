"""Miscellaneous file operations used by various parts of the CLTK."""

import os.path
import pickle
from typing import Any
from typing import List

from cltk.utils.cltk_logger import logger

__author__ = ['Andreas Grivas <andreasgrv@gmail.com>', 'Kyle P. Johnson <kyle@kyle-p-johnson.com>']
__license__ = 'MIT License. See LICENSE.'


def make_cltk_path(fp_list: List[str] = None) -> str:
    """Take list of arbitrary number of str and return expanded,
    absolute path to a user's cltk_data dir.

    Example:
    In [8]: make_cltk_path(['greek', 'model', 'greek_models_cltk'])
    Out[8]: '/Users/kyle/cltk_data/greek/model/greek_models_cltk'
    """
    if not fp_list:
        fp_list = ['']
    fp_joined = '/'.join(fp_list)  # type: str
    home = os.path.expanduser('~')  # type: str
    return os.path.join(home, 'cltk_data', fp_joined)


def open_pickle(path: str) -> Any:
    """Open a pickle and return loaded pickle object.
    :type path: str
    :param : path: File path to pickle file to be opened.
    :rtype : object
    """
    try:
        with open(path, 'rb') as opened_pickle:
            try:
                return pickle.load(opened_pickle)
            except Exception as pickle_error:
                logger.error(str(pickle_error))
                raise
    except FileNotFoundError as fnf_error:
        logger.error(str(fnf_error))
        raise
    except IOError as io_err:
        logger.error(str(io_err))
        raise
    except EOFError as eof_error:
        logger.error(str(eof_error))
        raise
    except pickle.UnpicklingError as unp_error:
        logger.error(str(unp_error))
        raise
