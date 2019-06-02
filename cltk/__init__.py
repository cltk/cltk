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

# ADDED: almostearthling 20190601
# provide a built-in variable containing the CLTK data directory instead of
# using the default, cluttering and venv-fairly-incompatible ~/cltk_data: if
# an environment variable named CLTK_DATA is available, use it to determine
# where data have to be stored, otherwise fall back to the old solution and
# use ~/cltk_data as usual; when a Python Virtual Environment is used the
# CLTK_DATA variable can be set in the activation script
if 'CLTK_DATA' in os.environ:
    get_cltk_data_dir = os.path.expanduser(
        os.path.normpath(os.environ['CLTK_DATA']))
else:
    get_cltk_data_dir = os.path.expanduser(
        os.path.normpath("~/cltk_data"))
builtins.get_cltk_data_dir = get_cltk_data_dir

# rm these namespaces from memory, or these show up in dir(cltk)
del get_distribution
del builtins
del os
del sys
