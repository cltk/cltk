"""Old Swedish transcriber
Provides a basic phonetic transcriber for Old Swedish.
"""

from cltk.phonology import utils as ut
from cltk.phonology.non.old_swedish import transcription as old_swedish

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class OldSwedishTranscription:
    """
    >>> text = "sigher hun oc hænnæ frændær".split(" ")
    >>> transcriber = OldSwedishTranscription()
    >>> [transcriber.transcribe(word) for word in text]
    ['siɣɛr', 'hun', 'ok', 'hɛnːɛ', 'frɛndɛr']

    """
    def __init__(self):
        self.transcriber = ut.Transcriber(
            old_swedish.DIPHTHONGS_IPA,
            old_swedish.DIPHTHONGS_IPA_class,
            old_swedish.IPA_class,
            old_swedish.old_swedish_rules,
        )

    def transcribe(self, word):
        return "".join([phoneme for phoneme in self.transcriber.word_to_phonetic_representation(word) if word])[1:-1]

    def __repr__(self):
        return f"<OldSwedishTranscription>"

    def __call__(self, word):
        return self.transcribe(word)
