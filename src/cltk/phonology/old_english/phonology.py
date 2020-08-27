"""
Sources:
    https://en.wikipedia.org/wiki/Old_English_phonology
    Hogg, Richard M. (1992). The Cambridge History of the English Language. Chapter 3
"""

from cltk.phonology.old_english.transcription import Transcriber
from cltk.phonology.syllabify import Syllabifier

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class OldEnglishTranscription:
    def __init__(self):
        self.transcriber = Transcriber()

    def transcribe(self, word):
        return self.transcriber.transcribe(word)

    def __repr__(self):
        return f"<OldEnglishTranscription>"

    def __call__(self, word):
        return self.transcribe(word)


class OldEnglishSyllabifier:
    def __init__(self):
        self.syllabifier = Syllabifier(language="ang")

    def syllabify(self, word):
        return self.syllabifier.syllabify(word)

    def __repr__(self):
        return f"<OldEnglishSyllabifier>"

    def __call__(self, word):
        return self.syllabify(word)
