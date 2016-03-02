# Classical Language Toolkit (NLTK)
#
# Copyright (c) 2016 Kyle P. Johnson.
# Authors: Kyle P. Johnson.
# URL: <http://cltk.org/>
# For license information, see LICENSE

"""
The Classical Language Toolkit (CLTK) offers natural language
processing support for Classical languages. CLTK is written
entirely in python.
The goals of the Classical Language Toolkit (CLTK) are to:
    compile analysis-friendly corpora in a variety of Classical
    languages
    gather, improve, and generate linguistic data required for NLP
    develop a free and open platform for generating reproducible,
    scientific research that advances the study of the languages
    and literatures of the ancient world.
See the webpage for more information and documentation:
    http://cltk.org
"""
from __future__ import print_function, absolute_import

import os

# //////////////////////////////////////////////////////
# Metadata
# //////////////////////////////////////////////////////

# Version.  For each new release, the version number should be updated
# in the file VERSION.
try:
    # If a VERSION file exists, use it!
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    with open(version_file, 'r') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (running code interactively?)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex

if __doc__ is not None:
    __doc__ += '\n@version: ' + __version__

# Copyright notice
__copyright__ = """\
Copyright (c) 2016 Kyle P. Johnson.
Distributed and Licensed under the MIT License.
"""

__license__ = "MIT license"
# Description of the project.
__longdescr__ = """\
The Classical Language Toolkit (CLTK) offers natural language
processing support for Classical languages."""
__keywords__ = ['NLP', 'natural language processing',
                'classical language', 'parsing', 'tagging',
                'tokenizing', 'language', 'text analytics']
__url__ = "http://cltk.org/"

# Maintainer, contributors, etc.
__maintainer__ = "Kyle P. Johnson et al."
__author__ = __maintainer__
