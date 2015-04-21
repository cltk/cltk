"""CLTK's logging module.
TODO: add pylint ignores for 'invalid-name'.
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import logging
import logging.config
import os

home_dir = os.path.expanduser('~/cltk_data')
log_path = os.path.join(home_dir, 'cltk.log')

if not os.path.isdir(home_dir):
    os.mkdir(home_dir)
else:
    pass

logger = logging.getLogger('CLTK')
handler = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s')  # pylint: disable=C0301
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
