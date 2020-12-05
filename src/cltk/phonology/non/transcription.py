"""Old Norse transcription module. Sources:
- https://fr.wikipedia.org/wiki/%C3%89criture_du_vieux_norrois
- Altnordisches Elementarbuch by Friedrich Ranke and Dietrich Hofmann

"""

from typing import Union

from cltk.phonology.non.syllabifier import BACK_TO_FRONT_VOWELS
from cltk.phonology.non.utils import (
    AbstractConsonant,
    AbstractPosition,
    Backness,
    Consonant,
    Height,
    Length,
    Manner,
    Place,
    Rank,
    Rule,
    Vowel,
)

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class OldNorsePhonology(Vowel):
    """Class that applies position-dependent phonological transformation"""

    U_UMLAUT = {"a": "ö", "ö": "u"}

    @staticmethod
    def phonetic_i_umlaut(sound: Vowel) -> Vowel:
        """
        >>> umlaut_a = OldNorsePhonology.phonetic_i_umlaut(a)
        >>> umlaut_a.ipar
        'ɛ'

        >>> umlaut_au = OldNorsePhonology.phonetic_i_umlaut(DIPHTHONGS_IPA_class["au"])
        >>> umlaut_au.ipar
        'ɐy'

        :param sound: vowel
        :return: transformed vowel
        """
        if sound.is_equal(a):
            return ee
        elif sound.is_equal(a.lengthen()):
            return ee.lengthen()
        elif sound.is_equal(o):
            return oee
        elif sound.is_equal(o.lengthen()):
            return oee.lengthen()
        elif sound.is_equal(u):
            return y
        elif sound.is_equal(u.lengthen()):
            return y.lengthen()
        if sound.is_equal(DIPHTHONGS_IPA_class["au"]):
            return DIPHTHONGS_IPA_class["ey"]

    @staticmethod
    def orthographic_i_umlaut(sound: str) -> str:
        """
        >>> OldNorsePhonology.orthographic_i_umlaut("a")
        'e'
        >>> OldNorsePhonology.orthographic_i_umlaut("ý")
        'ý'

        :param sound: vowel
        :return: transformed vowel
        """
        if sound in BACK_TO_FRONT_VOWELS:
            return BACK_TO_FRONT_VOWELS[sound]
        else:
            return sound

    @staticmethod
    def phonetic_u_umlaut(sound: Vowel) -> Vowel:
        """
        >>> umlaut_a = OldNorsePhonology.phonetic_u_umlaut(a)
        >>> umlaut_a.ipar
        'ø'

        >>> umlaut_o = OldNorsePhonology.phonetic_u_umlaut(o)
        >>> umlaut_o.ipar
        'u'

        >>> umlaut_e = OldNorsePhonology.phonetic_u_umlaut(e)
        >>> umlaut_e.ipar
        'e'


        :param sound: vowel
        :return: transformed vowel
        """
        if sound.is_equal(a):
            return oee  # or oe
        elif sound.is_equal(o):
            return u
        else:
            return sound

    @staticmethod
    def orthographic_u_umlaut(sound: str) -> str:
        """
        >>> OldNorsePhonology.orthographic_u_umlaut("a")
        'ö'
        >>> OldNorsePhonology.orthographic_u_umlaut("e")
        'e'

        :param sound: a vowel
        :return: transformed vowel
        """
        if sound in OldNorsePhonology.U_UMLAUT:
            return OldNorsePhonology.U_UMLAUT[sound]
        else:
            return sound


a = Vowel(Height.open, Backness.front, False, Length.short, "a")
ee = Vowel(Height.open_mid, Backness.front, False, Length.short, "ɛ")
e = Vowel(Height.close_mid, Backness.front, False, Length.short, "e")
oee = Vowel(Height.close_mid, Backness.front, True, Length.short, "ø")
oe = Vowel(Height.open_mid, Backness.front, True, Length.short, "œ")
i = Vowel(Height.close, Backness.front, False, Length.short, "i")
y = Vowel(Height.close, Backness.front, True, Length.short, "y")
ao = Vowel(Height.open, Backness.back, True, Length.short, "ɒ")
oo = Vowel(Height.open_mid, Backness.back, True, Length.short, "ɔ")
o = Vowel(Height.close_mid, Backness.back, True, Length.short, "o")
u = Vowel(Height.close, Backness.back, True, Length.short, "u")

b = Consonant(Place.bilabial, Manner.stop, True, "b", False)
d = Consonant(Place.alveolar, Manner.stop, True, "d", False)
f = Consonant(Place.labio_dental, Manner.fricative, False, "f", False)
g = Consonant(Place.velar, Manner.stop, True, "g", False)
gh = Consonant(Place.velar, Manner.fricative, True, "ɣ", False)
h = Consonant(Place.glottal, Manner.fricative, False, "h", False)
j = Consonant(Place.palatal, Manner.fricative, True, "j", False)
k = Consonant(Place.velar, Manner.stop, False, "k", False)
l = Consonant(Place.alveolar, Manner.lateral, True, "l", False)
m = Consonant(Place.bilabial, Manner.nasal, True, "m", False)
n = Consonant(Place.labio_dental, Manner.nasal, True, "n", False)
p = Consonant(Place.bilabial, Manner.stop, False, "p", False)
r = Consonant(Place.alveolar, Manner.trill, True, "r", False)
s = Consonant(Place.alveolar, Manner.fricative, False, "s", False)
t = Consonant(Place.alveolar, Manner.stop, False, "t", False)
v = Consonant(Place.labio_dental, Manner.fricative, True, "v", False)
# θ = Consonant(Place.dental, Manner.frictative, False, "θ")
th = Consonant(Place.dental, Manner.fricative, False, "θ", False)
# ð = Consonant(Place.dental, Manner.frictative, True, "ð")
dh = Consonant(Place.dental, Manner.fricative, True, "ð", False)

OLD_NORSE_PHONOLOGY = [
    a,
    ee,
    e,
    oe,
    i,
    y,
    ao,
    oo,
    u,
    a.lengthen(),
    e.lengthen(),
    i.lengthen(),
    o.lengthen(),
    u.lengthen(),
    y.lengthen(),
    b,
    d,
    f,
    g,
    h,
    k,
    l,
    m,
    n,
    p,
    r,
    s,
    t,
    v,
    th,
    dh,
]

# IPA Dictionary
DIPHTHONGS_IPA = {"ey": "ɐy", "au": "ɒu", "øy": "ɐy", "ei": "ei"}  # Diphthongs
# Wrong diphthongs implementation but not that bad for now
DIPHTHONGS_IPA_class = {
    "ey": Vowel(Height.open, Backness.front, True, Length.long, "ɐy"),
    "au": Vowel(Height.open, Backness.back, True, Length.long, "ɒu"),
    "øy": Vowel(Height.open, Backness.front, True, Length.long, "ɐy"),
    "ei": Vowel(Height.open, Backness.front, True, Length.long, "ɛi"),
}
IPA = {
    "a": "a",  # Short vowels
    "e": "ɛ",
    "i": "i",
    "o": "ɔ",
    "ǫ": "ɒ",
    "ö": "ø",
    "ø": "ø",
    "u": "u",
    "y": "y",
    "á": "aː",  # Long vowels
    "æ": "ɛː",
    "œ": "œ:",
    "é": "eː",
    "í": "iː",
    "ó": "oː",
    "ú": "uː",
    "ý": "y:",
    # Consonants
    "b": "b",
    "d": "d",
    "f": "f",
    "g": "g",
    "h": "h",
    "j": "j",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "p": "p",
    "r": "r",
    "s": "s",
    "t": "t",
    "v": "v",
    "x": "ks",
    "z": "ts",
    "þ": "θ",
    "ð": "ð",
}
IPA_class = {
    "a": a,  # Short vowels
    "e": ee,
    "i": i,
    "o": oo,
    "ǫ": ao,
    "ø": oee,
    "u": u,
    "y": y,
    "á": a.lengthen(),  # Long vowels
    "æ": ee.lengthen(),
    "ö": oe,
    "œ": oe.lengthen(),
    "é": e.lengthen(),
    "í": i.lengthen(),
    "ó": o.lengthen(),
    "ú": u.lengthen(),
    "ý": y.lengthen(),
    # Consonants
    "b": b,
    "d": d,
    "f": f,
    "g": g,
    "h": h,
    "j": j,
    "k": k,
    "l": l,
    "m": m,
    "n": n,
    "p": p,
    "r": r,
    "s": s,
    "t": t,
    "v": v,
    "x": k + s,
    "z": t + s,
    "þ": th,
    "ð": dh,
}
GEMINATE_CONSONANTS = {
    "bb": "bː",
    "dd": "dː",
    "ff": "fː",
    "gg": "gː",
    "kk": "kː",
    "ll": "lː",
    "mm": "mː",
    "nn": "nː",
    "pp": "pː",
    "rr": "rː",
    "ss": "sː",
    "tt": "tː",
    "vv": "vː",
}

# Some Old Norse rules
# The first rule which matches is retained
rule_th = [
    Rule(AbstractPosition(Rank.first, None, []), th, th),
    Rule(AbstractPosition(Rank.inner, [], [AbstractConsonant(voiced=True)]), th, th),
    Rule(AbstractPosition(Rank.inner, [AbstractConsonant(voiced=True)], []), th, th),
    Rule(AbstractPosition(Rank.inner, [], []), th, dh),
    Rule(AbstractPosition(Rank.last, [], None), th, dh),
]

rule_f = [
    Rule(AbstractPosition(Rank.first, None, []), f, f),
    Rule(AbstractPosition(Rank.inner, [], [AbstractConsonant(voiced=False)]), f, f),
    Rule(AbstractPosition(Rank.inner, [AbstractConsonant(voiced=False)], []), f, f),
    Rule(AbstractPosition(Rank.inner, [], []), f, v),
    Rule(AbstractPosition(Rank.last, [], None), f, v),
]

rule_g = [
    Rule(AbstractPosition(Rank.first, None, None), g, g),
    Rule(AbstractPosition(Rank.inner, [n.to_abstract()], None), g, g),
    Rule(AbstractPosition(Rank.inner, None, [AbstractConsonant(voiced=False)]), g, k),
    Rule(AbstractPosition(Rank.inner, [], []), g, gh),
    Rule(AbstractPosition(Rank.last, [], None), g, gh),
]

old_norse_rules = []
old_norse_rules.extend(rule_f)
old_norse_rules.extend(rule_g)
old_norse_rules.extend(rule_th)


def measure_old_norse_syllable(syllable: list) -> Union[Length, None]:
    """
    Old Norse syllables are considered as:
    - short if
    - long if
    - overlong if

    >>> measure_old_norse_syllable([m, a.lengthen(), l]).name
    'long'

    >>> measure_old_norse_syllable([a, l]).name
    'short'

    >>> measure_old_norse_syllable([s, t, ee, r, k, r]).name
    'long'

    >>> measure_old_norse_syllable([m, o.lengthen()]).name
    'long'

    :param syllable: list of Vowel and Consonant instances
    :return: instance of Length (short, long or overlong)
    """
    index = 0
    while index < len(syllable) and not isinstance(syllable[index], Vowel):
        index += 1
    if index == len(syllable):
        return None
    else:
        long_vowel_number = 0
        short_vowel_number = 0
        geminated_consonant_number = 0
        simple_consonant_number = 0
        for c in syllable[index:]:
            if isinstance(c, Vowel):
                if c.length == Length.long:
                    long_vowel_number += 1
                elif c.length == Length.short:
                    short_vowel_number += 1
            elif isinstance(c, Consonant):
                if c.geminate:
                    geminated_consonant_number += 1
                else:
                    simple_consonant_number += 1
        if (
            long_vowel_number == 0
            and short_vowel_number == 1
            and simple_consonant_number <= 1
            and geminated_consonant_number == 0
        ):
            return Length.short
        elif (
            (
                short_vowel_number == 1
                and (simple_consonant_number > 1 or geminated_consonant_number > 0)
            )
            or long_vowel_number > 0
            and simple_consonant_number <= 1
            and geminated_consonant_number == 0
        ):
            return Length.long
        elif long_vowel_number > 0 and (
            simple_consonant_number > 1 or geminated_consonant_number > 0
        ):
            return Length.overlong


def normalize_for_syllabifier(text: str) -> str:
    """
    >>> normalize_for_syllabifier("almaːtːiɣr")
    'almatiɣr'

    :param text: text to normalize for syllabification
    :return: normalized text for syllabification
    """
    text = text.replace("ː", "")
    return text
