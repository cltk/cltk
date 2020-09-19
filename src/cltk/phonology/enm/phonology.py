"""Middle English phonology tools
"""
from typing import List

from cltk.phonology.syllabify import Syllabifier

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class MiddleEnglishSyllabifier:
    """
    Middle English syllabifier
    """

    def __init__(self):
        self.syllabifier = Syllabifier(language="enm")

    def syllabify(self, word: str) -> List[str]:
        return self.syllabifier.syllabify(word)

    def __repr__(self):
        return f"<MiddleEnglishSyllabifier>"

    def __call__(self, word: str) -> List[str]:
        return self.syllabify(word)
