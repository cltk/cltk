"""A method of accessing what information about CLTK Core contributors."""

from collections import defaultdict
from collections import OrderedDict
import importlib.machinery
import os
import re
import sys

from cltk.utils.cltk_logger import logger

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'


class Contributors:
    """An object which data about available contributors."""

    def __init__(self):
        """Upon loading this class, query all modules for "__author__"
        variables throughout library."""
        self.credits = self._make_authors_dict()

    def walk_cltk(self):
        """Walk through either this repo's corpus or the directory where CLTK
        is installed. The former is useful when building a contribs file
        without before installing and packaging the software.
        """
        py_files_list = []
        for dir_path, dir_names, files in os.walk('cltk'):  # pylint: disable=W0612
            for name in files:
                if name.lower().endswith('.py') and not name.lower().startswith('__init__'):
                    py_files_list.append(os.path.join(dir_path, name))
        return py_files_list

    def get_module_authors(self, module):
        """# Get "__author__" variables for a module"""
        loader = importlib.machinery.SourceFileLoader('__author__', module)
        try:
            mod = loader.load_module()
        except ImportError:
            pass
        try:
            mod.__author__
        except AttributeError:
            return None
        if type(mod.__author__) is str:
            author_list = [mod.__author__]
        elif type(mod.__author__) is list:
            author_list = mod.__author__
        return author_list

    def _make_authors_dict(self):
        """Build a dict of 'author': ['modules', 'contributed', 'to']."""
        authors_dict = defaultdict(list)

        modules = self.walk_cltk()
        for _module in modules:
            authors = self.get_module_authors(_module)

            try:
                for author in authors:
                    authors_dict[author].append(_module)
            except TypeError as type_err:
                if type_err.args[0] == "'NoneType' object is not iterable":
                    continue

        authors_dict = OrderedDict(sorted(authors_dict.items()))  # Sort by first name

        return authors_dict

    def show(self):
        for contrib in self.credits:
            print('# ', contrib)
            for module in self.credits[contrib]:
                print('* ', module)
            print()

    def write_contribs(self):
        file_str = ''
        note = '# Contributors\nCLTK Core authors, ordered alphabetically by first name\n\n'
        file_str += note
        for contrib in self.credits:
            file_str += '## ' + contrib + '\n'
            for module in self.credits[contrib]:
                file_str += '* ' + module + '\n'
            file_str += '\n'
        with open('contributors.md', 'w') as file_open:
            file_open.write(file_str)


if __name__ == "__main__":
    contribs = Contributors()
    #contribs.write_contribs()
    #print(dir(contribs))
    #print(contribs.credits)  # a dict
    print(contribs.credits['Patrick J. Burns <patrick@diyclassics.org>'])  # a list of modules

