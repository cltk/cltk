# -*- coding: utf-8 -*-
#### Tests for Sanskrit Transliteration Module
import unittest
from itrans_transliterator import *
from unicode_transliterate import *
from langinfo import *
__author__ = ["Nurendra Choudhary <nurendrachoudhary31@gmail.com>","Anoop Kunchukuttan <anoop.kunchukuttan@gmail.com>"]
__license__ = "GPLv3"

class TestUnicode(unittest.TestCase):

    def test_py23char(self):
        try:
            self.assertEqual(py23char(0x92D),'भ'.decode('utf-8'))
            self.assertFalse(py23char(0x93D)=='भ'.decode('utf-8'))
        except:
            self.assertEqual(py23char(0x92D),'भ')
            self.assertFalse(py23char(0x93D)=='भ')

class TestTransliteration(unittest.TestCase):

    def test_Indicization(self): # Test ItransTransliterator - Convert from Itrans to Devanagari
        x=ItransTransliterator.from_itrans(u'pitL^In','hi')
        y=ItransTransliterator.from_itrans(u'yogazcittavRttinirodhaH','hi')
        try:
            self.assertEqual(x,'पितॣन्'.decode('utf-8'))
            self.assertEqual(y,'योगश्चित्तव्ऱ्त्तिनिरोधः'.decode('utf-8'))
        except:
            self.assertEqual(x,'पितॣन्')
            self.assertEqual(y,'योगश्चित्तव्ऱ्त्तिनिरोधः')

    def test_ScriptConversion(self): # Test UnicodeIndicTransliterator - Convert between various scripts
        x = UnicodeIndicTransliterator.transliterate(u'राजस्थान',"hi","pa")
        try:
            self.assertEqual(x,'ਰਾਜਸ੍ਥਾਨ'.decode('utf-8'))
        except:
            self.assertEqual(x,'ਰਾਜਸ੍ਥਾਨ')

    def test_Romanization(self):
        try:
            x = ItransTransliterator.to_itrans(u'राजस्थान','hi')
            self.assertEqual(x,'rAjasthAna')
        except:
            x = ItransTransliterator.to_itrans('राजस्थान','hi')
            self.assertEqual(x,'raajasthaana')


class TestScriptInformation(unittest.TestCase):
    
    def test_IsVowel(self):
        try:
            self.assertFalse(is_vowel(u'क','hi'))
            self.assertTrue(is_vowel(u'अ','hi'))
        except:
            self.assertFalse(is_vowel('क','hi'))
            self.assertTrue(is_vowel('अ','hi'))
    
    def test_IsConsonant(self):
        try:
            self.assertTrue(is_consonant(u'क','hi'))
            self.assertFalse(is_consonant(u'अ','hi'))
        except:
            self.assertTrue(is_consonant('क','hi'))
            self.assertFalse(is_consonant('अ','hi'))

    def test_IsVelar(self):
        try:
            self.assertTrue(is_velar(u'क','hi'))
            self.assertFalse(is_velar(u'अ','hi'))
        except:
            self.assertTrue(is_velar('क','hi'))
            self.assertFalse(is_velar('अ','hi'))
    
    def test_IsPalatal(self):
        try:
            self.assertTrue(is_palatal(u'च','hi'))
            self.assertFalse(is_palatal(u'त','hi'))
        except:
            self.assertTrue(is_palatal('च','hi'))
            self.assertFalse(is_palatal('त','hi'))

    def test_IsAspirated(self):
        try:
            self.assertTrue(is_aspirated(u'छ','hi'))
            self.assertFalse(is_aspirated(u'क','hi'))
        except:
            self.assertTrue(is_aspirated('छ','hi'))
            self.assertFalse(is_aspirated('क','hi'))

    def test_IsUnvoiced(self):
        try:
            self.assertTrue(is_unvoiced(u'ट','hi'))
            self.assertFalse(is_unvoiced(u'ग','hi'))
        except:
            self.assertTrue(is_unvoiced('ट','hi'))
            self.assertFalse(is_unvoiced('ग','hi'))

    def test_IsNasal(self):
        try:
            self.assertTrue(is_nasal(u'ण','hi'))
            self.assertFalse(is_nasal(u'ड','hi'))
        except:
            self.assertTrue(is_nasal('ण','hi'))
            self.assertFalse(is_nasal('ड','hi'))

if __name__ == '__main__':
    unittest.main()
