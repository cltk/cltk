"""Utility class for producing a scansion pattern for a Latin hendecasyllables.

Given a line of hendecasyllables, the scan method performs a series of transformation and checks
are performed and for each one performed successfully, a note is added to the scansion_notes
list so that end users may view the provenance of a scansion.
"""

import re

from Levenshtein import distance

import cltk.prosody.lat.string_utils as string_utils
from cltk.prosody.lat.metrical_validator import MetricalValidator
from cltk.prosody.lat.scansion_constants import ScansionConstants
from cltk.prosody.lat.scansion_formatter import ScansionFormatter
from cltk.prosody.lat.syllabifier import Syllabifier
from cltk.prosody.lat.verse import Verse
from cltk.prosody.lat.verse_scanner import VerseScanner

__author__ = ["Todd Cook <todd.g.cook@gmail.com>"]
__license__ = "MIT License"


class HendecasyllableScanner(VerseScanner):
    """The scansion symbols used can be configured by passing a suitable constants class to
    the constructor."""

    def __init__(
        self,
        constants=ScansionConstants(),
        syllabifier=Syllabifier(),
        optional_tranform=False,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
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
        self.optional_transform = optional_tranform

    def scan(self, original_line: str, optional_transform: bool = False) -> Verse:
        """
        Scan a line of Latin hendecasyllables and produce a scansion pattern, and other data.

        :param original_line: the original line of Latin verse
        :param optional_transform: whether or not to perform i to j transform for syllabification
        :return: a Verse object

        >>> scanner = HendecasyllableScanner()
        >>> print(scanner.scan("Cui dono lepidum novum libellum"))
        Verse(original='Cui dono lepidum novum libellum', scansion='  -  U -  U U -   U -   U -  U ', meter='hendecasyllable', valid=True, syllable_count=11, accented='Cui donō lepidūm novūm libēllum', scansion_notes=['Corrected invalid start.'], syllables = ['Cui', 'do', 'no', 'le', 'pi', 'dūm', 'no', 'vūm', 'li', 'bēl', 'lum'])
        >>> print(scanner.scan(
        ... "ārida modo pumice expolitum?").scansion)  # doctest: +NORMALIZE_WHITESPACE
        - U -  U U  - U   -  U - U
        """
        verse = Verse(original_line, meter="hendecasyllable")
        # replace punctuation with spaces
        line = original_line.translate(self.punctuation_substitutions)
        # conservative i to j
        line = self.transform_i_to_j(line)
        working_line = self.elide_all(line)
        working_line = self.accent_by_position(working_line)
        syllables = self.syllabifier.syllabify(working_line)
        if optional_transform:
            working_line = self.transform_i_to_j_optional(line)
            working_line = self.elide_all(working_line)
            working_line = self.accent_by_position(working_line)
            syllables = self.syllabifier.syllabify(working_line)
            verse.scansion_notes += [self.constants.NOTE_MAP["optional i to j"]]
        verse.working_line = working_line
        verse.syllable_count = self.syllabifier.get_syllable_count(syllables)
        verse.syllables = syllables
        # identify some obvious and probably choices based on number of syllables
        if verse.syllable_count > 11:
            verse.valid = False
            verse.scansion_notes += [self.constants.NOTE_MAP["> 11"]]
            return verse
        if verse.syllable_count < 11:
            verse.valid = False
            verse.scansion_notes += [self.constants.NOTE_MAP["< 11"]]
            return verse

        stresses = self.flag_dipthongs(syllables)
        syllables_wspaces = string_utils.to_syllables_with_trailing_spaces(
            working_line, syllables
        )
        offset_map = self.calc_offset(syllables_wspaces)
        for idx, syl in enumerate(syllables):
            for accented in self.constants.ACCENTED_VOWELS:
                if accented in syl:
                    stresses.append(idx)
        # second to last syllable is always long
        stresses.append(verse.syllable_count - 2)

        verse.scansion = self.produce_scansion(stresses, syllables_wspaces, offset_map)
        if len(
            string_utils.stress_positions(self.constants.STRESSED, verse.scansion)
        ) != len(set(stresses)):
            verse.valid = False
            verse.scansion_notes += [self.constants.NOTE_MAP["invalid syllables"]]
            return verse

        if self.metrical_validator.is_valid_hendecasyllables(verse.scansion):
            verse.scansion_notes += [self.constants.NOTE_MAP["positionally"]]
            return self.assign_candidate(verse, verse.scansion)

        smoothed = self.correct_invalid_start(verse.scansion)

        if distance(verse.scansion, smoothed) > 0:
            verse.scansion_notes += [self.constants.NOTE_MAP["invalid start"]]
            verse.scansion = smoothed
            stresses += string_utils.differences(verse.scansion, smoothed)

        if self.metrical_validator.is_valid_hendecasyllables(verse.scansion):
            return self.assign_candidate(verse, verse.scansion)

        smoothed = self.correct_antepenult_chain(verse.scansion)

        if distance(verse.scansion, smoothed) > 0:
            verse.scansion_notes += [self.constants.NOTE_MAP["antepenult chain"]]
            verse.scansion = smoothed
            stresses += string_utils.differences(verse.scansion, smoothed)

        if self.metrical_validator.is_valid_hendecasyllables(verse.scansion):
            return self.assign_candidate(verse, verse.scansion)

        candidates = self.metrical_validator.closest_hendecasyllable_patterns(
            verse.scansion
        )
        if candidates is not None:
            if (
                len(candidates) == 1
                and len(verse.scansion.replace(" ", "")) == len(candidates[0])
                and len(string_utils.differences(verse.scansion, candidates[0])) == 1
            ):
                tmp_scansion = self.produce_scansion(
                    string_utils.differences(verse.scansion, candidates[0]),
                    syllables_wspaces,
                    offset_map,
                )
                if self.metrical_validator.is_valid_hendecasyllables(tmp_scansion):
                    verse.scansion_notes += [self.constants.NOTE_MAP["closest match"]]
                    return self.assign_candidate(verse, tmp_scansion)

        # if the line doesn't scan "as is", if may scan if the optional i to j transformations
        # are made, so here we set them and try again.
        if self.optional_transform and not verse.valid:
            return self.scan(original_line, optional_transform=True)

        verse.accented = self.formatter.merge_line_scansion(
            verse.original, verse.scansion
        )
        return verse

    def correct_invalid_start(self, scansion: str) -> str:
        """
        The third syllable of a hendecasyllabic line is long, so we will convert it.

        :param scansion: scansion string
        :return: scansion string with corrected start

        >>> print(HendecasyllableScanner().correct_invalid_start(
        ... "- U U  U U  - U   -  U - U").strip())
        - U -  U U  - U   -  U - U
        """
        mark_list = string_utils.mark_list(scansion)
        vals = list(scansion.replace(" ", ""))
        corrected = vals[:2] + [self.constants.STRESSED] + vals[3:]
        new_line = list(" " * len(scansion))
        for idx, car in enumerate(corrected):
            new_line[mark_list[idx]] = car
        return "".join(new_line)

    def correct_antepenult_chain(self, scansion: str) -> str:
        """
        For hendecasyllables the last three feet of the verse are predictable
        and do not regularly allow substitutions.

        :param scansion: scansion line thus far
        :return: corrected line of scansion

        >>> print(HendecasyllableScanner().correct_antepenult_chain(
        ... "-U -UU UU UU UX").strip())
        -U -UU -U -U -X
        """
        mark_list = string_utils.mark_list(scansion)
        vals = list(scansion.replace(" ", ""))
        new_vals = (
            vals[: len(vals) - 6]
            + [
                self.constants.TROCHEE
                + self.constants.TROCHEE
                + self.constants.STRESSED
            ]
            + vals[-1:]
        )
        corrected = "".join(new_vals)
        new_line = list(" " * len(scansion))
        for idx, car in enumerate(corrected):
            new_line[mark_list[idx]] = car
        return "".join(new_line)
