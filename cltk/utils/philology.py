"""Miscellaneous operations for traditional philology and simple
statistics."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.utils.cltk_logger import logger
from nltk.text import ConcordanceIndex
from nltk.tokenize.punkt import PunktLanguageVars
from nltk.text import Text
import os

from collections import defaultdict



# AVAILABLE_LANGUAGES = ['latin']


class Philology:
    """Class for Philological and simple statistics."""

    def __init__(self):
        """Misc. contructors."""
        pass

    def _read_file(self, filepath):
        """Read a file and return it as a string"""
        filepath = os.path.expanduser(filepath)  #? Check this is ok if absolute paths passed in
        with open(filepath) as opened_file:
            read_file = opened_file.read()
            return read_file

    def _build_concordance(self, text_str):
        """
        Inherit or mimic the logic of ConcordanceIndex() at http://www.nltk.org/_modules/nltk/text.html
        and/or ConcordanceSearchView() & SearchCorpus() at https://github.com/nltk/nltk/blob/develop/nltk/app/concordance_app.py
        :param text_string: Text to be turned into a concordance
        :type text_string: str
        :return: str
        """
        p = PunktLanguageVars()
        tokens = p.word_tokenize(text_str.lower())  # mk lower() an option later
        #concordance = ConcordanceIndex(tokens) # this returns just one word
        #c.print_concordance('ut')  # this returns just one word

        tokens = [x for x in tokens if x not in ['[', ']', ',', ';', ':', '?']]
        tokens = set(tokens)

        t = Text(tokens)
        #t.concordance('ut')  # this has better formatting than c.print_concordance('ut')
        tokens_read = t.tokens

        for token in tokens_read:
            print(t.concordance(token, width=79, lines=1000000000))  # the original object prints a lot of junk; figure how to stop this
        #! from here, add lines to memory, then return

    def concordance(self, filepaths):
        """Replacer of text via the dict.
        :type filepaths: str or list
        :param filepaths: Filepath of text(s) to be used in concordance.
        :rtype : str
        """
        assert isinstance(filepaths, (str, list))
        if isinstance(filepaths, str):
            filepath = filepaths
            text = self._read_file(filepath)
        elif isinstance(filepaths, list):
            text = ''
            for filepath in filepaths:
                text += self._read_file(filepath)
        concordance = self._build_concordance(text)
        return concordance


class ConcordanceIndex(object):
    """
    An index that can be used to look up the offset locations at which
    a given word occurs in a document.
    # from: https://github.com/nltk/nltk/blob/7ba46b9d52ed0c03bf806193f38d8c0e9bd8a9b4/nltk/text.py
    # TODO: ch this to return str or print to file
    Test with:
    from cltk.utils.philology import ConcordanceIndex
    from nltk.tokenize.punkt import PunktLanguageVars

    with open('/Users/kyle/Desktop/bg.txt') as f:
        r = f.read()
    p = PunktLanguageVars()
    tokens = p.word_tokenize(r)

    c = ConcordanceIndex(tokens)

    tokens = set(tokens)  #! rm dupes after index, before loop
    tokens = [x for x in tokens if x not in [',', '.', ';', ':', '"', "'", '[', ']']]

    for token in tokens:
        c.print_concordance(token)
    """
    def __init__(self, tokens, key=lambda x:x):
        """
        Construct a new concordance index.
        :param tokens: The document (list of tokens) that this
            concordance index was created from.  This list can be used
            to access the context of a given word occurrence.
        :param key: A function that maps each token to a normalized
            version that will be used as a key in the index.  E.g., if
            you use ``key=lambda s:s.lower()``, then the index will be
            case-insensitive.
        """
        self._tokens = tokens
        """The document (list of tokens) that this concordance index
           was created from."""

        self._key = key
        """Function mapping each token to an index key (or None)."""

        self._offsets = defaultdict(list)
        """Dictionary mapping words (or keys) to lists of offset
           indices."""

        # Initialize the index (self._offsets)
        for index, word in enumerate(tokens):
            word = self._key(word)
            self._offsets[word].append(index)

    def tokens(self):
        """
        :rtype: list(str)
        :return: The document that this concordance index was
            created from.
        """
        return self._tokens

    def offsets(self, word):
        """
        :rtype: list(int)
        :return: A list of the offset positions at which the given
            word occurs.  If a key function was specified for the
            index, then given word's key will be looked up.
        """
        word = self._key(word)
        return self._offsets[word]

    def __repr__(self):
        return '<ConcordanceIndex for %d tokens (%d types)>' % (
            len(self._tokens), len(self._offsets))

    def print_concordance(self, word, width=150, lines=1000000):
        """
        Print a concordance for ``word`` with the specified context window.
        :param word: The target word
        :type word: str
        :param width: The width of each line, in characters (default=80)
        :type width: int
        :param lines: The number of lines to display (default=25)
        :type lines: int
        """
        half_width = (width - len(word) - 2) // 2
        context = width // 4 # approx number of words of context

        offsets = self.offsets(word)
        if offsets:
            lines = min(lines, len(offsets))
            print("Displaying %s of %s matches:" % (lines, len(offsets)))
            for i in offsets:
                if lines <= 0:
                    break
                left = (' ' * half_width +
                        ' '.join(self._tokens[i-context:i]))
                right = ' '.join(self._tokens[i+1:i+context])
                left = left[-half_width:]
                right = right[:half_width]
                print(left, self._tokens[i], right)
                lines -= 1
        else:
            print("No matches")

    def return_concordance_word(self, word, width=150, lines=1000000):
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

        return_list = []

        half_width = (width - len(word) - 2) // 2
        context = width // 4 # approx number of words of context

        offsets = self.offsets(word)
        if offsets:
            lines = min(lines, len(offsets))
            while lines:
                for i in offsets:
                    left = (' ' * half_width +
                            ' '.join(self._tokens[i-context:i]))
                    right = ' '.join(self._tokens[i+1:i+context])
                    left = left[-half_width:]
                    right = right[:half_width]
                    #print(left, '*', self._tokens[i], '*', right)
                    line_str = left + ' *' + self._tokens[i] + '* ' + right
                    return_list.append(line_str)
                    print(line_str)
                    lines -= 1
            return return_list

    def return_concordance_all(self, tokens):
        """Take a list of tokens, iteratively run each word through
        return_concordance_word and build a list of all. Ths returns a list
        of lists.
        """

        concordance_list = []
        for token in tokens:
            x = None
            x = self.return_concordance_word(token)
            concordance_list.append(x)

        return concordance_list

