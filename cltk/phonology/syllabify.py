
from typing import List
import logging
import unicodedata
from collections import defaultdict

from cltk.exceptions import InputError
from cltk.corpus.middle_english.syllabifier import Syllabifier as ME_Syllabifier
from cltk.corpus.middle_high_german.syllabifier import Syllabifier as MHG_Syllabifier
from cltk.corpus.old_english.syllabifier import Syllabifier as OE_Syllabifier
from cltk.corpus.old_norse.syllabifier import hierarchy as old_norse_hierarchy
from cltk.corpus.old_norse.syllabifier import ipa_hierarchy as ipa_old_norse_hierarchy


__author__ = ['Eleftheria Chatziargyriou <ele.hatzy@gmail.com>', "Clément Besnier <clemsciences@aol.com>"]
__license__ = 'MIT License. See LICENSE.'


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

    return [onset for onset, i in onset_dict.items() if i/n > threshold]


class Syllabifier:
    def __init__(self, low_vowels=None, mid_vowels=None, high_vowels=None, flaps=None, laterals=None, nasals=None,
                 fricatives=None, plosives=None, language=None, break_geminants=False):
        
        self.break_geminants = break_geminants
        self.invalid_onsets = []
        self.invalid_ultima = []
        
        if language == 'middle_english':
            hierarchy = [[] for _ in range(len(set(ME_Syllabifier.values())))]

            for k in ME_Syllabifier:
                hierarchy[ME_Syllabifier[k] - 1].append(k)

            self.set_hierarchy(hierarchy)
            self.set_vowels(hierarchy[0])

            self.invalid_ultima = ['a', 'ae', 'æ', 'e', 'ea', 'eo', 'i', 'o', 'u', 'y']
        
        elif language == 'old_english':
            hierarchy = [[] for _ in range(len(set(OE_Syllabifier.values())))]

            for k in OE_Syllabifier:
                hierarchy[OE_Syllabifier[k] - 1].append(k)

            self.set_hierarchy(hierarchy)
            self.set_vowels(hierarchy[0])

        elif language == 'middle_high_german':
            hierarchy = [[] for _ in range(len(set(MHG_Syllabifier.values())))]

            for k in MHG_Syllabifier:
                hierarchy[MHG_Syllabifier[k]-1].append(k)

            self.set_hierarchy(hierarchy)
            self.set_vowels(hierarchy[0])

        elif language == "old_norse":
            self.set_hierarchy(old_norse_hierarchy)
            self.set_vowels(old_norse_hierarchy[0])
            
        elif language == "old_norse_ipa":
            self.set_hierarchy(ipa_old_norse_hierarchy)
            self.set_vowels(ipa_old_norse_hierarchy[0])

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

    def set_invalid_onsets(self, invalid_onsets):
        self.invalid_onsets = invalid_onsets

    def set_invalid_ultima(self, invalid_ultima):
        self.invalid_ultima = invalid_ultima

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
            return self.syllabify_ssp(word)

    def syllabify_ssp(self, word):
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
            
            >>> s = Syllabifier(language='middle_high_german')
            
            >>> s.syllabify('lobebæren')
            ['lo', 'be', 'bæ', 'ren']
            
            >>> s = Syllabifier(language='middle_english')
            
            >>> s.syllabify("huntyng")
            ['hun', 'tyng']
            
            >>> s = Syllabifier(language='old_english')
            
            >>> s.syllabify("arcebiscop")
            ['ar', 'ce', 'bis', 'cop']
            
            The break_geminants parameter ensures a breakpoint is placed between geminants:
            
            >>> geminant_s = Syllabifier(break_geminants=True)
            
            >>> hierarchy = [["a", "á", "æ", "e", "é", "i", "í", "o", "ǫ", "ø", "ö", "œ", "ó", "u", "ú", "y", "ý"], ["j"], ["m"], ["n"], ["p", "b", "d", "g", "t", "k"], ["c", "f", "s", "h", "v", "x", "þ", "ð"], ["r"], ["l"]]
            
            >>> geminant_s.set_hierarchy(hierarchy)
            
            >>> geminant_s.set_vowels(hierarchy[0])
            
            >>> geminant_s.syllabify("ennitungl")
            ['en', 'ni', 'tungl']

            
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
                "The given string contains invalid characters. "
                "Make sure to define the mater of articulation for each phoneme.")
            raise InputError

        while i < len(word) - 1:
            # Search for nucleus
            while word[i] not in self.vowels and i < len(word) - 1 and find_nucleus:
                i += 1
            
            if find_nucleus is True:
                i += 1
            
            if i >= len(word) - 1:
                break

            else:
                # If the break_geminants parameter is set to True, prioritize geminants
                if self.break_geminants and word[i-1] == word[i]:
                    syllables.append(i-1)
                    find_nucleus = True 
                    
                # If a cluster of three phonemes with the same values exist, break syllable
                elif encoded[i - 1] == encoded[i] == encoded[i + 1]:
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

        return self.onset_maximization(word)

    def onset_maximization(self, syllables):

        for i, syl in enumerate(syllables):
            if i != len(syllables) - 1:
                if syllables[i+1][0] in self.vowels and syllables[i+1][-1] not in self.vowels:
                    syllables[i+1] = syllables[i][-1] + syllables[i+1]
                    syllables[i] = syllables[i][:-1]

        return self.legal_onsets(syllables)

    def legal_onsets(self, syllables):
        """
        Filters syllable respecting the legality principle
        :param syllables: str list

        Example:
            The method scans for invalid syllable onsets:

            >>> s = Syllabifier(["i", "u", "y"], ["o", "ø", "e"], ["a"], ["r"], ["l"], ["m", "n"], ["f", "v", "s", "h"], ["k", "g", "b", "p", "t", "d"])

            >>> s.set_invalid_onsets(['lm'])

            >>> s.legal_onsets(['a', 'lma', 'tigr'])
            ['al', 'ma', 'tigr']

            You can also define invalid syllable ultima:

            >>> s.set_invalid_ultima(['gr'])

            >>> s.legal_onsets(['al', 'ma', 'ti', 'gr'])
            ['al', 'ma', 'tigr']

        """

        vowels = self.vowels

        for i in range(1, len(syllables)):
            onset = ""
            
            for letter in syllables[i]:

                if letter in vowels:
                    break

                onset += letter

            for j in range(len(onset)):
                # Check whether the given onset is valid
                if onset[j:] not in self.invalid_onsets:
                    syllables[i - 1] += onset[:j]
                    syllables[i] = syllables[i][j:]
                    break

        # Check whether ultima is invalid

        if syllables[-1] in self.invalid_ultima:
            syllables[-2] += syllables[-1]
            syllables = syllables[:-1]

        return syllables

    def syllabify_ipa(self, word):
        """
        Parses IPA string
        :param word: word to be syllabified
        """
        word = word[1:-1]
        word = ''.join(l for l in unicodedata.normalize('NFD', word) if unicodedata.category(l) != 'Mn')

        return self.syllabify_ssp(word)

    def syllabify_phonemes(self, phonological_word):
        """

        :param phonological_word: result of Transcriber().text_to_phonemes in cltk.phonology.utils
        :return:
        """
        phoneme_lengths = []
        l_transcribed_word = []
        for phoneme in phonological_word:
            phoneme_lengths.append(len(phoneme.ipar))
            l_transcribed_word.append(phoneme.ipar)
        transcribed_word = "".join(l_transcribed_word)
        transcribed_word = transcribed_word.replace("ː", "")
        syllabified_transcribed_word = self.syllabify_ssp(transcribed_word)

        syllabified_phonological_word = []
        counter = 0  # number of IPA character processed
        for i, sts in enumerate(syllabified_transcribed_word):
            syllabified_phonological_word.append([])
            syllable_len = len(sts)
            somme = 0
            while somme < syllable_len:
                somme += phoneme_lengths[counter]
                syllabified_phonological_word[i].append(phonological_word[counter])
                counter += 1

        return syllabified_phonological_word


class Syllable:
    """
    A syllable has three main constituents:
    - onset
    - nucleus
    - coda

    Source: https://en.wikipedia.org/wiki/Syllable
    """
    def __init__(self, text: str, vowels: List[str], consonants: List[str]):
        """

        :param text:  a syllable
        :param vowels: list of characters
        :param consonants: list of characters
        """
        self.onset = []
        self.nucleus = []
        self.coda = []
        self.text = text
        self.consonants = consonants
        self.vowels = vowels

        self._compute_syllable(text)

    def _compute_syllable(self, text):
        """
        >>> sylla1 = Syllable("armr", ["a"], ["r", "m"])
        >>> sylla1.onset
        []
        >>> sylla1.nucleus
        ['a']
        >>> sylla1.coda
        ['r', 'm', 'r']

        >>> sylla2 = Syllable("gangr", ["a"], ["g", "n", "r"])
        >>> sylla2.onset
        ['g']
        >>> sylla2.nucleus
        ['a']
        >>> sylla2.coda
        ['n', 'g', 'r']


        >>> sylla3 = Syllable("aurr", ["a", "u"], ["r"])
        >>> sylla3.nucleus
        ['a', 'u']
        >>> sylla3.coda
        ['r', 'r']


        :param text: a syllable
        :return:
        """
        is_in_onset = True
        is_in_nucleus = False
        is_in_coda = False
        if len(text) > 0:
            for c in text:
                if is_in_onset and c in self.consonants:
                    self.onset.append(c)

                elif is_in_onset and c in self.vowels:
                    is_in_onset = False
                    is_in_nucleus = True
                    self.nucleus.append(c)

                elif is_in_nucleus and c in self.vowels:
                    self.nucleus.append(c)

                elif is_in_nucleus and c in self.consonants:
                    is_in_nucleus = False
                    is_in_coda = True
                    self.coda.append(c)

                elif is_in_coda and c in self.consonants:
                    self.coda.append(c)

                elif is_in_coda and c in self.vowels:
                    raise ValueError("This is not a correct syllable "
                                     "(a vowel '{}' cannot be inserted in coda)".format(c))

                else:
                    raise ValueError("{} is an unknown character".format(c))

            if len(self.nucleus) == 0:
                raise ValueError("This is not a correct syllable")
        else:
            raise ValueError("A syllable can't be void")

    def __str__(self):
        return "".join(self.onset)+"".join(self.nucleus)+"".join(self.coda)
