"""
Sources:
- https://en.wikipedia.org/wiki/Gothic_language
- Gotische Grammatik by W. Braune and K. Helm (Max Niemeyer Verlag 1952)
- Grammaire explicative du gotique by André Rousseau (L'Harmattan 2012)


Vowels:
<a>, <u> can be short or long. Here <a>, <u> => [a], [u]
<i> represents [i] and <ei> represents [i:]
<e> and <o> are long vowels: [e:] and [o:]
<ai>:
    - [ɛ] when <ai> is before <r>, <h> or <ƕ> or when it is in Ancient Greek borrowings
    - [ɛ:] when <ai> is before <a> or <an> and when it is at the end of a syllable or a word or when it is in an
    Ancient Greek borrowing
    - [ai] in other cases
Here -> [ɛ]

<au>:
    - [ɔ] when <au> is before <r>, <h> or <ƕ> or when it is in Ancient Greek borrowings
    - [ɔ:] when <ai> is before <a> or <an> and when it is at the end of a syllable or a word or when it is in an
    Ancient Greek borrowing
    - [au] in other cases
Here -> [ɔ]

Specialists do not agree on digraph pronunciation. Some of them think they were monophthongs whereas others think
that they were monophthongs or diphthongs according to cases.

Remaining issues:
<gg>: [ŋg]
<ggw>: [ŋgw] or [ggw] because in such cases the geminated gg are actually a reinforcement of [gww]
<z>: [z] in Germanic words or [dz] in Ancient Greek words
etc
"""

from cltk.phonology.utils import *

__author__ = ["Clément Besnier <clemsciences@gmail.com>"]

a = Vowel("open", "front", False, "short", "a")
long_a = a.lengthen()
ee = Vowel("open-mid", "front", False, "short", "ɛ")
long_ee = ee.lengthen()
e = Vowel("close-mid", "front", False, "short", "e")
long_e = e.lengthen()
i = Vowel("close", "front", False, "short", "i")
long_i = i.lengthen()
y = Vowel("close", "front", True, "short", "y")
oo = Vowel("open-mid", "back", True, "short", "ɔ")
long_oo = oo.lengthen()
o = Vowel("close-mid", "back", True, "short", "o")
long_o = o.lengthen()
u = Vowel("close", "back", True, "short", "u")
long_u = u.lengthen()

b = Consonant("bilabial", "stop", True, "b", False)
bh = Consonant("bilabial", "frictative", True, "β", False)
d = Consonant("alveolar", "stop", True, "d", False)
f = Consonant("labio-dental", "frictative", False, "f", False)
g = Consonant("velar", "stop", True, "g", False)
gh = Consonant("velar", "frictative", True, "Ɣ", False)
h = Consonant("glottal", "frictative", False, "h", False)
j = Consonant("palatal", "frictative", True, "j", False)
k = Consonant("velar", "stop", False, "k", False)
kh = Consonant("velar", "frictative", False, "", False)
l = Consonant("alveolar", "lateral", True, "l", False)
m = Consonant("bilabial", "nasal", True, "m", False)
n = Consonant("labio-dental", "nasal", True, "n", False)
ng = Consonant("velar", "nasal", True, "ŋ", False)
p = Consonant("bilabial", "stop", False, "p", False)
ph = Consonant("bilabial", "frictative", False, "ɸ", False)
r = Consonant("alveolar", "trill", False, "r", False)
s = Consonant("alveolar", "frictative", False, "s", False)
t = Consonant("alveolar", "stop", False, "t", False)
v = Consonant("labio-dental", "frictative", True, "v", False)
w = Consonant("bilabial", "spirant", True, "w", False)
x = k + s
z = Consonant("alveolar", "frictative", True, "z", False)
# θ = Consonant("dental", "frictative", False, "θ")
th = Consonant("dental", "frictative", False, "θ", False)
# ð = Consonant("dental", "frictative", True, "ð")
dh = Consonant("dental", "frictative", True, "ð", False)

GOTHIC_PHONOLOGY = [
    a, ee, e, i, y, oo, u, long_a, long_e, long_ee, long_i, long_oo, long_o, long_u,
    b, d, f, g, h, k, l, m, n, p, r, s, t, v, th, dh
]


# IPA Dictionary
DIPHTHONGS_IPA = {
    "iu": "iu",  # Diphthongs
    "ai": "ɛ",
    "ei": "i:",
    "au": "ɔ"
}
# Wrong diphthongs implementation but not that bad for now
DIPHTHONGS_IPA_class = {
    "iu": Vowel("open", "front", True, "short", "iu"),
    "ai": ee,
    "ei": i.lengthen(),
    "au": oo
}

ORIGINAL_IPA = {
    "𐌰": "a",
    "𐌱": "b",
    "𐌲": "g",
    "𐌳": "d",
    "𐌴": "ē",
    "𐌵": "q",
    "𐌶": "z",
    "𐌷": "h",
    "𐌸": "þ",
    "𐌹": "i",
    "𐌺": "k",
    "𐌻": "l",
    "𐌼": "m",
    "𐌽": "n",
    "𐌾": "j",
    "𐌿": "u",
    "𐍀": "p",
    "𐍂": "r",
    "𐍃": "s",
    "𐍄": "t",
    "𐍅": "w",
    "𐍆": "f",
    "𐍇": "x",
    "𐍈": "ƕ",
    "𐍉": "ō",
    "𐍊": "/",
    "𐍁": "/",
}


IPA = {
    "a": "a",  # Short vowels
    "e": "ɛ",
    "i": "i",
    "o": "ɔ",
    "u": "u",
    "y": "y",
    # Consonants
    "b": "b",
    "d": "d",
    "f": "ɸ",
    "g": "g",
    "h": "h",
    "j": "j",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "p": "p",
    "q": "kʷ",
    "r": "r",
    "s": "s",
    "t": "t",
    "v": "v",
    "w": "w",
    "z": "z",
    "þ": "θ",
    "ƕ": "hʷ"
}

IPA_class = {
    "a": a,  # Short vowels
    "e": e.lengthen(),
    "i": i,
    "o": o.lengthen(),
    "u": u,
    "y": y,
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
    "w": w,
    "x": x,
    "þ": th,
    "ð": dh,
    "ƕ": h+w
}
GEMINATE_CONSONANTS = {
    "bb": "b:",
    "dd": "d:",
    "ff": "f:",
    "gg": "ŋg",
    "kk": "k:",
    "ll": "l:",
    "mm": "m:",
    "nn": "n:",
    "pp": "p:",
    "rr": "r:",
    "ss": "s:",
    "tt": "t:",
    "vv": "v:",
}
GEMINATE_CONSONANTS_class = {
    "bb": b.lengthen(),
    "dd": d.lengthen(),
    "ff": f.lengthen(),
    "gg": ng + g,
    "kk": k.lengthen(),
    "ll": l.lengthen(),
    "mm": m.lengthen(),
    "nn": n.lengthen(),
    "pp": p.lengthen(),
    "rr": r.lengthen(),
    "ss": s.lengthen(),
    "tt": t.lengthen(),
    "vv": v.lengthen(),
}
DIPHTHONGS_IPA.update(GEMINATE_CONSONANTS)
DIPHTHONGS_IPA_class.update(GEMINATE_CONSONANTS_class)

# Rules
gothic_rules = []

gothic_rules_i = [
    Rule(AbstractPosition("first", None, [AbstractVowel()]), i, j),
]


gothic_rules_b = [
    Rule(AbstractPosition("first", None, []), b, b),
    Rule(AbstractPosition("inner", [n.to_abstract(), m.to_abstract()], []), b, b),
    Rule(AbstractPosition("inner", [r.to_abstract(), l.to_abstract()], []), b, b),
    Rule(AbstractPosition("inner", [AbstractVowel()], [AbstractVowel()]), b, bh),
    Rule(AbstractPosition("last", [], None), b, ph)
]

gothic_rules_d = [
    Rule(AbstractPosition("first", None, []), d, d),
    Rule(AbstractPosition("inner", [n.to_abstract(), m.to_abstract()], []), d, d),
    Rule(AbstractPosition("inner", [r.to_abstract(), l.to_abstract()], []), d, d),
    Rule(AbstractPosition("inner", [AbstractVowel()], [AbstractVowel()]), d, dh),
    Rule(AbstractPosition("last", [], None), b, th)
]

gothic_rules_g = [
    Rule(AbstractPosition("first", None, None), g, g),
    Rule(AbstractPosition("inner", [n.to_abstract(), m.to_abstract()], None), g, g),
    Rule(AbstractPosition("inner", [r.to_abstract(), l.to_abstract()], None), g, g),
    Rule(AbstractPosition("inner", [AbstractVowel()], [AbstractVowel()]), g, gh),
    Rule(AbstractPosition("last", [], None), b, kh)
]
gothic_rules_s = [
    Rule(AbstractPosition("first", None, None), s, z),
]
gothic_rules_ks = [
    Rule(AbstractPosition("first", None, [AbstractConsonant()]), x, k),
    Rule(AbstractPosition("inner", [], [AbstractConsonant()]), x, k),
]


gothic_rules_h = [
    Rule(AbstractPosition("first", None, [AbstractVowel()]), h, h),
    Rule(AbstractPosition("first", None, [AbstractConsonant()]), h, kh),
    Rule(AbstractPosition("inner", [], [s.to_abstract(), t.to_abstract()]), h, h),

]

gothic_rules.extend(gothic_rules_i)
gothic_rules.extend(gothic_rules_b)
gothic_rules.extend(gothic_rules_d)
gothic_rules.extend(gothic_rules_g)
gothic_rules.extend(gothic_rules_s)
gothic_rules.extend(gothic_rules_ks)
gothic_rules.extend(gothic_rules_h)
