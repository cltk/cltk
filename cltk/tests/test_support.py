
""" Test CLTK Support """

__author__ = 'Lakhdar Benzahia, <lakhdar.benzahia@gmail.com>'
__reviewers__ = ['Taha Zerrouki taha.zerrouki@gmail.com', 'Kyle P. Johnson <kyle@kyle-p-johnson.com>']


from cltk.support.arabic.pyarabic import araby
import unittest


class TestSequenceFunctions(unittest.TestCase):

    # test pyarabic lib support:
    def test_support_pyarabic_araby(self):

        # test is_fucntions
        self.assertTrue(araby.is_sukun(araby.SUKUN))
        self.assertTrue(araby.is_shadda(araby.SHADDA))
        self.assertTrue(araby.is_tatweel(araby.TATWEEL))

        for archar in araby.TANWIN:
            self.assertTrue(araby.is_tanwin(archar))

        for archar in araby.TASHKEEL:
            self.assertTrue(araby.is_tashkeel(archar))

        for haraka in araby.HARAKAT:
            self.assertTrue(araby.is_haraka(haraka))

        for short_haraka in araby.SHORTHARAKAT:
            self.assertTrue(araby.is_shortharaka(short_haraka))

        for liguature in araby.LIGUATURES:
            self.assertTrue(araby.is_ligature(liguature))

        for hamza in araby.HAMZAT:
            self.assertTrue(araby.is_hamza(hamza))

        for alef in araby.ALEFAT:
            self.assertTrue(araby.is_alef(alef))

        for yeh in araby.YEHLIKE:
            self.assertTrue(araby.is_yehlike(yeh))

        for waw in araby.WAWLIKE:
            self.assertTrue(araby.is_wawlike(waw))

        for teh in araby.TEHLIKE:
            self.assertTrue(araby.is_teh)

        for small in araby.SMALL:
            self.assertTrue(araby.is_small(small))

        for weak in araby.WEAK:
            self.assertTrue(araby.is_weak(weak))

        for archar in araby.MOON:
            self.assertTrue(araby.is_moon(archar))

        for archar in araby.SUN:
            self.assertTrue(araby.is_sun(archar))

        # test general functions order() and name()
        # test order()
        assert araby.order(araby.ALEF) == 1
        assert araby.order(araby.HAMZA) == 29
        assert araby.order(araby.YEH) == 28
        assert araby.order(araby.TEH_MARBUTA) == 3
        assert araby.order(araby.TEH) == 3

        # test name()
        assert araby.name(u"أ") == u'همزة على الألف'
        assert araby.name(u"ب") == u'باء'
        assert araby.name(araby.ALEF_HAMZA_ABOVE) == u'همزة على الألف'
        assert araby.name(u"ة") == u'تاء مربوطة'

        # test has_letter_functions
        self.assertTrue(araby.has_shadda(u'العربيّة'))
        self.assertFalse(araby.has_shadda(u'العربية'))

        # test word and text functions
        # is_vocalized(word)
        self.assertFalse(araby.is_vocalized(u'العربية'))
        self.assertTrue(araby.is_vocalized(u'الْعَرَبِيّةُ'))

        # is_vocalized(word)
        self.assertFalse(araby.is_vocalizedtext(u"العربية لغة جميلة"))
        self.assertTrue(araby.is_vocalizedtext(u'الْعَرَبيَّة لُغَةٌ جَمِيلَةٌ'))

        # is_arabicstring TODO: add more examples
        self.assertTrue(araby.is_arabicstring(u'العربية'))

        # is_arabicrange TODO: add test

        # is_arabicword TODO: test other cases

        self.assertFalse(araby.is_arabicword(u""))

        self.assertFalse(araby.is_arabicword(u"ْلاندخل"))  # start with sukun

        self.assertFalse(araby.is_arabicword(u'ؤكل'))  # start with waw hamza above
        self.assertFalse(araby.is_arabicword(u'ئكل'))  # start with waw hamza above4
        self.assertFalse(araby.is_arabicword(u'ةدخل'))  # start with teh_marbuta

        self.assertTrue(araby.is_arabicword("العربية"))

        # test char_functions
        # first_char(word)
        assert araby.first_char(u"محمد") == u'م'

        # second_char(word)
        assert araby.second_char(u"محمد") == u'ح'

        #  last_char(word)
        assert araby.last_char(u'محمد') == u'د'

        # secondlast_char
        assert araby.secondlast_char(u'محمد') == u'م'

        # test strip_functions
        # strip_harakat(text):
        assert araby.strip_harakat(u"الْعَرَبِيّةُ") == u'العربيّة'

        # strip_lastharaka(text)
        assert araby.strip_lastharaka(u"الْعَرَبِيّةُ") == u'الْعَرَبِيّة'

        # strip_tashkeel(text)
        assert araby.strip_tashkeel(u"الْعَرَبِيّةُ") == u'العربية'

        # strip_tatweel(text):
        assert araby.strip_tatweel(u"العـــــربية") == u'العربية'

        # strip_shadda(text):
        assert araby.strip_shadda(u"الشّمسيّة") == u'الشمسية'

        # test normalization_functions
        # normalize_ligature(text):TODO: fixme gives 'لانها لالء الاسلام'
        # assert  Araby.normalize_ligature( u"لانها لالء الاسلام") == u'لانها لالئ الاسلام'

        # normalize_hamza(word)
        assert araby.normalize_hamza(u"سئل أحد الأئمة") == u'سءل ءحد الءءمة'

        # test separate function  TODO: testme

        # test join letters with marks
        marks = u'\u064e\u0652\u064e\u064e\u064e\u064e\u064f'
        assert araby.joint(u"العربية", marks) == u'اَلْعَرَبَيَةُ'

        # test vocalizelike function
        word1 = u"ضَربٌ"
        word2 = u"ضَرْبٌ"
        self.assertTrue(araby.vocalizedlike(word1, word2))

        # test_waznlike
        word1 = u"ضارب"
        wazn = u"فَاعِل"
        wazn1 = u"فعال"
        self.assertTrue(araby.waznlike(word1, wazn))
        self.assertFalse(araby.waznlike(word1, wazn1))

        # test shaddalike(partial, fully)
        word1 = u"ردّ"
        word2 = u"ردَّ"
        word3 = u"رد"
        self.assertTrue(araby.shaddalike(word1, word2))
        self.assertFalse(araby.shaddalike(word1, word3))

        # test reduce_tashkeel(text)
        word = u"يُتَسََلَّمْنَ"
        assert araby.reduce_tashkeel(word) == u'يُتسلّمن'

        # test vocalized_similarity(word1, word2)
        word1 = u"ضَربٌ"
        word2 = u"ضَرْبٌ"
        word3 = u"ضَرْبٍ"
        self.assertTrue(araby.vocalized_similarity(word1, word2))
        assert araby.vocalized_similarity(word1, word3) == -1

        #test tokenize(text = u"")

        tests = ['اللُّغَةُ الْعَرَبِيَّةُ جَمِيلَةٌ.',
                 'انما الْمُؤْمِنُونَ اخوه فاصلحوا بَيْنَ اخويكم',
                 'الْعَجُزُ عَنِ الْإِدْرَاكِ إِدْرَاكٌ، وَالْبَحْثَ فِي ذاتِ اللَّه اشراك.',
                 'اللَّهُمُّ اُسْتُرْ عُيُوبَنَا وَأَحْسَنَ خَوَاتِيمَنَا الْكَاتِبِ: نَبِيلُ جلهوم',
                 'الرَّأْي قَبْلَ شَجَاعَة الشّجعَانِ',
                 'فَأَنْزَلْنَا مِنْ السَّمَاء مَاء فَأَسْقَيْنَاكُمُوهُ',
                 'سُئِلَ بَعْضُ الْكُتَّابِ عَنِ الْخَطّ، مَتَى يَسْتَحِقُّ أَنْ يُوصَفَ بِالْجَوْدَةِ ؟'
                 ]

        results = []
        for test in tests:
            result = araby.tokenize(test)
            results.append(result)

        target = [['اللُّغَةُ', 'الْعَرَبِيَّةُ', 'جَمِيلَةٌ', '.'],
                  ['انما', 'الْمُؤْمِنُونَ', 'اخوه', 'فاصلحوا', 'بَيْنَ', 'اخويكم'],
                  ['الْعَجُزُ', 'عَنِ', 'الْإِدْرَاكِ', 'إِدْرَاكٌ', '،', 'وَالْبَحْثَ', 'فِي', 'ذاتِ', 'اللَّه',
                   'اشراك', '.'],
                  ['اللَّهُمُّ', 'اُسْتُرْ', 'عُيُوبَنَا', 'وَأَحْسَنَ', 'خَوَاتِيمَنَا', 'الْكَاتِبِ', ':', 'نَبِيلُ',
                   'جلهوم'],
                  ['الرَّأْي', 'قَبْلَ', 'شَجَاعَة', 'الشّجعَانِ'],
                  ['فَأَنْزَلْنَا', 'مِنْ', 'السَّمَاء', 'مَاء', 'فَأَسْقَيْنَاكُمُوهُ'],
                  ['سُئِلَ', 'بَعْضُ', 'الْكُتَّابِ', 'عَنِ', 'الْخَطّ', '،', 'مَتَى', 'يَسْتَحِقُّ', 'أَنْ', 'يُوصَفَ',
                   'بِالْجَوْدَةِ', '؟']
                  ]
        self.assertEqual(results, target)

if __name__ == "__main__":
    unittest.main()
