"""Parent class and utility class for producing a scansion pattern for a line of Latin verse.

Some useful methods
* Perform a conservative i to j transformation
* Performs elisions
* Accents vowels by position
* Breaks the line into a list of syllables by calling a Syllabifier class which may be injected
into this classes constructor.

"""

import logging
import re
from typing import Any, Dict, List

import cltk.prosody.lat.string_utils as string_utils
from cltk.prosody.lat.metrical_validator import MetricalValidator
from cltk.prosody.lat.scansion_constants import ScansionConstants
from cltk.prosody.lat.scansion_formatter import ScansionFormatter
from cltk.prosody.lat.syllabifier import Syllabifier
from cltk.prosody.lat.verse import Verse

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

__author__ = ["Todd Cook <todd.g.cook@gmail.com>"]
__license__ = "MIT License"


class VerseScanner:
    """
    The scansion symbols used can be configured by passing a suitable constants class to
    the constructor.
    """

    def __init__(
        self, constants=ScansionConstants(), syllabifier=Syllabifier(), **kwargs
    ):
        self.constants = constants
        self.remove_punct_map = string_utils.remove_punctuation_dict()
        self.punctuation_substitutions = string_utils.punctuation_for_spaces_dict()
        self.metrical_validator = MetricalValidator(constants)
        self.formatter = ScansionFormatter(constants)
        self.syllabifier = syllabifier
        self.inverted_amphibrach_re = re.compile(
            r"{}\s*{}\s*{}".format(
                self.constants.STRESSED,
                self.constants.UNSTRESSED,
                self.constants.STRESSED,
            )
        )
        self.syllable_matcher = re.compile(
            r"[{}]".format(
                self.constants.VOWELS
                + self.constants.ACCENTED_VOWELS
                + self.constants.LIQUIDS
                + self.constants.MUTES
            )
        )

    def transform_i_to_j(self, line: str) -> str:
        """
        Transform instances of consonantal i to j
        :param line:
        :return:

        >>> print(VerseScanner().transform_i_to_j("iactātus"))
        jactātus
        >>> print(VerseScanner().transform_i_to_j("bracchia"))
        bracchia
        """

        words = line.split(" ")
        space_list = string_utils.space_list(line)
        corrected_words = []
        for word in words:
            found = False
            for prefix in self.constants.PREFIXES:
                if word.startswith(prefix) and word != prefix:
                    corrected_words.append(
                        self.syllabifier.convert_consonantal_i(prefix)
                    )
                    corrected_words.append(
                        self.syllabifier.convert_consonantal_i(word[len(prefix) :])
                    )
                    found = True
                    break
            if not found:
                corrected_words.append(self.syllabifier.convert_consonantal_i(word))
        new_line = string_utils.join_syllables_spaces(corrected_words, space_list)
        char_list = string_utils.overwrite(
            list(new_line),
            r"\b[iī][{}]".format(
                self.constants.VOWELS + self.constants.ACCENTED_VOWELS
            ),
            "j",
        )
        char_list = string_utils.overwrite(
            char_list, r"\b[I][{}]".format(self.constants.VOWELS_WO_I), "J"
        )
        char_list = string_utils.overwrite(
            char_list,
            r"[{}][i][{}]".format(self.constants.VOWELS_WO_I, self.constants.VOWELS),
            "j",
            1,
        )
        return "".join(char_list)

    def transform_i_to_j_optional(self, line: str) -> str:
        """
        Sometimes for the demands of meter a more permissive i to j transformation is warranted.

        :param line:
        :return:

        >>> print(VerseScanner().transform_i_to_j_optional("Italiam"))
        Italjam
        >>> print(VerseScanner().transform_i_to_j_optional("Lāvīniaque"))
        Lāvīnjaque
        >>> print(VerseScanner().transform_i_to_j_optional("omnium"))
        omnjum
        """
        words = line.split(" ")
        space_list = string_utils.space_list(line)
        corrected_words = []
        for word in words:
            found = False
            for prefix in self.constants.PREFIXES:
                if word.startswith(prefix) and word != prefix:
                    corrected_words.append(
                        self.syllabifier.convert_consonantal_i(prefix)
                    )
                    corrected_words.append(
                        self.syllabifier.convert_consonantal_i(word[len(prefix) :])
                    )
                    found = True
                    break
            if not found:
                corrected_words.append(self.syllabifier.convert_consonantal_i(word))
        new_line = string_utils.join_syllables_spaces(corrected_words, space_list)
        #  the following two may be tunable and subject to improvement
        char_list = string_utils.overwrite(
            list(new_line),
            "[bcdfgjkmpqrstvwxzBCDFGHJKMPQRSTVWXZ][i][{}]".format(
                self.constants.VOWELS_WO_I
            ),
            "j",
            1,
        )
        char_list = string_utils.overwrite(
            char_list,
            "[{}][iI][{}]".format(self.constants.LIQUIDS, self.constants.VOWELS_WO_I),
            "j",
            1,
        )
        return "".join(char_list)

    def accent_by_position(self, verse_line: str) -> str:
        """
        Accent vowels according to the rules of scansion.

        :param verse_line: a line of unaccented verse
        :return: the same line with vowels accented by position

        >>> print(VerseScanner().accent_by_position(
        ... "Arma virumque cano, Troiae qui primus ab oris").lstrip())
        Ārma virūmque canō  Trojae qui primus ab oris
        """
        line = verse_line.translate(self.punctuation_substitutions)
        line = self.transform_i_to_j(line)
        marks = list(line)

        # locate and save dipthong positions since we don't want them being accented
        dipthong_positions = []
        for dipth in self.constants.DIPTHONGS:
            if dipth in line:
                dipthong_positions.append(line.find(dipth))

        # Vowels followed by 2 consonants
        # The digraphs ch, ph, th, qu and sometimes gu and su count as single consonants.
        # see http://people.virginia.edu/~jdk3t/epicintrog/scansion.htm
        marks = string_utils.overwrite(
            marks,
            "[{}][{}][{}]".format(
                self.constants.VOWELS,
                self.constants.CONSONANTS,
                self.constants.CONSONANTS_WO_H,
            ),
            self.constants.STRESSED,
        )
        # one space (or more for 'dropped' punctuation may intervene)
        marks = string_utils.overwrite(
            marks,
            r"[{}][{}]\s*[{}]".format(
                self.constants.VOWELS,
                self.constants.CONSONANTS,
                self.constants.CONSONANTS_WO_H,
            ),
            self.constants.STRESSED,
        )
        # ... if both consonants are in the next word, the vowel may be long
        # .... but it could be short if the vowel is not on the thesis/emphatic part of the foot
        # ... see Gildersleeve and Lodge p.446
        marks = string_utils.overwrite(
            marks,
            r"[{}]\s*[{}][{}]".format(
                self.constants.VOWELS,
                self.constants.CONSONANTS,
                self.constants.CONSONANTS_WO_H,
            ),
            self.constants.STRESSED,
        )
        #  x is considered as two letters
        marks = string_utils.overwrite(
            marks, "[{}][xX]".format(self.constants.VOWELS), self.constants.STRESSED
        )
        #  z is considered as two letters
        marks = string_utils.overwrite(
            marks, r"[{}][zZ]".format(self.constants.VOWELS), self.constants.STRESSED
        )
        original_verse = list(line)
        for idx, word in enumerate(original_verse):
            if marks[idx] == self.constants.STRESSED:
                original_verse[idx] = self.constants.VOWELS_TO_ACCENTS[
                    original_verse[idx]
                ]
        # make sure dipthongs aren't accented
        for idx in dipthong_positions:
            if original_verse[idx + 1] in self.constants.ACCENTS_TO_VOWELS:
                original_verse[idx + 1] = self.constants.ACCENTS_TO_VOWELS[
                    original_verse[idx + 1]
                ]

        return "".join(original_verse)

    def elide_all(self, line: str) -> str:
        """
        Given a string of space separated syllables, erase with spaces the syllable portions
        that would disappear according to the rules of elision.

        :param line:
        :return:
        """
        marks = list(line.translate(self.remove_punct_map))
        all_vowels = self.constants.VOWELS + self.constants.ACCENTED_VOWELS
        tmp = "".join(marks)
        # Elision rules are compound but not cummulative: we place all elision edits into a list
        #  of candidates, and then merge, taking the least of each section of the line.
        candidates = [
            tmp,
            self.elide(
                tmp,
                r"[{}][{}]\s+[{}]".format(
                    self.constants.CONSONANTS, all_vowels, all_vowels
                ),
                1,
                1,
            ),
            self.elide(
                tmp,
                r"[{}][{}]\s+[hH]".format(self.constants.CONSONANTS, all_vowels),
                1,
                1,
            ),
            self.elide(tmp, r"[aāuū]m\s+[{}]".format(all_vowels), 2),
            self.elide(tmp, r"ae\s+[{}]".format(all_vowels), 2),
            self.elide(tmp, r"[{}]\s+[{}]".format(all_vowels, all_vowels), 1),
            self.elide(tmp, r"[uū]m\s+h", 2),
        ]
        results = string_utils.merge_elisions(candidates)
        return results

    def calc_offset(self, syllables_spaces: List[str]) -> Dict[int, int]:
        """
        Calculate a dictionary of accent positions from a list of syllables with spaces.

        :param syllables_spaces:
        :return:
        """
        line = string_utils.flatten(syllables_spaces)
        mydict = {}  # type: Dict[int, int]
        # #defaultdict(int) #type: Dict[int, int]
        for idx, syl in enumerate(syllables_spaces):
            target_syllable = syllables_spaces[idx]
            skip_qu = string_utils.starts_with_qu(target_syllable)
            matches = list(self.syllable_matcher.finditer(target_syllable))
            for position, possible in enumerate(matches):
                if skip_qu:
                    skip_qu = False
                    continue
                (start, end) = possible.span()
                if (
                    target_syllable[start:end]
                    in self.constants.VOWELS + self.constants.ACCENTED_VOWELS
                ):
                    part = line[: len("".join(syllables_spaces[:idx]))]
                    offset = len(part) + start
                    if (
                        line[offset]
                        not in self.constants.VOWELS + self.constants.ACCENTED_VOWELS
                    ):
                        LOG.error("Problem at line {} offset {}".format(line, offset))
                    mydict[idx] = offset
        return mydict

    def produce_scansion(
        self, stresses: list, syllables_wspaces: List[str], offset_map: Dict[int, int]
    ) -> str:
        """
        Create a scansion string that has stressed and unstressed syllable positions in locations
        that correspond with the original texts syllable vowels.

        :param stresses list of syllable positions
        :param syllables_wspaces list of syllables with spaces escaped for punctuation or elision
        :param offset_map dictionary of syllable positions, and an offset amount which is the
        number of spaces to skip in the original line before inserting the accent.
        """
        scansion = list(" " * len(string_utils.flatten(syllables_wspaces)))
        unstresses = string_utils.get_unstresses(stresses, len(syllables_wspaces))
        try:
            for idx in unstresses:
                location = offset_map.get(idx)
                if location is not None:
                    scansion[location] = self.constants.UNSTRESSED
            for idx in stresses:
                location = offset_map.get(idx)
                if location is not None:
                    scansion[location] = self.constants.STRESSED
        except Exception as e:
            LOG.error(
                "problem with syllables; check syllabification {}, {}".format(
                    syllables_wspaces, e
                )
            )
        return "".join(scansion)

    def flag_dipthongs(self, syllables: List[str]) -> List[int]:
        """
        Return a list of syllables that contain a dipthong

        :param syllables:
        :return:
        """
        long_positions = []
        for idx, syl in enumerate(syllables):
            for dipthong in self.constants.DIPTHONGS:
                if dipthong in syllables[idx]:
                    if not string_utils.starts_with_qu(syllables[idx]):
                        long_positions.append(idx)
        return long_positions

    def elide(self, line: str, regexp: str, quantity: int = 1, offset: int = 0) -> str:
        """
        Erase a section of a line, matching on a regex, pushing in a quantity of blank spaces,
        and jumping forward with an offset if necessary.
        If the elided vowel was strong, the vowel merged with takes on the stress.

        :param line:
        :param regexp:
        :param quantity:
        :param offset:
        :return:

        >>> print(VerseScanner().elide("uvae avaritia", r"[e]\s*[a]"))
        uv   āvaritia
        >>> print(VerseScanner().elide("mare avaritia", r"[e]\s*[a]"))
        mar  avaritia
        """
        matcher = re.compile(regexp)
        positions = matcher.finditer(line)
        new_line = line
        for match in positions:
            (start, end) = match.span()  # pylint: disable=unused-variable
            if (start > 0) and new_line[
                start - 1 : start + 1
            ] in self.constants.DIPTHONGS:
                vowel_to_coerce = new_line[end - 1]
                new_line = (
                    new_line[: (start - 1) + offset]
                    + (" " * (quantity + 2))
                    + self.constants.stress_accent_dict[vowel_to_coerce]
                    + new_line[end:]
                )
            else:
                new_line = (
                    new_line[: start + offset]
                    + (" " * quantity)
                    + new_line[start + quantity + offset :]
                )
        return new_line

    def correct_invalid_start(self, scansion: str) -> str:
        """
        If a hexameter, hendecasyllables, or pentameter scansion starts with spondee,
        an unstressed syllable in the third position must actually be stressed,
        so we will convert it: - - | U    ->  - - | -

        :param scansion:
        :return:

        >>> print(VerseScanner().correct_invalid_start(
        ... " -   - U   U -  -  U U U U  U U  - -").strip())
        -   - -   - -  -  U U U U  U U  - -
        """
        mark_list = string_utils.mark_list(scansion)
        raw_scansion = scansion.replace(" ", "")
        if raw_scansion.startswith(self.constants.SPONDEE + self.constants.UNSTRESSED):
            new_scansion = list(
                self.constants.SPONDEE + self.constants.SPONDEE + raw_scansion[4:]
            )
            corrected = "".join(new_scansion)
            new_sequence = list(" " * len(scansion))
            for idx, car in enumerate(corrected):
                new_sequence[mark_list[idx]] = car
            return "".join(new_sequence)
        return scansion

    def correct_first_two_dactyls(self, scansion: str) -> str:
        """
        If a hexameter or pentameter starts with spondee,
        an unstressed syllable in the third position must actually be stressed,
        so we will convert it: - - | U    ->  - - | -
        And/or if the starting pattern is spondee + trochee + stressed, then the unstressed
        trochee can be corrected: - - | - u | -   ->  - - | - -| -

        :param scansion:
        :return:

        >>> print(VerseScanner().correct_first_two_dactyls(
        ... " -   - U   U -  -  U U U U  U U  - -")) # doctest: +NORMALIZE_WHITESPACE
         -   - -   - -  -  U U U U  U U  - -
        """
        mark_list = string_utils.mark_list(scansion)
        new_line = self.correct_invalid_start(scansion)
        raw_scansion = new_line.replace(" ", "")
        if raw_scansion.startswith(
            self.constants.SPONDEE + self.constants.TROCHEE + self.constants.STRESSED
        ):
            new_scansion = list(
                self.constants.SPONDEE
                + self.constants.SPONDEE
                + self.constants.STRESSED
                + raw_scansion[5:]
            )
            corrected = "".join(new_scansion)
            new_sequence = list(" " * len(scansion))
            for idx, car in enumerate(corrected):
                new_sequence[mark_list[idx]] = car
            return "".join(new_sequence)
        return new_line

    def assign_candidate(self, verse: Verse, candidate: str) -> Verse:
        """
        Helper method; make sure that the verse object is properly packaged.

        :param verse:
        :param candidate:
        :return:
        """
        verse.scansion = candidate
        verse.valid = True
        verse.accented = self.formatter.merge_line_scansion(
            verse.original, verse.scansion
        )
        return verse
