"""

"""
import unicodedata

import cltk.phonology.grc.transcription as gret

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class GreekTranscription:
    def __init__(self):
        self.transcriber = gret.Transcriber("Attic", "Probert")

    def transcribe(self, word):
        return self.transcriber.transcribe(unicodedata.normalize("NFC", word))[1:-1]

    def __repr__(self):
        return f"<GreekTranscription>"

    def __call__(self, word):
        return self.transcribe(word)


class GreekSyllabifier:
    def __init__(self):
        self.transcriber = gret.Transcriber("Attic", "Probert")

    def transcribe(self, word):
        return gret.Word(
            self.transcriber.transcribe(word), gret.GREEK["Attic"]["Probert"]
        ).syllabify()

    def __repr__(self):
        return f"<GreekSyllabifier>"

    def __call__(self, word):
        return self.transcribe(word)
