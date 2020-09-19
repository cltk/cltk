"""Middle High German phonological transcriber module.

Note: there are no definite MHG  phonological rules, so this module serves
as an approximate reconstruction of the original. As of this version, the Transcribe
class doesn't support any specific dialects and serves as a superset encompassing
various regional accents.

Sources:
    * https://www.germanistik.uni-bonn.de/institut/abteilungen/germanistische-mediavistik/studium/leitfaeden-reader-links/b1-reader-oktober-2009-endversion.pdf
    * [A Middle High German Primer - Joseph Wright](http://www.minnesang.com/Themen/Ulrich%20Mueller%20zur%20Aussprache.pdf)
    * Clements, George N. "The role of the sonority cycle in core syllabification." Papers in laboratory phonology 1 (1990): 283-333.
"""

import re

__author__ = ["Eleftheria Chatziargyriou <ele.hatzy@gmail.com>"]
__license__ = "MIT License"


# IPA Dictionary
DIPHTHONGS_IPA = {
    "ei": "ɛ͡ɪ",  # Dipthongs
    "ie": "i͡ə",
    "üe": "y͡ə",
    "uo": "u͡ə",
    "iu": "yː",
    "öu": "ø͡u",
    "ou": "ɔ͡ʊ",
    "ch": "χ",
    "qu": "k",
    "tt": "t·t",
    "bb": "b·b",
    "gg": "g·g",
    "pp": "p·p",
    "tt": "t·t",
    "ck": "k·k",
    # c and k indicate the same sound and while c was most oftenly used at the beginning of a word, k was usually used at the end of a syllable
    "ff": "f·f",
    "ss": "s·s",
    "mm": "m·m",
    "nn": "n·n",
    "ll": "l·l",
    "rr": "r·r",
}

IPA = {
    "a": "a",  # Short vowels
    "ä": "æ",
    "e": "e",
    "ë": "e",
    "i": "ɪ",
    "o": "ɒ",
    "ö": "ọ̈",
    "u": "ʊ",
    "ü": "ʏ",
    "â": "ɑː",  # Long vowels
    "æ": "ɛ",
    "œ": "iu",
    "ê": "eː",
    "î": "iː",
    "ô": "oː",
    "û": "uː",
    "k": "k",  # Consonants
    "l": "l",
    "m": "m",
    "n": "n",
    "p": "p",
    "t": "t",
    "w": "w",
    "b": "b̥",
    # Ιn MHG. the consonants b, d, g were not voiced explosives like English b, d, g, but were voiceless lenes,
    "d": "d̥",  # and only differed from the fortes p, t, k in being produced with less intensity or force
    "g": "ɡ̊",  # - A Middle High German Primer, Joseph Wright
    "c": "k",
    "f": "f",  # Only accounts for labiodental form of latter HG
    "v": "f",
    "j": "j",
    "r": "r",  # Alveolar trilled r in all positions
    "w": "w",
    "z": "t͡s",
    "ȥ": "t͡s",
}


class Transcriber:
    """
    Transcriber for Middle High German
    """

    def __init__(self):
        pass  # To-do: Add different dialects and/or notations

    def transcribe(
        self, text: str, punctuation=True, with_squared_brackets=True
    ) -> str:
        """
        :param text: text to transcribe
        :param punctuation: if True, keeps punctuation
        :param with_squared_brackets: if True, put squared brackets around transcription.
        :return: an approximate pronunciation (IPA)
        """

        if not punctuation:
            text = re.sub(r"[\.\";\,\:\[\]\(\)!&?‘]", "", text)

        text = re.sub(r"sch", "ʃ", text)
        text = re.sub(r"(?<=[aeiouäëöüâæœêîôû])h", "χ", text)
        text = re.sub(r"h(?=[aeiouäëöüâæœêîôû])", "χ", text)
        text = re.sub(r"(?<=[aeiouäëöüâæœêîôû])s(?=[aeiouäëöüâæœêîôû])", "z̥", text)
        text = re.sub(r"^s(?=[aeiouäëöüâæœêîôû])", "z̥", text)

        for w, val in zip(DIPHTHONGS_IPA.keys(), DIPHTHONGS_IPA.values()):
            text = text.replace(w, val)

        for w, val in zip(IPA.keys(), IPA.values()):
            text = text.replace(w, val)
        if with_squared_brackets:
            return "[" + text + "]"
        return text
