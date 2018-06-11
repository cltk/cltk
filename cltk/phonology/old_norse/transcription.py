"""
https://fr.wikipedia.org/wiki/%C3%89criture_du_vieux_norrois

Altnordisches Elementarbuch by Friedrich Ranke and Dietrich Hofmann
"""
import re
import unicodedata


# Consonants
PLACES = ["bilabial", "labio-dental", "dental", "alveolar", "post-alveolar", "retroflex", "palatal", "velar", "uvular", "glottal"]
MANNERS = ["nasal", "stop", "lateral", "frictative", "trill"]


class AbstractConsonant:
    def __init__(self, place=None, manner=None, voiced=None, ipar=None):
        if place in PLACES or place is None:
            self.place = place
        else:
            raise ValueError
        if manner in MANNERS or manner is None:
            self.manner = manner
        else:
            raise ValueError
        if type(voiced) == bool or voiced is None:
            self.voiced = voiced
        else:
            raise TypeError
        self.ipar = ipar

    def match(self, other_consonant):

        # TODO
        if isinstance(other_consonant, AbstractConsonant):
            # TODO what is a match?
            return True
        else:
            return False


class Consonant(AbstractConsonant):
    def __init__(self, place, manner, voiced, ipar):
        assert place is not None
        assert manner is not None
        assert voiced is not None
        assert ipar is not None
        AbstractConsonant.__init__(self, place, manner, voiced, ipar)


# Vowels
HEIGHT = ["front", "central", "back"]
BACKNESS = ["open", "near-open", "open-mid", "mid", "close-mid", "near-close", "close"]
LENGTHS = ["short", "long", "overlong"]


class AbstractVowel:
    def __init__(self, height=None, backness=None, rounded=None, length=None, ipar=None):
        if height in HEIGHT or height is None:
            self.height = height
        else:
            raise ValueError
        if backness in BACKNESS or backness is None:
            self.backness = backness
        else:
            raise ValueError
        if type(rounded) == bool or rounded is None:
            self.rounded = rounded
        else:
            raise TypeError
        if length in LENGTHS or length is None:
            self.length = length
        else:
            raise ValueError
        self.ipar = ipar


class Vowel(AbstractVowel):
    def __init__(self, height, backness, rounded, length, ipar):
        assert height is not None
        assert backness is not None
        assert rounded is not None
        assert length is not None
        assert ipar is not None
        AbstractVowel.__init__(self, height, backness, rounded, length, ipar)

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
# θ = Consonant("dental", "frictative", False, "θ")
th = Consonant("dental", "frictative", False, "θ")
# ð = Consonant("dental", "frictative", True, "ð")
dh = Consonant("dental", "frictative", True, "ð")

OLD_NORSE8_PHONOLOGY = [
    a, ee, e, oe, i, y, ao, oo, u, a.lengthen(),
    e.lengthen(), i.lengthen(), o.lengthen(), u.lengthen(),
    y.lengthen(), b, d, f, g, h, k, l, m, n, p, r, s, t, v, th, dh
]
POSITIONS = ["first", "inner", "last"]


class Position:
    def __init__(self, position, before, after):
        self.position = position
        self.before = before
        self.after = after

    def match(self, other_pos):
        """
        Problem !
        :param other_pos:
        :return:
        """
        if self.position == other_pos.position:
            # TODO what is a match?
            if isinstance(self.before, AbstractConsonant):
                if isinstance(other_pos.before, AbstractConsonant):
                    return  True
                else:
                    return False
            return False



class Rule:
    def __init__(self, position, temp_sound, estimated_sound):
        assert isinstance(position, Position)
        self.position = position
        assert isinstance(temp_sound, AbstractVowel) or isinstance(temp_sound, AbstractConsonant)
        self.temp_sound = temp_sound
        assert isinstance(estimated_sound, AbstractVowel) or isinstance(estimated_sound, AbstractConsonant)
        self.estimated_sound = estimated_sound

    def apply(self, character, current_position: Position):
        if current_position.match(self.position):
            return ""
        else:
            return character



# IPA Dictionary
DIPHTONGS_IPA = {
    "ey": "ɐy",  # Dipthongs
    "au": "ɒu",
    "øy": "ɐy",
    "ei": "ei",
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
    "þ": th,
    "ð": dh,
}
GEMINATE_CONSONANTS = {
    "bb": "b:",
    "dd": "d:",
    "ff": "f:",
    "gg": "g:",
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


class Transcriber:

    def __init__(self):
        pass  # To-do: Add different dialects and/or notations

    def first_process(self, word: str):
        """
        Give a greedy approximation of the prononciation of word
        :param word:
        :return:
        """
        first_res = []
        # to_avoid = False

        for i in range(len(word)-1):
            # if to_avoid:
            #     to_avoid = False
            #     continue
            # elif word[i] == word[i+1]:  # geminate consonants
            #     first_res.append(word[i])
            #     to_avoid = True
            if word[i:i+2] in DIPHTONGS_IPA:  # diphtongs
                first_res.append(DIPHTONGS_IPA[word[i]+word[i+1]])
            else:
                first_res.append(IPA_class[word[i]])

    def second_process(self, first_result, rules):
        """
        Use of rules to precise pronunciation
        :param first_result:
        :param rules:
        :return:
        """
        assert len(first_result) >= 2
        res = []
        for i in range(len(first_result)):
            if i == 0:
                pos = Position("first", None, first_result[i])
            elif i == len(first_result)-1:
                pos = Position("inner", first_result[i-1], first_result[i+1])
            else:
                pos = Position("last", first_result[i-1], None)

            for rule in rules:
                rule.apply(first_result[i], pos)

        return "[" + "".join(res) + "]"

    def transcribe(self, text: str, punctuation=True):
        """
        Accepts a word and returns a string of an approximate pronounciation (IPA)
        :param text: str
        :param punctuation: boolean
        :return:
        """

        if not punctuation:
            text = re.sub(r"[\.\";\,\:\[\]\(\)!&?‘]", "", text)

        for w, val in DIPHTONGS_IPA:
            text = text.replace(w, val)

        for w, val in IPA:
            text = text.replace(w, val)

        return "[" + text + "]"


if __name__ == "__main__":
    # Word()
    pass