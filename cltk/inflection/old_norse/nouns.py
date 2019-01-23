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


class OldNorseNoun(decl_utils.Noun):
    def __init__(self, name: str, gender: decl_utils.Gender):
        super().__init__(name, gender)

    def get_representative_cases(self):
        """

        :return: nominative singular, genetive singular, nominative plural
        """
        return (self.get_declined(decl_utils.Case.nominative, decl_utils.Number.singular),
                self.get_declined(decl_utils.Case.genitive, decl_utils.Number.singular),
                self.get_declined(decl_utils.Case.nominative, decl_utils.Number.plural))


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

