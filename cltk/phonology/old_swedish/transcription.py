"""
*Svenska språket under sjuhundra år* by Gertrud Pettersson (Studentlitteratur 2017)

Klassisk fornsvenska (Classical Old Swedish): 1225-1375
Yngre fornsvenska (Younger Old Swedish): 1375-1526 (first prints)

"""

from cltk.phonology.utils import *

__author__ = ["Clément Besnier <clemsciences@gmail.com>"]

a = Vowel("open", "front", False, "short", "a")
ee = Vowel("open-mid", "front", False, "short", "ɛ")
e = Vowel("close-mid", "front", False, "short", "e")
oee = Vowel("close-mid", "front", True, "short", "ø")
i = Vowel("close", "front", False, "short", "i")
y = Vowel("close", "front", True, "short", "y")
o = Vowel("close-mid", "back", True, "short", "o")
u = Vowel("close", "back", True, "short", "u")

b = Consonant("bilabial", "stop", True, "b", False)
d = Consonant("alveolar", "stop", True, "d", False)
f = Consonant("labio-dental", "frictative", False, "f", False)
g = Consonant("velar", "stop", True, "g", False)
gh = Consonant("velar", "frictative", True, "ɣ", False)
h = Consonant("glottal", "frictative", False, "h", False)
j = Consonant("palatal", "frictative", True, "j", False)
k = Consonant("velar", "stop", False, "k", False)
l = Consonant("alveolar", "lateral", True, "l", False)
m = Consonant("bilabial", "nasal", True, "m", False)
n = Consonant("labio-dental", "nasal", True, "n", False)
p = Consonant("bilabial", "stop", False, "p", False)
r = Consonant("alveolar", "trill", True, "r", False)
s = Consonant("alveolar", "frictative", False, "s", False)
t = Consonant("alveolar", "stop", False, "t", False)
v = Consonant("labio-dental", "frictative", True, "v", False)
w = v
x = k+s
z = t+s
# θ = Consonant("dental", "frictative", False, "θ")
th = Consonant("dental", "frictative", False, "θ", False)
# ð = Consonant("dental", "frictative", True, "ð")
dh = Consonant("dental", "frictative", True, "ð", False)

OLD_NORSE8_PHONOLOGY = [
    a, ee, i, oee, y, u, o, a.lengthen(), ee.lengthen(), e.lengthen(), oee.lengthen(),
    i.lengthen(), y.lengthen(), u.lengthen(), o.lengthen(),
    p, b, t, d, k, g, f, v, th, dh, s, gh, h, j, l, r, n
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
    "x": k+s,
    "z": t+s,
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

rule_th = [Rule(AbstractPosition("inner", [AbstractVowel()], [AbstractVowel()]), th, dh),
           Rule(AbstractPosition("last", [AbstractConsonant()], None), th, dh),
           Rule(AbstractPosition("first", None, []), th, th),
           Rule(AbstractPosition("last", [r.to_abstract()], None), th, dh)]


old_swedish_rules = []
old_swedish_rules.extend(rule_th)
