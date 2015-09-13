"""Build a file ``contributors.md``, an index of contribs and what they've
helped on. This writes the file to whatever file from which it is run, thus,
to use, run from root of the project with ``python cltk/utils/build_contribs_index.py``.
"""

from collections import OrderedDict
import importlib.machinery
import os

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'


def build_contribs_file(test=None):
    """Build an index of authors and the modules for which they've
    contributed. Reads each ``*.py`` file and gets value of ``__author__``,
    then builds a dictionary of ``'author': [list of module contributions]``.

    TODO: This outputs wrong results, assigns people to work they're not
    authors of. Fix this.
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

        # test if file has __author__ in it; will fail w/o this try/except
        try:
            mod.__author__
        except AttributeError:
            continue
        # check if author value is a string, turn to list
        if type(mod.__author__) is str:
            authors = [mod.__author__]
        elif type(mod.__author__) is list:
            authors = mod.__author__
        else:
            print('ERROR: bad __author__ type: ', mod.__author__, type(mod.__author__))
            continue

        # get all authors
        for author in authors:
            if author not in file_author:
                file_author[author] = [mod_path]
            else:
                file_author[author].append(mod_path)

    # order dict by contrib's first name
    file_author_ordered = OrderedDict(sorted(file_author.items()))

    # build string to write to file
    contrib_str = ''
    note = '# Contributors\nCLTK authors alphabetically ordered by first name\n\n'
    contrib_str += note
    for name, py_files in file_author_ordered.items():
        author_row = '## {0}\n'.format(name)
        contrib_str += author_row
        for py_file in py_files:
            contrib_str += '* ' + py_file + '\n'
        contrib_str += '\n'
    if not test:
        with open('contributors.md', 'w') as contrib_md:
            contrib_md.write(contrib_str)
    else:
        return contrib_str

if __name__ == "__main__":
    build_contribs_file()
