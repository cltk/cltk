"""Gothic phonology tools
"""

import cltk.phonology.got.transcription as gt
from cltk.phonology.non import utils as ut

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class GothicTranscription:
    """Gothic transcriber"""

    def __init__(self):
        self.transcriber = ut.Transcriber(
            gt.DIPHTHONGS_IPA, gt.DIPHTHONGS_IPA_class, gt.IPA_class, gt.gothic_rules
        )

    def transcribe(self, word: str) -> str:
        """
        >>> got_transcriber = GothicTranscription()
        >>> got_transcriber.transcribe("anastodeins")
        'anastoːðiːns'

        :param word: word to transcribe
        :return: transcribed word
        """
        return self.transcriber.text_to_phonetic_representation(
            word, with_squared_brackets=False
        )

    def __repr__(self):
        return f"<GothicTranscription>"

    def __call__(self, word: str) -> str:
        return self.transcribe(word)
