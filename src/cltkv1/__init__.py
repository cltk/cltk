"""Init module for importing the CLTK class."""

from .nlp import NLP


def get_pyproject():
    """Read version and other info from the project's
    ``pyproject.toml`` file, located in the root of the
    source repo.

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


def get_cltk_data_dir():
    """Defines where to look for the ``cltk_data`` dir.
    By default, this is located in a user's home directory
    and the directory is created there (``~/cltk_data``).
    However a user may customize where this goes with
    the OS environment variable ``$CLTK_DATA``. If the
    variable is found, then its value is used.

    >>> import os
    >>> os.environ["CLTK_DATA"] = os.path.expanduser("~/cltk_data")
    >>> cltk_data_dir = get_cltk_data_dir()
    >>> os.path.split(cltk_data_dir)[1]
    'cltk_data'
    >>> del os.environ["CLTK_DATA"]
    >>> os.environ["CLTK_DATA"] = os.path.expanduser("~/custom_dir")
    >>> cltk_data_dir = os.environ.get("CLTK_DATA")
    >>> os.path.split(cltk_data_dir)[1]
    'custom_dir'
    """
    import os  # pylint: disable=import-outside-toplevel

    if "CLTK_DATA" in os.environ:
        cltk_data_dir = os.path.expanduser(os.path.normpath(os.environ["CLTK_DATA"]))
        if not os.path.isdir(cltk_data_dir):
            raise FileNotFoundError(
                "Custom data directory `%s` does not exist. "
                "Update your OS environment variable `$CLTK_DATA` "
                "or remove it." % cltk_data_dir
            )
        if not os.access(cltk_data_dir, os.W_OK):
            raise PermissionError(
                "Custom data directory `%s` must have "
                "write permission." % cltk_data_dir
            )
    else:
        cltk_data_dir = os.path.expanduser(os.path.normpath("~/cltk_data"))
    return cltk_data_dir


__cltk_data_dir__ = get_cltk_data_dir()


if __name__ == "__main__":
    get_cltk_data_dir()
