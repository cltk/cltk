"""Noun declensions"""

import cltk.inflection.utils as decl_utils
from cltk.phonology.syllabify import Syllabifier, Syllable
from cltk.corpus.old_norse.syllabifier import invalid_onsets, BACK_TO_FRONT_VOWELS, VOWELS, CONSONANTS
from cltk.inflection.old_norse.phonemic_rules import extract_common_stem, apply_u_umlaut

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
    >>> ns_has_i_umlaut("ketill", "ketils", "katlar")
    True
    >>> ns_has_i_umlaut("armr", "arms", "armar")
    False

    >>> ns_has_i_umlaut("mór", "mós", "móar")
    False

    >>> ns_has_i_umlaut("hirðir", "hirðis", "hirðar")
    False

    >>> ns_has_i_umlaut("söngr", "söngs", "söngvar")
    False

    >>> ns_has_i_umlaut("gestr", "gests", "gestir")
    False


    >>> ns_has_i_umlaut("staðr", "staðar", "staðir")

    :param ns:
    :param gs:
    :param np:
    :return:
    """

    ns_syl = s.syllabify_ssp(ns)
    gs_syl = s.syllabify_ssp(gs)
    np_syl = s.syllabify_ssp(np)
    s_ns_syl = [Syllable(syl, VOWELS, CONSONANTS) for syl in ns_syl]
    s_gs_syl = [Syllable(syl, VOWELS, CONSONANTS) for syl in gs_syl]
    s_np_syl = [Syllable(syl, VOWELS, CONSONANTS) for syl in np_syl]
    if len(gs_syl) >= 2 and s_gs_syl[-1].nucleus[0] == "i":
        if len(ns_syl) >= 2:
            vowel = s_ns_syl[-2].nucleus[0]
        else:
            vowel = s_ns_syl[-1].nucleus[0]
        return vowel in BACK_TO_FRONT_VOWELS and s_gs_syl[-2].nucleus[0] == BACK_TO_FRONT_VOWELS[vowel]

    if len(np_syl) >= 2 and s_np_syl[-1].nucleus[0] == "i":
        if len(ns_syl) >= 2:
            vowel = s_ns_syl[-2].nucleus[0]
        else:
            vowel = s_ns_syl[-1].nucleus[0]
        return vowel in BACK_TO_FRONT_VOWELS and s_np_syl[-2].nucleus[0] in BACK_TO_FRONT_VOWELS[vowel]

    return False


ns_has_i_umlaut("ketill", "ketils", "katlar")


def has_u_umlaut(word):
    """

    :param word:
    :return:
    """
    word_syl = s.syllabify_ssp(word)
    s_word_syl = [Syllable(syl, VOWELS, CONSONANTS) for syl in word_syl]

    if len(s_word_syl) == 1 and s_word_syl[-1].nucleus[0] in ["ö", "ǫ"]:
        return True
    elif len(s_word_syl) >= 2 and s_word_syl[-1].nucleus[0] == "u":
        return s_word_syl[-2].nucleus[0] in ["ö", "ǫ"]
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

    # >>> decline_strong_masculine_noun("ketill", "ketils", "katlar")
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
    stöðum
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
    ns_syl = s.syllabify_ssp(ns)
    gs_syl = s.syllabify_ssp(gs)
    np_syl = s.syllabify_ssp(np)
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
        print(apply_u_umlaut(common_stem)+"vum")

    elif np[len(common_stem):][0] == "j":
        print(apply_u_umlaut(common_stem)+"jum")
    else:
        print(apply_u_umlaut(common_stem)+"um")

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
    Most of strong feminine nouns follows the declension of rún and för.
    >>> decline_strong_feminine_noun("rún", "rúnar", "rúnar")
    rún
    rún
    rún
    rúnar
    rúnar
    rúnar
    rúnum
    rúna

    >>> decline_strong_feminine_noun("för", "farar", "farar")
    för
    för
    för
    farar
    farar
    farar
    förum
    fara

    >>> decline_strong_feminine_noun("kerling", "kerlingar", "kerlingar")
    kerling
    kerling
    kerlingu
    kerlingar
    kerlingar
    kerlingar
    kerlingum
    kerlinga

    >>> decline_strong_feminine_noun("skel", "skeljar", "skeljar")
    skel
    skel
    skel
    skeljar
    skeljar
    skeljar
    skeljum
    skelja

    >>> decline_strong_feminine_noun("ör", "örvar", "örvar")
    ör
    ör
    ör
    örvar
    örvar
    örvar
    örum
    örva

    >>> decline_strong_feminine_noun("heiðr", "heiðar", "heiðar")
    heiðr
    heiði
    heiði
    heiðar
    heiðar
    heiðar
    heiðum
    heiða

    i-stem

    >>> decline_strong_feminine_noun("öxl", "axlar", "axlir")
    öxl
    öxl
    öxl
    axlar
    axlir
    axlir
    öxlum
    axla

    >>> decline_strong_feminine_noun("höfn", "hafnar", "hafnir")
    höfn
    höfn
    höfn
    hafnar
    hafnir
    hafnir
    höfnum
    hafna

    >>> decline_strong_feminine_noun("norn", "nornar", "nornir")
    norn
    norn
    norn
    nornar
    nornir
    nornir
    nornum
    norna

    >>> decline_strong_feminine_noun("jörð", "jarðar", "jarðir")
    jörð
    jörð
    jörð
    jarðar
    jarðir
    jarðir
    jörðum
    jarða

    >>> decline_strong_feminine_noun("borg", "borgar", "borgir")
    borg
    borg
    borgu
    borgar
    borgir
    borgir
    borgum
    borga

    :param ns: nominative singular
    :param gs: genitive singular
    :param np: nominative plural
    :return:
    """

    # nominative singular
    print(ns)

    # accusative singular
    if len(ns) > 2 and ns[-1] == "r" and ns[-2] in CONSONANTS:
        print(ns[:-1]+"i")

    else:
        print(ns)

    # dative singular
    if len(ns) > 2 and ns[-1] == "r" and ns[-2] in CONSONANTS:
        print(ns[:-1]+"i")
    elif ns.endswith("ing") or ns.endswith("rg"):
        print(ns + "u")
    else:
        print(ns)

    # genitive singular
    print(gs)

    # nominative plural
    print(np)

    # accusative plural
    print(np)

    # dative plural
    # print("dative plural "+np[len(np[:-3]):][0])
    if np[len(np[:-3]):][0] == "v":
        print(apply_u_umlaut(np[:-2])[:-1]+"um")

    elif np[len(np[:-3]):][0] == "j":
        print(apply_u_umlaut(np[:-2])+"um")
    else:
        print(apply_u_umlaut(np[:-2])+"um")

    # genitive plural
    print(np[:-2]+"a")


def decline_strong_neuter_noun(ns: str, gs: str, np: str):
    """

    a-stem
    Most of strong neuter nouns follow the declensions of skip, land and herað.

    >>> decline_strong_neuter_noun("skip", "skips", "skip")
    'skip'
    'skip'
    'skipi'
    'skips'
    'skip'
    'skipum'
    'skipa'

    >>> decline_strong_neuter_noun("land", "lands", "lönd")
    'land'
    'land'
    'landi'
    'lands'
    'lönd'
    'lönd'
    'löndum'
    'landa'

    >>> decline_strong_neuter_noun("herað", "heraðs", "heruð")
    'herað'
    'herað'
    'heraði'
    'heraðs'
    'heruð'
    'heruð'
    'heruðum'
    'heraða'

    >>> decline_strong_neuter_noun("kyn", "kyns", "kyn")
    'kyn'
    'kyn'
    'kyni'
    'kyns'
    'kyn'
    'kyn'
    'kynjum'
    'kynja'

    >>> decline_strong_neuter_noun("högg", "höggs", "högg")
    'högg'
    'högg'
    'höggvi'
    'höggs'
    'högg'
    'högg'
    'höggum'
    'höggva'

    >>> decline_strong_neuter_noun("kvæði", "kvæðis", "kvæði")
    'kvæði'
    'kvæði'
    'kvæði'
    'kvæðis'
    'kvæði'
    'kvæði'
    'kvæðum'
    'kvæða'

    :param ns: nominative singular
    :param gs: genitive singular
    :param np: nominative plural
    :return:
    """

    # nominative singular
    print(ns)

    # accusative singular
    print(ns)

    # dative singular

    # genitive singular
    print(gs)

    # nominative plural
    print(np)

    # accusative plural
    print(np)

    # dative plural
    print(np)

    # genitive plural


def decline_weak_masculine_noun(ns: str, gs: str, np: str):
    """

    >>> decline_weak_masculine_noun("goði", "goða", "goðar")
    'goði'
    'goða'
    'goða'
    'goða'
    'goðar'
    'goða'
    'goðum'
    'goða'

    >>> decline_weak_masculine_noun("hluti", "hluta", "hlutar")
    'hluti'
    'hluta'
    'hluta'
    'hluta'
    'hlutar'
    'hluta'
    'hlutum'
    'hluta'

    >>> decline_weak_masculine_noun("arfi", "arfa", "arfar")
    'arfi'
    'arfa'
    'arfa'
    'arfa'
    'arfar'
    'arfa'
    'örfum'
    'arfa'

    >>> decline_weak_masculine_noun("bryti", "brytja", "brytjar")
    'bryti'
    'bryta'
    'bryta'
    'bryta'
    'brytjar'
    'brytja'
    'brytjum'
    'brytja'

    >>> decline_weak_masculine_noun("vöðvi", "vöðva", "vöðvar")
    'vöðvi'
    'vöðva'
    'vöðva'
    'vöðva'
    'vöðvar'
    'vöðva'
    'vöðum'
    'vöðva'

    :param ns:
    :param gs:
    :param np:
    :return:
    """
    # nominative singular
    print(ns)

    # accusative singular
    print(ns)

    # dative singular

    # genitive singular
    print(gs)

    # nominative plural
    print(np)

    # accusative plural

    # dative plural

    # genitive plural


def decline_weak_feminine_noun(ns: str, gs: str, np: str):
    """

    :param ns:
    :param gs:
    :param np:
    :return:
    """

    # nominative singular
    print(ns)

    # accusative singular
    print(ns)

    # dative singular

    # genitive singular
    print(gs)

    # nominative plural
    print(np)

    # accusative plural

    # dative plural

    # genitive plural


def decline_weak_neuter_noun(ns: str, gs: str, np: str):
    """

    :param ns:
    :param gs:
    :param np:
    :return:
    """
    # nominative singular
    print(ns)

    # accusative singular
    print(ns)

    # dative singular

    # genitive singular
    print(gs)

    # nominative plural
    print(np)

    # accusative plural

    # dative plural

    # genitive plural
