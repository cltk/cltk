"""Miscellaneous operations for traditional philology and simple
statistics."""

from collections import defaultdict
import os
from typing import Any  # pylint: disable=unused-import
from typing import DefaultDict  # pylint: disable=unused-import
from typing import IO  # pylint: disable=unused-import
from typing import List
from typing import Set  # pylint: disable=unused-import
from typing import Union

# from nltk.text import ConcordanceIndex
from nltk.tokenize.punkt import PunktLanguageVars
import pyuca

from cltk.utils.cltk_logger import logger

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Steven Bird <stevenbird1@gmail.com>',  # original author of NLTK's ConcordanceIndex()
              'Edward Loper <edloper@gmail.com>']  # original author of NLTK's ConcordanceIndex()  # type: List[str]  # pylint: disable=line-too-long
__license__ = 'MIT License. See LICENSE.'  # type: str


def read_file(filepath: str) -> str:
    """Read a file and return it as a string"""
    # ? Check this is ok if absolute paths passed in
    filepath = os.path.expanduser(filepath)
    with open(filepath) as opened_file:  # type: IO
        file_read = opened_file.read()  # type: str
        return file_read


def build_concordance(text_str: str) -> List[List[str]]:
    """
    Inherit or mimic the logic of ConcordanceIndex() at:
     http://www.nltk.org/_modules/nltk/text.html
    and/or ConcordanceSearchView() & SearchCorpus() at:
     https://github.com/nltk/nltk/blob/develop/nltk/app/concordance_app.py
    :param text_string: Text to be turned into a concordance
    :type text_string: str
    :return: list
    """
    punkt_vars = PunktLanguageVars()  # type: PunktLanguageVars
    orig_tokens = punkt_vars.word_tokenize(text_str)  # type: List[str]
    concordance_index = ConcordanceIndex(orig_tokens)  # type: Any
    #! rm dupes after index, before loop
    tokens_set = set(orig_tokens)  # type: Set[str]
    punct_list = [',', '.', ';', ':', '"', "'", '[', ']']  # type: List[str]
    # this needs to be changed or rm'ed
    tokens = [x for x in tokens_set if x not in punct_list]  # List[str]
    index = concordance_index.return_concordance_all(tokens)  # List[List[str]]
    return index


def write_concordance_from_string(text: str, name: str) -> None:
    """A reworkinng of write_concordance_from_file(). Refactor these."""
    list_of_lists = build_concordance(text)  # type: List[List[str]]
    user_data_rel = '~/cltk_data/user_data'  # type: str
    user_data = os.path.expanduser(user_data_rel)  # type: str
    if not os.path.isdir(user_data):
        os.makedirs(user_data)
    file_path = os.path.join(user_data, 'concordance_' + name + '.txt')  # type: str
    concordance_output = ''  # type: str
    for word_list in list_of_lists:
        for line in word_list:
            concordance_output += line + '\n'
    try:
        with open(file_path, 'w') as open_file:
            open_file.write(concordance_output)
            logger.info("Wrote concordance to '%s'.", file_path)
    except IOError as io_error:
        logger.error("Failed to write concordance to '%s'. Error: %s", file_path, io_error)


def write_concordance_from_file(filepaths: Union[str, List[str]], name: str) -> None:
    """This calls the modified ConcordanceIndex, taken and modified from
    the NLTK, and writes to disk a file named 'concordance_' + name at
    '~/cltk_data/user_data/'.

    TODO: Add language (here or in class), lowercase option, stemming/
    lemmatization, else?

    :type filepaths: str or list
    :param filepaths: Filepath of text(s) to be used in concordance.
    :rtype : str
    """
    assert isinstance(filepaths, (str, list))
    if isinstance(filepaths, str):
        filepath = filepaths  # type: str
        text = read_file(filepath)  # type: str
    elif isinstance(filepaths, list):
        text = ''
        for filepath in filepaths:
            text += read_file(filepath)
    list_of_lists = build_concordance(text)  # type: List[List[str]]
    user_data_rel = '~/cltk_data/user_data'  # type: str
    user_data = os.path.expanduser(user_data_rel)  # type: str
    if not os.path.isdir(user_data):
        os.makedirs(user_data)
    file_path = os.path.join(user_data, 'concordance_' + name + '.txt')
    concordance_output = ''  # type: str
    for word_list in list_of_lists:
        for line in word_list:
            concordance_output += line + '\n'
    try:
        with open(file_path, 'w') as open_file:  # type: IO
            open_file.write(concordance_output)
            logger.info("Wrote concordance to '%s'.", file_path)
    except IOError as io_error:
        logger.error("Failed to write concordance to '%s'. Error: %s", file_path, io_error)


class ConcordanceIndex:
    """
    An index that can be used to look up the offset locations at which
    a given word occurs in a document. This is a helper class not
    intended for direct use. Repurposed from the NLTK:
    https://github.com/nltk/nltk/blob/7ba46b9d52ed0c03bf806193f38d8c0e9bd8a9b4/nltk/text.py

    TODO: Try redoing this with inheritance from NLTK.
    """
    def __init__(self, tokens: List[str]) -> None:
        """
        Construct a new concordance index.
        :param tokens: The document (list of tokens) that this
            concordance index was created from.  This list can be used
            to access the context of a given word occurrence.
        """
        self._tokens = tokens  # type: List[str]
        """The document (list of tokens) that this concordance index
           was created from."""

        self._offsets = defaultdict(list)  # type: DefaultDict[str, List[int]]
        """Dictionary mapping words (or keys) to lists of offset indices."""
        # Initialize the index (self._offsets)
        for index, word in enumerate(tokens):
            self._offsets[word].append(index)

    def tokens(self) -> List[str]:
        """
        :rtype: list(str)
        :return: The document that this concordance index was
            created from.
        """
        return self._tokens

    def offsets(self, word: str) -> List[int]:
        """
        :rtype: list(int)
        :return: A list of the offset positions at which the given
            word occurs.  If a key function was specified for the
            index, then given word's key will be looked up.
        """
        return self._offsets[word]

    def __repr__(self) -> str:
        return '<ConcordanceIndex for %d tokens (%d types)>' % (
            len(self._tokens), len(self._offsets))

    def return_concordance_word(self, word: str,
                                width: int = 150,
                                lines: int = 1000000) -> List[str]:
        """
        Makes concordance for ``word`` with the specified context window.
        Returns a list of concordance lines for the given input word.
        :param word: The target word
        :type word: str
        :param width: The width of each line, in characters (default=80)
        :type width: int
        :param lines: The number of lines to display (default=25)
        :type lines: int
        """

        return_list = []  # type: List[str]

        half_width = (width - len(word) - 2) // 2  # type: int
        context = width // 4  # type: int  # approx number of words of context

        offsets = self.offsets(word)  # type: List[int]
        if offsets:
            lines = min(lines, len(offsets))
            while lines:
                for i in offsets:
                    left = (' ' * half_width +
                            ' '.join(self._tokens[i-context:i]))  # type: str
                    right = ' '.join(self._tokens[i+1:i+context])  # type: str
                    left = left[-half_width:]
                    right = right[:half_width]
                    line_str = left + ' ' + self._tokens[i] + ' ' + right  # type: str
                    return_list.append(line_str)  # type: List[str]
                    lines -= 1
            return return_list
        return list()

    def return_concordance_all(self, tokens: List[str]) -> List[List[str]]:
        """Take a list of tokens, iteratively run each word through
        return_concordance_word and build a list of all. This returns a list
        of lists.
        """

        coll = pyuca.Collator()  # type: pyuca.Collator
        tokens = sorted(tokens, key=coll.sort_key)  #! is the list order preserved?

        concordance_list = []  # type: List[List[str]]
        for token in tokens:
            concordance_list_for_word = self.return_concordance_word(token)  # List[str]
            if concordance_list_for_word:
                concordance_list.append(concordance_list_for_word)

        return concordance_list
