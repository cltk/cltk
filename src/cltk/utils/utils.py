"""Module for commonly reused classes and functions."""

import os
import re
import sys
import unicodedata
from contextlib import contextmanager

# from enum import EnumMeta, IntEnum
from typing import TYPE_CHECKING, Any, Iterator, Optional, Union

from dotenv import load_dotenv


def file_exists(file_path: str, is_dir: bool = False) -> bool:
    """Try to expand `~/` and check if a file or dir exists.

    Optionally check if it's a dir.

    Examples:
        ```python
        file_exists('~/fake_file')
        # False

        file_exists('~/', is_dir=True)
        # True
        ```

    """
    file_path_expanded: str = os.path.expanduser(file_path)
    if is_dir:
        return os.path.isdir(file_path_expanded)
    return os.path.isfile(file_path_expanded)


def reverse_dict(
    input_dict: dict[str, Any],  # pylint: disable=bad-continuation
    ignore_keys: Optional[list[str]] = None,  # pylint: disable=bad-continuation
) -> dict[str, str]:
    """Take a dict and reverse its keys and values.

    Optional parameter to ignore certain keys.

    Examples:
        ```python
        ids_lang = dict(anci1242='Ancient Greek', lati1261='Latin', unlabeled=['Ottoman'])
        reverse_dict(ids_lang, ignore_keys=['unlabeled'])
        # {'Ancient Greek': 'anci1242', 'Latin': 'lati1261'}

        reverse_dict(dict(anci1242='Ancient Greek', lati1261='Latin'))
        # {'Ancient Greek': 'anci1242', 'Latin': 'lati1261'}

        try:
            reverse_dict(ids_lang)
        except TypeError:
            pass

        try:
            reverse_dict(ids_lang, ignore_keys='unlabeled')
        except TypeError:
            pass

        try:
            reverse_dict(ids_lang, ignore_keys=['UNUSED-KEY'])
        except TypeError:
            pass
        ```

    """
    if ignore_keys and not isinstance(ignore_keys, list):
        raise TypeError(
            "The `ignore_key` parameter must be either types None or list. Received type `{}` instead.".format(
                type(ignore_keys)
            )
        )
    output_dict: dict[str, str] = dict()
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
def suppress_stdout() -> Iterator[None]:
    """Wrap a function with this to suppress its printing to screen.

    Source: `<https://thesmithfam.org/blog/2012/10/25/temporarily-suppress-console-output-in-python/>`_.

    Examples:
        ```python
        print("You can see this")

        with suppress_stdout():
            print("YY")

        print("And you can see this again")
        ```

    """
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def get_cltk_data_dir() -> str:
    """Return where to look for the ``cltk_data`` dir.

    By default, this is located in a user's home directory
    and the directory is created there (``~/cltk_data``).
    However a user may customize where this goes with
    the OS environment variable ``$CLTK_DATA``. If the
    variable is found, then its value is used.

    Examples:
        ```python
        from cltk.utils import CLTK_DATA_DIR
        import os

        os.environ["CLTK_DATA"] = os.path.expanduser("~/cltk_data")
        cltk_data_dir = get_cltk_data_dir()
        assert os.path.split(cltk_data_dir)[1] == "cltk_data"
        del os.environ["CLTK_DATA"]

        os.environ["CLTK_DATA"] = os.path.expanduser("~/custom_dir")
        cltk_data_dir = os.environ.get("CLTK_DATA")
        assert os.path.split(cltk_data_dir)[1] == "custom_dir"
        del os.environ["CLTK_DATA"]
        ```

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
                "Custom data directory `%s` must have write permission." % cltk_data_dir
            )
    else:
        cltk_data_dir = os.path.expanduser(
            os.path.normpath(os.path.join("~", "cltk_data"))
        )
    return cltk_data_dir


def str_to_bool(string: str, truths: Optional[list[str]] = None) -> bool:
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
    """Make all dirs specified for final file.

    If dir already exists, then silently continue.

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


def pascal_case(value: str) -> str:
    return capital_case(camel_case(value))


def camel_case(value: str) -> str:
    string = re.sub(r"\w[\s\W]+\w", "", str(value))
    if not string:
        return string
    return string[0].lower() + re.sub(
        r"[\-_\.\s]([a-z])", lambda matched: matched.group(1).upper(), string[1:]
    )


def capital_case(value: str) -> str:
    return value[0].upper() + value[1:]


def load_env_file(env_file: str = ".env") -> None:
    """Load environment variables from a .env file.

    Args:
        env_file: Path to the .env file. Defaults to ".env".

    Returns:
        None

    """
    load_dotenv(env_file)


def strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


if TYPE_CHECKING:
    from cltk.core.data_types import Doc, Word


def doc_to_conllu(doc: "Doc") -> str:
    """Return a CONLL-U formatted string for the word annotations in ``doc``.

    Args:
        doc: CLTK ``Doc`` instance containing annotated words.

    Returns:
        A string in CONLL-U format representing the document's word annotations.
        Returns an empty string when the document has no words.

    """

    def _clean_field(value: Optional[Any]) -> str:
        if value is None:
            return "_"
        text = str(value)
        text = text.replace("\t", " ").replace("\n", " ").strip()
        return text if text else "_"

    def _format_feats(word: "Word") -> str:
        feats = getattr(word, "features", None)
        feature_list = getattr(feats, "features", None)
        if not feature_list:
            return "_"
        items: list[str] = []
        for feat in feature_list:
            key = getattr(feat, "key", None)
            val = getattr(feat, "value", None)
            if key and val:
                items.append(f"{key}={val}")
        return "|".join(sorted(items)) if items else "_"

    def _format_head(word: "Word") -> str:
        governor = getattr(word, "governor", None)
        if governor is None:
            return "0"
        try:
            return str(int(governor) + 1)
        except (ValueError, TypeError):
            return "_"

    def _format_deprel(word: "Word") -> str:
        dep = getattr(word, "dependency_relation", None)
        if dep is None:
            return "_"
        code = getattr(dep, "code", None)
        subtype = getattr(dep, "subtype", None)
        if not code:
            return "_"
        return f"{code}:{subtype}" if subtype else str(code)

    words: list["Word"] = getattr(doc, "words", []) or []
    if not words:
        return ""

    grouped: dict[Optional[int], list[tuple[int, "Word"]]] = {}
    for order_idx, word in enumerate(words):
        sent_idx = getattr(word, "index_sentence", None)
        if sent_idx not in grouped:
            grouped[sent_idx] = []
        grouped[sent_idx].append((order_idx, word))

    output_lines: list[str] = []
    for _, sentence_entries in grouped.items():
        sentence_words = sorted(
            sentence_entries,
            key=lambda item: (
                getattr(item[1], "index_token", None)
                if getattr(item[1], "index_token", None) is not None
                else item[0]
            ),
        )
        for token_idx, (_, word) in enumerate(sentence_words, start=1):
            upos = getattr(getattr(word, "upos", None), "tag", None)
            xpos = getattr(word, "xpos", None)
            columns = [
                str(token_idx),
                _clean_field(getattr(word, "string", None)),
                _clean_field(getattr(word, "lemma", None)),
                _clean_field(upos),
                _clean_field(xpos),
                _format_feats(word),
                _format_head(word),
                _format_deprel(word),
                "_",
                "_",
            ]
            output_lines.append("\t".join(columns))
        output_lines.append("")

    return "\n".join(output_lines)


CLTK_DATA_DIR = get_cltk_data_dir()
