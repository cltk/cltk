__author__ = ['Eleftheria Chatziargyriou <ele.hatzy@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import logging
import unicodedata

from collections import defaultdict
from cltk.exceptions import InputError
from cltk.corpus.middle_high_german.syllabifier import Syllabifier as MHG_Syllabifier


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


def get_onsets(text, vowels="aeiou", threshold=0.0002):
    """
    Source: Resonances in Middle High German: New Methodologies in Prosody,
    2017, C. L. Hench

    :param text: str list: text to be analysed

    :param vowels: str: valid vowels constituting the syllable

    :param threshold: minimum frequency count for valid onset, C. Hench noted
    that the algorithm produces the best result for an untagged wordset of MHG,
    when retaining onsets which appear in at least 0.02% of the words

    Example:
        Let's test it on the opening lines of Nibelungenlied

        >>> text = ['uns', 'ist', 'in', 'alten', 'mæren', 'wunders', 'vil', 'geseit', 'von', 'helden', 'lobebæren', 'von', 'grôzer', 'arebeit', 'von', 'fröuden', 'hôchgezîten', 'von', 'weinen', 'und', 'von', 'klagen', 'von', 'küener', 'recken', 'strîten', 'muget', 'ir', 'nu', 'wunder', 'hœren', 'sagen']

        >>> vowels = "aeiouæœôîöü"

        >>> get_onsets(text, vowels=vowels)
        ['lt', 'm', 'r', 'w', 'nd', 'v', 'g', 's', 'h', 'ld', 'l', 'b', 'gr', 'z', 'fr', 'd', 'chg', 't', 'n', 'kl', 'k', 'ck', 'str']

         Of course, this is an insignificant sample, but we could try and see
         how modifying the threshold affects the returned onset:

        >>> get_onsets(text, threshold = 0.05, vowels=vowels)
        ['m', 'r', 'w', 'nd', 'v', 'g', 's', 'h', 'b', 'z', 't', 'n']
    """
    onset_dict = defaultdict(lambda: 0)
    n = len(text)

    for word in text:
        onset = ''
        candidates = []

        for l in word:

            if l not in vowels:
                onset += l

            else:
                if onset != '':
                    candidates.append(onset)
                    onset = ''

        for c in candidates:
            onset_dict[c] += 1

    return return [onset for onset, i in onset_dict.items() if i/n > threshold]


class Syllabifier:

    def __init__(self, low_vowels=None, mid_vowels=None, high_vowels=None, flaps=None, laterals=None, nasals=None,
                 fricatives=None, plosives=None, language=None):

        if language == 'middle high german':
            hierarchy = [[] for _ in range(len(set(MHG_Syllabifier.values())))]

            for k in MHG_Syllabifier:
                hierarchy[MHG_Syllabifier[k]-1].append(k)

            self.set_hierarchy(hierarchy)
            self.set_vowels(hierarchy[0])

        else:

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
            
            Additionally, you can utilize the language parameter:
            
            >>> s = Syllabifier(language='middle high german')
            
            >>> s.syllabify('lobebæren')
            ['lo', 'be', 'bæ', 'ren']
            
        """

        # List indicating the syllable indices
        syllables = []

        find_nucleus = True

        i = 0

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


    def syllabify_IPA(self, word):
        """
        Parses IPA string
        :param word: word to be syllabified
        """
        word = word[1:-1]
        word = ''.join(l for l in unicodedata.normalize('NFD', word)
                                if unicodedata.category(l) != 'Mn')

        print(word)
        return self.syllabify_SSP(word)

