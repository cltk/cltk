"""The Classical Language Toolkit (CLTK) offers natural language
processing support for Classical languages. See the webpage for
more information and documentation: http://cltk.org
"""

import sys
import os
import builtins
from pkg_resources import get_distribution

if sys.version_info[0] != 3:
    raise ImportError('Python Version 3 or above is required for cltk.')

__copyright__ = 'Copyright (c) 2016 Kyle P. Johnson. Distributed and Licensed under the MIT License.'  # pylint: disable=line-too-long

__description__ = __doc__

__license__ = 'MIT'

__url__ = 'http://cltk.org'

__version__ = get_distribution('cltk').version  # pylint: disable=no-member


# retrieve the data directory from environment, fall back if not found
# WARNING: skip coverage test on unreachable branch (tip: change test
# script to run tests with a defined CLTK_DATA environment variable)
if 'CLTK_DATA' in os.environ:   # pragma: no cover
    __cltk_data_dir__ = os.path.expanduser(
        os.path.normpath(os.environ['CLTK_DATA']))
else:
    __cltk_data_dir__ = os.path.expanduser(
        os.path.normpath("~/cltk_data"))


# return the data directory instead of providing direct access to the variable
def get_cltk_data_dir():
    return __cltk_data_dir__


builtins.get_cltk_data_dir = get_cltk_data_dir

# rm these namespaces from memory, or these show up in dir(cltk)
del get_distribution
del builtins
del os
del sys
