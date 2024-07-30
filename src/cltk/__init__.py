"""Init module for importing the CLTK class."""

# Fix for importing when using different Python versions
# https://stackoverflow.com/questions/59216175/importerror-cannot-import-name-metadata-from-importlib
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

from .nlp import NLP

curr_version: str = metadata.version("cltk")
__version__: str = curr_version
