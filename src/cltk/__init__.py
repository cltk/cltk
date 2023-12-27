"""Init module for importing the CLTK class."""

import importlib.metadata

from .nlp import NLP

__version__ = curr_version = importlib.metadata.version("cltk")
