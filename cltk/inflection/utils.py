"""Declensions of pronouns, nouns, adjectives"""

from enum import Enum, auto

from cltk.corpus.old_norse.syllabifier import VOWELS, CONSONANTS


class Number(Enum):
    singular = auto()
    plural = auto()


class Gender(Enum):
    masculine = auto()
    feminine = auto()
    neuter = auto()


class Case(Enum):
    nominative = auto()
    accusative = auto()
    dative = auto()
    genitive = auto()


class Declinable:
    def __init__(self, name: str):
        self.declension = []
        self.name = name

    def set_declension(self, declension):
        self.declension = declension

    def get_declined(self, case: Case, number: Number, gender=None):
        if gender is not None:
            return self.declension[gender.value-1][number.value-1][case.value-1]
        else:
            return self.declension[number.value-1][case.value-1]

    def print_declension(self):
        for a_gender in Gender:
            for a_number in Number:
                for a_case in Case:
                    print(a_case.name, a_number.name, a_gender.name, ":\t",
                          self.get_declined(a_case, a_number, a_gender))
        print("\n")


class Pronoun(Declinable):
    def __init__(self, name: str):
        Declinable.__init__(self, name)


class Adjective:
    pass


class DeclinableNoGender:
    def __init__(self, name: str):
        self.declension = []
        self.name = name

    def set_declension(self, declension):
        self.declension = declension

    def get_declined(self, case: Case, number: Number):
        return self.declension[number.value-1][case.value-1]

    def print_declension(self):
        for a_number in Number:
            for a_case in Case:
                print(a_case.name, a_number.name, ":\t",
                      self.get_declined(a_case, a_number))
        print("\n")


class DeclinableOneGender:
    def __init__(self, name: str, gender: Gender):
        self.declension = []
        self.name = name
        self.gender = gender

    def set_declension(self, declension):
        self.declension = declension

    def get_declined(self, case: Case, number: Number):
        return self.declension[number.value-1][case.value-1]

    def print_declension(self):
        for a_number in Number:
            for a_case in Case:
                print(a_case.name, a_number.name, ":\t",
                      self.get_declined(a_case, a_number))
        print("\n")


class Noun(DeclinableOneGender):
    def __init__(self, name: str, gender: Gender):
        DeclinableOneGender.__init__(self, name, gender)
        self.gender = gender
        self.name = name
        self.declension = []


class DeclensionPattern(Declinable):
    def __init__(self, name: str):
        Declinable.__init__(self, name)

    def apply(self, word: str, gender: Gender, number: Number, case: Case):
        return word + self.declension[gender.value-1][number.value-1][case.value-1]


class Syllable:
    def __init__(self, text, vowels, consonants):
        self.onset = []
        self.nucleus = []
        self.coda = []
        self.text = text
        self.consonants = consonants
        self.vowels = vowels

        self._compute_syllable(text)

    def _compute_syllable(self, text):
        """
        >>> sylla = Syllable("armr", VOWELS, CONSONANTS)
        >>> sylla.onset
        []
        >>> sylla.nucleus
        ['a']
        >>> sylla.coda
        ['r', 'm', 'r']

        :param text:
        :return:
        """
        is_in_onset = True
        is_in_nucleus = False
        is_in_coda = False
        if len(text) > 0:
            for c in text:
                if is_in_onset and c in self.consonants:
                    self.onset.append(c)

                elif is_in_onset and c in self.vowels:
                    is_in_onset = False
                    is_in_nucleus = True
                    self.nucleus.append(c)

                elif is_in_nucleus and c in self.vowels:
                    self.nucleus.append(c)

                elif is_in_nucleus and c in self.consonants:
                    is_in_nucleus = False
                    is_in_coda = True
                    self.coda.append(c)

                elif is_in_coda and c in self.consonants:
                    self.coda.append(c)

                elif is_in_coda and c in self.vowels:
                    raise ValueError("This is not a correct syllable")

                else:
                    raise ValueError("{} is an unknown character".format(c))
        else:
            raise ValueError("A syllable can't be void")
