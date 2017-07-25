"""Utility class for producing a scansion pattern for a Latin hexameter.
Given a line of hexameter the scan method:
1. Removes punctuation preserving spaces
2. Performs a conservative i to j transformation
3. Performs elisions
4. Accents vowels by position
5. Breaks the line into a list of syllables by calling a Syllabifier class which may be injected
 into this classes constructor
6.  A series of transformation and checks are performed and for each one performed successfully a
 note is added to the scansion_notes list so that end users may view the provenance of a scansion.

Because hexameters have strict rules on the position and quantity of stressed and unstressed
syllables, we can often infer the many stress qualities of the syllables, given a valid hexameter.
If the Latin hexameter provided is not accented with macrons, then a best guess is made.
For the scansion produced, the stress of a dipthong is indicated in the second of the two vowel
positions; for the accented line produced, the dipthong stress is not indicated with any macronized
vowels.
"""

import re
from collections import defaultdict

from Levenshtein import distance

from cltk.prosody.latin.Hexameter import Hexameter
from cltk.prosody.latin.MetricalValidator import MetricalValidator
from cltk.prosody.latin.ScansionConstants import ScansionConstants
from cltk.prosody.latin.ScansionFormatter import ScansionFormatter
from cltk.prosody.latin.Syllabifier import Syllabifier
import cltk.prosody.latin.StringUtils as StringUtils

__author__ = ['Todd Cook <todd.g.cook@gmail.com>']
__license__ = 'MIT License'


class HexameterScanner:
    """The scansion symbols used can be configured by passing a suitable constants class to
    the constructor."""

    def __init__(self, constants=ScansionConstants(), syllabifier=Syllabifier()):
        self.constants = constants
        self.remove_punct_map = StringUtils.remove_punctuation_dict()
        self.punctuation_substitutions = StringUtils.punctuation_for_spaces_dict()
        self.metrical_validator = MetricalValidator(constants)
        self.formatter = ScansionFormatter(constants)
        self.syllabifier = syllabifier
        self.inverted_amphibrach_re = re.compile(
            r"{}\s*{}\s*{}".format(self.constants.STRESSED,
                                   self.constants.UNSTRESSED,
                                   self.constants.STRESSED))
        self.syllable_matcher = re.compile(r"[{}]".format(self.constants.VOWELS +
                                                     self.constants.ACCENTED_VOWELS +
                                                     self.constants.LIQUIDS +
                                                     self.constants.MUTES))

    def transform_i_to_j(self, line: str) -> str:
        """Transform instances of consonantal i to j
        :param line:
        :return:

        >>> print(HexameterScanner().transform_i_to_j("iactātus"))
        jactātus
        >>> print(HexameterScanner().transform_i_to_j("bracchia"))
        bracchia
        """

        words = line.split(" ")
        space_list = StringUtils.space_list(line)
        corrected_words = []
        for word in words:
            found = False
            for prefix in self.constants.PREFIXES:
                if word.startswith(prefix) and word != prefix:
                    corrected_words.append(self.syllabifier.convert_consonantal_i(prefix))
                    corrected_words.append(
                        self.syllabifier.convert_consonantal_i(word[len(prefix):]))
                    found = True
                    break
            if not found:
                corrected_words.append(self.syllabifier.convert_consonantal_i(word))
        new_line = StringUtils.join_syllables_spaces(corrected_words, space_list)
        char_list = StringUtils.overwrite(list(new_line),
                              r"\b[iī][{}]".format(
                                  self.constants.VOWELS + self.constants.ACCENTED_VOWELS),
                              "j")
        char_list = StringUtils.overwrite(char_list,
                              r"\b[I][{}]".format(self.constants.VOWELS_WO_I),
                              "J")
        char_list = StringUtils.overwrite(char_list, r"[{}][i][{}]".format(
            self.constants.VOWELS_WO_I, self.constants.VOWELS),
                              "j", 1)
        return "".join(char_list)

    def transform_i_to_j_optional(self, line: str) -> str:
        """Sometimes for the demands of meter a more permissive i to j transformation is warranted.
        :param line:
        :return:

        >>> print(HexameterScanner().transform_i_to_j_optional("Italiam"))
        Italjam
        >>> print(HexameterScanner().transform_i_to_j_optional("Lāvīniaque"))
        Lāvīnjaque
        >>> print(HexameterScanner().transform_i_to_j_optional("omnium"))
        omnjum
        """

        words = line.split(" ")
        space_list = StringUtils.space_list(line)
        corrected_words = []
        for word in words:
            found = False
            for prefix in self.constants.PREFIXES:
                if word.startswith(prefix) and word != prefix:
                    corrected_words.append(self.syllabifier.convert_consonantal_i(prefix))
                    corrected_words.append(
                        self.syllabifier.convert_consonantal_i(word[len(prefix):]))
                    found = True
                    break
            if not found:
                corrected_words.append(self.syllabifier.convert_consonantal_i(word))
        new_line = StringUtils.join_syllables_spaces(corrected_words, space_list)
        #  the following two may be tunable and subject to improvement
        char_list = StringUtils.overwrite(list(new_line),
                               "[bcdfgjkmpqrstvwxzBCDFGHJKMPQRSTVWXZ][i][{}]".format(
                                   self.constants.VOWELS_WO_I),
                               "j", 1)
        char_list = StringUtils.overwrite(char_list,
                              "[{}][iI][{}]".format(self.constants.LIQUIDS,
                                                   self.constants.VOWELS_WO_I),
                              "j", 1)
        return "".join(char_list)

    def accent_by_position(self, verse: str) -> str:
        """:param verse: a line of unaccented hexameter verse
        :return: the same line with vowels accented by position

        >>> print(HexameterScanner().accent_by_position(
        ... "Arma virumque cano, Troiae qui primus ab oris").lstrip())
        Ārma virūmque canō  Trojae quī primus ab oris
        """
        line = verse.translate(self.punctuation_substitutions)
        line = self.transform_i_to_j(line)
        marks = list(line)
        # Vowels followed by 2 consonants
        # The digraphs ch, ph, th, qu and sometimes gu and su count as single consonants.
        # see http://people.virginia.edu/~jdk3t/epicintrog/scansion.htm
        marks = StringUtils.overwrite(marks, "[{}][{}][{}]".format(
                                self.constants.VOWELS,
                                self.constants.CONSONANTS,
                                self.constants.CONSONANTS_WO_H),
                                      self.constants.STRESSED)
        # one space (or more for 'dropped' punctuation may intervene)
        marks = StringUtils.overwrite(marks,
                            r"[{}][{}]\s*[{}]".format(
                                self.constants.VOWELS,
                                self.constants.CONSONANTS,
                                self.constants.CONSONANTS_WO_H),
                                      self.constants.STRESSED)
        # ... if both consonants are in the next word, the vowel may be long
        # .... but it could be short if the vowel is not on the thesis/emphatic part of the foot
        # ... see Gildersleeve and Lodge p.446
        marks = StringUtils.overwrite(marks,
                            r"[{}]\s*[{}][{}]".format(
                                self.constants.VOWELS,
                                self.constants.CONSONANTS,
                                self.constants.CONSONANTS_WO_H),
                                      self.constants.STRESSED)
        #  x is considered as two letters
        marks = StringUtils.overwrite(marks,
                            "[{}][xX]".format(self.constants.VOWELS),
                                      self.constants.STRESSED)
        #  z is considered as two letters
        marks = StringUtils.overwrite(marks,
                            r"[{}][zZ]".format(self.constants.VOWELS),
                                      self.constants.STRESSED)
        original_verse = list(line)
        for idx, word in enumerate(original_verse):
            if marks[idx] == self.constants.STRESSED:
                original_verse[idx] = self.constants.VOWELS_TO_ACCENTS[original_verse[idx]]
        return "".join(original_verse)

    def elide_all(self, line: str) ->str:
        """Given a string of space separated syllables, erase with spaces the syllable portions
        that would disappear according to the rules of elision."""
        marks = list(line.translate(self.remove_punct_map))
        all_vowels = self.constants.VOWELS + self.constants.ACCENTED_VOWELS
        tmp = "".join(marks)
        # Elision rules are compound but not cummulative: we place all elision edits into a list
        #  of candidates, and then merge, taking the least of each section of the line.
        candidates = [tmp, self.elide(tmp, r"[{}][{}]\s+[{}]".format(self.constants.CONSONANTS,
                                                                     all_vowels, all_vowels), 1, 1),
                      self.elide(tmp,
                                 r"[{}][{}]\s+[hH]".format(self.constants.CONSONANTS, all_vowels),
                                 1, 1), self.elide(tmp, r"[aāuū]m\s+[{}]".format(all_vowels), 2),
                      self.elide(tmp, r"ae\s+[{}]".format(all_vowels), 2),
                      self.elide(tmp, r"[{}]\s+[{}]".format(all_vowels, all_vowels), 1),
                      self.elide(tmp, r"[uū]m\s+h", 2)]
        results = StringUtils.merge_elisions(candidates)
        return results

    # pylint: disable=line-too-long
    def scan(self, original_line: str, optional_transform: bool = False,
             dactyl_smoothing: bool = False) -> Hexameter:
        """Scan a line of Latin hexameter and produce a scansion pattern, and other data.
        >>> scanner = HexameterScanner()
        >>> print(scanner.scan("impulerit. Tantaene animis caelestibus irae?"))
        Hexameter( original='impulerit. Tantaene animis caelestibus irae?', scansion='-  U U -    -   -   U U -    - -  U U  -  - ', valid=True, syllable_count=15, accented='īmpulerīt. Tāntaene animīs caelēstibus īrae?', scansion_notes=['Valid by positional stresses.'], syllables = ['īm, pu, le, rīt, Tān, taen, a, ni, mīs, cae, lēs, ti, bus, i, rae'])
        >>> # Note: possible doctest quirk with leading whitespace; so we strip responses:
        >>> print(scanner.scan(
        ... "Arma virumque cano, Troiae qui prīmus ab ōrīs").scansion.strip())
        -  U  U -   U  U -    -  -   -   - U  U  - -
        >>> print(scanner.scan(
        ... "Ītaliam, fāto profugus, Lāvīniaque vēnit").scansion.strip())
        - -  -    - -   U U -    - -  U  U  - U
        >>> print(HexameterScanner().scan(
        ... "lītora, multum ille et terrīs iactātus et alto").scansion.strip())
        - U U   -     -    -   -  -   -  - U  U  -  U
        >>> print(HexameterScanner().scan(
        ... "vī superum saevae memorem Iūnōnis ob īram;").scansion.strip())
        -  U U -    -  -  U U -   - - U  U  - U
        >>> # handle multiple elisions
        >>> print(scanner.scan(
        ... "monstrum horrendum, informe, ingens, cui lumen ademptum"
        ... ).scansion.strip())
        -        -  -      -  -     -  -      -  - U  U -   U
        >>> # if we have 17 syllables, create a chain of all dactyls
        >>> print(scanner.scan("quadrupedante putrem sonitu quatit ungula campum"
        ... ).scansion.strip())
        -  U U -  U  U  -   U U -   U U  -  U U  -  U
        >>> print(HexameterScanner().scan(
        ... "illi inter sese multa vi bracchia tollunt").scansion.strip())
        -    -  -   - -  -  -  -   -   UU  -  -
        >>> print( HexameterScanner().scan(
        ... "dat latus; insequitur cumulo praeruptus aquae mons").scansion.strip())
        -   U U   -  U  U -   U U -    - -  U  U   -  -
        >>> print(HexameterScanner().scan(
        ... "Non quivis videt inmodulata poëmata iudex").scansion.strip())
        -    - -   U U  -  U U - U  U- U U  - -
        >>> print( HexameterScanner().scan(
        ... "certabant urbem Romam Remoramne vocarent").scansion.strip())
        -  - -   -  -   - -   U U -  U  U - -
        >>> # advanced smoothing is available via keyword flags
        >>> print(HexameterScanner().scan(
        ... "his verbis: 'o gnata, tibi sunt ante ferendae",
        ... dactyl_smoothing=True).scansion.strip() )
        -   -  -    -   - U   U -  -   -  U  U -   -

        """
        hexameter = Hexameter(original_line)
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
            hexameter.scansion_notes += [self.constants.NOTE_MAP["optional i to j"]]
        hexameter.working_line = working_line
        hexameter.syllable_count = len(syllables)
        hexameter.syllables = syllables
        stresses = self.flag_dipthongs(syllables)
        syllables_wspaces = StringUtils.to_syllables_with_trailing_spaces(working_line, syllables)
        offset_map = self.calc_offset(syllables_wspaces)
        for idx, syl in enumerate(syllables):
            for accented in self.constants.ACCENTED_VOWELS:
                if accented in syl:
                    stresses.append(idx)
        # first syllable is always long
        stresses.append(0)
        # second to last syllable is always long
        stresses.append(hexameter.syllable_count - 2)

        def validate(scansion: str) ->bool:
            """Helper closure for validation."""
            if self.metrical_validator.is_valid_hexameter(scansion):
                hexameter.scansion = scansion
                hexameter.valid = True
                hexameter.accented = self.formatter.merge_line_scansion(
                    hexameter.original, hexameter.scansion)
                return True
            return False

        hexameter.scansion = self.produce_scansion(stresses,
                                                    syllables_wspaces, offset_map)
        if len(StringUtils.stress_positions(self.constants.STRESSED, hexameter.scansion)) != \
                len(set(stresses)):
            hexameter.valid = False
            hexameter.scansion_notes += [self.constants.NOTE_MAP["invalid syllables"]]
            return hexameter

        if validate(hexameter.scansion):
            hexameter.scansion_notes += [self.constants.NOTE_MAP["positionally"]]
            return hexameter

        smoothed = self.correct_inverted_amphibrachs(hexameter.scansion)

        if distance(hexameter.scansion, smoothed) > 0:
            hexameter.scansion_notes += [self.constants.NOTE_MAP["inverted"]]
            hexameter.scansion = smoothed
            stresses += StringUtils.differences(hexameter.scansion, smoothed)

        if validate(hexameter.scansion):
            return hexameter

        smoothed = self.correct_invalid_start(hexameter.scansion)

        if distance(hexameter.scansion, smoothed) > 0:
            hexameter.scansion_notes += [self.constants.NOTE_MAP["invalid start"]]
            hexameter.scansion = smoothed
            stresses += StringUtils.differences(hexameter.scansion, smoothed)

        if validate(hexameter.scansion):
            return hexameter

        smoothed = self.correct_invalid_fifth_foot(hexameter.scansion)

        if distance(hexameter.scansion, smoothed) > 0:
            hexameter.scansion_notes += [self.constants.NOTE_MAP["invalid 5th"]]
            hexameter.scansion = smoothed
            stresses += StringUtils.differences(hexameter.scansion, smoothed)

        if validate(hexameter.scansion):
            return hexameter

        feet = self.metrical_validator.hexameter_feet(hexameter.scansion.replace(" ", ""))
        if feet:
            #  Normal good citizens are unwelcome in the house of hexameter
            invalid_feet_in_hexameter = [self.constants.IAMB, self.constants.TROCHEE]
            current_foot = 0
            ending = feet.pop()  # don't process the ending, a possible trochee, add it back after
            scanned_line = ""
            for foot in feet:
                if foot.replace(" ", "") in invalid_feet_in_hexameter:
                    scanned_line = self.invalid_foot_to_spondee(feet, foot, current_foot)
                    scanned_line = scanned_line + ending
                current_foot += 1
            smoothed = self.produce_scansion(stresses +
                                                 StringUtils.stress_positions(
                                                     self.constants.STRESSED, scanned_line),
                                                 syllables_wspaces, offset_map)
            if validate(smoothed):
                hexameter.scansion_notes += [self.constants.NOTE_MAP["invalid foot"]]
                return hexameter

        # need to do this again, since the scansion has changed
        smoothed = self.correct_inverted_amphibrachs(hexameter.scansion)

        if distance(hexameter.scansion, smoothed) > 0:
            hexameter.scansion_notes += [self.constants.NOTE_MAP["inverted"]]
            hexameter.scansion = smoothed
            stresses += StringUtils.differences(hexameter.scansion, smoothed)

        if validate(hexameter.scansion):
            return hexameter

        candidates = self.metrical_validator.closest_hexameter_patterns(hexameter.scansion)
        if candidates is not None:
            if len(candidates) == 1 \
                    and len(hexameter.scansion.replace(" ", "")) == len(candidates[0]) \
                    and len(StringUtils.differences(hexameter.scansion, candidates[0])) == 1:
                tmp_scansion = self.produce_scansion(
                    StringUtils.differences(hexameter.scansion, candidates[0]),
                                                     syllables_wspaces, offset_map)
                if validate(tmp_scansion):
                    hexameter.scansion = tmp_scansion
                    hexameter.scansion_notes += [self.constants.NOTE_MAP["closest match"]]
                    return hexameter

        #  identify some obvious and probably choices based on number of syllables
        if hexameter.syllable_count == 17:  # produce all dactyls
            candidate = self.produce_scansion(
                self.metrical_validator.hexameter_known_stresses(),
                syllables_wspaces, offset_map)
            hexameter.scansion_notes += [self.constants.NOTE_MAP["17"]]
            if validate(candidate):
                return hexameter
        if hexameter.syllable_count == 12:  # create all spondee hexameter
            if validate(self.produce_scansion(list(range(12)), syllables_wspaces, offset_map)):
                hexameter.scansion_notes += [self.constants.NOTE_MAP["12"]]
                return hexameter
        if hexameter.syllable_count < 12:
            hexameter.valid = False
            hexameter.scansion_notes += [self.constants.NOTE_MAP["< 12"]]
            return hexameter
        if hexameter.syllable_count == 13:  # create spondee hexameter with a dactyl at 5th foot
            known_unaccents = [9, 10, 12]
            if set(known_unaccents) - set(stresses) != len(known_unaccents):
                hexameter.scansion = self.produce_scansion([x for x in range(13)
                                                   if x not in known_unaccents],
                                                           syllables_wspaces, offset_map)
                hexameter.scansion_notes += [self.constants.NOTE_MAP["5th dactyl"]]
                if validate(hexameter.scansion):
                    return hexameter
        if hexameter.syllable_count > 17:
            hexameter.valid = False
            hexameter.scansion_notes += [self.constants.NOTE_MAP["> 17"]]
            return hexameter

        # need to do this again, since the scansion has changed
        smoothed = self.correct_inverted_amphibrachs(smoothed)
        if validate(smoothed):
            hexameter.scansion = smoothed
            hexameter.scansion_notes += [self.constants.NOTE_MAP["inverted"]]
            return hexameter

        if dactyl_smoothing:
            smoothed = self.correct_dactyl_chain(smoothed)
            if distance(hexameter.scansion, smoothed) > 0:
                hexameter.scansion_notes += [self.constants.NOTE_MAP["dactyl smoothing"]]
                hexameter.scansion = smoothed
            if validate(hexameter.scansion):
                return hexameter

        # if the line doesn't scan "as is", if may scan if the optional i to j transformations
        # are made, so here we set them and try again.
        if not optional_transform and not hexameter.valid:
            return self.scan(original_line, optional_transform=True, dactyl_smoothing=True)

        return hexameter

    def calc_offset(self, syllables_spaces: list) ->dict:
        """Calculate a dictionary of accent positions from a list of syllables with spaces."""
        line = StringUtils.flatten(syllables_spaces)
        mydict = defaultdict(lambda: None)
        for idx, syl in enumerate(syllables_spaces):
            target_syllable = syllables_spaces[idx]
            skip_qu = StringUtils.starts_with_qu(target_syllable)
            matches = list(self.syllable_matcher.finditer(target_syllable))
            for position, possible in enumerate(matches):
                if skip_qu:
                    skip_qu = False
                    continue
                (start, end) = possible.span()
                if target_syllable[start:end] in \
                                self.constants.VOWELS + self.constants.ACCENTED_VOWELS:
                    part = line[:len("".join(syllables_spaces[:idx]))]
                    offset = len(part) + start
                    if line[offset] not in self.constants.VOWELS + self.constants.ACCENTED_VOWELS:
                        print("Problem at line %s offset %s" % (line, offset))
                    mydict[idx] = offset
        return mydict

    def produce_scansion(self, stresses: list, syllables_wspaces: list, offset_map: dict) ->str:
        """Create a scansion string that has stressed and unstressed syllable positions in locations
        that correspond with the original texts syllable vowels.
         :param stresses list of syllable positions
         :param syllables_wspaces list of syllables with spaces escaped for punctuation or elision
         :param offset_map dictionary of syllable positions, and an offset amount which is the
          number of spaces to skip in the original line before inserting the accent.
         """
        scansion = list(" " * len(StringUtils.flatten(syllables_wspaces)))
        unstresses = StringUtils.get_unstresses(stresses, len(syllables_wspaces))
        try:
            for idx in unstresses:
                location = offset_map[idx]
                if location is not None:
                    scansion[location] = self.constants.UNSTRESSED
            for idx in stresses:
                location = offset_map[idx]
                if location is not None:
                    scansion[location] = self.constants.STRESSED
        except Exception as e:
            print("problem with syllables; check syllabification %s %s" % (syllables_wspaces, e))
            pass
        return "".join(scansion)

    def flag_dipthongs(self, syllables: list) ->list:
        """Return a list of syllables that contain a dipthong"""
        long_positions = []
        for idx, syl in enumerate(syllables):
            for dipthong in self.constants.DIPTHONGS:
                if dipthong in syllables[idx]:
                    if not StringUtils.starts_with_qu(syllables[idx]):
                        long_positions.append(idx)
        return long_positions

    def elide(self, line: str, regexp: str, quantity: 'int' = 1, offset: 'int >=0 ' = 0) -> str:
        """Erase a section of a line, matching on a regex, pushing in a quantity of blank spaces,
        and jumping forward with an offset if necessary.
        If the elided vowel was strong, the vowel merged with takes on the stress.

        >>> print(HexameterScanner().elide("uvae avaritia", r"[e]\s*[a]"))
        uv   āvaritia
        >>> print(HexameterScanner().elide("mare avaritia", r"[e]\s*[a]"))
        mar  avaritia
        """
        matcher = re.compile(regexp)
        positions = matcher.finditer(line)
        new_line = line
        for match in positions:
            (start, end) = match.span()    # pylint: disable=unused-variable
            if (start > 0) and new_line[start - 1: start + 1] in self.constants.DIPTHONGS:
                vowel_to_coerce = new_line[end - 1]
                new_line = new_line[:(start - 1) + offset] + (" " * (quantity + 2)) +  \
                    self.constants.stress_accent_dict[vowel_to_coerce] + new_line[end:]
            else:
                new_line = new_line[:start + offset] +\
                           (" " * quantity) + new_line[start + quantity + offset:]
        return new_line

    def correct_invalid_start(self, scansion: str) -> str:
        """If a hexameter scansion starts with spondee, an unstressed syllable in the third
        position must actually be stressed, so we will convert it: - - | U    ->  - - | -
        And or if the starting pattern is spondee + trochee + stressed, then the unstressed
        trochee can be corrected: - - | - u | -   ->  - - | - -| -
        :param scansion:
        :return:
        >>> print(HexameterScanner().correct_invalid_start(
        ... " -   - U   U -  -  U U U U  U U  - -").strip())
        -   - -   - -  -  U U U U  U U  - -
        """
        new_line = scansion
        scansion_wo_spaces = scansion.replace(" ", "")
        if scansion_wo_spaces.startswith(self.constants.SPONDEE + self.constants.UNSTRESSED):
            # pylint: disable=unused-variable
            (start, end) = re.compile(self.constants.UNSTRESSED).search(new_line).span()
            new_line = new_line[:start] + self.constants.STRESSED + new_line[start + 1:]

        if new_line.replace(" ", "").startswith(self.constants.SPONDEE +
                                                self.constants.TROCHEE +
                                                self.constants.STRESSED):
            (start, end) = re.compile(self.constants.UNSTRESSED).search(new_line).span()
            new_line = new_line[:start] + self.constants.STRESSED + new_line[start + 1:]
        return new_line

    def correct_invalid_fifth_foot(self, scansion: str) -> str:
        """The 'inverted amphibrach': stressed_unstressed_stressed syllable pattern is invalid
               in hexameters, so here we coerce it to stressed when it occurs at the end of a line
               :param scansion:
               :return:
        >>> print(HexameterScanner().correct_invalid_fifth_foot(
        ... " -   - -   U U  -  U U U -  - U U U  - x").strip())
        -   - -   U U  -  U U U -  - - U U  - x
        """
        scansion_wo_spaces = scansion.replace(" ", "")[:-1] + self.constants.OPTIONAL_ENDING
        if scansion_wo_spaces.endswith(self.constants.DACTYL +
                                       self.constants.IAMB +
                                       self.constants.OPTIONAL_ENDING):
            matches = list(re.compile
                           (r"{}\s*{}\s*{}\s*{}\s*{}".format(
                               self.constants.STRESSED,
                               self.constants.UNSTRESSED,
                               self.constants.UNSTRESSED,
                               self.constants.UNSTRESSED,
                               self.constants.STRESSED)).finditer(scansion))
            (start, end) = matches[len(matches) - 1].span()  # pylint: disable=unused-variable
            unstressed_idx = scansion.index(self.constants.UNSTRESSED, start)
            new_line = scansion[:unstressed_idx] + self.constants.STRESSED \
                + scansion[unstressed_idx + 1:]
            return new_line
        return scansion

    def invalid_foot_to_spondee(self, feet: list, foot: str, idx: int) -> str:
        """In hexameters, a single foot that is a  unstressed_stressed syllable pattern is often
        just a double spondee, so here we coerce it to stressed
               :param idx:
               :param feet: list of string representations of meterical feet
               :param foot: the bad foot to correct
               :parm idx: the index of the foot to correct
               :return: corrected scansion

        # >>> print(HexameterScanner().invalid_foot_to_spondee(
        " ... -   - U   - U  -  U U U -  - U U U  - x").strip())
        # -   - -   U U  -  U U U -  - - U U  - x
        """
        new_foot = foot.replace(self.constants.UNSTRESSED, self.constants.STRESSED)
        feet[idx] = new_foot
        return "".join(feet)

    def correct_dactyl_chain(self, scansion: str) -> str:
        """Three or more unstressed accents in a row is a broken dactyl chain,
         best detected and processed backwards.
         Since this method takes a Procrustean approach to modifying the scansion pattern,
         it is not used by default in the scan method; however, it is available as an optional
         keyword parameter, and users looking to further automate the generation of scansion
         candidates should consider using this as a fall back.
        :param scansion: scansion with broken dactyl chain; inverted amphibrachs not allowed
        :return: corrected line of scansion

        >>> print(HexameterScanner().correct_dactyl_chain(
        ... "-   U U  -  - U U -  - - U U  - x").strip())
        -   - -  -  - U U -  - - U U  - x
        >>> print(HexameterScanner().correct_dactyl_chain(
        ... "-   U  U U  U -     -   -   -  -   U  U -   U").strip())
        -   -  - U  U -     -   -   -  -   U  U -   U
        """
        mark_list = StringUtils.mark_list(scansion)
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
            if one == self.constants.UNSTRESSED and \
                            two == self.constants.UNSTRESSED and \
                            three == self.constants.STRESSED:
                feet += [one]
                feet += [two]
                feet += [three]
                idx -= 3
                continue
            # Spondee foot is okay, no corrections
            if one == self.constants.STRESSED and \
                            two == self.constants.STRESSED:
                feet += [one]
                feet += [two]
                idx -= 2
                continue
            # handle "U U U" foot as "- U U"
            if one == self.constants.UNSTRESSED and \
                            two == self.constants.UNSTRESSED and \
                            three == self.constants.UNSTRESSED:
                feet += [one]
                feet += [two]
                feet += [self.constants.STRESSED]
                idx -= 3
                continue
            # handle "U U -" foot as "- -"
            if one == self.constants.STRESSED and \
                            two == self.constants.UNSTRESSED and \
                            three == self.constants.UNSTRESSED:
                feet += [self.constants.STRESSED]
                feet += [self.constants.STRESSED]
                idx -= 2
                continue
            # handle "-  U" foot as "- -"
            if one == self.constants.UNSTRESSED and \
                            two == self.constants.STRESSED:
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
        """The 'inverted amphibrach': stressed_unstressed_stressed syllable pattern is invalid
        in hexameters, so here we coerce it to stressed:  - U - -> - - -
        :param scansion:
        :return: a string with the corrected scansion pattern

        >>> print(HexameterScanner().correct_inverted_amphibrachs(
        ... " -   U -   - U  -  U U U U  - U  - x").strip())
        -   - -   - -  -  U U U U  - -  - x
        >>> print(HexameterScanner().correct_inverted_amphibrachs(
        ... " -   - -   U -  -  U U U U  U- - U  - x").strip())
        -   - -   - -  -  U U U U  U- - -  - x
        >>> print(HexameterScanner().correct_inverted_amphibrachs(
        ... "-  - -   -  -   U -   U U -  U  U - -").strip())
        -  - -   -  -   - -   U U -  U  U - -
        >>> print(HexameterScanner().correct_inverted_amphibrachs(
        ... "- UU-   U -   U -  -   U   U U   U-   U").strip())
        - UU-   - -   - -  -   U   U U   U-   U
        """
        new_line = scansion
        while list(self.inverted_amphibrach_re.finditer(new_line)):
            matches = list(self.inverted_amphibrach_re.finditer(new_line))
            for match in matches:
                (start, end) = match.span()  # pylint: disable=unused-variable
                unstressed_idx = new_line.index(self.constants.UNSTRESSED, start)
                new_line = new_line[:unstressed_idx] + \
                    self.constants.STRESSED + new_line[unstressed_idx + 1:]
        return new_line
