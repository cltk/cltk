"""Declensions of pronouns, nouns, adjectives

This module seems not to be general enough.
"""

from enum import Enum, auto
from typing import Union

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


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
    def __init__(self, root: str):
        self.declension = []
        self.root = root

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
    def __init__(self, root: str):
        Declinable.__init__(self, root)


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

    def set_void_declension(self, number_type, case_type):
        """
        >>> decl = DeclinableOneGender("armr", Gender.masculine)
        >>> decl.declension
        []
        >>> decl.set_void_declension(Number, Case)
        >>> decl.declension
        [['', '', '', ''], ['', '', '', '']]

        :param number_type:
        :param case_type:
        :return:
        """
        self.declension = []
        for i, a_number in enumerate(number_type):
            self.declension.append([])
            for _ in case_type:
                self.declension[i].append("")

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
        super().__init__(name, gender)


class DeclensionPattern(Declinable):
    def __init__(self, root: str):
        super().__init__(root)

    def apply(self, root: str, gender: Union[Gender, None], number: Number, case: Case):
        """
        >>> armr = DeclensionPattern("arm")
        >>> armr.set_declension([["armr", "arm", "armi", "arms"], ["armar", "arma", "örmum", "arma"]])
        >>> armr.get_declined(Case.accusative, Number.singular, None)
        'arm'

        >>> armr.apply("hest", None, Number.singular, Case.dative)
        'hesti'

        >>> armr.apply("hest", None, Number.plural, Case.dative)
        'hestum'

        >>> armr.apply("hest", None, Number.singular, Case.genitive)
        'hests'

        :param root: root of the word to decline
        :param gender: instance of Gender of the word to decline (nouns have only one gender so the gender is not mentioned
        in the declension: the value of gender must be None)
        :param number: instance of Number
        :param case: instance of Case
        :return: word declined the same way as the the attribute root of the DeclensionPattern instance.
        """
        if gender is None:
            return root + self.declension[number.value - 1][case.value - 1][len(self.root):]
        else:
            return root + self.declension[gender.value - 1][number.value - 1][case.value - 1][len(self.root):]
