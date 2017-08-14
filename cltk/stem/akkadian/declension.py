"""
Decline an Akkadian noun.
"""

__author__ = ['M. Willis Monroe <willismonroe@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

from cltk.stem.akkadian.stem import Stemmer
from cltk.stem.akkadian.stem import ENDINGS
from cltk.phonology.akkadian.stress import AKKADIAN


class NaiveDecliner(object):
    """Simple noun decliner"""

    def __init__(self):
        self.endings = ENDINGS
        self.akkadian = AKKADIAN
        self.stemmer = Stemmer()

    def decline_noun(self, noun, gender, mimation=True):
        """Return a list of all possible declined forms given any form
         of a noun and its gender."""
        stem = self.stemmer.get_stem(noun, gender)
        declension = []
        for case in self.endings[gender]['singular']:
            if gender == 'm':
                form = stem + self.endings[gender]['singular'][case]
            else:
                form = stem + self.endings[gender]['singular'][case][1:]
            declension.append((form, {'case': case, 'number': 'singular'}))
        for case in self.endings[gender]['dual']:
            if gender == 'm':
                form = stem + self.endings[gender]['dual'][case]
            else:
                form = stem + self.endings[gender]['dual'][case][1:]
            declension.append((form, {'case': case, 'number': 'dual'}))
        for case in self.endings[gender]['plural']:
            if gender == 'm':
                form = stem + self.endings[gender]['plural'][case]
            else:
                if stem[-3] in self.akkadian['macron_vowels']:
                    theme_vowel = stem[-3]
                else:
                    theme_vowel = 'ā'
                ending = [x for x in self.endings[gender]['plural'][case] if x[0] == theme_vowel]
                if stem[-2] in self.akkadian['short_vowels']:
                    form = stem[:-2] + ending[0]
                elif stem[-1] in self.akkadian['consonants'] and stem[-2] in self.akkadian['macron_vowels']:
                    form = stem + ending[0]
                else:
                    form = stem[:-1] + ending[0]
            declension.append((form, {'case': case, 'number': 'plural'}))
        return declension
