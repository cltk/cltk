"""Test cltk.stem."""

__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.utils.importer import CorpusImporter
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.latin.stem import Stemmer
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.syllabifier import Syllabifier
from cltk.stem.latin.declension import CollatinusDecliner
from cltk.exceptions import UnknownLemma
from cltk.stem.sanskrit.indian_syllabifier import Syllabifier as IndianSyllabifier
from cltk.stem.akkadian.bound_form import BoundForm as AkkadianBoundForm
from cltk.stem.akkadian.cv_pattern import CVPattern as AkkadianCVPattern
from cltk.stem.akkadian.declension import NaiveDecliner as AkkadianNaiveDecliner
from cltk.stem.akkadian.stem import Stemmer as AkkadianStemmer
from cltk.stem.akkadian.syllabifier import Syllabifier as AkkadianSyllabifier
from cltk.stem.french.stem import stem

import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        """Import sanskrit models first, some CSV files necessary for the
        Indian lang tokenizers.
        """
        corpus_importer = CorpusImporter('sanskrit')
        corpus_importer.import_corpus('sanskrit_models_cltk')
        file_rel = os.path.join('~/cltk_data/sanskrit/model/sanskrit_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_latin_i_u_transform(self):
        """Test converting ``j`` to ``i`` and ``v`` to ``u``."""
        jv_replacer = JVReplacer()
        trans = jv_replacer.replace('vem jam VEL JAM')
        self.assertEqual(trans, 'uem iam UEL IAM')

    def test_latin_stemmer(self):
        """Test Latin stemmer."""
        sentence = 'Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum.'  # pylint: disable=line-too-long
        stemmer = Stemmer()
        stemmed_text = stemmer.stem(sentence.lower())
        target = 'est interd praestar mercatur r quaerere, nisi tam periculos sit, et it foenerari, si tam honestum. '  # pylint: disable=line-too-long
        self.assertEqual(stemmed_text, target)


    def test_lemmatizer_inlist_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=False)
        target = ['homo', 'divus', 'voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=False)
        target = ['hominum/homo', 'divomque/divus', 'voluptas/voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=True)
        target = 'homo divus voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=True)
        target = 'hominum/homo divomque/divus voluptas/voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=False)
        target = ['homo', 'divus', 'voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=False)
        target = ['hominum/homo', 'divomque/divus', 'voluptas/voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=True)
        target = 'homo divus voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=True)
        target = 'hominum/homo divomque/divus voluptas/voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=False)
        target = ['τὴν', 'διάγνωσις', 'ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=False)
        target = ['τὴν/τὴν', 'διάγνωσιν/διάγνωσις', 'ἔρχεσθαι/ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=True)
        target = 'τὴν διάγνωσις ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=True)
        target = 'τὴν/τὴν διάγνωσιν/διάγνωσις ἔρχεσθαι/ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=False)
        target = ['τὴν', 'διάγνωσις', 'ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=False)
        target = ['τὴν/τὴν', 'διάγνωσιν/διάγνωσις', 'ἔρχεσθαι/ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=False, return_string=True)
        target = 'τὴν διάγνωσις ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_raw=True, return_string=True)
        target = 'τὴν/τὴν διάγνωσιν/διάγνωσις ἔρχεσθαι/ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_latin_syllabifier(self):
        """Test Latin syllabifier."""
        word = 'sidere'
        syllabifier = Syllabifier()
        syllables = syllabifier.syllabify(word)
        target = ['si', 'de', 're']
        self.assertEqual(syllables, target)

    def test_syllabify(self):
        """Test Indic Syllabifier method"""
        correct = ['न', 'म', 'स्ते']
        syllabifier = IndianSyllabifier('hindi')
        current = syllabifier.orthographic_syllabify('नमस्ते')
        self.assertEqual(current, correct)

    def test_get_offset(self):
        """Test Indic Syllabifier get_offset method"""
        correct = 40
        syllabifier = IndianSyllabifier('hindi')
        current = syllabifier.get_offset('न', 'hi')
        self.assertEqual(current, correct)

    def test_coordinated_range(self):
        """Test Indic Syllabifier in_coordinated_range method"""
        syllabifier = IndianSyllabifier('hindi')
        current = syllabifier.get_offset('न', 'hi')
        current1 = syllabifier.in_coordinated_range_offset(current)
        self.assertTrue(current1)

    def test_akkadian_bound_form(self):
        """Test Akkadian bound form method"""
        bound_former = AkkadianBoundForm()
        word = "awīlum"
        bound_form = bound_former.get_bound_form(word, 'm')
        target = "awīl"
        self.assertEquals(bound_form, target)

    def test_akkadian_cv_pattern(self):
        """Test Akkadian CV pattern method"""
        cv_patterner = AkkadianCVPattern()
        word = "iparras"
        cv_pattern = cv_patterner.get_cv_pattern(word, pprint=True)
        target = "V₁C₁V₂C₂C₂V₂C₃"
        self.assertEquals(cv_pattern, target)

    def test_akkadian_declension(self):
        """Test Akkadian noun declension"""
        decliner = AkkadianNaiveDecliner()
        word = "iltum"
        declension = decliner.decline_noun(word, 'f')
        target = [('iltim', {'case': 'genitive', 'number': 'singular'}),
                  ('iltum', {'case': 'nominative', 'number': 'singular'}),
                  ('iltam', {'case': 'accusative', 'number': 'singular'}),
                  ('iltīn', {'case': 'oblique', 'number': 'dual'}),
                  ('iltān', {'case': 'nominative', 'number': 'dual'}),
                  ('ilātim', {'case': 'oblique', 'number': 'plural'}),
                  ('ilātum', {'case': 'nominative', 'number': 'plural'})]
        self.assertEquals(sorted(declension), sorted(target))

    def test_akkadian_stemmer(self):
        """Test Akkadian stemmer"""
        stemmer = AkkadianStemmer()
        word = "šarrū"
        stem = stemmer.get_stem(word, 'm')
        target = "šarr"
        self.assertEquals(stem, target)

    def test_akkadian_syllabifier(self):
        """Test Akkadian syllabifier"""
        syllabifier = AkkadianSyllabifier()
        word = "epištašu"
        syllables = syllabifier.syllabify(word)
        target = ['e','piš','ta','šu']
        self.assertEqual(syllables, target)

    '''
    #? Someone fix this; assertTrue() doesn't make sense here
    def test_phonetic_vector(self):
        cor = [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0]
        correct = bytearray(cor)
        syllabifier = IndianSyllabifier('hindi')
        current = syllabifier.get_phonetic_feature_vector('न', 'hi')
        # self.assertTrue(current, correct)
    '''

    def test_is_misc(self):
        """Test Indic Syllabifier is_misc method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_misc(v))

    def test_is_consonant(self):
        """Test Indic Syllabifier is_consonant method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertTrue(syllabifier.is_consonant(v))

    def test_is_vowel(self):
        """Test Indic Syllabifier is_vowel method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_vowel(v))

    def test_is_anusvaar(self):
        """Test Indic Syllabifier is_anusvaar method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_anusvaar(v))

    def test_is_plosive(self):
        """Test Indic Syllabifier is_plosive method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertTrue(syllabifier.is_plosive(v))

    def test_is_nukta(self):
        """Test Indic Syllabifier is_nukta method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_nukta(v))

    def test_is_valid(self):
        """Test Indic Syllabifier is_valid method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertTrue(syllabifier.is_valid(v))

    def test_is_dependent_vowel(self):
        """Test Indic Syllabifier is_dependent_vowel method"""
        syllabifier = IndianSyllabifier('hindi')
        v = syllabifier.get_phonetic_feature_vector('न', 'hi')
        self.assertFalse(syllabifier.is_dependent_vowel(v))

    def test_collatinus_decline(self):
        """ Ensure lemmatization works well """
        decliner = CollatinusDecliner()
        self.assertEqual(
            decliner.decline("via", collatinus_dict=True),
            {1: ['via'], 2: ['via'], 3: ['viam'], 4: ['viae'], 5: ['viae'], 6: ['via'], 7: ['viae'],
             8: ['viae'], 9: ['vias'], 10: ['viarum'], 11: ['viis'], 12: ['viis']},
            "Declination of via should be right"
        )
        self.assertEqual(
            decliner.decline("doctus", collatinus_dict=True),
            {13: ['doctus'], 14: ['docte'], 15: ['doctum'], 16: ['docti'], 17: ['docto'], 18: ['docto'],
             19: ['docti'], 20: ['docti'], 21: ['doctos'], 22: ['doctorum'], 23: ['doctis'], 24: ['doctis'],
             25: ['docta'], 26: ['docta'], 27: ['doctam'], 28: ['doctae'], 29: ['doctae'], 30: ['docta'],
             31: ['doctae'], 32: ['doctae'], 33: ['doctas'], 34: ['doctarum'], 35: ['doctis'], 36: ['doctis'],
             37: ['doctum'], 38: ['doctum'], 39: ['doctum'], 40: ['docti'], 41: ['docto'], 42: ['docto'],
             43: ['docta'], 44: ['docta'], 45: ['docta'], 46: ['doctorum'], 47: ['doctis'], 48: ['doctis'],
             49: ['doctior'], 50: ['doctior'], 51: ['doctiorem'], 52: ['doctioris'], 53: ['doctiori'],
             54: ['doctiore'], 55: ['doctiores'], 56: ['doctiores'], 57: ['doctiores'], 58: ['doctiorum'],
             59: ['doctioribus'], 60: ['doctioribus'], 61: ['doctior'], 62: ['doctior'], 63: ['doctiorem'],
             64: ['doctioris'], 65: ['doctiori'], 66: ['doctiore'], 67: ['doctiores'], 68: ['doctiores'],
             69: ['doctiores'], 70: ['doctiorum'], 71: ['doctioribus'], 72: ['doctioribus'], 73: ['doctius'],
             74: ['doctius'], 75: ['doctius'], 76: ['doctioris'], 77: ['doctiori'], 78: ['doctiore'],
             79: ['doctiora'], 80: ['doctiora'], 81: ['doctiora'], 82: ['doctiorum'], 83: ['doctioribus'],
             85: ['doctissimus'], 86: ['doctissime'], 87: ['doctissimum'], 88: ['doctissimi'], 89: ['doctissimo'],
             90: ['doctissimo'], 91: ['doctissimi'], 92: ['doctissimi'], 93: ['doctissimos'], 94: ['doctissimorum'],
             95: ['doctissimis'], 96: ['doctissimis'], 97: ['doctissima'], 98: ['doctissima'], 99: ['doctissimam'],
             100: ['doctissimae'], 101: ['doctissimae'], 102: ['doctissima'], 103: ['doctissimae'],
             104: ['doctissimae'], 105: ['doctissimas'], 106: ['doctissimarum'], 107: ['doctissimis'],
             108: ['doctissimis'], 109: ['doctissimum'], 110: ['doctissimum'], 111: ['doctissimum'],
             112: ['doctissimi'], 113: ['doctissimo'], 114: ['doctissimo'], 115: ['doctissima'],
             116: ['doctissima'], 117: ['doctissima'], 118: ['doctissimorum'], 119: ['doctissimis'],
             120: ['doctissimis']},
            "Doctus has three radicals and lots of forms"
        )
        self.assertEqual(
            decliner.decline("verbex", collatinus_dict=True),
            {1: ['verbex'], 2: ['verbex'], 3: ['verbicem'], 4: ['verbicis'], 5: ['verbici'], 6: ['verbice'],
             7: ['verbices'], 8: ['verbices'], 9: ['verbices'], 10: ['verbicum'], 11: ['verbicibus'],
             12: ['verbicibus']},
            "Verbex has two different roots : checking they are taken into account"
        )
        self.assertEqual(
            decliner.decline("vendo", collatinus_dict=True),
            {121: ['vendo'], 122: ['vendis'], 123: ['vendit'], 124: ['vendimus'], 125: ['venditis'],
             126: ['vendunt'], 127: ['vendebam'], 128: ['vendebas'], 129: ['vendebat'], 130: ['vendebamus'],
             131: ['vendebatis'], 132: ['vendebant'], 133: ['vendam'], 134: ['vendes'], 135: ['vendet'],
             136: ['vendemus'], 137: ['vendetis'], 138: ['vendent'], 139: ['vendavi'], 140: ['vendavisti'],
             141: ['vendavit'], 142: ['vendavimus'], 143: ['vendavistis'], 144: ['vendaverunt', 'vendavere'],
             145: ['vendaveram'], 146: ['vendaveras'], 147: ['vendaverat'], 148: ['vendaveramus'],
             149: ['vendaveratis'], 150: ['vendaverant'], 151: ['vendavero'], 152: ['vendaveris'],
             153: ['vendaverit'], 154: ['vendaverimus'], 155: ['vendaveritis'], 156: ['vendaverint'],
             157: ['vendam'], 158: ['vendas'], 159: ['vendat'], 160: ['vendamus'], 161: ['vendatis'],
             162: ['vendant'], 163: ['venderem'], 164: ['venderes'], 165: ['venderet'], 166: ['venderemus'],
             167: ['venderetis'], 168: ['venderent'], 169: ['vendaverim'], 170: ['vendaveris'], 171: ['vendaverit'],
             172: ['vendaverimus'], 173: ['vendaveritis'], 174: ['vendaverint'], 175: ['vendavissem'],
             176: ['vendavisses'], 177: ['vendavisset'], 178: ['vendavissemus'], 179: ['vendavissetis'],
             180: ['vendavissent'], 181: ['vende'], 182: ['vendite'], 183: ['vendito'], 184: ['vendito'],
             185: ['venditote'], 186: ['vendunto'], 187: ['vendere'], 188: ['vendasse'], 189: ['vendens'],
             190: ['vendens'], 191: ['vendentem'], 192: ['vendentis'], 193: ['vendenti'], 194: ['vendente'],
             195: ['vendentes'], 196: ['vendentes'], 197: ['vendentes'], 198: ['vendentium', 'vendentum'],
             199: ['vendentibus'], 200: ['vendentibus'], 201: ['vendens'], 202: ['vendens'], 203: ['vendentem'],
             204: ['vendentis'], 205: ['vendenti'], 206: ['vendente'], 207: ['vendentes'], 208: ['vendentes'],
             209: ['vendentes'], 210: ['vendentium', 'vendentum'], 211: ['vendentibus'], 212: ['vendentibus'],
             213: ['vendens'], 214: ['vendens'], 215: ['vendens'], 216: ['vendentis'], 217: ['vendenti'],
             218: ['vendente'], 219: ['vendentia'], 220: ['vendentia'], 221: ['vendentia'],
             222: ['vendentium', 'vendentum'], 223: ['vendentibus'], 224: ['vendentibus'], 225: ['vendaturus'],
             226: ['vendature'], 227: ['vendaturum'], 228: ['vendaturi'], 229: ['vendaturo'], 230: ['vendaturo'],
             231: ['vendaturi'], 232: ['vendaturi'], 233: ['vendaturos'], 234: ['vendaturorum'],
             235: ['vendaturis'], 236: ['vendaturis'], 237: ['vendatura'], 238: ['vendatura'], 239: ['vendaturam'],
             240: ['vendaturae'], 241: ['vendaturae'], 242: ['vendatura'], 243: ['vendaturae'], 244: ['vendaturae'],
             245: ['vendaturas'], 246: ['vendaturarum'], 247: ['vendaturis'], 248: ['vendaturis'],
             249: ['vendaturum'], 250: ['vendaturum'], 251: ['vendaturum'], 252: ['vendaturi'], 253: ['vendaturo'],
             254: ['vendaturo'], 255: ['vendatura'], 256: ['vendatura'], 257: ['vendatura'], 258: ['vendaturorum'],
             259: ['vendaturis'], 260: ['vendaturis'], 261: ['vendendum'], 262: ['vendendi'], 263: ['vendendo'],
             264: ['vendendo'], 265: ['vendatum'], 266: ['vendatu'], 267: ['vendor'], 268: ['venderis', 'vendere'],
             269: ['venditur'], 270: ['vendimur'], 271: ['vendimini'], 272: ['venduntur'], 273: ['vendebar'],
             274: ['vendebaris', 'vendebare'], 275: ['vendebatur'], 276: ['vendebamur'], 277: ['vendebamini'],
             278: ['vendebantur'], 279: ['vendar'], 280: ['venderis', 'vendere'], 281: ['vendetur'],
             282: ['vendemur'], 283: ['vendemini'], 284: ['vendentur'], 285: ['vendar'], 286: ['vendaris',
                                                                                               'vendare'],
             287: ['vendatur'], 288: ['vendamur'], 289: ['vendamini'], 290: ['vendantur'], 291: ['venderer'],
             292: ['vendereris', "venderere"], 293: ['venderetur'], 294: ['venderemur'], 295: ['venderemini'],
             296: ['venderentur'], 297: ['vendere'], 298: ['vendimini'], 299: ['venditor'], 300: ['venditor'],
             301: ['venduntor'], 302: ['vendi'], 303: ['vendatus'], 304: ['vendate'], 305: ['vendatum'],
             306: ['vendati'], 307: ['vendato'], 308: ['vendato'], 309: ['vendati'], 310: ['vendati'],
             311: ['vendatos'], 312: ['vendatorum'], 313: ['vendatis'], 314: ['vendatis'], 315: ['vendata'],
             316: ['vendata'], 317: ['vendatam'], 318: ['vendatae'], 319: ['vendatae'], 320: ['vendata'],
             321: ['vendatae'], 322: ['vendatae'], 323: ['vendatas'], 324: ['vendatarum'], 325: ['vendatis'],
             326: ['vendatis'], 327: ['vendatum'], 328: ['vendatum'], 329: ['vendatum'], 330: ['vendati'],
             331: ['vendato'], 332: ['vendato'], 333: ['vendata'], 334: ['vendata'], 335: ['vendata'],
             336: ['vendatorum'], 337: ['vendatis'], 338: ['vendatis'], 339: ['vendendus'], 340: ['vendende'],
             341: ['vendendum'], 342: ['vendendi'], 343: ['vendendo'], 344: ['vendendo'], 345: ['vendendi'],
             346: ['vendendi'], 347: ['vendendos'], 348: ['vendendorum'], 349: ['vendendis'], 350: ['vendendis'],
             351: ['vendenda'], 352: ['vendenda'], 353: ['vendendam'], 354: ['vendendae'], 355: ['vendendae'],
             356: ['vendenda'], 357: ['vendendae'], 358: ['vendendae'], 359: ['vendendas'], 360: ['vendendarum'],
             361: ['vendendis'], 362: ['vendendis'], 363: ['vendendum'], 364: ['vendendum'], 365: ['vendendum'],
             366: ['vendendi'], 367: ['vendendo'], 368: ['vendendo'], 369: ['vendenda'], 370: ['vendenda'],
             371: ['vendenda'], 372: ['vendendorum'], 373: ['vendendis'], 374: ['vendendis']},
            "Check verb vendo declines well"
        )
        self.assertEqual(
            decliner.decline("poesis", collatinus_dict=True),
            {1: ['poesis'], 2: ['poesis'], 3: ["poesem", 'poesin', "poesim"], 4: ["poesis", 'poeseos'], 5: ['poesi'],
             6: ['poese'], 7: ['poeses'],
             8: ['poeses'], 9: ["poeses", 'poesis'], 10: ['poesium'], 11: ['poesibus'], 12: ['poesibus']},
            "Duplicity of forms should be accepted"
        )

        self.assertEqual(
            decliner.decline("hic", collatinus_dict=True),
            {13: ['hic', 'hice', 'hicine'], 15: ['hunc'], 16: ['hujus', 'hujusce'], 17: ['huic'],
             18: ['hoc', 'hocine'], 19: ['hi'], 21: ['hos', 'hosce'], 22: ['horum'],
             23: ['his', 'hisce'], 24: ['his', 'hisce'], 25: ['haec', 'haece', 'haecine', 'haeccine'],
             27: ['hanc'], 28: ['hujus', 'hujusce'], 29: ['huic'], 30: ['hac'], 31: ['hae'],
             33: ['has', 'hasce'], 34: ['harum'], 35: ['his', 'hisce'], 36: ['his', 'hisce'], 37: ['hoc', 'hocine'],
             39: ['hoc', 'hocine'], 40: ['hujus', 'hujusce'], 41: ['huic'], 42: ['hoc', 'hocine'],
             43: ['haec', 'haecine', 'haeccine'], 45: ['ha', 'haine', 'hacine'], 46: ['horum'],
             47: ['his', 'hisce'], 48: ['his', 'hisce']},
            "Check that suffixes are well added"
        )

        self.assertEqual(
            decliner.decline("quicumque", collatinus_dict=True),
            {13: ['quicumque', 'quicunque'], 15: ['quemcumque', 'quemcunque'],
             16: ['cujuscumque', 'quojuscumque', 'cujuscunque', 'quojuscunque'],
             17: ['cuicumque', 'quoicumque', 'cuicunque', 'quoicunque'], 18: ['quocumque', 'quocunque'],
             19: ['quicumque', 'quicunque'], 21: ['quoscumque', 'quoscunque'], 22: ['quorumcumque', 'quorumcunque'],
             23: ['quibuscumque', 'quibuscunque'], 25: ['quaecumque', 'quaecunque'],
             27: ['quamcumque', 'quamcunque'], 28: ['cujuscumque', 'quojuscumque', 'cujuscunque', 'quojuscunque'],
             29: ['cuicumque', 'quoicumque', 'cuicunque', 'quoicunque'], 30: ['quacumque', 'quacunque'],
             31: ['quaecumque', 'quaecunque'], 33: ['quascumque', 'quascunque'],
             34: ['quarumcumque', 'quarumcunque'], 35: ['quibuscumque', 'quibuscunque'],
             37: ['quodcumque', 'quodcunque'], 39: ['quodcumque', 'quodcunque'],
             40: ['cujuscumque', 'quojuscumque', 'cujuscunque', 'quojuscunque'],
             41: ['cuicumque', 'quoicumque', 'cuicunque', 'quoicunque'], 42: ['quocumque', 'quocunque'],
             43: ['quaecumque', 'quaecunque'], 45: ['quaecumque', 'quaecunque'],
             46: ['quorumcumque', 'quorumcunque'], 47: ['quibuscumque', 'quibuscunque']},
            "Constant suffix should be added"
        )
        self.assertEqual(
            decliner.decline("plerique", collatinus_dict=True),
            {19: ['plerique'], 20: ['plerique'], 21: ['plerosque'], 22: ['plerorumque'], 23: ['plerisque'],
             24: ['plerisque'], 31: ['pleraeque'], 32: ['pleraeque'], 33: ['plerasque'], 34: ['plerarumque'],
             35: ['plerisque'], 36: ['plerisque'], 43: ['pleraque'], 44: ['pleraque'], 45: ['pleraque'],
             46: ['plerorumque'], 47: ['plerisque'], 48: ['plerisque']},
            "Checking abs is applied correctly"
        )
        self.assertEqual(
            decliner.decline("edo", collatinus_dict=True)[122] + \
            decliner.decline("edo", collatinus_dict=True)[163],
            ["edis", "es"] + ['ederem', 'essem'],
            "Alternative desisences should be added, even with different root"
        )

    def test_collatinus_flatten_decline(self):
        """ Ensure that flattening decline result is consistant"""
        decliner = CollatinusDecliner()
        self.assertEqual(
            decliner.decline("via", flatten=True),
            ['via', 'via', 'viam', 'viae', 'viae', 'via', 'viae', 'viae', 'vias', 'viarum', 'viis', 'viis'],
            "Declination of via should be right"
        )
        self.assertEqual(
            decliner.decline("poesis", flatten=True),
            ['poesis', 'poesis', 'poesem', 'poesin', 'poesim', 'poesis', 'poeseos', 'poesi', 'poese', 'poeses',
             'poeses', 'poeses', 'poesis', 'poesium', 'poesibus', 'poesibus'],
            "Duplicity of forms should be accepted"
        )

    def test_collatinus_POS_decline(self):
        """ Ensure that POS decline result is consistant"""
        decliner = CollatinusDecliner()
        self.assertEqual(
            decliner.decline("via"),
            [('via', '--s----n-'), ('via', '--s----v-'), ('viam', '--s----a-'), ('viae', '--s----g-'),
             ('viae', '--s----d-'), ('via', '--s----b-'), ('viae', '--p----n-'), ('viae', '--p----v-'),
             ('vias', '--p----a-'), ('viarum', '--p----g-'), ('viis', '--p----d-'), ('viis', '--p----b-')]
            ,
            "Declination of via should be right"
        )
        self.assertEqual(
            decliner.decline("poesis"),
            [('poesis', '--s----n-'), ('poesis', '--s----v-'), ('poesem', '--s----a-'), ('poesin', '--s----a-'),
             ('poesim', '--s----a-'), ('poesis', '--s----g-'), ('poeseos', '--s----g-'), ('poesi', '--s----d-'),
             ('poese', '--s----b-'), ('poeses', '--p----n-'), ('poeses', '--p----v-'), ('poeses', '--p----a-'),
             ('poesis', '--p----a-'), ('poesium', '--p----g-'), ('poesibus', '--p----d-'),
             ('poesibus', '--p----b-')]
            ,
            "Duplicity of forms should be accepted"
        )

    def test_collatinus_raise(self):
        """ Unknown lemma should raise exception """
        def decline():
            decliner = CollatinusDecliner()
            decliner.decline("this lemma will never exist")

        self.assertRaises(
            UnknownLemma, decline
        )

    def french_stemmer_test(self):
        sentence = "ja departissent a itant quant par la vile vint errant tut a cheval " \
                    "une pucele en tut le siecle n'ot si bele un blanc palefrei chevalchot"
        stemmed_text = stem(sentence)
        target = "j depart a it quant par la vil v err tut a cheval un pucel en tut le siecl n' o si bel un blanc palefre" \
                    " chevalcho "
        self.assertEqual(stemmed_text, target)

if __name__ == '__main__':
    unittest.main()
