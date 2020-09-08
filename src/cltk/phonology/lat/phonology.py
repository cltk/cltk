"""

"""

import unicodedata

import cltk.phonology.lat.transcription as latt
from cltk.phonology.lat.syllabifier import syllabify

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class LatinTranscription:
    def __init__(self):
        self.transcriber = latt.Transcriber("Classical", "Allen")

    def transcribe(self, word):

        return self.transcriber.transcribe(
            unicodedata.normalize("NFC", word), False, False, False
        )

    def __repr__(self):
        return f"<LatinTranscription>"

    def __call__(self, word):
        return self.transcribe(word)


class LatinSyllabifier:
    def __init__(self):
        self.transcriber = latt.Transcriber("Classical", "Allen")

    def syllabify(self, word):
        return syllabify(word)

    def __repr__(self):
        return f"<LatinSyllabifier>"

    def __call__(self, word):
        return self.syllabify(word)
