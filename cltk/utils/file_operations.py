"""Miscellaneous file operations used by various parts of the CLTK."""

import os.path
import pickle

from cltk.utils.cltk_logger import logger

__author__ = ['Andreas Grivas <andreasgrv@gmail.com>', 'Kyle P. Johnson <kyle@kyle-p-johnson.com>']
__license__ = 'MIT License. See LICENSE.'


def make_cltk_path(*fp_list):
    """Take arbitrary number of str arguments (not list) and return expanded,
    absolute path to a user's cltk_data dir.

    Example:
    In [8]: make_cltk_path('greek', 'model', 'greek_models_cltk')
    Out[8]: '/Users/kyle/cltk_data/greek/model/greek_models_cltk'

    :type fp_list: str positional arguments
    :param: : fp_list tokens to join together beginning from cltk_root folder
    :rtype: str
    """
    
    home = os.path.expanduser('~')
    return os.path.join(home, 'cltk_data', *fp_list)


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
