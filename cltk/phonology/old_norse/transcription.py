"""
https://fr.wikipedia.org/wiki/%C3%89criture_du_vieux_norrois

Altnordisches Elementarbuch by Friedrich Ranke and Dietrich Hofmann
"""
import re
import unicodedata


# Consonants
PLACES = ["bilabial", "labio-dental", "dental", "alveolar", "post-alveolar", "retroflex", "palatal", "velar", "uvular", "glottal"]
MANNERS = ["nasal", "stop", "lateral", "frictative", "trill"]


class Consonant:
    def __init__(self, place, manner, voiced, ipar):
        if place in PLACES:
            self.place = place
        else:
            raise ValueError
        if place in PLACES:
            self.manner = manner
        else:
            raise ValueError
        if type(voiced) == bool:
            self.voiced = voiced
        else:
            raise TypeError
        self.ipar = ipar


# Vowels
HEIGHT = ["front", "central", "back"]
BACKNESS = ["open", "near-open", "open-mid", "mid", "close-mid", "near-close", "close"]
LENGTHS = ["short", "long", "overlong"]


class Vowel:
    def __init__(self, height, backness, rounded, length, ipar):
        if height in HEIGHT:
            self.height = height
        else:
            raise ValueError
        if backness in BACKNESS:
            self.backness = backness
        else:
            raise ValueError
        if type(rounded) == bool:
            self.rounded = rounded
        else:
            raise TypeError
        if length in LENGTHS:
            self.length = length
        else:
            raise ValueError
        self.ipar = ipar

    def lengthen(self):
        if self.length == "short":
            length = "long"
            ipar = self.ipar + ":"
        else:
            ipar = self.ipar
            length = "short"
        return Vowel(self.height, self.backness, self.rounded, length, ipar)

    # def overlengthen(self):
    #     self.length = "overlong"

    def i_umlaut(self):
        pass

    def u_umlaut(self):
        pass


a = Vowel("open", "front", False, "short", "a")
ee = Vowel("open-mid", "front", False, "short", "ɛ")
e = Vowel("close-mid", "front", False, "short", "e")
oee = Vowel("close-mid", "front", True, "short", "ø")
oe = Vowel("open-mid", "front", True, "short", "œ")
i = Vowel("close", "front", False, "short", "i")
y = Vowel("close", "front", True, "short", "y")
ao = Vowel("open", "back", True, "short", "ɒ"),
oo = Vowel("open-mid", "back", True, "short", "ɔ")
o = Vowel("close-mid", "back", True, "short", "o")
u = Vowel("close", "back", True, "short", "u")

b = Consonant("bilabial", "stop", True, "b")
d = Consonant("alveolar", "stop", True, "d")
f = Consonant("labio-dental", "frictative", False, "f")
g = Consonant("velar", "stop", True, "g")
h = Consonant("glottal", "frictative", False, "h")
k = Consonant("velar", "stop", False, "k")
l = Consonant("alveolar", "lateral", True, "l")
m = Consonant("bilabial", "nasal", True, "m")
n = Consonant("labio-dental", "nasal", True, "n")
p = Consonant("bilabial", "stop", False, "p")
r = Consonant("alveolar", "trill", False, "r")
s = Consonant("alveolar", "frictative", False, "s")
t = Consonant("alveolar", "stop", False, "t")
v = Consonant("labio-dental", "frictative", True, "v")
θ = Consonant("dental", "frictative", False, "θ")
ð = Consonant("dental", "frictative", True, "ð")

OLD_NORSE8_PHONOLOGY = [
    a, ee, e, oe, i, y, ao, oo, u, a.lengthen(),
    e.lengthen(), i.lengthen(), o.lengthen(), u.lengthen(),
    y.lengthen(), b, d, f, g, h, k, l, m, n, p, r, s, t, v, θ, ð
]


# IPA Dictionary
Dipthongs_IPA = {
    "ey": "ɐy",  # Dipthongs
    "au": "ɒu",
    "øy": "ɐy",
    "ei": "ei"
}

IPA = {
    "a": "a",  # Short vowels
    "e": "ɛ",
    "i": "i",
    "o": "ɔ",
    "ǫ": "ɒ",
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
    "k": k,
    "l": l,
    "m": m,
    "n": n,
    "p": p,
    "r": r,
    "s": s,
    "t": t,
    "v": v,
    "þ": θ,
    "ð": ð,
}

class TransformationRule():
    pass


class Transcriber:

    def __init__(self):
        pass  # To-do: Add different dialects and/or notations

    def transcribe(self, text: str, punctuation=True):
        """
        Accepts a word and returns a string of an approximate pronounciation (IPA)
        :param text: str
        :param punctuation: boolean
        :return:
        """

        if not punctuation:
            text = re.sub(r"[\.\";\,\:\[\]\(\)!&?‘]", "", text)

        for w, val in Dipthongs_IPA:
            text = text.replace(w, val)

        for w, val in IPA:
            text = text.replace(w, val)

        return "[" + text + "]"


if __name__ == "__main__":
    # Word()
    pass