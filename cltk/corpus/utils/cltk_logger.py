"""CLTK's logging module."""

import logging
import logging.config
import os

home_dir = os.path.expanduser('~/cltk_data')
log_path = os.path.join(home_dir, 'cltk.log')

'''
LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'simpleExample': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': 'no',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('CLTK')
logger.debug('A debug message')
logger.info('A debug message')
logger.warning('A debug message')
logger.error('A debug message')
logger.critical('A debug message')
'''

import os
import logging
import logging.handlers


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

            '''
            fmt = logging.Formatter(
                '%(asctime)s %(filename)s:%(lineno)s'
                ' %(levelname)-8s %(message)s',
                datefmt='%H:%M:%S')
            '''
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
