"""Latin language syllabifier.
Parses a latin word or a space separated list of words into a list of syllables.
Consonantal I is transformed into a J at the start of a word as necessary.
Tuned for poetry and verse, this class is tolerant of isolated single character consonants that
may appear due to elision."""

import copy
import re
import logging
from cltk.prosody.latin.ScansionConstants import ScansionConstants
import cltk.prosody.latin.StringUtils as StringUtils

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

__author__ = ['Todd Cook <todd.g.cook@gmail.com>']
__license__ = 'MIT License'


class Syllabifier:
    """Scansion constants can be modified and passed into the constructor if desired."""

    def __init__(self, constants=ScansionConstants()):
        self.constants = constants
        self.consonant_matcher = re.compile("[{}]".format(constants.CONSONANTS))
        self.vowel_matcher = re.compile(
            "[{}]".format(constants.VOWELS + constants.ACCENTED_VOWELS))
        self.consonantal_i_matcher = re.compile(
            r"\b[iIīĪ][{}]".format(constants.VOWELS + constants.ACCENTED_VOWELS))
        self.remove_punct_map = StringUtils.remove_punctuation_dict()
        self.kw_matcher = re.compile("[kK][w]")
        self.ACCEPTABLE_CHARS = constants.ACCENTED_VOWELS + constants.VOWELS + ' ' \
                                + constants.CONSONANTS

    def syllabify(self, words: str) -> list:
        """Parse a Latin word into a list of syllable strings.
        :param words: a string containing one latin word or many words separated by spaces.
        :return: list of string, each representing a syllable.

        >>> syllabifier = Syllabifier()
        >>> print(syllabifier.syllabify("libri"))
        ['li', 'bri']
        >>> print(syllabifier.syllabify("contra"))
        ['con', 'tra']
        >>> print(syllabifier.syllabify("iaculum"))
        ['ja', 'cu', 'lum']
        >>> print(syllabifier.syllabify("amo"))
        ['a', 'mo']
        >>> print(syllabifier.syllabify("bracchia"))
        ['brac', 'chi', 'a']
        >>> print(syllabifier.syllabify("deinde"))
        ['dein', 'de']
        >>> print(syllabifier.syllabify("certabant"))
        ['cer', 'ta', 'bant']
        >>> print(syllabifier.syllabify("aere"))
        ['ae', 're']
        >>> print(syllabifier.syllabify("adiungere"))
        ['ad', 'jun', 'ge', 're']
        >>> print(syllabifier.syllabify("mōns"))
        ['mōns']
        >>> print(syllabifier.syllabify("domus"))
        ['do', 'mus']
        >>> print(syllabifier.syllabify("lixa"))
        ['li', 'xa']
        >>> print(syllabifier.syllabify("asper"))
        ['as', 'per']
        >>> #  handle doubles
        >>> print(syllabifier.syllabify("siccus"))
        ['sic', 'cus']
        >>> # handle liquid + liquid
        >>> print(syllabifier.syllabify("almus"))
        ['al', 'mus']
        >>> # handle liquid + mute
        >>> print(syllabifier.syllabify("ambo"))
        ['am', 'bo']
        >>> print(syllabifier.syllabify("anguis"))
        ['an', 'guis']
        >>> print(syllabifier.syllabify("arbor"))
        ['ar', 'bor']
        >>> print(syllabifier.syllabify("pulcher"))
        ['pul', 'cher']
        >>> print(syllabifier.syllabify("ruptus"))
        ['ru', 'ptus']
        >>> print(syllabifier.syllabify("Bīthÿnus"))
        ['Bī', 'thÿ', 'nus']
        """
        cleaned = words.translate(self.remove_punct_map)
        cleaned = cleaned.replace("qu", "kw")
        cleaned = cleaned.replace("Qu", "Kw")
        items = cleaned.strip().split(" ")
        for char in cleaned:
            if not char in self.ACCEPTABLE_CHARS:
                LOG.error("Unsupported character found in %s " % cleaned)
                return items
        syllables: list = []
        for item in items:
            syllables += self._setup(item)
        for idx, syl in enumerate(syllables):
            if "kw" in syl:
                syl = syl.replace("kw", "qu")
                syllables[idx] = syl
            if "Kw" in syl:
                syl = syl.replace("Kw", "Qu")
                syllables[idx] = syl

        return StringUtils.remove_blank_spaces(syllables)

    def _setup(self, word) -> list:
        """Prepares a word for syllable processing.

        If the word starts with a prefix, process it separately.
        """
        if len(word) == 1:
            return [word]
        for prefix in self.constants.PREFIXES:
            if word.startswith(prefix):
                (first, rest) = StringUtils.split_on(word, prefix)
                if self._contains_vowels(rest):
                    return StringUtils.remove_blank_spaces(
                        self._process(first) + self._process(rest))
                # a word like pror can happen from ellision
                return StringUtils.remove_blank_spaces(self._process(word))
        return StringUtils.remove_blank_spaces(self._process(word))

    def convert_consonantal_i(self, word) -> str:
        """Convert i to j when at the start of a word."""
        match = list(self.consonantal_i_matcher.finditer(word))
        if match:
            if word[0].isupper():
                return "J" + word[1:]
            return "j" + word[1:]
        return word

    def _process(self, word: str) -> list:
        """Process a word into a list of strings representing the syllables of the word. This
        method describes rules for consonant grouping behaviors and then iteratively applies those
        rules the list of letters that comprise the word, until all the letters are grouped into
        appropriate syllable groups."""
        #   if a blank arrives from splitting, just return an empty list
        if len(word.strip()) == 0:
            return []
        word = self.convert_consonantal_i(word)
        my_word = " " + word + " "
        letters = list(my_word)
        positions = []
        for dipth in self.constants.DIPTHONGS:
            if dipth in my_word:
                dipth_matcher = re.compile("{}".format(dipth))
                matches = dipth_matcher.finditer(my_word)
                for match in matches:
                    (start, end) = match.span()
                    positions.append(start)
        matches = self.kw_matcher.finditer(my_word)
        for match in matches:
            (start, end) = match.span()
            positions.append(start)
        letters = StringUtils.merge_next(letters, positions)
        letters = StringUtils.remove_blanks(letters)
        positions.clear()
        if not self._contains_vowels("".join(letters)):
            return ["".join(letters).strip()]  # occurs when only 'qu' appears by ellision
        positions = self._starting_consonants_only(letters)
        while len(positions) > 0:
            letters = StringUtils.move_consonant_right(letters, positions)
            letters = StringUtils.remove_blanks(letters)
            positions = self._starting_consonants_only(letters)
        positions = self._ending_consonants_only(letters)
        while len(positions) > 0:
            letters = StringUtils.move_consonant_left(letters, positions)
            letters = StringUtils.remove_blanks(letters)
            positions = self._ending_consonants_only(letters)
        positions = self._find_solo_consonant(letters)
        while len(positions) > 0:
            letters = self._move_consonant(letters, positions)
            letters = StringUtils.remove_blanks(letters)
            positions = self._find_solo_consonant(letters)
        positions = self._find_consonant_cluster(letters)
        while len(positions) > 0:
            letters = self._move_consonant(letters, positions)
            letters = StringUtils.remove_blanks(letters)
            positions = self._find_consonant_cluster(letters)
        return letters

    def _contains_consonants(self, letter_group: str) -> bool:
        """Check if a string contains consonants."""
        return self.consonant_matcher.search(letter_group) is not None

    def _contains_vowels(self, letter_group: str) -> bool:
        """Check if a string contains vowels."""
        return self.vowel_matcher.search(letter_group) is not None

    def _ends_with_vowel(self, letter_group: str) -> bool:
        """Check if a string ends with a vowel."""
        if len(letter_group) == 0:
            return False
        return self._contains_vowels(letter_group[-1])

    def _starts_with_vowel(self, letter_group: str) -> bool:
        """Check if a string starts with a vowel."""
        if len(letter_group) == 0:
            return False
        return self._contains_vowels(letter_group[0])

    def _starting_consonants_only(self, letters: list) -> list:
        """Return a list of starting consonant positions."""
        for idx, letter in enumerate(letters):
            if not self._contains_vowels(letter) and self._contains_consonants(letter):
                return [idx]
            if self._contains_vowels(letter):
                return []
            if self._contains_vowels(letter) and self._contains_consonants(letter):
                return []
        return []

    def _ending_consonants_only(self, letters: list) -> list:
        """Return a list of positions for ending consonants."""
        reversed_letters = list(reversed(letters))
        length = len(letters)
        for idx, letter in enumerate(reversed_letters):
            if not self._contains_vowels(letter) and self._contains_consonants(letter):
                return [(length - idx) - 1]
            if self._contains_vowels(letter):
                return []
            if self._contains_vowels(letter) and self._contains_consonants(letter):
                return []
        return []

    def _find_solo_consonant(self, letters: list) -> list:
        """Find the positions of any solo consonants that are not yet paired with a vowel."""
        solos = []
        for idx, letter in enumerate(letters):
            if len(letter) == 1 and self._contains_consonants(letter):
                solos.append(idx)
        return solos

    def _find_consonant_cluster(self, letters: list) -> list:
        """Find clusters of consonants that do not contain a vowel."""
        for idx, letter_group in enumerate(letters):
            if self._contains_consonants(letter_group) and not self._contains_vowels(letter_group):
                return [idx]
        return []

    def _move_consonant(self, letters: list, positions: list) -> list:
        """Given a list of consonant positions, move the consonants according to certain
        consonant syllable behavioral rules for gathering and grouping."""
        for pos in positions:
            previous_letter = letters[pos - 1]
            consonant = letters[pos]
            next_letter = letters[pos + 1]
            if self._contains_vowels(next_letter) and self._starts_with_vowel(next_letter):
                return StringUtils.move_consonant_right(letters, [pos])
            if self._contains_vowels(previous_letter) and self._ends_with_vowel(
                    previous_letter) and len(previous_letter) == 1:
                return StringUtils.move_consonant_left(letters, [pos])
            if previous_letter + consonant in self.constants.ASPIRATES:
                return StringUtils.move_consonant_left(letters, [pos])
            if consonant + next_letter in self.constants.ASPIRATES:
                return StringUtils.move_consonant_right(letters, [pos])
            if next_letter[0] == consonant:
                return StringUtils.move_consonant_left(letters, [pos])
            if consonant in self.constants.MUTES and next_letter[0] in self.constants.LIQUIDS:
                return StringUtils.move_consonant_right(letters, [pos])
            if consonant in ['k', 'K'] and next_letter[0] in ['w', 'W']:
                return StringUtils.move_consonant_right(letters, [pos])
            if self._contains_consonants(next_letter[0]) and self._starts_with_vowel(
                    previous_letter[-1]):
                return StringUtils.move_consonant_left(letters, [pos])
            # fall through case
            if self._contains_consonants(next_letter[0]):
                return StringUtils.move_consonant_right(letters, [pos])
        return letters

    def get_syllable_count(self, syllables: list) -> int:
        """Counts the number of syllable groups that would occur after ellision.

        Often we will want preserve the position and separation of syllables so that they
        can be used to reconstitute a line, and apply stresses to the original word positions.
        However, we also want to be able to count the number of syllables accurately.

        >>> syllabifier = Syllabifier()
        >>> print(syllabifier.get_syllable_count([
        ... 'Jām', 'tūm', 'c', 'au', 'sus', 'es', 'u', 'nus', 'I', 'ta', 'lo', 'rum']))
        11
        """
        tmp_syllables = copy.deepcopy(syllables)
        return len(StringUtils.remove_blank_spaces(
            StringUtils.move_consonant_right(tmp_syllables,
                                             self._find_solo_consonant(tmp_syllables))))
