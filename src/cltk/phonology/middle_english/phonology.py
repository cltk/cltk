"""

"""

# from cltk.phonology.orthophonology import Orthophonology
from cltk.phonology.syllabify import Syllabifier


__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class MiddleEnglishTranscription:
    def __init__(self):
        pass

    def transcribe(self, word):
        # TODO
        # transcriber = Orthophonology(sound_inventory, alphabet, diphthongs_ipa, digraphs_ipa)
        # transcriber = None
        # return transcriber.transcribe(word)
        return None

    def __repr__(self):
        return f"<OldSwedishTranscription>"

    def __call__(self, word):
        return self.transcribe(word)


class MiddleEnglishSyllabifier:
    def __init__(self):
        self.syllabifier = Syllabifier(language="enm")

    def syllabify(self, word):
        return self.syllabifier.syllabify(word)

    def __repr__(self):
        return f"<MiddleEnglishSyllabifier>"

    def __call__(self, word):
        return self.syllabify(word)
