"""

"""

from cltk.phonology.gmh.transcription import Transcriber
from cltk.phonology.syllabify import Syllabifier


__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class MiddleHighGermanTranscription:
    def __init__(self):
        self.transcriber = Transcriber()

    def transcribe(self, word):
        return self.transcriber.transcribe(word, with_squared_brackets=False)

    def __repr__(self):
        return f"<MiddleHighGermanTranscription>"

    def __call__(self, word):
        return self.transcribe(word)


class MiddleHighGermanSyllabifier:
    def __init__(self):
        self.syllabifier = Syllabifier(language="gmh")

    def syllabify(self, word):
        return self.syllabifier.syllabify(word, mode="MOP")

    def __repr__(self):
        return f"<MiddleHighGermanSyllabifier>"

    def __call__(self, word):
        return self.syllabify(word)
