# encoding: utf-8
"""The base-level `cltk` class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import site
import os
from cltk.config import CLTK_DATA
from cltk.logger import Logger

"""
@property
def corpus(self):
    method = CORPORA.get(self.name, None)
    if method:
        return method()
    else:
        error_msg = 'Unrecognized corpus name.'
        possible_corpora = ', '.join(list(CORPORA.keys()))
        log_msg = 'Choose one of the following: ' + possible_corpora
        self.logger.error(log_msg)
        raise RuntimeError(error_msg)
"""


class CLTK(object):
    def __init__(self, data_path=None):
        # Can be either
        if data_path:
            self.cltk_data = self.resolve_path(data_path)
        else:
            self.cltk_data = self.resolve_path(CLTK_DATA)
        # What does this do?
        self.cltk_bin_path = os.path.join(site.getsitepackages()[0], 'cltk')
        # Prepare local dirs
        self.originals_dir = self.resolve_path(os.path.join(self.cltk_data,
                                                            'originals'))
        self.compiled_dir = self.resolve_path(os.path.join(self.cltk_data,
                                                           'compiled'))
        # Instantiate logger
        self.logger = Logger().logger

    def resolve_path(self, path):
        # Resolve absolute path
        if os.path.isabs(path):
            full_path = path
        elif path.startswith('~'):
            full_path = os.path.expanduser(path)
        elif path.startswith('.'):
            full_path = os.path.abspath(path)
        # Ensure absolute path exists
        if not os.path.exists(full_path):
            # If directory
            if os.path.splitext(full_path)[1] == '':
                os.mkdir(full_path)
                self.logger.info('Directory created at : {}'.format(full_path))
            # If file
            else:
                open(full_path).close()
                self.logger.info('File created at : {}'.format(full_path))
        return full_path
