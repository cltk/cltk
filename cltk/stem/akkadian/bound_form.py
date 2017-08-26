"""
Return a the bound form of a normalized Akkadian noun.
"""

__author__ = ['M. Willis Monroe <willismonroe@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

from cltk.stem.akkadian.syllabifier import Syllabifier
from cltk.stem.akkadian.stem import Stemmer
from cltk.stem.akkadian.cv_pattern import CVPattern


class BoundForm(object):
    """
    Return the bound form of a noun, suitable for adding suffixed pronouns.
    """

    def __init__(self):
        self.syllabifier = Syllabifier()
        self.stemmer = Stemmer()
        self.cv_patterner = CVPattern()

    def get_bound_form(self, noun, gender):
        """Return bound form of nound, given its gender."""
        syllables = self.syllabifier.syllabify(noun)
        stem = self.stemmer.get_stem(noun, gender)
        cv_pattern = self.cv_patterner.get_cv_pattern(stem)
        # Based on Huehnergard Appendix 6.C.1: base in -VC
        if [letter[0] for letter in cv_pattern[-2:]] == ['V', 'C'] or stem in ['nakr']:
            # a. 2-syllable
            if len(syllables) > 2:
                # awīlum > awīl, nakrum > naker
                if stem in ['nakr']:
                    return 'naker'
                else:
                    return stem
            # b. 1-syllable
            elif len(syllables) > 1:
                # bēlum > bēl
                return stem
            # c. abum, aḫum
            if stem in ['ab', 'aḫ']:
                return stem + 'i'
        # Appendix 6.C.2: base in -C₁C₁
        if cv_pattern[-1][:2] == cv_pattern[-2][:2]:
            # a. 1-syllable
            if 3 > len(syllables) > 1:
                return stem + 'i'
            # b. 2-syllable, -tt
            if len(syllables) > 2 and cv_pattern[-1][2] + cv_pattern[-2][2] == 'tt':
                return stem + 'i'
            # c. 2-syllable, other
            if len(syllables) > 2:
                return stem[:-1]
        # Appendix 6.C.3: base in -C₁C₂, C₂ ≠ t, i.e. pVrs
        if cv_pattern[-1][0] == cv_pattern[-2][0] and cv_pattern[-1][1] != cv_pattern[-2][1]:
            return stem[:-1] + stem[1] + stem[-1]
        # Appendix 6.C.4: base in -Ct (fem.)
        if cv_pattern[-1][2] == 't' and cv_pattern[-2][0] == 'C':
            if len(syllables) > 2:
                return stem + 'i'
            # Need to deal with fem. Ptcpl. māḫirtum -> māḫirat
            if len(syllables) > 1:
                # These are case by case
                if stem in ['qīšt']:
                    return stem + 'i'
                if stem in ['mārt']:
                    return stem[:-1] + stem[1] + stem[-1]
                    # Appendix 6.C.5: base in -V
                    # Weak nouns...
