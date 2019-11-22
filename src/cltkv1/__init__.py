"""Init module for importing the CLTK class."""

# TODO: Figure out right way to do these init imports and in submodules

from cltkv1.dependency import *
from cltkv1.languages import *
from cltkv1.tokenizers import *
from cltkv1.utils import *

# modules
from .nlp import NLP


def get_pyproject():
    """Read version and other info from the project's ``pyproject.toml``
    file, located in the root of the source repo.
    """
    import os
    import toml

    init_path = os.path.abspath(os.path.dirname(__file__))
    pyproject_path = os.path.join(init_path, "../../pyproject.toml")

    with open(pyproject_path, "r") as fopen:
        pyproject = toml.load(fopen)

    return pyproject["tool"]["poetry"]


__version__ = get_pyproject()["version"]
__doc__ = get_pyproject()["description"]
