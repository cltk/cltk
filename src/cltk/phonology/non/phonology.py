"""


"""
from typing import List

from cltk.phonology.non import syllabifier as ons
from cltk.phonology.non import transcription as ont
from cltk.phonology.non import utils as ut
from cltk.phonology.syllabify import Syllabifier

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class OldNorseTranscription:
    """
    Phonological transcriber for Old Norse
    """

    def __init__(self):
        self.transcriber = ut.Transcriber(
            ont.DIPHTHONGS_IPA,
            ont.DIPHTHONGS_IPA_class,
            ont.IPA_class,
            ont.old_norse_rules,
        )

    def transcribe(self, word: str) -> str:
        """
        >>> non_transcriber = OldNorseTranscription()
        >>> non_transcriber.transcribe("Óðinn")
        '[oːðinː]'

        :param word: word to transcribe
        :return: transcribed word
        """
        return self.transcriber.text_to_phonetic_representation(word)

    def __repr__(self):
        return f"<OldNorseTranscription>"

    def __call__(self, word: str) -> str:
        return self.transcribe(word)


class OldNorseSyllabifier:
    """
    Syllabifier for Old Norse
    """

    def __init__(self):
        self.syllabifier = Syllabifier(language="non", break_geminants=True)

        self.syllabifier.set_invalid_onsets(ons.invalid_onsets)

    def syllabify(self, word: str) -> List[str]:
        """
        >>> non_syllabifier = OldNorseSyllabifier()
        >>> non_syllabifier.syllabify('Miðgarðr'.lower())
        ['mið', 'garðr']

        :param word: word to syllabify
        :return: syllabified word
        """
        return self.syllabifier.syllabify(word)

    def __repr__(self):
        return f"<OldNorseScanner>"

    def __call__(self, word: str) -> List[str]:
        return self.syllabify(word)
