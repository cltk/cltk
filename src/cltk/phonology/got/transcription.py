"""Gothic phonological transcription module.
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
- [ɛ:] when <ai> is before <a> or <an> and when it is at the end of a syllable or a word
  or when it is in an Ancient Greek borrowing
- [ai] in other cases

Here -> [ɛ]

<au>:

- [ɔ] when <au> is before <r>, <h> or <ƕ> or when it is in Ancient Greek borrowings
- [ɔ:] when <ai> is before <a> or <an> and when it is at the end of a syllable or a word
  or when it is in an Ancient Greek borrowing
- [au] in other cases

Here -> [ɔ]

Specialists do not agree on digraph pronunciation. Some of them think they were monophthongs whereas others think
that they were monophthongs or diphthongs according to cases.

Remaining issues:

- <gg>: [ŋg]
- <ggw>: [ŋgw] or [ggw] because in such cases the geminated gg are actually a reinforcement of [gww]
- <z>: [z] in Germanic words or [dz] in Ancient Greek words
- etc

"""

from cltk.phonology.non.utils import *

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

a = Vowel(Height.open, Backness.front, False, Length.short, "a")
long_a = a.lengthen()
ee = Vowel(Height.open_mid, Backness.front, False, Length.short, "ɛ")
long_ee = ee.lengthen()
e = Vowel(Height.close_mid, Backness.front, False, Length.short, "e")
long_e = e.lengthen()
i = Vowel(Height.close, Backness.front, False, Length.short, "i")
long_i = i.lengthen()
y = Vowel(Height.close, Backness.front, True, Length.short, "y")
oo = Vowel(Height.open_mid, Backness.back, True, Length.short, "ɔ")
long_oo = oo.lengthen()
o = Vowel(Height.close_mid, Backness.back, True, Length.short, "o")
long_o = o.lengthen()
u = Vowel(Height.close, Backness.back, True, Length.short, "u")
long_u = u.lengthen()

b = Consonant(Place.bilabial, Manner.stop, True, "b", False)
bh = Consonant(Place.bilabial, Manner.fricative, True, "β", False)
d = Consonant(Place.alveolar, Manner.stop, True, "d", False)
f = Consonant(Place.labio_dental, Manner.fricative, False, "f", False)
g = Consonant(Place.velar, Manner.stop, True, "g", False)
gh = Consonant(Place.velar, Manner.fricative, True, "Ɣ", False)
h = Consonant(Place.glottal, Manner.fricative, False, "h", False)
j = Consonant(Place.palatal, Manner.fricative, True, "j", False)
k = Consonant(Place.velar, Manner.stop, False, "k", False)
kh = Consonant(Place.velar, Manner.fricative, False, "x", False)
l = Consonant(Place.alveolar, Manner.lateral, True, "l", False)
m = Consonant(Place.bilabial, Manner.nasal, True, "m", False)
n = Consonant(Place.labio_dental, Manner.nasal, True, "n", False)
ng = Consonant(Place.velar, Manner.nasal, True, "ŋ", False)
p = Consonant(Place.bilabial, Manner.stop, False, "p", False)
ph = Consonant(Place.bilabial, Manner.fricative, False, "ɸ", False)
r = Consonant(Place.alveolar, Manner.trill, False, "r", False)
s = Consonant(Place.alveolar, Manner.fricative, False, "s", False)
t = Consonant(Place.alveolar, Manner.stop, False, "t", False)
v = Consonant(Place.labio_dental, Manner.fricative, True, "v", False)
w = Consonant(Place.bilabial, Manner.spirant, True, "w", False)
x = k + s
z = Consonant(Place.alveolar, Manner.fricative, True, "z", False)
# θ = Consonant(Place.dental, Manner.frictative, False, "θ")
th = Consonant(Place.dental, Manner.fricative, False, "θ", False)
# ð = Consonant(Place.dental, Manner.frictative, True, "ð")
dh = Consonant(Place.dental, Manner.fricative, True, "ð", False)

GOTHIC_PHONOLOGY = [
    a,
    ee,
    e,
    i,
    y,
    oo,
    u,
    long_a,
    long_e,
    long_ee,
    long_i,
    long_oo,
    long_o,
    long_u,
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
DIPHTHONGS_IPA = {"iu": "iu", "ai": "ɛ", "ei": "i:", "au": "ɔ"}  # Diphthongs
# Wrong diphthongs implementation but not that bad for now
DIPHTHONGS_IPA_class = {
    "iu": Vowel(Height.open, Backness.front, True, Length.short, "iu"),
    "ai": ee,
    "ei": i.lengthen(),
    "au": oo,
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
    "ƕ": "hʷ",
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
    "q": k + w,
    "l": l,
    "m": m,
    "n": n,
    "p": p,
    "r": r,
    "s": s,
    "z": z,
    "t": t,
    "v": v,
    "w": w,
    "x": x,
    "þ": th,
    "ð": dh,
    "ƕ": h + w,
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

gothic_rules_i = [Rule(AbstractPosition(Rank.first, None, [AbstractVowel()]), i, j)]


gothic_rules_b = [
    Rule(AbstractPosition(Rank.first, None, []), b, b),
    Rule(AbstractPosition(Rank.inner, [n.to_abstract(), m.to_abstract()], []), b, b),
    Rule(AbstractPosition(Rank.inner, [r.to_abstract(), l.to_abstract()], []), b, b),
    Rule(AbstractPosition(Rank.inner, [AbstractVowel()], [AbstractVowel()]), b, bh),
    Rule(AbstractPosition(Rank.last, [], None), b, ph),
]

gothic_rules_d = [
    Rule(AbstractPosition(Rank.first, None, []), d, d),
    Rule(AbstractPosition(Rank.inner, [n.to_abstract(), m.to_abstract()], []), d, d),
    Rule(AbstractPosition(Rank.inner, [r.to_abstract(), l.to_abstract()], []), d, d),
    Rule(AbstractPosition(Rank.inner, [AbstractVowel()], [AbstractVowel()]), d, dh),
    Rule(AbstractPosition(Rank.last, [], None), b, th),
]

gothic_rules_g = [
    Rule(AbstractPosition(Rank.first, None, None), g, g),
    Rule(AbstractPosition(Rank.inner, [n.to_abstract(), m.to_abstract()], None), g, g),
    Rule(AbstractPosition(Rank.inner, [r.to_abstract(), l.to_abstract()], None), g, g),
    Rule(AbstractPosition(Rank.inner, [AbstractVowel()], [AbstractVowel()]), g, gh),
    Rule(AbstractPosition(Rank.last, [], None), b, kh),
]
gothic_rules_s = [Rule(AbstractPosition(Rank.first, None, None), s, z)]
gothic_rules_ks = [
    Rule(AbstractPosition(Rank.first, None, [AbstractConsonant()]), x, k),
    Rule(AbstractPosition(Rank.inner, [], [AbstractConsonant()]), x, k),
]


gothic_rules_h = [
    Rule(AbstractPosition(Rank.first, None, [AbstractVowel()]), h, h),
    Rule(AbstractPosition(Rank.first, None, [AbstractConsonant()]), h, kh),
    Rule(AbstractPosition(Rank.inner, [], [s.to_abstract(), t.to_abstract()]), h, h),
]

gothic_rules.extend(gothic_rules_i)
gothic_rules.extend(gothic_rules_b)
gothic_rules.extend(gothic_rules_d)
gothic_rules.extend(gothic_rules_g)
gothic_rules.extend(gothic_rules_s)
gothic_rules.extend(gothic_rules_ks)
gothic_rules.extend(gothic_rules_h)
