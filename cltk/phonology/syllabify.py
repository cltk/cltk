
__author__ = ['Eleftheria Chatziargyriou <ele.hatzy@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import logging
from cltk.exceptions import InputError

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

class Syllabifier:

    def __init__(self, low_vowels=[], mid_vowels=[], high_vowels=[], flaps=[], laterals=[], nasals=[], fricatives=[], plosives=[]):

        self.low_vowels = low_vowels
        self.mid_vowels = mid_vowels
        self.high_vowels = high_vowels
        self.vowels = low_vowels + mid_vowels + high_vowels

        self.flaps = flaps
        self.laterals = laterals
        self.nasals = nasals
        self.fricatives = fricatives
        self.plosives = plosives
        self.consonants = flaps + laterals + fricatives + plosives

        #Dictionary indicating sonority hierarchy
        self.hierarchy = {key:0 for key in self.low_vowels}
        self.hierarchy.update({key: 1 for key in self.mid_vowels})
        self.hierarchy.update({key: 2 for key in self.high_vowels})
        self.hierarchy.update({key: 3 for key in self.flaps})
        self.hierarchy.update({key: 4 for key in self.laterals})
        self.hierarchy.update({key: 5 for key in self.nasals})
        self.hierarchy.update({key: 6 for key in self.fricatives})
        self.hierarchy.update({key: 7 for key in self.plosives})

    def syllabify(self, word, mode = 'SSP'):
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
            cltk.exceptions.InputError: The given string contains invalid characters. Make sure to define the mater of articulation for each phoneme.
        """

        #List indicating the syllable indices
        syllables = []

        find_nucleus = True

        i = 1

        try:
            #Replace each letter occurence with its corresponding number
            #indicating its position in the sonority hierarchy
            encoded = list(map(lambda x: self.hierarchy[x], word))

        except KeyError:
            LOG.error("The given string contains invalid characters. Make sure to define the mater of articulation for each phoneme.")
            raise InputError

        while i < len(word) - 1:
            #Search for nucleus
            while word[i] not in self.vowels and i < len(word) - 1 and find_nucleus:
                    i += 1

            if i >= len(word) - 1:
                break

            else:
                #If a cluster of three phonemes with the same values exist, break syllable
                if encoded[i-1] == encoded[i] == encoded[i+1]:
                    syllables.append(i)
                    find_nucleus = True

                elif encoded[i] > encoded[i-1] and encoded[i] > encoded[i+1]:
                    syllables.append(i)
                    find_nucleus = True

                elif encoded[i] < encoded[i-1] and encoded[i] < encoded[i+1]:
                    syllables.append(i)
                    find_nucleus = True

                else:
                    find_nucleus = False

                i += 1

        for n, k in enumerate(syllables):
            word = word[:k + n + 1] + "." + word[k + n + 1:]

        word = word.split('.')

        #Check if last syllable has a nucleus

        if sum(map(lambda x: x in self.vowels, word[-1])) == 0:
             word[-2] += word[-1]
             word = word[:-1]

        return word

