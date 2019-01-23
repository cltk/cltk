"""Noun declensions"""

import cltk.inflection.utils as decl_utils
from cltk.phonology.syllabify import Syllabifier
from cltk.corpus.old_norse.syllabifier import invalid_onsets, VOWELS, CONSONANTS, SHORT_VOWELS, LONG_VOWELS, DIPHTHONGS
from cltk.inflection.old_norse.phonemic_rules import extract_common_stem

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

sumar = [["sumar", "sumar", "sumri", "sumars"], ["sumur", "sumur", "sumrum", "sumra"]]
noun_sumar = decl_utils.DeclinableOneGender("sumar", decl_utils.Gender.neuter)
noun_sumar.set_declension(sumar)

s = Syllabifier(language="old_norse", break_geminants=True)
s.set_invalid_onsets(invalid_onsets)


class OldNorseNoun(decl_utils.Noun):
    def __init__(self, name: str, gender: decl_utils.Gender):

        super().__init__(name, gender)

    def set_representative_cases(self, ns, gs, np):
        """
        >>> armr = OldNorseNoun("armr", decl_utils.Gender.masculine)
        >>> armr.set_representative_cases("armr", "arms", "armar")
        >>> armr.get_representative_cases()
        ('armr', 'arms', 'armar')

        >>> armr.declension
        [['armr', '', '', 'arms'], ['armar', '', '', '']]

        :param ns:
        :param gs:
        :param np:
        :return:
        """
        self.set_void_declension(decl_utils.Number, decl_utils.Case)
        self.declension[decl_utils.Number.singular.value-1][decl_utils.Case.nominative.value-1] = ns
        self.declension[decl_utils.Number.singular.value-1][decl_utils.Case.genitive.value-1] = gs
        self.declension[decl_utils.Number.plural.value-1][decl_utils.Case.nominative.value-1] = np

    def get_representative_cases(self):
        """

        :return: nominative singular, genetive singular, nominative plural
        """
        return (self.get_declined(decl_utils.Case.nominative, decl_utils.Number.singular),
                self.get_declined(decl_utils.Case.genitive, decl_utils.Number.singular),
                self.get_declined(decl_utils.Case.nominative, decl_utils.Number.plural))


def ns_has_i_umlaut(ns: str, gs: str, np: str):
    """

    :param ns:
    :param gs:
    :param np:
    :return:
    """
    return False


def decline_strong_masculine_noun(ns: str, gs: str, np: str):
    """
    >>> decline_strong_masculine_noun("armr", "arms", "armar")
    armr
    arm
    armi
    arms
    armar
    arma
    örmum
    arma

    >>> decline_strong_masculine_noun("ketill", "ketils", "katlar")
    ketill
    ketil
    katli
    ketils
    katlar
    katla
    kötlum
    katla

    >>> decline_strong_masculine_noun("mór", "mós", "móar")
    mór
    mó
    mói
    mós
    móar
    móa
    móum
    móa

    >>> decline_strong_masculine_noun("hirðir", "hirðis", "hirðar")
    hirðir
    hirð
    hirði
    hirðis
    hirðar
    hirða
    hirðum
    hirða

    >>> decline_strong_masculine_noun("söngr", "söngs", "söngvar")
    söngr
    söng
    söngvi
    söngs
    söngvar
    söngva
    söngvum
    söngva

    >>> decline_strong_masculine_noun("gestr", "gests", "gestir")
    gestr
    gest
    gesti
    gests
    gestir
    gesti
    gestum
    gesta

    >>> decline_strong_masculine_noun("staðr", "staðar", "staðir")
    staðr
    stað
    staði
    staðar
    staðir
    staði
    staðum
    staða

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
    common_stem = extract_common_stem(ns, gs, np)

    # nominative singular
    print(ns)

    # accusative singular
    print(common_stem)

    # dative singular
    if np[len(common_stem):][0] == "v":
        print(common_stem+"vi")
    else:
        print(common_stem+"i")

    # genitive singular
    print(gs)

    # nominative plural
    print(np)

    # accusative plural
    # if np[len(common_stem):][0] in ["v", "j"]:
    #     print(gs)

    if last_np_syl.endswith("ar"):
        # print("a-stem")
        print(np[:-1])

    elif last_np_syl.endswith("ir"):
        # print("i-stem")
        print(np[:-1])

    elif last_np_syl.endswith("ur"):
        # print("u-stem")
        print(np[:-1])

    # dative plural
    if np[len(common_stem):][0] == "v":
        print(common_stem+"vum")

    elif np[len(common_stem):][0] == "j":
        print(common_stem+"jum")
    else:
        print(common_stem + "um")

    # genitive plural

    if np[len(common_stem):][0] == "v":
        print(common_stem+"va")
    elif np[len(common_stem):][0] == "j":
        print(common_stem+"ja")
    else:
        print(common_stem + "a")


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

