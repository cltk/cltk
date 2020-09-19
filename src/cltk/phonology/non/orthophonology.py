"""
Old Norse orthophonology module similar to the cltk.phonology.non.transcription with a different way to transcribe
"""

from cltk.phonology.orthophonology import *

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

# Vowels
a = Vowel(Height.open, Backness.front, Roundedness.neg, Length.short, "a")
ee = Vowel(Height.open_mid, Backness.front, Roundedness.neg, Length.short, "ɛ")
e = Vowel(Height.close_mid, Backness.front, Roundedness.neg, Length.short, "e")
oee = Vowel(Height.close_mid, Backness.front, Roundedness.pos, Length.short, "ø")
oe = Vowel(Height.open_mid, Backness.front, Roundedness.pos, Length.short, "œ")
i = Vowel(Height.close, Backness.front, Roundedness.neg, Length.short, "i")
y = Vowel(Height.close, Backness.front, Roundedness.pos, Length.short, "y")
ao = Vowel(Height.open, Backness.back, Roundedness.pos, Length.short, "ɒ")
oo = Vowel(Height.open_mid, Backness.back, Roundedness.pos, Length.short, "ɔ")
o = Vowel(Height.close_mid, Backness.back, Roundedness.pos, Length.short, "o")
u = Vowel(Height.close, Backness.back, Roundedness.pos, Length.short, "u")

# Consonants
b = Consonant(Place.bilabial, Manner.stop, Voiced.pos, "b", Geminate.neg)
d = Consonant(Place.alveolar, Manner.stop, Voiced.pos, "d", Geminate.neg)
f = Consonant(Place.labio_dental, Manner.fricative, Voiced.neg, "f", Geminate.neg)
g = Consonant(Place.velar, Manner.stop, Voiced.pos, "g", Geminate.neg)
gh = Consonant(Place.velar, Manner.fricative, Voiced.pos, "ɣ", Geminate.neg)
h = Consonant(Place.glottal, Manner.fricative, Voiced.neg, "h", Geminate.neg)
j = Consonant(Place.palatal, Manner.fricative, Voiced.pos, "j", Geminate.neg)
k = Consonant(Place.velar, Manner.stop, Voiced.neg, "k", Geminate.neg)
l = Consonant(Place.alveolar, Manner.lateral, Voiced.pos, "l", Geminate.neg)
m = Consonant(Place.bilabial, Manner.nasal, Voiced.pos, "m", Geminate.neg)
n = Consonant(Place.labio_dental, Manner.nasal, Voiced.pos, "n", Geminate.neg)
p = Consonant(Place.bilabial, Manner.stop, Voiced.neg, "p", Geminate.neg)
r = Consonant(Place.alveolar, Manner.trill, Voiced.pos, "r", Geminate.neg)
s = Consonant(Place.alveolar, Manner.fricative, Voiced.neg, "s", Geminate.neg)
t = Consonant(Place.alveolar, Manner.stop, Voiced.neg, "t", Geminate.neg)
v = Consonant(Place.labio_dental, Manner.fricative, Voiced.pos, "v", Geminate.neg)
th = Consonant(Place.dental, Manner.fricative, Voiced.neg, "θ", Geminate.neg)
dh = Consonant(Place.dental, Manner.fricative, Voiced.pos, "ð", Geminate.neg)

x = Consonant(Place.velar, Manner.affricate, Voiced.neg, "k͡s")
z = Consonant(Place.alveolar, Manner.affricate, Voiced.neg, "t͡s")

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

consonants = [b, d, f, g, gh, h, j, k, l, m, n, p, r, s, t, v, th, dh]

vowels = [a, ee, e, oee, oe, i, y, ao, oo, o, u]

diphthongs = []

diphthongs_ipa = {"ey": a + y, "au": a + u, "øy": a + y, "ei": ee + i}

digraphs_ipa = {
    consonant.ipa + consonant.ipa: consonant.geminate() for consonant in consonants
}

sound_inventory = consonants + vowels + diphthongs

alphabet = {
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
    "x": x,
    "z": z,
    "þ": th,
    "ð": dh,
}


class OldNorsePhonologicalTranscriber:
    """
    Old Norse phonological transcriber using orthophonology.
    """

    def __init__(self):
        self.on = Orthophonology(
            sound_inventory, alphabet, diphthongs_ipa, digraphs_ipa
        )

        self.on.rules = [
            th // f >> Voiced.pos | Consonantal.neg - Consonantal.neg,
            th // f >> Voiced.pos | Voiced.pos - Consonantal.neg,
            th // f >> Voiced.pos | Consonantal.neg - Voiced.pos,
            th // f >> Voiced.pos | Voiced.pos - Voiced.pos,
            g >> gh | Voiced.pos - Voiced.pos,
            g >> gh | Consonantal.neg - Consonantal.neg,
            g >> gh | Voiced.pos - Consonantal.neg,
            g >> gh | Consonantal.neg - Voiced.pos,
            g >> gh | Consonantal.neg - W,
        ]

    def transcribe(self, word):
        return "".join([phoneme.ipa for phoneme in self.on.transcribe_word(word)])

    def __repr__(self):
        return f"<OldNorseScanner>"

    def __call__(self, word):
        return self.transcribe(word)
