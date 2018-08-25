'''
Various test cases for akkadian functions in the CLTK
'''

__author__ = ['M. Willis Monroe <willismonroe@gmail.com>',
              'Andrew Deloucas <adeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'

from cltk.phonology.akkadian.stress import StressFinder  # pylint: disable=import-error
from cltk.corpus.akkadian.cdli_corpus import CDLICorpus  # pylint: disable=import-error
from cltk.corpus.akkadian.pretty_print import PrettyPrint  # pylint: disable=import-error
from cltk.corpus.akkadian.file_importer import FileImport  # pylint: disable=import-error
from cltk.corpus.akkadian.tokenizer import Tokenizer  # pylint: disable=import-error

import unittest
import os

TOKENIZER = Tokenizer(preserve_damage=False)
SAMPLE_TEXT = \
['Primary publication: ARM 01, 001',
 'Author(s): Dossin, Georges',
 'Publication date: 1946',
 'Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0305',
 'Collection: National Museum of Syria, Damascus, Syria',
 'Museum no.: NMSD —',
 'Accession no.:',
 'Provenience: Mari (mod. Tell Hariri)',
 'Excavation no.:',
 'Period: Old Babylonian (ca. 1900-1600 BC)',
 'Dates referenced:',
 'Object type: tablet',
 'Remarks:',
 'Material: clay',
 'Language: Akkadian',
 'Genre: Letter',
 'Sub-genre:',
 'CDLI comments:',
 'Catalogue source: 20050104 cdliadmin',
 'ATF source: cdlistaff',
 'Translation: Durand, Jean-Marie (fr); Guerra, Dylan M. (en)',
 'UCLA Library ARK: 21198/zz001rsp8x',
 'Composite no.:',
 'Seal no.:',
 'CDLI no.: P254202',
 'Transliteration:',
 '&P254202 = ARM 01, 001',
 '#atf: lang akk',
 '@tablet',
 '@obverse',
 '1. a-na ia-ah-du-li-[im]',
 '2. qi2-bi2-[ma]',
 '3. um-ma a-bi-sa-mar#-[ma]',
 '4. sa-li-ma-am e-pu-[usz]',
 '5. asz-szum mu-sze-zi-ba-am# [la i-szu]',
 '6. [sa]-li#-ma-am sza e-[pu-szu]',
 '7. [u2-ul] e-pu-usz sa#-[li-mu-um]',
 '8. [u2-ul] sa-[li-mu-um-ma]',
 '$ rest broken',
 '@reverse',
 '$ beginning broken',
 "1'. isz#-tu mu#-[sze-zi-ba-am la i-szu]",
 "2'. a-la-nu-ia sza la is,-s,a-ab#-[tu]",
 "3'. i-na-an-na is,-s,a-ab-[tu]",
 "4'. i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]",
 "5'. ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]",
 "6'. u3 ia-am-ha-ad[{ki}]",
 "7'. a-la-nu an-nu-tum u2-ul ih-li-qu2#",
 "8'. i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma",
 "9'. ih-ta-al-qu2",
 "10'. u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#",
 "11'. u3 na-pa-asz2-ti u2-ba-li-it,",
 "12'. pi2-qa-at ha-s,e-ra#-at",
 "13'. asz-szum a-la-nu-ka",
 "14'. u3 ma-ru-ka sza-al#-[mu]",
 "15'. [a-na na-pa]-asz2#-ti-ia i-tu-ur",
 '',
 '',
 'Primary publication: ARM 01, 002',
 'Author(s): Dossin, Georges',
 'Publication date: 1946',
 'Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0306',
 'Collection: National Museum of Syria, Damascus, Syria',
 'Museum no.: NMSD —',
 'Accession no.:',
 'Provenience: Mari (mod. Tell Hariri)',
 'Excavation no.:',
 'Period: Old Babylonian (ca. 1900-1600 BC)',
 'Dates referenced:',
 'Object type: tablet',
 'Remarks:',
 'Material: clay',
 'Language: Akkadian',
 'Genre: Letter',
 'Sub-genre:',
 'CDLI comments:',
 'Catalogue source: 20050104 cdliadmin',
 'ATF source: cdlistaff',
 'Translation:',
 'UCLA Library ARK: 21198/zz001rsp9f',
 'Composite no.:',
 'Seal no.:',
 'CDLI no.: P254203',
 'Transliteration:',
 '&P254203 = ARM 01, 002',
 '#atf: lang akk',
 '@tablet',
 '@obverse',
 '1. a-na ia-ah-du-[li-im]',
 '2. qi2-bi2-[ma]',
 '3. um-ma a-bi-sa-mar-[ma]',
 '4. asz-szum sza a-qa-bi-kum la ta-ha-asz2#',
 '5. a-na ma-ni-im lu-ud-bu-ub',
 '6. szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]',
 '7. szum-ma a-bi-sa-mar te-zi-ir#',
 '8. u3 a-la#-ni#-ka te-zi-ir-ma#',
 '9. i-na an-ni-a-tim sza a-da-bu-[bu]',
 '10. a-na-ku mi-im-ma u2-ul e-le#-[i]',
 '11. sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]',
 '12. u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]',
 '13. u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]',
 '14. u3 lu ma-at ia-ma-ha-ad#{ki}',
 '15. u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]',
 '$ rest broken',
 '@reverse',
 '$ beginning broken',
 "1'. um#-[...]",
 "2'. lu#-[...]",
 "3'. a-[...]",
 "4'. szum#-[...]",
 "5'. a-na# [...]",
 "6'. ma-li# [...]",
 "7'. u3 u2-hu-ur# [...]",
 "8'. a-su2-ur-ri [...]",
 "9'. szu-zi-ba-an#-[ni ...]",
 "10'. a-na [...]",
 "11'. pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]",
 '@left',
 '1. {disz}a-bi-sa-mar u2-ul ma-ri u3 bi-ti a-na la bi-tu#-[tu-ur2-ma]',
 '2. bi-tum bi-it-ka u3 {disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]']

class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    '''
    An experiment to use Huehnergard's grammar and key to test the functions
    in the cltk.
    '''

    def test_lesson_1_exercise_d(self):
        """Tests stresser"""
        nouns = ['abum', 'ālum', 'amtum', 'bēlum', 'ḫurāṣum', 'iltum',
                 'ilum', 'kaspum', 'mārtum', 'mārum', 'qaqqadum',
                 'ṣābum', 'šarratum', 'šarrum', 'wardum']
        stresser = StressFinder()
        stress = []
        for noun in nouns:
            stress.append(stresser.find_stress(noun))
        target = [['[a]', 'bum'], ['[ā]', 'lum'], ['[am]', 'tum'],
                  ['[bē]', 'lum'], ['ḫu', '[rā]', 'ṣum'],
                  ['[il]', 'tum'], ['[i]', 'lum'], ['[kas]', 'pum'],
                  ['[mār]', 'tum'], ['[mā]', 'rum'],
                  ['[qaq]', 'qa', 'dum'], ['[ṣā]', 'bum'],
                  ['[šar]', 'ra', 'tum'], ['[šar]', 'rum'],
                  ['[war]', 'dum']]

        self.assertEqual(stress, target)

    def test_lesson_1_exercise_e(self):
        """Tests Stresser"""
        nouns = ['mušallimum', 'išāl', 'idin', 'iddinūniššum',
                 'tabnianni', 'niqīaš', 'epēšum', 'kullumum', 'tabnû',
                 'iššiakkum', 'rēdûm', 'iqbi', 'paris', 'išmeānim',
                 'pete', 'šūṣû']
        stresser = StressFinder()
        stress = []
        for noun in nouns:
            stress.append(stresser.find_stress(noun))
        target = [['mu', '[šal]', 'li', 'mum'], ['i', '[šāl]'],
                  ['[i]', 'din'], ['id', 'di', 'nū', '[niš]', 'šum'],
                  ['tab', 'ni', '[an]', 'ni'], ['ni', '[qī]', 'aš'],
                  ['e', '[pē]', 'šum'], ['[kul]', 'lu', 'mum'],
                  ['tab', '[nû]'], ['iš', 'ši', '[ak]', 'kum'],
                  ['rē', '[dûm]'], ['[iq]', 'bi'], ['[pa]', 'ris'],
                  ['iš', 'me', '[ā]', 'nim'], ['[pe]', 'te'], ['šū', '[ṣû]']]

        self.assertEqual(stress, target)

    def test_lesson_2_exercise_b(self):
        """Tests Stresser"""
        nouns = ['aššatum', 'bītum', 'emūqum', 'īnum', 'išdum',
                 'libbum', 'mutum', 'nārum', 'šīpātum', 'ṭuppum',
                 'ummum', 'uznum']
        stresser = StressFinder()
        stress = []
        for noun in nouns:
            stress.append(stresser.find_stress(noun))
        target = [['[aš]', 'ša', 'tum'], ['[bī]', 'tum'],
                  ['e', '[mū]', 'qum'], ['[ī]', 'num'], ['[iš]', 'dum'],
                  ['[lib]', 'bum'], ['[mu]', 'tum'],
                  ['[nā]', 'rum'], ['šī', '[pā]', 'tum'], ['[ṭup]', 'pum'],
                  ['[um]', 'mum'], ['[uz]', 'num']]

        self.assertEqual(stress, target)


class TestcasesfromGSOC(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""
    def test_read_file(self):
        """
        Tests read_file.
        """
        cdli = FileImport(os.path.join(os.path.dirname(__file__), 'single_text.txt'))
        cdli.read_file()
        final = cdli.file_lines
        goal = ['Primary publication: ARM 01, 001',
                'Author(s): Dossin, Georges',
                'Publication date: 1946',
                'Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0305',
                'Collection: National Museum of Syria, Damascus, Syria',
                'Museum no.: NMSD —',
                'Accession no.:',
                'Provenience: Mari (mod. Tell Hariri)',
                'Excavation no.:',
                'Period: Old Babylonian (ca. 1900-1600 BC)',
                'Dates referenced:',
                'Object type: tablet',
                'Remarks:',
                'Material: clay',
                'Language: Akkadian',
                'Genre: Letter',
                'Sub-genre:',
                'CDLI comments:',
                'Catalogue source: 20050104 cdliadmin',
                'ATF source: cdlistaff',
                'Translation: Durand, Jean-Marie (fr); Guerra, Dylan M. (en)',
                'UCLA Library ARK: 21198/zz001rsp8x',
                'Composite no.:',
                'Seal no.:',
                'CDLI no.: P254202',
                'Transliteration:',
                '&P254202 = ARM 01, 001',
                '#atf: lang akk',
                '@tablet',
                '@obverse',
                '1. a-na ia-ah-du-li-[im]',
                '2. qi2-bi2-[ma]',
                '3. um-ma a-bi-sa-mar#-[ma]',
                '4. sa-li-ma-am e-pu-[usz]',
                '5. asz-szum mu-sze-zi-ba-am# [la i-szu]',
                '6. [sa]-li#-ma-am sza e-[pu-szu]',
                '7. [u2-ul] e-pu-usz sa#-[li-mu-um]',
                '8. [u2-ul] sa-[li-mu-um-ma]',
                '$ rest broken',
                '@reverse',
                '$ beginning broken',
                "1'. isz#-tu mu#-[sze-zi-ba-am la i-szu]",
                "2'. a-la-nu-ia sza la is,-s,a-ab#-[tu]",
                "3'. i-na-an-na is,-s,a-ab-[tu]",
                "4'. i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]",
                "5'. ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]",
                "6'. u3 ia-am-ha-ad[{ki}]",
                "7'. a-la-nu an-nu-tum u2-ul ih-li-qu2#",
                "8'. i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma",
                "9'. ih-ta-al-qu2",
                "10'. u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#",
                "11'. u3 na-pa-asz2-ti u2-ba-li-it,",
                "12'. pi2-qa-at ha-s,e-ra#-at",
                "13'. asz-szum a-la-nu-ka",
                "14'. u3 ma-ru-ka sza-al#-[mu]",
                "15'. [a-na na-pa]-asz2#-ti-ia i-tu-ur"]
        print(os.getcwd())
        self.assertEqual(final, goal)

    def test_file_catalog(self):
        """
        Tests file_catalog.
        """
        cdli = FileImport(os.path.join(os.path.dirname(__file__), 'single_text.txt'))
        cdli.file_catalog()
        final = cdli.catalog
        goal = ['__pycache__', 'html_file.html', 'html_single_text.html',
                'single_text.txt', 'test_akkadian.py',
                'two_text_abnormalities.txt']
        self.assertEqual(final, goal)

    def test_parse_file(self):
        """
        Tests parse_file.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        output = cdli.chunks
        goal = [['Primary publication: ARM 01, 001',
                 'Author(s): Dossin, Georges',
                 'Publication date: 1946',
                 'Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0305',
                 'Collection: National Museum of Syria, Damascus, Syria',
                 'Museum no.: NMSD —',
                 'Accession no.:',
                 'Provenience: Mari (mod. Tell Hariri)',
                 'Excavation no.:',
                 'Period: Old Babylonian (ca. 1900-1600 BC)',
                 'Dates referenced:',
                 'Object type: tablet',
                 'Remarks:',
                 'Material: clay',
                 'Language: Akkadian',
                 'Genre: Letter',
                 'Sub-genre:',
                 'CDLI comments:',
                 'Catalogue source: 20050104 cdliadmin',
                 'ATF source: cdlistaff',
                 'Translation: Durand, Jean-Marie (fr); Guerra, Dylan M. (en)',
                 'UCLA Library ARK: 21198/zz001rsp8x',
                 'Composite no.:',
                 'Seal no.:',
                 'CDLI no.: P254202',
                 'Transliteration:',
                 '&P254202 = ARM 01, 001',
                 '#atf: lang akk',
                 '@tablet',
                 '@obverse',
                 '1. a-na ia-ah-du-li-[im]',
                 '2. qi2-bi2-[ma]',
                 '3. um-ma a-bi-sa-mar#-[ma]',
                 '4. sa-li-ma-am e-pu-[usz]',
                 '5. asz-szum mu-sze-zi-ba-am# [la i-szu]',
                 '6. [sa]-li#-ma-am sza e-[pu-szu]',
                 '7. [u2-ul] e-pu-usz sa#-[li-mu-um]',
                 '8. [u2-ul] sa-[li-mu-um-ma]',
                 '$ rest broken',
                 '@reverse',
                 '$ beginning broken',
                 "1'. isz#-tu mu#-[sze-zi-ba-am la i-szu]",
                 "2'. a-la-nu-ia sza la is,-s,a-ab#-[tu]",
                 "3'. i-na-an-na is,-s,a-ab-[tu]",
                 "4'. i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]",
                 "5'. ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]",
                 "6'. u3 ia-am-ha-ad[{ki}]",
                 "7'. a-la-nu an-nu-tum u2-ul ih-li-qu2#",
                 "8'. i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma",
                 "9'. ih-ta-al-qu2",
                 "10'. u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#",
                 "11'. u3 na-pa-asz2-ti u2-ba-li-it,",
                 "12'. pi2-qa-at ha-s,e-ra#-at",
                 "13'. asz-szum a-la-nu-ka",
                 "14'. u3 ma-ru-ka sza-al#-[mu]",
                 "15'. [a-na na-pa]-asz2#-ti-ia i-tu-ur"],
                ['Primary publication: ARM 01, 002',
                 'Author(s): Dossin, Georges',
                 'Publication date: 1946',
                 'Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0306',
                 'Collection: National Museum of Syria, Damascus, Syria',
                 'Museum no.: NMSD —',
                 'Accession no.:',
                 'Provenience: Mari (mod. Tell Hariri)',
                 'Excavation no.:',
                 'Period: Old Babylonian (ca. 1900-1600 BC)',
                 'Dates referenced:',
                 'Object type: tablet',
                 'Remarks:',
                 'Material: clay',
                 'Language: Akkadian',
                 'Genre: Letter',
                 'Sub-genre:',
                 'CDLI comments:',
                 'Catalogue source: 20050104 cdliadmin',
                 'ATF source: cdlistaff',
                 'Translation:',
                 'UCLA Library ARK: 21198/zz001rsp9f',
                 'Composite no.:',
                 'Seal no.:',
                 'CDLI no.: P254203',
                 'Transliteration:',
                 '&P254203 = ARM 01, 002',
                 '#atf: lang akk',
                 '@tablet',
                 '@obverse',
                 '1. a-na ia-ah-du-[li-im]',
                 '2. qi2-bi2-[ma]',
                 '3. um-ma a-bi-sa-mar-[ma]',
                 '4. asz-szum sza a-qa-bi-kum la ta-ha-asz2#',
                 '5. a-na ma-ni-im lu-ud-bu-ub',
                 '6. szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]',
                 '7. szum-ma a-bi-sa-mar te-zi-ir#',
                 '8. u3 a-la#-ni#-ka te-zi-ir-ma#',
                 '9. i-na an-ni-a-tim sza a-da-bu-[bu]',
                 '10. a-na-ku mi-im-ma u2-ul e-le#-[i]',
                 '11. sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]',
                 '12. u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]',
                 '13. u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]',
                 '14. u3 lu ma-at ia-ma-ha-ad#{ki}',
                 '15. u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]',
                 '$ rest broken',
                 '@reverse',
                 '$ beginning broken',
                 "1'. um#-[...]",
                 "2'. lu#-[...]",
                 "3'. a-[...]",
                 "4'. szum#-[...]",
                 "5'. a-na# [...]",
                 "6'. ma-li# [...]",
                 "7'. u3 u2-hu-ur# [...]",
                 "8'. a-su2-ur-ri [...]",
                 "9'. szu-zi-ba-an#-[ni ...]",
                 "10'. a-na [...]",
                 "11'. pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]",
                 '@left',
                 '1. {disz}a-bi-sa-mar u2-ul ma-ri u3 bi-ti a-na '
                 'la bi-tu#-[tu-ur2-ma]',
                 '2. bi-tum bi-it-ka u3 {disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]']]
        self.assertEqual(output, goal)

    def test_call_text(self):
        """
        Tests calling a text.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        output = cdli.catalog['P254203']['raw_text']
        goal = ['@obverse',
                '1. a-na ia-ah-du-[li-im]',
                '2. qi2-bi2-[ma]',
                '3. um-ma a-bi-sa-mar-[ma]',
                '4. asz-szum sza a-qa-bi-kum la ta-ha-asz2#',
                '5. a-na ma-ni-im lu-ud-bu-ub',
                '6. szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]',
                '7. szum-ma a-bi-sa-mar te-zi-ir#',
                '8. u3 a-la#-ni#-ka te-zi-ir-ma#',
                '9. i-na an-ni-a-tim sza a-da-bu-[bu]',
                '10. a-na-ku mi-im-ma u2-ul e-le#-[i]',
                '11. sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]',
                '12. u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]',
                '13. u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]',
                '14. u3 lu ma-at ia-ma-ha-ad#{ki}',
                '15. u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]',
                '$ rest broken',
                '@reverse',
                '$ beginning broken',
                "1'. um#-[...]",
                "2'. lu#-[...]",
                "3'. a-[...]",
                "4'. szum#-[...]",
                "5'. a-na# [...]",
                "6'. ma-li# [...]",
                "7'. u3 u2-hu-ur# [...]",
                "8'. a-su2-ur-ri [...]",
                "9'. szu-zi-ba-an#-[ni ...]",
                "10'. a-na [...]",
                "11'. pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]",
                '@left',
                '1. {disz}a-bi-sa-mar u2-ul ma-ri u3 bi-ti a-na la bi-tu#-[tu-ur2-ma]',
                '2. bi-tum bi-it-ka u3 {disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]']
        self.assertEqual(output, goal)

    def test_find_cdli_number(self):
        """
        Tests list_pnums.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        output = cdli.list_pnums()
        goal = ['P254202', 'P254203']
        self.assertEqual(output, goal)

    def test_find_edition(self):
        """
        Tests list_editions.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        output = cdli.list_editions()
        goal = ['ARM 01, 001', 'ARM 01, 002']
        self.assertEqual(output, goal)

    def test_find_metadata(self):
        """
        Tests calling metadata in a file.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        output = [cdli.catalog[text]['metadata'] for text in cdli.catalog]
        goal = [['Primary publication: ARM 01, 001',
                 'Author(s): Dossin, Georges',
                 'Publication date: 1946',
                 'Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0305',
                 'Collection: National Museum of Syria, Damascus, Syria',
                 'Museum no.: NMSD —',
                 'Accession no.:',
                 'Provenience: Mari (mod. Tell Hariri)',
                 'Excavation no.:',
                 'Period: Old Babylonian (ca. 1900-1600 BC)',
                 'Dates referenced:',
                 'Object type: tablet',
                 'Remarks:',
                 'Material: clay',
                 'Language: Akkadian',
                 'Genre: Letter',
                 'Sub-genre:',
                 'CDLI comments:',
                 'Catalogue source: 20050104 cdliadmin',
                 'ATF source: cdlistaff',
                 'Translation: Durand, Jean-Marie (fr); Guerra, Dylan M. (en)',
                 'UCLA Library ARK: 21198/zz001rsp8x',
                 'Composite no.:',
                 'Seal no.:',
                 'CDLI no.: P254202'],
                ['Primary publication: ARM 01, 002',
                 'Author(s): Dossin, Georges',
                 'Publication date: 1946',
                 'Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0306',
                 'Collection: National Museum of Syria, Damascus, Syria',
                 'Museum no.: NMSD —',
                 'Accession no.:',
                 'Provenience: Mari (mod. Tell Hariri)',
                 'Excavation no.:',
                 'Period: Old Babylonian (ca. 1900-1600 BC)',
                 'Dates referenced:',
                 'Object type: tablet',
                 'Remarks:',
                 'Material: clay',
                 'Language: Akkadian',
                 'Genre: Letter',
                 'Sub-genre:',
                 'CDLI comments:',
                 'Catalogue source: 20050104 cdliadmin',
                 'ATF source: cdlistaff',
                 'Translation:',
                 'UCLA Library ARK: 21198/zz001rsp9f',
                 'Composite no.:',
                 'Seal no.:',
                 'CDLI no.: P254203']]
        self.assertEqual(output, goal)

    def test_find_transliteration(self):
        """
        Tests calling transliteration in a file.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        output = [cdli.catalog[text]['transliteration'] for text in cdli.catalog]
        goal = [['a-na ia-ah-du-li-[im]',
                 'qi2-bi2-[ma]',
                 'um-ma a-bi-sa-mar#-[ma]',
                 'sa-li-ma-am e-pu-[usz]',
                 'asz-szum mu-sze-zi-ba-am# [la i-szu]',
                 '[sa]-li#-ma-am sza e-[pu-szu]',
                 '[u2-ul] e-pu-usz sa#-[li-mu-um]',
                 '[u2-ul] sa-[li-mu-um-ma]',
                 'isz#-tu mu#-[sze-zi-ba-am la i-szu]',
                 'a-la-nu-ia sza la is,-s,a-ab#-[tu]',
                 'i-na-an-na is,-s,a-ab-[tu]',
                 'i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]',
                 'ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]',
                 'u3 ia-am-ha-ad[{ki}]',
                 'a-la-nu an-nu-tum u2-ul ih-li-qu2#',
                 'i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma',
                 'ih-ta-al-qu2',
                 'u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#',
                 'u3 na-pa-asz2-ti u2-ba-li-it,',
                 'pi2-qa-at ha-s,e-ra#-at',
                 'asz-szum a-la-nu-ka',
                 'u3 ma-ru-ka sza-al#-[mu]',
                 '[a-na na-pa]-asz2#-ti-ia i-tu-ur'],
                ['a-na ia-ah-du-[li-im]',
                 'qi2-bi2-[ma]',
                 'um-ma a-bi-sa-mar-[ma]',
                 'asz-szum sza a-qa-bi-kum la ta-ha-asz2#',
                 'a-na ma-ni-im lu-ud-bu-ub',
                 'szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]',
                 'szum-ma a-bi-sa-mar te-zi-ir#',
                 'u3 a-la#-ni#-ka te-zi-ir-ma#',
                 'i-na an-ni-a-tim sza a-da-bu-[bu]',
                 'a-na-ku mi-im-ma u2-ul e-le#-[i]',
                 'sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]',
                 'u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]',
                 'u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]',
                 'u3 lu ma-at ia-ma-ha-ad#{ki}',
                 'u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]',
                 'um#-[...]',
                 'lu#-[...]',
                 'a-[...]',
                 'szum#-[...]',
                 'a-na# [...]',
                 'ma-li# [...]',
                 'u3 u2-hu-ur# [...]',
                 'a-su2-ur-ri [...]',
                 'szu-zi-ba-an#-[ni ...]',
                 'a-na [...]',
                 'pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]',
                 '{disz}a-bi-sa-mar u2-ul ma-ri u3 bi-ti a-na la bi-tu#-[tu-ur2-ma]',
                 'bi-tum bi-it-ka u3 {disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]']]
        self.assertEqual(output, goal)

    def test_table_of_contents(self):
        """
        Tests toc.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        output = cdli.toc()
        goal = ['Pnum: P254202, Edition: ARM 01, 001, length: 23 line(s)',
                'Pnum: P254203, Edition: ARM 01, 002, length: 28 line(s)']
        self.assertEqual(output, goal)

    def test_abnormalities(self):
        """Tests lines 83, 102, 121-2"""
        f_i = FileImport(os.path.join(os.path.dirname(__file__), 'two_text_abnormalities.txt'))
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        cdli.parse_file(text_file)
        goal = \
            {'P254202':
                 {'edition': 'ARM 01, 001',
                  'metadata': [],
                  'normalization': [],
                  'pnum': 'P254202',
                  'raw_text': ['@obverse',
                               '1. a-na ia-ah-du-li-[im]',
                               '2. qi2-bi2-[ma]',
                               '3. um-ma a-bi-sa-mar#-[ma]',
                               '4. sa-li-ma-am e-pu-[usz]',
                               '5. asz-szum mu-sze-zi-ba-am# [la i-szu]',
                               '6. [sa]-li#-ma-am sza e-[pu-szu]',
                               '7. [u2-ul] e-pu-usz sa#-[li-mu-um]',
                               '8. [u2-ul] sa-[li-mu-um-ma]',
                               '$ rest broken',
                               '@reverse',
                               '$ beginning broken',
                               "1'. isz#-tu mu#-[sze-zi-ba-am la i-szu]",
                               "2'. a-la-nu-ia sza la is,-s,a-ab#-[tu]",
                               "3'. i-na-an-na is,-s,a-ab-[tu]",
                               "4'. i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]",
                               "5'. ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]",
                               "6'. u3 ia-am-ha-ad[{ki}]",
                               "7'. a-la-nu an-nu-tum u2-ul ih-li-qu2#",
                               "8'. i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma",
                               "9'. ih-ta-al-qu2",
                               "10'. u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#",
                               "11'. u3 na-pa-asz2-ti u2-ba-li-it,",
                               "12'. pi2-qa-at ha-s,e-ra#-at",
                               "13'. asz-szum a-la-nu-ka",
                               "14'. u3 ma-ru-ka sza-al#-[mu]",
                               "15'. [a-na na-pa]-asz2#-ti-ia i-tu-ur"],
                  'translation': [],
                  'transliteration': ['a-na ia-ah-du-li-[im]',
                                      'qi2-bi2-[ma]',
                                      'um-ma a-bi-sa-mar#-[ma]',
                                      'sa-li-ma-am e-pu-[usz]',
                                      'asz-szum mu-sze-zi-ba-am# [la i-szu]',
                                      '[sa]-li#-ma-am sza e-[pu-szu]',
                                      '[u2-ul] e-pu-usz sa#-[li-mu-um]',
                                      '[u2-ul] sa-[li-mu-um-ma]',
                                      'isz#-tu mu#-[sze-zi-ba-am la i-szu]',
                                      'a-la-nu-ia sza la is,-s,a-ab#-[tu]',
                                      'i-na-an-na is,-s,a-ab-[tu]',
                                      'i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]',
                                      'ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]',
                                      'u3 ia-am-ha-ad[{ki}]',
                                      'a-la-nu an-nu-tum u2-ul ih-li-qu2#',
                                      'i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma',
                                      'ih-ta-al-qu2',
                                      'u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#',
                                      'u3 na-pa-asz2-ti u2-ba-li-it,',
                                      'pi2-qa-at ha-s,e-ra#-at',
                                      'asz-szum a-la-nu-ka',
                                      'u3 ma-ru-ka sza-al#-[mu]',
                                      '[a-na na-pa]-asz2#-ti-ia i-tu-ur']},
             'P254203': {'edition': '',
                         'metadata': [],
                         'normalization': [],
                         'pnum': 'P254203',
                         'raw_text': ['@obverse',
                                      '1. a-na ia-ah-du-[li-im]',
                                      '2. qi2-bi2-[ma]',
                                      '3. um-ma a-bi-sa-mar-[ma]',
                                      '4. asz-szum sza a-qa-bi-kum la ta-ha-asz2#',
                                      '5. a-na ma-ni-im lu-ud-bu-ub',
                                      '6. szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]',
                                      '7. szum-ma a-bi-sa-mar te-zi-ir#',
                                      '8. u3 a-la#-ni#-ka te-zi-ir-ma#',
                                      '9. i-na an-ni-a-tim sza a-da-bu-[bu]',
                                      '10. a-na-ku mi-im-ma u2-ul e-le#-[i]',
                                      '11. sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]',
                                      '12. u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]',
                                      '13. u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]',
                                      '14. u3 lu ma-at ia-ma-ha-ad#{ki}',
                                      '15. u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]',
                                      '$ rest broken',
                                      '@reverse',
                                      '$ beginning broken',
                                      "1'. um#-[...]",
                                      "2'. lu#-[...]",
                                      "3'. a-[...]",
                                      "4'. szum#-[...]",
                                      "5'. a-na# [...]",
                                      "6'. ma-li# [...]",
                                      "7'. u3 u2-hu-ur# [...]",
                                      "8'. a-su2-ur-ri [...]",
                                      "9'. szu-zi-ba-an#-[ni ...]",
                                      "10'. a-na [...]",
                                      "11'. pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]",
                                      '@left',
                                      '1. {disz}a-bi-sa-mar u2-ul ma-ri u3 '
                                      'bi-ti a-na la bi-tu#-[tu-ur2-ma]',
                                      '2. bi-tum bi-it-ka u3 {disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]'],
                         'translation': [],
                         'transliteration': ['a-na ia-ah-du-[li-im]',
                                             'qi2-bi2-[ma]',
                                             'um-ma a-bi-sa-mar-[ma]',
                                             'asz-szum sza a-qa-bi-kum la ta-ha-asz2#',
                                             'a-na ma-ni-im lu-ud-bu-ub',
                                             'szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]',
                                             'szum-ma a-bi-sa-mar te-zi-ir#',
                                             'u3 a-la#-ni#-ka te-zi-ir-ma#',
                                             'i-na an-ni-a-tim sza a-da-bu-[bu]',
                                             'a-na-ku mi-im-ma u2-ul e-le#-[i]',
                                             'sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]',
                                             'u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]',
                                             'u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]',
                                             'u3 lu ma-at ia-ma-ha-ad#{ki}',
                                             'u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]',
                                             'um#-[...]',
                                             'lu#-[...]',
                                             'a-[...]',
                                             'szum#-[...]',
                                             'a-na# [...]',
                                             'ma-li# [...]',
                                             'u3 u2-hu-ur# [...]',
                                             'a-su2-ur-ri [...]',
                                             'szu-zi-ba-an#-[ni ...]',
                                             'a-na [...]',
                                             'pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]',
                                             '{disz}a-bi-sa-mar u2-ul ma-ri u3 '
                                             'bi-ti a-na la bi-tu#-[tu-ur2-ma]',
                                             'bi-tum bi-it-ka u3 '
                                             '{disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]']}}
        self.assertEqual(cdli.catalog, goal)

    def test_print_catalog(self):
        """
        Tests _chunk_text.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        output = cdli.print_catalog(catalog_filter=['transliteration'])
        goal = print(output)
        self.assertEqual(output, goal)

    def test_string_tokenizer(self):
        """
        Tests string_tokenizer.
        """
        text = '20. u2-sza-bi-la-kum\n1. a-na ia-as2-ma-ah-{d}iszkur#\n' \
               '2. qi2-bi2-ma\n3. um-ma {d}utu-szi-{d}iszkur\n' \
               '4. a-bu-ka-a-ma\n5. t,up-pa-[ka] sza#-[tu]-sza-bi-lam esz-me' \
               '\n' '6. asz-szum t,e4#-em# {d}utu-illat-su2\n' \
               '7. u3 ia#-szu-ub-dingir sza a-na la i-[zu]-zi-im\n'
        output = TOKENIZER.string_tokenizer(text, include_blanks=False)
        goal = ['20. u2-sza-bi-la-kum',
                '1. a-na ia-as2-ma-ah-{d}iszkur',
                '2. qi2-bi2-ma',
                '3. um-ma {d}utu-szi-{d}iszkur',
                '4. a-bu-ka-a-ma',
                '5. t,up-pa-ka sza-tu-sza-bi-lam esz-me',
                '6. asz-szum t,e4-em {d}utu-illat-su2',
                '7. u3 ia-szu-ub-dingir sza a-na la i-zu-zi-im']
        self.assertEqual(output, goal)

    def test_line_tokenizer(self):
        """
        Tests line_tokenizer.
        """
        output = TOKENIZER.line_tokenizer(os.path.join(
            os.path.dirname(__file__), 'single_text.txt'))
        goal = ['1. a-na ia-ah-du-li-im',
                '2. qi2-bi2-ma',
                '3. um-ma a-bi-sa-mar-ma',
                '4. sa-li-ma-am e-pu-usz',
                '5. asz-szum mu-sze-zi-ba-am la i-szu',
                '6. sa-li-ma-am sza e-pu-szu',
                '7. u2-ul e-pu-usz sa-li-mu-um',
                '8. u2-ul sa-li-mu-um-ma',
                '$ rest broken',
                '@reverse']
        self.assertEqual(output[30:40], goal)

    def test_markdown_single_text(self):
        """
        Tests markdown_single_text.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        p_p = PrettyPrint()
        p_p.markdown_single_text(cdli.catalog, 'P254203')
        output = p_p.markdown_text
        goal = """ARM 01, 002
P254203
---
### metadata
    Primary publication: ARM 01, 002
	Author(s): Dossin, Georges
	Publication date: 1946
	Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0306
	Collection: National Museum of Syria, Damascus, Syria
	Museum no.: NMSD —
	Accession no.:
	Provenience: Mari (mod. Tell Hariri)
	Excavation no.:
	Period: Old Babylonian (ca. 1900-1600 BC)
	Dates referenced:
	Object type: tablet
	Remarks:
	Material: clay
	Language: Akkadian
	Genre: Letter
	Sub-genre:
	CDLI comments:
	Catalogue source: 20050104 cdliadmin
	ATF source: cdlistaff
	Translation:
	UCLA Library ARK: 21198/zz001rsp9f
	Composite no.:
	Seal no.:
	CDLI no.: P254203
### transliteration
    a-na ia-ah-du-[li-im]
	qi2-bi2-[ma]
	um-ma a-bi-sa-mar-[ma]
	asz-szum sza a-qa-bi-kum la ta-ha-asz2#
	a-na ma-ni-im lu-ud-bu-ub
	szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]
	szum-ma a-bi-sa-mar te-zi-ir#
	u3 a-la#-ni#-ka te-zi-ir-ma#
	i-na an-ni-a-tim sza a-da-bu-[bu]
	a-na-ku mi-im-ma u2-ul e-le#-[i]
	sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]
	u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]
	u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]
	u3 lu ma-at ia-ma-ha-ad#{ki}
	u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]
	um#-[...]
	lu#-[...]
	a-[...]
	szum#-[...]
	a-na# [...]
	ma-li# [...]
	u3 u2-hu-ur# [...]
	a-su2-ur-ri [...]
	szu-zi-ba-an#-[ni ...]
	a-na [...]
	pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]
	{disz}a-bi-sa-mar u2-ul ma-ri u3 bi-ti a-na la bi-tu#-[tu-ur2-ma]
	bi-tum bi-it-ka u3 {disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]
### normalization
    
### translation
      
"""
        self.assertEqual(output, goal)

    def test_html_print_file(self):
        """
        Tests html_print_file.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        p_p = PrettyPrint()
        p_p.html_print_file(cdli.catalog, os.path.join(os.path.dirname(__file__), 'html_file.html'))
        f_o = FileImport(os.path.join(os.path.dirname(__file__), 'html_file.html'))
        f_o.read_file()
        output = f_o.raw_file
        goal = \
"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ARM 01, 001</title>
</head>
<body><table cellpadding="10"; border="1">
<tr><th>
<h2>ARM 01, 001<br>P254202</h2>
</th><th>
<h3>transliteration</h3>
</th><th>
<h3>normalization</h3>
</th><th>
<h3>translation</h3>
</tr><tr><td>
Primary publication: ARM 01, 001<br>
Author(s): Dossin, Georges<br>
Publication date: 1946<br>
Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0305<br>
Collection: National Museum of Syria, Damascus, Syria<br>
Museum no.: NMSD —<br>
Accession no.:<br>
Provenience: Mari (mod. Tell Hariri)<br>
Excavation no.:<br>
Period: Old Babylonian (ca. 1900-1600 BC)<br>
Dates referenced:<br>
Object type: tablet<br>
Remarks:<br>
Material: clay<br>
Language: Akkadian<br>
Genre: Letter<br>
Sub-genre:<br>
CDLI comments:<br>
Catalogue source: 20050104 cdliadmin<br>
ATF source: cdlistaff<br>
Translation: Durand, Jean-Marie (fr); Guerra, Dylan M. (en)<br>
UCLA Library ARK: 21198/zz001rsp8x<br>
Composite no.:<br>
Seal no.:<br>
CDLI no.: P254202</td><td>
<p>a-na ia-ah-du-li-[im]<br>
qi2-bi2-[ma]<br>
um-ma a-bi-sa-mar#-[ma]<br>
sa-li-ma-am e-pu-[usz]<br>
asz-szum mu-sze-zi-ba-am# [la i-szu]<br>
[sa]-li#-ma-am sza e-[pu-szu]<br>
[u2-ul] e-pu-usz sa#-[li-mu-um]<br>
[u2-ul] sa-[li-mu-um-ma]<br>
isz#-tu mu#-[sze-zi-ba-am la i-szu]<br>
a-la-nu-ia sza la is,-s,a-ab#-[tu]<br>
i-na-an-na is,-s,a-ab-[tu]<br>
i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]<br>
ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]<br>
u3 ia-am-ha-ad[{ki}]<br>
a-la-nu an-nu-tum u2-ul ih-li-qu2#<br>
i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma<br>
ih-ta-al-qu2<br>
u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#<br>
u3 na-pa-asz2-ti u2-ba-li-it,<br>
pi2-qa-at ha-s,e-ra#-at<br>
asz-szum a-la-nu-ka<br>
u3 ma-ru-ka sza-al#-[mu]<br>
[a-na na-pa]-asz2#-ti-ia i-tu-ur
</td><td>
<p>
</td><td>
<font size='2'>

</font></td></tr>

</table>
<br>
</body>
</html><!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ARM 01, 002</title>
</head>
<body><table cellpadding="10"; border="1">
<tr><th>
<h2>ARM 01, 002<br>P254203</h2>
</th><th>
<h3>transliteration</h3>
</th><th>
<h3>normalization</h3>
</th><th>
<h3>translation</h3>
</tr><tr><td>
Primary publication: ARM 01, 002<br>
Author(s): Dossin, Georges<br>
Publication date: 1946<br>
Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0306<br>
Collection: National Museum of Syria, Damascus, Syria<br>
Museum no.: NMSD —<br>
Accession no.:<br>
Provenience: Mari (mod. Tell Hariri)<br>
Excavation no.:<br>
Period: Old Babylonian (ca. 1900-1600 BC)<br>
Dates referenced:<br>
Object type: tablet<br>
Remarks:<br>
Material: clay<br>
Language: Akkadian<br>
Genre: Letter<br>
Sub-genre:<br>
CDLI comments:<br>
Catalogue source: 20050104 cdliadmin<br>
ATF source: cdlistaff<br>
Translation:<br>
UCLA Library ARK: 21198/zz001rsp9f<br>
Composite no.:<br>
Seal no.:<br>
CDLI no.: P254203</td><td>
<p>a-na ia-ah-du-[li-im]<br>
qi2-bi2-[ma]<br>
um-ma a-bi-sa-mar-[ma]<br>
asz-szum sza a-qa-bi-kum la ta-ha-asz2#<br>
a-na ma-ni-im lu-ud-bu-ub<br>
szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]<br>
szum-ma a-bi-sa-mar te-zi-ir#<br>
u3 a-la#-ni#-ka te-zi-ir-ma#<br>
i-na an-ni-a-tim sza a-da-bu-[bu]<br>
a-na-ku mi-im-ma u2-ul e-le#-[i]<br>
sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]<br>
u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]<br>
u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]<br>
u3 lu ma-at ia-ma-ha-ad#{ki}<br>
u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]<br>
um#-[...]<br>
lu#-[...]<br>
a-[...]<br>
szum#-[...]<br>
a-na# [...]<br>
ma-li# [...]<br>
u3 u2-hu-ur# [...]<br>
a-su2-ur-ri [...]<br>
szu-zi-ba-an#-[ni ...]<br>
a-na [...]<br>
pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]<br>
{disz}a-bi-sa-mar u2-ul ma-ri u3 bi-ti a-na la bi-tu#-[tu-ur2-ma]<br>
bi-tum bi-it-ka u3 {disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]
</td><td>
<p>
</td><td>
<font size='2'>

</font></td></tr>

</table>
<br>
</body>
</html>"""
        self.assertEqual(output, goal)

    def test_html_print_single_text(self):
        """
        Tests html_print_single_text.
        """
        cdli = CDLICorpus()
        cdli.parse_file(SAMPLE_TEXT)
        p_p = PrettyPrint()
        p_p.html_print_single_text(cdli.catalog, 'P500444', os.path.join(os.path.dirname(__file__),
                                                                         'html_single_text.html'))
        f_o = FileImport(os.path.join(os.path.dirname(__file__), 'html_single_text.html'))
        f_o.read_file()
        output = f_o.raw_file
        goal = \
            """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NABU 2017/015</title>
</head>
<body><table cellpadding="10"; border="1">
<tr><th>
<h2>NABU 2017/015<br>P500444</h2>
</th><th>
<h3>transliteration</h3>
</th><th>
<h3>normalization</h3>
</th><th>
<h3>translation</h3>
</tr><tr><td>
</td><td>
<p>a-na {d}nin-urta<br>
be-li2 ra-bi-i<br>
be-li2-szu<br>
ka-dasz2-man-{d}en-lil2<br>
_lugal_ babila2{ki}<br>
_dumu_ ka-dasz2-man-tur2-gu _lugal_<br>
a-na szu-ru-uk _bala_-szu<br>
i-qi2-isz
</td><td>
<p>ana ninurta<br>
bēli rabî<br>
bēlišu<br>
kadašman-enlil<br>
šar bābili<br>
mār kadašman-turgu šarri<br>
ana šūruk palîšu<br>
iqīš
</td><td>
<font size='2'>
For Ninurta,<br>
the great lord,<br>
his lord,<br>
did Kadašman-Enlil,<br>
king of Babylon,<br>
son of Kadašman-Turgu, the king,<br>
for the lengthening of his reign<br>
offer (this seal).
</font></td></tr>

</table>
<br>
</body>
</html>"""
        self.assertEqual(output, goal)


if __name__ == '__main__':
    unittest.main()
