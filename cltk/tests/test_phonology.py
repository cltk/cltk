"""Test cltk.phonology."""

__author__ = ['Jack Duff <jmunroeduff@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import unicodedata
from cltk.phonology.arabic.romanization import transliterate as AarabicTransliterate
from cltk.phonology.greek import transcription as grc
from cltk.phonology.latin import transcription as lat
from cltk.phonology.akkadian import stress as AkkadianStress
import unittest

class TestSequenceFunctions(unittest.TestCase):
    """Class for unittest"""

    """greek.transcription"""
    def test_greek_refresh(self):
        """Test the Word class's `_refresh` method in Greek."""
        test_word = grc.Word("pʰór.miŋks", grc.GREEK["Attic"]["Probert"])
        test_word._refresh()
        contexts = [test_word.phones[0].left.ipa, 
            test_word.phones[1].left.ipa, test_word.phones[1].right.ipa,
            test_word.phones[-1].right.ipa]
        target = [grc.Phone("#").ipa, grc.Phone("pʰ").ipa, 
            grc.Phone("r").ipa, grc.Phone("#").ipa]
        self.assertEqual(contexts, target)

    def test_greek_r_devoice(self):
        """Test the Word class's method `_r_devoice` in Greek."""
        condition_1 = grc.Word("rɑ́ks", grc.GREEK["Attic"]["Probert"])
        condition_1._refresh()
        condition_1._r_devoice()
        condition_2 = grc.Word("syrrɑ́ptɔː", grc.GREEK["Attic"]["Probert"])
        condition_2._refresh()
        condition_2._r_devoice()
        outputs = [''.join(p.ipa for p in condition_1.phones), 
                    ''.join(p.ipa for p in condition_2.phones)]
        target = [unicodedata.normalize('NFC', y) for y in
                    ["r̥ɑ́ks", "syrr̥ɑ́ptɔː"]]
        self.assertEqual(outputs, target)

    def test_greek_s_voice_assimilation(self):
        """Test the Word class's method `_s_voice_assimilation` in Greek."""
        condition = grc.Word("ẹːrgɑsménon", grc.GREEK["Attic"]["Probert"])
        condition._refresh()
        condition._s_voice_assimilation()
        output = ''.join([p.ipa for p in condition.phones])
        target = unicodedata.normalize('NFC', "ẹːrgɑzménon")
        self.assertEqual(output, target)

    def test_greek_nasal_place_assimilation(self):
        """Test the Word method `_nasal_place_assimilation` in Greek."""
        condition_1 = grc.Word("pʰórmigks", grc.GREEK["Attic"]["Probert"])
        condition_1._refresh()
        condition_1._nasal_place_assimilation()
        condition_2 = grc.Word("ɑ́ggelos", grc.GREEK["Attic"]["Probert"])
        condition_2._refresh()
        condition_2._nasal_place_assimilation()
        outputs = [''.join([p.ipa for p in condition_1.phones]), 
                    ''.join([p.ipa for p in condition_2.phones])]
        target = [unicodedata.normalize('NFC', y) for y in 
                    ["pʰórmiŋks", "ɑ́ŋgelos"]]
        self.assertEqual(outputs, target)

    def test_greek_g_nasality_assimilation(self):
        """Test the Word class's `_g_nasality_assimilation` in Greek."""
        condition = grc.Word("gignɔ́ːskɔː", grc.GREEK["Attic"]["Probert"])
        condition._refresh()
        condition._g_nasality_assimilation()
        output = ''.join([p.ipa for p in condition.phones])
        target = unicodedata.normalize('NFC', "giŋnɔ́ːskɔː")
        self.assertEqual(output, target)

    def test_greek_alternate(self):
        """Test the Word class's `_alternate` in Greek."""
        raw_inputs = ["rɑ́ks", "syrrɑ́ptɔː", "ẹːrgɑsménon", 
                        "pʰórmigks", "ɑ́ggelos", "gignɔ́ːskɔː"]
        outputs = []
        for i in raw_inputs:
            w = grc.Word(i, grc.GREEK["Attic"]["Probert"])
            w._alternate()
            outputs.append(''.join([p.ipa for p in w.phones]))
        target = [unicodedata.normalize('NFC', y) for y in ["r̥ɑ́ks", 
                    "syrr̥ɑ́ptɔː", "ẹːrgɑzménon", 
                    "pʰórmiŋks", "ɑ́ŋgelos", "giŋnɔ́ːskɔː"]]
        self.assertEqual(outputs, target)

    def test_greek_syllabify(self):
        """Test the Word class's `_syllabify` in Greek."""
        raw_inputs = ["lẹ́ːpẹː", "píptɔː", "téknọː", "skɛ̂ːptron"]
        outputs = []
        for i in raw_inputs:
            w = grc.Word(i, grc.GREEK["Attic"]["Probert"])
            w._alternate()
            outputs.append([''.join([p.ipa for l in n for p in l]) 
                for n in w._syllabify()])
        target = [[unicodedata.normalize('NFC', s) for s in y] for y in 
            [["lẹ́ː", "pẹː"], ["píp", "tɔː"], 
            ["té", "knọː"], ["skɛ̂ːp", "tron"]]]
        self.assertEqual(outputs, target)

    def test_greek_print_ipa(self):
        """Test the Word class's `_print_ipa` in Greek."""
        w = grc.Word("élipe", grc.GREEK["Attic"]["Probert"])
        output = [w._print_ipa(True), w._print_ipa(False)]
        target = [unicodedata.normalize('NFC', "é.li.pe"),
                    unicodedata.normalize('NFC', "élipe")]
        self.assertEqual(output, target)

    def test_greek_parse_diacritics(self):
        """Test the Transcriber class's `_parse_diacritics` in Greek."""
        inputs = ["ἄ", "Φ", "ῷ", "ὑ", "ϊ", "ῑ"]
        transcriber = grc.Transcriber("Attic", "Probert")
        outputs = [transcriber._parse_diacritics(char) for char in inputs]
        target = [unicodedata.normalize('NFC', c) for c in 
            ["α/" + grc.chars.ACUTE + "//", 
            "φ///", "ω/" + grc.chars.CIRCUMFLEX + "/" 
            + grc.chars.IOTA_SUBSCRIPT + "/", "h///υ///", 
            "ι//" + grc.chars.DIAERESIS + "/", "ι//" + grc.chars.LONG + "/"]]
        self.assertEqual(outputs, target)

    def test_greek_prep_text(self):
        """Test the Transcriber class's `_prep_text` in Greek."""
        inputs = ["λείπειν", "ὕπνῳ"]
        transcriber = grc.Transcriber("Attic", "Probert")
        outputs = [transcriber._prep_text(w) for w in inputs]
        target = [[('λ', '', ''), ('ει', '́', ''), ('π', '', ''), 
                        ('ει', '', ''), ('ν', '', '')], 
                    [('h', '', ''), ('υ', '́', ''), ('π', '', ''), 
                        ('ν', '', ''), ('ωι', '', '̄')]]
        self.assertEqual(outputs, target)

    def test_transcriber_probert(self):
        """Test Attic Greek IPA transcription via Probert reconstruction."""
        transcriber = grc.Transcriber("Attic", "Probert").transcribe
        transcription = [transcriber(x) for x in 
            [unicodedata.normalize('NFC', y) for y in 
            ["ῥάξ", "εἰργασμένον", "φόρμιγξ", "γιγνώσκω"]]]
        target = [unicodedata.normalize('NFC', y) for y in 
            ["[r̥ɑ́ks]", "[ẹːr.gɑz.mé.non]", "[pʰór.miŋks]", "[giŋ.nɔ́ːs.kɔː]"]]
        self.assertEqual(transcription, target)


    """latin.transcription"""
    def test_latin_refresh(self):
        """Test the Word class's `_refresh` method in Latin."""
        test_word = lat.Word("ɔmn̪ɪs", lat.LATIN["Classical"]["Allen"])
        test_word._refresh()
        contexts = [test_word.phones[0].left.ipa, 
            test_word.phones[1].left.ipa, test_word.phones[1].right.ipa,
            test_word.phones[-1].right.ipa]
        target = [grc.Phone("#").ipa, grc.Phone("ɔ").ipa, 
            grc.Phone("n̪").ipa, grc.Phone("#").ipa]
        self.assertEqual(contexts, target)

    def test_latin_j_maker(self):
        """Test the Word class's method `_j_maker` in Latin."""
        condition = lat.Word("t̪roːɪaj", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._j_maker()
        output = ''.join([p.ipa for p in condition.phones])
        target = unicodedata.normalize('NFC', "t̪roːjaj")
        self.assertEqual(output, target)

    def test_latin_w_maker(self):
        """Test the Word class's method `_w_maker` in Latin."""
        condition = lat.Word("ʊɪrʊmkʷɛ", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._w_maker()
        output = ''.join([p.ipa for p in condition.phones])
        target = unicodedata.normalize('NFC', "wɪrʊmkʷɛ")
        self.assertEqual(output, target)

    def test_latin_wj_block(self):
        """Test the Word class's method `_wj_maker` in Latin."""
        condition = lat.Word("wjrʊmkʷɛ", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._wj_block()
        output = ''.join([p.ipa for p in condition.phones])
        target = unicodedata.normalize('NFC', "wɪrʊmkʷɛ")
        self.assertEqual(output, target)

    def test_latin_uj_diph_maker(self):
        """Test the Word class's method `_uj_diph_maker` in Latin."""
        condition = lat.Word("kʊɪ", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._uj_diph_maker()
        output = ''.join([p.ipa for p in condition.phones])
        target = unicodedata.normalize('NFC', "kuj")
        self.assertEqual(output, target)

    def test_latin_b_devoice(self):
        """Test the Word class's method `_b_devoice` in Latin."""
        condition_1 = lat.Word("abs", lat.LATIN["Classical"]["Allen"])
        condition_1._refresh()
        condition_1._b_devoice()
        condition_2 = lat.Word("sʊbt̪ʊs", lat.LATIN["Classical"]["Allen"])
        condition_2._refresh()
        condition_2._b_devoice()
        outputs = [''.join([p.ipa for p in condition_1.phones]), 
                    ''.join([p.ipa for p in condition_2.phones])]
        target = [unicodedata.normalize('NFC', y) for y in 
                    ["aps", "sʊpt̪ʊs"]]
        self.assertEqual(outputs, target)

    def test_latin_final_m_drop(self):
        """Test the Word class's method `_final_m_drop` in Latin."""
        condition = lat.Word("kʷaːrum", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._final_m_drop()
        output = ''.join([p.ipa for p in condition.phones])
        target = unicodedata.normalize('NFC', "kʷaːrũː")
        self.assertEqual(output, target)

    def test_latin_n_place_assimilation(self):
        """Test the Word class's method `_n_place_assimilation` in Latin."""
        condition = lat.Word("lɪn̪gʷa", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._n_place_assimilation()
        output = ''.join([p.ipa for p in condition.phones])
        target = unicodedata.normalize('NFC', "lɪŋgʷa")
        self.assertEqual(output, target)

    def test_latin_g_n_nasality_assimilation(self):
        """Test the Word class's `_g_n_nasality_assimilation` in Latin."""
        condition = lat.Word("magn̪ʊs", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._g_n_nasality_assimilation()
        output = ''.join([p.ipa for p in condition.phones])
        target = unicodedata.normalize('NFC', "maŋn̪ʊs")
        self.assertEqual(output, target)

    def test_latin_ns_nf_lengthening(self):
        """Test the Word class's method `_ns_nf_lengthening` in Latin."""
        condition_1 = lat.Word("kɔn̪sɔl", lat.LATIN["Classical"]["Allen"])
        condition_1._refresh()
        condition_1._ns_nf_lengthening()
        condition_2 = lat.Word("kɔn̪fɛkiː", lat.LATIN["Classical"]["Allen"])
        condition_2._refresh()
        condition_2._ns_nf_lengthening()
        outputs = [''.join([p.ipa for p in condition_1.phones]), 
                    ''.join([p.ipa for p in condition_2.phones])]
        target = [unicodedata.normalize('NFC', y) for y in 
                    ["kɔːn̪sɔl", "kɔːn̪fɛkiː"]]
        self.assertEqual(outputs, target)

    def test_latin_l_darken(self):
        """Test the Word class's method `_l_darken` in Latin."""
        condition_1 = lat.Word("bɛlgaj", lat.LATIN["Classical"]["Allen"])
        condition_1._refresh()
        condition_1._l_darken()
        condition_2 = lat.Word("kɔːn̪sɔl", lat.LATIN["Classical"]["Allen"])
        condition_2._refresh()
        condition_2._l_darken()
        outputs = [''.join([p.ipa for p in condition_1.phones]), 
                    ''.join([p.ipa for p in condition_2.phones])]
        target = [unicodedata.normalize('NFC', y) for y in 
                    ["bɛɫgaj", "kɔːn̪sɔɫ"]]
        self.assertEqual(outputs, target)

    def test_latin_j_z_doubling(self):
        """Test the Word class's method `_j_z_doubling` in Latin."""
        condition_1 = lat.Word("t̪roːjaj", lat.LATIN["Classical"]["Allen"])
        condition_1._refresh()
        condition_1._j_z_doubling()
        condition_2 = lat.Word("amaːzɔn", lat.LATIN["Classical"]["Allen"])
        condition_2._refresh()
        condition_2._j_z_doubling()
        outputs = [''.join([p.ipa for p in condition_1.phones]), 
                    ''.join([p.ipa for p in condition_2.phones])]
        target = [unicodedata.normalize('NFC', y) for y in 
                    ["t̪roːjjaj", "amaːzzɔn"]]
        self.assertEqual(outputs, target)

    def test_latin_long_vowel_catcher(self):
        """Test the Word class's method `_long_vowel_catcher` in Latin."""
        conditions = [lat.Word(s, lat.LATIN["Classical"]["Allen"]) for s in
                        ["ɪː", 'ʊː', 'ɛː', 'ɪ̃ː', 'ʊ̃ː', 'ɛ̃ː']]
        for w in conditions:
            w._long_vowel_catcher()
        outputs = [''.join([p.ipa for p in c.phones]) for c in conditions]
        target = [unicodedata.normalize('NFC', y) for y in 
                    ["iː", 'uː', 'eː', 'ĩː', 'ũː', 'ẽː']]
        self.assertEqual(outputs, target)

    def test_latin_e_i_closer_before_vowel(self):
        """Test the Word class's `_e_i_closer_before_vowel` in Latin."""
        condition_1 = lat.Word("gaɫlɪa", lat.LATIN["Classical"]["Allen"])
        condition_1._refresh()
        condition_1._e_i_closer_before_vowel()
        condition_2 = lat.Word("mɛa", lat.LATIN["Classical"]["Allen"])
        condition_2._refresh()
        condition_2._e_i_closer_before_vowel()
        outputs = [''.join([p.ipa for p in condition_1.phones]), 
                    ''.join([p.ipa for p in condition_2.phones])]
        target = [unicodedata.normalize('NFC', y) for y in 
                    ["gaɫlɪ̣a", "mɛ̣a"]]
        self.assertEqual(outputs, target)

    def test_latin_intervocalic_j(self):
        """Test the Word class's method `_intervocalic_j` in Latin."""
        condition = lat.Word("gaɫlɪ̣a", lat.LATIN["Classical"]["Allen"])
        condition._refresh()
        condition._intervocalic_j()
        outputs = ''.join([p.ipa for p in condition.phones])
        target = unicodedata.normalize('NFC', "gaɫlɪ̣ja")
        self.assertEqual(outputs, target)

    def test_latin_alternate(self):
        """Test the Word class's method `_alternate` in Latin."""
        raw_inputs = ["gallɪa", "d̪iːʊiːsa", "kʷaːrʊm"]
        outputs = []
        for i in raw_inputs:
            w = lat.Word(i, lat.LATIN["Classical"]["Allen"])
            w._alternate()
            outputs.append(''.join([p.ipa for p in w.phones]))
        target = [unicodedata.normalize('NFC', y) for y in 
                    ["gaɫlɪ̣ja", "d̪iːwiːsa", "kʷaːrũː"]]
        self.assertEqual(outputs, target)

    def test_latin_syllabify(self):
        """Test the Word class's `_syllabify` in Latin."""
        raw_inputs = ["arma", "kan̪oː", "t̪roːjjaj", "gaɫlɪ̣ja"]
        outputs = []
        for i in raw_inputs:
            w = lat.Word(i, lat.LATIN["Classical"]["Allen"])
            w._syllabify()
            outputs.append([''.join([p.ipa for l in n for p in l]) 
                for n in w._syllabify()])
        target = [[unicodedata.normalize('NFC', s) for s in y] for y in 
            [["ar", "ma"], ["ka", "n̪oː"], 
            ["t̪roːj", "jaj"], ["gaɫ", "lɪ̣", "ja"]]]
        self.assertEqual(outputs, target)

    def test_latin_print_ipa(self):
        """Test the Word class's method `_print_ipa` in Latin."""
        inputs = [lat.Word(w, lat.LATIN["Classical"]["Allen"]) for w in 
                    ["gaɫlɪ̣ja", "d̪iːwiːsa"]]
        output = [[w._print_ipa(syllabify=False, accentuate=False),
                    w._print_ipa(syllabify=True, accentuate=False), 
                    w._print_ipa(syllabify=True, accentuate=True)]
                     for w in inputs]
        target = [[unicodedata.normalize('NFC', x) for x in 
                        ["gaɫlɪ̣ja", "gaɫ.lɪ̣.ja", "'gaɫ.lɪ̣.ja"]],
                    [unicodedata.normalize('NFC', x) for x in 
                        ["d̪iːwiːsa", "d̪iː.wiː.sa", "d̪iː.'wiː.sa"]]]
        self.assertEqual(output, target)

    def test_latin_parse_diacritics(self):
        """Test the Transcriber class's `_parse_diacritics` in Latin."""
        inputs = ["a", "ū", "ï"]
        transcriber = lat.Transcriber("Classical", "Allen")
        outputs = [transcriber._parse_diacritics(char) for char in inputs]
        target = [unicodedata.normalize('NFC', c) for c in 
            ["a///", "u/" + lat.chars.LONG + "//", 
                "i//" + lat.chars.DIAERESIS + "/"]]
        self.assertEqual(outputs, target)

    def test_latin_prep_text(self):
        """Test the Transcriber class's `_prep_text` in Latin."""
        inputs = ["ūnam", "qui", "Belgae"]
        transcriber = lat.Transcriber("Classical", "Allen")
        outputs = [transcriber._prep_text(w) for w in inputs]
        target = [[('u', '̄', ''), ('n', '', ''), ('a', '', ''), 
                        ('m', '', '')], 
                    [('qu', '', ''), ('i', '', '')],
                    [('b', '', ''), ('e', '', ''), ('l', '', ''),
                    ('g', '', ''), ("ae", '', '')]]
        self.assertEqual(outputs, target)

    def test_transcriber_allen_without_macronizer(self):
        """Test Classical Latin IPA transcription via Allen reconstruction,\ 
         input pre-macronized."""
        transcriber = lat.Transcriber("Classical", "Allen").transcribe
        transcription = [transcriber(x, macronize=False) for x in 
            [unicodedata.normalize('NFC', y) for y in 
            ["Trōiae", "Gallia", "dīuīsa", "ūnam", "incolunt", "Belgae"]]]
        target = [unicodedata.normalize('NFC', y) for y in 
            ["['t̪roːj.jaj]", "['gaɫ.lɪ̣.ja]", "[d̪iː.'wiː.sa]", 
            "['uː.n̪ãː]", "['ɪŋ.kɔ.lʊn̪t̪]", "['bɛɫ.gaj]"]]
        self.assertEqual(transcription, target)

    def test_transcriber_allen_with_macronizer(self):
        """Test Classical Latin IPA transcription via Allen reconstruction,\
         with automatic macronization."""
        transcriber = lat.Transcriber("Classical", "Allen").transcribe
        transcription = transcriber(
            "Quo usque tandem, O Catilina, abutere nostra patientia?", 
            macronize=True)
        target = ("['kʷoː 'ʊs.kʷɛ 't̪an̪.d̪ẽː 'oː ka.t̪ɪ.'liː.n̪aː a.buː.'t̪eː.rɛ" 
            + " 'n̪ɔs.t̪raː pa.t̪ɪ̣.'jɛn̪.t̪ɪ̣.ja]")
        self.assertEqual(transcription, target)

    def test_akkadian_stress(self):
        """Test finding stressed syllable in an Akkadian word."""
        word = "napištašunu"
        target = ['na', '[piš]', 'ta', 'šu', 'nu']
        stresser = AkkadianStress.StressFinder()
        stress = stresser.find_stress(word)
        self.assertEqual(target, stress)

    def test_arabic_transliterate(self):
        """
         arabic transliterate: Roman <-> Arabic
        :return:
        """
        ar_string = 'بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ'
        buckwalter_string = 'bisomi Allhi Alra~Hom`ni Alra~Hiyomi'
        iso2332_string = 'bis°mi ʾllhi ʾlraّḥ°mٰni ʾlraّḥiy°mi'
        mode = "buckwalter"
        ignore = ''
        reverse = True

        # from arabic native script to buckwalter
        assert AarabicTransliterate(mode,ar_string,ignore,reverse) == 'bisomi Allhi Alra~Hom`ni Alra~Hiyomi'
        # from buckwalter to arabic native script
        reverse = False
        assert AarabicTransliterate(mode,buckwalter_string,ignore,reverse) == 'بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ'

        # from arabic native script to ISO233-2
        mode = 'iso233-2'
        reverse = True
        assert AarabicTransliterate(mode, ar_string, ignore, reverse) == 'bis°mi ʾllhi ʾlraّḥ°mٰni ʾlraّḥiy°mi'

        # from iso233-2 to arabic native script
        reverse = False
        assert AarabicTransliterate(mode,iso2332_string,ignore,reverse) == 'بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ'

if __name__ == '__main__':
    unittest.main()


