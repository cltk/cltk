"""Init module for importing the CLTK class."""

from importlib import metadata

from .nlp import NLP

curr_version: str = metadata.version("cltk")
__version__: str = curr_version
