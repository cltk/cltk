"""Verb inflection"""

from cltk.phonology.syllabify import Syllabifier, Syllable
from cltk.corpus.old_norse.syllabifier import invalid_onsets, VOWELS, CONSONANTS, LONG_VOWELS
from cltk.inflection.utils import Number
from enum import Enum, auto

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

s = Syllabifier(language="old_norse", break_geminants=True)
s.set_invalid_onsets(invalid_onsets)


class Person(Enum):
    first = auto()
    second = auto()
    third = auto()


class Mood(Enum):
    infinitive = auto()
    imperative = auto()
    indicative = auto()
    subjunctive = auto()
    supine = auto()
    present_participle = auto()
    past_participle = auto()


class Voice(Enum):
    active = auto()
    middle = auto()


class Tense(Enum):
    present = auto()
    past = auto()


class VerbCategory(Enum):
    strong = auto()
    weak = auto()
    preteritopresent = auto()


class OldNorseVerb:

    def __init__(self):
        self.name = ""
        self.category = None
        self.forms = {}

    def set_canonic_forms(self, canonic_forms):
        """
        >>> verb = OldNorseVerb()

        Weak verbs
        I
        >>> verb.set_canonic_forms()

        II
        >>> verb.set_canonic_forms()

        III
        >>> verb.set_canonic_forms()

        IV
        >>> verb.set_canonic_forms()

        Strong verbs
        I
        >>> verb.set_canonic_forms()

        II
        >>> verb.set_canonic_forms()

        III
        >>> verb.set_canonic_forms()

        IV
        >>> verb.set_canonic_forms()

        V
        >>> verb.set_canonic_forms()

        VI
        >>> verb.set_canonic_forms()

        VII
        >>> verb.set_canonic_forms()


        :param canonic_forms: 3-tuple or 5-tuple
        :return:
        """
        if len(canonic_forms) == 3:
            sng, sfg3et, stgken = canonic_forms
            self.category = VerbCategory.weak
            self.name = sng
        elif len(canonic_forms) == 5:
            sng, sfg3en, sfg3et, sfg3ft, stgken = canonic_forms
            self.category = VerbCategory.strong
            self.name = sng
        else:
            raise ValueError("Not a correct argument")

    def get_form(self, *args):
        """

        :param args:
        :return:
        """
        for i in args:
            if isinstance(i, Person):
                pass
            elif isinstance(i, Tense):
                pass

            elif isinstance(i, Number):
                pass

            elif isinstance(i, Mood):
                pass

            elif isinstance(i, Voice):
                pass

        return self.forms

    def _present__active_weak(self):
        pass

    def _past_active_weak(self):
        pass

    def _present_active_strong(self):
        pass

    def _past_active_strong(self):
        pass

    def _present_mediopassive_weak(self):
        pass

    def _past_mediopassive_weak(self):
        pass

    def _present_mediopassive_strong(self):
        pass

    def _past_mediopassive_strong(self):
        pass


def add_t_ending_to_syllable(last_syllable):
    """

    >>> add_t_ending_to_syllable("batt")
    'bazt'
    >>> add_t_ending_to_syllable("gat")
    'gazt'
    >>> add_t_ending_to_syllable("varð")
    'vart'
    >>> add_t_ending_to_syllable("hélt")
    'hélt'
    >>> add_t_ending_to_syllable("réð")
    'rétt'
    >>> add_t_ending_to_syllable("laust")
    'laust'
    >>> add_t_ending_to_syllable("sá")
    'sátt'

    :param last_syllable:
    :return:
    """
    if len(last_syllable) >= 2:
        if last_syllable[-1] == 't':
            if last_syllable[-2] in VOWELS:
                # Apocope of r
                return last_syllable[:-1]+"zt"
            elif last_syllable[-2] == 't':
                return last_syllable[:-2]+"zt"
            elif last_syllable[-2] in ['r', 'l', 's']:
                return last_syllable
            else:
                return last_syllable + "t"
        elif last_syllable[-1] == 'ð':
            if last_syllable[-2] in ['r', 'l', 's']:
                return last_syllable[:-1] + "t"
            else:
                return last_syllable[:-1]+"tt"

        elif last_syllable[-1] == 'd':
            return last_syllable[:-1]+"t"
        elif last_syllable[-1] in LONG_VOWELS:
            return last_syllable + "tt"
        else:
            return last_syllable + "t"
    else:
        return last_syllable + "t"


def add_t_ending(stem: str) -> str:
    """

    >>> add_t_ending("batt")
    'bazt'
    >>> add_t_ending("gat")
    'gazt'
    >>> add_t_ending("varð")
    'vart'
    >>> add_t_ending("hélt")
    'hélt'
    >>> add_t_ending("réð")
    'rétt'
    >>> add_t_ending("laust")
    'laust'
    >>> add_t_ending("sá")
    'sátt'

    :param stem:
    :return:
    """
    s_stem = s.syllabify_ssp(stem.lower())
    last_syllable = Syllable(s_stem[-1], VOWELS, CONSONANTS)
    return "".join(s_stem[:-1]) + add_t_ending_to_syllable(last_syllable.text)
