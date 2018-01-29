"""
Split Akkadian words into a list of syllables.  Logic is based on
A Grammar of Akkadian, Huehnergard 3rd. ed.

TODO: Check this logic with von Soden's Grundriss der akkadischen Grammatik.
TODO: Deal with j/y issue.
"""

__author__ = ['M. Willis Monroe <willismonroe@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

AKKADIAN = {
    'short_vowels': ['a', 'e', 'i', 'u'],
    'macron_vowels': ['ā', 'ē', 'ī', 'ū'],
    'circumflex_vowels': ['â', 'ê', 'î', 'û'],

    'consonants': ['b', 'd', 'g', 'h', 'ḫ', 'k', 'l', 'm',
                   'n', 'p', 'q', 'r', 's', 'ṣ', 'š',
                   't', 'ṭ', 'w', 'y', 'z', 'ʾ']
}


class Syllabifier(object):
    """Split Akkadian words into list of syllables"""

    def __init__(self, language=AKKADIAN):
        self.language = language

    def _is_consonant(self, char):
        return char in self.language['consonants']

    def _is_vowel(self, char):
        return char in self.language['short_vowels'] + \
               self.language['macron_vowels'] + \
               self.language['circumflex_vowels']

    def syllabify(self, word):
        syllables = []

        # catch single character words
        if len(word) == 1:
            return [word]

        # If there's an initial vowel and the word is longer than 2 letters,
        # and the third syllable is a not consonant (easy way to check for VCC pattern),
        # the initial vowel is the first syllable.
        # Rule (b.ii)
        if self._is_vowel(word[0]):
            if len(word) > 2 and not self._is_consonant(word[2]):
                syllables.append(word[0])
                word = word[1:]

        # flip the word and count from the back:
        word = word[::-1]

        # Here we iterate over the characters backwards trying to match
        # consonant and vowel patterns in a hierarchical way.
        # Each time we find a match we store the syllable (in reverse order)
        # and move the index ahead the length of the syllable.
        syllables_reverse = []
        i = 0
        while i < len(word):
            char = word[i]

            # CV:
            if self._is_vowel(char):
                if self._is_vowel(word[i + 1]):
                    # Next char is a vowel so cut off syllable here
                    syllables_reverse.append(word[i])
                    i += 1
                else:
                    syllables_reverse.append(word[i + 1] + word[i])
                    i += 2

            # CVC and VC:
            elif self._is_consonant(char):
                if self._is_vowel(word[i + 1]):
                    # If there are only two characters left, that's it.
                    if i + 2 >= len(word):
                        syllables_reverse.append(word[i + 1] + word[i])
                        break
                    # CVC
                    elif self._is_consonant(word[i + 2]):
                        syllables_reverse.append(word[i + 2] + word[i + 1] + word[i])
                        i += 3
                    # VC (remember it's backwards here)
                    elif self._is_vowel(word[i + 2]):
                        syllables_reverse.append(word[i + 1] + word[i])
                        i += 2

        return syllables + syllables_reverse[::-1]
