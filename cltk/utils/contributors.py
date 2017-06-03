"""Collect CLTK authors and write contribs md."""

import ast
from collections import defaultdict
from collections import OrderedDict
import os
import re

from cltk.utils.cltk_logger import logger

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>']
__license__ = 'MIT License. See LICENSE.'


def eval_str(input_str):
    """Turn str into str or tuple."""
    inner_cast = ast.literal_eval(input_str)
    if type(inner_cast) == str:
        inner_list = [inner_cast]
    elif type(inner_cast) == tuple:
        inner_list = list(inner_cast)
    else:
        raise ValueError
    return inner_list


def get_authors(filepath):
    """Open file and check for author info."""
    str_oneline = r'(^__author__ = \[)(.*)(\])'
    comp_oneline = re.compile(str_oneline, re.MULTILINE)
    with open(filepath) as file_open:
        file_read = file_open.read()
    match = comp_oneline.findall(file_read)
    if match:
        inner_str = match[0][1]
        inner_str = eval_str(inner_str)
        return inner_str


def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  # see below for Python 2.x
        else:
            if entry.name.endswith('.py'):
                yield entry


def write_contribs(def_dict_list):
    """Write to file, in current dir, 'contributors.md'."""
    file_str = ''
    note = '# Contributors\nCLTK Core authors, ordered alphabetically by first name\n\n'
    file_str += note
    for contrib in def_dict_list:
        file_str += '## ' + contrib + '\n'
        for module in def_dict_list[contrib]:
            file_str += '* ' + module + '\n'
        file_str += '\n'
    file_name = 'contributors.md'
    with open(file_name, 'w') as file_open:
        file_open.write(file_str)
    logger.info('Wrote contribs file at "%s".', file_name)


def find_write_contribs():
    """Look for files, find authors, sort, write file."""
    map_file_auth = {}
    for x in scantree('cltk'):
        filepath = x.path
        authors_list = get_authors(filepath)
        if authors_list:
            map_file_auth[filepath] = authors_list

    map_auth_file = defaultdict(list)
    for file, authors_file in map_file_auth.items():
        for author in authors_file:
            map_auth_file[author].append(file)
    map_auth_file_alpha = OrderedDict(sorted(map_auth_file.items()))

    write_contribs(map_auth_file_alpha)


if __name__ == "__main__":
    find_write_contribs()
