__author__ = ['Chatziargyriou Eleftheria <ele.hatzy@gmail.com>']
__license__ = 'MIT License'
"""
The hyphenation/syllabification algorithm is based on the typical syllable structure model of onset/nucleus/coda.
TODO: Add hypothesized IPA transcription
"""


"""
An additional problem arises with the distinction between long and short vowels, since many use identical graphemes for
both long and short vowels. 
"""

SHORT_VOWELS = ['a', 'e', 'i', 'o', 'u', 'y', 'æ']

LONG_VOWELS = ['aa', 'ee', 'oo', 'ou', 'ow', 'ae']

DIPHTHONGS = ['ai', 'au', 'aw', 'ay', 'ei', 'eu', 'ew', 'ey', 'iu', 'iw', 'oi', 'ow', 'oy', 'uw']

CONSONANTS = ['b', 'c', 'd', 'f', 'g', 'h', 'l', 'm', 'n', 'p', 'r', 's', 't', 'x', 'ð', 'þ', 'ƿ']

class Word:

    def __init__(self, word):
        self.word = word

    def syllabify(self):

        #Array holding the index of each given syllable
        ind = []

        i = 0
        #Iterate through letters of word searching for the nuclei
        while i < len(self.word) - 1:

            if self.word[i] in SHORT_VOWELS:

                nucleus = ''

                #Find cluster of vowels
                while self.word[i] in SHORT_VOWELS and i < len(self.word) - 1:
                    nucleus += self.word[i]
                    i += 1

                try:
                    #Check whether it is suceeded by a geminant

                    # Throught the early 11th-14th century, ME went through a process of loss of gemination (double
                    # consonants. Originally, the syllable preceding a geminate was a closed one. The following assumes
                    # any occuring geminates will be separated like in Modern English (working both as coda of first
                    # syllable and onset of the other

                    if self.word[i] == self.word[i + 1]:
                       ind.append(i)
                       i+=2
                       continue

                    #Vowels were shortened before clusters of three consonants
                    elif sum(c not in CONSONANTS for c in self.word[i:i+3]) == 0:
                       ind.append(i)
                       i += 3
                       continue

                except IndexError:
                    pass

                if nucleus in SHORT_VOWELS:
                    ind.append(i)
                    continue

                else:
                    ind.append(i - 1)
                    continue

            i += 1


        #Check whether the last nucleus should be merged with the previous syllable
        if ind[-1] in [len(self.word), len(self.word) - 1]:
            ind = ind[:-(1 + (ind[-2] == len(self.word) - 1))]

        for n, k in enumerate(ind):
            self.word = self.word[:k + n + 1] + "." + self.word[k + n + 1:]
            
  
