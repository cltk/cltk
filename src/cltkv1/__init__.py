"""Init module for importing the CLTK class."""

from .nlp import NLP


def get_pyproject():
    """Read version and other info from the project's
    ``pyproject.toml`` file, located in the root of the
    source repo.

    TODO: It doesn't make sense to check for a repo file here, does it?

    >>> pyproject_configs = get_pyproject()
    >>> sorted(pyproject_configs.keys())
    ['authors', 'classifiers', 'dependencies', 'description', 'dev-dependencies', 'documentation', 'homepage', 'keywords', 'license', 'name', 'readme', 'repository', 'version']
    """
    import os  # pylint: disable=import-outside-toplevel
    import toml  # pylint: disable=import-outside-toplevel

    init_path = os.path.abspath(os.path.dirname(__file__))
    pyproject_path = os.path.join(init_path, "../../pyproject.toml")

    with open(pyproject_path, "r") as file_open:
        pyproject = toml.load(file_open)

    return pyproject["tool"]["poetry"]


__version__ = get_pyproject()["version"]
__doc__ = get_pyproject()["description"]
