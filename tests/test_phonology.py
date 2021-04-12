"""Test cltk.phonology."""

__author__ = [
    "Jack Duff <jmunroeduff@gmail.com>",
    "Clément Besnier <clem@clementbesnier.fr>",
]
__license__ = "MIT License. See LICENSE."

import unicodedata
import unittest

from cltk.alphabet.gmh import normalize_middle_high_german
from cltk.phonology.arb.romanization import transliterate as arabic_transliterate
from cltk.phonology.gmh import syllabifier as mhgs
from cltk.phonology.gmh import transcription as mhgt
from cltk.phonology.got import transcription as gothic
from cltk.phonology.grc import transcription as grc
from cltk.phonology.lat import transcription as lat
from cltk.phonology.lat.syllabifier import syllabify as lat_syllabify
from cltk.phonology.non import transcription as ont
from cltk.phonology.non import utils as ut
from cltk.phonology.non.old_swedish import transcription as old_swedish
from cltk.phonology.non.syllabifier import invalid_onsets
from cltk.phonology.syllabify import Syllabifier, Syllable
from cltk.tokenizers.non import OldNorseWordTokenizer


class TestSequenceFunctions(unittest.TestCase):
    """Class for unittest"""

    """Test the Latin Library corpus reader filter"""

    @classmethod
    def setUpClass(self):
        self.greek_transcriber = grc.Transcriber("Attic", "Probert")
        self.latin_transcriber = lat.Transcriber("Classical", "Allen")

    """greek.transcription"""

    def test_greek_refresh(self):
        """Test the Word class's `_refresh` method in Greek."""
        test_word = grc.Word("pʰór.miŋks", grc.GREEK["Attic"]["Probert"])
        test_word._refresh()
        contexts = [
            test_word.phones[0].left.ipa,
            test_word.phones[1].left.ipa,
            test_word.phones[1].right.ipa,
            test_word.phones[-1].right.ipa,
        ]
        target = [
            grc.Phone("#").ipa,
            grc.Phone("pʰ").ipa,
            grc.Phone("r").ipa,
            grc.Phone("#").ipa,
        ]
        self.assertEqual(contexts, target)

    def test_greek_r_devoice(self):
        """Test the Word class's method `_r_devoice` in Greek."""
        condition_1 = grc.Word("rɑ́ks", grc.GREEK["Attic"]["Probert"])
        condition_1._refresh()
        condition_1._r_devoice()
        condition_2 = grc.Word("syrrɑ́ptɔː", grc.GREEK["Attic"]["Probert"])
        condition_2._refresh()
        condition_2._r_devoice()
        outputs = [
            "".join(p.ipa for p in condition_1.phones),
            "".join(p.ipa for p in condition_2.phones),
        ]
        target = [unicodedata.normalize("NFC", y) for y in ["r̥ɑ́ks", "syrr̥ɑ́ptɔː"]]
        self.assertEqual(outputs, target)

    def test_greek_s_voice_assimilation(self):
        """Test the Word class's method `_s_voice_assimilation` in Greek."""
        condition = grc.Word("ẹːrgɑsménon", grc.GREEK["Attic"]["Probert"])
        condition._refresh()
        condition._s_voice_assimilation()
        output = "".join([p.ipa for p in condition.phones])
        target = unicodedata.normalize("NFC", "ẹːrgɑzménon")
        self.assertEqual(output, target)

    def test_greek_nasal_place_assimilation(self):
        """Test the Word method `_nasal_place_assimilation` in Greek."""
        condition_1 = grc.Word("pʰórmigks", grc.GREEK["Attic"]["Probert"])
        condition_1._refresh()
        condition_1._nasal_place_assimilation()
        condition_2 = grc.Word("ɑ́ggelos", grc.GREEK["Attic"]["Probert"])
        condition_2._refresh()
        condition_2._nasal_place_assimilation()
        outputs = [
            "".join([p.ipa for p in condition_1.phones]),
            "".join([p.ipa for p in condition_2.phones]),
        ]
        target = [unicodedata.normalize("NFC", y) for y in ["pʰórmiŋks", "ɑ́ŋgelos"]]
        self.assertEqual(outputs, target)

    def test_greek_g_nasality_assimilation(self):
        """Test the Word class's `_g_nasality_assimilation` in Greek."""
        condition = grc.Word("gignɔ́ːskɔː", grc.GREEK["Attic"]["Probert"])
        condition._refresh()
        condition._g_nasality_assimilation()
        output = "".join([p.ipa for p in condition.phones])
        target = unicodedata.normalize("NFC", "giŋnɔ́ːskɔː")
        self.assertEqual(output, target)

    def test_greek_alternate(self):
        """Test the Word class's `_alternate` in Greek."""
        raw_inputs = [
            "rɑ́ks",
            "syrrɑ́ptɔː",
            "ẹːrgɑsménon",
            "pʰórmigks",
            "ɑ́ggelos",
            "gignɔ́ːskɔː",
        ]
        outputs = []
        for i in raw_inputs:
            w = grc.Word(i, grc.GREEK["Attic"]["Probert"])
            w._alternate()
            outputs.append("".join([p.ipa for p in w.phones]))
        target = [
            unicodedata.normalize("NFC", y)
            for y in [
                "r̥ɑ́ks",
                "syrr̥ɑ́ptɔː",
                "ẹːrgɑzménon",
                "pʰórmiŋks",
                "ɑ́ŋgelos",
                "giŋnɔ́ːskɔː",
            ]
        ]
        self.assertEqual(outputs, target)

    def test_greek_syllabify(self):
        """Test the Word class's `_syllabify` in Greek."""
        raw_inputs = ["lẹ́ːpẹː", "píptɔː", "téknọː", "skɛ̂ːptron"]
        outputs = []
        for i in raw_inputs:
            w = grc.Word(i, grc.GREEK["Attic"]["Probert"])
            w._alternate()
            outputs.append(
                ["".join([p.ipa for l in n for p in l]) for n in w.syllabify()]
            )
        target = [
            [unicodedata.normalize("NFC", s) for s in y]
            for y in [
                ["lẹ́ː", "pẹː"],
                ["píp", "tɔː"],
                ["té", "knọː"],
                ["skɛ̂ːp", "tron"],
            ]
        ]
        self.assertEqual(outputs, target)

    def test_greek_print_ipa(self):
        """Test the Word class's `_print_ipa` in Greek."""
        w = grc.Word("élipe", grc.GREEK["Attic"]["Probert"])
        output = [w._print_ipa(True), w._print_ipa(False)]
        target = [
            unicodedata.normalize("NFC", "é.li.pe"),
            unicodedata.normalize("NFC", "élipe"),
        ]
        self.assertEqual(output, target)

    def test_greek_parse_diacritics(self):
        """Test the Transcriber class's `_parse_diacritics` in Greek."""
        inputs = ["ἄ", "Φ", "ῷ", "ὑ", "ϊ", "ῑ"]
        outputs = [self.greek_transcriber._parse_diacritics(char) for char in inputs]
        target = [
            unicodedata.normalize("NFC", c)
            for c in [
                "α/" + grc.chars.ACUTE + "//",
                "φ///",
                "ω/" + grc.chars.CIRCUMFLEX + "/" + grc.chars.IOTA_SUBSCRIPT + "/",
                "h///υ///",
                "ι//" + grc.chars.DIAERESIS + "/",
                "ι//" + grc.chars.LONG + "/",
            ]
        ]
        self.assertEqual(outputs, target)

    def test_greek_prep_text(self):
        """Test the Transcriber class's `_prep_text` in Greek."""
        inputs = ["λείπειν", "ὕπνῳ"]
        outputs = [self.greek_transcriber._prep_text(w) for w in inputs]
        target = [
            [
                ("λ", "", ""),
                ("ει", "́", ""),
                ("π", "", ""),
                ("ει", "", ""),
                ("ν", "", ""),
            ],
            [
                ("h", "", ""),
                ("υ", "́", ""),
                ("π", "", ""),
                ("ν", "", ""),
                ("ωι", "", "̄"),
            ],
        ]
        self.assertEqual(outputs, target)

    def test_transcriber_probert(self):
        """Test Attic Greek IPA transcription via Probert reconstruction."""
        transcriber = self.greek_transcriber.transcribe
        transcription = [
            transcriber(x)
            for x in [
                unicodedata.normalize("NFC", y)
                for y in ["ῥάξ", "εἰργασμένον", "φόρμιγξ", "γιγνώσκω"]
            ]
        ]
        target = [
            unicodedata.normalize("NFC", y)
            for y in [
                "[r̥ɑ́ks]",
                "[ẹːr.gɑz.mé.non]",
                "[pʰór.miŋks]",
                "[giŋ.nɔ́ːs.kɔː]",
            ]
        ]
        self.assertEqual(transcription, target)

    """lat.transcription"""

    def test_latin_refresh(self):
        """Test the Word class's `_refresh` method in Latin."""
        test_word = lat.Word("ɔmn̪ɪs", lat.LATIN["Classical"]["Allen"])
        test_word._refresh()
        contexts = [
            test_word.phones[0].left.ipa,
            test_word.phones[1].left.ipa,
            test_word.phones[1].right.ipa,
            test_word.phones[-1].right.ipa,
        ]
        target = [
            grc.Phone("#").ipa,
            grc.Phone("ɔ").ipa,
            grc.Phone("n̪").ipa,
            grc.Phone("#").ipa,
        ]
        self.assertEqual(contexts, target)

    def test_latin_j_maker(self):
        """Test the Word class's method `_j_maker` in Latin."""
        condition = lat.Word("t̪roːɪaj", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._j_maker()
        output = "".join([p.ipa for p in condition.phones])
        target = unicodedata.normalize("NFC", "t̪roːjaj")
        self.assertEqual(output, target)

    def test_latin_w_maker(self):
        """Test the Word class's method `_w_maker` in Latin."""
        condition = lat.Word("ʊɪrʊmkʷɛ", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._w_maker()
        output = "".join([p.ipa for p in condition.phones])
        target = unicodedata.normalize("NFC", "wɪrʊmkʷɛ")
        self.assertEqual(output, target)

    def test_latin_wj_block(self):
        """Test the Word class's method `_wj_maker` in Latin."""
        condition = lat.Word("wjrʊmkʷɛ", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._wj_block()
        output = "".join([p.ipa for p in condition.phones])
        target = unicodedata.normalize("NFC", "wɪrʊmkʷɛ")
        self.assertEqual(output, target)

    def test_latin_uj_diph_maker(self):
        """Test the Word class's method `_uj_diph_maker` in Latin."""
        condition = lat.Word("kʊɪ", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._uj_diph_maker()
        output = "".join([p.ipa for p in condition.phones])
        target = unicodedata.normalize("NFC", "kuj")
        self.assertEqual(output, target)

    def test_latin_b_devoice(self):
        """Test the Word class's method `_b_devoice` in Latin."""
        condition_1 = lat.Word("abs", lat.LATIN["Classical"]["Allen"])
        condition_1._refresh()
        condition_1._b_devoice()
        condition_2 = lat.Word("sʊbt̪ʊs", lat.LATIN["Classical"]["Allen"])
        condition_2._refresh()
        condition_2._b_devoice()
        outputs = [
            "".join([p.ipa for p in condition_1.phones]),
            "".join([p.ipa for p in condition_2.phones]),
        ]
        target = [unicodedata.normalize("NFC", y) for y in ["aps", "sʊpt̪ʊs"]]
        self.assertEqual(outputs, target)

    def test_latin_final_m_drop(self):
        """Test the Word class's method `_final_m_drop` in Latin."""
        condition = lat.Word("kʷaːrum", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._final_m_drop()
        output = "".join([p.ipa for p in condition.phones])
        target = unicodedata.normalize("NFC", "kʷaːrũː")
        self.assertEqual(output, target)

    def test_latin_n_place_assimilation(self):
        """Test the Word class's method `_n_place_assimilation` in Latin."""
        condition = lat.Word("lɪn̪gʷa", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._n_place_assimilation()
        output = "".join([p.ipa for p in condition.phones])
        target = unicodedata.normalize("NFC", "lɪŋgʷa")
        self.assertEqual(output, target)

    def test_latin_g_n_nasality_assimilation(self):
        """Test the Word class's `_g_n_nasality_assimilation` in Latin."""
        condition = lat.Word("magn̪ʊs", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._g_n_nasality_assimilation()
        output = "".join([p.ipa for p in condition.phones])
        target = unicodedata.normalize("NFC", "maŋn̪ʊs")
        self.assertEqual(output, target)

    def test_latin_ns_nf_lengthening(self):
        """Test the Word class's method `_ns_nf_lengthening` in Latin."""
        condition_1 = lat.Word("kɔn̪sɔl", lat.LATIN["Classical"]["Allen"])
        condition_1._refresh()
        condition_1._ns_nf_lengthening()
        condition_2 = lat.Word("kɔn̪fɛkiː", lat.LATIN["Classical"]["Allen"])
        condition_2._refresh()
        condition_2._ns_nf_lengthening()
        outputs = [
            "".join([p.ipa for p in condition_1.phones]),
            "".join([p.ipa for p in condition_2.phones]),
        ]
        target = [unicodedata.normalize("NFC", y) for y in ["kɔːn̪sɔl", "kɔːn̪fɛkiː"]]
        self.assertEqual(outputs, target)

    def test_latin_l_darken(self):
        """Test the Word class's method `_l_darken` in Latin."""
        condition_1 = lat.Word("bɛlgaj", lat.LATIN["Classical"]["Allen"])
        condition_1._refresh()
        condition_1._l_darken()
        condition_2 = lat.Word("kɔːn̪sɔl", lat.LATIN["Classical"]["Allen"])
        condition_2._refresh()
        condition_2._l_darken()
        outputs = [
            "".join([p.ipa for p in condition_1.phones]),
            "".join([p.ipa for p in condition_2.phones]),
        ]
        target = [unicodedata.normalize("NFC", y) for y in ["bɛɫgaj", "kɔːn̪sɔɫ"]]
        self.assertEqual(outputs, target)

    def test_latin_j_z_doubling(self):
        """Test the Word class's method `_j_z_doubling` in Latin."""
        condition_1 = lat.Word("t̪roːjaj", lat.LATIN["Classical"]["Allen"])
        condition_1._refresh()
        condition_1._j_z_doubling()
        condition_2 = lat.Word("amaːzɔn", lat.LATIN["Classical"]["Allen"])
        condition_2._refresh()
        condition_2._j_z_doubling()
        outputs = [
            "".join([p.ipa for p in condition_1.phones]),
            "".join([p.ipa for p in condition_2.phones]),
        ]
        target = [unicodedata.normalize("NFC", y) for y in ["t̪roːjjaj", "amaːzzɔn"]]
        self.assertEqual(outputs, target)

    def test_latin_long_vowel_catcher(self):
        """Test the Word class's method `_long_vowel_catcher` in Latin."""
        conditions = [
            lat.Word(s, lat.LATIN["Classical"]["Allen"])
            for s in ["ɪː", "ʊː", "ɛː", "ɪ̃ː", "ʊ̃ː", "ɛ̃ː"]
        ]
        for w in conditions:
            w._long_vowel_catcher()
        outputs = ["".join([p.ipa for p in c.phones]) for c in conditions]
        target = [
            unicodedata.normalize("NFC", y)
            for y in ["iː", "uː", "eː", "ĩː", "ũː", "ẽː"]
        ]
        self.assertEqual(outputs, target)

    def test_latin_e_i_closer_before_vowel(self):
        """Test the Word class's `_e_i_closer_before_vowel` in Latin."""
        condition_1 = lat.Word("gaɫlɪa", lat.LATIN["Classical"]["Allen"])
        condition_1._refresh()
        condition_1._e_i_closer_before_vowel()
        condition_2 = lat.Word("mɛa", lat.LATIN["Classical"]["Allen"])
        condition_2._refresh()
        condition_2._e_i_closer_before_vowel()
        outputs = [
            "".join([p.ipa for p in condition_1.phones]),
            "".join([p.ipa for p in condition_2.phones]),
        ]
        target = [unicodedata.normalize("NFC", y) for y in ["gaɫlɪ̣a", "mɛ̣a"]]
        self.assertEqual(outputs, target)

    def test_latin_intervocalic_j(self):
        """Test the Word class's method `_intervocalic_j` in Latin."""
        condition = lat.Word("gaɫlɪ̣a", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._intervocalic_j()
        outputs = "".join([p.ipa for p in condition.phones])
        target = unicodedata.normalize("NFC", "gaɫlɪ̣ja")
        self.assertEqual(outputs, target)

    def test_latin_alternate(self):
        """Test the Word class's method `_alternate` in Latin."""
        raw_inputs = ["gallɪa", "d̪iːʊiːsa", "kʷaːrʊm"]
        outputs = []
        for i in raw_inputs:
            w = lat.Word(i, lat.LATIN["Classical"]["Allen"])
            w._alternate()
            outputs.append("".join([p.ipa for p in w.phones]))
        target = [
            unicodedata.normalize("NFC", y)
            for y in ["gaɫlɪ̣ja", "d̪iːwiːsa", "kʷaːrũː"]
        ]
        self.assertEqual(outputs, target)

    def test_latin_syllabify(self):
        """Test the Word class's `_syllabify` in Latin."""
        raw_inputs = ["arma", "kan̪oː", "t̪roːjjaj", "gaɫlɪ̣ja"]
        outputs = []
        for i in raw_inputs:
            w = lat.Word(i, lat.LATIN["Classical"]["Allen"])
            w.syllabify()
            outputs.append(
                ["".join([p.ipa for l in n for p in l]) for n in w.syllabify()]
            )
        target = [
            [unicodedata.normalize("NFC", s) for s in y]
            for y in [
                ["ar", "ma"],
                ["ka", "n̪oː"],
                ["t̪roːj", "jaj"],
                ["gaɫ", "lɪ̣", "ja"],
            ]
        ]
        self.assertEqual(outputs, target)

    def test_latin_syllabifier(self):
        """Test Latin syllabifier."""
        word = "sidere"
        syllables = lat_syllabify(word)
        target = ["si", "de", "re"]
        self.assertEqual(syllables, target)

        # tests for macronized words
        macronized_word = "audītū"
        macronized_syllables = lat_syllabify(macronized_word)
        macronized_target = ["au", "dī", "tū"]
        self.assertEqual(macronized_syllables, macronized_target)

        macronized_word2 = "conjiciō"
        macronized_syllables2 = lat_syllabify(macronized_word2)
        macronized_target2 = ["con", "ji", "ci", "ō"]
        self.assertEqual(macronized_syllables2, macronized_target2)

        macronized_word3 = "ā"
        macronized_syllables3 = lat_syllabify(macronized_word3)
        macronized_target3 = ["ā"]
        self.assertEqual(macronized_syllables3, macronized_target3)

    def test_latin_print_ipa(self):
        """Test the Word class's method `_print_ipa` in Latin."""
        inputs = [
            lat.Word(w, lat.LATIN["Classical"]["Allen"])
            for w in ["gaɫlɪ̣ja", "d̪iːwiːsa"]
        ]
        output = [
            [
                w._print_ipa(syllabify=False, accentuate=False),
                w._print_ipa(syllabify=True, accentuate=False),
                w._print_ipa(syllabify=True, accentuate=True),
            ]
            for w in inputs
        ]
        target = [
            [
                unicodedata.normalize("NFC", x)
                for x in ["gaɫlɪ̣ja", "gaɫ.lɪ̣.ja", "'gaɫ.lɪ̣.ja"]
            ],
            [
                unicodedata.normalize("NFC", x)
                for x in ["d̪iːwiːsa", "d̪iː.wiː.sa", "d̪iː.'wiː.sa"]
            ],
        ]
        self.assertEqual(output, target)

    def test_latin_parse_diacritics(self):
        """Test the Transcriber class's `_parse_diacritics` in Latin."""
        inputs = ["a", "ū", "ï"]
        outputs = [self.latin_transcriber._parse_diacritics(char) for char in inputs]
        target = [
            unicodedata.normalize("NFC", c)
            for c in [
                "a///",
                "u/" + lat.chars.LONG + "//",
                "i//" + lat.chars.DIAERESIS + "/",
            ]
        ]
        self.assertEqual(outputs, target)

    def test_latin_prep_text(self):
        """Test the Transcriber class's `_prep_text` in Latin."""
        inputs = ["ūnam", "qui", "Belgae"]
        outputs = [self.latin_transcriber._prep_text(w) for w in inputs]
        target = [
            [("u", "̄", ""), ("n", "", ""), ("a", "", ""), ("m", "", "")],
            [("qu", "", ""), ("i", "", "")],
            [
                ("b", "", ""),
                ("e", "", ""),
                ("l", "", ""),
                ("g", "", ""),
                ("ae", "", ""),
            ],
        ]
        self.assertEqual(outputs, target)

    def test_transcriber_allen_without_macronizer(self):
        """Test Classical Latin IPA transcription via Allen reconstruction,\
         input pre-macronized."""
        transcriber = self.latin_transcriber.transcribe
        transcription = [
            transcriber(x, macronize=False)
            for x in [
                unicodedata.normalize("NFC", y)
                for y in [
                    "Trōiae",
                    "Gallia",
                    "dīuīsa",
                    "ūnam",
                    "incolunt",
                    "Belgae",
                ]
            ]
        ]
        target = [
            unicodedata.normalize("NFC", y)
            for y in [
                "['t̪roːj.jaj]",
                "['gaɫ.lɪ̣.ja]",
                "[d̪iː.'wiː.sa]",
                "['uː.n̪ãː]",
                "['ɪŋ.kɔ.lʊn̪t̪]",
                "['bɛɫ.gaj]",
            ]
        ]
        self.assertEqual(transcription, target)

    def test_transcriber_allen_with_macronizer(self):
        """Test Classical Latin IPA transcription via Allen reconstruction,\
         with automatic macronization."""
        transcriber = self.latin_transcriber.transcribe
        transcription = transcriber(
            "Quo usque tandem, O Catilina, abutere nostra patientia?", macronize=True
        )
        target = (
            "['kʷoː 'ʊs.kʷɛ 't̪an̪.d̪ẽː 'oː ka.t̪ɪ.'liː.n̪aː a.buː.'t̪eː.rɛ"
            + " 'n̪ɔs.t̪raː pa.t̪ɪ̣.'jɛn̪.t̪ɪ̣.ja]"
        )
        self.assertEqual(transcription, target)

    def test_arabic_transliterate(self):
        """
         arabic transliterate: Roman <-> Arabic
        :return:
        """
        ar_string = "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ"
        buckwalter_string = "bisomi Allhi Alra~Hom`ni Alra~Hiyomi"
        iso2332_string = "bis°mi ʾllhi ʾlraّḥ°mٰni ʾlraّḥiy°mi"
        mode = "buckwalter"
        ignore = ""
        reverse = True

        # from arabic native script to buckwalter
        assert (
            arabic_transliterate(mode, ar_string, ignore, reverse)
            == "bisomi Allhi Alra~Hom`ni Alra~Hiyomi"
        )
        # from buckwalter to arabic native script
        reverse = False
        assert (
            arabic_transliterate(mode, buckwalter_string, ignore, reverse)
            == "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ"
        )

        # from arabic native script to ISO233-2
        mode = "iso233-2"
        reverse = True
        assert (
            arabic_transliterate(mode, ar_string, ignore, reverse)
            == "bis°mi ʾllhi ʾlraّḥ°mٰni ʾlraّḥiy°mi"
        )

        # from iso233-2 to arabic native script
        reverse = False
        assert (
            arabic_transliterate(mode, iso2332_string, ignore, reverse)
            == "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ"
        )

    def test_middle_high_german_transcriber(self):
        """
        Test MHG IPA transcriber
        """
        inputs = "Slâfest du friedel ziere?"
        transcriber = mhgt.Transcriber().transcribe
        transcription = [unicodedata.normalize("NFC", x) for x in transcriber(inputs)]
        target = [
            unicodedata.normalize("NFC", x)
            for x in "[Slɑːfest d̥ʊ frɪ͡əd̥el t͡sɪ͡əre?]"
        ]
        self.assertEqual(target, transcription)

    def test_middle_high_german_soundex(self):
        """
        Test MHG Soundex Phonetic Index
        """
        w1 = mhgs.Word("krêatiure").phonetic_indexing(p="SE")
        w2 = mhgs.Word("kreatur").phonetic_indexing(p="SE")
        target = ["K535", "K535"]

        self.assertEqual([w1, w2], target)

    def test_middle_high_german_ascii_encoding(self):
        """
        Test MHG ASCII encoder
        """
        s1 = normalize_middle_high_german("vogellîn", ascii=True)
        s2 = normalize_middle_high_german("vogellīn", ascii=True)
        target = ["vogellin", "vogellin"]

        self.assertEqual([s1, s2], target)

    def test_middle_english_syllabify(self):
        """Test syllabification for middle english"""

        words = ["marchall", "content", "thyne", "greef", "commaundyd"]
        syllabifier = Syllabifier(language="enm")
        syllabified = [syllabifier.syllabify(w, mode="MOP") for w in words]
        target_syllabified = [
            ["mar", "chall"],
            ["con", "tent"],
            ["thyne"],
            ["greef"],
            ["com", "mau", "ndyd"],
        ]

        self.assertListEqual(syllabified, target_syllabified)

        syllabifier = Syllabifier(language="enm", sep=".")
        syllabified_str = [syllabifier.syllabify(w, "MOP") for w in words]
        target_syllabified_str = [
            "mar.chall",
            "con.tent",
            "thyne",
            "greef",
            "com.mau.ndyd",
        ]

        self.assertListEqual(syllabified_str, target_syllabified_str)

    def test_old_norse_transcriber(self):
        example_sentence = (
            "Almáttigr guð skapaði í upphafi himin ok jörð ok alla þá hluti, er þeim fylgja, og "
            "síðast menn tvá, er ættir eru frá komnar, Adam ok Evu, ok fjölgaðist þeira kynslóð ok "
            "dreifðist um heim allan."
        )

        tr = ut.Transcriber(
            ont.DIPHTHONGS_IPA,
            ont.DIPHTHONGS_IPA_class,
            ont.IPA_class,
            ont.old_norse_rules,
        )
        transcribed_sentence = tr.text_to_phonetic_representation(
            example_sentence, with_squared_brackets=True
        )
        target = (
            "[almaːtːiɣr guð skapaði iː upːhavi himin ɔk jœrð ɔk alːa θaː hluti ɛr θɛim fylɣja ɔɣ siːðast mɛnː "
            "tvaː ɛr ɛːtːir ɛru fraː kɔmnar adam ɔk ɛvu ɔk fjœlɣaðist θɛira kynsloːð ɔk drɛivðist um hɛim alːan]"
        )
        self.assertEqual(target, transcribed_sentence)

    def test_gothic_transcriber(self):
        example_sentence = "Anastodeins aiwaggeljons Iesuis Xristaus sunaus gudis."

        tr = ut.Transcriber(
            gothic.DIPHTHONGS_IPA,
            gothic.DIPHTHONGS_IPA_class,
            gothic.IPA_class,
            gothic.gothic_rules,
        )
        transcribed_sentence = tr.text_to_phonetic_representation(
            example_sentence, with_squared_brackets=True
        )
        target = "[anastoːðiːns ɛwaŋgeːljoːns jeːsuis kristɔs sunɔs guðis]"
        self.assertEqual(target, transcribed_sentence)

    def test_old_swedish(self):
        sentence = "Far man kunu oc dör han för en hun far barn. oc sigher hun oc hænnæ frændær."
        tr = ut.Transcriber(
            old_swedish.DIPHTHONGS_IPA,
            old_swedish.DIPHTHONGS_IPA_class,
            old_swedish.IPA_class,
            old_swedish.old_swedish_rules,
        )
        transcribed_sentence = tr.text_to_phonetic_representation(
            sentence, with_squared_brackets=True
        )
        self.assertEqual(
            "[far man kunu ok dør han før ɛn hun far barn ok siɣɛr hun ok hɛnːɛ frɛndɛr]",
            transcribed_sentence,
        )
        pass

    def test_utils(self):
        # definition of a Vowel
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        self.assertListEqual(
            [a.ipar, a.backness, a.height, a.length, a.rounded],
            ["a", ut.Backness.front, ut.Height.open, ut.Length.short, False],
        )

    def test_vowel_lengthening_utils(self):
        # how lengthen works
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        aa = a.lengthen()
        self.assertEqual(aa.ipar, "aː")

    def test_consonant_utils(self):
        # example of a Consonant
        b = ut.Consonant(ut.Place.bilabial, ut.Manner.stop, True, "b", False)
        self.assertListEqual(
            [b.ipar, b.manner, b.place, b.voiced, b.geminate],
            ["b", ut.Manner.stop, ut.Place.bilabial, True, False],
        )

    def test_add_consonants_utils(self):
        # This is how Consonant instances can be added to each other
        k = ut.Consonant(ut.Place.velar, ut.Manner.stop, False, "k", False)
        s = ut.Consonant(ut.Place.alveolar, ut.Manner.fricative, False, "s", False)
        x = k + s
        self.assertEqual(x.ipar, "ks")

    def test_rule1_utils(self):
        # examples of Rule instances
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)
        rule = ut.Rule(
            ut.AbstractPosition(
                ut.Rank.inner, [ut.AbstractVowel()], [ut.AbstractVowel()]
            ),
            th,
            dh,
        )
        pos = ut.Position(ut.Rank.inner, a, a)
        self.assertEqual(rule.can_apply(pos), True)

    def test_rule2_utils(self):
        k = ut.Consonant(ut.Place.velar, ut.Manner.stop, False, "k", False)
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)
        rule = ut.Rule(
            ut.AbstractPosition(
                ut.Rank.inner, [ut.AbstractVowel()], [ut.AbstractVowel()]
            ),
            th,
            dh,
        )
        pos = ut.Position(ut.Rank.inner, k, a)
        self.assertEqual(rule.can_apply(pos), False)

    def test_rule3_utils(self):
        s = ut.Consonant(ut.Place.alveolar, ut.Manner.fricative, False, "s", False)
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)
        rule = ut.Rule(
            ut.AbstractPosition(
                ut.Rank.inner, [ut.AbstractVowel()], [ut.AbstractVowel()]
            ),
            th,
            dh,
        )
        pos = ut.Position(ut.Rank.inner, a, s)
        self.assertEqual(rule.can_apply(pos), False)

    def test_rule4_utils(self):
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)
        rule = ut.Rule(
            ut.AbstractPosition(
                ut.Rank.inner,
                [ut.AbstractConsonant(voiced=True)],
                [ut.AbstractConsonant(voiced=True)],
            ),
            th,
            dh,
        )
        pos = ut.Position(ut.Rank.inner, a, a)
        self.assertEqual(rule.can_apply(pos), False)

    def test_rule5_utils(self):
        k = ut.Consonant(ut.Place.velar, ut.Manner.stop, False, "k", False)
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)
        rule = ut.Rule(
            ut.AbstractPosition(
                ut.Rank.inner,
                [ut.AbstractConsonant(voiced=True)],
                [ut.AbstractConsonant(voiced=True)],
            ),
            th,
            dh,
        )
        pos = ut.Position(ut.Rank.inner, k, a)
        self.assertEqual(rule.can_apply(pos), False)

    def test_rule6_utils(self):
        s = ut.Consonant(ut.Place.alveolar, ut.Manner.fricative, False, "s", False)
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)
        pos = ut.Position(ut.Rank.inner, a, s)
        rule = ut.Rule(
            ut.AbstractPosition(
                ut.Rank.inner,
                [ut.AbstractConsonant(voiced=True)],
                [ut.AbstractConsonant(voiced=True)],
            ),
            th,
            dh,
        )
        self.assertEqual(rule.can_apply(pos), False)

    def test_rule7_utils(self):
        b = ut.Consonant(ut.Place.bilabial, ut.Manner.stop, True, "b", False)
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)
        rule = ut.Rule(
            ut.AbstractPosition(
                ut.Rank.inner,
                [ut.AbstractConsonant(voiced=True)],
                [ut.AbstractConsonant(voiced=True)],
            ),
            th,
            dh,
        )
        pos = ut.Position(ut.Rank.inner, b, b)
        self.assertEqual(rule.can_apply(pos), True)

    def test_rule_conversion1(self):
        # Definition of real Vowel and Consonant instances
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        e = ut.Vowel(
            ut.Height.close_mid, ut.Backness.front, False, ut.Length.short, "e"
        )
        i = ut.Vowel(ut.Height.close, ut.Backness.front, False, ut.Length.short, "i")
        o = ut.Vowel(ut.Height.close_mid, ut.Backness.back, True, ut.Length.short, "o")
        u = ut.Vowel(ut.Height.close, ut.Backness.back, True, ut.Length.short, "u")

        b = ut.Consonant(ut.Place.bilabial, ut.Manner.stop, True, "b", False)
        d = ut.Consonant(ut.Place.alveolar, ut.Manner.stop, True, "d", False)
        f = ut.Consonant(ut.Place.labio_dental, ut.Manner.fricative, False, "f", False)
        g = ut.Consonant(ut.Place.velar, ut.Manner.stop, True, "g", False)
        k = ut.Consonant(ut.Place.velar, ut.Manner.stop, False, "k", False)
        p = ut.Consonant(ut.Place.bilabial, ut.Manner.stop, False, "p", False)
        s = ut.Consonant(ut.Place.alveolar, ut.Manner.fricative, False, "s", False)
        t = ut.Consonant(ut.Place.alveolar, ut.Manner.stop, False, "t", False)
        v = ut.Consonant(ut.Place.labio_dental, ut.Manner.fricative, True, "v", False)
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)

        # examples of phonology and ipa_class
        phonology = [a, e, i, o, u, b, d, f, g, k, p, s, t, v, th, dh]

        # examples of ipa_to_regular_expression and from_regular_expression methods
        ru1 = ut.Rule(
            ut.AbstractPosition(
                ut.Rank.inner,
                [ut.AbstractConsonant(voiced=False)],
                [ut.AbstractConsonant(voiced=True)],
            ),
            th,
            th,
        )
        self.assertEqual(
            ru1.ipa_to_regular_expression(phonology), "(?<=[fkpstθ])θ(?=[bdgvð])"
        )

    def test_rule_conversion2(self):
        # Definition of real Vowel and Consonant instances
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        e = ut.Vowel(
            ut.Height.close_mid, ut.Backness.front, False, ut.Length.short, "e"
        )
        i = ut.Vowel(ut.Height.close, ut.Backness.front, False, ut.Length.short, "i")
        o = ut.Vowel(ut.Height.close_mid, ut.Backness.back, True, ut.Length.short, "o")
        u = ut.Vowel(ut.Height.close, ut.Backness.back, True, ut.Length.short, "u")

        b = ut.Consonant(ut.Place.bilabial, ut.Manner.stop, True, "b", False)
        d = ut.Consonant(ut.Place.alveolar, ut.Manner.stop, True, "d", False)
        f = ut.Consonant(ut.Place.labio_dental, ut.Manner.fricative, False, "f", False)
        g = ut.Consonant(ut.Place.velar, ut.Manner.stop, True, "g", False)
        k = ut.Consonant(ut.Place.velar, ut.Manner.stop, False, "k", False)
        p = ut.Consonant(ut.Place.bilabial, ut.Manner.stop, False, "p", False)
        s = ut.Consonant(ut.Place.alveolar, ut.Manner.fricative, False, "s", False)
        t = ut.Consonant(ut.Place.alveolar, ut.Manner.stop, False, "t", False)
        v = ut.Consonant(ut.Place.labio_dental, ut.Manner.fricative, True, "v", False)
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)

        # examples of phonology and ipa_class
        phonology = [a, e, i, o, u, b, d, f, g, k, p, s, t, v, th, dh]
        ru2 = ut.Rule(
            ut.AbstractPosition(
                ut.Rank.first, None, [ut.AbstractConsonant(place=ut.Place.velar)]
            ),
            p,
            k,
        )
        self.assertEqual(ru2.ipa_to_regular_expression(phonology), "^p(?=[gk])")

    def test_rule_conversion3(self):
        # Definition of real Vowel and Consonant instances
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        e = ut.Vowel(
            ut.Height.close_mid, ut.Backness.front, False, ut.Length.short, "e"
        )
        i = ut.Vowel(ut.Height.close, ut.Backness.front, False, ut.Length.short, "i")
        o = ut.Vowel(ut.Height.close_mid, ut.Backness.back, True, ut.Length.short, "o")
        u = ut.Vowel(ut.Height.close, ut.Backness.back, True, ut.Length.short, "u")

        b = ut.Consonant(ut.Place.bilabial, ut.Manner.stop, True, "b", False)
        d = ut.Consonant(ut.Place.alveolar, ut.Manner.stop, True, "d", False)
        f = ut.Consonant(ut.Place.labio_dental, ut.Manner.fricative, False, "f", False)
        g = ut.Consonant(ut.Place.velar, ut.Manner.stop, True, "g", False)
        k = ut.Consonant(ut.Place.velar, ut.Manner.stop, False, "k", False)
        p = ut.Consonant(ut.Place.bilabial, ut.Manner.stop, False, "p", False)
        s = ut.Consonant(ut.Place.alveolar, ut.Manner.fricative, False, "s", False)
        t = ut.Consonant(ut.Place.alveolar, ut.Manner.stop, False, "t", False)
        v = ut.Consonant(ut.Place.labio_dental, ut.Manner.fricative, True, "v", False)
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)

        # examples of phonology and ipa_class
        phonology = [a, e, i, o, u, b, d, f, g, k, p, s, t, v, th, dh]

        ru3 = ut.Rule(
            ut.AbstractPosition(
                ut.Rank.last, [ut.AbstractConsonant(manner=ut.Manner.stop)], None
            ),
            dh,
            th,
        )
        self.assertEqual(ru3.ipa_to_regular_expression(phonology), "(?<=[bdgkpt])ð$")

    def test_rule_conversion4(self):
        # Definition of real Vowel and Consonant instances
        a = ut.Vowel(ut.Height.open, ut.Backness.front, False, ut.Length.short, "a")
        e = ut.Vowel(
            ut.Height.close_mid, ut.Backness.front, False, ut.Length.short, "e"
        )
        i = ut.Vowel(ut.Height.close, ut.Backness.front, False, ut.Length.short, "i")
        o = ut.Vowel(ut.Height.close_mid, ut.Backness.back, True, ut.Length.short, "o")
        u = ut.Vowel(ut.Height.close, ut.Backness.back, True, ut.Length.short, "u")

        b = ut.Consonant(ut.Place.bilabial, ut.Manner.stop, True, "b", False)
        d = ut.Consonant(ut.Place.alveolar, ut.Manner.stop, True, "d", False)
        f = ut.Consonant(ut.Place.labio_dental, ut.Manner.fricative, False, "f", False)
        g = ut.Consonant(ut.Place.velar, ut.Manner.stop, True, "g", False)
        k = ut.Consonant(ut.Place.velar, ut.Manner.stop, False, "k", False)
        p = ut.Consonant(ut.Place.bilabial, ut.Manner.stop, False, "p", False)
        s = ut.Consonant(ut.Place.alveolar, ut.Manner.fricative, False, "s", False)
        t = ut.Consonant(ut.Place.alveolar, ut.Manner.stop, False, "t", False)
        v = ut.Consonant(ut.Place.labio_dental, ut.Manner.fricative, True, "v", False)
        th = ut.Consonant(ut.Place.dental, ut.Manner.fricative, False, "θ", False)
        dh = ut.Consonant(ut.Place.dental, ut.Manner.fricative, True, "ð", False)

        # examples of phonology and ipa_class
        phonology = [a, e, i, o, u, b, d, f, g, k, p, s, t, v, th, dh]

        ipa_class = {
            "a": a,
            "e": e,
            "i": i,
            "o": o,
            "u": u,
            "b": b,
            "d": d,
            "f": f,
            "g": g,
            "k": k,
            "p": p,
            "s": s,
            "t": t,
            "v": v,
            "þ": th,
            "ð": dh,
        }
        # from regular expression to Rule
        example = r"(?<=[aeiou])f(?=[aeiou])"
        ru4 = ut.Rule.from_regular_expression(example, "v", ipa_class)
        self.assertEqual(ru4.ipa_to_regular_expression(phonology), example)

    def test_syllabification_old_norse(self):
        old_norse_syllabifier = Syllabifier(language="non", break_geminants=True)
        text = (
            "Gefjun dró frá Gylfa glöð djúpröðul óðla, svá at af rennirauknum rauk, Danmarkar auka. Báru öxn ok "
            "átta ennitungl, þars gengu fyrir vineyjar víðri valrauf, fjögur höfuð."
        )
        tokenizer = OldNorseWordTokenizer()
        words = tokenizer.tokenize(text)
        old_norse_syllabifier.set_invalid_onsets(invalid_onsets)

        syllabified_words = [
            old_norse_syllabifier.syllabify_ssp(word.lower())
            for word in words
            if word not in ",."
        ]

        target = [
            ["gef", "jun"],
            ["dró"],
            ["frá"],
            ["gyl", "fa"],
            ["glöð"],
            ["djúp", "rö", "ðul"],
            ["óðl", "a"],
            ["svá"],
            ["at"],
            ["af"],
            ["ren", "ni", "rauk", "num"],
            ["rauk"],
            ["dan", "mar", "kar"],
            ["auk", "a"],
            ["bár", "u"],
            ["öxn"],
            ["ok"],
            ["át", "ta"],
            ["en", "ni", "tungl"],
            ["þars"],
            ["geng", "u"],
            ["fy", "rir"],
            ["vi", "ney", "jar"],
            ["víðr", "i"],
            ["val", "rauf"],
            ["fjö", "gur"],
            ["hö", "fuð"],
        ]
        self.assertListEqual(syllabified_words, target)

    def test_syllabify_phonemes(self):
        vowels = ["a", "ɛ", "i", "ɔ", "ɒ", "ø", "u", "y", "œ", "e", "o", "j"]
        ipa_hierarchy = [
            vowels,
            ["r"],
            ["l"],
            ["m", "n"],
            ["f", "v", "θ", "ð", "s", "h"],
            ["b", "d", "g", "k", "p", "t"],
        ]
        syllabifier = Syllabifier()
        syllabifier.set_hierarchy(ipa_hierarchy)
        syllabifier.set_vowels(vowels)
        word = [ont.a, ont.s, ont.g, ont.a, ont.r, ont.dh, ont.r]
        syllabified_word = syllabifier.syllabify_phonemes(word)
        self.assertListEqual(
            syllabified_word, [[ont.a, ont.s], [ont.g, ont.a, ont.r, ont.dh, ont.r]]
        )

    def test_syllable1(self):
        sylla1 = Syllable("armr", ["a"], ["r", "m"])
        self.assertListEqual(sylla1.nucleus, ["a"])
        self.assertLessEqual(sylla1.onset, [])
        self.assertLessEqual(sylla1.coda, ["r", "m", "r"])

    def test_syllable2(self):
        sylla2 = Syllable("gangr", ["a"], ["g", "n", "r"])
        self.assertLessEqual(sylla2.onset, ["g"])
        self.assertLessEqual(sylla2.nucleus, ["a"])
        self.assertLessEqual(sylla2.coda, ["n", "g", "r"])

    def test_syllable3(self):
        self.assertRaises(ValueError, Syllable, "r", [], ["r"])

    def test_syllable4(self):
        self.assertRaises(ValueError, Syllable, "", [], [])

    def test_syllable5(self):
        self.assertRaises(ValueError, Syllable, "e", ["a"], ["r"])

    def test_syllable6(self):
        self.assertRaises(ValueError, Syllable, "armar", ["a"], ["r", "m"])


if __name__ == "__main__":
    unittest.main()
