"""Test cltk.stem."""

import unittest

from cltk.core.exceptions import CLTKException
from cltk.data.fetch import FetchCorpus
from cltk.stem.akkadian.atf_converter import ATFConverter
from cltk.stem.akkadian.bound_form import BoundForm as AkkadianBoundForm
from cltk.stem.akkadian.cv_pattern import CVPattern as AkkadianCVPattern
from cltk.stem.akkadian.declension import NaiveDecliner as AkkadianNaiveDecliner
from cltk.stem.akkadian.stem import Stemmer as AkkadianStemmer
from cltk.stem.akkadian.syllabifier import Syllabifier as AkkadianSyllabifier
from cltk.stem.french.stem import stem
from cltk.stem.latin.declension import CollatinusDecliner
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.latin.stem import Stemmer
from cltk.stem.latin.syllabifier import Syllabifier
from cltk.stem.middle_english.stem import affix_stemmer as MiddleEnglishAffixStemmer
from cltk.stem.sanskrit.indian_syllabifier import Syllabifier as IndianSyllabifier


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    # def setUp(self):
    #     """Import sanskrit models first, some CSV files necessary for the
    #     Indian lang tokenizers.
    #     """
    #     corpus_importer = FetchCorpus('sanskrit')
    #     corpus_importer.import_corpus('sanskrit_models_cltk')
    #     file_rel = os.path.join(get_cltk_data_dir() + '/sanskrit/model/sanskrit_models_cltk/README.md')
    #     file = os.path.expanduser(file_rel)
    #     file_exists = os.path.isfile(file)
    #     self.assertTrue(file_exists)

    @classmethod
    def setUpClass(self):
        try:
            corpus_importer = FetchCorpus("san")
            corpus_importer.import_corpus("san_models_cltk")
            corpus_importer = FetchCorpus("grc")
            corpus_importer.import_corpus("grc_models_cltk")
        except:
            raise Exception("Failure to download test corpus")

    def test_latin_i_u_transform(self):
        """Test converting ``j`` to ``i`` and ``v`` to ``u``."""
        jv_replacer = JVReplacer()
        trans = jv_replacer.replace("vem jam VEL JAM")
        self.assertEqual(trans, "uem iam UEL IAM")

    def test_latin_stemmer(self):
        """Test Latin stemmer."""
        sentence = "Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum."  # pylint: disable=line-too-long
        stemmer = Stemmer()
        stemmed_text = stemmer.stem(sentence.lower())
        target = "est interd praestar mercatur r quaerere, nisi tam periculos sit, et it foenerari, si tam honestum. "  # pylint: disable=line-too-long
        self.assertEqual(stemmed_text, target)

    def test_latin_syllabifier(self):
        """Test Latin syllabifier."""
        word = "sidere"
        syllabifier = Syllabifier()
        syllables = syllabifier.syllabify(word)
        target = ["si", "de", "re"]
        self.assertEqual(syllables, target)
        # tests for macronized words
        macronized_word = "audītū"
        macronized_syllables = syllabifier.syllabify(macronized_word)
        macronized_target = ["au", "dī", "tū"]
        self.assertEqual(macronized_syllables, macronized_target)
        macronized_word2 = "conjiciō"
        macronized_syllables2 = syllabifier.syllabify(macronized_word2)
        macronized_target2 = ["con", "ji", "ci", "ō"]
        self.assertEqual(macronized_syllables2, macronized_target2)
        macronized_word3 = "ā"
        macronized_syllables3 = syllabifier.syllabify(macronized_word3)
        macronized_target3 = ["ā"]
        self.assertEqual(macronized_syllables3, macronized_target3)

    def test_syllabify(self):
        """Test Indic Syllabifier method"""
        correct = ["न", "म", "स्ते"]
        syllabifier = IndianSyllabifier("hindi")
        current = syllabifier.orthographic_syllabify("नमस्ते")
        self.assertEqual(current, correct)

    def test_get_offset(self):
        """Test Indic Syllabifier get_offset method"""
        correct = 40
        syllabifier = IndianSyllabifier("hindi")
        current = syllabifier.get_offset("न", "hi")
        self.assertEqual(current, correct)

    def test_coordinated_range(self):
        """Test Indic Syllabifier in_coordinated_range method"""
        syllabifier = IndianSyllabifier("hindi")
        current = syllabifier.get_offset("न", "hi")
        current1 = syllabifier.in_coordinated_range_offset(current)
        self.assertTrue(current1)

    def test_akkadian_bound_form(self):
        """Test Akkadian bound form method"""
        bound_former = AkkadianBoundForm()
        word = "awīlum"
        bound_form = bound_former.get_bound_form(word, "m")
        target = "awīl"
        self.assertEqual(bound_form, target)

    def test_akkadian_cv_pattern(self):
        """Test Akkadian CV pattern method"""
        cv_patterner = AkkadianCVPattern()
        word = "iparras"
        cv_pattern = cv_patterner.get_cv_pattern(word, pprint=True)
        target = "V₁C₁V₂C₂C₂V₂C₃"
        self.assertEqual(cv_pattern, target)

    def test_akkadian_declension(self):
        """Test Akkadian noun declension"""
        decliner = AkkadianNaiveDecliner()
        word = "iltum"
        declension = decliner.decline_noun(word, "f")
        target = [
            ("iltim", {"case": "genitive", "number": "singular"}),
            ("iltum", {"case": "nominative", "number": "singular"}),
            ("iltam", {"case": "accusative", "number": "singular"}),
            ("iltīn", {"case": "oblique", "number": "dual"}),
            ("iltān", {"case": "nominative", "number": "dual"}),
            ("ilātim", {"case": "oblique", "number": "plural"}),
            ("ilātum", {"case": "nominative", "number": "plural"}),
        ]
        self.assertEqual(sorted(declension), sorted(target))

    def test_akkadian_stemmer(self):
        """Test Akkadian stemmer"""
        stemmer = AkkadianStemmer()
        word = "šarrū"
        stem = stemmer.get_stem(word, "m")
        target = "šarr"
        self.assertEqual(stem, target)

    def test_akkadian_syllabifier(self):
        """Test Akkadian syllabifier"""
        syllabifier = AkkadianSyllabifier()
        word = "epištašu"
        syllables = syllabifier.syllabify(word)
        target = ["e", "piš", "ta", "šu"]
        self.assertEqual(syllables, target)

    """
    #? Someone fix this; assertTrue() doesn't make sense here
    def test_phonetic_vector(self):
        cor = [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0]
        correct = bytearray(cor)
        syllabifier = IndianSyllabifier('hindi')
        current = syllabifier.get_phonetic_feature_vector('न', 'hi')
        # self.assertTrue(current, correct)
    """

    def test_is_misc(self):
        """Test Indic Syllabifier is_misc method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertFalse(syllabifier.is_misc(v))

    def test_is_consonant(self):
        """Test Indic Syllabifier is_consonant method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertTrue(syllabifier.is_consonant(v))

    def test_is_vowel(self):
        """Test Indic Syllabifier is_vowel method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertFalse(syllabifier.is_vowel(v))

    def test_is_anusvaar(self):
        """Test Indic Syllabifier is_anusvaar method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertFalse(syllabifier.is_anusvaar(v))

    def test_is_plosive(self):
        """Test Indic Syllabifier is_plosive method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertTrue(syllabifier.is_plosive(v))

    def test_is_nukta(self):
        """Test Indic Syllabifier is_nukta method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertFalse(syllabifier.is_nukta(v))

    def test_is_valid(self):
        """Test Indic Syllabifier is_valid method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertTrue(syllabifier.is_valid(v))

    def test_is_dependent_vowel(self):
        """Test Indic Syllabifier is_dependent_vowel method"""
        syllabifier = IndianSyllabifier("hindi")
        v = syllabifier.get_phonetic_feature_vector("न", "hi")
        self.assertFalse(syllabifier.is_dependent_vowel(v))

    def test_collatinus_decline(self):
        """ Ensure lemmatization works well """
        decliner = CollatinusDecliner()

        def sort_result(result):
            return {key: sorted(val) for key, val in result.items()}

        self.maxDiff = None
        self.assertEqual(
            decliner.decline("via", collatinus_dict=True),
            {
                1: ["via"],
                2: ["via"],
                3: ["viam"],
                4: ["viae"],
                5: ["viae"],
                6: ["via"],
                7: ["viae"],
                8: ["viae"],
                9: ["vias"],
                10: ["viarum"],
                11: ["viis"],
                12: ["viis"],
            },
            "Declination of via should be right",
        )
        self.assertEqual(
            decliner.decline("doctus", collatinus_dict=True),
            {
                13: ["doctus"],
                14: ["docte"],
                15: ["doctum"],
                16: ["docti"],
                17: ["docto"],
                18: ["docto"],
                19: ["docti"],
                20: ["docti"],
                21: ["doctos"],
                22: ["doctorum"],
                23: ["doctis"],
                24: ["doctis"],
                25: ["docta"],
                26: ["docta"],
                27: ["doctam"],
                28: ["doctae"],
                29: ["doctae"],
                30: ["docta"],
                31: ["doctae"],
                32: ["doctae"],
                33: ["doctas"],
                34: ["doctarum"],
                35: ["doctis"],
                36: ["doctis"],
                37: ["doctum"],
                38: ["doctum"],
                39: ["doctum"],
                40: ["docti"],
                41: ["docto"],
                42: ["docto"],
                43: ["docta"],
                44: ["docta"],
                45: ["docta"],
                46: ["doctorum"],
                47: ["doctis"],
                48: ["doctis"],
                49: ["doctior"],
                50: ["doctior"],
                51: ["doctiorem"],
                52: ["doctioris"],
                53: ["doctiori"],
                54: ["doctiore"],
                55: ["doctiores"],
                56: ["doctiores"],
                57: ["doctiores"],
                58: ["doctiorum"],
                59: ["doctioribus"],
                60: ["doctioribus"],
                61: ["doctior"],
                62: ["doctior"],
                63: ["doctiorem"],
                64: ["doctioris"],
                65: ["doctiori"],
                66: ["doctiore"],
                67: ["doctiores"],
                68: ["doctiores"],
                69: ["doctiores"],
                70: ["doctiorum"],
                71: ["doctioribus"],
                72: ["doctioribus"],
                73: ["doctius"],
                74: ["doctius"],
                75: ["doctius"],
                76: ["doctioris"],
                77: ["doctiori"],
                78: ["doctiore"],
                79: ["doctiora"],
                80: ["doctiora"],
                81: ["doctiora"],
                82: ["doctiorum"],
                83: ["doctioribus"],
                84: ["doctioribus"],
                85: ["doctissimus"],
                86: ["doctissime"],
                87: ["doctissimum"],
                88: ["doctissimi"],
                89: ["doctissimo"],
                90: ["doctissimo"],
                91: ["doctissimi"],
                92: ["doctissimi"],
                93: ["doctissimos"],
                94: ["doctissimorum"],
                95: ["doctissimis"],
                96: ["doctissimis"],
                97: ["doctissima"],
                98: ["doctissima"],
                99: ["doctissimam"],
                100: ["doctissimae"],
                101: ["doctissimae"],
                102: ["doctissima"],
                103: ["doctissimae"],
                104: ["doctissimae"],
                105: ["doctissimas"],
                106: ["doctissimarum"],
                107: ["doctissimis"],
                108: ["doctissimis"],
                109: ["doctissimum"],
                110: ["doctissimum"],
                111: ["doctissimum"],
                112: ["doctissimi"],
                113: ["doctissimo"],
                114: ["doctissimo"],
                115: ["doctissima"],
                116: ["doctissima"],
                117: ["doctissima"],
                118: ["doctissimorum"],
                119: ["doctissimis"],
                120: ["doctissimis"],
            },
            "Doctus has three radicals and lots of forms",
        )
        self.assertEqual(
            sort_result(decliner.decline("verbex", collatinus_dict=True)),
            {
                1: ["berbex", "verbex", "vervex"],
                2: ["berbex", "verbex", "vervex"],
                3: ["berbecem", "verbecem", "vervecem"],
                4: ["berbecis", "verbecis", "vervecis"],
                5: ["berbeci", "verbeci", "verveci"],
                6: ["berbece", "verbece", "vervece"],
                7: ["berbeces", "verbeces", "verveces"],
                8: ["berbeces", "verbeces", "verveces"],
                9: ["berbeces", "verbeces", "verveces"],
                10: ["berbecum", "verbecum", "vervecum"],
                11: ["berbecibus", "verbecibus", "vervecibus"],
                12: ["berbecibus", "verbecibus", "vervecibus"],
            },  # Missing 12 ?
            "Verbex has two different roots : checking they are taken into account",
        )
        self.assertEqual(
            sort_result(decliner.decline("vendo", collatinus_dict=True)),
            {
                121: ["vendo"],
                122: ["vendis"],
                123: ["vendit"],
                124: ["vendimus"],
                125: ["venditis"],
                126: ["vendunt"],
                127: ["vendebam"],
                128: ["vendebas"],
                129: ["vendebat"],
                130: ["vendebamus"],
                131: ["vendebatis"],
                132: ["vendebant"],
                133: ["vendam"],
                134: ["vendes"],
                135: ["vendet"],
                136: ["vendemus"],
                137: ["vendetis"],
                138: ["vendent"],
                139: ["vendavi", "vendidi"],
                140: ["vendavisti", "vendidisti"],
                141: ["vendavit", "vendidit"],
                142: ["vendavimus", "vendidimus"],
                143: ["vendavistis", "vendidistis"],
                144: ["vendavere", "vendaverunt", "vendidere", "vendiderunt"],
                145: ["vendaveram", "vendideram"],
                146: ["vendaveras", "vendideras"],
                147: ["vendaverat", "vendiderat"],
                148: ["vendaveramus", "vendideramus"],
                149: ["vendaveratis", "vendideratis"],
                150: ["vendaverant", "vendiderant"],
                151: ["vendavero", "vendidero"],
                152: ["vendaveris", "vendideris"],
                153: ["vendaverit", "vendiderit"],
                154: ["vendaverimus", "vendiderimus"],
                155: ["vendaveritis", "vendideritis"],
                156: ["vendaverint", "vendiderint"],
                157: ["vendam"],
                158: ["vendas"],
                159: ["vendat"],
                160: ["vendamus"],
                161: ["vendatis"],
                162: ["vendant"],
                163: ["venderem"],
                164: ["venderes"],
                165: ["venderet"],
                166: ["venderemus"],
                167: ["venderetis"],
                168: ["venderent"],
                169: ["vendaverim", "vendiderim"],
                170: ["vendaveris", "vendideris"],
                171: ["vendaverit", "vendiderit"],
                172: ["vendaverimus", "vendiderimus"],
                173: ["vendaveritis", "vendideritis"],
                174: ["vendaverint", "vendiderint"],
                175: ["vendavissem", "vendidissem"],
                176: ["vendavisses", "vendidisses"],
                177: ["vendavisset", "vendidisset"],
                178: ["vendavissemus", "vendidissemus"],
                179: ["vendavissetis", "vendidissetis"],
                180: ["vendavissent", "vendidissent"],
                181: ["vende"],
                182: ["vendite"],
                183: ["vendito"],
                184: ["vendito"],
                185: ["venditote"],
                186: ["vendunto"],
                187: ["vendere"],
                188: ["vendavisse", "vendidisse"],
                189: ["vendens"],
                190: ["vendens"],
                191: ["vendentem"],
                192: ["vendentis"],
                193: ["vendenti"],
                194: ["vendente"],
                195: ["vendentes"],
                196: ["vendentes"],
                197: ["vendentes"],
                198: ["vendentium", "vendentum"],
                199: ["vendentibus"],
                200: ["vendentibus"],
                201: ["vendens"],
                202: ["vendens"],
                203: ["vendentem"],
                204: ["vendentis"],
                205: ["vendenti"],
                206: ["vendente"],
                207: ["vendentes"],
                208: ["vendentes"],
                209: ["vendentes"],
                210: ["vendentium", "vendentum"],
                211: ["vendentibus"],
                212: ["vendentibus"],
                213: ["vendens"],
                214: ["vendens"],
                215: ["vendens"],
                216: ["vendentis"],
                217: ["vendenti"],
                218: ["vendente"],
                219: ["vendentia"],
                220: ["vendentia"],
                221: ["vendentia"],
                222: ["vendentium", "vendentum"],
                223: ["vendentibus"],
                224: ["vendentibus"],
                225: ["vendaturus", "venditurus"],
                226: ["vendature", "venditure"],
                227: ["vendaturum", "venditurum"],
                228: ["vendaturi", "vendituri"],
                229: ["vendaturo", "vendituro"],
                230: ["vendaturo", "vendituro"],
                231: ["vendaturi", "vendituri"],
                232: ["vendaturi", "vendituri"],
                233: ["vendaturos", "vendituros"],
                234: ["vendaturorum", "venditurorum"],
                235: ["vendaturis", "vendituris"],
                236: ["vendaturis", "vendituris"],
                237: ["vendatura", "venditura"],
                238: ["vendatura", "venditura"],
                239: ["vendaturam", "vendituram"],
                240: ["vendaturae", "venditurae"],
                241: ["vendaturae", "venditurae"],
                242: ["vendatura", "venditura"],
                243: ["vendaturae", "venditurae"],
                244: ["vendaturae", "venditurae"],
                245: ["vendaturas", "vendituras"],
                246: ["vendaturarum", "venditurarum"],
                247: ["vendaturis", "vendituris"],
                248: ["vendaturis", "vendituris"],
                249: ["vendaturum", "venditurum"],
                250: ["vendaturum", "venditurum"],
                251: ["vendaturum", "venditurum"],
                252: ["vendaturi", "vendituri"],
                253: ["vendaturo", "vendituro"],
                254: ["vendaturo", "vendituro"],
                255: ["vendatura", "venditura"],
                256: ["vendatura", "venditura"],
                257: ["vendatura", "venditura"],
                258: ["vendaturorum", "venditurorum"],
                259: ["vendaturis", "vendituris"],
                260: ["vendaturis", "vendituris"],
                261: ["vendendum"],
                262: ["vendendi"],
                263: ["vendendo"],
                264: ["vendendo"],
                265: ["vendatum", "venditum"],
                266: ["vendatu", "venditu"],
                267: ["vendor"],
                268: ["vendere", "venderis"],
                269: ["venditur"],
                270: ["vendimur"],
                271: ["vendimini"],
                272: ["venduntur"],
                273: ["vendebar"],
                274: ["vendebare", "vendebaris"],
                275: ["vendebatur"],
                276: ["vendebamur"],
                277: ["vendebamini"],
                278: ["vendebantur"],
                279: ["vendar"],
                280: ["vendere", "venderis"],
                281: ["vendetur"],
                282: ["vendemur"],
                283: ["vendemini"],
                284: ["vendentur"],
                285: ["vendar"],
                286: ["vendare", "vendaris"],
                287: ["vendatur"],
                288: ["vendamur"],
                289: ["vendamini"],
                290: ["vendantur"],
                291: ["venderer"],
                292: ["venderere", "vendereris"],
                293: ["venderetur"],
                294: ["venderemur"],
                295: ["venderemini"],
                296: ["venderentur"],
                297: ["vendere"],
                298: ["vendimini"],
                299: ["venditor"],
                300: ["venditor"],
                301: ["venduntor"],
                302: ["vendi"],
                303: ["vendatus", "venditus"],
                304: ["vendate", "vendite"],
                305: ["vendatum", "venditum"],
                306: ["vendati", "venditi"],
                307: ["vendato", "vendito"],
                308: ["vendato", "vendito"],
                309: ["vendati", "venditi"],
                310: ["vendati", "venditi"],
                311: ["vendatos", "venditos"],
                312: ["vendatorum", "venditorum"],
                313: ["vendatis", "venditis"],
                314: ["vendatis", "venditis"],
                315: ["vendata", "vendita"],
                316: ["vendata", "vendita"],
                317: ["vendatam", "venditam"],
                318: ["vendatae", "venditae"],
                319: ["vendatae", "venditae"],
                320: ["vendata", "vendita"],
                321: ["vendatae", "venditae"],
                322: ["vendatae", "venditae"],
                323: ["vendatas", "venditas"],
                324: ["vendatarum", "venditarum"],
                325: ["vendatis", "venditis"],
                326: ["vendatis", "venditis"],
                327: ["vendatum", "venditum"],
                328: ["vendatum", "venditum"],
                329: ["vendatum", "venditum"],
                330: ["vendati", "venditi"],
                331: ["vendato", "vendito"],
                332: ["vendato", "vendito"],
                333: ["vendata", "vendita"],
                334: ["vendata", "vendita"],
                335: ["vendata", "vendita"],
                336: ["vendatorum", "venditorum"],
                337: ["vendatis", "venditis"],
                338: ["vendatis", "venditis"],
                339: ["vendendus"],
                340: ["vendende"],
                341: ["vendendum"],
                342: ["vendendi"],
                343: ["vendendo"],
                344: ["vendendo"],
                345: ["vendendi"],
                346: ["vendendi"],
                347: ["vendendos"],
                348: ["vendendorum"],
                349: ["vendendis"],
                350: ["vendendis"],
                351: ["vendenda"],
                352: ["vendenda"],
                353: ["vendendam"],
                354: ["vendendae"],
                355: ["vendendae"],
                356: ["vendenda"],
                357: ["vendendae"],
                358: ["vendendae"],
                359: ["vendendas"],
                360: ["vendendarum"],
                361: ["vendendis"],
                362: ["vendendis"],
                363: ["vendendum"],
                364: ["vendendum"],
                365: ["vendendum"],
                366: ["vendendi"],
                367: ["vendendo"],
                368: ["vendendo"],
                369: ["vendenda"],
                370: ["vendenda"],
                371: ["vendenda"],
                372: ["vendendorum"],
                373: ["vendendis"],
                374: ["vendendis"],
            },
            "Check verb vendo declines well",
        )
        self.assertEqual(
            decliner.decline("poesis", collatinus_dict=True),
            {
                1: ["poesis"],
                2: ["poesis"],
                3: ["poesem", "poesin", "poesim"],
                4: ["poesis", "poeseos"],
                5: ["poesi"],
                6: ["poese"],
                7: ["poeses"],
                8: ["poeses"],
                9: ["poeses", "poesis"],
                10: ["poesium"],
                11: ["poesibus"],
                12: ["poesibus"],
            },
            "Duplicity of forms should be accepted",
        )

        self.assertEqual(
            sort_result(decliner.decline("hic", collatinus_dict=True)),
            {
                13: ["hic", "hice", "hicine"],
                15: ["hunc"],
                16: ["hujus", "hujusce"],
                17: ["huic"],
                18: ["hoc", "hocine"],
                19: ["hi"],
                21: ["hos", "hosce"],
                22: ["horum"],
                23: ["his", "hisce"],
                24: ["his", "hisce"],
                25: ["haec", "haeccine", "haece", "haecine"],
                27: ["hanc"],
                28: ["hujus", "hujusce"],
                29: ["huic"],
                30: ["hac"],
                31: ["hae"],
                33: ["has", "hasce"],
                34: ["harum"],
                35: ["his", "hisce"],
                36: ["his", "hisce"],
                37: ["hoc", "hocine"],
                39: ["hoc", "hocine"],
                40: ["hujus", "hujusce"],
                41: ["huic"],
                42: ["hoc", "hocine"],
                43: ["haec", "haeccine", "haecine"],
                45: ["haec", "haeccine", "haecine"],
                46: ["horum"],
                47: ["his", "hisce"],
                48: ["his", "hisce"],
            },
            "Check that suffixes are well added",
        )
        self.assertEqual(
            sort_result(decliner.decline("quicumque", collatinus_dict=True)),
            {
                13: ["quicumque", "quicunque"],
                15: ["quemcumque", "quemcunque"],
                16: ["cujuscumque", "cujuscunque", "quojuscumque", "quojuscunque"],
                17: ["cuicumque", "cuicunque", "quoicumque", "quoicunque"],
                18: ["quocumque", "quocunque"],
                19: ["quicumque", "quicunque"],
                21: ["quoscumque", "quoscunque"],
                22: ["quorumcumque", "quorumcunque"],
                23: ["quibuscumque", "quibuscunque"],
                24: ["quibuscumque", "quibuscunque"],
                25: ["quaecumque", "quaecunque"],
                27: ["quamcumque", "quamcunque"],
                28: ["cujuscumque", "cujuscunque", "quojuscumque", "quojuscunque"],
                29: ["cuicumque", "cuicunque", "quoicumque", "quoicunque"],
                30: ["quacumque", "quacunque"],
                31: ["quaecumque", "quaecunque"],
                33: ["quascumque", "quascunque"],
                34: ["quarumcumque", "quarumcunque"],
                35: ["quibuscumque", "quibuscunque"],
                36: ["quibuscumque", "quibuscunque"],
                37: ["quodcumque", "quodcunque"],
                39: ["quodcumque", "quodcunque"],
                40: ["cujuscumque", "cujuscunque", "quojuscumque", "quojuscunque"],
                41: ["cuicumque", "cuicunque", "quoicumque", "quoicunque"],
                42: ["quocumque", "quocunque"],
                43: ["quaecumque", "quaecunque"],
                45: ["quaecumque", "quaecunque"],
                46: ["quorumcumque", "quorumcunque"],
                47: ["quibuscumque", "quibuscunque"],
                48: ["quibuscumque", "quibuscunque"],
            },
            "Constant suffix should be added",
        )
        self.assertEqual(
            decliner.decline("plerique", collatinus_dict=True),
            {
                19: ["plerique"],
                20: ["plerique"],
                21: ["plerosque"],
                22: ["plerorumque"],
                23: ["plerisque"],
                24: ["plerisque"],
                31: ["pleraeque"],
                32: ["pleraeque"],
                33: ["plerasque"],
                34: ["plerarumque"],
                35: ["plerisque"],
                36: ["plerisque"],
                43: ["pleraque"],
                44: ["pleraque"],
                45: ["pleraque"],
                46: ["plerorumque"],
                47: ["plerisque"],
                48: ["plerisque"],
            },
            "Checking abs is applied correctly",
        )
        self.assertEqual(
            decliner.decline("edo", collatinus_dict=True)[122]
            + decliner.decline("edo", collatinus_dict=True)[163],
            ["edis", "es"] + ["ederem", "essem"],
            "Alternative desisences should be added, even with different root",
        )

        self.assertEqual(
            decliner.decline("aggero2")[0],
            ("aggero", "v1spia---"),
            "Lemma with disambiguation indexes should not fail their declension [aggero and not aggeroo]",
        )

    def test_collatinus_flatten_decline(self):
        """ Ensure that flattening decline result is consistant"""
        decliner = CollatinusDecliner()
        self.assertEqual(
            decliner.decline("via", flatten=True),
            [
                "via",
                "via",
                "viam",
                "viae",
                "viae",
                "via",
                "viae",
                "viae",
                "vias",
                "viarum",
                "viis",
                "viis",
            ],
            "Declination of via should be right",
        )
        self.assertEqual(
            decliner.decline("poesis", flatten=True),
            [
                "poesis",
                "poesis",
                "poesem",
                "poesin",
                "poesim",
                "poesis",
                "poeseos",
                "poesi",
                "poese",
                "poeses",
                "poeses",
                "poeses",
                "poesis",
                "poesium",
                "poesibus",
                "poesibus",
            ],
            "Duplicity of forms should be accepted",
        )

    def test_collatinus_POS_decline(self):
        """ Ensure that POS decline result is consistant"""
        decliner = CollatinusDecliner()
        self.assertEqual(
            decliner.decline("via"),
            [
                ("via", "--s----n-"),
                ("via", "--s----v-"),
                ("viam", "--s----a-"),
                ("viae", "--s----g-"),
                ("viae", "--s----d-"),
                ("via", "--s----b-"),
                ("viae", "--p----n-"),
                ("viae", "--p----v-"),
                ("vias", "--p----a-"),
                ("viarum", "--p----g-"),
                ("viis", "--p----d-"),
                ("viis", "--p----b-"),
            ],
            "Declination of via should be right",
        )
        self.assertEqual(
            decliner.decline("poesis"),
            [
                ("poesis", "--s----n-"),
                ("poesis", "--s----v-"),
                ("poesem", "--s----a-"),
                ("poesin", "--s----a-"),
                ("poesim", "--s----a-"),
                ("poesis", "--s----g-"),
                ("poeseos", "--s----g-"),
                ("poesi", "--s----d-"),
                ("poese", "--s----b-"),
                ("poeses", "--p----n-"),
                ("poeses", "--p----v-"),
                ("poeses", "--p----a-"),
                ("poesis", "--p----a-"),
                ("poesium", "--p----g-"),
                ("poesibus", "--p----d-"),
                ("poesibus", "--p----b-"),
            ],
            "Duplicity of forms should be accepted",
        )

    def test_collatinus_multiple_radicals(self):
        coll = CollatinusDecliner()
        self.assertEqual(
            sorted(coll.decline("sandaraca")[:3], key=lambda x: x[0]),
            [
                ("sandaraca", "--s----n-"),
                ("sandaracha", "--s----n-"),
                ("sanderaca", "--s----n-"),
            ],
        )
        jajunitas = [form for form, _ in coll.decline("jajunitas")]
        self.assertIn("jajunitas", jajunitas)
        self.assertIn("jejunitas", jajunitas)
        self.assertIn("jajunitatem", jajunitas)
        self.assertIn("jejunitatem", jajunitas)

    def test_collatinus_raise(self):
        """ Unknown lemma should raise exception """

        def decline():
            decliner = CollatinusDecliner()
            decliner.decline("this lemma will never exist")

        self.assertRaises(CLTKException, decline)

    def french_stemmer_test(self):
        sentence = (
            "ja departissent a itant quant par la vile vint errant tut a cheval "
            "une pucele en tut le siecle n'ot si bele un blanc palefrei chevalchot"
        )
        stemmed_text = stem(sentence)
        target = (
            "j depart a it quant par la vil v err tut a cheval un pucel en tut le siecl n' o si bel un blanc palefre"
            " chevalcho "
        )
        self.assertEqual(stemmed_text, target)

    def test_middle_english_stemmer(self):
        sentence = [
            "the",
            "speke",
            "the",
            "henmest",
            "kyng",
            "in",
            "the",
            "hillis",
            "he",
            "beholdis",
            "he",
            "lokis",
            "vnder",
            "his",
            "hondis",
            "and",
            "his",
            "hed",
            "heldis",
        ]
        stemmed = MiddleEnglishAffixStemmer(sentence)
        target = "the spek the henm kyng in the hill he behold he lok vnd his hond and his hed held"
        self.assertEqual(stemmed, target)

    def test_convert_consonant(self):
        """
        Tests convert_consonant.
        """
        atf = ATFConverter()
        signs = ["as,", "S,ATU", "tet,", "T,et", "sza", "ASZ"]
        target = ["aṣ", "ṢATU", "teṭ", "Ṭet", "ša", "AŠ"]
        output = [atf._convert_consonant(s) for s in signs]
        self.assertEqual(output, target)

    def test_get_number_from_sign(self):
        """
        Tests get_number_from_sign.
        """
        atf = ATFConverter()
        signs = ["a", "a1", "be2", "bad3", "buru14"]
        target = [0, 1, 2, 3, 14]
        output = [atf._get_number_from_sign(s)[1] for s in signs]
        self.assertEqual(output, target)

    def test_single_sign(self):
        """
        Tests process with two_three as active.
        """
        atf = ATFConverter(two_three=True)
        signs = ["a", "a1", "a2", "a3", "be2", "be3", "bad2", "bad3"]
        target = ["a", "a₁", "a₂", "a₃", "be₂", "be₃", "bad₂", "bad₃"]
        output = atf.process(signs)
        self.assertEqual(output, target)

    def test_accents(self):
        """
        Tests process with two_three as inactive.
        """
        atf = ATFConverter(two_three=False)
        signs = ["a", "a2", "a3", "be2", "bad3", "buru14"]
        target = ["a", "á", "à", "bé", "bàd", "buru₁₄"]
        output = atf.process(signs)
        self.assertEqual(output, target)

    def test_unknown_token(self):
        """
        Tests process with unrecognizable tokens.
        """
        atf = ATFConverter(two_three=True)
        signs = ["a2", "☉", "be3"]
        target = ["a₂", "☉", "be₃"]
        output = atf.process(signs)
        self.assertEqual(output, target)


if __name__ == "__main__":
    unittest.main()
