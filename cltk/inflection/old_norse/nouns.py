"""Noun declensions"""

import cltk.inflection.utils as decl_utils

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

sumar = [["sumar", "sumar", "sumri", "sumars"], ["sumur", "sumur", "sumrum", "sumra"]]
noun_sumar = decl_utils.DeclinableOneGender("sumar", decl_utils.Gender.neuter)
noun_sumar.set_declension(sumar)


def decline_strong_masculine_noun(word):
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



    :param word:
    :return:
    """
    pass


def decline_strong_feminine_noun(word):
    """
    o macron-stem



    i-stem


    :param word:
    :return:
    """
    pass


def decline_strong_neuter_noun(word):
    """
    a-stem
    :param word:
    :return:
    """
    pass


def decline_weak_masculine_noun(word):
    pass


def decline_weak_feminine_noun(word):
    pass


def decline_weak_neuter_noun(word):
    pass
