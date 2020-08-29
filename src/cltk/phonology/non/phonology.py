"""


"""

from cltk.phonology import utils as ut
from cltk.phonology.non import syllabifier as ons
from cltk.phonology.non import transcription as ont
from cltk.phonology.syllabify import Syllabifier

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class OldNorseTranscription:
    def __init__(self):
        self.transcriber = ut.Transcriber(
            ont.DIPHTHONGS_IPA,
            ont.DIPHTHONGS_IPA_class,
            ont.IPA_class,
            ont.old_norse_rules,
        )

    def transcribe(self, word):
        return self.transcriber.text_to_phonetic_representation(word)

    def __repr__(self):
        return f"<OldNorseTranscription>"

    def __call__(self, word):
        return self.transcribe(word)


class OldNorseSyllabifier:
    def __init__(self):
        self.syllabifier = Syllabifier(language="non", break_geminants=True)

        self.syllabifier.set_invalid_onsets(ons.invalid_onsets)

    def syllabify(self, word):
        return self.syllabifier.syllabify(word)

    def __repr__(self):
        return f"<OldNorseScanner>"

    def __call__(self, word):
        return self.syllabify(word)
