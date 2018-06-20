"""
Sources:
- https://en.wikipedia.org/wiki/Gothic_language
- Gotische Grammatik by W. Braune and K. Helm (Max Niemeyer Verlag 1952)
- Grammaire explicative du gotique by André Rousseau (L'Harmattan 2012)
"""

from cltk.phonology.utils import *


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
d = Consonant("alveolar", "stop", True, "d", False)
f = Consonant("labio-dental", "frictative", False, "f", False)
g = Consonant("velar", "stop", True, "g", False)
gh = Consonant("velar", "frictative", True, "Ɣ", False)
h = Consonant("glottal", "frictative", False, "h", False)
j = Consonant("palatal", "frictative", True, "j", False)
k = Consonant("velar", "stop", False, "k", False)
l = Consonant("alveolar", "lateral", True, "l", False)
m = Consonant("bilabial", "nasal", True, "m", False)
n = Consonant("labio-dental", "nasal", True, "n", False)
p = Consonant("bilabial", "stop", False, "p", False)
r = Consonant("alveolar", "trill", False, "r", False)
s = Consonant("alveolar", "frictative", False, "s", False)
t = Consonant("alveolar", "stop", False, "t", False)
v = Consonant("labio-dental", "frictative", True, "v", False)
w = Consonant("bilabial", "spirant", True, "w", False)
x = k + s
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
    "ai": "ai",
    "ei": "ei",
}
# Wrong diphthongs implementation but not that bad for now
DIPHTHONGS_IPA_class = {
    "iu": Vowel("open", "front", True, "short", "iu"),
    "ai": Vowel("open", "front", True, "long", "ai"),
    "ei": Vowel("open", "front", True, "short", "ɛi"),
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
    "e": ee,
    "i": i,
    "o": oo,
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

<<<<<<< HEAD

if __name__ == "__main__":
    example_sentence = "Anastodeins aiwaggeljons Iesuis Xristaus sunaus gudis."

    gothic_rules = []

    tr = Transcriber(DIPHTHONGS_IPA, DIPHTHONGS_IPA_class, IPA_class)
=======
gothic_rules = []


class Transcriber:
    """
    There are two steps to transcribe words:
        - firstly, a greedy approximation of the pronunciation of word
        - then, use of rules to precise pronunciation of a preprocessed list of transcribed words
    """
    def __init__(self):
        pass

    def main(self, sentence: str, rules) -> str:
        translitterated = []
        sentence = sentence.lower()
        sentence = re.sub(r"[.\";,:\[\]()!&?‘]", "", sentence)
        for word in sentence.split(" "):
            first_res = self.first_process(word)
            second_res = self.second_process(first_res, rules)
            translitterated.append(second_res)
        return "[" + " ".join(translitterated) + "]"

    @staticmethod
    def first_process(word: str):
        """
        Give a greedy approximation of the pronunciation of word
        :param word:
        :return:
        """
        first_res = []
        is_repeted = False
        if len(word) >= 2:
            for index in range(len(word) - 1):
                if is_repeted:
                    is_repeted = False
                    continue
                if word[index:index + 2] in DIPHTHONGS_IPA:  # diphthongs
                    first_res.append(DIPHTHONGS_IPA_class[word[index] + word[index + 1]])
                    is_repeted = True
                elif word[index] == word[index+1]:
                    first_res.append(IPA_class[word[index]].lengthen())
                    is_repeted = True
                else:
                    first_res.append(IPA_class[word[index]])
            if not is_repeted:
                first_res.append(IPA_class[word[len(word) - 1]])
        else:
            first_res.append(IPA_class[word[0]])
        return first_res

    @staticmethod
    def second_process(first_result, rules) -> str:
        """
        Use of rules to precise pronunciation of a preprocessed list of transcribed words
        :param first_result: list(Vowel or Consonant)
        :param rules: list(Rule)
        :return: str
        """
        res = []
        if len(first_result) >= 2:
            for i in range(len(first_result)):
                if i == 0:
                    current_pos = Position("first", None, first_result[i])
                elif i < len(first_result) - 1:
                    current_pos = Position("inner", first_result[i - 1], first_result[i + 1])
                else:
                    current_pos = Position("last", first_result[i - 1], None)
                found = False
                for rule in rules:
                    if rule.temp_sound.ipar == first_result[i].ipar:
                        if rule.apply(current_pos):
                            res.append(rule.estimated_sound.ipar)
                            found = True
                            break
                if not found:
                    res.append(first_result[i].ipar)
        else:
            res.append(first_result[0].ipar)
        return "".join(res)


if __name__ == "__main__":
    example_sentence = "Anastodeins aiwaggeljons Iesuis Xristaus sunaus gudis."
    tr = Transcriber()
>>>>>>> origin/gothic
    ipa_sentence = tr.main(example_sentence, gothic_rules)
    print(ipa_sentence)
