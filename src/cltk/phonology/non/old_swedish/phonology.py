"""

"""

from cltk.phonology import utils as ut
from cltk.phonology.non.old_swedish import transcription as old_swedish

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class OldSwedishTranscription:
    def __init__(self):
        self.transcriber = ut.Transcriber(
            old_swedish.DIPHTHONGS_IPA,
            old_swedish.DIPHTHONGS_IPA_class,
            old_swedish.IPA_class,
            old_swedish.old_swedish_rules,
        )

    def transcribe(self, word):
        return self.transcriber.text_to_phonemes(word)

    def __repr__(self):
        return f"<OldSwedishTranscription>"

    def __call__(self, word):
        return self.transcribe(word)
