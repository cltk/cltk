"""Noun declensions"""

import cltk.inflection.utils as decl_utils
from cltk.phonology.syllabify import Syllabifier
from cltk.corpus.old_norse.syllabifier import invalid_onsets, VOWELS, CONSONANTS, SHORT_VOWELS, LONG_VOWELS, DIPHTHONGS
__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

sumar = [["sumar", "sumar", "sumri", "sumars"], ["sumur", "sumur", "sumrum", "sumra"]]
noun_sumar = decl_utils.DeclinableOneGender("sumar", decl_utils.Gender.neuter)
noun_sumar.set_declension(sumar)

s = Syllabifier(language="old_norse", break_geminants=True)
s.set_invalid_onsets(invalid_onsets)


class Syllable:

    def __init__(self, text, vowels, consonants):
        self.onset = []
        self.nucleus = []
        self.coda = []
        self.text = text
        self.consonants = consonants
        self.vowels = vowels

        self._compute_syllable(text)

    def _compute_syllable(self, text):
        """
        >>> sylla = Syllable("armr", VOWELS, CONSONANTS)
        >>> sylla.onset
        []
        >>> sylla.nucleus
        ['a']
        >>> sylla.coda
        ['r', 'm', 'r']

        :param text:
        :return:
        """
        is_in_onset = True
        is_in_nucleus = False
        is_in_coda = False
        if len(text) > 0:
            for c in text:
                if is_in_onset and c in self.consonants:
                    self.onset.append(c)

                elif is_in_onset and c in self.vowels:
                    is_in_onset = False
                    is_in_nucleus = True
                    self.nucleus.append(c)

                elif is_in_nucleus and c in self.vowels:
                    self.nucleus.append(c)

                elif is_in_nucleus and c in self.consonants:
                    is_in_nucleus = False
                    is_in_coda = True
                    self.coda.append(c)

                elif is_in_coda and c in self.consonants:
                    self.coda.append(c)

                elif is_in_coda and c in self.vowels:
                    raise ValueError("This is not a correct syllable")

                else:
                    raise ValueError("{} is an unknown character".format(c))
        else:
            raise ValueError("A syllable can't be void")


def decline_strong_masculine_noun(ns: str, gs: str, np: str):
    """
    a-stem
    armr, arm, armi, arms; armar, arma, örmum, arma

    ketill, ketil, katli, ketils; katlar, katla, kötlum, katla

    mór, mó, mó, mós; móar, móa, móm, móa

    hirðir, hirði, hirði, hirðis; hirðar, hirða, hirðum, hirða

    söngr, söng, söngvi, söngs; söngvar, söngva, söngvum, söngva

    i-stem
    gestr, gest, gest, gests; gestir, gesti, gestum, gesta

    staðr, stað stað, staðar; staðir, staði, stöðum, staða


     u-stem



    :param ns: nominative singular
    :param gs: genitive singular
    :param np: nominative plural
    :return:
    """
    ns_syl = s.syllabify_SSP(ns)
    gs_syl = s.syllabify_SSP(gs)
    np_syl = s.syllabify_SSP(np)
    last_ns_syl = ns_syl[-1]
    last_gs_syl = gs_syl[-1]
    last_np_syl = np_syl[-1]

    if last_np_syl.endswith("ar"):
        print("a-stem")

    elif last_np_syl.endswith("ir"):
        print("i-stem")

    elif last_np_syl.endswith("ur"):
        print("u-stem")


def decline_strong_feminine_noun(ns: str, gs: str, np: str):
    """
    o macron-stem



    i-stem


    :param ns: nominative singular
    :param gs: genitive singular
    :param np: nominative plural
    :return:
    """
    pass


def decline_strong_neuter_noun(ns: str, gs: str, np: str):
    """
    a-stem

    :param ns: nominative singular
    :param gs: genitive singular
    :param np: nominative plural
    :return:
    """
    pass


def decline_weak_masculine_noun(ns: str, gs: str, np: str):
    """

    :param ns:
    :param gs:
    :param np:
    :return:
    """
    pass


def decline_weak_feminine_noun(ns: str, gs: str, np: str):
    """

    :param ns:
    :param gs:
    :param np:
    :return:
    """
    pass


def decline_weak_neuter_noun(ns: str, gs: str, np: str):
    """

    :param ns:
    :param gs:
    :param np:
    :return:
    """
    pass


def add_r(stem):
    """

    >>> add_r("arm")
    'armr'
    >>> add_r("ás")
    'áss'
    >>> add_r("stól")
    'stóll'

    :param stem:
    :return:
    """
    if len(stem) >= 2:
        if stem[-2] in CONSONANTS:
            if stem[-1] == "l":
                return stem + "l"
            elif stem[-1] == "s":
                return stem + "s"
            elif stem[-1] == "n":
                return stem + "n"
            return stem + "r"

    if len(stem) > 1:
        if stem[-1] == "l":
            return stem + "l"
        elif stem[-1] == "s":
            return stem + "s"
        elif stem[-1] == "n":
            return stem + "n"
        return stem + "r"

    else:
        return stem + "r"




# def apply_r_assimilation(stem):
#     s_stem = s.syllabify_SSP(stem)
#     n_stem = len(s_stem)
#     last_syllable = Syllable(s_stem[-1], VOWELS, CONSONANTS)
#     if n_stem == 1:
#         if "".join(last_syllable.nucleus) in DIPHTHONGS:
#             return stem +
#         elif "".join(last_syllable.nucleus) in SHORT_VOWELS:
#
#         elif "".join(last_syllable.nucleus) in LONG_VOWELS:
#
#     else:
#         if "".join(last_syllable.nucleus) in DIPHTHONGS:
#
#         elif "".join(last_syllable.nucleus) in SHORT_VOWELS:
#
#         elif "".join(last_syllable.nucleus) in LONG_VOWELS:

