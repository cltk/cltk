"""CLTK's logging module."""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import logging
import logging.config
import os

home_dir = os.path.expanduser('~/cltk_data')  # pylint: disable=invalid-name
log_path = os.path.join(home_dir, 'cltk.log')  # pylint: disable=invalid-name

if not os.path.isdir(home_dir):
    os.mkdir(home_dir)

logger = logging.getLogger('CLTK')  # pylint: disable=invalid-name
handler = logging.FileHandler(log_path)  # pylint: disable=invalid-name
formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s')  # pylint: disable=line-too-long,invalid-name
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
