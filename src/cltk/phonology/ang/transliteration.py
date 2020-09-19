"""
Transliteration module for Old English

Anglo-Saxon or Anglo-Frisian runes <-> Latin alphabet
"""

import logging

from cltk.core.exceptions import UnimplementedAlgorithmError
from cltk.phonology.ang.transcription import L_Transliteration, R_Transliteration

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class Transliterate:
    """
    Class that provides a transliteration method from Anglo-Saxon or Anglo-Frisian runic alphabet to Latin alphabet
    and vice versa.
    """

    def __init__(self):
        pass

    @staticmethod
    def transliterate(text, mode="Latin"):
        """
        Transliterates Anglo-Saxon runes into lat and vice versa.

        Sources:
            http://www.arild-hauge.com/eanglor.htm
            https://en.wikipedia.org/wiki/Anglo-Saxon_runes

        :param text: str: The text to be transcribed
        :param mode: Specifies transliteration mode, options:

            Latin (default): Transliterates Anglo-Saxon runes into the lat
            alphabet, using the Dickins system

            Anglo-Saxon/Anglo-Frisian : Transliterates Latin text into Anglo-Saxon runes

        Examples:

        >>> Transliterate().transliterate("Hƿæt Ƿe Gardena in geardagum", "Anglo-Saxon")
        'ᚻᚹᚫᛏ ᚹᛖ ᚷᚪᚱᛞᛖᚾᚪ ᛁᚾ ᚷᛠᚱᛞᚪᚷᚢᛗ'

        >>> Transliterate().transliterate("ᚩᚠᛏ ᛋᚳᚣᛚᛞ ᛋᚳᛖᚠᛁᛝ ᛋᚳᛠᚦᛖᚾᚪ ᚦᚱᛠᛏᚢᛗ", "Latin")
        'oft scyld scefin sceathena threatum'
        """
        if mode == "Latin":
            return Transliterate.__transliterate_helper(text, L_Transliteration)

        elif mode in ["Anglo-Saxon", "Anglo-Frisian"]:
            return Transliterate.__transliterate_helper(text, R_Transliteration)

        else:
            LOG.error("The specified mode is currently not supported")
            raise UnimplementedAlgorithmError(
                "The specified mode is currently not supported"
            )

    @staticmethod
    def __transliterate_helper(text, dicts):

        text = text.lower()
        for w, val in zip(dicts.keys(), dicts.values()):
            text = text.replace(w, val)

        return text
