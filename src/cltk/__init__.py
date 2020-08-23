"""Init module for importing the CLTK class.

TODO: Add ``__version__`` here with ``curr_version = pkg_resources.get_distribution("cltk")  # type: pkg_resources.EggInfoDistribution`` and ``release = curr_version.version  # type: str``
"""

import pkg_resources

__version__ = curr_version = pkg_resources.get_distribution("cltk")  # type: pkg_resources.EggInfoDistribution

from .nlp import NLP
