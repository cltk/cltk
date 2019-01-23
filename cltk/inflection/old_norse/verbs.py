"""Verb inflection"""

import cltk.inflection.utils as decl_utils
from cltk.phonology.syllabify import Syllabifier
from cltk.corpus.old_norse.syllabifier import invalid_onsets, VOWELS, CONSONANTS, SHORT_VOWELS, LONG_VOWELS, DIPHTHONGS


__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

s = Syllabifier(language="old_norse", break_geminants=True)
s.set_invalid_onsets(invalid_onsets)


class OldNorseVerb:
    def __init__(self, inifinitive_form: str):
        self.inifinitive_form = inifinitive_form
        self.sfg3en = ""  # name of the variables come from the POS tag names
        self.sfg3fn = ""
        pass

    def set_basic_forms(self):
        pass


def add_t_ending_to_syllable(last_syllable):
    """

    >>> add_t_ending_to_syllable("batt")
    'bazt'
    >>> add_t_ending_to_syllable("gat")
    'gazt'
    >>> add_t_ending_to_syllable("varð")
    'vart'
    >>> add_t_ending_to_syllable("hélt")
    'hélt'
    >>> add_t_ending_to_syllable("réð")
    'rétt'
    >>> add_t_ending_to_syllable("laust")
    'laust'
    >>> add_t_ending_to_syllable("sá")
    'sátt'

    :param last_syllable:
    :return:
    """
    if len(last_syllable) >= 2:
        if last_syllable[-1] == 't':
            if last_syllable[-2] in VOWELS:
                # Apocope of r
                return last_syllable[:-1]+"zt"
            elif last_syllable[-2] == 't':
                return last_syllable[:-2]+"zt"
            elif last_syllable[-2] in ['r', 'l', 's']:
                return last_syllable
            else:
                return last_syllable + "t"
        elif last_syllable[-1] == 'ð':
            if last_syllable[-2] in ['r', 'l', 's']:
                return last_syllable[:-1] + "t"
            else:
                return last_syllable[:-1]+"tt"

        elif last_syllable[-1] == 'd':
            return last_syllable[:-1]+"t"
        elif last_syllable[-1] in LONG_VOWELS:
            return last_syllable + "tt"
        else:
            return last_syllable + "t"
    else:
        return last_syllable + "t"


def add_t_ending(stem: str):
    s_stem = s.syllabify_SSP(stem.lower())
    last_syllable = decl_utils.Syllable(s_stem[-1], VOWELS, CONSONANTS)
    return "".join(s_stem[:-1]) + add_t_ending_to_syllable(last_syllable.text)
