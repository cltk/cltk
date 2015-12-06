"""A method of accessing what information about CLTK Core contributors."""

from collections import defaultdict
from collections import OrderedDict
import importlib.machinery
import os

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

    @staticmethod
    def get_module_authors(module):
        """Get "__author__" variables for a module.

        TODO: If ImportError occurs (as with word2vec.py), then correctly
        get authors' names anyway.
        """
        loader = importlib.machinery.SourceFileLoader('__author__', module)
        try:
            mod = loader.load_module()
        except ImportError:
            return
        if module == 'cltk/vector/word2vec.py':
            print(True)
            input()
        try:
            mod.__author__
        except AttributeError:
            return None
        if isinstance(mod.__author__, str):
            author_list = [mod.__author__]
        elif isinstance(mod.__author__, list):
            author_list = mod.__author__

        return author_list

    def _make_authors_dict(self):
        """Build a dict of 'author': ['modules', 'contributed', 'to']."""
        authors_dict = defaultdict(list)

        modules = self.walk_cltk()
        for _module in modules:
            authors = []
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
        """Print to screen contributor info."""
        for contrib in self.credits:
            print('# ', contrib)
            for module in self.credits[contrib]:
                print('* ', module)
            print()

    def write_contribs(self):
        """Write to file, in current dir, 'contributors.md'."""
        file_str = ''
        note = '# Contributors\nCLTK Core authors, ordered alphabetically by first name\n\n'
        file_str += note
        for contrib in self.credits:
            file_str += '## ' + contrib + '\n'
            for module in self.credits[contrib]:
                file_str += '* ' + module + '\n'
            file_str += '\n'
        file_name = 'contributors.md'
        with open(file_name, 'w') as file_open:
            file_open.write(file_str)
        logger.info('Wrote contribs file at "%s".', file_name)


if __name__ == "__main__":
    CONTRIBS = Contributors()
    CONTRIBS.write_contribs()
    #print(dir(CONTRIBS))
    #print(CONTRIBS.credits)  # a dict
    print(CONTRIBS.credits['Steven Bird <stevenbird1@gmail.com>'])  # a list of modules

