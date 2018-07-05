__author__ = ['Eleftheria Chatziargyriou <ele.hatzy@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import logging
from cltk.exceptions import InputError

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class Syllabifier:

    def __init__(self, low_vowels=None, mid_vowels=None, high_vowels=None, flaps=None, laterals=None, nasals=None,
                 fricatives=None, plosives=None):

        self.low_vowels = [] if low_vowels is None else low_vowels
        self.mid_vowels = [] if mid_vowels is None else mid_vowels
        self.high_vowels = [] if high_vowels is None else high_vowels
        self.vowels = self.low_vowels + self.mid_vowels + self.high_vowels

        self.flaps = [] if flaps is None else flaps
        self.laterals = [] if laterals is None else laterals
        self.nasals = [] if nasals is None else nasals
        self.fricatives = [] if fricatives is None else fricatives
        self.plosives = [] if plosives is None else plosives
        self.consonants = self.flaps + self.laterals + self.fricatives + self.plosives

        # Dictionary indicating sonority hierarchy
        self.hierarchy = {key: 0 for key in self.low_vowels}
        self.hierarchy.update({key: 1 for key in self.mid_vowels})
        self.hierarchy.update({key: 2 for key in self.high_vowels})
        self.hierarchy.update({key: 3 for key in self.flaps})
        self.hierarchy.update({key: 4 for key in self.laterals})
        self.hierarchy.update({key: 5 for key in self.nasals})
        self.hierarchy.update({key: 6 for key in self.fricatives})
        self.hierarchy.update({key: 7 for key in self.plosives})

    def set_hierarchy(self, hierarchy):
        """
        Sets an alternative sonority hierarchy, note that you will also need
        to specify the vowelset with the set_vowels, in order for the module
        to correctly identify each nucleus.

        The order of the phonemes defined is by decreased consonantality

        Example:
            >>> s = Syllabifier()

            >>> s.set_hierarchy([['i', 'u'], ['e'], ['a'], ['r'], ['m', 'n'], ['f']])

            >>> s.set_vowels(['i', 'u', 'e', 'a'])

            >>> s.syllabify('feminarum')
            ['fe', 'mi', 'na', 'rum']
        """
        self.hierarchy = dict([(k, i) for i, j in enumerate(hierarchy) for k in j])

    def set_vowels(self, vowels):
        """
        Define the vowel set of the syllabifier module

        Example:
            >>> s = Syllabifier()

            >>> s.set_vowels(['i', 'u', 'e', 'a'])
            
            >>> s.vowels
            ['i', 'u', 'e', 'a']
        """
        self.vowels = vowels

    def syllabify(self, word, mode='SSP'):
        if mode == 'SSP':
            return self.syllabify_SSP(word)

    def syllabify_SSP(self, word):
        """
        Syllabifies a word according to the Sonority Sequencing Principle

        :param word: Word to be syllabified
        :return: List consisting of syllables

        Example:
            First you need to define the matters of articulation
            >>> high_vowels = ['a']

            >>> mid_vowels = ['e']

            >>> low_vowels = ['i', 'u']

            >>> flaps = ['r']

            >>> nasals = ['m', 'n']

            >>> fricatives = ['f']

            >>> s = Syllabifier(high_vowels=high_vowels, mid_vowels=mid_vowels, low_vowels=low_vowels, flaps=flaps, nasals=nasals, fricatives=fricatives)

            >>> s.syllabify("feminarum")
            ['fe', 'mi', 'na', 'rum']

            Not specifying your alphabet results in an error:

            >>> s.syllabify("foemina")
            Traceback (most recent call last):
                ...
            cltk.exceptions.InputError
        """

        # List indicating the syllable indices
        syllables = []

        find_nucleus = True

        i = 1

        try:
            # Replace each letter occurence with its corresponding number
            # indicating its position in the sonority hierarchy
            encoded = list(map(lambda x: self.hierarchy[x], word))

        except KeyError:
            LOG.error(
                "The given string contains invalid characters. Make sure to define the mater of articulation for each phoneme.")
            raise InputError

        while i < len(word) - 1:
            # Search for nucleus
            while word[i] not in self.vowels and i < len(word) - 1 and find_nucleus:
                i += 1

            if i >= len(word) - 1:
                break

            else:
                # If a cluster of three phonemes with the same values exist, break syllable
                if encoded[i - 1] == encoded[i] == encoded[i + 1]:
                    syllables.append(i)
                    find_nucleus = True

                elif encoded[i] > encoded[i - 1] and encoded[i] > encoded[i + 1]:
                    syllables.append(i)
                    find_nucleus = True

                elif encoded[i] < encoded[i - 1] and encoded[i] < encoded[i + 1]:
                    syllables.append(i)
                    find_nucleus = True

                else:
                    find_nucleus = False

                i += 1

        for n, k in enumerate(syllables):
            word = word[:k + n + 1] + "." + word[k + n + 1:]

        word = word.split('.')

        # Check if last syllable has a nucleus

        if sum([x in self.vowels for x in word[-1]]) == 0:
            word[-2] += word[-1]
            word = word[:-1]

        return word
    
    
