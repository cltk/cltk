"""
Sources:

* *Svenska språket under sjuhundra år* by Gertrud Pettersson (Studentlitteratur 2017)
* Klassisk fornsvenska (Classical Old Swedish): 1225-1375
* Yngre fornsvenska (Younger Old Swedish): 1375-1526 (first prints)

"""

from cltk.phonology.non.utils import *

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

a = Vowel(Height.open, Backness.front, False, Length.short, "a")
ee = Vowel(Height.open_mid, Backness.front, False, Length.short, "ɛ")
e = Vowel(Height.close_mid, Backness.front, False, Length.short, "e")
oee = Vowel(Height.close_mid, Backness.front, True, Length.short, "ø")
i = Vowel(Height.close, Backness.front, False, Length.short, "i")
y = Vowel(Height.close, Backness.front, True, Length.short, "y")
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
w = v
x = k + s
z = t + s
# θ = Consonant(Place.dental, Manner.frictative, False, "θ")
th = Consonant(Place.dental, Manner.fricative, False, "θ", False)
# ð = Consonant(Place.dental, Manner.frictative, True, "ð")
dh = Consonant(Place.dental, Manner.fricative, True, "ð", False)

OLD_NORSE8_PHONOLOGY = [
    a,
    ee,
    i,
    oee,
    y,
    u,
    o,
    a.lengthen(),
    ee.lengthen(),
    e.lengthen(),
    oee.lengthen(),
    i.lengthen(),
    y.lengthen(),
    u.lengthen(),
    o.lengthen(),
    p,
    b,
    t,
    d,
    k,
    g,
    f,
    v,
    th,
    dh,
    s,
    gh,
    h,
    j,
    l,
    r,
    n,
]

# IPA Dictionary
DIPHTHONGS_IPA = {"ey": "ɐy", "au": "ɒu", "øy": "ɐy", "ei": "ei"}  # Diphthongs
# Wrong diphthongs implementation but not that bad for now
DIPHTHONGS_IPA_class = {
    "ey": Vowel(Height.open, Backness.front, True, Length.short, "ɐy"),
    "au": Vowel(Height.open, Backness.back, True, Length.short, "ɒu"),
    "øy": Vowel(Height.open, Backness.front, True, Length.short, "ɐy"),
    "ei": Vowel(Height.open, Backness.front, True, Length.short, "ɛi"),
}
IPA = {
    "a": "a",  # Short vowels
    "e": "ɛ",
    "i": "i",
    "o": "o",
    "ö": "ø",
    "ø": "ø",
    "u": "u",
    "y": "y",
    "æ": "ɛ",
    # Consonants
    "b": "b",
    "c": "k",
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
    "q": "k",
    "r": "r",
    "s": "s",
    "t": "t",
    "v": "v",
    "w": "v",
    "x": "ks",
    "z": "ts",
    "þ": "θ",
    "ð": "ð",
}
IPA_class = {
    "a": a,  # Short vowels
    "æ": ee,
    "e": ee,
    "i": i,
    "o": o,
    "ø": oee,
    "ö": oee,
    "u": u,
    "y": y,
    # Consonants
    "b": b,
    "c": k,
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
    "q": k,
    "r": r,
    "s": s,
    "t": t,
    "v": v,
    "w": v,
    "x": k + s,
    "z": t + s,
    "þ": th,
    "ð": dh,
}

GEMINATE_CONSONANTS = {
    "bb": "bː",
    "dd": "dː",
    "dh": "ð",
    "ff": "fː",
    "gg": "gː",
    "gh": "ɣ",
    "kk": "kː",
    "ll": "lː",
    "mm": "mː",
    "nn": "nː",
    "pp": "pː",
    "rr": "rː",
    "ss": "sː",
    "th": "θ",
    "tt": "tː",
    "vv": "vː",
}

GEMINATE_CONSONANTS_class = {
    "bb": b.lengthen(),
    "dd": d.lengthen(),
    "dh": dh,
    "ff": f.lengthen(),
    "gg": g.lengthen(),
    "gh": gh,
    "kk": k.lengthen(),
    "ll": l.lengthen(),
    "mm": m.lengthen(),
    "nn": n.lengthen(),
    "pp": p.lengthen(),
    "rr": r.lengthen(),
    "ss": s.lengthen(),
    "th": th,
    "tt": t.lengthen(),
    "vv": v.lengthen(),
}

DIPHTHONGS_IPA.update(GEMINATE_CONSONANTS)
DIPHTHONGS_IPA_class.update(GEMINATE_CONSONANTS_class)

# Some Old Norse rules
# The first rule which matches is retained

rule_th = [
    Rule(AbstractPosition(Rank.inner, [AbstractVowel()], [AbstractVowel()]), th, dh),
    Rule(AbstractPosition(Rank.last, [AbstractConsonant()], None), th, dh),
    Rule(AbstractPosition(Rank.first, None, []), th, th),
    Rule(AbstractPosition(Rank.last, [r.to_abstract()], None), th, dh),
]


old_swedish_rules = []
old_swedish_rules.extend(rule_th)
