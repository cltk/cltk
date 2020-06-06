"""Noun declensions

This module intends to
- set inflected forms of Old Norse nouns,
- guess declined forms just with the nominative singular, the genitive singular and the nominative plural.

Old Norse nouns vary according to gender (masculine, feminine and neuter), the number (singular and plural) and the case
(nominative, accusative, dative and genitive). They are classified into the strong and the weak nouns.

All dative plural nouns finish with -um ending.
All genitive plural nouns finish with -a ending.

Commented doctests do not work as expected, because there is no way, for now, to guess correctly all the forms.

"""

import cltk.inflection.utils as decl_utils
from cltk.phonology.syllabify import Syllabifier, Syllable
from cltk.corpus.old_norse.syllabifier import invalid_onsets, BACK_TO_FRONT_VOWELS, VOWELS, CONSONANTS
from cltk.inflection.old_norse.phonemic_rules import extract_common_stem, apply_u_umlaut, has_u_umlaut

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

sumar = [["sumar", "sumar", "sumri", "sumars"], ["sumur", "sumur", "sumrum", "sumra"]]
noun_sumar = decl_utils.Noun("sumar", decl_utils.Gender.neuter)
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
        >>> armr = OldNorseNoun("armr", decl_utils.Gender.masculine)
        >>> armr.set_representative_cases("armr", "arms", "armar")
        >>> armr.get_representative_cases()
        ('armr', 'arms', 'armar')

        :return: nominative singular, genetive singular, nominative plural
        """
        return (self.get_declined(decl_utils.Case.nominative, decl_utils.Number.singular),
                self.get_declined(decl_utils.Case.genitive, decl_utils.Number.singular),
                self.get_declined(decl_utils.Case.nominative, decl_utils.Number.plural))


def decline_strong_masculine_noun(ns: str, gs: str, np: str):
    """
    Gives the full declension of strong masculine nouns.

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
    # ketill
    # ketil
    # katli
    # ketils
    # katlar
    # katla
    # kötlum
    # katla

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

    # >>> decline_strong_masculine_noun("skjöldr", "skjaldar", "skildir")
    # skjöldr
    # skjöld
    # skildi
    # skjaldar
    # skildir
    # skjöldu
    # skjöldum
    # skjalda
    #
    # >>> decline_strong_masculine_noun("völlr", "vallar", "vellir")
    # völlr
    # völl
    # velli
    # vallar
    # vellir
    # völlu
    # völlum
    # valla
    #
    # >>> decline_strong_masculine_noun("fögnuðr", "fagnaðar", "fagnaðir")
    # fögnuðr
    # fögnuð
    # fagnaði
    # fagnaðar
    # fagnaðir
    # fögnuðu
    # fögnuðum
    # fagnaða

    a-stem
    armr, arm, armi, arms; armar, arma, örmum, arma
    ketill, ketil, katli, ketils; katlar, katla, kötlum, katla
    mór, mó, mó, mós; móar, móa, móm, móa
    hirðir, hirði, hirði, hirðis; hirðar, hirða, hirðum, hirða
    söngr, söng, söngvi, söngs; söngvar, söngva, söngvum, söngva

    i-stem
    gestr, gest, gest, gests; gestir, gesti, gestum, gesta
    staðr, stað stað, staðar; staðir, staði, stöðum, staða

    # u-stem
    # skjödr, skjöld, skildi, skjaldar; skildir, skjöldu, skjöldum, skjalda
    # völlr, völl, velli, vallar; vellir, völlu, völlum, valla
    # fögnuðr, fögnuð, fągnaði, fagnaðar; fagnaðir, fögnuðu, fögnuðum, fagnaða

    :param ns: nominative singular
    :param gs: genitive singular
    :param np: nominative plural
    :return:
    """
    np_syl = s.syllabify_ssp(np)

    last_np_syl = np_syl[-1]

    if last_np_syl.endswith("ar"):
        # a-stem
        common_stem = extract_common_stem(ns, gs, np)

        # nominative singular
        print(ns)

        # accusative singular
        print(common_stem)

        # dative singular
        if np[len(common_stem):][0] == "v":
            print(common_stem + "vi")
        else:
            print(common_stem + "i")

        # genitive singular
        print(gs)

        # nominative plural
        print(np)

        # accusative plural
        if last_np_syl.endswith("ar"):
            print(np[:-1])

        elif last_np_syl.endswith("ir"):
            print(np[:-1])

        # dative plural
        if np[len(common_stem):][0] == "v":
            print(apply_u_umlaut(common_stem) + "vum")

        elif np[len(common_stem):][0] == "j":
            print(apply_u_umlaut(common_stem) + "jum")
        else:
            print(apply_u_umlaut(common_stem) + "um")

        # genitive plural
        if np[len(common_stem):][0] == "v":
            print(common_stem + "va")
        elif np[len(common_stem):][0] == "j":
            print(common_stem + "ja")
        else:
            print(common_stem + "a")

    elif last_np_syl.endswith("ir"):
        # if has_u_umlaut(ns):
        #     # u-stem
        #     common_stem = ns[:-1]
        #
        #     # nominative singular
        #     print(ns)
        #
        #     # accusative singular
        #     print(common_stem)
        #
        #     # dative singular
        #     if np[len(common_stem):][0] == "v":
        #         print(common_stem + "vi")
        #     else:
        #         print(common_stem + "i")
        #
        #     # genitive singular
        #     print(gs)
        #
        #     common_stem_p = np[:-2]
        #     # nominative plural
        #     print(np)
        #
        #     # accusative plural
        #     print(apply_u_umlaut(common_stem_p)+"u")
        #
        #     # dative plural
        #     if np[len(common_stem):][0] == "v":
        #         print(apply_u_umlaut(common_stem_p) + "vum")
        #
        #     elif np[len(common_stem):][0] == "j":
        #         print(apply_u_umlaut(common_stem_p) + "jum")
        #     else:
        #         print(apply_u_umlaut(common_stem_p) + "um")
        #
        #     # genitive plural
        #     if np[len(common_stem):][0] == "v":
        #         print(common_stem_p + "va")
        #     elif np[len(common_stem):][0] == "j":
        #         print(common_stem_p + "ja")
        #     else:
        #         print(common_stem_p + "a")
        # else:

        # i-stem
        common_stem = extract_common_stem(ns, gs, np)

        # nominative singular
        print(ns)

        # accusative singular
        print(common_stem)

        # dative singular
        if np[len(common_stem):][0] == "v":
            print(common_stem + "vi")
        else:
            print(common_stem + "i")

        # genitive singular
        print(gs)

        # nominative plural
        print(np)

        # accusative plural
        print(np[:-1])

        # dative plural
        if np[len(common_stem):][0] == "v":
            print(apply_u_umlaut(common_stem) + "vum")

        elif np[len(common_stem):][0] == "j":
            print(apply_u_umlaut(common_stem) + "jum")
        else:
            print(apply_u_umlaut(common_stem) + "um")

        # genitive plural
        if np[len(common_stem):][0] == "v":
            print(common_stem + "va")
        elif np[len(common_stem):][0] == "j":
            print(common_stem + "ja")
        else:
            print(common_stem + "a")


def decline_strong_feminine_noun(ns: str, gs: str, np: str):
    """
    Gives the full declension of strong feminine nouns.

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
    Gives the full declension of strong neuter nouns.

    a-stem
    Most of strong neuter nouns follow the declensions of skip, land and herað.

    >>> decline_strong_neuter_noun("skip", "skips", "skip")
    skip
    skip
    skipi
    skips
    skip
    skip
    skipum
    skipa

    >>> decline_strong_neuter_noun("land", "lands", "lönd")
    land
    land
    landi
    lands
    lönd
    lönd
    löndum
    landa

    >>> decline_strong_neuter_noun("herað", "heraðs", "heruð")
    herað
    herað
    heraði
    heraðs
    heruð
    heruð
    heruðum
    heraða

    # >>> decline_strong_neuter_noun("kyn", "kyns", "kyn")
    # kyn
    # kyn
    # kyni
    # kyns
    # kyn
    # kyn
    # kynjum
    # kynja
    #
    # >>> decline_strong_neuter_noun("högg", "höggs", "högg")
    # högg
    # högg
    # höggvi
    # höggs
    # högg
    # högg
    # höggum
    # höggva

    >>> decline_strong_neuter_noun("kvæði", "kvæðis", "kvæði")
    kvæði
    kvæði
    kvæði
    kvæðis
    kvæði
    kvæði
    kvæðum
    kvæða

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
    if ns[-1] == "i":
        print(ns)
    # TODO  +"vi"
    else:
        print(ns+"i")

    # genitive singular
    print(gs)

    # nominative plural
    print(np)

    # accusative plural
    print(np)

    # dative plural
    if ns[-1] in CONSONANTS:
        print(apply_u_umlaut(np)+"um")
    else:
        print(apply_u_umlaut(np[:-1]) + "um")
    # TODO +"vum"

    # genitive plural
    if ns[-1] in CONSONANTS:
        print(ns+"a")
    # TODO + "va"
    else:
        print(ns[:-1]+"a")


def decline_weak_masculine_noun(ns: str, gs: str, np: str):
    """
    Gives the full declension of weak masculine nouns.

    >>> decline_weak_masculine_noun("goði", "goða", "goðar")
    goði
    goða
    goða
    goða
    goðar
    goða
    goðum
    goða

    >>> decline_weak_masculine_noun("hluti", "hluta", "hlutar")
    hluti
    hluta
    hluta
    hluta
    hlutar
    hluta
    hlutum
    hluta

    >>> decline_weak_masculine_noun("arfi", "arfa", "arfar")
    arfi
    arfa
    arfa
    arfa
    arfar
    arfa
    örfum
    arfa

    >>> decline_weak_masculine_noun("bryti", "bryta", "brytjar")
    bryti
    bryta
    bryta
    bryta
    brytjar
    brytja
    brytjum
    brytja

    >>> decline_weak_masculine_noun("vöðvi", "vöðva", "vöðvar")
    vöðvi
    vöðva
    vöðva
    vöðva
    vöðvar
    vöðva
    vöðum
    vöðva

    The main pattern is:

    :param ns: nominative singular
    :param gs: genitive singular
    :param np: nominative plural
    :return:
    """
    # nominative singular
    print(ns)

    # accusative singular
    print(gs)

    # dative singular
    print(gs)

    # genitive singular
    print(gs)

    # nominative plural
    print(np)

    # accusative plural
    print(np[:-1])

    # dative plural
    if len(np) > 3 and np[-3] == "v":
        print(apply_u_umlaut(np[:-3]) + "um")
    else:
        print(apply_u_umlaut(np[:-2]) + "um")

    # genitive plural
    print(np[:-1])


def decline_weak_feminine_noun(ns: str, gs: str, np: str):
    """
    Gives the full declension of weak feminine nouns.

    >>> decline_weak_feminine_noun("saga", "sögu", "sögur")
    saga
    sögu
    sögu
    sögu
    sögur
    sögur
    sögum
    sagna

    >>> decline_weak_feminine_noun("kona", "konu", "konur")
    kona
    konu
    konu
    konu
    konur
    konur
    konum
    kvenna

    >>> decline_weak_feminine_noun("kirkja", "kirkju", "kirkjur")
    kirkja
    kirkju
    kirkju
    kirkju
    kirkjur
    kirkjur
    kirkjum
    kirkna


    >>> decline_weak_feminine_noun("völva", "völu", "völur")
    völva
    völu
    völu
    völu
    völur
    völur
    völum
    völna

    >>> decline_weak_feminine_noun("speki", "speki", "")
    speki
    speki
    speki
    speki

    >>> decline_weak_feminine_noun("reiði", "reiði", "")
    reiði
    reiði
    reiði
    reiði

    >>> decline_weak_feminine_noun("elli", "elli", "")
    elli
    elli
    elli
    elli

    >>> decline_weak_feminine_noun("frœði", "frœði", "")
    frœði
    frœði
    frœði
    frœði

    It is to note that the genitive plural of völva is not attested so the given form is analogously reconstructed.

    The main pattern is:
    -a
    -u
    -u
    -u
    -ur
    -ur
    -um
    -na

    :param ns: nominative singular
    :param gs: genitive singular
    :param np: nominative plural
    :return:
    """

    if ns[-1] == "i" and gs[-1] == "i" and not np:
        print(ns)
        print(ns)
        print(ns)
        print(ns)
    else:

        # nominative singular
        print(ns)

        # accusative singular
        print(gs)

        # dative singular
        print(gs)

        # genitive singular
        print(gs)

        # nominative plural
        print(np)

        # accusative plural
        print(np)

        # dative plural
        print(np[:-1]+"m")

        # genitive plural
        if ns == "kona":
            print("kvenna")
        elif ns[-2] == "v" or ns[-2] == "j":
            print(ns[:-2]+"na")
        else:
            print(ns[:-1]+"na")


def decline_weak_neuter_noun(ns: str, gs: str, np: str):
    """
    Gives the full declension of weak neuter nouns.

    >>> decline_weak_neuter_noun("auga", "auga", "augu")
    auga
    auga
    auga
    auga
    augu
    augu
    augum
    augna

    >>> decline_weak_neuter_noun("hjarta", "hjarta", "hjörtu")
    hjarta
    hjarta
    hjarta
    hjarta
    hjörtu
    hjörtu
    hjörtum
    hjartna

    >>> decline_weak_neuter_noun("lunga", "lunga", "lungu")
    lunga
    lunga
    lunga
    lunga
    lungu
    lungu
    lungum
    lungna

    >>> decline_weak_neuter_noun("eyra", "eyra", "eyru")
    eyra
    eyra
    eyra
    eyra
    eyru
    eyru
    eyrum
    eyrna

    The main pattern is:
    -a
    -a
    -a
    -a
    -u
    -u
    -um
    -na

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
    print(ns)

    # genitive singular
    print(gs)

    # nominative plural
    print(np)

    # accusative plural
    print(np)

    # dative plural
    print(np+"m")

    # genitive plural
    print(ns[:-1]+"na")
