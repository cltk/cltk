"""Build a file ``contributors.txt``, an index of contribs and what they've
helped on. This writes the file to whatever file from which it is run.
TODO: Print this in Markdown, not an ordered Python dictionary.
"""

from collections import OrderedDict
import os
import importlib.machinery
from pprint import pprint


def build_contribs_file():
    """Build an index of authors and the modules for which they've
    contributed. Reads each ``*.py`` file and gets value of ``__author__``,
    then builds a dictionary of ``'author': [list of module contributions]``.
    """
    py_files_list = []
    for dir_path, dir_names, files in os.walk('cltk'):  # pylint: disable=W0612
        for name in files:
            if name.lower().endswith('.py') and not name.lower().startswith('__init__'):
                py_files_list.append(os.path.join(dir_path, name))

    file_author = {}
    # get all authors in each file
    for py_file in py_files_list:
        loader = importlib.machinery.SourceFileLoader('__author__', py_file)
        mod = loader.load_module()
        mod_path = mod.__file__

        # check if author value is a string, turn to list
        if type(mod.__author__) is str:
            authors = [mod.__author__]
        elif type(mod.__author__) is list:
            authors = mod.__author__
        else:
            print('ERROR: bad __author__ type: ', mod.__author__, type(mod.__author__))

        # get all authors
        for author in authors:
            if author not in file_author:
                file_author[author] = [mod_path]
            else:
                file_author[author].append(mod_path)

    # order dict by contrib's first name
    file_author_ordered = OrderedDict(sorted(file_author.items()))

    with open('contributors.txt', 'w') as contrib_f:
        pprint(file_author_ordered, contrib_f)

if __name__ == "__main__":
    build_contribs_file()
