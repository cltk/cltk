"""

"""
import re
import unicodedata

from cltk.alphabet.gmh import (
    CONSONANTS,
    DIPHTHONGS,
    LONG_VOWELS,
    SHORT_VOWELS,
    TRIPHTHONGS,
)
from cltk.stem.gmh import stem

__author__ = ["Eleftheria Chatziargyriou <ele.hatzy@gmail.com>"]
__license__ = "MIT License"


# Soundex Dictionary
dict_diphth_se = {"ng": "2", "ch": "2", "pf": "4", "ts": "4"}

dict_se = {
    "f": "1",
    "b": "1",
    "p": "1",
    "v": "1",
    "w": "1",
    "m": "2",
    "n": "2",
    "t": "3",
    "d": "3",
    "r": "3",
    "l": "3",
    "k": "3",
    "c": "3",
    "g": "3",
    "s": "3",
    "z": "4",
    "ȥ": "4",
    "s": "4",
    "r": "5",
    "l": "5",
    "j": "6",
}

hierarchy = [
    ["a", "e", "i", "o", "u", "y", "ä", "ö", "ü", "æ", "œ", "â", "ô", "û", "ê", "î"],
    ["l", "m", "n", "r", "w", "j"],
    ["b", "c", "d", "f", "g", "h", "k", "p", "q", "v", "t", "s", "z"],
]


class Word:
    """
    Word class that helps
    """

    def __init__(self, word):
        self.word = word.lower()
        self.syllabified = []

    def phonetic_indexing(self, p="SE"):
        """Specifies the phonetic indexing method.
        SE: Soundex variant for MHG"""

        if p == "SE":
            return self._soundex()
        else:
            print("Parameter value not supported")

    def _soundex(self):
        """
        Soundex variant was based on the original American Soundex  developed by Russel
        and King, altered to better fit Middle High German morphology. The replacement
        rules were based on matching places and manners of articulation between the
        two languages (AE and MHG).

        Algorithm:

        -Normalize word and convert the first letter to uppercase
        -Remove other vowels

        Replacement Rules:
        - f,v,b,p,w -> 1 Labiodental fricatives [f,v] and bilabial plosives [p,b], approximant [w]
        - m,n,ng -> 2 Nasals
        - t,d,r,l,k,c,g,ch,s -> 3 [non-nasal velars/alveolars]
        - pf, ts, z, s -> 4  Affricates and alveolar fricatives
        - r,l -> 5 Liquids
        - j -> 6 Palatal Approximant

        -Remove double numbers
        -Remove remaining letters
        -Retain first 3 numbers (add 0 if less than 3)
        """
        t_word = stem(self.word[0].lower()).upper() + stem(self.word[1:]).lower()

        for w, val in zip(dict_diphth_se.keys(), dict_diphth_se.values()):
            t_word = t_word.replace(w, val)

        for w, val in zip(dict_se.keys(), dict_se.values()):
            t_word = t_word.replace(w, val)

        # Remove adjacent duplicate numbers
        t_word = re.sub(r"(\d)\1+", r"\1", t_word)

        # Strip remaining letters
        t_word = re.sub(r"[a-zæœ]+", "", t_word)

        return (t_word + "0" * 3)[:4]  # Add trailing zeroes
