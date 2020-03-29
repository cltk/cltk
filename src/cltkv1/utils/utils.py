"""Module for commonly reused classes and functions."""

import os
import sys
from contextlib import contextmanager
from typing import Any, Dict, List, Optional


def file_exists(file_path: str, is_dir: bool = False) -> bool:
    """Try to expand `~/` and check if a file or dir exists.
    Optionally check if it's a dir.

    >>> file_exists('~/fake_file')
    False

    >>> file_exists('~/', is_dir=True)
    True
    """
    file_path_expanded = os.path.expanduser(file_path)  # type: str
    if is_dir:
        return os.path.isdir(file_path_expanded)
    return os.path.isfile(file_path_expanded)


def reverse_dict(
    input_dict: Dict[str, Any],  # pylint: disable=bad-continuation
    ignore_keys: Optional[List[str]] = None,  # pylint: disable=bad-continuation
) -> Dict[str, str]:
    """Take a dict and reverse its keys and values. Optional
    parameter to ignore certain keys.

    >>> ids_lang = dict(anci1242='Ancient Greek', lati1261='Latin', unlabeled=['Ottoman'])
    >>> reverse_dict(ids_lang, ignore_keys=['unlabeled'])
    {'Ancient Greek': 'anci1242', 'Latin': 'lati1261'}

    >>> reverse_dict(dict(anci1242='Ancient Greek', lati1261='Latin'))
    {'Ancient Greek': 'anci1242', 'Latin': 'lati1261'}

    >>> reverse_dict(ids_lang)
    Traceback (most recent call last):
      ...
    TypeError: This function can only convert type str value to a key. Received value type `<class 'list'>` for key `unlabeled` instead. Consider using `ignore_keys` for this key-value pair to be skipped.

    >>> reverse_dict(ids_lang, ignore_keys='unlabeled')
    Traceback (most recent call last):
      ...
    TypeError: The `ignore_key` parameter must be either types None or list. Received type `<class 'str'>` instead.

    >>> reverse_dict(ids_lang, ignore_keys=['UNUSED-KEY'])
    Traceback (most recent call last):
      ...
    TypeError: This function can only convert type str value to a key. Received value type `<class 'list'>` for key `unlabeled` instead. Consider using `ignore_keys` for this key-value pair to be skipped.
    """
    if ignore_keys and not isinstance(ignore_keys, list):
        raise TypeError(
            "The `ignore_key` parameter must be either types None or list. Received type `{}` instead.".format(
                type(ignore_keys)
            )
        )
    output_dict = dict()  # type: Dict[str, str]
    for key, val in input_dict.items():
        if ignore_keys and key in ignore_keys:
            continue
        try:
            output_dict[val] = key
        except TypeError:
            raise TypeError(
                "This function can only convert type str value to a key. Received value type `{0}` for key `{1}` instead. Consider using `ignore_keys` for this key-value pair to be skipped.".format(
                    type(val), key
                )
            )
    return output_dict


@contextmanager
def suppress_stdout():
    """Wrap a function with this to suppress
    its printing to screen.

    Source: `<https://thesmithfam.org/blog/2012/10/25/temporarily-suppress-console-output-in-python/>`_.

    >>> print("You can see this")
    You can see this

    >>> with suppress_stdout():
    ...     print("YY")

    >>> print("And you can see this again")
    And you can see this again
    """
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def get_cltk_data_dir():
    """Defines where to look for the ``cltk_data`` dir.
    By default, this is located in a user's home directory
    and the directory is created there (``~/cltk_data``).
    However a user may customize where this goes with
    the OS environment variable ``$CLTK_DATA``. If the
    variable is found, then its value is used.

    >>> from cltkv1.utils import get_cltk_data_dir
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


CLTK_DATA_DIR = get_cltk_data_dir()
