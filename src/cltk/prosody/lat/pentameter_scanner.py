"""Utility class for producing a scansion pattern for a Latin pentameter.

Given a line of pentameter, the scan method performs a series of transformation and checks 
are performed, and for each one performed successfully, a note is added to the scansion_notes
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


class PentameterScanner(VerseScanner):
    """The scansion symbols used can be configured by passing a suitable constants class to
    the constructor."""

    def __init__(
        self,
        constants=ScansionConstants(),
        syllabifier=Syllabifier(),
        optional_transform: bool = False,
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
        self.optional_transform = optional_transform
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
        self.SPONDAIC_PENTAMETER = (
            self.constants.SPONDEE
            + self.constants.SPONDEE
            + self.constants.STRESSED
            + self.constants.DACTYL
            + self.constants.DACTYL
            + self.constants.OPTIONAL_ENDING
        )

        self.DACTYLIC_PENTAMETER = (
            self.constants.DACTYL
            + self.constants.DACTYL
            + self.constants.STRESSED
            + self.constants.DACTYL
            + self.constants.DACTYL
            + self.constants.OPTIONAL_ENDING
        )

    def scan(self, original_line: str, optional_transform: bool = False) -> Verse:
        """
        Scan a line of Latin pentameter and produce a scansion pattern, and other data.

        :param original_line: the original line of Latin verse
        :param optional_transform: whether or not to perform i to j transform for syllabification
        :return: a Verse object

        >>> scanner = PentameterScanner()
        >>> print(scanner.scan('ex hoc ingrato gaudia amore tibi.'))
        Verse(original='ex hoc ingrato gaudia amore tibi.', scansion='-   -  -   - -   - U  U - U  U U ', meter='pentameter', valid=True, syllable_count=12, accented='ēx hōc īngrātō gaudia amōre tibi.', scansion_notes=['Spondaic pentameter'], syllables = ['ēx', 'hoc', 'īn', 'gra', 'to', 'gau', 'di', 'a', 'mo', 're', 'ti', 'bi'])
        >>> print(scanner.scan(
        ... "in vento et rapida scribere oportet aqua.").scansion) # doctest: +NORMALIZE_WHITESPACE
        -   -    -   U U -    - U   U -  U  U  U
        """
        verse = Verse(original_line, meter="pentameter")
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
        if verse.syllable_count < 12:
            verse.valid = False
            verse.scansion_notes += [self.constants.NOTE_MAP["< 12p"]]
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
        # first syllable is always long in Pentameter
        stresses.append(0)
        # second to last syllable is always long
        stresses.append(verse.syllable_count - 2)

        verse.scansion = self.produce_scansion(stresses, syllables_wspaces, offset_map)
        if len(
            string_utils.stress_positions(self.constants.STRESSED, verse.scansion)
        ) != len(set(stresses)):
            verse.valid = False
            verse.scansion_notes += [self.constants.NOTE_MAP["invalid syllables"]]
            return verse

        if self.metrical_validator.is_valid_pentameter(verse.scansion):
            verse.scansion_notes += [self.constants.NOTE_MAP["positionally"]]
            return self.assign_candidate(verse, verse.scansion)

        # identify some obvious and probably choices based on number of syllables
        if verse.syllable_count == 12:  # produce spondees where possible
            candidate = self.make_spondaic(verse.scansion)
            verse.scansion_notes += [self.constants.NOTE_MAP["12p"]]
            return self.assign_candidate(verse, candidate)
        if verse.syllable_count == 14:  # produce spondees where possible
            candidate = self.make_dactyls(verse.scansion)
            verse.scansion_notes += [self.constants.NOTE_MAP["14p"]]
            return self.assign_candidate(verse, candidate)
        if verse.syllable_count > 14:
            verse.valid = False
            verse.scansion_notes += [self.constants.NOTE_MAP["> 14"]]
            return verse

        smoothed = self.correct_first_two_dactyls(verse.scansion)

        if distance(verse.scansion, smoothed) > 0:
            verse.scansion_notes += [self.constants.NOTE_MAP["invalid start"]]
            verse.scansion = smoothed
            stresses += string_utils.differences(verse.scansion, smoothed)

        if self.metrical_validator.is_valid_pentameter(verse.scansion):
            return self.assign_candidate(verse, verse.scansion)

        smoothed = self.correct_penultimate_dactyl_chain(verse.scansion)

        if distance(verse.scansion, smoothed) > 0:
            verse.scansion_notes += [
                self.constants.NOTE_MAP["penultimate dactyl chain"]
            ]
            verse.scansion = smoothed
            stresses += string_utils.differences(verse.scansion, smoothed)

        if self.metrical_validator.is_valid_pentameter(verse.scansion):
            return self.assign_candidate(verse, verse.scansion)

        candidates = self.metrical_validator.closest_pentameter_patterns(verse.scansion)
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

                if self.metrical_validator.is_valid_pentameter(tmp_scansion):
                    verse.scansion_notes += [self.constants.NOTE_MAP["closest match"]]
                    return self.assign_candidate(verse, tmp_scansion)

        # if the line doesn't scan "as is", it may scan if the optional i to j transformations
        # are made, so here we set them and try again.
        if self.optional_transform and not verse.valid:
            return self.scan(original_line, optional_transform=True)

        verse.accented = self.formatter.merge_line_scansion(
            verse.original, verse.scansion
        )
        return verse

    def make_spondaic(self, scansion: str) -> str:
        """
        If a pentameter line has 12 syllables, then it must start with double spondees.

        :param scansion: a string of scansion patterns
        :return: a scansion pattern string starting with two spondees

        >>> print(PentameterScanner().make_spondaic("U  U  U  U  U  U  U  U  U  U  U  U"))
        -  -  -  -  -  -  U  U  -  U  U  U
        """
        mark_list = string_utils.mark_list(scansion)
        vals = list(scansion.replace(" ", ""))
        new_vals = self.SPONDAIC_PENTAMETER[:-1] + vals[-1]
        corrected = "".join(new_vals)
        new_line = list(" " * len(scansion))
        for idx, car in enumerate(corrected):
            new_line[mark_list[idx]] = car
        return "".join(new_line)

    def make_dactyls(self, scansion: str) -> str:
        """
        If a pentameter line has 14 syllables, it starts and ends with double dactyls.

        :param scansion: a string of scansion patterns
        :return: a scansion pattern string starting and ending with double dactyls

        >>> print(PentameterScanner().make_dactyls("U  U  U  U  U  U  U  U  U  U  U  U  U  U"))
        -  U  U  -  U  U  -  -  U  U  -  U  U  U
        """
        mark_list = string_utils.mark_list(scansion)
        vals = list(scansion.replace(" ", ""))
        new_vals = self.DACTYLIC_PENTAMETER[:-1] + vals[-1]
        corrected = "".join(new_vals)
        new_line = list(" " * len(scansion))
        for idx, car in enumerate(corrected):
            new_line[mark_list[idx]] = car
        return "".join(new_line)

    def correct_penultimate_dactyl_chain(self, scansion: str) -> str:
        """
        For pentameter the last two feet of the verse are predictable dactyls,
        and do not regularly allow substitutions.

        :param scansion: scansion line thus far
        :return: corrected line of scansion

        >>> print(PentameterScanner().correct_penultimate_dactyl_chain(
        ... "U  U  U  U  U  U  U  U  U  U  U  U  U  U"))
        U  U  U  U  U  U  U  -  U  U  -  U  U  U
        """
        mark_list = string_utils.mark_list(scansion)
        vals = list(scansion.replace(" ", ""))
        n_vals = (
            vals[:-7] + [self.constants.DACTYL + self.constants.DACTYL] + [vals[-1]]
        )
        corrected = "".join(n_vals)
        new_line = list(" " * len(scansion))
        for idx, car in enumerate(corrected):
            new_line[mark_list[idx]] = car
        return "".join(new_line)
