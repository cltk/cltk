"""
https://fr.wikipedia.org/wiki/%C3%89criture_du_vieux_norrois

Altnordisches Elementarbuch by Friedrich Ranke and Dietrich Hofmann
"""

from cltk.phonology.utils import *

__author__ = ["Clément Besnier <clemsciences@gmail.com>"]


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
f = Consonant(Place.labio_dental, Manner.frictative, False, "f", False)
g = Consonant(Place.velar, Manner.stop, True, "g", False)
gh = Consonant(Place.velar, Manner.frictative, True, "ɣ", False)
h = Consonant(Place.glottal, Manner.frictative, False, "h", False)
j = Consonant(Place.palatal, Manner.frictative, True, "j", False)
k = Consonant(Place.velar, Manner.stop, False, "k", False)
l = Consonant(Place.alveolar, Manner.lateral, True, "l", False)
m = Consonant(Place.bilabial, Manner.nasal, True, "m", False)
n = Consonant(Place.labio_dental, Manner.nasal, True, "n", False)
p = Consonant(Place.bilabial, Manner.stop, False, "p", False)
r = Consonant(Place.alveolar, Manner.trill, True, "r", False)
s = Consonant(Place.alveolar, Manner.frictative, False, "s", False)
t = Consonant(Place.alveolar, Manner.stop, False, "t", False)
v = Consonant(Place.labio_dental, Manner.frictative, True, "v", False)
# θ = Consonant(Place.dental, Manner.frictative, False, "θ")
th = Consonant(Place.dental, Manner.frictative, False, "θ", False)
# ð = Consonant(Place.dental, Manner.frictative, True, "ð")
dh = Consonant(Place.dental, Manner.frictative, True, "ð", False)

OLD_NORSE8_PHONOLOGY = [
    a, ee, e, oe, i, y, ao, oo, u, a.lengthen(),
    e.lengthen(), i.lengthen(), o.lengthen(), u.lengthen(),
    y.lengthen(), b, d, f, g, h, k, l, m, n, p, r, s, t, v, th, dh
]

# IPA Dictionary
DIPHTHONGS_IPA = {
    "ey": "ɐy",  # Diphthongs
    "au": "ɒu",
    "øy": "ɐy",
    "ei": "ei",
}
# Wrong diphthongs implementation but not that bad for now
DIPHTHONGS_IPA_class = {
    "ey": Vowel("open", "front", True, "short", "ɐy"),
    "au": Vowel("open", "back", True, "short", "ɒu"),
    "øy": Vowel("open", "front", True, "short", "ɐy"),
    "ei": Vowel("open", "front", True, "short", "ɛi"),
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
    "x": k+s,
    "z": s,
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
rule_th = [Rule(AbstractPosition("first", None, []), th, th),
           Rule(AbstractPosition("inner", [], [AbstractConsonant(voiced=True)]), th, th),
           Rule(AbstractPosition("inner", [AbstractConsonant(voiced=True)], []), th, th),
           Rule(AbstractPosition("inner", [], []), th, dh),
           Rule(AbstractPosition("last", [], None), th, dh)]

rule_f = [Rule(AbstractPosition("first", None, []), f, f),
          Rule(AbstractPosition("inner", [], [AbstractConsonant(voiced=False)]), f, f),
          Rule(AbstractPosition("inner", [AbstractConsonant(voiced=False)], []), f, f),
          Rule(AbstractPosition("inner", [], []), f, v),
          Rule(AbstractPosition("last", [], None), f, v)]

rule_g = [Rule(AbstractPosition("first", None, None), g, g),
          Rule(AbstractPosition("inner", [n.to_abstract()], None), g, g),
          Rule(AbstractPosition("inner", None, [AbstractConsonant(voiced=False)]), g, k),
          Rule(AbstractPosition("inner", [], []), g, gh),
          Rule(AbstractPosition("last", [], None), g, gh)]

old_norse_rules = []
old_norse_rules.extend(rule_f)
old_norse_rules.extend(rule_g)
old_norse_rules.extend(rule_th)
