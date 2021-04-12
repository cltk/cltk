"""Latin phonology tools
"""
import unicodedata
from typing import List

import cltk.phonology.lat.transcription as latt
from cltk.phonology.lat.syllabifier import syllabify

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class LatinTranscription:
    """Latin transcriber"""

    def __init__(self):
        self.transcriber = latt.Transcriber("Classical", "Allen")

    def transcribe(self, word: str) -> str:
        """
        >>> LatinTranscription().transcribe("meditationes")
        '[mɛd̪ɪt̪at̪ɪ̣jɔn̪ɛs]'

        :param word: word to transcribe
        :return: transcribed word
        """
        return self.transcriber.transcribe(
            unicodedata.normalize("NFC", word), False, False, False
        )

    def __repr__(self):
        return f"<LatinTranscription>"

    def __call__(self, word: str) -> str:
        return self.transcribe(word)


class LatinSyllabifier:
    """Latin syllabifier"""

    def __init__(self):
        self.transcriber = latt.Transcriber("Classical", "Allen")

    def syllabify(self, word: str) -> List[str]:
        """
        >>> LatinSyllabifier().syllabify("relinquus")
        ['re', 'lin', 'qu', 'us']

        :param word: word to syllabify
        :return: syllabified word
        """
        return syllabify(word)

    def __repr__(self):
        return f"<LatinSyllabifier>"

    def __call__(self, word: str) -> List[str]:
        return self.syllabify(word)
