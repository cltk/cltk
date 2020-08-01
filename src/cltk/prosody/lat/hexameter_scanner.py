"""Utility class for producing a scansion pattern for a Latin hexameter.

Given a line of hexameter, the scan method performs a series of transformation and checks
are performed and for each one performed successfully, a note is added to the scansion_notes
list so that end users may view the provenance of a scansion.

Because hexameters have strict rules on the position and quantity of stressed and unstressed
syllables, we can often infer the many stress qualities of the syllables, given a valid hexameter.
If the Latin hexameter provided is not accented with macrons, then a best guess is made.
For the scansion produced, the stress of a dipthong is indicated in the second of the two vowel
positions; for the accented line produced, the dipthong stress is not indicated with any macronized
vowels.
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


class HexameterScanner(VerseScanner):
    """The scansion symbols used can be configured by passing a suitable constants class to
    the constructor."""

    def __init__(
        self,
        constants=ScansionConstants(),
        syllabifier=Syllabifier(),
        optional_transform=False,
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
        self.optional_transform = optional_transform

    def scan(
        self,
        original_line: str,
        optional_transform: bool = False,
        dactyl_smoothing: bool = False,
    ) -> Verse:
        """
        Scan a line of Latin hexameter and produce a scansion pattern, and other data.

        :param original_line: the original line of Latin verse
        :param optional_transform: whether or not to perform i to j transform for syllabification
        :param dactyl_smoothing: whether or not to perform dactyl smoothing
        :return: a Verse object

        >>> scanner = HexameterScanner()

        >>> print(HexameterScanner().scan(
        ... "ēxiguām sedēm pariturae tērra negavit").scansion) # doctest: +NORMALIZE_WHITESPACE
        - -  -   - -   U U -  -  -  U  U - U
        >>> print(scanner.scan("impulerit. Tantaene animis caelestibus irae?"))
        Verse(original='impulerit. Tantaene animis caelestibus irae?', scansion='-  U U -    -   -   U U -    - -  U U  -  - ', meter='hexameter', valid=True, syllable_count=15, accented='īmpulerīt. Tāntaene animīs caelēstibus īrae?', scansion_notes=['Valid by positional stresses.'], syllables = ['īm', 'pu', 'le', 'rīt', 'Tān', 'taen', 'a', 'ni', 'mīs', 'cae', 'lēs', 'ti', 'bus', 'i', 'rae'])
        >>> print(scanner.scan(
        ... "Arma virumque cano, Troiae qui prīmus ab ōrīs").scansion) # doctest: +NORMALIZE_WHITESPACE
        -  U  U -   U  U -    -  -   -   - U  U  - -
        >>> # some hexameters need the optional transformations:
        >>> optional_transform_scanner = HexameterScanner(optional_transform=True)
        >>> print(optional_transform_scanner.scan(
        ... "Ītaliam, fāto profugus, Lāvīniaque vēnit").scansion) # doctest: +NORMALIZE_WHITESPACE
        - -  -    - -   U U -    - -  U  U  - U
        >>> print(HexameterScanner().scan(
        ... "lītora, multum ille et terrīs iactātus et alto").scansion) # doctest: +NORMALIZE_WHITESPACE
        - U U   -     -    -   -  -   -  - U  U  -  U
        >>> print(HexameterScanner().scan(
        ... "vī superum saevae memorem Iūnōnis ob īram;").scansion) # doctest: +NORMALIZE_WHITESPACE
        -  U U -    -  -  U U -   - - U  U  - U
        >>> # handle multiple elisions
        >>> print(scanner.scan("monstrum horrendum, informe, ingens, cui lumen ademptum").scansion) # doctest: +NORMALIZE_WHITESPACE
        -        -  -      -  -     -  -      -  - U  U -   U
        >>> # if we have 17 syllables, create a chain of all dactyls
        >>> print(scanner.scan("quadrupedante putrem sonitu quatit ungula campum"
        ... ).scansion) # doctest: +NORMALIZE_WHITESPACE
        -  U U -  U  U  -   U U -   U U  -  U U  -  U
        >>> # if we have 13 syllables exactly, we'll create a spondaic hexameter
        >>> print(HexameterScanner().scan(
        ... "illi inter sese multa vi bracchia tollunt").scansion)  # doctest: +NORMALIZE_WHITESPACE
        -    -  -   - -  -  -  -   -   UU  -  -
        >>> print(HexameterScanner().scan(
        ... "dat latus; insequitur cumulo praeruptus aquae mons").scansion) # doctest: +NORMALIZE_WHITESPACE
        -   U U   -  U  U -   U U -    - -  U  U   -  -
        >>> print(optional_transform_scanner.scan(
        ... "Non quivis videt inmodulata poëmata iudex").scansion) # doctest: +NORMALIZE_WHITESPACE
        -    - -   U U  -  U U - U  U- U U  - -
        >>> print(HexameterScanner().scan(
        ... "certabant urbem Romam Remoramne vocarent").scansion) # doctest: +NORMALIZE_WHITESPACE
        -  - -   -  -   - -   U U -  U  U - -
        >>> # advanced smoothing is available via keyword flags: dactyl_smoothing
        >>> # print(HexameterScanner().scan(
        #... "his verbis: 'o gnata, tibi sunt ante ferendae",
        #... dactyl_smoothing=True).scansion) # doctest: +NORMALIZE_WHITESPACE
        #-   -  -    -   - U   U -  -   -  U  U -   -
        """
        verse = Verse(original_line, meter="hexameter")
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
            verse.scansion_notes += [self.constants.NOTE_MAP["< 12"]]
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
        # first syllable is always long in hexameter
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

        if self.metrical_validator.is_valid_hexameter(verse.scansion):
            verse.scansion_notes += [self.constants.NOTE_MAP["positionally"]]
            return self.assign_candidate(verse, verse.scansion)

        # identify some obvious and probably choices based on number of syllables
        if verse.syllable_count == 17:  # produce all dactyls
            candidate = self.produce_scansion(
                self.metrical_validator.hexameter_known_stresses(),
                syllables_wspaces,
                offset_map,
            )
            verse.scansion_notes += [self.constants.NOTE_MAP["17"]]
            if self.metrical_validator.is_valid_hexameter(candidate):
                return self.assign_candidate(verse, candidate)
        if verse.syllable_count == 12:  # create all spondee hexameter
            candidate = self.produce_scansion(
                list(range(12)), syllables_wspaces, offset_map
            )
            if self.metrical_validator.is_valid_hexameter(verse.scansion):
                verse.scansion_notes += [self.constants.NOTE_MAP["12"]]
                return self.assign_candidate(verse, candidate)
        if (
            verse.syllable_count == 13
        ):  # create spondee hexameter with a dactyl at 5th foot
            known_unaccents = [9, 10]
            last_syllable_accented = False
            for vowel in self.constants.ACCENTED_VOWELS:
                if vowel in verse.syllables[12]:
                    last_syllable_accented = True
            if not last_syllable_accented:
                known_unaccents.append(12)
            if set(known_unaccents) - set(stresses) != len(known_unaccents):
                verse.scansion = self.produce_scansion(
                    [x for x in range(13) if x not in known_unaccents],
                    syllables_wspaces,
                    offset_map,
                )
                verse.scansion_notes += [self.constants.NOTE_MAP["5th dactyl"]]
                if self.metrical_validator.is_valid_hexameter(verse.scansion):
                    return self.assign_candidate(verse, verse.scansion)
        if verse.syllable_count > 17:
            verse.valid = False
            verse.scansion_notes += [self.constants.NOTE_MAP["> 17"]]
            return verse

        smoothed = self.correct_inverted_amphibrachs(verse.scansion)
        if distance(verse.scansion, smoothed) > 0:
            verse.scansion_notes += [self.constants.NOTE_MAP["inverted"]]
            verse.scansion = smoothed
            stresses += string_utils.differences(verse.scansion, smoothed)

        if self.metrical_validator.is_valid_hexameter(verse.scansion):
            return self.assign_candidate(verse, verse.scansion)

        smoothed = self.correct_first_two_dactyls(verse.scansion)
        if distance(verse.scansion, smoothed) > 0:
            verse.scansion_notes += [self.constants.NOTE_MAP["invalid start"]]
            verse.scansion = smoothed
            stresses += string_utils.differences(verse.scansion, smoothed)

        if self.metrical_validator.is_valid_hexameter(verse.scansion):
            return self.assign_candidate(verse, verse.scansion)

        smoothed = self.correct_invalid_fifth_foot(verse.scansion)
        if distance(verse.scansion, smoothed) > 0:
            verse.scansion_notes += [self.constants.NOTE_MAP["invalid 5th"]]
            verse.scansion = smoothed
            stresses += string_utils.differences(verse.scansion, smoothed)

        if self.metrical_validator.is_valid_hexameter(verse.scansion):
            return self.assign_candidate(verse, verse.scansion)

        feet = self.metrical_validator.hexameter_feet(verse.scansion.replace(" ", ""))
        if feet:
            #  Normal good citizens are unwelcome in the house of hexameter
            invalid_feet_in_hexameter = [self.constants.IAMB, self.constants.TROCHEE]
            current_foot = 0
            ending = (
                feet.pop()
            )  # don't process the ending, a possible trochee, add it back after
            scanned_line = ""
            for foot in feet:
                if foot.replace(" ", "") in invalid_feet_in_hexameter:
                    scanned_line = self.invalid_foot_to_spondee(
                        feet, foot, current_foot
                    )
                    scanned_line = scanned_line + ending
                current_foot += 1
            smoothed = self.produce_scansion(
                stresses
                + string_utils.stress_positions(self.constants.STRESSED, scanned_line),
                syllables_wspaces,
                offset_map,
            )

            if self.metrical_validator.is_valid_hexameter(smoothed):
                verse.scansion_notes += [self.constants.NOTE_MAP["invalid foot"]]
                return self.assign_candidate(verse, smoothed)

        # need to do this again, since the scansion has changed
        smoothed = self.correct_inverted_amphibrachs(verse.scansion)
        if distance(verse.scansion, smoothed) > 0:
            verse.scansion_notes += [self.constants.NOTE_MAP["inverted"]]
            verse.scansion = smoothed
            stresses += string_utils.differences(verse.scansion, smoothed)

        if self.metrical_validator.is_valid_hexameter(verse.scansion):
            return self.assign_candidate(verse, verse.scansion)

        candidates = self.metrical_validator.closest_hexameter_patterns(verse.scansion)
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
                if self.metrical_validator.is_valid_hexameter(tmp_scansion):
                    verse.scansion_notes += [self.constants.NOTE_MAP["closest match"]]
                    return self.assign_candidate(verse, tmp_scansion)

        # need to do this again, since the scansion has changed
        smoothed = self.correct_inverted_amphibrachs(smoothed)
        if self.metrical_validator.is_valid_hexameter(smoothed):
            verse.scansion_notes += [self.constants.NOTE_MAP["inverted"]]
            return self.assign_candidate(verse, smoothed)

        if dactyl_smoothing:
            smoothed = self.correct_dactyl_chain(smoothed)
            if distance(verse.scansion, smoothed) > 0:
                verse.scansion_notes += [self.constants.NOTE_MAP["dactyl smoothing"]]
                verse.scansion = smoothed
            if self.metrical_validator.is_valid_hexameter(verse.scansion):
                return self.assign_candidate(verse, verse.scansion)

        # if the line doesn't scan "as is", if may scan if the optional i to j transformations
        # are made, so here we set them and try again.
        if self.optional_transform and not verse.valid:
            return self.scan(
                original_line, optional_transform=True, dactyl_smoothing=True
            )
        return verse

    def correct_invalid_fifth_foot(self, scansion: str) -> str:
        """
        The 'inverted amphibrach': stressed_unstressed_stressed syllable pattern is invalid
        in hexameters, so here we coerce it to stressed when it occurs at the end of a line

        :param scansion: the scansion pattern
        :return corrected scansion: the corrected scansion pattern

        >>> print(HexameterScanner().correct_invalid_fifth_foot(
        ... " -   - -   U U  -  U U U -  - U U U  - x")) # doctest: +NORMALIZE_WHITESPACE
        -   - -   U U  -  U U U -  - - U U  - x
        """
        scansion_wo_spaces = (
            scansion.replace(" ", "")[:-1] + self.constants.OPTIONAL_ENDING
        )
        if scansion_wo_spaces.endswith(
            self.constants.DACTYL + self.constants.IAMB + self.constants.OPTIONAL_ENDING
        ):
            matches = list(
                re.compile(
                    r"{}\s*{}\s*{}\s*{}\s*{}".format(
                        self.constants.STRESSED,
                        self.constants.UNSTRESSED,
                        self.constants.UNSTRESSED,
                        self.constants.UNSTRESSED,
                        self.constants.STRESSED,
                    )
                ).finditer(scansion)
            )
            (start, end) = matches[len(matches) - 1].span()
            unstressed_idx = scansion.index(self.constants.UNSTRESSED, start)
            new_line = (
                scansion[:unstressed_idx]
                + self.constants.STRESSED
                + scansion[unstressed_idx + 1 :]
            )
            return new_line
        return scansion

    def invalid_foot_to_spondee(self, feet: list, foot: str, idx: int) -> str:
        """
        In hexameters, a single foot that is a  unstressed_stressed syllable pattern is often
        just a double spondee, so here we coerce it to stressed.

        :param feet: list of string representations of meterical feet
        :param foot: the bad foot to correct
        :param idx: the index of the foot to correct
        :return: corrected scansion

        >>> print(HexameterScanner().invalid_foot_to_spondee(
        ... ['-UU', '--', '-U', 'U-', '--', '-UU'],'-U', 2))  # doctest: +NORMALIZE_WHITESPACE
        -UU----U----UU
        """
        new_foot = foot.replace(self.constants.UNSTRESSED, self.constants.STRESSED)
        feet[idx] = new_foot
        return "".join(feet)

    def correct_dactyl_chain(self, scansion: str) -> str:
        """
        Three or more unstressed accents in a row is a broken dactyl chain, best detected and
        processed backwards.

        Since this method takes a Procrustean approach to modifying the scansion pattern,
        it is not used by default in the scan method; however, it is available as an optional
        keyword parameter, and users looking to further automate the generation of scansion
        candidates should consider using this as a fall back.

        :param scansion: scansion with broken dactyl chain; inverted amphibrachs not allowed
        :return: corrected line of scansion

        >>> print(HexameterScanner().correct_dactyl_chain(
        ... "-   U U  -  - U U -  - - U U  - x"))
        -   - -  -  - U U -  - - U U  - x
        >>> print(HexameterScanner().correct_dactyl_chain(
        ... "-   U  U U  U -     -   -   -  -   U  U -   U")) # doctest: +NORMALIZE_WHITESPACE
        -   -  - U  U -     -   -   -  -   U  U -   U
        """
        mark_list = string_utils.mark_list(scansion)
        vals = list(scansion.replace(" ", ""))
        #  ignore last two positions, save them
        feet = [vals.pop(), vals.pop()]
        length = len(vals)
        idx = length - 1
        while idx > 0:
            one = vals[idx]
            two = vals[idx - 1]
            if idx > 1:
                three = vals[idx - 2]
            else:
                three = ""
            # Dactyl foot is okay, no corrections
            if (
                one == self.constants.UNSTRESSED
                and two == self.constants.UNSTRESSED
                and three == self.constants.STRESSED
            ):
                feet += [one]
                feet += [two]
                feet += [three]
                idx -= 3
                continue
            # Spondee foot is okay, no corrections
            if one == self.constants.STRESSED and two == self.constants.STRESSED:
                feet += [one]
                feet += [two]
                idx -= 2
                continue
            # handle "U U U" foot as "- U U"
            if (
                one == self.constants.UNSTRESSED
                and two == self.constants.UNSTRESSED
                and three == self.constants.UNSTRESSED
            ):
                feet += [one]
                feet += [two]
                feet += [self.constants.STRESSED]
                idx -= 3
                continue
            # handle "U U -" foot as "- -"
            if (
                one == self.constants.STRESSED
                and two == self.constants.UNSTRESSED
                and three == self.constants.UNSTRESSED
            ):
                feet += [self.constants.STRESSED]
                feet += [self.constants.STRESSED]
                idx -= 2
                continue
            # handle "-  U" foot as "- -"
            if one == self.constants.UNSTRESSED and two == self.constants.STRESSED:
                feet += [self.constants.STRESSED]
                feet += [two]
                idx -= 2
                continue
        corrected = "".join(feet[::-1])
        new_line = list(" " * len(scansion))
        for idx, car in enumerate(corrected):
            new_line[mark_list[idx]] = car
        return "".join(new_line)

    def correct_inverted_amphibrachs(self, scansion: str) -> str:
        """
        The 'inverted amphibrach': stressed_unstressed_stressed syllable pattern is invalid
        in hexameters, so here we coerce it to stressed:  - U - -> - - -

        :param scansion: the scansion stress pattern
        :return: a string with the corrected scansion pattern

        >>> print(HexameterScanner().correct_inverted_amphibrachs(
        ... " -   U -   - U  -  U U U U  - U  - x")) # doctest: +NORMALIZE_WHITESPACE
        -   - -   - -  -  U U U U  - -  - x
        >>> print(HexameterScanner().correct_inverted_amphibrachs(
        ... " -   - -   U -  -  U U U U  U- - U  - x")) # doctest: +NORMALIZE_WHITESPACE
        -   - -   - -  -  U U U U  U- - -  - x
        >>> print(HexameterScanner().correct_inverted_amphibrachs(
        ... "-  - -   -  -   U -   U U -  U  U - -")) # doctest: +NORMALIZE_WHITESPACE
        -  - -   -  -   - -   U U -  U  U - -
        >>> print(HexameterScanner().correct_inverted_amphibrachs(
        ... "- UU-   U -   U -  -   U   U U   U-   U")) # doctest: +NORMALIZE_WHITESPACE
        - UU-   - -   - -  -   U   U U   U-   U
        """
        new_line = scansion
        while list(self.inverted_amphibrach_re.finditer(new_line)):
            matches = list(self.inverted_amphibrach_re.finditer(new_line))
            for match in matches:
                (start, end) = match.span()  # pylint: disable=unused-variable
                unstressed_idx = new_line.index(self.constants.UNSTRESSED, start)
                new_line = (
                    new_line[:unstressed_idx]
                    + self.constants.STRESSED
                    + new_line[unstressed_idx + 1 :]
                )
        return new_line
