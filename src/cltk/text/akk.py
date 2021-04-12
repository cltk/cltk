import re
from typing import List, Tuple
from unicodedata import normalize

__author__ = ["Andrew Deloucas <ADeloucas@g.harvard.com>"]
__license__ = "MIT License. See LICENSE."

VOWELS = "aeiouAEIOU"
TITTLES = {
    r"s,": chr(0x1E63),
    r"sz": chr(0x0161),
    r"t,": chr(0x1E6D),
    r"'": chr(0x02BE),
    r"S,": chr(0x1E62),
    r"SZ": chr(0x0160),
    r"T,": chr(0x1E6C),
}


def _convert_consonant(sign: str) -> str:
    """
    Uses dictionary to replace ATF convention for unicode characters.

    >>> signs = ["as,", "S,ATU", "tet,", "T,et", "sza", "ASZ"]
    >>> [_convert_consonant(s) for s in signs]
    ['aṣ', 'ṢATU', 'teṭ', 'Ṭet', 'ša', 'AŠ']
    """

    for key in TITTLES:
        sign = sign.replace(key, TITTLES[key])
    return sign


def _convert_number_to_subscript(num: int) -> str:
    """
    Converts number into subscript.

    >>> signs = ["a", "a1", "be2", "bad3", "buru14"]
    >>> [_get_number_from_sign(s)[1] for s in signs]
    [0, 1, 2, 3, 14]
    """

    subscript = ""
    for character in str(num):
        subscript += chr(0x2080 + int(character))
    return subscript


def _get_number_from_sign(sign: str) -> Tuple[str, int]:
    """
    Captures numbers after sign for __convert_num__.

    input = ["a", "a1", "be2", "bad3", "buru14"]
    output = [0, 1, 2, 3, 14]

    :param sign: string
    :return: string, integer
    """

    match = re.search(r"\d{1,3}$", sign)
    if match is None:
        number = 0
    else:
        number = match[0]
    return sign, int(number)


# noinspection PyUnboundLocalVariable
class ATFConverter:  # pylint: disable=too-few-public-methods
    """
    Class to convert tokens to unicode.


    Transliterates ATF data from CDLI into readable unicode.
        sz = š
        s, = ṣ
        t, = ṭ
        ' = ʾ
        Sign values for 2-3 take accent aigu and accent grave standards,
        otherwise signs are printed as subscript.

    For in depth reading on ATF-formatting for CDLI and ORACC:
        Oracc ATF Primer = http://oracc.museum.upenn.edu/doc/help/editinginatf/
        primer/index.html
        ATF Structure = http://oracc.museum.upenn.edu/doc/help/editinginatf/
        primer/structuretutorial/index.html
        ATF Inline = http://oracc.museum.upenn.edu/doc/help/editinginatf/
        primer/inlinetutorial/index.html
    """

    def __init__(self, two_three: bool = True):
        """
        :param two_three: turns on or off accent marking.
        """

        self.two_three = two_three

    def _convert_num(self, sign: str) -> str:
        """
        Converts number registered in get_number_from_sign.
        """

        # Check if there's a number at the end
        new_sign, num = _get_number_from_sign(sign)
        if num < 2:  # "ab" -> "ab"
            return new_sign.replace(str(num), _convert_number_to_subscript(num))
        if num > 3:  # "buru14" -> "buru₁₄"
            return new_sign.replace(str(num), _convert_number_to_subscript(num))
        if self.two_three:  # pylint: disable=no-else-return
            return new_sign.replace(str(num), _convert_number_to_subscript(num))
        else:
            # "bad3" -> "bàd"
            for i, character in enumerate(new_sign):
                new_vowel = ""
                if character in VOWELS:
                    if num == 2:
                        # noinspection PyUnusedLocal
                        new_vowel = character + chr(0x0301)
                    elif num == 3:
                        new_vowel = character + chr(0x0300)
                    break
            return (
                new_sign[:i]
                + normalize("NFC", new_vowel)
                + new_sign[i + 1 :].replace(str(num), "")
            )

    def process(self, tokens: List[str]) -> List[str]:
        """
        Expects a list of tokens, will return the list converted from ATF
        format to print-format.

        >>> c = ATFConverter()
        >>> c.process(["a", "a2", "a3", "geme2", "bad3", "buru14"])
        ['a', 'a₂', 'a₃', 'geme₂', 'bad₃', 'buru₁₄']
        """

        return [self._convert_num(_convert_consonant(token)) for token in tokens]
