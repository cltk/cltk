"""This module attempts to reconstruct the approximate phonology of Old English.
"""

import logging
import re
import unicodedata

__author__ = [
    "John Stewart <johnstewart@aya.yale.edu>",
    "Clément Besnier <clem@clementbesnier.fr>",
]


IPA_rules = {
    "ea": "æːɑ",
    "ēa": "æːɑ",
    "nk": "ŋk",
    "ng": "ŋg",
    "hw": "ʍ",
    "hl": "l",
    "hn": "n̥",
    "hr": "r̥",
    "sċ": "ʃ",
}

IPA = {
    "a": "ɑ",
    "æ": "æ",
    "b": "b",
    "c": "k",
    "ċ": "tʃ",
    "d": "d",
    "ð": "ð",
    "e": "e",
    "f": "f",
    "g": "g",
    "ġ": "j",
    "h": "h",
    "i": "i",
    "l": "l",
    "m": "m",
    "n": "n",
    "o": "o",
    "p": "p",
    "r": "r",
    "s": "s",
    "t": "t",
    "u": "u",
    "w": "w",
    "ƿ": "ƿ",
    "x": "x",
    "y": "y",
    "þ": "θ",
    "ǣ": "æː",
    "ā": "ɑː",
    "ē": "eː",
    "ī": "iː",
    "ū": "uː",
    "ō": "oː",
    "ȳ": "yː",
}

Normalize = {
    "Æ": "Ae",
    "Ƿ": "W",
    "Þ": "Th",
    "Ð": "D",
    "æ": "ae",
    "ƿ": "w",
    "þ": "th",
    "ð": "d",
}

L_Transliteration = Transliteration = {
    "ᚪ": "a",
    "ᚫ": "æ",
    "ᛒ": "b",
    "ᚳ": "c",
    "ᛞ": "d",
    "ᛖ": "e",
    "ᛠ": "ea",
    "ᚠ": "f",
    "ᚷ": "g",
    "ᚸ": "g",
    "ᚻ": "h",
    "ᛁ": "i",
    "ᛇ": "i",
    "ᛄ": "j",
    "ᛣ": "k",
    "ᛤ": "k",
    "ᛚ": "l",
    "ᛗ": "m",
    "ᚾ": "n",
    "ᛝ": "n",
    "ᚩ": "o",
    "ᛟ": "oe",
    "ᛈ": "p",
    "ᚱ": "r",
    "ᛋ": "s",
    "ᛏ": "t",
    "ᚦ": "th",
    "ᚢ": "u",
    "ᚹ": "w",
    "ᛉ": "x",
    "ᚣ": "y",
}

R_Transliteration = {
    "ae": "ᚫ",
    "ea": "ᛠ",
    "eo": "ᛇ",
    "oe": "ᛟ",
    "ia": "ᛡ",
    "io": "ᛡ",
    "a": "ᚪ",
    "æ": "ᚫ",
    "b": "ᛒ",
    "c": "ᚳ",
    "d": "ᛞ",
    "e": "ᛖ",
    "f": "ᚠ",
    "g": "ᚷ",
    "h": "ᚻ",
    "i": "ᛁ",
    "j": "ᛄ",
    "k": "ᛣ",
    "l": "ᛚ",
    "m": "ᛗ",
    "n": "ᚾ",
    "ŋ": "ᛝ",
    "o": "ᚩ",
    "œ": "ᛟ",
    "p": "ᛈ",
    "þ": "ᚦ",
    "ð": "ᚦ",
    "ƿ": "ᚹ",
    "q": "ᛤ",
    "r": "ᚱ",
    "s": "ᛋ",
    "t": "ᛏ",
    "u": "ᚢ",
    "v": "ᚹ",
    "w": "ᚹ",
    "x": "ᛉ",
    "y": "ᚣ",
    "z": "ᛉ",
}


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class Transcriber:
    """"""

    def __init__(self):
        pass

    @staticmethod
    def transcribe(text: str, punctuation=True, with_squared_brackets=True) -> str:
        """
        :param text: The text to be transcribed
        :param punctuation: Retain punctuation
        :param with_squared_brackets: if True, add squared bracked around transcription

        The algorithm first tries the substitutions defined in
        IPA_rules and IPA.

        The following exceptions are considered:

        - Geminants are pronounced as long consonants/vowels

        - [v ð z] are allophones of the fricatives /f θ s/ between vowels
        - [ŋ] is an allophone of /n/ occurring before /k/ and /ɡ/
        - [ɣ] is an allophone of /g/ after a vowel or liquid
        - /l r/ were velarized when geminated or before a consonant
        - [ç, x]  are allophones of /h/ when occuring in the coda of a syllable and
          preceded by front and back vowels respectively

        Examples:

        >>> Transcriber().transcribe('Fæder ūre þū þe eeart on heofonum,', punctuation = True)
        '[fæder uːre θuː θe eːɑrˠt on heovonum,]'

        >>> Transcriber().transcribe('Hwæt! wē Gār-Dena in ġēar-dagum', punctuation = False)
        '[ʍæt weː gɑːrdenɑ in jæːɑrdɑgum]'
        """

        if not punctuation:
            text = re.sub(r"[\.\";\,\:\[\]\(\)!&?‘]", "", text)

        text = text.lower()
        text = re.sub(r"rr", "rˠ", text)
        text = re.sub(r"(\w)\1", r"\1ː", text)

        text = re.sub(r"(?<=[iīæǣeē])h", "ç", text)
        text = re.sub(r"(?<=[aāoōuū])h", "x", text)

        text = re.sub(r"r(?=[bcdðfgġhlmnprstwƿxþ])", "rˠ", text)
        text = re.sub(r"l(?=[bcdðfgġhlmnprstwƿxþ])", "ɫ", text)

        text = re.sub(r"(?<=[aæeiouyǣāēīūōȳ])f(?=[aæeiouyǣāēīūōȳ])", "v", text)
        text = re.sub(r"(?<=[aæeiouyǣāēīūōȳ])þ(?=[aæeiouyǣāēīūōȳ])", "ð", text)
        text = re.sub(r"(?<=[aæeiouyǣāēīūōȳ])s(?=[aæeiouyǣāēīūōȳ])", "z", text)

        for w, val in zip(IPA_rules.keys(), IPA_rules.values()):
            text = text.replace(w, val)

        for w, val in zip(IPA.keys(), IPA.values()):
            text = text.replace(w, val)

        if with_squared_brackets:
            return "[" + text.replace("-", "") + "]"
        else:
            return text.replace("-", "")


class Word:
    """
    Transcription of Old English words
    """

    def __init__(self, w: str):
        self.word = w

    def remove_diacritics(self) -> str:
        """
        :return: str: the input string stripped of its diacritics

        Examples:

        >>> Word('ġelǣd').remove_diacritics()
        'gelæd'

        """

        w = ""
        for c in unicodedata.normalize("NFKD", self.word):
            if "LATIN" == unicodedata.name(c)[:5]:
                w += c

        return w

    def ascii_encoding(self):
        """
        :return: str: Returns the ASCII-encoded string

        Thorn (Þ, þ) and Ash(Æ, æ) are substituted by the digraphs
        'th' and 'ae' respectively. Wynn(Ƿ, ƿ) and Eth(Ð, ð) are replaced
        by 'w' and 'd'.

        Examples:

        >>> Word('ġelǣd').ascii_encoding()
        'gelaed'

        >>> Word('ƿeorðunga').ascii_encoding()
        'weordunga'

        """

        w = self.remove_diacritics()

        for k, val in zip(Normalize.keys(), Normalize.values()):
            w = w.replace(k, val)

        return w
