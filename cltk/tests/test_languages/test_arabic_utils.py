
""" Test CLTK Support """

__author__ = 'Lakhdar Benzahia, <lakhdar.benzahia@gmail.com>'
__reviewers__ = ['Taha Zerrouki taha.zerrouki@gmail.com', 'Kyle P. Johnson <kyle@kyle-p-johnson.com>']


from cltk.corpus.arabic.utils.pyarabic import araby
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
        assert araby.name("أ") == 'همزة على الألف'
        assert araby.name("ب") == u'باء'
        assert araby.name(araby.ALEF_HAMZA_ABOVE) == 'همزة على الألف'
        assert araby.name("ة") == 'تاء مربوطة'

        # test has_letter_functions
        self.assertTrue(araby.has_shadda('العربيّة'))
        self.assertFalse(araby.has_shadda('العربية'))

        # test word and text functions
        # is_vocalized(word)
        self.assertFalse(araby.is_vocalized('العربية'))
        self.assertTrue(araby.is_vocalized('الْعَرَبِيّةُ'))

        # is_vocalized(word)
        self.assertFalse(araby.is_vocalizedtext("العربية لغة جميلة"))
        self.assertTrue(araby.is_vocalizedtext('الْعَرَبيَّة لُغَةٌ جَمِيلَةٌ'))

        # is_arabicstring TODO: add more examples
        self.assertTrue(araby.is_arabicstring('العربية'))

        # is_arabicrange TODO: add test

        # is_arabicword TODO: test other cases

        self.assertFalse(araby.is_arabicword(""))

        self.assertFalse(araby.is_arabicword("ْلاندخل"))  # start with sukun

        self.assertFalse(araby.is_arabicword('ؤكل'))  # start with waw hamza above
        self.assertFalse(araby.is_arabicword('ئكل'))  # start with waw hamza above4
        self.assertFalse(araby.is_arabicword('ةدخل'))  # start with teh_marbuta

        self.assertTrue(araby.is_arabicword("العربية"))

        # test char_functions
        # first_char(word)
        assert araby.first_char("محمد") == 'م'

        # second_char(word)
        assert araby.second_char("محمد") == 'ح'

        #  last_char(word)
        assert araby.last_char('محمد') == 'د'

        # secondlast_char
        assert araby.secondlast_char('محمد') == 'م'

        # test strip_functions
        # strip_harakat(text):
        assert araby.strip_harakat("الْعَرَبِيّةُ") == 'العربيّة'

        # strip_lastharaka(text)
        assert araby.strip_lastharaka("الْعَرَبِيّةُ") == 'الْعَرَبِيّة'

        # strip_tashkeel(text)
        assert araby.strip_tashkeel("الْعَرَبِيّةُ") == 'العربية'

        # strip_tatweel(text):
        assert araby.strip_tatweel("العـــــربية") == 'العربية'

        # strip_shadda(text):
        assert araby.strip_shadda("الشّمسيّة") == 'الشمسية'

        # test normalization_functions
        # normalize_ligature(text):TODO: fixme gives 'لانها لالء الاسلام'
        # assert  Araby.normalize_ligature( "لانها لالء الاسلام") == 'لانها لالئ الاسلام'

        # normalize_hamza(word)
        assert araby.normalize_hamza("سئل أحد الأئمة") == 'سءل ءحد الءءمة'

        # test separate function  TODO: testme

        # test join letters with marks
        marks = u'\u064e\u0652\u064e\u064e\u064e\u064e\u064f'
        assert araby.joint("العربية", marks) == 'اَلْعَرَبَيَةُ'

        # test vocalizelike function
        word1 = "ضَربٌ"
        word2 = "ضَرْبٌ"
        self.assertTrue(araby.vocalizedlike(word1, word2))

        # test_waznlike
        word1 = "ضارب"
        wazn = "فَاعِل"
        wazn1 = "فعال"
        self.assertTrue(araby.waznlike(word1, wazn))
        self.assertFalse(araby.waznlike(word1, wazn1))

        # test shaddalike(partial, fully)
        word1 = "ردّ"
        word2 = "ردَّ"
        word3 = "رد"
        self.assertTrue(araby.shaddalike(word1, word2))
        self.assertFalse(araby.shaddalike(word1, word3))

        # test reduce_tashkeel(text)
        word = "يُتَسََلَّمْنَ"
        assert araby.reduce_tashkeel(word) == 'يُتسلّمن'

        # test vocalized_similarity(word1, word2)
        word1 = "ضَربٌ"
        word2 = "ضَرْبٌ"
        word3 = "ضَرْبٍ"
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

if __name__ == '__main__':
    unittest.main()

