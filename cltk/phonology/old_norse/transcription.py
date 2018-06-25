"""
https://fr.wikipedia.org/wiki/%C3%89criture_du_vieux_norrois

Altnordisches Elementarbuch by Friedrich Ranke and Dietrich Hofmann
"""

import re
from cltk.utils.cltk_logger import logger

__author__ = ["Clément Besnier <clemsciences@gmail.com>"]

# Definition of consonants
PLACES = ["bilabial", "labio-dental", "dental", "alveolar", "post-alveolar", "retroflex", "palatal", "velar", "uvular",
          "glottal"]
MANNERS = ["nasal", "stop", "lateral", "frictative", "trill"]


class AbstractConsonant:
    """
    Used with AbstractPosition to define an environment of a sound
    """
    def __init__(self, place=None, manner=None, voiced=None, ipar=None, geminate=None):
        if place in PLACES or place is None:
            self.place = place
        else:
            logger.error("Incorrect argument")
        if manner in MANNERS or manner is None:
            self.manner = manner
        else:
            logger.error("Incorrect argument")
            raise ValueError
        if type(voiced) == bool or voiced is None:
            self.voiced = voiced
        else:
            logger.error("Incorrect argument")
            raise TypeError
        if type(geminate) == bool or geminate is None:
            self.geminate = geminate
        else:
            logger.error("Incorrect argument")
            raise TypeError
        self.ipar = ipar


class Consonant(AbstractConsonant):
    """
    https://en.wikipedia.org/wiki/Consonant
    A consonant is defined mostly by the its place (where in the vocal tract the obstruction of the consonant occurs,
    and which speech organs are involved), its manner  how air escapes from the vocal tract when the consonant or
    approximant (vowel-like) sound is made), by if it is voiced or not, its length (if it is geminate). An IPA
    transcription is given (https://en.wikipedia.org/wiki/International_Phonetic_Alphabet)
    """
    def __init__(self, place, manner, voiced, ipar, geminate):
        assert place is not None
        assert manner is not None
        assert voiced is not None
        assert ipar is not None
        assert geminate is not None
        AbstractConsonant.__init__(self, place, manner, voiced, ipar, geminate)

    def match(self, abstract_consonant: AbstractConsonant) -> bool:
        """
        A real consonant matches an abstract consonant if and only if the required features of the abstract consonant
        are also features of the real consonant.
        :param abstract_consonant: AbstractConsonant
        :return: bool
        """
        if isinstance(abstract_consonant, AbstractConsonant):
            res = True
            if abstract_consonant.place is not None:
                res = res and abstract_consonant.place == self.place
            if abstract_consonant.manner is not None:
                res = res and abstract_consonant.manner == self.manner
            if abstract_consonant.voiced is not None:
                res = res and abstract_consonant.voiced == self.voiced
            if abstract_consonant.geminate is not None:
                res = res and abstract_consonant.geminate == self.geminate
            return res
        elif abstract_consonant is None:
            return True
        else:
            return False

    def lengthen(self):
        """

        :return: a new lengthened Consonant
        """
        geminate = True
        if not self.geminate:
            ipar = self.ipar + "ː"
        else:
            ipar = self.ipar

        return Consonant(self.place, self.manner, self.voiced, ipar, geminate)


# Vowels
HEIGHT = ["open", "near-open", "open-mid", "mid", "close-mid", "near-close", "close"]
BACKNESS = ["front", "central", "back"]
LENGTHS = ["short", "long", "overlong"]


class AbstractVowel:
    """
    Used with AbstractPosition to define an environment of a sound
    """
    def __init__(self, height=None, backness=None, rounded=None, length=None, ipar=None):
        if height in HEIGHT or height is None:
            self.height = height
        else:
            logger.error("Incorrect argument")
            raise ValueError
        if backness in BACKNESS or backness is None:
            self.backness = backness
        else:
            logger.error("Incorrect argument")
            raise ValueError
        if type(rounded) == bool or rounded is None:
            self.rounded = rounded
        else:
            logger.error("Incorrect argument")
            raise TypeError
        if length in LENGTHS or length is None:
            self.length = length
        else:
            logger.error("Incorrect argument")
            raise ValueError
        self.ipar = ipar


class Vowel(AbstractVowel):
    """
    https://en.wikipedia.org/wiki/Vowel

    """
    def __init__(self, height, backness, rounded, length, ipar):
        assert height is not None
        assert backness is not None
        assert rounded is not None
        assert length is not None
        assert ipar is not None
        AbstractVowel.__init__(self, height, backness, rounded, length, ipar)

    def lengthen(self):
        """

        :return: a new lengthened Vowel
        """
        if self.length == "short":
            length = "long"
            ipar = self.ipar + "ː"
        else:
            ipar = self.ipar
            length = "short"
        return Vowel(self.height, self.backness, self.rounded, length, ipar)

    def match(self, abstract_vowel):
        if isinstance(abstract_vowel, AbstractVowel):
            res = True
            if abstract_vowel.height is not None:
                res = res and abstract_vowel.height == self.height
            if abstract_vowel.backness is not None:
                res = res and abstract_vowel.backness == self.backness
            if abstract_vowel.rounded is not None:
                res = res and abstract_vowel.rounded == self.rounded
            if abstract_vowel.length is not None:
                res = res and abstract_vowel.length == self.length
            return res
        elif abstract_vowel is None:
            return True
        else:
            return False

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
ao = Vowel("open", "back", True, "short", "ɒ")
oo = Vowel("open-mid", "back", True, "short", "ɔ")
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
# θ = Consonant("dental", "frictative", False, "θ")
th = Consonant("dental", "frictative", False, "θ", False)
# ð = Consonant("dental", "frictative", True, "ð")
dh = Consonant("dental", "frictative", True, "ð", False)

OLD_NORSE8_PHONOLOGY = [
    a, ee, e, oe, i, y, ao, oo, u, a.lengthen(),
    e.lengthen(), i.lengthen(), o.lengthen(), u.lengthen(),
    y.lengthen(), b, d, f, g, h, k, l, m, n, p, r, s, t, v, th, dh
]
POSITIONS = ["first", "inner", "last"]


class AbstractPosition:
    """
    This is a position (at the beginning, inside or at the end) that a rule can be applied at,
     a sound or a set of sounds before and a sound or a set of sounds after
    """
    def __init__(self, position, before, after):
        assert position in POSITIONS
        self.position = position
        # assert isinstance(before, AbstractConsonant) or isinstance(before, AbstractVowel)
        self.before = before
        # assert isinstance(after, AbstractConsonant) or isinstance(after, AbstractVowel)
        self.after = after


class Position:
    """
    This is a position (at the beginning, inside or at the end) of a an observed word, a sound before and a sound after
    """
    def __init__(self, position, before, after):
        assert position in POSITIONS
        self.position = position
        assert isinstance(before, Consonant) or isinstance(before, Vowel) or before is None
        self.before = before
        assert isinstance(after, Consonant) or isinstance(after, Vowel) or after is None
        self.after = after

    def real_sound_match_abstract_sound(self, abstract_pos: AbstractPosition) -> bool:
        """
        If an observed position
        :param abstract_pos:
        :return:
        """
        assert isinstance(abstract_pos, AbstractPosition)
        if self.before is not None and self.after is not None:
            return self.position == abstract_pos.position and self.before.match(abstract_pos.before) and \
               self.after.match(abstract_pos.after)
        elif self.before is None and self.after is None:
                return self.position == abstract_pos.position
        elif self.before is None:
            return self.position == abstract_pos.position and self.after.match(abstract_pos.after)
        else:
            return self.position == abstract_pos.position and self.before.match(abstract_pos.before)


class Rule:
    """
    A Rule iz used to transform one sound to another according to its direct environment
    (the letter before and the letter after). If a rule is applicable, then it is applied.
    """
    def __init__(self, position, temp_sound, estimated_sound):
        """

        :param position: AbstractPosition
        :param temp_sound: Vowel or Consonant
        :param estimated_sound: Vowel or Consonant
        """
        assert isinstance(position, AbstractPosition)
        self.position = position
        assert isinstance(temp_sound, Vowel) or isinstance(temp_sound, Consonant)
        self.temp_sound = temp_sound
        assert isinstance(estimated_sound, Vowel) or isinstance(estimated_sound, Consonant)
        self.estimated_sound = estimated_sound

    def apply(self, current_position: Position) -> bool:
        """
        A Rule is applied if and only if a letter has a direct environment (the sound just before and the sound just
        after) which matches the environment of Rule
        :param current_position:
        :return: bool
        """
        return current_position.real_sound_match_abstract_sound(self.position)


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
rule_th = [Rule(AbstractPosition("first", None, None), th, th),
           Rule(AbstractPosition("inner", None, AbstractConsonant(voiced=True)), th, th),
           Rule(AbstractPosition("inner", AbstractConsonant(voiced=True), None), th, th),
           Rule(AbstractPosition("inner", None, None), th, dh),
           Rule(AbstractPosition("last", None, None), th, dh)]


rule_f = [Rule(AbstractPosition("first", None, None), f, f),
          Rule(AbstractPosition("inner", None, AbstractConsonant(voiced=False)), f, f),
          Rule(AbstractPosition("inner", AbstractConsonant(voiced=False), None), f, f),
          Rule(AbstractPosition("inner", None, None), f, v),
          Rule(AbstractPosition("last", None, None), f, v)]
rule_g = [Rule(AbstractPosition("first", None, None), g, g),
          Rule(AbstractPosition("inner", n, None), g, g),
          Rule(AbstractPosition("inner", None, AbstractConsonant(voiced=False)), g, k),
          Rule(AbstractPosition("inner", None, None), g, gh),
          Rule(AbstractPosition("last", None, None), g, gh)]

old_norse_rules = []
old_norse_rules.extend(rule_f)
old_norse_rules.extend(rule_g)
old_norse_rules.extend(rule_th)


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
    example_sentence = "Almáttigr guð skapaði í upphafi himin ok jörð ok alla þá hluti, er þeim fylgja, og " \
                       "síðast menn tvá, er ættir eru frá komnar, Adam ok Evu, ok fjölgaðist þeira kynslóð ok " \
                       "dreifðist um heim allan."
    sentence = "Gylfi konungr var maðr vitr ok fjölkunnigr"
    tr = Transcriber()
    transcribed_sentence = tr.main(example_sentence, old_norse_rules)
    print(transcribed_sentence)
    transcribed_sentence = tr.main(sentence, old_norse_rules)
    print(transcribed_sentence)

