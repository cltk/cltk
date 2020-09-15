"""Middle English phonology tools

"""

from cltk.phonology.syllabify import Syllabifier

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class MiddleEnglishSyllabifier:
    def __init__(self):
        self.syllabifier = Syllabifier(language="enm")

    def syllabify(self, word):
        return self.syllabifier.syllabify(word)

    def __repr__(self):
        return f"<MiddleEnglishSyllabifier>"

    def __call__(self, word):
        return self.syllabify(word)
