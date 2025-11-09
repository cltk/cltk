"""Module for commonly reused classes and functions."""

import json
import os
import re
import sys
import unicodedata
from contextlib import contextmanager

# from enum import EnumMeta, IntEnum
from typing import TYPE_CHECKING, Any, Iterator, Optional, Union

from dotenv import load_dotenv

from cltk.core.data_types import Doc, Word

if TYPE_CHECKING:
    import pyarrow as pa  # type: ignore[import-untyped]

    type Table = pa.Table
else:
    # no runtime dependency on pyarrow for annotations
    type Table = Any


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
    input_dict: dict[str, Any],
    ignore_keys: Optional[list[str]] = None,
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


def doc_to_conllu(doc: Doc) -> str:
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

        def _sentence_sort_key(item: tuple[int, "Word"]) -> int:
            idx_token: Optional[int] = getattr(item[1], "index_token", None)
            if idx_token is None:
                return item[0]
            return idx_token

        sentence_words = sorted(sentence_entries, key=_sentence_sort_key)
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


def doc_to_feature_table(doc: Doc) -> Table:
    """Return a ``pyarrow.Table`` of POS, morphology, and dependency features.

    - Raises ValueError when ``Doc.words`` is missing or empty.
    - Writes an empty row (all ``None``) when a list entry is ``None``.
    - Ignores ``Word.xpos``.
    - Adds tree-shape features, document metadata, and sentence-level metrics.
    - Requires ``pyarrow`` to serialize downstream. Example::

        >>> table = doc_to_feature_table(doc)
        >>> import pyarrow.parquet as pq
        >>> pq.write_table(table, "doc_features.parquet")

    Feature Glossary (selected)
    - head_upos: UPOS tag of the head token (empty for root)
    - dir_to_head: Direction to head within sentence: ``L``, ``R``, or ``ROOT``
    - dist_to_head: Absolute token distance to head (0 for root)
    - dist_to_head_norm: ``dist_to_head`` normalized by sentence length
    - child_count: Number of dependents of the token (out-degree)
    - left_child_count / right_child_count: Dependents to the left/right of the token
    - is_leaf: ``1`` if token has no dependents else ``0``
    - depth_from_root / path_len_to_root: Steps from root to token (root = 0)
    - height_to_leaf: Max steps from token down to any leaf (leaf = 0)
    - subtree_size: Tokens in token’s subtree (including the token itself)
    - subtree_span_width: Index span width covering the subtree (max − min + 1)
    - subtree_gap: ``subtree_span_width - subtree_size`` (non‑zero suggests discontinuity)
    - crossing_arcs: Number of arcs that cross this token’s arc
    - parent_branching_factor: Number of children of the token’s parent
    - sibling_index: Position among siblings by token order (0‑based)
    - sibling_count: Number of siblings (``parent_branching_factor - 1``)
    - is_root: ``1`` if root token else ``0``
    - valid_head: ``1`` if token’s head index is valid else ``0``

    Sentence-level (repeated per token)
    - sent_root_index: 1‑based index of the root in sentence order
    - sent_tree_depth: Max ``depth_from_root`` within the sentence
    - sent_avg_branching_nonleaf: Average children among non‑leaf nodes
    - sent_crossing_arcs: Number of crossing‑arc pairs in the sentence
    - sent_is_projective: ``1`` if no crossings, else ``0``
    - sent_len: Sentence length in tokens
    """
    words: Optional[list[Optional[Word]]] = getattr(doc, "words", None)
    if not words:
        raise ValueError("Doc.words must be a non-empty list.")

    # Collect UD feature keys across the document
    feature_keys: set[str] = set()
    for w in words:
        if not w:
            continue
        feats = getattr(w, "features", None)
        feature_list = getattr(feats, "features", None)
        if not feature_list:
            continue
        for feat in feature_list:
            key = getattr(feat, "key", None)
            if key:
                feature_keys.add(str(key))
    sorted_feature_keys: list[str] = sorted(feature_keys)

    metadata_map_raw = getattr(doc, "metadata", {}) or {}
    metadata_map: dict[str, Any]
    if not isinstance(metadata_map_raw, dict):
        metadata_map = dict(metadata_map_raw)
    else:
        metadata_map = metadata_map_raw
    metadata_keys: list[str] = sorted(str(k) for k in metadata_map.keys())

    # Group by sentence index (may be None)
    sent_groups: dict[Optional[int], list[tuple[int, Word]]] = {}
    for doc_idx, w in enumerate(words):
        if w is None:
            continue
        sidx = getattr(w, "index_sentence", None)
        sent_groups.setdefault(sidx, []).append((doc_idx, w))

    # Derived features per token, keyed by doc index
    dep_feats_by_doc_idx: dict[int, dict[str, Union[str, int, float, None]]] = {}

    def _cross(a1: int, a2: int, b1: int, b2: int) -> bool:
        x1, x2 = (a1, a2) if a1 <= a2 else (a2, a1)
        y1, y2 = (b1, b2) if b1 <= b2 else (b2, b1)
        return (x1 < y1 < x2 < y2) or (y1 < x1 < y2 < x2)

    for sidx, entries in sent_groups.items():
        # Sort sentence tokens by in-sentence order: prefer index_token else doc order
        def sort_key(item: tuple[int, Word]) -> int:
            _, w = item
            tok = getattr(w, "index_token", None)
            return int(tok) if tok is not None else item[0]

        entries_sorted = sorted(entries, key=sort_key)
        n = len(entries_sorted)
        if n == 0:
            continue

        # Maps
        local_to_doc: list[int] = [doc_i for doc_i, _ in entries_sorted]
        # doc_to_local: dict[int, int] = {doc_i: i for i, doc_i in enumerate(local_to_doc)}

        upos_by_local: list[str] = [""] * n
        lemma_by_local: list[str] = [""] * n
        form_by_local: list[str] = [""] * n
        head_local: list[Optional[int]] = [None] * n
        depcode_by_local: list[str] = [""] * n

        index_token_to_local: dict[int, int] = {}
        for i, (_, w) in enumerate(entries_sorted):
            tok = getattr(w, "index_token", None)
            if isinstance(tok, int):
                index_token_to_local[tok] = i

        for i, (_, w) in enumerate(entries_sorted):
            upos = getattr(getattr(w, "upos", None), "tag", None) or ""
            upos_by_local[i] = str(upos)
            lemma_by_local[i] = getattr(w, "lemma", "") or ""
            form_by_local[i] = getattr(w, "string", "") or ""
            dep = getattr(w, "dependency_relation", None)
            if dep:
                code = getattr(dep, "code", None)
                subtype = getattr(dep, "subtype", None)
                depcode_by_local[i] = (
                    f"{code}:{subtype}"
                    if code and subtype
                    else (str(code) if code else "")
                )
            gov = getattr(w, "governor", None)
            if isinstance(gov, int) and 0 <= gov < n:
                head_local[i] = gov
            elif isinstance(gov, int) and gov in index_token_to_local:
                head_local[i] = index_token_to_local[gov]
            else:
                head_local[i] = None

        # Children adjacency
        children: list[list[int]] = [[] for _ in range(n)]
        for i, h in enumerate(head_local):
            if isinstance(h, int) and 0 <= h < n:
                children[h].append(i)
        for kids in children:
            kids.sort()

        # Depth from root and cycle detection
        depths: list[Optional[int]] = [None] * n
        for i in range(n):
            if depths[i] is not None:
                continue
            seen: set[int] = set()
            cur = i
            d = 0
            while True:
                if cur in seen:
                    for node in seen:
                        depths[node] = None
                    break
                seen.add(cur)
                h = head_local[cur]
                if h is None:
                    # Assign precise depths by walking from i upward
                    dd = 0
                    node = i
                    visited2: set[int] = set()
                    while node not in visited2:
                        visited2.add(node)
                        depths[node] = dd
                        h2 = head_local[node]
                        if h2 is None:
                            break
                        node = h2
                        dd += 1
                    break
                cur = h
                d += 1
                if d > n + 5:
                    for node in seen:
                        depths[node] = None
                    break

        # Subtree metrics (height, size, span)
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def subtree_metrics(
            i: int, _stack: tuple[int, ...] = ()
        ) -> tuple[Optional[int], Optional[int], int, int]:
            if i in _stack:
                return None, None, i, i
            kids = children[i]
            if not kids:
                return 0, 1, i, i
            max_h: Optional[int] = 0
            total_size = 1
            mn = i
            mx = i
            for c in kids:
                h, sz, c_mn, c_mx = subtree_metrics(c, _stack + (i,))
                if h is None or sz is None:
                    max_h = None
                else:
                    if max_h is not None:
                        max_h = max(max_h, 1 + h)
                    total_size += sz
                mn = min(mn, c_mn)
                mx = max(mx, c_mx)
            return max_h, (None if max_h is None else total_size), mn, mx

        height_to_leaf: list[Optional[int]] = [None] * n
        subtree_size: list[Optional[int]] = [None] * n
        span_min: list[int] = [0] * n
        span_max: list[int] = [0] * n
        for i in range(n):
            h, sz, mn, mx = subtree_metrics(i)
            height_to_leaf[i] = h
            subtree_size[i] = sz
            span_min[i] = mn
            span_max[i] = mx

        # Left/right child counts and leaf flags
        left_child_count = [0] * n
        right_child_count = [0] * n
        child_count = [len(children[i]) for i in range(n)]
        for i in range(n):
            for c in children[i]:
                if c < i:
                    left_child_count[i] += 1
                elif c > i:
                    right_child_count[i] += 1
        is_leaf = [1 if child_count[i] == 0 else 0 for i in range(n)]

        # Distances and directions to head
        dist_to_head = [0] * n
        dir_to_head = ["ROOT"] * n
        for i in range(n):
            h = head_local[i]
            if h is None:
                dist_to_head[i] = 0
                dir_to_head[i] = "ROOT"
            else:
                dist_to_head[i] = abs(i - h)
                dir_to_head[i] = "L" if h < i else "R"
        dist_to_head_norm = [(d / n) if n > 0 else 0.0 for d in dist_to_head]

        # Sibling info
        sibling_index = [0] * n
        sibling_count = [0] * n
        parent_branching_factor = [0] * n
        for i in range(n):
            h = head_local[i]
            if h is None:
                sibling_index[i] = 0
                sibling_count[i] = 0
                parent_branching_factor[i] = 0
            else:
                sibs = children[h]
                parent_branching_factor[i] = len(sibs)
                sibling_count[i] = max(0, len(sibs) - 1)
                try:
                    sibling_index[i] = sibs.index(i)
                except ValueError:
                    sibling_index[i] = 0

        # Span metrics
        subtree_span_width: list[int] = [0] * n
        subtree_gap: list[Optional[int]] = [None] * n
        for i in range(n):
            width = span_max[i] - span_min[i] + 1
            subtree_span_width[i] = width
            size_val = subtree_size[i]
            gap_val: Optional[int]
            if size_val is None:
                gap_val = None
            else:
                gap_val = width - size_val
            subtree_gap[i] = gap_val

        # Crossing arcs
        arcs: list[tuple[int, int, int]] = []
        for i in range(n):
            h = head_local[i]
            if h is None:
                continue
            lo, hi = (i, h) if i <= h else (h, i)
            arcs.append((lo, hi, i))
        crossing_per_token = [0] * n
        total_crossings = 0
        for a in range(len(arcs)):
            a1, a2, ai = arcs[a]
            for b in range(a + 1, len(arcs)):
                b1, b2, bi = arcs[b]
                if _cross(a1, a2, b1, b2):
                    total_crossings += 1
                    crossing_per_token[ai] += 1
                    crossing_per_token[bi] += 1

        roots = [i for i, h in enumerate(head_local) if h is None]
        sent_root_index_1b = (roots[0] + 1) if roots else 1
        sent_tree_depth = max([d for d in depths if d is not None], default=0)
        nonleaf = [i for i in range(n) if child_count[i] > 0]
        sent_avg_branching_nonleaf = (
            (sum(child_count[i] for i in nonleaf) / len(nonleaf)) if nonleaf else 0.0
        )
        sent_crossing_arcs = total_crossings
        sent_is_projective = 1 if total_crossings == 0 else 0
        sent_len = n

        # Head attributes
        head_upos = [""] * n
        head_form = [""] * n
        head_lemma = [""] * n
        for i in range(n):
            h = head_local[i]
            if h is not None and 0 <= h < n:
                head_upos[i] = upos_by_local[h]
                head_form[i] = form_by_local[h]
                head_lemma[i] = lemma_by_local[h]

        # Child extremes
        leftmost_child_index_1b = [""] * n
        rightmost_child_index_1b = [""] * n
        for i in range(n):
            if children[i]:
                leftmost_child_index_1b[i] = str(children[i][0] + 1)
                rightmost_child_index_1b[i] = str(children[i][-1] + 1)

        # Assign per-token features back by doc index
        for local_i, doc_i in enumerate(local_to_doc):
            head_idx = head_local[local_i]
            depth_val = depths[local_i]
            height_val = height_to_leaf[local_i]
            subtree_size_val = subtree_size[local_i]
            subtree_gap_val = subtree_gap[local_i]

            if head_idx is None:
                head_value: Optional[int] = None
                dir_value = "ROOT"
            else:
                head_value = head_idx + 1
                dir_value = "L" if head_idx < local_i else "R"

            dep_feats_by_doc_idx[doc_i] = {
                "token_index_sentence": local_i + 1,
                "head": head_value,
                "deprel": depcode_by_local[local_i],
                "head_upos": head_upos[local_i],
                "head_form": head_form[local_i],
                "head_lemma": head_lemma[local_i],
                "dir_to_head": dir_value,
                "dist_to_head": dist_to_head[local_i],
                "dist_to_head_norm": dist_to_head_norm[local_i],
                "child_count": child_count[local_i],
                "left_child_count": left_child_count[local_i],
                "right_child_count": right_child_count[local_i],
                "is_leaf": is_leaf[local_i],
                "depth_from_root": depth_val,
                "path_len_to_root": depth_val,
                "height_to_leaf": height_val,
                "subtree_size": subtree_size_val,
                "subtree_span_width": subtree_span_width[local_i],
                "subtree_gap": subtree_gap_val,
                "crossing_arcs": crossing_per_token[local_i],
                "parent_branching_factor": parent_branching_factor[local_i],
                "sibling_index": sibling_index[local_i],
                "sibling_count": sibling_count[local_i],
                "is_root": 1 if head_local[local_i] is None else 0,
                "valid_head": 1 if head_local[local_i] is not None else 0,
                # Sentence-level metrics
                "sent_root_index": sent_root_index_1b,
                "sent_tree_depth": sent_tree_depth,
                "sent_avg_branching_nonleaf": sent_avg_branching_nonleaf,
                "sent_crossing_arcs": sent_crossing_arcs,
                "sent_is_projective": sent_is_projective,
                "sent_len": sent_len,
            }

    # Build header/order for downstream schema/rows
    base_header: list[str] = [
        "sentence_index",
        "token_index",
        "token_index_sentence",
        "token",
        "lemma",
        "upos",
        "head",
        "deprel",
    ]
    metadata_header = [f"metadata_{key}" for key in metadata_keys]
    feat_header = [f"feat_{key}" for key in sorted_feature_keys]
    # Dependency feature columns (token-level)
    dep_extra_header: list[str] = [
        "head_upos",
        "head_form",
        "head_lemma",
        "dir_to_head",
        "dist_to_head",
        "dist_to_head_norm",
        "child_count",
        "left_child_count",
        "right_child_count",
        "is_leaf",
        "depth_from_root",
        "path_len_to_root",
        "height_to_leaf",
        "subtree_size",
        "subtree_span_width",
        "subtree_gap",
        "crossing_arcs",
        "parent_branching_factor",
        "sibling_index",
        "sibling_count",
        "is_root",
        "valid_head",
        # Sentence-level features (repeated per token)
        "sent_root_index",
        "sent_tree_depth",
        "sent_avg_branching_nonleaf",
        "sent_crossing_arcs",
        "sent_is_projective",
        "sent_len",
    ]
    header = base_header + metadata_header + feat_header + dep_extra_header

    try:
        import pyarrow as pa
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise ImportError(
            "doc_to_feature_table() requires `pyarrow`. Install it via `pip install pyarrow`."
        ) from exc

    def _build_schema(feature_keys: list[str], metadata_keys: list[str]) -> "pa.Schema":
        base_fields = [
            pa.field("sentence_index", pa.int64()),
            pa.field("token_index", pa.int64()),
            pa.field("token_index_sentence", pa.int64()),
            pa.field("token", pa.string()),
            pa.field("lemma", pa.string()),
            pa.field("upos", pa.string()),
            pa.field("head", pa.int64()),
            pa.field("deprel", pa.string()),
        ]
        metadata_fields = [
            pa.field(f"metadata_{key}", pa.string()) for key in metadata_keys
        ]
        feat_fields = [pa.field(f"feat_{key}", pa.string()) for key in feature_keys]
        dep_fields = [
            pa.field("head_upos", pa.string()),
            pa.field("head_form", pa.string()),
            pa.field("head_lemma", pa.string()),
            pa.field("dir_to_head", pa.string()),
            pa.field("dist_to_head", pa.int64()),
            pa.field("dist_to_head_norm", pa.float64()),
            pa.field("child_count", pa.int64()),
            pa.field("left_child_count", pa.int64()),
            pa.field("right_child_count", pa.int64()),
            pa.field("is_leaf", pa.int64()),
            pa.field("depth_from_root", pa.int64()),
            pa.field("path_len_to_root", pa.int64()),
            pa.field("height_to_leaf", pa.int64()),
            pa.field("subtree_size", pa.int64()),
            pa.field("subtree_span_width", pa.int64()),
            pa.field("subtree_gap", pa.int64()),
            pa.field("crossing_arcs", pa.int64()),
            pa.field("parent_branching_factor", pa.int64()),
            pa.field("sibling_index", pa.int64()),
            pa.field("sibling_count", pa.int64()),
            pa.field("is_root", pa.int8()),
            pa.field("valid_head", pa.int8()),
            pa.field("sent_root_index", pa.int64()),
            pa.field("sent_tree_depth", pa.int64()),
            pa.field("sent_avg_branching_nonleaf", pa.float64()),
            pa.field("sent_crossing_arcs", pa.int64()),
            pa.field("sent_is_projective", pa.int8()),
            pa.field("sent_len", pa.int64()),
        ]
        return pa.schema(base_fields + metadata_fields + feat_fields + dep_fields)

    schema = _build_schema(sorted_feature_keys, metadata_keys)
    columns: dict[str, list[Any]] = {name: [] for name in header}

    def _serialize_metadata_value(value: Any) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, (int, float, bool)):
            return str(value)
        try:
            return json.dumps(value, ensure_ascii=True, sort_keys=True)
        except TypeError:
            return str(value)

    for doc_idx, word in enumerate(words):
        if word is None:
            for name in header:
                columns[name].append(None)
            continue

        sentence_idx_raw = getattr(word, "index_sentence", None)
        global_idx = getattr(word, "index_token", None)
        if global_idx is None:
            global_idx = doc_idx
        upos_tag = getattr(getattr(word, "upos", None), "tag", "") or ""

        dep_extra = dep_feats_by_doc_idx.get(doc_idx, {})
        deprel_value_raw = dep_extra.get("deprel", "")
        raw_head = dep_extra.get("head")
        try:
            head_value = int(raw_head) if raw_head is not None else None
        except (TypeError, ValueError):
            head_value = None
        token_in_sentence = dep_extra.get("token_index_sentence")

        deprel_value = str(deprel_value_raw) if deprel_value_raw is not None else ""

        # Explode UD features for this word
        feature_map: dict[str, str] = {}
        feats_obj = getattr(word, "features", None)
        feature_list = getattr(feats_obj, "features", None)
        if feature_list:
            for feat in feature_list:
                key = getattr(feat, "key", None)
                val = getattr(feat, "value", None)
                if key and val:
                    feature_map[str(key)] = str(val)

        row: list[Union[str, int, float, None]] = [
            sentence_idx_raw,
            global_idx,
            token_in_sentence,
            getattr(word, "string", "") or "",
            getattr(word, "lemma", "") or "",
            upos_tag,
            head_value,
            deprel_value,
        ]
        row.extend(
            _serialize_metadata_value(metadata_map.get(key)) for key in metadata_keys
        )
        row.extend(feature_map.get(key) for key in sorted_feature_keys)
        for col in dep_extra_header:
            row.append(dep_extra.get(col))
        for name, value in zip(header, row):
            columns[name].append(value)

    arrays = [pa.array(columns[field.name], type=field.type) for field in schema]
    return pa.Table.from_arrays(arrays, schema=schema)


CLTK_DATA_DIR = get_cltk_data_dir()
