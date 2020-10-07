"""Ancient Greek phonology tools

"""
import unicodedata
from typing import List

import cltk.phonology.grc.transcription as gret

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class GreekTranscription:
    """Ancient Greek transcriber"""

    def __init__(self):
        self.transcriber = gret.Transcriber("Attic", "Probert")

    def transcribe(self, word: str) -> str:
        """

        :param word: word to transcribe
        :return: transcribed word
        """
        return self.transcriber.transcribe(unicodedata.normalize("NFC", word))[1:-1]

    def __repr__(self):
        return f"<GreekTranscription>"

    def __call__(self, word: str) -> str:
        return self.transcribe(word)


class GreekSyllabifier:
    def __init__(self):
        self.transcriber = gret.Transcriber("Attic", "Probert")

    def syllabify(self, word: str) -> List[str]:
        """
        >>> GreekTranscription().transcribe("Ὀδύσσεια")
        'o.dýs.sẹː.ɑ'

        :param word: word to syllabify
        :return: syllabified word
        """
        return gret.Word(
            self.transcriber.transcribe(word), gret.GREEK["Attic"]["Probert"]
        ).syllabify()

    def __repr__(self):
        return f"<GreekSyllabifier>"

    def __call__(self, word: str) -> List[str]:
        return self.syllabify(word)
