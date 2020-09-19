"""Old Englih phonology tools

Sources:
    https://en.wikipedia.org/wiki/Old_English_phonology
    Hogg, Richard M. (1992). The Cambridge History of the English Language. Chapter 3
"""
from typing import List

from cltk.phonology.ang.transcription import Transcriber
from cltk.phonology.syllabify import Syllabifier

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class OldEnglishTranscription:
    """
    Old English transcriber
    """

    def __init__(self):
        self.transcriber = Transcriber()

    def transcribe(self, word):
        """
        >>> ang_transriber = OldEnglishTranscription()
        >>> ang_transriber.transcribe("Bēowulf")
        'beːowuɫf'

        :param word: word to transcribe
        :return: transcribed word
        """
        return self.transcriber.transcribe(word, with_squared_brackets=False)

    def __repr__(self):
        return f"<OldEnglishTranscription>"

    def __call__(self, word):
        return self.transcribe(word)


class OldEnglishSyllabifier:
    """
    Old English syllabifier
    """

    def __init__(self):
        self.syllabifier = Syllabifier(language="ang")

    def syllabify(self, word: str) -> List[str]:
        """
        >>> ang_syllabifier = OldEnglishSyllabifier()
        >>> ang_syllabifier.syllabify("Beowulf".lower())
        ['beo', 'wulf']

        :param word: word to syllabify
        :return: syllabified word
        """
        return self.syllabifier.syllabify(word)

    def __repr__(self):
        return f"<OldEnglishSyllabifier>"

    def __call__(self, word):
        return self.syllabify(word)
