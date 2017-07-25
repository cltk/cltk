"""Utility class for validating scansion patterns.
Allows users to configure the scansion symbols internally via a constructor argument;
a suitable default is provided."""

from cltk.prosody.latin.ScansionConstants import ScansionConstants
from Levenshtein import distance

__author__ = ['Todd Cook <todd.g.cook@gmail.com>']
__license__ = 'MIT License'


class MetricalValidator:
    """Currently supports: hexameter validation."""

    def is_valid_hexameter(self, scanned_line: str) -> bool:
        """Determine if a scansion pattern is one of the valid hexameter metrical patterns
        :param scanned_line: a line containing a sequence of stressed and unstressed syllables
        :return bool

        >>> print(MetricalValidator().is_valid_hexameter("-UU---UU---UU-U"))
        True
        """

        line = scanned_line.replace(self.constants.FOOT_SEPARATOR, "")
        line = line.replace(" ", "")
        if len(line) < 12:
            return False
        line = line[:-1] + self.constants.OPTIONAL_ENDING
        return self.VALID_HEXAMETERS.__contains__(line)

    def __init__(self, constants=ScansionConstants()):
        self.constants = constants
        self.VALID_HEXAMETERS = [self._build_hexameter_template(bin(x)[3:]) for x in range(32, 64)]

    def hexameter_feet(self, scansion: str) -> list:
        """Produces a list of hexameter feet, stressed and unstressed syllables with spaces intact.
        If the scansion line is not entirely correct, it will attempt to corral one or more improper
        patterns into one or more feet.

        :param: scansion: the scanned line
        :return list of strings, representing the feet of the hexameter, or if the scansion is
        wildly incorrect, the function will return an empty list.

        >>> print("|".join(MetricalValidator().hexameter_feet(
        ... "- U U   -     -  - -   -  -     - U  U  -  U")).strip() )
        - U U   |-     -  |- -   |-  -     |- U  U  |-  U
        >>> print("|".join(MetricalValidator().hexameter_feet(
        ... "- U U   -     -  U -   -  -     - U  U  -  U")).strip())
        - U U   |-     -  |U -   |-  -     |- U  U  |-  U
        """
        backwards_scan = list(scansion.rstrip())
        feet = []
        candidates = [self.constants.STRESSED + self.constants.OPTIONAL_ENDING,
                      self.constants.STRESSED + self.constants.STRESSED,
                      self.constants.STRESSED + self.constants.UNSTRESSED,
                      self.constants.UNSTRESSED + self.constants.STRESSED]
        incomplete_foot = self.constants.UNSTRESSED + self.constants.UNSTRESSED
        try:
            while len(backwards_scan) > 0:
                spaces = []
                chunk1 = backwards_scan.pop()
                while len("".join(chunk1).replace(" ", "")) == 0:
                    if len(backwards_scan) == 0:
                        feet.append(chunk1)
                        return feet[::-1]
                    chunk1 = backwards_scan.pop() + "".join(chunk1)
                chunk2 = backwards_scan.pop()
                while chunk2 == " ":
                    spaces.append(chunk2)
                    if len(backwards_scan) == 0:
                        feet.append(chunk2)
                        return feet[::-1]
                    chunk2 = backwards_scan.pop()
                new_candidate = "".join(chunk2) + "".join(spaces) + "".join(chunk1)
                if new_candidate.replace(" ", "") in candidates:
                    feet.append(new_candidate)
                else:
                    if new_candidate.replace(" ", "") == incomplete_foot:
                        spaces2 = []
                        previous_mark = backwards_scan.pop()
                        while previous_mark == " ":
                            spaces2.append(previous_mark)
                            previous_mark = backwards_scan.pop()
                        if previous_mark == self.constants.STRESSED:
                            new_candidate = "".join(previous_mark) + "".join(
                                spaces2) + new_candidate
                            feet.append(new_candidate)
                        else:
                            feet.append(new_candidate)  # invalid foot
                            spaces3 = []
                            next_mark = backwards_scan.pop()
                            while next_mark == " ":
                                spaces3.append(previous_mark)
                                next_mark = backwards_scan.pop()
                            feet.append("".join(next_mark) + "".join(spaces3) + previous_mark)
        except:
            # print("err at: " + scansion)
            return list()
        return feet[::-1]

    def _build_hexameter_template(self, stress_positions: str) -> str:
        """Build a hexameter scansion template from string of 5 binary numbers;
        NOTE: Traditionally the fifth foot is dactyl and spondee substitution is rare,
         however since it *is* a possible combination, we include it here.
        :param stress_positions: 5 binary integers, indicating whether foot is dactyl or spondee
        :return: a valid hexameter scansion template, a string representing stressed and
        unstresssed syllables with the optional terminal ending.

        >>> print(MetricalValidator()._build_hexameter_template("01010"))
        -UU---UU---UU-X
        """

        hexameter = []
        for binary in stress_positions:
            if binary == "1":
                hexameter.append(self.constants.SPONDEE)
            if binary == "0":
                hexameter.append(self.constants.DACTYL)
        hexameter.append(self.constants.HEXAMETER_ENDING)
        return "".join(hexameter)

    @staticmethod
    def hexameter_known_stresses() -> list:
        """Provide a list of known stress positions for a hexameter.
        :return: a zero based list enumerating which syllables are known to be stressed."""
        return list(range(17)[::3])

    @staticmethod
    def hexameter_possible_unstresses() -> list:
        """Provide a list of possible positions which may be unstressed syllables in a hexameter.
        :return: a zero based list enumerating which syllables are known to be unstressed."""
        return list(set(range(17)) - set(range(17)[::3]))

    def closest_hexameter_patterns(self, scansion: str) -> list:
        """Find the closest group of matching valid hexameter patterns.
        :return: list of the closest valid hexameter patterns; only candidates with a matching
        length/number of syllables are considered."""
        pattern = scansion.replace(" ", "")
        pattern = pattern.replace(self.constants.FOOT_SEPARATOR, "")
        ending = pattern[-1]
        candidate = pattern[:len(pattern) - 1] + self.constants.OPTIONAL_ENDING
        cans = [(distance(candidate, x), x) for x in self.VALID_HEXAMETERS
                if len(x) == len(candidate)]
        if cans:
            cans = sorted(cans, key=lambda tup: tup[0])
            top = cans[0][0]
            return [can[1][:-1] + ending for can in cans if can[0] == top]
        return []
