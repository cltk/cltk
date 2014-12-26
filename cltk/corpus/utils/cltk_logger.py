"""CLTK's logging module."""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import os
import logging
import logging.config

home_dir = os.path.expanduser('~/cltk_data')
log_path = os.path.join(home_dir, 'cltk.log')

if not os.path.isdir(home_dir):
    os.mkdir(home_dir)
else:
    pass

logger = logging.getLogger('CLTK')
handler = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


'''
I would like to use this but it wasn't writing to file in the tests. Can we
make it work similar with `from cltk.corpus.utils.cltk_logger import logger`
and then usual commands like `logger.info('msg')`?

home_dir = os.path.expanduser('~/cltk_data')
log_path = os.path.join(home_dir, 'cltk.log')

import logging
import logging.handlers
import os


class Logger(object):
    def __init__(self):
        self.logfile = os.path.expanduser(os.path.join('~/cltk_data', 'cltk.log'))
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

            fmt = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s')

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

# Alias
logger = Logger().logger
'''
