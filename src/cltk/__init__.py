"""Init module for importing the CLTK class."""

import sys

# Fix for importing when using different Python versions
# https://stackoverflow.com/questions/59216175/importerror-cannot-import-name-metadata-from-importlib
if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

from .nlp import NLP

# Commented this out because it was causing the packageNotFoundError
#curr_version: str = metadata.version("CLTK")
#__version__: str = curr_version
