"""Declensions of pronouns, nouns, adjectives"""

from enum import Enum, auto


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
