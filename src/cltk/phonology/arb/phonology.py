"""Arabic phonology tools
"""

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class ArabicTranscription:
    def __init__(self):
        pass

    def transcribe(self, word):
        # return transcribe(word)
        return None

    def __repr__(self):
        return f"<OldSwedishTranscription>"

    def __call__(self, word):
        return self.transcribe(word)
