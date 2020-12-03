"""Middle English stress module
"""

import re
from typing import List

from cltk.phonology.enm.syllabifier import (
    CONSONANTS,
    DIPHTHONGS,
    SHORT_VOWELS,
    TRIPHTHONGS,
)
from cltk.stem.enm import stem

__author__ = [
    "Eleftheria Chatziargyriou <ele.hatzy@gmail.com>",
    "Clément Besnier <clem@clementbesnier.fr>",
]

# Soundex replacement rules
dict_SE = {
    "p": "1",
    "b": "1",
    "f": "1",
    "v": "1",
    "gh": "1",
    "sh": "2",
    "t": "2",
    "d": "2",
    "s": "2",
    "z": "2",
    "r": "2",  # TODO
    "k": "2",
    "g": "2",
    "w": "2",
    "l": "3",
    "m": "4",
    "n": "4",
    "r": "5",  # TODO
}


class MiddleEnglishStresser:
    """
    Middle English stresser
    """

    def __init__(self, syllabifier=None):
        """

        :param syllabifier: Syllabifier instance
        """
        self.syllabifier = syllabifier

    def stress(self, word, stress_rule="FSR") -> List:
        """
        :param word: word to stress
        :param stress_rule: Stress Rule, valid options:

            'FSR': French Stress Rule, stress falls on the ultima, unless it contains schwa (ends with e), in which case the penult is stressed.

            'GSR': Germanic Stress Rule, stress falls on the first syllable of the stemm. Note that the accuracy of the function directly depends on that of the stemmer.

            'LSR': Latin Stress Rule, stress falls on the penult if its heavy, else, if it has more than two syllables on the antepenult, else on the ultima.

        :return: A list containing the separate syllable, where the stressed syllable is prefixed by ' . Monosyllabic words are left unchanged, since stress indicates relative emphasis.

        Examples:

        >>> from cltk.phonology.syllabify import Syllabifier
        >>> from cltk.phonology.enm.syllabifier import DIPHTHONGS, TRIPHTHONGS, SHORT_VOWELS, LONG_VOWELS
        >>> enm_syllabifier = Syllabifier()
        >>> enm_syllabifier.set_short_vowels(SHORT_VOWELS)
        >>> enm_syllabifier.set_vowels(SHORT_VOWELS+LONG_VOWELS)
        >>> enm_syllabifier.set_diphthongs(DIPHTHONGS)
        >>> enm_syllabifier.set_triphthongs(TRIPHTHONGS)
        >>> stresser = MiddleEnglishStresser(enm_syllabifier)
        >>> stresser.stress('beren', stress_rule="FSR")
        ['ber', "'en"]
        >>> stresser.stress('prendre', stress_rule="FSR")
        ["'pren", 'dre']
        >>> stresser.stress('yisterday', stress_rule="GSR")
        ['yi', 'ster', "'day"]
        >>> stresser.stress('day', stress_rule="GSR")
        ['day']
        >>> stresser.stress('mervelus', stress_rule="LSR")
        ["'mer", 'vel', 'us']
        >>> stresser.stress('verbum', stress_rule="LSR")
        ['ver', "'bum"]

        """

        assert self.syllabifier is not None

        # Syllabify word
        syllabified = self.syllabifier.syllabify(word, mode="MOP")

        # Check whether word is monosyllabic
        if len(syllabified) == 1:
            return syllabified

        if stress_rule == "FSR":
            # Check whether ultima ends in e
            if syllabified[-1][-1] == "e":
                return (
                    syllabified[:-2]
                    + ["'{0}".format(syllabified[-2])]
                    + syllabified[-1:]
                )

            else:
                return syllabified[:-1] + ["'{0}".format(syllabified[-1])]

        elif stress_rule == "GSR":
            # The word striped of suffixes
            st_word = stem(word, strip_suf=False)
            affix = word[: len(word) - len(st_word)]

            # Syllabify stripped word and affix

            syl_word = self.syllabifier.syllabify(st_word, mode="MOP")

            # Add stress
            syl_word = ["'{0}".format(syl_word[0])] + syl_word[1:]

            if affix:
                affix = self.syllabifier.syllabify(affix, mode="MOP")
                syl_word = affix + syl_word

            return syl_word

        elif stress_rule == "LSR":
            # Check whether penult is heavy (contains more than one mora)
            if sum(map(lambda x: x in SHORT_VOWELS, syllabified[-1])) > 1:
                return (
                    syllabified[:-2]
                    + ["'{0}".format(syllabified[-2])]
                    + syllabified[-1:]
                )

            elif len(syllabified) > 2:
                return (
                    syllabified[:-3]
                    + ["'{0}".format(syllabified[-3])]
                    + syllabified[-2:]
                )

            else:
                return syllabified[:-1] + ["'{0}".format(syllabified[-1])]

    def phonetic_indexing(self, word, p="SE") -> str:
        """
        :param word: word
        :param p: Specifies the phonetic indexing method
                SE: Soundex variant for MHG

        :return: Encoded string corresponding to the word's phonetic
            representation
        """

        if p == "SE":
            return self._soundex(word)

    def _soundex(self, word):
        """
        The Soundex phonetic indexing algorithm adapted to ME phonology.

        Algorithm:

        Let w the original word and W the resulting one

        1) Capitalize the first letter of w and append it to W

        2) Apply the following replacement rules

            p, b, f, v, gh (non-nasal fricatives) -> 1

            t, d, s, sh, z, r, k, g, w (non-nasal alveolars and velars) -> 2

            l (alveolar lateral) -> 3

            m, n (nasals) -> 4

            r (alveolar approximant) -> 5

        3) Concetate multiple occurrences of numbers into one

        4) Remove non-numerical characters

        Notes:
            /h/ was thought to be either a voiceless or velar fricative
        when occurring in the coda with its most used grapheme being <gh>.
        Those phonemes either disappeared, resulting in the lengthening
        of preceding vowel clusters, or were developed into /f/ as evident
        by modern spelling (e.g. 'enough': /ɪˈnʌf/ and 'though': /ðəʊ/)

        Examples:

        >>> MiddleEnglishStresser().phonetic_indexing("midel", "SE")
        'M230'

        >>> MiddleEnglishStresser().phonetic_indexing("myddle", "SE")
        'M230'

        >>> MiddleEnglishStresser().phonetic_indexing("might", "SE")
        'M120'

        >>> MiddleEnglishStresser().phonetic_indexing("myghtely", "SE")
        'M123'
        """

        self.word = word
        word = self.word[1:]

        for w, val in zip(dict_SE.keys(), dict_SE.values()):
            word = word.replace(w, val)

        # Remove multiple adjacent occurences of digit
        word = re.sub(r"(\d)\1+", r"\1", word)

        # Strip remaining letters
        word = re.sub(r"[a-zðþƿ]+", "", word)

        # Add trailing zeroes and return
        return (self.word[0].upper() + word + "0" * 3)[:4]
