"""

"""

import cltk.phonology.got.transcription as gt
from cltk.phonology import utils as ut

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class GothicTranscription:
    def __init__(self):
        self.transcriber = ut.Transcriber(
            gt.DIPHTHONGS_IPA, gt.DIPHTHONGS_IPA_class, gt.IPA_class, gt.gothic_rules
        )

    def transcribe(self, word):
        return self.transcriber.text_to_phonetic_representation(
            word, with_squared_brackets=False
        )

    def __repr__(self):
        return f"<GothicTranscription>"

    def __call__(self, word):
        return self.transcribe(word)
