"""

"""

from enum import Enum, auto


# class AutoName(Enum):
#     def _generate_next_value_(name, a, b, d):
#         return name


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


class Noun(Declinable):
    def __init__(self, name: str, gender: Gender):
        Declinable.__init__(self, name)
        self.gender = gender

    def get_declined(self, case: Case, number: Number, gender=None):
        return self.declension[self.gender.value-1][number.value-1][case.value-1]


class Pronoun(Declinable):
    def __init__(self, name: str):
        Declinable.__init__(self, name)


class Adjective:
    pass


class DeclensionPattern(Declinable):
    def __init__(self, name: str):
        Declinable.__init__(self, name)

    def apply(self, word: str, gender: Gender, number: Number, case: Case):
        return word + self.declension[gender.value-1][number.value-1][case.value-1]


# Demonstrative pronouns
demonstrative_pronouns_this = [
    [["þessi", "þenna", "þessum", "þessa"], ["þessir", "þessa", "þessum", "þessa"]],
    [["þessi", "þessa", "þessi", "þessar"], ["þessar", "þessar", "þessum", "þessa"]],
    [["þetta", "þetta", "þessu", "þessa"], ["þessi", "þessi", "þessum", "þessa"]]
]

if __name__ == "__main__":
    pronouns = Pronoun("demonstrative_pronouns_this")
    pronouns.set_declension(demonstrative_pronouns_this)
    print(pronouns.get_declined(Case.dative, Number.singular, Gender.neuter))
    for gender in Gender:
        for number in Number:
            for case in Case:
                print(pronouns.get_declined(case, number, gender))