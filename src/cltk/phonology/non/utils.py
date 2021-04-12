"""To define sounds, phonetic rules for phonetic transcription.
"""

import re
from enum import Enum, auto

from cltk.core.cltk_logger import logger

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class AutoName(Enum):
    def _generate_next_value_(name, a, b, d):
        return name


# Definition of consonants
class Manner(AutoName):
    nasal = auto()
    stop = auto()
    lateral = auto()
    fricative = auto()
    trill = auto()
    spirant = auto()
    affricate = auto()
    approximant = auto()


class Place(AutoName):
    bilabial = auto()
    labio_dental = auto()
    dental = auto()
    alveolar = auto()
    post_alveolar = auto()
    retroflex = auto()
    palatal = auto()
    velar = auto()
    uvular = auto()
    glottal = auto()


class AbstractConsonant:
    """
    Used with AbstractPosition to define an environment of a sound
    """

    def __init__(self, place=None, manner=None, voiced=None, ipar=None, geminate=None):
        if isinstance(place, Place) or place is None:
            self.place = place
        else:
            logger.error("Incorrect argument")
        if isinstance(manner, Manner) or manner is None:
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
    """A `consonant <https://en.wikipedia.org/wiki/Consonant>`_ is defined mostly by the its place (where in the vocal tract the obstruction of the consonant occurs,
    and which speech organs are involved), its manner  how air escapes from the vocal tract when the consonant or
    approximant (vowel-like) sound is made), by if it is voiced or not, its length (if it is geminate). An IPA
    standard is at: <https://en.wikipedia.org/wiki/International_Phonetic_Alphabet>_.
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
        return AbstractConsonant(
            self.place, self.manner, self.voiced, self.ipar, self.geminate
        )

    def __add__(self, other):
        return Consonant(
            self.place, self.manner, self.voiced, self.ipar + other.ipar, False
        )

    def __str__(self):
        return self.ipar

    __repr__ = __str__

    def is_equal(self, other_consonnant):
        """
        >>> v_consonant = Consonant(Place.labio_dental, Manner.fricative, True, "v", False)
        >>> f_consonant = Consonant(Place.labio_dental, Manner.fricative, False, "f", False)
        >>> v_consonant.is_equal(f_consonant)
        False

        :param other_consonnant:
        :return:
        """
        return (
            self.place == other_consonnant.place
            and self.manner == other_consonnant.manner
            and self.voiced == other_consonnant.voiced
            and self.geminate == other_consonnant.geminate
        )


# Vowels
class Height(AutoName):
    open = auto()
    near_open = auto()
    open_mid = auto()
    mid = auto()
    close_mid = auto()
    near_close = auto()
    close = auto()


class Backness(AutoName):
    front = auto()
    central = auto()
    back = auto()


class Length(AutoName):
    short = auto()
    long = auto()
    overlong = auto()


class AbstractVowel:
    """
    Used with AbstractPosition to define an environment of a sound
    """

    def __init__(
        self, height=None, backness=None, rounded=None, length=None, ipar=None
    ):
        if isinstance(height, Height) or height is None:
            self.height = height
        else:
            logger.error("Incorrect argument")
            raise ValueError
        if isinstance(backness, Backness) or backness is None:
            self.backness = backness
        else:
            logger.error("Incorrect argument")
            raise ValueError
        if type(rounded) == bool or rounded is None:
            self.rounded = rounded
        else:
            logger.error("Incorrect argument")
            raise TypeError
        if isinstance(length, Length) or length is None:
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
        if self.length == Length.short:
            length = Length.long
            ipar = self.ipar + "ː"
        else:
            ipar = self.ipar
            length = Length.short
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
        return AbstractVowel(
            self.height, self.backness, self.rounded, self.length, self.ipar
        )

    # def overlengthen(self):
    #     self.length = "overlong"

    def i_umlaut(self):
        pass

    def u_umlaut(self):
        pass

    def __str__(self):
        return self.ipar

    __repr__ = __str__

    def is_equal(self, other_sound):
        """

        :param other_sound:
        :return:
        """
        return (
            self.height == other_sound.height
            and self.backness == other_sound.backness
            and self.rounded == other_sound.rounded
            and self.length == other_sound.length
        )

    def __add__(self, other):
        return Vowel(
            self.height,
            self.backness,
            self.rounded,
            self.length,
            self.ipar + other.ipar,
        )


class Rank(AutoName):
    first = auto()
    inner = auto()
    last = auto()


class AbstractPosition:
    """
    This is a position (at the beginning, inside or at the end) that a rule can be applied at,
     a sound or a set of sounds before and a sound or a set of sounds after
    """

    def __init__(self, position, before, after):
        assert isinstance(position, Rank)

        self.position = position
        # assert isinstance(before, AbstractConsonant) or isinstance(before, AbstractVowel)
        self.before = before
        # assert isinstance(after, AbstractConsonant) or isinstance(after, AbstractVowel)
        self.after = after

    def __eq__(self, other):
        assert isinstance(other, AbstractPosition)
        return (
            self.position == other.position
            and self.before == other.before
            and self.after == other.after
        )

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
        assert isinstance(position, Rank)
        self.position = position
        assert (
            isinstance(before, Consonant) or isinstance(before, Vowel) or before is None
        )
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
            return (
                self.position == abstract_pos.position
                and self.before.match_list(abstract_pos.before)
                and self.after.match_list(abstract_pos.after)
            )
        elif self.before is None and self.after is None:
            return self.position == abstract_pos.position
        elif self.before is None:
            return self.position == abstract_pos.position and self.after.match_list(
                abstract_pos.after
            )
        else:
            return self.position == abstract_pos.position and self.before.match_list(
                abstract_pos.before
            )


class Rule:
    """
    A Rule is used to transform one sound to another according to its direct environment
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
        assert isinstance(estimated_sound, Vowel) or isinstance(
            estimated_sound, Consonant
        )
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
        if self.position.position == Rank.first:
            re_before = r"^"
        elif self.position.before is None:
            re_before = r""
        else:
            re_before = r"(?<=["
            for phoneme in phonology:
                if phoneme.match_list(self.position.before):
                    re_before += phoneme.ipar
            re_before += r"])"

        if self.position.position == Rank.last:
            re_after = r"$"
        elif self.position.after is None:
            re_after = r""
        else:
            re_after = r"(?=["
            for phoneme in phonology:
                if phoneme.match_list(self.position.after):
                    re_after += phoneme.ipar
            re_after += "])"
        return re_before + self.temp_sound.ipar + re_after

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
            place = Rank.first
        elif re_rule[-1] == "$":
            place = Rank.last
        else:
            place = Rank.inner

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

    def __init__(
        self,
        diphthongs_ipa: dict,
        diphthongs_ipa_class: dict,
        ipa_class: dict,
        rules: list,
    ):
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

    def word_to_phonetic_representation(self, word, with_squared_brackets=True):
        """

        :param word: normalized word
        :param with_squared_brackets:
        :return:
        """
        phonemes = self.text_to_phonemes(word)
        phonetic_representation = self.phonemes_to_phonetic_representation(phonemes)
        if with_squared_brackets:
            return f"[{phonetic_representation}]"
        return phonetic_representation

    def text_to_phonetic_representation(
        self, sentence: str, with_squared_brackets=True
    ) -> str:
        """

        :param sentence:
        :param with_squared_brackets:
        :return:
        """
        transliterated = []
        sentence = sentence.lower()
        sentence = re.sub(r"[.\";,:\[\]()!&?‘]", "", sentence)
        for word in sentence.split(" "):
            transliterated.append(self.word_to_phonetic_representation(word, False))
        if with_squared_brackets:
            return "[" + " ".join(transliterated) + "]"
        return " ".join(transliterated)

    def text_to_phonemes(self, word: str) -> list:
        """
        Give a greedy approximation of the pronunciation of word
        :param word:
        :return:
        """
        phonemes = []
        is_repeated = False
        if len(word) >= 2:
            for index in range(len(word) - 1):
                if is_repeated:
                    is_repeated = False
                    continue
                if word[index : index + 2] in self.diphthongs_ipa:  # diphthongs
                    phonemes.append(
                        self.diphthongs_ipa_class[word[index] + word[index + 1]]
                    )
                    is_repeated = True
                elif word[index] == word[index + 1]:
                    phonemes.append(self.ipa_class[word[index]].lengthen())
                    is_repeated = True
                else:
                    phonemes.append(self.ipa_class[word[index]])
            if not is_repeated:
                phonemes.append(self.ipa_class[word[len(word) - 1]])
        else:
            phonemes.append(self.ipa_class[word[0]])
        return phonemes

    def phonemes_to_phonetic_representation(self, phonemes: list) -> str:
        """
        Use of rules to precise pronunciation of a preprocessed list of transcribed words
        :param phonemes: list(Vowel or Consonant)
        :return: str
        """
        phonetic_representation = []
        if len(phonemes) >= 2:
            for i in range(len(phonemes)):
                if i == 0:
                    current_pos = Position(Rank.first, None, phonemes[i])
                elif i < len(phonemes) - 1:
                    current_pos = Position(Rank.inner, phonemes[i - 1], phonemes[i + 1])
                else:
                    current_pos = Position(Rank.last, phonemes[i - 1], None)
                found = False
                for rule in self.rules:
                    if rule.temp_sound.ipar == phonemes[i].ipar:
                        if rule.can_apply(current_pos):
                            phonetic_representation.append(rule.estimated_sound.ipar)
                            found = True
                            break
                if not found:
                    phonetic_representation.append(phonemes[i].ipar)
        else:
            phonetic_representation.append(phonemes[0].ipar)
        return "".join(phonetic_representation)


class BasePhonologicalRule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def perform_action(self, phonemes, pos):
        return self.action(phonemes[pos])

    def __call__(self, phonemes, pos):
        return self.perform_action(phonemes, pos)


class PhonologicalRule(BasePhonologicalRule):
    def check_environment(self, phonemes, pos):
        before = phonemes[pos - 1] if pos > 0 else None
        after = phonemes[pos + 1] if pos < len(phonemes) - 1 else None
        return self.condition(before, phonemes[pos], after)


class WordInitialPhonologicalRule(BasePhonologicalRule):
    def check_environment(self, phonemes, pos):
        return (
            self.condition(phonemes[0], phonemes[1])
            if pos == 0 and len(phonemes) > 1
            else False
        )

    def perform_action(self, phonemes, _):
        return self.action(phonemes[0])


class WordFinalPhonologicalRule(BasePhonologicalRule):
    def check_environment(self, phonemes, pos):
        last = len(phonemes) - 1
        return (
            self.condition(phonemes[last - 1], phonemes[last])
            if pos == last and len(phonemes) > 1
            else False
        )

    def perform_action(self, phonemes, _):
        return self.action(phonemes[len(phonemes) - 2])


class IPATranscriber:
    def __init__(self, digraphs: dict, dipthongs: dict, alphabet: dict, rules: list):
        self.digraphs = digraphs
        self.dipthongs = dipthongs
        self.alphabet = alphabet
        self.rules = rules

    @staticmethod
    def tokenize(text):
        text = text.lower()
        text = re.sub(r"[.\";,:\[\]()!&?‘]", "", text)
        return text.split(" ")

    def transcribe_word(self, word):
        phonemes = [self.alphabet[letter] for letter in word]
        for i in range(len(phonemes)):
            for rule in self.rules:
                if rule.check_environment(phonemes, i):
                    phonemes[i] = rule(phonemes, i)
        return phonemes

    def transcribe(self, text):
        return [self.transcribe_word(word) for word in self.tokenize(text)]
