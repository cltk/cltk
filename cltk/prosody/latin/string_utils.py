"""Utillity class for processing scansion and text."""

import unicodedata
import sys
import re
from typing import Dict, List, Tuple

__author__ = ['Todd Cook <todd.g.cook@gmail.com>']
__license__ = 'MIT License'

"""Helper methods for processing scansion"""
qu_matcher = re.compile("[qQ][uU]")


def remove_punctuation_dict() -> Dict[int, None]:
    """
    Provide a dictionary for removing punctuation, swallowing spaces.

    :return dict with punctuation from the unicode table

    >>> print("I'm ok! Oh #%&*()[]{}!? Fine!".translate(
    ... remove_punctuation_dict()).lstrip())
    Im ok Oh  Fine
    """
    tmp = dict((i, None) for i in range(sys.maxunicode)
               if unicodedata.category(chr(i)).startswith('P'))
    return tmp


def punctuation_for_spaces_dict() -> Dict[int, str]:
    """
    Provide a dictionary for removing punctuation, keeping spaces. Essential for scansion
    to keep stress patterns in alignment with original vowel positions in the verse.

    :return dict with punctuation from the unicode table

    >>> print("I'm ok! Oh #%&*()[]{}!? Fine!".translate(
    ... punctuation_for_spaces_dict()).strip())
    I m ok  Oh              Fine
    """
    return dict((i, " ") for i in range(sys.maxunicode)
                if unicodedata.category(chr(i)).startswith('P'))


def differences(scansion: str, candidate: str) -> List[int]:
    """
    Given two strings, return a list of index positions where the contents differ.

    :param scansion:
    :param candidate:
    :return:

    >>> differences("abc", "abz")
    [2]
    """
    before = scansion.replace(" ", "")
    after = candidate.replace(" ", "")
    diffs = []
    for idx, tmp in enumerate(before):
        if before[idx] != after[idx]:
            diffs.append(idx)
    return diffs


def mark_list(line: str) -> List[int]:
    """
    Given a string, return a list of index positions where a character/non blank space exists.

    :param line:
    :return:

    >>> mark_list(" a b c")
    [1, 3, 5]
    """
    marks = []
    for idx, car in enumerate(list(line)):
        if car != " ":
            marks.append(idx)
    return marks


def space_list(line: str) -> List[int]:
    """
    Given a string, return a list of index positions where a blank space occurs.

    :param line:
    :return:

    >>> space_list("    abc ")
    [0, 1, 2, 3, 7]
    """
    spaces = []
    for idx, car in enumerate(list(line)):
        if car == " ":
            spaces.append(idx)
    return spaces


def flatten(list_of_lists):
    """
    Given a list of lists, flatten all the items into one list.

    :param list_of_lists:
    :return:

    >>> flatten([ [1, 2, 3], [4, 5, 6]])
    [1, 2, 3, 4, 5, 6]
    """
    return [val for sublist in list_of_lists for val in sublist]


def to_syllables_with_trailing_spaces(line: str, syllables: List[str]) -> List[str]:
    """
    Given a line of syllables and spaces, and a list of syllables, produce a list of the
    syllables with trailing spaces attached as approriate.

    :param line:
    :param syllables:
    :return:

    >>> to_syllables_with_trailing_spaces(' arma virumque cano ',
    ... ['ar', 'ma', 'vi', 'rum', 'que', 'ca', 'no' ])
    [' ar', 'ma ', 'vi', 'rum', 'que ', 'ca', 'no ']
    """
    syllabs_spaces = []
    idx = 0
    linelen = len(line)
    for position, syl in enumerate(syllables):
        if not syl in line and re.match('w', syl, flags=re.IGNORECASE):
            syl = syl.replace('w', 'u').replace('W', 'U')
        start = line.index(syl, idx)
        idx = start + len(syl)
        if position == 0 and start > 0:  # line starts with punctuation, substituted w/ spaces
            syl = (start * " ") + syl
        if idx + 1 > len(line):
            syllabs_spaces.append(syl)
            return syllabs_spaces
        nextchar = line[idx]
        if nextchar != " ":
            syllabs_spaces.append(syl)
            continue
        else:
            tmpidx = idx
            while tmpidx < linelen and nextchar == " ":
                syl += " "
                tmpidx += 1
                if tmpidx == linelen:
                    syllabs_spaces.append(syl)
                    return syllabs_spaces
                nextchar = line[tmpidx]
            idx = tmpidx - 1
            syllabs_spaces.append(syl)
    return syllabs_spaces


def join_syllables_spaces(syllables: List[str], spaces: List[int]) -> str:
    """
    Given a list of syllables, and a list of integers indicating the position of spaces, return
    a string that has a space inserted at the designated points.

    :param syllables:
    :param spaces:
    :return:

    >>> join_syllables_spaces(["won", "to", "tree", "dun"], [3, 6, 11])
    'won to tree dun'
    """
    syllable_line = list("".join(syllables))
    for space in spaces:
        syllable_line.insert(space, " ")
    return "".join(flatten(syllable_line))


def starts_with_qu(word) -> bool:
    """
    Determine whether or not a word start with the letters Q and U.

    :param word:
    :return:

    >>> starts_with_qu("qui")
    True
    >>> starts_with_qu("Quirites")
    True
    """
    return qu_matcher.search(word) is not None


def stress_positions(stress: str, scansion: str) -> List[int]:
    """
    Given a stress value and a scansion line, return the index positions of the stresses.

    :param stress:
    :param scansion:
    :return:

    >>> stress_positions("-", "    -  U   U - UU    - U U")
    [0, 3, 6]
    """
    line = scansion.replace(" ", "")
    stresses = []
    for idx, char in enumerate(line):
        if char == stress:
            stresses.append(idx)
    return stresses


def merge_elisions(elided: List[str]) -> str:
    """
    Given a list of strings with different space swapping elisions applied, merge the elisions,
    taking the most without compounding the omissions.

    :param elided:
    :return:

    >>> merge_elisions([
    ... "ignavae agua multum hiatus", "ignav   agua multum hiatus" ,"ignavae agua mult   hiatus"])
    'ignav   agua mult   hiatus'
    """
    results = list(elided[0])
    for line in elided:
        for idx, car in enumerate(line):
            if car == " ":
                results[idx] = " "
    return "".join(results)


def move_consonant_right(letters: List[str], positions: List[int]) -> List[str]:
    """
    Given a list of letters, and a list of consonant positions, move the consonant positions to
    the right, merging strings as necessary.

    :param letters:
    :param positions:
    :return:

    >>> move_consonant_right(list("abbra"), [ 2, 3])
    ['a', 'b', '', '', 'bra']
    """
    for pos in positions:
        letters[pos + 1] = letters[pos] + letters[pos + 1]
        letters[pos] = ""
    return letters


def move_consonant_left(letters: List[str], positions: List[int]) -> List[str]:
    """
    Given a list of letters, and a list of consonant positions, move the consonant positions to
    the left, merging strings as necessary.

    :param letters:
    :param positions:
    :return:

    >>> move_consonant_left(['a', 'b', '', '', 'bra'], [1])
    ['ab', '', '', '', 'bra']
    """
    for pos in positions:
        letters[pos - 1] = letters[pos - 1] + letters[pos]
        letters[pos] = ""
    return letters


def merge_next(letters: List[str], positions: List[int]) -> List[str]:
    """
    Given a list of letter positions, merge each letter with its next neighbor.

    :param letters:
    :param positions:
    :return:

    >>> merge_next(['a', 'b', 'o', 'v', 'o' ], [0, 2])
    ['ab', '', 'ov', '', 'o']
    >>> # Note: because it operates on the original list passed in, the effect is not cummulative:
    >>> merge_next(['a', 'b', 'o', 'v', 'o' ], [0, 2, 3])
    ['ab', '', 'ov', 'o', '']
    """
    for pos in positions:
        letters[pos] = letters[pos] + letters[pos + 1]
        letters[pos + 1] = ""
    return letters


def remove_blanks(letters: List[str]):
    """
    Given a list of letters, remove any empty strings.

    :param letters:
    :return:

    >>> remove_blanks(['a', '', 'b', '', 'c'])
    ['a', 'b', 'c']
    """
    cleaned = []
    for letter in letters:
        if letter != "":
            cleaned.append(letter)
    return cleaned


def split_on(word: str, section: str) -> Tuple[str, str]:
    """
    Given a string, split on a section, and return the two sections as a tuple.

    :param word:
    :param section:
    :return:

    >>> split_on('hamrye', 'ham')
    ('ham', 'rye')
    """
    return word[:word.index(section)] + section, word[word.index(section) + len(section):]


def remove_blank_spaces(syllables: List[str]) -> List[str]:
    """
    Given a list of letters, remove any blank spaces or empty strings.

    :param syllables:
    :return:

    >>> remove_blank_spaces(['', 'a', ' ', 'b', ' ', 'c', ''])
    ['a', 'b', 'c']
    """
    cleaned = []
    for syl in syllables:
        if syl == " " or syl == '':
            pass
        else:
            cleaned.append(syl)
    return cleaned


def overwrite(char_list: List[str], regexp: str, quality: str, offset: int = 0) -> List[str]:
    """
    Given a list of characters and spaces, a matching regular expression, and a quality or
    character, replace the matching character with a space, overwriting with an offset and
    a multiplier if provided.

    :param char_list:
    :param regexp:
    :param quality:
    :param offset:
    :return:

    >>> overwrite(list('multe igne'), r'e\s[aeiou]', ' ')
    ['m', 'u', 'l', 't', ' ', ' ', 'i', 'g', 'n', 'e']
    """
    long_matcher = re.compile(regexp)
    line = "".join(char_list)
    long_positions = long_matcher.finditer(line)
    for match in long_positions:
        (start, end) = match.span()  # pylint: disable=unused-variable
        char_list[start + offset] = quality
    return char_list


def overwrite_dipthong(char_list: List[str], regexp: str, quality: str) -> List[str]:
    """
    Given a list of characters and spaces, a matching regular expression, and a quality or
    character, replace the matching character with a space, overwriting with an offset and
    a multiplier if provided.

    :param char_list: a list of characters
    :param regexp: a matching regular expression
    :param quality: a quality or character to replace
    :return: a list of characters with the dipthong overwritten

    >>> overwrite_dipthong(list('multae aguae'), r'ae\s[aeou]', ' ')
    ['m', 'u', 'l', 't', ' ', ' ', ' ', 'a', 'g', 'u', 'a', 'e']
    """
    long_matcher = re.compile(regexp)
    line = "".join(char_list)
    long_positions = long_matcher.finditer(line)
    for match in long_positions:
        (start, end) = match.span()  # pylint: disable=unused-variable
        char_list[start] = quality
        char_list[start + 1] = quality
    return char_list


def get_unstresses(stresses: List[int], count: int) -> List[int]:
    """
    Given a list of stressed positions, and count of possible positions, return a list of
    the unstressed positions.

    :param stresses: a list of stressed positions
    :param count: the number of possible positions
    :return: a list of unstressed positions

    >>> get_unstresses([0, 3, 6, 9, 12, 15], 17)
    [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16]
    """
    return list(set(range(count)) - set(stresses))
