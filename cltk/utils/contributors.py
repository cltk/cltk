"""Collect CLTK authors and write contribs md."""

import ast
from collections import defaultdict
from collections import OrderedDict
import os
import re

from typing import Dict
from typing import List
from typing import Generator
from typing import Pattern  # pylint: disable=unused-import
from typing import Union  # pylint: disable=unused-import
from typing import Tuple  # pylint: disable=unused-import
from typing import IO  # pylint: disable=unused-import

from cltk.utils.cltk_logger import logger

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>']  # type: List[str]
__license__ = 'MIT License. See LICENSE.'  # type: str


def eval_str_to_list(input_str: str) -> List[str]:
    """Turn str into str or tuple."""
    inner_cast = ast.literal_eval(input_str)  # type: List[str]
    if isinstance(inner_cast, list):
        return inner_cast
    else:
        raise ValueError


def get_authors(filepath: str) -> List[str]:
    """Open file and check for author info."""
    str_oneline = r'(^__author__ = )(\[.*?\])'  # type" str
    comp_oneline = re.compile(str_oneline, re.MULTILINE)  # type: Pattern[str]
    with open(filepath) as file_open:
        file_read = file_open.read()  # type: str
    match = comp_oneline.findall(file_read)
    if match:
        inner_list_as_str = match[0][1]  # type: str
        inner_list = eval_str_to_list(inner_list_as_str)  # type: List[str]
        return inner_list
    return list()


def scantree(path: str) -> Generator:
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            if entry.name.endswith('.py'):
                yield entry


def write_contribs(def_dict_list: Dict[str, List[str]]) -> None:
    """Write to file, in current dir, 'contributors.md'."""
    file_str = ''  # type: str
    note = '# Contributors\nCLTK Core authors, ordered alphabetically by first name\n\n'  # type: str  # pylint: disable=line-too-long
    file_str += note
    for contrib in def_dict_list:
        file_str += '## ' + contrib + '\n'
        for module in def_dict_list[contrib]:
            file_str += '* ' + module + '\n'
        file_str += '\n'
    file_name = 'contributors.md'  # type: str
    with open(file_name, 'w') as file_open:  # type: IO
        file_open.write(file_str)
    logger.info('Wrote contribs file at "%s".', file_name)


def sort_def_dict(def_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Sort values of the lists of a defaultdict(list)."""
    for _, dd_list in def_dict.items():
        dd_list.sort()
    return def_dict


def find_write_contribs() -> None:
    """Look for files, find authors, sort, write file."""
    map_file_auth = {}  # type: Dict[str, List[str]]
    for filename in scantree('cltk'):
        filepath = filename.path  # type: str
        authors_list = get_authors(filepath)  # type: List[str]
        if authors_list:
            map_file_auth[filepath] = authors_list

    map_auth_file = defaultdict(list)  # type: Dict[str, List[str]]
    for file, authors_file in map_file_auth.items():
        for author in authors_file:
            map_auth_file[author].append(file)
    # now sort the str contents of the list value
    map_auth_file = sort_def_dict(map_auth_file)
    map_auth_file_sorted = sorted(map_auth_file.items())  # type: List[Tuple[str, List[str]]]
    map_auth_file = OrderedDict(map_auth_file_sorted)

    write_contribs(map_auth_file)


if __name__ == "__main__":
    find_write_contribs()
