"""
Given an Akkadian word, either normalized or as a list of syllables, return a list of syllables with the stressed
syllable surrounded by square brackets.
"""

#TODO: fails on: ['hammurabi', 'u', 'išmeānim']

from cltk.stem.akkadian.syllabifier import Syllabifier

__author__ = ['M. Willis Monroe <willismonroe@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

AKKADIAN = {
    'short_vowels': ['a', 'e', 'i', 'u'],
    'macron_vowels': ['ā', 'ē', 'ī', 'ū'],
    'circumflex_vowels': ['â', 'ê', 'î', 'û'],

    'consonants': ['b', 'd', 'g', 'ḫ', 'k', 'l', 'm',
                   'n', 'p', 'q', 'r', 's', 'ṣ', 'š',
                   't', 'ṭ', 'w', 'y', 'z', 'ʾ']
}


class StressFinder(object):
    """
    Returns list of syllables with stressed syllable in square brackets.
    """

    def __init__(self, language=AKKADIAN):
        self.language = language

    def _is_consonant(self, char):
        return char in self.language['consonants']

    def _is_vowel(self, char):
        return char in self.language['short_vowels'] + \
               self.language['macron_vowels'] + \
               self.language['circumflex_vowels']

    def _is_short_vowel(self, char):
        return char in self.language['short_vowels']

    def _is_macron_vowel(self, char):
        return char in self.language['macron_vowels']

    def _is_circumflex_vowel(self, char):
        return char in self.language['circumflex_vowels']

    def find_stress(self, word):
        """
        Find the stressed syllable in a word.
        The general logic follows Huehnergard 3rd edition (pgs. 3-4):
        (a) Light: ending in a short vowel: e.g., -a, -ba
        (b) Heavy: ending in a long vowel marked with a macron, or in a
        short vowel plus a consonant: e.g., -ā, -bā, -ak, -bak
        (c) Ultraheavy: ending in a long vowel marked with a circumflex,
        in any long vowel plus a consonant: e.g., -â, -bâ, -āk, -bāk, -âk, -bâk.
        (a) If the last syllable is ultraheavy, it bears the stress.
        (b) Otherwise, stress falls on the last non-final heavy or ultraheavy syllable.
        (c) Words that contain no non-final heavy or ultraheavy syllables have the
        stress fall on the first syllable.
        :param word: a string (or list) in Akkadian
        :return: a list of syllables with stressed syllable surrounded by "[]"
        """
        syllabifier = Syllabifier()

        if type(word) is str:
            word = syllabifier.syllabify(word)

        syllables_stress = []

        for i, syllable in enumerate(word):
            # Enumerate over the syllables and mark them for length
            # We check each type of length by looking at the length of the
            # syllable and verifying rules based on character length.

            # Ultraheavy:
            # -â, -bâ, -āk, -bāk, -âk, -bâk.
            if len(syllable) == 1:
                if self._is_circumflex_vowel(syllable):
                    syllables_stress.append((syllable, "Ultraheavy"))
                    continue
            elif len(syllable) == 2:
                if self._is_consonant(syllable[0]) and self._is_circumflex_vowel(syllable[1]):
                    syllables_stress.append((syllable, "Ultraheavy"))
                    continue
                if (self._is_macron_vowel(syllable[0]) or self._is_circumflex_vowel(syllable[0])) \
                        and self._is_consonant(syllable[1]):
                    syllables_stress.append((syllable, "Ultraheavy"))
                    continue
            elif len(syllable) == 3:
                if self._is_macron_vowel(syllable[1]) or self._is_circumflex_vowel(syllable[1]):
                    syllables_stress.append((syllable, "Ultraheavy"))
                    continue

            # Heavy:
            # -ā, -bā, -ak, -bak
            if len(syllable) == 1:
                if self._is_macron_vowel(syllable):
                    syllables_stress.append((syllable, "Heavy"))
                    continue
            elif len(syllable) == 2:
                if self._is_consonant(syllable[0]) and self._is_macron_vowel(syllable[1]):
                    syllables_stress.append((syllable, "Heavy"))
                    continue
                if self._is_short_vowel(syllable[0]) and self._is_consonant(syllable[1]):
                    syllables_stress.append((syllable, "Heavy"))
                    continue
            elif len(syllable) == 3:
                if self._is_short_vowel(syllable[1]):
                    syllables_stress.append((syllable, "Heavy"))
                    continue

            # Light:
            # -a, -ba
            if len(syllable) == 1:
                if self._is_short_vowel(syllable):
                    syllables_stress.append((syllable, "Light"))
                    continue
            elif len(syllable) == 2:
                if self._is_consonant(syllable[0]) and self._is_short_vowel(syllable[1]):
                    syllables_stress.append((syllable, "Light"))
                    continue

        # It's easier to find stress backwards
        syllables_stress = syllables_stress[::-1]

        syllables = []
        found_stress = 0
        for i, syllable in enumerate(syllables_stress):
            # If we've found the stressed syllable just append the next syllable
            if found_stress:
                syllables.append(syllable[0])
                continue

            # Rule (a)
            elif syllable[1] == "Ultraheavy" and i == 0:
                syllables.append("[{}]".format(syllable[0]))
                found_stress = 1
                continue

            # Rule (b)
            elif syllable[1] in ['Ultraheavy', 'Heavy'] and i > 0:
                syllables.append("[{}]".format(syllable[0]))
                found_stress = 1
                continue

            # Final 'Heavy' syllable, gets no stress
            elif syllable[1] == 'Heavy' and i == 0:
                syllables.append(syllable[0])
                continue

            # Light syllable gets no stress
            elif syllable[1] == "Light":
                syllables.append(syllable[0])
                continue

        # Reverse the list again
        syllables = syllables[::-1]

        # If we still haven't found stress then rule (c) applies
        # Rule (c)
        if not found_stress:
            syllables[0] = "[{}]".format(syllables[0])

        return syllables
