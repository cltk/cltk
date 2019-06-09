"""The Classical Language Toolkit (CLTK) offers natural language
processing support for Classical languages. See the webpage for
more information and documentation: http://cltk.org
"""

import sys
import os
import builtins
from pkg_resources import get_distribution

if sys.version_info[0] != 3:  # pragma: no cover
    raise ImportError('Python Version 3 or above is required for cltk.')

__copyright__ = 'Copyright (c) 2016 Kyle P. Johnson. Distributed and Licensed under the MIT License.'  # pylint: disable=line-too-long

__description__ = __doc__

__license__ = 'MIT'

__url__ = 'http://cltk.org'

__version__ = get_distribution('cltk').version  # pylint: disable=no-member

if 'CLTK_DATA' in os.environ:
    __cltk_data_dir__ = os.path.expanduser(
        os.path.normpath(os.environ['CLTK_DATA']))
    if not os.path.isdir(__cltk_data_dir__):
        raise FileNotFoundError('Custom data directory `%s` does not exist. '
                                'Update your OS environment variable `$CLTK_DATA` '
                                'or remove it.' % __cltk_data_dir__)
    if not os.access(__cltk_data_dir__, os.W_OK):
        raise PermissionError('Custom data directory `%s` must have '
                              'write permission.' % __cltk_data_dir__)
else:
    __cltk_data_dir__ = os.path.expanduser(
        os.path.normpath('~/cltk_data'))


def get_cltk_data_dir() -> str:
    """Defines where to look for the `cltk_data` dir. By default, this is located
     in a user's home directory and the directory is created there (`~/cltk_data`).
     However a user may customize where this goes with the OS environment variable
     `$CLTK_DATA`. If the variable is found, then its value is used.

    TODO: Run tests with a defined `$CLTK_DATA` environment variable)
    """
    return __cltk_data_dir__


builtins.get_cltk_data_dir = get_cltk_data_dir

# rm these namespaces from memory, or these show up in dir(cltk)
del get_distribution
del builtins
del os
del sys
