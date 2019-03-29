"""Verb inflection"""

from enum import Enum, auto
from typing import List

from cltk.phonology.old_norse.transcription import measure_old_norse_syllable, DIPHTHONGS_IPA, DIPHTHONGS_IPA_class, \
    IPA_class, old_norse_rules

from cltk.phonology.syllabify import Syllabifier, Syllable
from cltk.corpus.old_norse.syllabifier import invalid_onsets, VOWELS, CONSONANTS, LONG_VOWELS, BACK_TO_FRONT_VOWELS
from cltk.inflection.utils import Number
from cltk.phonology.utils import Length, Transcriber
from cltk.inflection.old_norse.phonemic_rules import apply_i_umlaut, apply_u_umlaut, add_r_ending

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

s = Syllabifier(language="old_norse", break_geminants=True)
s.set_invalid_onsets(invalid_onsets)

s_ipa = Syllabifier(language="old_norse_ipa", break_geminants=True)
s_ipa.set_invalid_onsets(invalid_onsets)

transcriber = Transcriber(DIPHTHONGS_IPA, DIPHTHONGS_IPA_class, IPA_class, old_norse_rules)


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

    def set_canonic_forms(self, canonic_forms: List[str]):
        """

        :param canonic_forms: 3-tuple or 5-tuple
        :return:
        """
        pass

    def get_form(self, *args: List[str]):
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

    def present_active(self):
        pass

    def past_active(self):
        pass

    # def present_mediopassive(self):
    #     pass
    #
    # def past_mediopassive(self):
    #     pass

    def present_active_subjunctive(self):
        pass

    def past_active_subjunctive(self):
        pass

    # def present_mediopassive_subjunctive(self):
    #     pass
    #
    # def past_mediopassive_subjunctive(self):
    #     pass

    def past_participle(self):
        pass


class StrongOldNorseVerb(OldNorseVerb):
    def __init__(self):
        super().__init__()

        self.sng = ""
        self.s_sng = None
        self.sp_sng = None

        self.sfg3en = ""
        self.s_sfg3en = None
        self.sp_sfg3en = None

        self.sfg3et = ""
        self.s_sfg3et = None
        self.sp_sfg3et = None

        self.sfg3ft = ""
        self.s_sfg3ft = None
        self.sp_sfg3ft = None

        self.stgken = ""
        self.s_stgken = None
        self.sp_stgken = None

        self.subclass = 0
        self.syllabified = []

    def set_canonic_forms(self, canonic_forms: List[str]):
        """

        Strong verbs

        I
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["líta", "lítr", "leit", "litu", "litinn"])
        >>> verb.subclass
        1

        II
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bjóða", "býðr", "bauð", "buðu", "boðinn"])
        >>> verb.subclass
        2

        III
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["verða", "verðr", "varð", "urðu", "orðinn"])
        >>> verb.subclass
        3

        IV
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bera", "berr", "bar", "báru", "borinn"])
        >>> verb.subclass
        4

        V
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["gefa", "gefr", "gaf", "gáfu", "gefinn"])
        >>> verb.subclass
        5

        VI
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["fara", "ferr", "fór", "fóru", "farinn"])
        >>> verb.subclass
        6


        VII
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["ráða", "ræðr", "réð", "réðu", "ráðinn"])
        >>> verb.subclass
        7

        :param canonic_forms:
        :return:
        """
        if len(canonic_forms) == 5:
            sng, sfg3en, sfg3et, sfg3ft, stgken = canonic_forms
            self.category = VerbCategory.strong
            self.name = sng

            self.sng = sng
            self.s_sng = s.syllabify_ssp(self.sng)
            self.sp_sng = s_ipa.syllabify_phonemes(transcriber.text_to_phonemes(self.sng))

            self.sfg3en = sfg3en
            self.s_sfg3en = s.syllabify_ssp(self.sfg3en)
            self.sp_sfg3en = s_ipa.syllabify_phonemes(transcriber.text_to_phonemes(self.sfg3en))

            self.sfg3et = sfg3et
            self.s_sfg3et = s.syllabify_ssp(self.sfg3et)
            self.sp_sfg3et = s_ipa.syllabify_phonemes(transcriber.text_to_phonemes(self.sfg3et))

            self.sfg3ft = sfg3ft
            self.s_sfg3ft = s.syllabify_ssp(self.sfg3ft)
            self.sp_sfg3ft = s_ipa.syllabify_phonemes(transcriber.text_to_phonemes(self.sfg3ft))

            self.stgken = stgken
            self.s_stgken = s.syllabify_ssp(self.stgken)
            self.sp_stgken = s_ipa.syllabify_phonemes(transcriber.text_to_phonemes(self.stgken))

            self.classify()
        else:
            raise ValueError("Not a correct argument")

    def classify(self):

        signature = ["".join(Syllable(self.s_sng[0], VOWELS, CONSONANTS).nucleus),
                     "".join(Syllable(self.s_sfg3en[0], VOWELS, CONSONANTS).nucleus),
                     "".join(Syllable(self.s_sfg3et[0], VOWELS, CONSONANTS).nucleus),
                     "".join(Syllable(self.s_sfg3ft[0], VOWELS, CONSONANTS).nucleus),
                     "".join(Syllable(self.s_stgken[0], VOWELS, CONSONANTS).nucleus)
                     ]
        if signature == ['í', 'í', 'ei', 'i', 'i']:
            self.subclass = 1
        elif signature == ['ó', 'ý', 'au', 'u', 'o']:
            self.subclass = 2
        elif signature == ['e', 'e', 'a', 'u', 'o']:
            self.subclass = 3
        elif signature == ['e', 'e', 'a', 'á', 'o']:
            self.subclass = 4
        elif signature == ['e', 'e', 'a', 'á', 'e']:
            self.subclass = 5
        elif signature == ['a', 'e', 'ó', 'ó', 'a']:
            self.subclass = 6
        elif signature == ['á', 'æ', 'é', 'é', 'á']:
            self.subclass = 7

    def present_active(self):
        """
        Strong verbs

        I
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["líta", "lítr", "leit", "litu", "litinn"])
        >>> verb.present_active()
        ['lít', 'lítr', 'lítr', 'lítum', 'lítið', 'líta']

        II
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bjóða", "býðr", "bauð", "buðu", "boðinn"])
        >>> verb.present_active()
        ['býð', 'býðr', 'býðr', 'bjóðum', 'bjóðið', 'bjóða']

        III
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["verða", "verðr", "varð", "urðu", "orðinn"])
        >>> verb.present_active()
        ['verð', 'verðr', 'verðr', 'verðum', 'verðið', 'verða']

        IV
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bera", "berr", "bar", "báru", "borinn"])
        >>> verb.present_active()
        ['ber', 'berr', 'berr', 'berum', 'berið', 'bera']

        V
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["gefa", "gefr", "gaf", "gáfu", "gefinn"])
        >>> verb.present_active()
        ['gef', 'gefr', 'gefr', 'gefum', 'gefið', 'gefa']

        VI
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["fara", "ferr", "fór", "fóru", "farinn"])
        >>> verb.present_active()
        ['fer', 'ferr', 'ferr', 'förum', 'farið', 'fara']

        VII
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["ráða", "ræðr", "réð", "réðu", "ráðinn"])
        >>> verb.present_active()
        ['ræð', 'ræðr', 'ræðr', 'ráðum', 'ráðið', 'ráða']

        :return:
        """
        forms = []
        singular_stem = self.sfg3en[:-1]
        forms.append(singular_stem)
        forms.append(self.sfg3en)
        forms.append(self.sfg3en)
        plural_stem = self.sng[:-1] if self.sng[-1] == "a" else self.sng
        forms.append(apply_u_umlaut(plural_stem)+"um")
        forms.append(plural_stem+"ið")
        forms.append(self.sng)
        return forms

    def past_active(self):
        """
        Strong verbs

        I
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["líta", "lítr", "leit", "litu", "litinn"])
        >>> verb.past_active()
        ['leit', 'leizt', 'leit', 'litum', 'lituð', 'litu']

        II
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bjóða", "býðr", "bauð", "buðu", "boðinn"])
        >>> verb.past_active()
        ['bauð', 'bautt', 'bauð', 'buðum', 'buðuð', 'buðu']

        III
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["verða", "verðr", "varð", "urðu", "orðinn"])
        >>> verb.past_active()
        ['varð', 'vart', 'varð', 'urðum', 'urðuð', 'urðu']

        IV
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bera", "berr", "bar", "báru", "borinn"])
        >>> verb.past_active()
        ['bar', 'bart', 'bar', 'bárum', 'báruð', 'báru']

        V
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["gefa", "gefr", "gaf", "gáfu", "gefinn"])
        >>> verb.past_active()
        ['gaf', 'gaft', 'gaf', 'gáfum', 'gáfuð', 'gáfu']

        VI
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["fara", "ferr", "fór", "fóru", "farinn"])
        >>> verb.past_active()
        ['fór', 'fórt', 'fór', 'fórum', 'fóruð', 'fóru']

        VII
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["ráða", "ræðr", "réð", "réðu", "ráðinn"])
        >>> verb.past_active()
        ['réð', 'rétt', 'réð', 'réðum', 'réðuð', 'réðu']

        :return:
        """

        forms = [self.sfg3et,
                 add_t_ending(self.sfg3et),
                 self.sfg3et,
                 apply_u_umlaut(self.sfg3ft) + "m",
                 apply_u_umlaut(self.sfg3ft) + "ð",
                 self.sfg3ft]
        return forms

    # def present_mediopassive(self):
    #     pass
    #
    # def past_mediopassive(self):
    #     pass

    def present_active_subjunctive(self):
        """
        Strong verbs

        I
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["líta", "lítr", "leit", "litu", "litinn"])
        >>> verb.present_active_subjunctive()
        ['líta', 'lítir', 'líti', 'lítim', 'lítið', 'líti']

        II
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bjóða", "býðr", "bauð", "buðu", "boðinn"])
        >>> verb.present_active_subjunctive()
        ['bjóða', 'bjóðir', 'bjóði', 'bjóðim', 'bjóðið', 'bjóði']

        III
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["verða", "verðr", "varð", "urðu", "orðinn"])
        >>> verb.present_active_subjunctive()
        ['verða', 'verðir', 'verði', 'verðim', 'verðið', 'verði']

        IV
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bera", "berr", "bar", "báru", "borinn"])
        >>> verb.present_active_subjunctive()
        ['bera', 'berir', 'beri', 'berim', 'berið', 'beri']

        V
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["gefa", "gefr", "gaf", "gáfu", "gefinn"])
        >>> verb.present_active_subjunctive()
        ['gefa', 'gefir', 'gefi', 'gefim', 'gefið', 'gefi']

        VI
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["fara", "ferr", "fór", "fóru", "farinn"])
        >>> verb.present_active_subjunctive()
        ['fara', 'farir', 'fari', 'farim', 'farið', 'fari']

        VII
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["ráða", "ræðr", "réð", "réðu", "ráðinn"])
        >>> verb.present_active_subjunctive()
        ['ráða', 'ráðir', 'ráði', 'ráðim', 'ráðið', 'ráði']

        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["vera", "a", "a", "a", "a"])
        >>> verb.present_active_subjunctive()
        ['sé', 'sér', 'sé', 'sém', 'séð', 'sé']

        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["sjá", "a", "a", "a", "a"])
        >>> verb.present_active_subjunctive()
        ['sjá', 'sér', 'sé', 'sém', 'séð', 'sé']

        :return:
        """

        if self.sng == "vera":
            forms = ["sé", "sér", "sé", "sém", "séð", "sé"]
            return forms
        elif self.sng == "sjá":
            forms = ["sjá", "sér", "sé", "sém", "séð", "sé"]
            return forms
        else:
            subjunctive_root = self.sng[:-1] if self.sng[-1] == "a" else self.sng

            forms = [subjunctive_root + "a"]
            subjunctive_root = subjunctive_root[:-1] if subjunctive_root[-1] == "j" else subjunctive_root
            forms.append(subjunctive_root + "ir")
            forms.append(subjunctive_root + "i")
            forms.append(subjunctive_root + "im")
            forms.append(subjunctive_root + "ið")
            forms.append(subjunctive_root + "i")
            return forms

    def past_active_subjunctive(self):
        """
        Strong verbs

        I
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["líta", "lítr", "leit", "litu", "litinn"])
        >>> verb.past_active_subjunctive()
        ['lita', 'litir', 'liti', 'litim', 'litið', 'liti']

        II
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bjóða", "býðr", "bauð", "buðu", "boðinn"])
        >>> verb.past_active_subjunctive()
        ['byða', 'byðir', 'byði', 'byðim', 'byðið', 'byði']

        III
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["verða", "verðr", "varð", "urðu", "orðinn"])
        >>> verb.past_active_subjunctive()
        ['yrða', 'yrðir', 'yrði', 'yrðim', 'yrðið', 'yrði']

        IV
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bera", "berr", "bar", "báru", "borinn"])
        >>> verb.past_active_subjunctive()
        ['bæra', 'bærir', 'bæri', 'bærim', 'bærið', 'bæri']

        V
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["gefa", "gefr", "gaf", "gáfu", "gefinn"])
        >>> verb.past_active_subjunctive()
        ['gæfa', 'gæfir', 'gæfi', 'gæfim', 'gæfið', 'gæfi']

        VI
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["fara", "ferr", "fór", "fóru", "farinn"])
        >>> verb.past_active_subjunctive()
        ['fœra', 'fœrir', 'fœri', 'fœrim', 'fœrið', 'fœri']

        VII
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["ráða", "ræðr", "réð", "réðu", "ráðinn"])
        >>> verb.past_active_subjunctive()
        ['réða', 'réðir', 'réði', 'réðim', 'réðið', 'réði']

        :return:
        """

        forms = []
        subjunctive_root = apply_i_umlaut(self.sfg3ft[:-1])
        if subjunctive_root[-1] in ['g', 'k']:
            forms.append(subjunctive_root + "ja")
        else:
            forms.append(subjunctive_root + "a")
        subjunctive_root = subjunctive_root[:-1] if subjunctive_root[-1] == "j" else subjunctive_root
        forms.append(subjunctive_root + "ir")
        forms.append(subjunctive_root + "i")
        forms.append(subjunctive_root + "im")
        forms.append(subjunctive_root + "ið")
        forms.append(subjunctive_root + "i")

        return forms

    # def present_mediopassive_subjunctive(self):
    #     pass
    #
    # def past_mediopassive_subjunctive(self):
    #     pass

    def past_participle(self):
        """
        Strong verbs

        I
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["líta", "lítr", "leit", "litu", "litinn"])
        >>> verb.past_participle()
        [['litinn', 'litinn', 'litnum', 'litins', 'litnir', 'litna', 'litnum', 'litinna'], ['litin', 'litna', 'litinni', 'litinnar', 'litnar', 'litnar', 'litnum', 'litinna'], ['litit', 'litit', 'litnu', 'litins', 'litit', 'litit', 'litnum', 'litinna']]

        II
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bjóða", "býðr", "bauð", "buðu", "boðinn"])
        >>> verb.past_participle()
        [['boðinn', 'boðinn', 'boðnum', 'boðins', 'boðnir', 'boðna', 'boðnum', 'boðinna'], ['boðin', 'boðna', 'boðinni', 'boðinnar', 'boðnar', 'boðnar', 'boðnum', 'boðinna'], ['boðit', 'boðit', 'boðnu', 'boðins', 'boðit', 'boðit', 'boðnum', 'boðinna']]

        III
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["verða", "verðr", "varð", "urðu", "orðinn"])
        >>> verb.past_participle()
        [['orðinn', 'orðinn', 'orðnum', 'orðins', 'orðnir', 'orðna', 'orðnum', 'orðinna'], ['orðin', 'orðna', 'orðinni', 'orðinnar', 'orðnar', 'orðnar', 'orðnum', 'orðinna'], ['orðit', 'orðit', 'orðnu', 'orðins', 'orðit', 'orðit', 'orðnum', 'orðinna']]

        IV
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["bera", "berr", "bar", "báru", "borinn"])
        >>> verb.past_participle()
        [['borinn', 'borinn', 'bornum', 'borins', 'bornir', 'borna', 'bornum', 'borinna'], ['borin', 'borna', 'borinni', 'borinnar', 'bornar', 'bornar', 'bornum', 'borinna'], ['borit', 'borit', 'bornu', 'borins', 'borit', 'borit', 'bornum', 'borinna']]

        V
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["gefa", "gefr", "gaf", "gáfu", "gefinn"])
        >>> verb.past_participle()
        [['gefinn', 'gefinn', 'gefnum', 'gefins', 'gefnir', 'gefna', 'gefnum', 'gefinna'], ['gefin', 'gefna', 'gefinni', 'gefinnar', 'gefnar', 'gefnar', 'gefnum', 'gefinna'], ['gefit', 'gefit', 'gefnu', 'gefins', 'gefit', 'gefit', 'gefnum', 'gefinna']]

        VI
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["fara", "ferr", "fór", "fóru", "farinn"])
        >>> verb.past_participle()
        [['farinn', 'farinn', 'förnum', 'farins', 'farnir', 'farna', 'förnum', 'farinna'], ['farin', 'farna', 'farinni', 'farinnar', 'farnar', 'farnar', 'förnum', 'farinna'], ['farit', 'farit', 'förnu', 'farins', 'farit', 'farit', 'förnum', 'farinna']]

        VII
        >>> verb = StrongOldNorseVerb()
        >>> verb.set_canonic_forms(["ráða", "ræðr", "réð", "réðu", "ráðinn"])
        >>> verb.past_participle()
        [['ráðinn', 'ráðinn', 'ráðnum', 'ráðins', 'ráðnir', 'ráðna', 'ráðnum', 'ráðinna'], ['ráðin', 'ráðna', 'ráðinni', 'ráðinnar', 'ráðnar', 'ráðnar', 'ráðnum', 'ráðinna'], ['ráðit', 'ráðit', 'ráðnu', 'ráðins', 'ráðit', 'ráðit', 'ráðnum', 'ráðinna']]

        :return:
        """
        forms = []
        pp_stem = self.stgken[:-3]  # past participle stem
        pp_shortened_stem = self.stgken[:-1]  # past participle stem

        forms.append([])
        # masculine
        forms[0].append(pp_stem+"inn")
        forms[0].append(pp_stem+"inn")
        forms[0].append(apply_u_umlaut(pp_stem) + "num")
        forms[0].append(pp_stem + "ins")

        forms[0].append(pp_stem + "nir")
        forms[0].append(pp_stem + "na")
        forms[0].append(apply_u_umlaut(pp_stem) + "num")
        forms[0].append(pp_stem + "inna")

        # feminine
        forms.append([])
        forms[1].append(pp_stem+"in")
        forms[1].append(pp_stem + "na")
        forms[1].append(pp_stem + "inni")
        forms[1].append(pp_stem + "innar")

        forms[1].append(pp_stem + "nar")
        forms[1].append(pp_stem + "nar")
        forms[1].append(apply_u_umlaut(pp_stem) + "num")
        forms[1].append(pp_stem + "inna")

        # neuter
        forms.append([])
        forms[2].append(pp_stem+"it")
        forms[2].append(pp_stem+"it")
        forms[2].append(apply_u_umlaut(pp_stem) + "nu")
        forms[2].append(pp_stem + "ins")

        forms[2].append(pp_stem+"it")
        forms[2].append(pp_stem+"it")
        forms[2].append(apply_u_umlaut(pp_stem) + "num")
        forms[2].append(pp_stem + "inna")
        # pp_stem = self.stgken[:-1]  # past participle steù
        # pp_shortened_stem = self.stgken[:-1]  # past participle steù
        # # masculine
        # print(add_r_ending(pp_stem))
        # print(add_r_ending(pp_stem))
        # print(pp_stem + "an")
        # print(apply_u_umlaut(pp_stem) + "um")
        # print(pp_stem + "s")
        #
        # print(pp_stem + "ir")
        # print(pp_stem + "a")
        # print(apply_u_umlaut(pp_stem) + "um")
        # print(pp_stem + "ra")
        #
        # # feminine
        # print(apply_u_umlaut(pp_stem))
        # print(pp_stem + "a")
        # print(pp_stem + "ri")
        # print(pp_stem + "rar")
        #
        # print(pp_stem + "ar")
        # print(pp_stem + "ar")
        # print(apply_u_umlaut(pp_stem) + "um")
        # print(pp_stem + "ra")
        #
        # # neuter
        # print(add_t_ending(pp_stem))
        # print(add_t_ending(pp_stem))
        # print(apply_u_umlaut(pp_stem) + "u")
        # print(pp_stem + "s")
        #
        # print(apply_u_umlaut(pp_stem))
        # print(apply_u_umlaut(pp_stem))
        # print(apply_u_umlaut(pp_stem) + "um")
        # print(pp_stem + "ra")

        return forms


class WeakOldNorseVerb(OldNorseVerb):

    def __init__(self):
        super().__init__()

        self.sng = ""
        self.s_sng = None
        self.sp_sng = None

        self.sfg3et = ""
        self.s_sfg3et = None
        self.sp_sfg3et = None

        self.stgken = ""
        self.s_stgken = None
        self.sp_stgken = None

        self.subclass = 0
        self.syllabified = []

    def set_canonic_forms(self, canonic_forms: List[str]):
        """


        Weak verbs
        I
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["kalla", "kallaði", "kallaðinn"])
        >>> verb.subclass
        1

        II
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["mæla", "mælti", "mæltr"])
        >>> verb.subclass
        2

        III
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["telja", "taldi", "talinn"])
        >>> verb.subclass
        3

        IV
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["vaka", "vakta", "vakat"])
        >>> verb.subclass
        4

        :param canonic_forms: (infinitive, third person singular past indicative,
        past participle masculine singular nominative)
        :return:
        """
        if len(canonic_forms) == 3:
            self.sng, self.sfg3et, self.stgken = canonic_forms
            self.category = VerbCategory.weak
            self.name = self.sng

            self.s_sng = s.syllabify_ssp(self.sng)
            self.sp_sng = s_ipa.syllabify_phonemes(transcriber.text_to_phonemes(self.sng))

            self.s_sfg3et = s.syllabify_ssp(self.sfg3et)
            self.sp_sfg3et = s_ipa.syllabify_phonemes(transcriber.text_to_phonemes(self.sfg3et))

            self.s_stgken = s.syllabify_ssp(self.stgken)
            self.sp_stgken = s_ipa.syllabify_phonemes(transcriber.text_to_phonemes(self.stgken))
            self.classify()
        else:
            raise ValueError("Not a correct argument")

    def present_active(self):
        """
        Weak verbs
        I
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["kalla", "kallaði", "kallaðinn"])
        >>> verb.present_active()
        ['kalla', 'kallar', 'kallar', 'köllum', 'kallið', 'kalla']

        II
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["mæla", "mælti", "mæltr"])
        >>> verb.present_active()
        ['mæli', 'mælir', 'mælir', 'mælum', 'mælið', 'mæla']

        III
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["telja", "taldi", "talinn"])
        >>> verb.present_active()
        ['tel', 'telr', 'telr', 'teljum', 'telið', 'telja']

        IV
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["vaka", "vakti", "vakat"])
        >>> verb.present_active()
        ['vaki', 'vakir', 'vakir', 'vökum', 'vakið', 'vaka']

        :return:
        """
        forms = []
        stem_ending_by_j = self.sng[-1] == "a" and self.sng[-2] == "j"
        stem_ending_by_v = self.sng[-1] == "a" and self.sng[-2] == "v"
        stem = self.sng[:-1] if self.sng[-1] == "a" else self.sng
        if stem_ending_by_j or stem_ending_by_v:
            stem = stem[:-1]

        if self.subclass == 1:
            if stem_ending_by_v:
                forms.append(stem+"va")
                forms.append(stem + "r")
                forms.append(stem + "r")
                forms.append(apply_u_umlaut(stem) + "um")  # apply u umlaut
                forms.append(stem + "við")
                forms.append(stem+"va")
            elif stem_ending_by_j:
                forms.append(stem+"ja")
                forms.append(stem + "r")
                forms.append(stem + "r")
                forms.append(apply_u_umlaut(stem) + "jum")  # apply u umlaut
                forms.append(stem + "ið")
                forms.append(stem+"ja")
            else:
                forms.append(stem+"a")
                forms.append(stem + "ar")
                forms.append(stem + "ar")
                forms.append(apply_u_umlaut(stem) + "um")  # apply u umlaut
                forms.append(stem + "ið")
                forms.append(self.sng)

        elif self.subclass == 2:
            if stem_ending_by_v:
                forms.append(stem + "vi")
                forms.append(stem + "vir")
                forms.append(stem + "vir")
                forms.append(apply_u_umlaut(stem) + "um")  # apply u umlaut
                forms.append(stem + "við")
                forms.append(self.sng)

            elif stem_ending_by_j:
                forms.append(stem + "i")
                forms.append(stem + "ir")
                forms.append(stem + "ir")
                forms.append(apply_u_umlaut(stem) + "jum")  # apply u umlaut
                forms.append(stem + "ið")
                forms.append(self.sng)

            else:
                forms.append(stem + "i")
                forms.append(stem + "ir")
                forms.append(stem + "ir")
                forms.append(apply_u_umlaut(stem) + "um")  # apply u umlaut
                forms.append(stem + "ið")
                forms.append(self.sng)

        elif self.subclass == 3:
            if stem_ending_by_v:
                forms.append(stem)
                forms.append(stem + "r")
                forms.append(stem + "r")
                forms.append(apply_u_umlaut(stem) + "um")  # apply u umlaut
                forms.append(stem + "við")
                forms.append(self.sng)

            elif stem_ending_by_j:
                forms.append(stem)
                forms.append(stem + "r")
                forms.append(stem + "r")
                forms.append(apply_u_umlaut(stem) + "jum")  # apply u umlaut
                forms.append(stem + "ið")
                forms.append(self.sng)

            else:
                forms.append(stem)
                forms.append(stem + "r")
                forms.append(stem + "r")
                forms.append(apply_u_umlaut(stem) + "um")  # apply u umlaut
                forms.append(stem + "ið")
                forms.append(self.sng)

        elif self.subclass == 4:

            if stem_ending_by_v:
                forms.append(stem + "vi")
                forms.append(stem + "vir")
                forms.append(stem + "vir")
                forms.append(apply_u_umlaut(stem) + "um")  # apply u umlaut
                forms.append(stem + "við")
                forms.append(self.sng)

            elif stem_ending_by_j:
                forms.append(stem + "i")
                forms.append(stem + "ir")
                forms.append(stem + "ir")
                forms.append(apply_u_umlaut(stem) + "jum")  # apply u umlaut
                forms.append(stem + "ið")
                forms.append(self.sng)

            else:
                forms.append(stem + "i")
                forms.append(stem + "ir")
                forms.append(stem + "ir")
                forms.append(apply_u_umlaut(stem) + "um")  # apply u umlaut
                forms.append(stem + "ið")
                forms.append(self.sng)
        return forms

    def past_active(self):
        """
        Weak verbs
        I
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["kalla", "kallaði", "kallaðinn"])
        >>> verb.past_active()
        ['kallaða', 'kallaðir', 'kallaði', 'kölluðum', 'kölluðuð', 'kölluðu']

        II
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["mæla", "mælti", "mæltr"])
        >>> verb.past_active()
        ['mælta', 'mæltir', 'mælti', 'mæltum', 'mæltuð', 'mæltu']

        III
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["telja", "taldi", "talinn"])
        >>> verb.past_active()
        ['talda', 'taldir', 'taldi', 'töldum', 'tölduð', 'töldu']

        IV
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["vaka", "vakti", "vakat"])
        >>> verb.past_active()
        ['vakta', 'vaktir', 'vakti', 'vöktum', 'vöktuð', 'vöktu']

        :return:
        """
        forms = []
        stem = self.sfg3et[:-1]
        forms.append(stem+"a")
        forms.append(self.sfg3et+"r")
        forms.append(self.sfg3et)
        forms.append(apply_u_umlaut(stem)+"um")
        forms.append(apply_u_umlaut(stem)+"uð")
        forms.append(apply_u_umlaut(stem)+"u")
        return forms

    # def present_mediopassive(self):
    #     pass
    #
    # def past_mediopassive(self):
    #     pass

    def present_active_subjunctive(self):
        """
        Weak verbs
        I
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["kalla", "kallaði", "kallaðinn"])
        >>> verb.present_active_subjunctive()
        ['kalla', 'kallir', 'kalli', 'kallim', 'kallið', 'kalli']

        II
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["mæla", "mælti", "mæltr"])
        >>> verb.present_active_subjunctive()
        ['mæla', 'mælir', 'mæli', 'mælim', 'mælið', 'mæli']

        III
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["telja", "taldi", "talinn"])
        >>> verb.present_active_subjunctive()
        ['telja', 'telir', 'teli', 'telim', 'telið', 'teli']

        IV
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["vaka", "vakta", "vakat"])
        >>> verb.present_active_subjunctive()
        ['vaka', 'vakir', 'vaki', 'vakim', 'vakið', 'vaki']

        :return:
        """
        subjunctive_root = self.sng[:-1] if self.sng[-1] == "a" else self.sng
        forms = [subjunctive_root + "a"]

        subjunctive_root = subjunctive_root[:-1] if subjunctive_root[-1] == "j" else subjunctive_root
        forms.append(subjunctive_root+"ir")
        forms.append(subjunctive_root+"i")
        forms.append(subjunctive_root+"im")
        forms.append(subjunctive_root+"ið")
        forms.append(subjunctive_root+"i")
        return forms

    def past_active_subjunctive(self):
        """
        Weak verbs
        I
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["kalla", "kallaði", "kallaðinn"])
        >>> verb.past_active_subjunctive()
        ['kallaða', 'kallaðir', 'kallaði', 'kallaðim', 'kallaðið', 'kallaði']

        II
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["mæla", "mælti", "mæltr"])
        >>> verb.past_active_subjunctive()
        ['mælta', 'mæltir', 'mælti', 'mæltim', 'mæltið', 'mælti']

        III
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["telja", "taldi", "talinn"])
        >>> verb.past_active_subjunctive()
        ['telda', 'teldir', 'teldi', 'teldim', 'teldið', 'teldi']

        IV
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["vaka", "vakti", "vakat"])
        >>> verb.past_active_subjunctive()
        ['vekta', 'vektir', 'vekti', 'vektim', 'vektið', 'vekti']

        :return:
        """
        subjunctive_root = self.sfg3et[:-1] if self.sng[-1] == "a" else self.sfg3et
        forms = []

        if self.subclass in [1, 2]:
            forms.append(subjunctive_root + "a")
            subjunctive_root = subjunctive_root[:-1] if subjunctive_root[-1] == "j" else subjunctive_root
            forms.append(subjunctive_root + "ir")
            forms.append(subjunctive_root + "i")
            forms.append(subjunctive_root + "im")
            forms.append(subjunctive_root + "ið")
            forms.append(subjunctive_root + "i")

        elif self.subclass in [3, 4]:
            subjunctive_root = apply_i_umlaut(subjunctive_root)
            forms.append(subjunctive_root + "a")
            subjunctive_root = subjunctive_root[:-1] if subjunctive_root[-1] == "j" else subjunctive_root
            forms.append(subjunctive_root + "ir")
            forms.append(subjunctive_root + "i")
            forms.append(subjunctive_root + "im")
            forms.append(subjunctive_root + "ið")
            forms.append(subjunctive_root + "i")
        return forms

    # def present_mediopassive_subjunctive(self):
    #     pass
    #
    # def past_mediopassive_subjunctive(self):
    #     pass

    def past_participle(self):
        """

        Weak verbs
        I
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["kalla", "kallaði", "kallaðr"])
        >>> verb.past_participle()
        [['kallaðr', 'kallaðan', 'kölluðum', 'kallaðs', 'kallaðir', 'kallaða', 'kölluðum', 'kallaðra'], ['kölluð', 'kallaða', 'kallaðri', 'kallaðrar', 'kallaðar', 'kallaðar', 'kölluðum', 'kallaðra'], ['kallatt', 'kallatt', 'kölluðu', 'kallaðs', 'kölluð', 'kölluð', 'kölluðum', 'kallaðra']]

        II
        >>> verb = WeakOldNorseVerb()
        >>> verb.set_canonic_forms(["mæla", "mælti", "mæltr"])
        >>> verb.past_participle()
        [['mæltr', 'mæltan', 'mæltum', 'mælts', 'mæltir', 'mælta', 'mæltum', 'mæltra'], ['mælt', 'mælta', 'mæltri', 'mæltrar', 'mæltar', 'mæltar', 'mæltum', 'mæltra'], ['mælt', 'mælt', 'mæltu', 'mælts', 'mælt', 'mælt', 'mæltum', 'mæltra']]

        III
        # >>> verb = WeakOldNorseVerb()
        # >>> verb.set_canonic_forms(["telja", "taldi", "talinn"])
        # >>> verb.past_participle()

        IV
        # >>> verb = WeakOldNorseVerb()
        # >>> verb.set_canonic_forms(["vaka", "vakti", "vakat"])
        # >>> verb.past_participle()

        :return:
        """
        forms = []
        if self.subclass in [1, 2]:
            pp_stem = self.stgken[:-1]  # past participle stem

            # masculine
            forms.append([])

            forms[0].append(add_r_ending(pp_stem))
            forms[0].append(pp_stem+"an")
            forms[0].append(apply_u_umlaut(pp_stem)+"um")
            forms[0].append(pp_stem+"s")

            forms[0].append(pp_stem+"ir")
            forms[0].append(pp_stem+"a")
            forms[0].append(apply_u_umlaut(pp_stem)+"um")
            forms[0].append(pp_stem+"ra")

            # feminine
            forms.append([])

            forms[1].append(apply_u_umlaut(pp_stem))
            forms[1].append(pp_stem+"a")
            forms[1].append(pp_stem+"ri")
            forms[1].append(pp_stem+"rar")

            forms[1].append(pp_stem+"ar")
            forms[1].append(pp_stem+"ar")
            forms[1].append(apply_u_umlaut(pp_stem)+"um")
            forms[1].append(pp_stem+"ra")

            # neuter
            forms.append([])

            forms[2].append(add_t_ending(pp_stem))
            forms[2].append(add_t_ending(pp_stem))
            forms[2].append(apply_u_umlaut(pp_stem)+"u")
            forms[2].append(pp_stem+"s")

            forms[2].append(apply_u_umlaut(pp_stem))
            forms[2].append(apply_u_umlaut(pp_stem))
            forms[2].append(apply_u_umlaut(pp_stem)+"um")
            forms[2].append(pp_stem+"ra")
        elif self.subclass in [3, 4]:
            pp_stem = self.stgken[:-1]  # past participle stem
            # masculine
            forms[0].append(add_r_ending(pp_stem))
            forms[0].append(pp_stem + "an")
            forms[0].append(apply_u_umlaut(pp_stem) + "um")
            forms[0].append(pp_stem + "s")

            forms[0].append(pp_stem + "ir")
            forms[0].append(pp_stem + "a")
            forms[0].append(apply_u_umlaut(pp_stem) + "um")
            forms[0].append(pp_stem + "ra")

            # feminine
            forms[1].append(apply_u_umlaut(pp_stem))
            forms[1].append(pp_stem + "a")
            forms[1].append(pp_stem + "ri")
            forms[1].append(pp_stem + "rar")

            forms[1].append(pp_stem + "ar")
            forms[1].append(pp_stem + "ar")
            forms[1].append(apply_u_umlaut(pp_stem) + "um")
            forms[1].append(pp_stem + "ra")

            # neuter
            forms[2].append(add_t_ending(pp_stem))
            forms[2].append(add_t_ending(pp_stem))
            forms[2].append(apply_u_umlaut(pp_stem) + "u")
            forms[2].append(pp_stem + "s")

            forms[2].append(apply_u_umlaut(pp_stem))
            forms[2].append(apply_u_umlaut(pp_stem))
            forms[2].append(apply_u_umlaut(pp_stem) + "um")
            forms[2].append(pp_stem + "ra")

        return forms

    def classify(self):
        if self.sng in ["segja", "þegja"]:
            self.subclass = 4
        elif self.sng in ["vilja", "gera"]:
            self.subclass = 3
        elif self.sng in ["spá"]:
            self.subclass = 2
        elif self.sng and self.sfg3et and self.stgken:
            if self.sfg3et.endswith("aði"):
                self.subclass = 1

            elif not "".join(Syllable(self.s_sng[0], VOWELS, CONSONANTS).nucleus) in BACK_TO_FRONT_VOWELS.values():
                self.subclass = 4
            else:
                stem_length = measure_old_norse_syllable(self.sp_sng[0])
                if stem_length == Length.long or stem_length == Length.overlong:
                    self.subclass = 2
                elif stem_length == Length.short:
                    self.subclass = 3
                else:
                    self.subclass = 5


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
