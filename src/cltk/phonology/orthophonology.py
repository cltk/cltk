"""
A module for representing the orthophonology of a language:
the mapping from orthographic representations to IPA symbols.

Pre-modern languages are characterized by their non-standardized writing rules.
Writers attempt to follow rules that fit morphology (words of same family tend to have close spelling)
and phonology (words of similar pronunciations are written the same way).
As languages evolve, their phonology changes faster than their writing rules.
This module aims to unify writing rules with phonological rules by borrowing
the representation of sound changes used by historical linguistics.

Based on many ideas in cltk.phonology.non.utils by Clément Besnier <clem@clementbesnier.fr>.
"""

import re
from copy import deepcopy
from enum import auto
from typing import Union

from cltk.utils.utils import CLTKEnum

# The list of features and their values are from the IPA charts.
# Features for non-pulmonic consonants (e.g. clicks, implosives) are not yet provided.


__author__ = [
    "John Stewart <johnstewart@aya.yale.edu>",
    "Clément Besnier <clem@clementbesnier.fr>",
]


# ------------------- Phonological Features -------------------


class PhonologicalFeature(CLTKEnum):
    def __sub__(self, other):
        return make_phoneme(self) - other

    def __rshift__(self, other):
        return make_phoneme(self) >> other

    def __le__(self, other):
        return make_phoneme(self) <= other

    def __ge__(self, other):
        return make_phoneme(self) >= other

    def matches(self, other):
        return make_phoneme(self).matches(other)

    def __floordiv__(self, other):
        return make_phoneme(self) // other


class Consonantal(PhonologicalFeature):
    neg = auto()
    pos = auto()


class Voiced(PhonologicalFeature):
    neg = auto()
    pos = auto()


class Aspirated(PhonologicalFeature):
    neg = auto()
    pos = auto()


class Geminate(PhonologicalFeature):
    neg = auto()
    pos = auto()


class Roundedness(PhonologicalFeature):
    neg = auto()
    pos = auto()


class Length(PhonologicalFeature):
    short = auto()
    long = auto()
    overlong = auto()


# order for Height, Backness, and Manner is important
# the feature values must be ordered by *increasing sonority*
class Height(PhonologicalFeature):
    close = auto()
    near_close = auto()
    close_mid = auto()
    mid = auto()
    open_mid = auto()
    near_open = auto()
    open = auto()


class Backness(PhonologicalFeature):
    front = auto()
    central = auto()
    back = auto()


class Manner(PhonologicalFeature):
    stop = auto()
    fricative = auto()
    affricate = auto()
    nasal = auto()
    lateral = auto()
    trill = auto()
    spirant = auto()
    approximant = auto()


class Place(PhonologicalFeature):
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


# ------------------- Phonemes -------------------


class AbstractPhoneme:
    """
    An abstract phoneme is just a bundle of phonological features.
    """

    def __init__(self, features=None, ipa=None):
        features = {} if features is None else features

        # ensure unique features
        if len(set(features.keys())) != len(features.keys()):
            raise ValueError("non-unique features")

        # ensure feature values correctly match their types
        # this is a barbaric bit of type checking that the language should provide
        for feature_name, feature_value in features.items():
            if not issubclass(feature_name, PhonologicalFeature):
                raise TypeError(str(feature_name) + " is not a phonological feature")
            if type(feature_value) != feature_name:
                raise TypeError(str(feature_value) + " is not a " + str(feature_name))

        self.features = features
        self.ipa = ipa

    def is_vowel(self):
        return self[Consonantal] == Consonantal.neg

    def merge(self, other):
        """
        Returns a *copy* of this phoneme, with the features of other merged into this feature bundle.
        Other can be a list of phonemes, in which case the list is returned (for technical reasons).
        Other may also be a single feature value or a list of feature values.
        """
        phoneme = deepcopy(self)

        # special case for list of phonemes
        if (
            isinstance(other, list)
            and len(other) > 0
            and isinstance(other[0], AbstractPhoneme)
        ):
            return other

        if isinstance(other, AbstractPhoneme):
            feature_values = other.features.values()
        elif type(other) != list and type(other) != tuple:
            feature_values = [other]
        else:
            feature_values = other

        for f in feature_values:
            if type(f) == list:
                for inner_f in f:
                    phoneme[type(inner_f)] = inner_f
            elif isinstance(f, AbstractPhoneme):
                phoneme = phoneme << f
            else:
                phoneme[type(f)] = f

        if isinstance(other, AbstractPhoneme) and other.ipa is not None:
            phoneme.ipa = other.ipa

        return phoneme

    def is_equal(self, other):
        """
        Phonemes are equal if they share the same features.
        Note that the IPA symbol is *not* taken into account.
        """
        return other is not None and self.features == other.features

    def matches(self, other):
        """
        This phoneme matches other if other contains all the features of this phoneme,
        i.e. if this phoneme has an improper subset of other's.
        If other is a disjunctive list, then a match is sought for any of the list.
        If other is a feature value or list of feature values, it is promoted to a phoneme first.
        """
        if other is None:
            return False
        if isinstance(other, PhonemeDisjunction):
            return any([self <= phoneme for phoneme in other])
        if isinstance(other, list) or isinstance(other, PhonologicalFeature):
            other = make_phoneme(other)
        return other.features.items() >= self.features.items()

    def __getitem__(self, feature_name):
        """
        Use dict-type syntax for accessing the values of features.
        """
        if not issubclass(feature_name, PhonologicalFeature):
            raise TypeError(str(feature_name) + " is not a phonological feature")
        return self.features.get(feature_name, None)

    def __setitem__(self, feature_name, feature_value):
        """
        Use dict-type syntax to set the value of features.
        """
        if not issubclass(feature_name, PhonologicalFeature):
            raise TypeError(str(feature_name) + " is not a phonological feature")
        if type(feature_value) != feature_name:
            raise TypeError(str(feature_value) + " is not a " + str(feature_name))
        self.features[feature_name] = feature_value
        return self

    def __str__(self):
        return ("IPA:{0} ".format(self.ipa) if self.ipa is not None else "") + " ".join(
            [str(v) for v in self.features.values()]
        )

    __repr__ = __str__

    def __eq__(self, other):
        return self.is_equal(other)

    def __le__(self, other):
        return self.matches(other)

    def __ge__(self, other):
        if type(other) == list:
            other = make_phoneme(other)
        return other.matches(self)

    def __lt__(self, other):
        return other.is_more_sonorous(self)

    def __gt__(self, other):
        return self.is_more_sonorous(other)

    def __rshift__(self, other):
        """
        Creates a phonological rule, merging other with self when applied
        to phonemes matching self.
        """
        return PhonologicalRule(
            condition=lambda _, target, __: self <= target,
            action=lambda target: target << other,
        )

    def __lshift__(self, other):
        return self.merge(other)

    def __sub__(self, other):
        """
        Creates environment functions: boolean functions of the position before and after the target.
        """
        other = (
            make_phoneme(other)
            if not (
                isinstance(other, AbstractPhoneme)
                or isinstance(other, PhonemeDisjunction)
            )
            else other
        )
        env_start = PositionedPhoneme(self, env_start=True)
        env_end = PositionedPhoneme(other, env_end=True)
        return lambda before, _, after: env_start <= before and env_end <= after

    def __floordiv__(self, other):
        """
        Creates disjunctive lists of phonemes.
        """
        return PhonemeDisjunction(self, other)


def make_phoneme(*feature_values) -> AbstractPhoneme:
    """
    Creates an abstract phoneme made of the feature specifications given in the vararg.
    """
    phoneme = AbstractPhoneme({})
    phoneme = phoneme << feature_values
    return phoneme


def PositionedPhoneme(
    phoneme,
    word_initial=False,
    word_final=False,
    syllable_initial=False,
    syllable_final=False,
    env_start=False,
    env_end=False,
):
    """
    A decorator for phonemes, used in applying rules over words.
    Returns a copy of the input phoneme, with additional attributes,
    specifying whether the phoneme occurs at a word or syllable boundary,
    or its position in an environment.
    """

    pos_phoneme = deepcopy(phoneme)
    pos_phoneme.word_initial = word_initial
    pos_phoneme.word_final = word_final
    pos_phoneme.syllable_initial = syllable_initial
    pos_phoneme.syllable_final = syllable_final
    pos_phoneme.env_start = env_start
    pos_phoneme.env_end = env_end

    return pos_phoneme


class AlwaysMatchingPseudoPhoneme(AbstractPhoneme):
    """
    A pseudo-phoneme that matches all other phonemes.
    """

    def __init__(self):
        AbstractPhoneme.__init__(self, ipa="*")

    def matches(self, other: AbstractPhoneme) -> bool:
        return True


class WordBoundaryPseudoPhoneme(AbstractPhoneme):
    """
    A pseudo-phoneme that only matches at the start or end of a word.
    """

    def __init__(self):
        AbstractPhoneme.__init__(self, ipa="#")

    def matches(self, other) -> bool:
        return other is None

    def is_equal(self, other) -> bool:
        return self is other


class SyllableBoundaryPseudoPhoneme(AbstractPhoneme):
    """
    A pseudo-phoneme that matches at word boundaries
    and matches positioned phonemes that are at syllable boundaries.
    """

    def __init__(self):
        AbstractPhoneme.__init__(self, ipa="$")

    def matches(self, other) -> bool:
        if other is None:
            return True
        elif getattr(self, "env_start", False) and getattr(
            other, "syllable_final", False
        ):
            return True
        elif getattr(self, "env_end", False) and getattr(
            other, "syllable_initial", False
        ):
            return True
        else:
            return False


ANY = AlwaysMatchingPseudoPhoneme()
W = WordBoundaryPseudoPhoneme()
S = SyllableBoundaryPseudoPhoneme()


class PhonemeDisjunction(list):
    """
    A list of phonemes, with special properties for disjunctive ("or") matching.
    """

    def __init__(self, *phonemes):
        super().__init__(self)
        if any(
            [
                not isinstance(p, AbstractPhoneme)
                and not isinstance(p, PhonologicalFeature)
                and not isinstance(p, list)
                for p in phonemes
            ]
        ):
            raise TypeError(phonemes)
        true_phonemes = [
            make_phoneme(p) if not isinstance(p, AbstractPhoneme) else p
            for p in phonemes
        ]
        self.extend(true_phonemes)

    def __floordiv__(self, other):
        """
        Adds other to this list of phonemes.
        If other is a feature or list of features it is promoted to a phoneme.
        """
        other = (
            make_phoneme(other)
            if (isinstance(other, PhonologicalFeature) or isinstance(other, list))
            else other
        )
        if isinstance(other, AbstractPhoneme):
            self.append(other)
            return self
        else:
            raise TypeError(other)

    def __rshift__(self, other):
        """
        Creates a phonological rule that fires when any member of the list matches the target.
        """
        return PhonologicalRule(
            condition=lambda _, target, __: any(
                [phoneme <= target for phoneme in self]
            ),
            action=lambda target: target << other,
        )

    def matches(self, other) -> bool:
        """
        A disjunctive list matches a phoneme if any of its members matches the phoneme.
        If other is also a disjunctive list, any match between this list and the other returns true.
        """
        if other is None:
            return False
        if isinstance(other, PhonemeDisjunction):
            return any([phoneme.matches(other) for phoneme in self])
        if isinstance(other, list) or isinstance(other, PhonologicalFeature):
            other = make_phoneme(other)
        return any([phoneme <= other for phoneme in self])

    def __sub__(self, other):
        """
        Creates a boolean environmental function whose before is this list of phonemes.
        """
        other = (
            make_phoneme(other)
            if not (
                isinstance(other, AbstractPhoneme)
                or isinstance(other, PhonemeDisjunction)
            )
            else other
        )
        env_start = [PositionedPhoneme(phoneme, env_start=True) for phoneme in self]
        env_end = PositionedPhoneme(other, env_end=True)
        return (
            lambda before, _, after: any([phoneme <= before for phoneme in env_start])
            and env_end <= after
        )

    def __le__(self, other):
        return False if other is None else self.matches(other)

    def __ge__(self, other):
        return False if other is None else other.matches(self)


class Consonant(AbstractPhoneme):
    """
    Based on cltk.phonology.utils by @clemsciences.
    A consonant is a phoneme that is specified for the features listed in the IPA chart for consonants:
    Place, Manner, Voicing.  These may be read directly off the IPA chart, which also gives the IPA symbol.
    The Consonantal feature is set to positive, and the aspirated is defaulted to negative.
    See http://www.ipachart.com/
    """

    def __init__(
        self, place, manner, voiced, ipa, geminate=Geminate.neg, aspirated=Aspirated.neg
    ):
        assert place is not None
        assert manner is not None
        assert voiced is not None
        assert geminate is not None
        assert ipa is not None

        AbstractPhoneme.__init__(
            self,
            {
                Consonantal: Consonantal.pos,
                Place: place,
                Manner: manner,
                Voiced: voiced,
                Aspirated: aspirated,
                Geminate: geminate,
            },
            ipa,
        )

    def is_more_sonorous(self, other) -> bool:
        """
        compare this phoneme to another for sonority.
        Used for SSP considerations.
        """
        return (
            True
            if isinstance(other, Consonant) and self[Manner] > other[Manner]
            else False
        )

    def merge(self, other):
        if isinstance(other, Vowel):
            return other
        else:
            return AbstractPhoneme.merge(self, other)

    def geminate(self):
        """
        Returns a new Consonant with its Geminate pos,
        and "ː" appended to its IPA symbol.
        """
        consonant = deepcopy(self)

        if consonant[Geminate] == Geminate.neg:
            consonant[Geminate] = Geminate.pos
            consonant.ipa += "ː"
        return consonant


class Vowel(AbstractPhoneme):
    """
    The representation of a vowel by its features, as given in the IPA chart for vowels.
    See http://www.ipachart.com/
    """

    def __init__(self, height, backness, rounded, length, ipa):
        assert height is not None
        assert backness is not None
        assert rounded is not None
        assert length is not None
        assert ipa is not None

        AbstractPhoneme.__init__(
            self,
            {
                Consonantal: Consonantal.neg,
                Height: height,
                Backness: backness,
                Roundedness: rounded,
                Length: length,
            },
            ipa,
        )

    def __add__(self, other):
        """
        Summed vowels produce diphthongs, returning a copy of the first vowel
        and the concatenation of the IPA symbols.
        A hack because the features of the second vowel are lost.
        """
        diphthong = deepcopy(self)
        diphthong.ipa += other.ipa
        return diphthong

    def lengthen(self):
        """
        Returns a new Vowel with its Length lengthened,
        and "ː" appended to its IPA symbol.
        """
        vowel = deepcopy(self)

        if vowel[Length] == Length.short:
            vowel[Length] = Length.long
        elif vowel[Length] == Length.long:
            vowel[Length] = Length.overlong

        vowel.ipa += "ː"
        return vowel

    def is_more_sonorous(self, other) -> bool:
        """
        compare this phoneme to another for sonority.
        Used for SSP considerations.
        """
        if isinstance(other, Consonant):
            return True
        elif self[Height] > other[Height]:
            return True
        elif self[Height] == other[Height]:
            return self[Backness] > other[Backness]
        else:
            return False

    def merge(self, other):
        if isinstance(other, Consonant):
            return other
        else:
            return AbstractPhoneme.merge(self, other)


# ------------------- Phonological Rule Templates -------------------


class BasePhonologicalRule:
    """
    Base class for conditional phonological rules.
    A phonological rule relates an item (a phoneme) to its environment to define a transformation.
    Specifically, a rule specifies a condition and an action.

    * The condition characterizes the phonological environment of a phoneme in terms of the
      characteristics of the phomeme before it (if any), and after it (if any).
      In general it is a function taking three arguments: before, target, after, the phonemes in the environment,
      an returning a boolean for whether the rule should fire.
    * The action defines a transformation of the target phoneme, e.g. its vocalization.
      It is a function taking only the action, which returns the replacement phoneme OR a *list* of phonemes.

    """

    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def perform_action(self, phonemes, pos):
        return self.action(phonemes[pos])

    def __call__(self, phonemes, pos):
        return self.perform_action(phonemes, pos)

    def __or__(self, other_condition):
        prev_function = self.condition
        self.condition = lambda before, target, after: prev_function(
            before, target, after
        ) and other_condition(before, target, after)
        return self


class PhonologicalRule(BasePhonologicalRule):
    """
    The most general phonological rule can apply anywhere in the word.
    before and after phonemes may therefore be null when calling the condition.
    """

    def check_environment(self, phonemes, pos):
        if pos >= len(phonemes):
            return False

        before = None if pos == 0 else phonemes[pos - 1]
        after = None if pos == len(phonemes) - 1 else phonemes[pos + 1]
        return self.condition(before, phonemes[pos], after)


# ------------------- The ortho-phonology of a language -------------------#


class PhonemeNotFound(Exception):
    """
    Exception raised when a search for a phoneme in the investory fails.
    """

    def __init__(self, phoneme):
        self.unfound_phoneme = phoneme


class LetterNotFound(Exception):
    """
    Exception raised when a search for a letter in the alphabet fails.
    """

    def __init__(self, letter):
        self.unfound_letter = letter


# A mapping of IPA symbols to English orthographic approximations.
# Thousands of problems here.
ipa_to_pde = {
    "m": "m",
    "n": "n",
    "n̥": "ng",
    "ŋ": "ng",
    "p": "p",
    "b": "b",
    "t": "t",
    "d": "d",
    "k": "k",
    "g": "g",
    "t͡ʃ": "ch",
    "d͡ʒ": "ge",
    "f": "f",
    "v": "v",
    "θ": "th",
    "ð": "th",
    "s": "s",
    "z": "z",
    "ʃ": "sh",
    "ç": "ch",
    "x": "ch",  # tough one -- like in Scottish loch
    "y": "y",
    "h": "h",
    "l": "l",
    "l̥": "l",
    "j": "y",
    "w": "w",
    "r": "r",
    "r̥": "r",
    "i": "i",
    "i:": "ee",
    "y:": "y",
    "u": "u",
    "u:": "oo",
    "e": "e",
    "e:": "ee",
    "ø": "e",
    "ø:": "ee",
    "o": "o",
    "o:": "oo",
    "æ": "a",
    "æ:": "aa",
    "ɑ": "o",
    "ɑ:": "oo",
    "æɑ": "ao",
    "æ:ɑ": "ao",
    "eo": "eo",
    "e:o": "eeo",
    "iu": "iu",
    "i:u": "iiu",
}

# this is just the barest of beginnings!
pde_phonotactics = [(r"(^|(?<= ))hw", "wh"), (r"oo(.)(^|(?= ))", "o\\1e")]


class Orthophonology:
    """
    The ortho-phonology of a language is described by:

    * The inventory of all the phonemes of the language.
    * A mapping of orthographic symbols to phonemes.
    * mappings of orthographic symbols pairs to:

      * diphthongs
      * phonemes (i.e. digraphs)

    * phonological rules for the contextual transformation of phonological representations.

    The class is very clearly aimed at alphabetic orthographies.
    Its usefulness for e.g. pictographic orthographies is questionable.
    """

    def __init__(
        self,
        sound_inventory,
        alphabet,
        diphthongs,
        digraphs,
        to_modern=(ipa_to_pde, pde_phonotactics),
    ):
        self.sound_inventory = sound_inventory
        self.alphabet = alphabet
        self.diphthongs = diphthongs
        self.digraphs = digraphs
        self.di = {**self.diphthongs, **self.digraphs}
        self.rules = []
        self.to_modern = to_modern

    def add_rule(self, rule):
        """
        Adds a rule to the orthophonology.
        The *order* in which rules are added is critcial, since the first rule that matches fires."""
        self.rules.append(rule)

    # these are not static because language-specific subclasses probably need access to the sound inventory
    def is_syllable_initial(self, phonemes, pos) -> bool:
        if pos == len(phonemes) - 1:
            return False
        # start of word is always syllable-initial, otherwise use SSP
        return pos == 0 or (
            phonemes[pos - 1].is_more_sonorous(phonemes[pos])
            and not phonemes[pos].is_more_sonorous(phonemes[pos + 1])
        )

    def is_syllable_final(self, phonemes, pos) -> bool:
        # end of word is always syllable-final, otherwise use SSP
        return pos == len(phonemes) - 1 or self.is_syllable_initial(phonemes, pos + 1)

    @staticmethod
    def _tokenize(text):
        text = text.lower()
        text = re.sub(r"[.\";,:\[\]()!&?‘]", "", text)
        return text.split(" ")

    def _position_phonemes(self, phonemes):
        """
        Mark syllable boundaries, and, in future, other positional/suprasegmental features?
        """
        for i in range(len(phonemes)):
            phonemes[i] = PositionedPhoneme(phonemes[i])
            phonemes[i].syllable_initial = self.is_syllable_initial(phonemes, i)
            phonemes[i].syllable_final = self.is_syllable_final(phonemes, i)

        return phonemes

    def _find_sound(self, phoneme):
        for sound in self.sound_inventory:
            if sound.is_equal(phoneme):
                return sound
        raise PhonemeNotFound(phoneme)

    def transcribe_word(self, word):
        """
        The heart of the transcription process.
        Similar to the system in in cltk.phonology.utils, the algorithm:
        1) Applies digraphs and diphthongs to the text of the word.
        2) Carries out a naive ("greedy", per @clemsciences) substitution of letters to phonemes,
        according to the alphabet.
        3) Applies the conditions of the rules to the environment of each phoneme in turn.
        The first rule matched fires.  There is no restart and later rules are not tested.
        Also, if a rule returns multiple phonemes, these are never re-tested by the rule set.
        """
        phonemes = []

        i = 0
        while i < len(word):
            # check for digraphs and diphthongs
            if i < len(word) - 1 and word[i : i + 2] in self.di:
                letter_pair = word[i : i + 2]
                replacement = self.di[letter_pair]
                replacement = (
                    replacement if isinstance(replacement, list) else [replacement]
                )
                phonemes.extend(replacement)
                i += 2
            else:
                phonemes.append(self[word[i]])
                i += 1

        # apply phonological rules.  Note: no restart!
        i = 0
        while i < len(phonemes):
            for rule in self.rules:
                phonemes = self._position_phonemes(phonemes)

                if rule.check_environment(phonemes, i):
                    replacement = rule(phonemes, i)
                    replacement = (
                        [replacement]
                        if not isinstance(replacement, list)
                        else replacement
                    )
                    new_phonemes = [self._find_sound(p) for p in replacement]
                    phonemes[i : i + 1] = new_phonemes
                    i += len(replacement) - 1
                    break
            i += 1

        return phonemes

    def transcribe(self, text: str, as_phonemes=False) -> Union[str, list]:
        """
        Transcribes a text, which is first tokenized for words, then each word is transcribed.
        If as_phonemes is true, returns a list of list of phoneme objects,
        else returns a string concatenation of the IPA symbols of the phonemes.
        """
        phoneme_words = [self.transcribe_word(word) for word in self._tokenize(text)]
        if not as_phonemes:
            words = [
                "".join([phoneme.ipa for phoneme in word]) for word in phoneme_words
            ]
            return " ".join(words)
        else:
            return phoneme_words

    def transcribe_to_modern(self, text: str) -> str:
        """
        A very first attempt at transcribing from IPA to some modern orthography.
        The method is intended to provide the student with clues to the pronunciation of old orthographies.
        """
        # first transcribe letter by letter
        phoneme_words = self.transcribe(text, as_phonemes=True)
        words = [
            "".join([self.to_modern[0][phoneme.ipa] for phoneme in word])
            for word in phoneme_words
        ]
        modern_text = " ".join(words)

        # then apply phonotactic fixes
        for regexp, replacement in self.to_modern[1]:
            modern_text = re.sub(regexp, replacement, modern_text)

        return modern_text

    def voice(self, consonant: Consonant) -> Consonant:
        """
        Voices a consonant, by searching the sound inventory for a consonant having the same
        features as the argument, but +voice.
        """
        voiced_consonant = deepcopy(consonant)
        voiced_consonant[Voiced] = Voiced.pos
        return self._find_sound(voiced_consonant)

    def aspirate(self, consonant: Consonant) -> Consonant:
        """
        Aspirates a consonant, by searching the sound inventory for a consonant having the same
        features as the argument, but +aspirated.
        """
        aspirated_consonant = deepcopy(consonant)
        aspirated_consonant[Aspirated] = Aspirated.pos
        return self._find_sound(aspirated_consonant)

    def geminate(self, consonant: Consonant) -> Consonant:
        """

        :param consonant:
        :return:
        """
        geminate_consonant = deepcopy(consonant)
        geminate_consonant[Geminate] = Geminate.pos
        return self._find_sound(geminate_consonant)

    @staticmethod
    def lengthen(vowel) -> Vowel:
        """
        Returns a lengthened copy of the vowel argument.
        """
        return vowel.lengthen()

    def __call__(self, text, as_phonemes=False) -> Union[str, list]:
        """
        syntactic sugar for call the transcribe method
        """
        return self.transcribe(text, as_phonemes)

    def __getitem__(self, letter):
        """
        Returns the phoneme associated with a letter, or None.
        """
        phoneme = self.alphabet.get(letter, None)
        if phoneme is not None:
            return phoneme
        else:
            raise LetterNotFound(letter)

    def __lshift__(self, rule):
        """
        Syntactic sugar for adding a rule
        """
        self.add_rule(rule)
