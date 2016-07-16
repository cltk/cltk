"""Miscellaneous file operations used by various parts of the CLTK."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.utils.cltk_logger import logger
import pickle


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
