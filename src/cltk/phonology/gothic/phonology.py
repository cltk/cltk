"""

"""

from cltk.phonology import utils as ut
import cltk.phonology.gothic.transcription as gt


__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class GothicTranscription:
    def __init__(self):
        self.transcriber = ut.Transcriber(
            gt.DIPHTHONGS_IPA,
            gt.DIPHTHONGS_IPA_class,
            gt.IPA_class,
            gt.gothic_rules,
        )

    def transcribe(self, word):
        return self.transcriber.text_to_phonemes(word)

    def __repr__(self):
        return f"<GothicTranscription>"

    def __call__(self, word):
        return self.transcribe(word)
