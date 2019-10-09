"""Test for inflections: declension, conjugation, etc"""

import unittest
import cltk.inflection.utils as decl_utils
from cltk.inflection.old_norse import nouns
from cltk.inflection.old_norse import pronouns


__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


class TestInflection(unittest.TestCase):
    """Class for unittest"""

    def test_declinable(self):
        saa = decl_utils.Declinable("sá")
        saa.set_declension(pronouns.demonstrative_pronouns_that)
        self.assertEqual(saa.get_declined(decl_utils.Case.dative, decl_utils.Number.plural, decl_utils.Gender.neuter),
                         "þeim")

    def test_declinable_no_gender(self):
        ek = decl_utils.DeclinableNoGender("ek")
        ek.set_declension(pronouns.personal_pronouns_ek)
        self.assertEqual(ek.get_declined(decl_utils.Case.dative, decl_utils.Number.singular), "mér")

    def test_declinable_one_gender(self):
        noun_sumar = decl_utils.DeclinableOneGender("sumar", decl_utils.Gender.neuter)
        noun_sumar.set_declension(nouns.sumar)
        self.assertEqual(noun_sumar.get_declined(decl_utils.Case.nominative, decl_utils.Number.plural), "sumur")

    def test_declensions(self):
        thessi_declension = [
            [["þessi", "þenna", "þessum", "þessa"], ["þessir", "þessa", "þessum", "þessa"]],
            [["þessi", "þessa", "þessi", "þessar"], ["þessar", "þessar", "þessum", "þessa"]],
            [["þetta", "þetta", "þessu", "þessa"], ["þessi", "þessi", "þessum", "þessa"]]
        ]
        self.assertListEqual(pronouns.pro_demonstrative_pronouns_this.declension, thessi_declension)


if __name__ == '__main__':
    unittest.main()
