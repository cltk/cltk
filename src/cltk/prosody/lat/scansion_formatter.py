"""Utility class for formatting scansion patterns"""

import logging

from cltk.prosody.lat.scansion_constants import ScansionConstants

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

__author__ = ["Todd Cook <todd.g.cook@gmail.com>"]
__license__ = "MIT License"


class ScansionFormatter:
    """
    Users can specify which scansion symbols to use in the formatting.

    >>> print(ScansionFormatter().hexameter( "-UU-UU-UU---UU--"))
    -UU|-UU|-UU|--|-UU|--
    >>> constants = ScansionConstants(unstressed="˘", \
            stressed= "¯", optional_terminal_ending="x")
    >>> formatter = ScansionFormatter(constants)
    >>> print(formatter.hexameter( "¯˘˘¯˘˘¯˘˘¯¯¯˘˘¯¯"))
    ¯˘˘|¯˘˘|¯˘˘|¯¯|¯˘˘|¯¯
    """

    def __init__(self, constants=ScansionConstants()):
        self.constants = constants
        self.stress_accent_dict = dict(
            zip(
                list(self.constants.VOWELS + self.constants.ACCENTED_VOWELS),
                list(self.constants.ACCENTED_VOWELS + self.constants.ACCENTED_VOWELS),
            )
        )

    def hexameter(self, line: str) -> str:
        """
        Format a string of hexameter metrical stress patterns into foot divisions

        :param line: the scansion pattern
        :return: the scansion string formatted with foot breaks

        >>> print(ScansionFormatter().hexameter( "-UU-UU-UU---UU--"))
        -UU|-UU|-UU|--|-UU|--
        """
        mylist = list(line)
        items = len(mylist)
        idx_start = items - 2
        idx_end = items
        while idx_start > 0:
            potential_foot = "".join(mylist[idx_start:idx_end])
            if (
                potential_foot == self.constants.HEXAMETER_ENDING
                or potential_foot == self.constants.SPONDEE
            ):
                mylist.insert(idx_start, self.constants.FOOT_SEPARATOR)
                idx_start -= 1
                idx_end -= 2
            if potential_foot == self.constants.DACTYL:
                mylist.insert(idx_start, "|")
                idx_start -= 1
                idx_end -= 3
            idx_start -= 1
        return "".join(mylist)

    def merge_line_scansion(self, line: str, scansion: str) -> str:
        """
        Merge a line of verse with its scansion string. Do not accent dipthongs.

        :param line: the original Latin verse line
        :param scansion: the scansion pattern
        :return: the original line with the scansion pattern applied via macrons

        >>> print(ScansionFormatter().merge_line_scansion(
        ... "Arma virumque cano, Troiae qui prīmus ab ōrīs",
        ... "-  U  U -  U  U  -     UU-   -   - U  U  - -"))
        Ārma virūmque canō, Troiae quī prīmus ab ōrīs

        >>> print(ScansionFormatter().merge_line_scansion(
        ... "lītora, multum ille et terrīs iactātus et alto",
        ... " - U U   -     -    -   -  -   -  - U  U  -  U"))
        lītora, mūltum īlle ēt tērrīs iāctātus et ālto

        >>> print(ScansionFormatter().merge_line_scansion(
        ... 'aut facere, haec a te dictaque factaque sunt',
        ... ' -   U U      -  -  -  -  U  U  -  U  U  -  '))
        aut facere, haec ā tē dīctaque fāctaque sūnt
        """
        letters = list(line)
        marks = list(scansion)
        if len(scansion) < len(line):
            marks += ((len(line) - len(scansion)) * " ").split()
        for idx in range(0, len(marks)):
            if marks[idx] == self.constants.STRESSED:
                vowel = letters[idx]
                if vowel not in self.stress_accent_dict:
                    LOG.error(
                        "problem! vowel: {} not in dict for line {}".format(vowel, line)
                    )
                    pass
                else:
                    if idx > 1:
                        if (letters[idx - 2] + letters[idx - 1]).lower() == "qu":
                            new_vowel = self.stress_accent_dict[vowel]
                            letters[idx] = new_vowel
                            continue
                    if idx > 0:
                        if letters[idx - 1] + vowel in self.constants.DIPTHONGS:
                            continue
                        new_vowel = self.stress_accent_dict[vowel]
                        letters[idx] = new_vowel
                    else:
                        new_vowel = self.stress_accent_dict[vowel]
                        letters[idx] = new_vowel
        return "".join(letters).rstrip()
