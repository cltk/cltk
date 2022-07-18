"""Module for commonly reused classes and functions."""

import os
import sys
from contextlib import contextmanager
from enum import EnumMeta, IntEnum
from typing import Any, Dict, List, Optional, Union

import requests
from tqdm import tqdm


class CLTKEnumMeta(EnumMeta):
    def __repr__(cls):
        return cls.__name__


class CLTKEnum(IntEnum, metaclass=CLTKEnumMeta):
    def __repr__(self):
        return f"{self._name_}"

    __str__ = __repr__

    def __eq__(self, other):
        return False if type(self) != type(other) else IntEnum.__eq__(self, other)


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


def get_cltk_data_dir() -> str:
    """Defines where to look for the ``cltk_data`` dir.
    By default, this is located in a user's home directory
    and the directory is created there (``~/cltk_data``).
    However a user may customize where this goes with
    the OS environment variable ``$CLTK_DATA``. If the
    variable is found, then its value is used.

    >>> from cltk.utils import CLTK_DATA_DIR
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
    >>> del os.environ["CLTK_DATA"]
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


def str_to_bool(string: str, truths: Optional[List[str]] = None) -> bool:
    """Convert a string into a boolean (case insensitively).

    Args:
        string: String to convert.
        truths: List of strings that count as Truthy; defaults to "yes" and "y".

    Returns:
        ``True`` if string is in truths; otherwise, returns ``False``. All strings
        are compared in lowercase, so the method is case insensitive.
    """
    truths = truths or ["yes", "y"]
    return string.lower() in [t.lower() for t in truths]


def query_yes_no(question: str, default: Union[str, None] = "yes") -> bool:
    """Ask a yes/no question via ``input()`` and return ``True``/``False``.

    Source: `<https://stackoverflow.com/a/3041990>`_.

    Args:
        question: Question string presented to the user.
        default: Presumed answer if the user just hits <Enter>.
           It must be "yes" (the default), "no", or None (meaning
           an answer is required of the user).

    Returns:
        ``True`` for "yes" and "y" or ``False`` for "no" and "n".
    """
    # 1. Construct prompt
    if default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    elif not default:
        prompt = " [y/n] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)

    # 2. Check user input and return correct boolean
    while True:
        # sys.stdout.write(question + prompt)
        print(question + prompt)
        choice = input()
        if default and choice == "":
            return str_to_bool(default)
        try:
            return str_to_bool(choice)
        except ValueError:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def mk_dirs_for_file(file_path: str) -> None:
    """Make all dirs specified for final file. If dir already exists,
    then silently continue.

    Args:
        file_path: Paths of dirs to be created (i.e., `mkdir -p`)

    Returns:
        None
    """
    dirs = os.path.split(file_path)[0]
    try:
        os.makedirs(dirs)
    except FileExistsError:
        # TODO: Log INFO level; it's OK if dir already exists
        return None


def get_file_with_progress_bar(model_url: str, file_path: str) -> None:
    """Download file with a progress bar.

    Source: https://stackoverflow.com/a/37573701

    Args:
        model_url: URL from which to downloaded file.
        file_path: Location at which to save file.

    Raises:
        IOError: If size of downloaded file differs from that in remote's ``content-length`` header.

    Returns:
        None
    """
    mk_dirs_for_file(file_path=file_path)
    req_obj = requests.get(url=model_url, stream=True)
    total_size = int(req_obj.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
    with open(file_path, "wb") as file_open:
        for data in req_obj.iter_content(block_size):
            progress_bar.update(len(data))
            file_open.write(data)
    progress_bar.close()
    if total_size != 0 and progress_bar.n != total_size:
        raise IOError(
            f"Expected downloaded file to be of size '{total_size}' however it is in fact '{progress_bar.n}'."
        )


CLTK_DATA_DIR = get_cltk_data_dir()
