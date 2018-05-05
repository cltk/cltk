
__author__ = ['Chatziargyriou Eleftheria <ele.hatzy@gmail.com>']
__license__ = 'MIT License'

from cltk.stem.middle_english.stem import affix_stemmer

"""
The hyphenation/syllabification algorithm is based on the typical syllable 
structure model of onset/nucleus/coda. An additional problem arises with the
distinction between long and short vowels, since many use identical graphemes 
for both long and short vowels. The great vowel shift that dates back to the
early stages of ME poses an additional problem.
"""

SHORT_VOWELS = ['a', 'e', 'i', 'o', 'u', 'y', 'æ']

LONG_VOWELS = ['aa', 'ee', 'oo', 'ou', 'ow', 'ae']

DIPHTHONGS = ['th', 'gh', 'ht', 'ch']

TRIPHTHONGS = ['ght', 'ghl']

CONSONANTS = ['b', 'c', 'd', 'f', 'g', 'h', 'l', 'm', 'n', 'p', 'r', 's', 't', 'x', 'ð', 'þ', 'ƿ']


class Word:

    def __init__(self, word):
        self.word = word
        self.syllabified = None
        self.stressed = None

    def syllabify(self):
        """
        Syllabification module for Middle English.

        Throughout the early 11th-14th century, ME went through a process of
        loss of gemination. Originally, the syllable preceding a geminate was
        a closed one. The method assumes any occurring geminates will be
        separated like in Modern English (working both as coda of first syllable
        and onset of the other).

        The algorithm also takes into account the shortening of vowels before a
        cluster of consonants which took place at the earlier stages of the
        language.

         Returns:
             list: string list containing the syllables of the given word
        
        Examples:
            >>> Word('heldis').syllabify()
            ['hel', 'dis']
            >>> Word('greef').syllabify()
            ['greef']

            Once you syllabify the word, the result will be saved as a class
            variable

            >>> word = Word('commaundyd')

            >>> word.syllabify()
            ['com', 'mau', 'ndyd']

            >>> word.syllabified
            ['com', 'mau', 'ndyd']
        """

        # Array holding the index of each given syllable
        ind = []

        i = 0
        # Iterate through letters of word searching for the nuclei
        while i < len(self.word) - 1:

            if self.word[i] in SHORT_VOWELS:

                nucleus = ''

                # Find cluster of vowels
                while self.word[i] in SHORT_VOWELS and i < len(self.word) - 1:
                    nucleus += self.word[i]
                    i += 1

                try:
                    # Check whether it is suceeded by a geminant

                    if self.word[i] == self.word[i + 1]:
                        ind.append(i)
                        i += 2
                        continue

                    elif sum(c not in CONSONANTS for c in self.word[i:i + 3]) == 0:
                        ind.append(i - 1 if self.word[i:i + 3] in TRIPHTHONGS else i)
                        i += 3
                        continue

                except IndexError:
                    pass

                if nucleus in SHORT_VOWELS:
                    ind.append(i - 1 if self.word[i:i + 2] in DIPHTHONGS else i)
                    continue

                else:
                    ind.append(i - 1)
                    continue

            i += 1

        #Check whether the last syllable should be merged with the previous one
        try:
            if ind[-1] in [len(self.word) - 2, len(self.word) - 1]:
                ind = ind[:-(1 + (ind[-2] == len(self.word) - 2))]

        except IndexError:
            if ind[-1] in [len(self.word) - 2, len(self.word) - 1]:
                ind = ind[:-1]

        self.syllabified = self.word

        for n, k in enumerate(ind):
            self.syllabified = self.syllabified[:k + n + 1] + "." + self.syllabified[k + n + 1:]

        # Check whether the last syllable lacks a vowel nucleus

        self.syllabified = self.syllabified.split(".")

        if sum(map(lambda x: x in SHORT_VOWELS, self.syllabified[-1])) == 0:
            self.syllabified[-2] += self.syllabified[-1]
            self.syllabified = self.syllabified[:-1]

        return self.syllabified

    def syllabified_str(self, separator="."):
        """
        Returns:
             str: Syllabified word in string format
        
        Examples:
            >>> Word('conseil').syllabified_str()
            'con.seil'
            
            You can also specify the separator('.' by default)
            
            >>> Word('sikerly').syllabified_str(separator = '-')
            'sik-er-ly'
        """
        return separator.join(self.syllabified if self.syllabified else self.syllabify())

    def stresser(self, stress_rule = 'FSR'):
        """
        Args:
        
            :param stress_rule: Stress Rule, valid options:

                'FSR': French Stress Rule, stress falls on the ultima, unless
                 it contains schwa (ends with e), in which case the penult is
                stressed

                'GSR': Germanic Stress Rule, stress falls on the first syllable
                of the stemm. Note that the accuracy of the function directly
                depends on that of the stemmer.

                'LSR': Latin Stress Rule, stress falls on the penult if its 
                heavy, else, if it has more than two syllables on the 
                antepenult, else on the ultima.

        Returns:
        
            list: A list containing the separate syllable, where the stressed
            syllable is prefixed by ' . Monosyllabic words are left unchanged,
            since stress indicates relative emphasis.

        Examples:

            >>> Word('beren').stresser(stress_rule = "FSR")
            ['ber', "'en"]

            >>> Word('prendre').stresser(stress_rule = "FSR")
            ["'pren", 'dre']

            >>> Word('yisterday').stresser(stress_rule = "GSR")
            ['yi', 'ster', "'day"]

            >>> Word('day').stresser(stress_rule = "GSR")
            ['day']

            >>> Word('mervelus').stresser(stress_rule = "LSR")
            ["'mer", 'vel', 'us']

            >>> Word('verbum').stresser(stress_rule = "LSR")
            ['ver', "'bum"]
        """

        #Syllabify word
        if not self.syllabified:
            self.syllabify()

        #Check whether word is monosyllabic
        if len(self.syllabified) == 1:
            return self.syllabified

        if stress_rule == 'FSR':
            #Check whether ultima ends in e
            if self.syllabified[-1][-1] == 'e':
                return self.syllabified[:-2] + ['\'{0}'.format(self.syllabified[-2])] + self.syllabified[-1:]

            else:
                return self.syllabified[:-1] + ['\'{0}'.format(self.syllabified[-1])]

        elif stress_rule == 'GSR':
            #The word striped of suffixes
            st_word = affix_stemmer([self.word], strip_suf = False)
            affix = self.word[:len(self.word) - len(st_word)]

            #Syllabify stripped word and affix

            syl_word = Word(st_word).syllabify()

            #Add stress
            syl_word = ['\'{0}'.format(syl_word[0])] + syl_word[1:]

            if affix:
                affix = Word(affix).syllabify()
                syl_word = affix + syl_word

            return syl_word

        elif stress_rule == 'LSR':
            #Check whether penult is heavy (contains more than one mora)
            if sum(map(lambda x: x in SHORT_VOWELS, self.syllabified[-1])) > 1:
                return self.syllabified[:-2] + ['\'{0}'.format(self.syllabified[-2])] + self.syllabified[-1:]

            elif len(self.syllabified) > 2:
                return self.syllabified[:-3] + ['\'{0}'.format(self.syllabified[-3])] + self.syllabified[-2:]

            else:
                return self.syllabified[:-1] + ['\'{0}'.format(self.syllabified[-1])]
            
 
