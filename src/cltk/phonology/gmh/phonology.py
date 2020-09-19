"""Middle High German phonology tools
"""
from typing import List

from cltk.phonology.gmh.transcription import Transcriber
from cltk.phonology.syllabify import Syllabifier

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class MiddleHighGermanTranscription:
    """
    Middle High German Transcriber
    """

    def __init__(self):
        self.transcriber = Transcriber()

    def transcribe(self, word):
        """
        >>> MiddleHighGermanTranscription().transcribe("Brynhild")
        'Brynχɪld̥'

        :param word: word to transcribe
        :return: transcribed word
        """
        return self.transcriber.transcribe(word, with_squared_brackets=False)

    def __repr__(self):
        return f"<MiddleHighGermanTranscription>"

    def __call__(self, word):
        return self.transcribe(word)


class MiddleHighGermanSyllabifier:
    """
    Middle High German syllabifier based on sonority phoneme hierarchy for MHG.
    Source: Resonances in Middle High German: New Methodologies in Prosody, Christopher Leo Hench, 2017
    """

    def __init__(self):
        self.syllabifier = Syllabifier(language="gmh")

    def syllabify(self, word: str) -> List[str]:
        """
        >>> MiddleHighGermanSyllabifier().syllabify("Gunther")
        ['Gunt', 'her']

        :param word: word to syllabify
        :return: syllabified word
        """
        return self.syllabifier.syllabify(word, mode="MOP")

    def __repr__(self):
        return f"<MiddleHighGermanSyllabifier>"

    def __call__(self, word):
        return self.syllabify(word)
