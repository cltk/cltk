"""Logging for CLTK. Writes files to `cltk_dir/`.

Use:
from cltk.corpus.cltk_logging import logging
logger.info('Directory created at: {}'.format(full_path))

"""

__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'

from cltk.corpus import CLTK_DATA_DIR
import logging
import logging.handlers
import os


class Logger(object):
    """CLTK logging class."""
    def __init__(self):
        home_rel = CLTK_DATA_DIR
        home = os.path.expanduser(home_rel)
        self.logfile = os.path.join(home, 'cltk.log')
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
                '%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p'
            )

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
