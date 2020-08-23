"""Init module for importing the CLTK class."""

import pkg_resources

__version__ = curr_version = pkg_resources.get_distribution("cltk")  # type: pkg_resources.EggInfoDistribution

from .nlp import NLP
