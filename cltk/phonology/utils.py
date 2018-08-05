"""
Factorize code
"""

import re
from cltk.utils.cltk_logger import logger

__author__ = ["Clément Besnier <clemsciences@gmail.com>"]

# Definition of consonants
PLACES = ["bilabial", "labio-dental", "dental", "alveolar", "post-alveolar", "retroflex", "palatal", "velar", "uvular",
          "glottal"]
MANNERS = ["nasal", "stop", "lateral", "frictative", "trill", "spirant"]



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

    def __str__(self):
        return self.ipar


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

    def match_list(self, abstract_consonant_list):
        if type(abstract_consonant_list) == list:
            if len(abstract_consonant_list) == 0:
                return True
            else:
                res = False
                for ac in abstract_consonant_list:
                    if isinstance(ac, AbstractConsonant):
                        res = self.match(ac) or res
                return res
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

    def to_abstract(self):
        return AbstractConsonant(self.place, self.manner, self.voiced, self.ipar, self.geminate)

    def __add__(self, other):
        return Consonant(self.place, self.manner, self.voiced, self.ipar + other.ipar, False)

    def __str__(self):
        return self.ipar


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

    def __str__(self):
        return self.ipar


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

    def match_list(self, abstract_vowel_list):
        if type(abstract_vowel_list) == list:
            if len(abstract_vowel_list) == 0:
                return True
            else:
                res = False
                for av in abstract_vowel_list:
                    if isinstance(av, AbstractVowel):
                        res = self.match(av) or res
                return res
        else:
            return False

    def to_abstract(self):
        return AbstractVowel(self.height, self.backness, self.rounded, self.length, self.ipar)

    # def overlengthen(self):
    #     self.length = "overlong"

    def i_umlaut(self):
        pass

    def u_umlaut(self):
        pass

    def __str__(self):
        return self.ipar


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

    def __eq__(self, other):
        assert isinstance(other, AbstractPosition)
        return self.position == other.position and self.before == other.before and self.after == other.after

    def same_place(self, other):
        assert isinstance(other, AbstractPosition)
        return self.position == other.position

    def __add__(self, other):
        assert self.position == other.position
        if self.before is None and other.before:
            before = None
        elif self.before is None:
            before = other.before
        elif other.before is None:
            before = self.before
        else:
            before = []
            before.extend(self.before)
            before.extend(other.before)
        if self.after is None and other.after is None:
            after = None
        elif self.after is None:
            after = other.after
        elif other.after is None:
            after = self.after
        else:
            after = []
            after.extend(self.after)
            after.extend(other.after)
        return AbstractPosition(self.position, before, after)


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
            return self.position == abstract_pos.position and self.before.match_list(abstract_pos.before) and \
               self.after.match_list(abstract_pos.after)
        elif self.before is None and self.after is None:
                return self.position == abstract_pos.position
        elif self.before is None:
            return self.position == abstract_pos.position and self.after.match_list(abstract_pos.after)
        else:
            return self.position == abstract_pos.position and self.before.match_list(abstract_pos.before)


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

    def can_apply(self, current_position: Position) -> bool:
        """
        A Rule is applied if and only if a letter has a direct environment (the sound just before and the sound just
        after) which matches the environment of Rule
        :param current_position:
        :return: bool
        """
        return current_position.real_sound_match_abstract_sound(self.position)

    def ipa_to_regular_expression(self, phonology):
        """

        :param phonology: list of Vowel or Consonant instances
        :return: pattern which can be the first argument of re.sub
        """
        if self.position.position == "first":
            re_before = r"^"
        elif self.position.before is None:
            re_before = r""
        else:
            re_before = r"(?<=["
            for phoneme in phonology:
                if phoneme.match_list(self.position.before):
                    re_before += phoneme.ipar
            re_before += r"])"

        if self.position.position == "last":
            re_after = r"$"
        elif self.position.after is None:
            re_after = r""
        else:
            re_after = r"(?=["
            for phoneme in phonology:
                if phoneme.match_list(self.position.after):
                    re_after += phoneme.ipar
            re_after += "])"
        return re_before+self.temp_sound.ipar+re_after

    @staticmethod
    def from_regular_expression(re_rule, estimated_sound, ipa_class):
        """

        :param re_rule: pattern (first argument of re.sub)
        :param estimated_sound: an IPA character (second argument of re.sub)
        :param ipa_class: dict whose keys are IPA characters and values are Vowel or Consonant instances
        :return: corresponding Rule instance
        """
        assert len(re_rule) > 0
        if re_rule[0] == "^":
            place = "first"
        elif re_rule[-1] == "$":
            place = "last"
        else:
            place = "inner"

        before_pattern = r"(?<=\(\?\<\=\[)\w*"
        core_pattern = r"(?<=\))\w(?=\(\?\=)|(?<=\^)\w(?=\(\?\=)|(?<=\))\w(?=\$)"
        after_pattern = r"(?<=\(\?\=\[)\w*"
        before_search = re.search(before_pattern, re_rule)
        core_search = re.search(core_pattern, re_rule)
        after_search = re.search(after_pattern, re_rule)
        if before_search is None:
            before = None
        else:
            before = [ipa_class[ipar].to_abstract() for ipar in before_search.group(0)]
        if core_search is not None:
            core = ipa_class[core_search.group(0)]
        else:
            logger.error("No core")
            raise ValueError
        if after_search is None:
            after = None
        else:
            after = [ipa_class[ipar].to_abstract() for ipar in after_search.group(0)]
        abstract_position = AbstractPosition(place, before, after)
        return Rule(abstract_position, core, ipa_class[estimated_sound])

    def __add__(self, other):
        assert isinstance(other, Rule)
        assert self.position.same_place(other.position)
        assert self.temp_sound.ipar == other.temp_sound.ipar
        assert self.estimated_sound.ipar == other.estimated_sound.ipar
        position = self.position + other.position
        return Rule(position, self.temp_sound, self.estimated_sound)


class Transcriber:
    """
    There are two steps to transcribe words:
        - firstly, a greedy approximation of the pronunciation of word
        - then, use of rules to precise pronunciation of a preprocessed list of transcribed words
    """
    def __init__(self, diphthongs_ipa, diphthongs_ipa_class, ipa_class, rules):
        """

        :param diphthongs_ipa: dict whose keys are written diphthongs and and values IPA trasncription of them
        :param diphthongs_ipa_class: dict whose keys are written diphthongs and and values are Vowel instances
        :param ipa_class: dict whose keys are written characters and and values are Vowel or Consonant instances
        :param rules: list of Rule instances
        """
        self.diphthongs_ipa = diphthongs_ipa
        self.diphthongs_ipa_class = diphthongs_ipa_class
        self.ipa_class = ipa_class
        self.rules = rules

    def main(self, sentence: str) -> str:
        translitterated = []
        sentence = sentence.lower()
        sentence = re.sub(r"[.\";,:\[\]()!&?‘]", "", sentence)
        for word in sentence.split(" "):
            first_res = self.first_process(word)
            second_res = self.second_process(first_res)
            translitterated.append(second_res)
        return "[" + " ".join(translitterated) + "]"

    def first_process(self, word: str):
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
                if word[index:index + 2] in self.diphthongs_ipa:  # diphthongs
                    first_res.append(self.diphthongs_ipa_class[word[index] + word[index + 1]])
                    is_repeted = True
                elif word[index] == word[index+1]:
                    first_res.append(self.ipa_class[word[index]].lengthen())
                    is_repeted = True
                else:
                    first_res.append(self.ipa_class[word[index]])
            if not is_repeted:
                first_res.append(self.ipa_class[word[len(word) - 1]])
        else:
            first_res.append(self.ipa_class[word[0]])
        return first_res

    def second_process(self, first_result) -> str:
        """
        Use of rules to precise pronunciation of a preprocessed list of transcribed words
        :param first_result: list(Vowel or Consonant)
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
                for rule in self.rules:
                    if rule.temp_sound.ipar == first_result[i].ipar:
                        if rule.can_apply(current_pos):
                            res.append(rule.estimated_sound.ipar)
                            found = True
                            break
                if not found:
                    res.append(first_result[i].ipar)
        else:
            res.append(first_result[0].ipar)
        return "".join(res)
