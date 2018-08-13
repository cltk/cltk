"""
The Importer feature sets up the ability to work with cuneiform text(s)
one-on-one, whether it is the Code of Hammurabi, a collection of texts such as
ARM01, or whatever your research desires.

This file_importer module is for importing text files. Currently, this is
made for the purpose of reading from one of the CDLI's "download all  text"
option: (https://cdli.ucla.edu/search/download_data_new.php?data_type=all).

From this link, one has produced either one text (e.g. Code of Hammurabi:
https://cdli.ucla.edu/search/search_results.php?ObjectID=P249253)
or a variety of texts through a search function (e.g. ARM 01 publication:
https://cdli.ucla.edu/search/search_results.php?PrimaryPublication=ARM+01).
"""

import os

__author__ = ['Andrew Deloucas <ADeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'


class FileImport(object):
    """
    Takes a text file and prepares it in two ways: as a whole (raw_file) and as
    a list of strings denoting the text line by line.
    """
    def __init__(self, filename):
        """
        :param filename: name of any downloaded file, ideally from CDLI as
        discussed in the method docstring.
        """
        self.filename = filename

    def read_file(self):
        """
        Grabs filename and enables it to be read.
        :return: raw_file = unaltered text; file_lines = text split by lines.
        """
        with open(self.filename, mode='r+', encoding='utf8') as text_file:
            self.raw_file = text_file.read()  # pylint: disable= attribute-defined-outside-init
        self.file_lines = [x.rstrip() for x in self.raw_file.splitlines()]  # pylint: disable= attribute-defined-outside-init

    def file_catalog(self):
        """
        Looks at the folder filename is in and lists other files in the folder.
        :return: list of files.
        """
        pathway = os.path.split(self.filename)
        self.catalog = sorted(os.listdir(pathway[0]))  # pylint: disable= attribute-defined-outside-init
