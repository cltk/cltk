"""

"""

from cltk.inflection.utils import *


__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


# Demonstrative pronouns
demonstrative_pronouns_this = [
    [["þessi", "þenna", "þessum", "þessa"], ["þessir", "þessa", "þessum", "þessa"]],
    [["þessi", "þessa", "þessi", "þessar"], ["þessar", "þessar", "þessum", "þessa"]],
    [["þetta", "þetta", "þessu", "þessa"], ["þessi", "þessi", "þessum", "þessa"]]
]

demonstrative_pronouns_that = [
    [["sá", "þann", "þeim", "þess"], ["þeir", "þá", "þeim", "þeirra"]],
    [["sú", "þá", "þeirri", "þeirrar"], ["þær", "þær", "þeim", "þeirra"]],
    [["þat", "þat", "því, þí", "þess"], ["þau", "þau", "þeim", "þeirra"]]
]

personal_pronouns_ek = [["ek", "mik", "mér", "mín"], ["vér", "oss", "oss", "vár"]]
personal_pronouns_thu = [["þú", "þik", "þér", "þín"], ["ér", "yðr", "yðr", "yðar"]]
personal_pronouns_hann_hon_that = [
    [["hann", "hann", "hánum", "hans"], ["þeir", "þá", "þeim", "þeirra"]],
    [["hon", "hana", "henni", "hennar"], ["þær", "þær", "þeim", "þeirra"]],
    [["þat", "þat", "því", "þess"], ["þau", "þau", "þeim", "þeirra"]]
]

pro_demonstrative_pronouns_this = Pronoun("demonstrative_pronouns_this")
pro_demonstrative_pronouns_this.set_declension(demonstrative_pronouns_this)

pro_demonstrative_pronouns_that = Pronoun("demonstrative_pronouns_that")
pro_demonstrative_pronouns_that.set_declension(demonstrative_pronouns_this)

pro_personal_pronouns_ek = DeclinableNoGender("personal_pronouns_ek")
pro_personal_pronouns_ek.set_declension(personal_pronouns_ek)

pro_personal_pronouns_thu = DeclinableNoGender("personal_pronouns_thu")
pro_personal_pronouns_thu.set_declension(personal_pronouns_thu)

pro_personal_pronouns_hann_hon_that = Declinable("personal_pronouns_hann_hon_that")
pro_personal_pronouns_hann_hon_that.set_declension(personal_pronouns_hann_hon_that)
