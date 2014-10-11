# encoding: utf-8
"""The base-level `cltk` class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import os
import logging
import logging.handlers
from cltk.config import CLTK_DATA


class Logger(object):
    def __init__(self):
        self.logfile = os.path.join(CLTK_DATA, 'cltk.log')
        self._logger = None

    @property
    def logger(self):
        """Create and return a logger that logs to both console and
        a log file.

        :returns: an initialised logger
        :rtype: `~logging.Logger` instance

        """

        if self._logger:
            return self._logger

        # Initialise new logger and optionally handlers
        logger = logging.getLogger('cltk')

        if not logger.handlers:  # Only add one set of handlers
            logfile = logging.handlers.RotatingFileHandler(
                self.logfile,
                maxBytes=1024 * 1024,
                backupCount=0)

            console = logging.StreamHandler()

            fmt = logging.Formatter(
                '%(asctime)s %(filename)s:%(lineno)s'
                ' %(levelname)-8s %(message)s',
                datefmt='%H:%M:%S')

            logfile.setFormatter(fmt)
            console.setFormatter(fmt)

            logger.addHandler(logfile)
            logger.addHandler(console)

        logger.setLevel(logging.DEBUG)
        self._logger = logger

        return self._logger

    @logger.setter
    def logger(self, logger):
        """Set a custom logger.

        :param logger: The logger to use
        :type logger: `~logging.Logger` instance

        """

        self._logger = logger
