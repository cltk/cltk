'''
Various test cases for akkadian functions in the CLTK
'''

__author__ = ['M. Willis Monroe <willismonroe@gmail.com>',
              'Andrew Deloucas <adeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'

from cltk.phonology.akkadian.stress import StressFinder
from cltk.corpus.akkadian.cdli_corpus import CDLICorpus
from cltk.corpus.akkadian.pretty_print import PrettyPrint
from cltk.corpus.akkadian.file_importer import FileImport
from cltk.corpus.akkadian.tokenizer import Tokenizer

import unittest
import os

TOKENIZER = Tokenizer(preserve_damage=False)


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    '''
    An experiment to use Huehnergard's grammar and key to test the functions
    in the cltk.
    '''

    def test_lesson_1_exercise_d(self):
        nouns = ['abum', 'ālum', 'amtum', 'bēlum', 'ḫurāṣum', 'iltum', 'ilum', 'kaspum', 'mārtum', 'mārum', 'qaqqadum',
                 'ṣābum', 'šarratum', 'šarrum', 'wardum']
        stresser = StressFinder()
        stress = []
        for noun in nouns:
            stress.append(stresser.find_stress(noun))
        target = [['[a]', 'bum'], ['[ā]', 'lum'], ['[am]', 'tum'], ['[bē]', 'lum'], ['ḫu', '[rā]', 'ṣum'],
                  ['[il]', 'tum'], ['[i]', 'lum'], ['[kas]', 'pum'], ['[mār]', 'tum'], ['[mā]', 'rum'],
                  ['[qaq]', 'qa', 'dum'], ['[ṣā]', 'bum'], ['[šar]', 'ra', 'tum'], ['[šar]', 'rum'], ['[war]', 'dum']]

        self.assertEqual(stress, target)

    def test_lesson_1_exercise_e(self):
        nouns = ['mušallimum', 'išāl', 'idin', 'iddinūniššum', 'tabnianni', 'niqīaš', 'epēšum', 'kullumum', 'tabnû',
                 'iššiakkum', 'rēdûm', 'iqbi', 'paris', 'išmeānim', 'pete', 'šūṣû']
        stresser = StressFinder()
        stress = []
        for noun in nouns:
            stress.append(stresser.find_stress(noun))
        target = [['mu', '[šal]', 'li', 'mum'], ['i', '[šāl]'], ['[i]', 'din'], ['id', 'di', 'nū', '[niš]', 'šum'],
                  ['tab', 'ni', '[an]', 'ni'], ['ni', '[qī]', 'aš'], ['e', '[pē]', 'šum'], ['[kul]', 'lu', 'mum'],
                  ['tab', '[nû]'], ['iš', 'ši', '[ak]', 'kum'], ['rē', '[dûm]'], ['[iq]', 'bi'], ['[pa]', 'ris'],
                  ['iš', 'me', '[ā]', 'nim'], ['[pe]', 'te'], ['šū', '[ṣû]']]

        self.assertEqual(stress, target)

    def test_lesson_2_exercise_b(self):
        nouns = ['aššatum', 'bītum', 'emūqum', 'īnum', 'išdum', 'libbum', 'mutum', 'nārum', 'šīpātum', 'ṭuppum',
                 'ummum', 'uznum']
        stresser = StressFinder()
        stress = []
        for noun in nouns:
            stress.append(stresser.find_stress(noun))
        target = [['[aš]', 'ša', 'tum'], ['[bī]', 'tum'], ['e', '[mū]', 'qum'], ['[ī]', 'num'], ['[iš]', 'dum'],
                  ['[lib]', 'bum'], ['[mu]', 'tum'], ['[nā]', 'rum'], ['šī', '[pā]', 'tum'], ['[ṭup]', 'pum'],
                  ['[um]', 'mum'], ['[uz]', 'num']]

        self.assertEqual(stress, target)

class TestcasesfromGSOC(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_read_file(self):
        """
        Tests read_file.
        """
        text = os.path.join('..', 'Akkadian_test_texts', 'Akkadian.txt')
        cdli = FileImport(text)
        cdli.read_file()
        final = cdli.file_lines[3042:3054]
        goal = ['24. _{gesz}ma2_ dan-na-tam',
                '25. a-na be-el _{gesz}ma2_',
                '26. i-na-ad-di-in',
                '@law 236',
                '27. szum-ma a-wi-lum',
                '28. _{gesz}ma2_-szu',
                '29. a-na _ma2-lah5_',
                '30. a-na ig-ri-im',
                '31. id-di-in-ma',
                '32. _ma2-lah5_ i-gi-ma',
                '33. _{gesz}ma2_ ut,-t,e4-bi',
                '34. u3 lu uh2-ta-al-li-iq']
        self.assertEqual(final, goal)

    def test_file_catalog(self):
        """
        Tests file_catalog.
        """
        text = os.path.join('..', 'Akkadian_test_texts', 'Akkadian.txt')
        ex = os.path.split(text)
        final = os.listdir(ex[0])
        goal = ['Akkadian.txt', 'ARM1Akkadian.txt', 'cdli_corpus.txt',
                'html_file.html', 'html_single_text.html', 'single_text.txt',
                'tutorial_html.html', 'two_text.txt',
                'two_text_abnormalities.txt', 'two_text_no_metadata.txt']
        self.assertEqual(final, goal)

    def test_chunk_text(self):
        """
        Tests chunk_text.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        output = cdli._chunk_text(text_file, only_normalization=False)
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

    def test_chunk_text_norm(self):
        """
        Tests chunk_text normalized text finding and collating.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'cdli_corpus.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        output = cdli._chunk_text(text_file, only_normalization=True)[2]
        goal = ['&P254202 = ARM 01, 001',
                '#tr.ts: ana yaḫdu-lim',
                '#tr.ts: qibima',
                '#tr.ts: umma abi-samarma',
                '#tr.ts: salīmam ēpuš',
                '#tr.ts: aššum mušēzibam lā īšu',
                '#tr.ts: salīmam ša ēpušu',
                '#tr.ts: ul ēpuš salīmum',
                '#tr.ts: ul salīmumma',
                '#tr.ts: ištu mušēzibam lā īšu',
                '#tr.ts: alānūya ša lā iṣṣabtū',
                '#tr.ts: inanna iṣṣabtū',
                '#tr.ts: ina nekurti awīl ḫaššim',
                '#tr.ts: ursim awīl karkamis',
                '#tr.ts: u yamḫad',
                '#tr.ts: alānū annûtum ul iḫliqū',
                '#tr.ts: ina nekurti samsi-adduma',
                '#tr.ts: iḫtalqū',
                '#tr.ts: u alānū ša kīma uḫḫuru ušezib',
                '#tr.ts: u napaštī uballiṭ',
                '#tr.ts: pīqat ḫaṣerāt',
                '#tr.ts: aššum ālanūka',
                '#tr.ts: u mārūka šalmū',
                '#tr.ts: ana napaštiya itūr']
        self.assertEqual(output, goal)

    def test_find_cdli_number(self):
        """
        Tests find_cdli_number.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        output = cdli._find_cdli_number(text_file)
        goal = ['&P254202', '&P254203']
        self.assertEqual(output, goal)

    def test_find_edition(self):
        """
        Tests find_edition.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        output = cdli._find_edition(text_file)
        goal = ['ARM 01, 001', 'ARM 01, 002']
        self.assertEqual(output, goal)

    def test_find_metadata(self):
        """
        Tests find_metadata.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        output = cdli._find_metadata(text_file)
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
        Tests find_transliteration.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        output = cdli._find_transliteration(text_file)
        goal = [['&P254202 = ARM 01, 001',
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
                ['&P254203 = ARM 01, 002',
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

    def test_ingest(self):
        """
        Tests ingest.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'single_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        cdli._ingest(text_file)
        goal = {'cdli number': ['&P254202'],
                'text edition': ['ARM 01, 001'],
                'metadata': ['Primary publication: ARM 01, 001',
                             'Author(s): Dossin, Georges',
                             'Publication date: 1946',
                             'Secondary publication(s): Durand, '
                             'Jean-Marie, LAPO 16, 0305',
                             'Collection: National Museum of Syria, '
                             'Damascus, Syria',
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
                             'Translation: Durand, Jean-Marie (fr); '
                             'Guerra, Dylan M. (en)',
                             'UCLA Library ARK: 21198/zz001rsp8x',
                             'Composite no.:',
                             'Seal no.:',
                             'CDLI no.: P254202'],
                'transliteration': ['&P254202 = ARM 01, 001',
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
                                    "4'. i-na ne2-kur-ti _lu2_ "
                                    "ha-szi-[im{ki}]",
                                    "5'. ur-si-im{ki} _lu2"
                                    "_ ka-ar-ka#-[mi-is{ki}]",
                                    "6'. u3 ia-am-ha-ad[{ki}]",
                                    "7'. a-la-nu an-nu-tum u2-ul ih-li-qu2#",
                                    "8'. i-na ne2-kur-ti "
                                    "{disz}sa-am-si-{d}iszkur#-ma",
                                    "9'. ih-ta-al-qu2",
                                    "10'. u3 a-la-nu sza ki-ma "
                                    "u2-hu-ru u2-sze-zi-ib#",
                                    "11'. u3 na-pa-asz2-ti u2-ba-li-it,",
                                    "12'. pi2-qa-at ha-s,e-ra#-at",
                                    "13'. asz-szum a-la-nu-ka",
                                    "14'. u3 ma-ru-ka sza-al#-[mu]",
                                    "15'. [a-na na-pa]-asz2#-ti-ia i-tu-ur"]}
        self.assertEqual(cdli.text, goal)

    def test_ingest_text_file(self):
        """
        Tests ingest_text_file.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        cdli.ingest_text_file(text_file)
        goal = [{'cdli number': ['&P254202'],
                 'metadata': ['Primary publication: ARM 01, 001',
                              'Author(s): Dossin, Georges',
                              'Publication date: 1946',
                              'Secondary publication(s): Durand, '
                              'Jean-Marie, LAPO 16, 0305',
                              'Collection: National Museum of '
                              'Syria, Damascus, Syria',
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
                              'Translation: Durand, Jean-Marie (fr); '
                              'Guerra, Dylan M. (en)',
                              'UCLA Library ARK: 21198/zz001rsp8x',
                              'Composite no.:',
                              'Seal no.:',
                              'CDLI no.: P254202'],
                 'text edition': ['ARM 01, 001'],
                 'transliteration': ['&P254202 = ARM 01, 001',
                                     '#atf: lang akk',
                                     '@tablet',
                                     '@obverse',
                                     '1. a-na ia-ah-du-li-[im]',
                                     '2. qi2-bi2-[ma]',
                                     '3. um-ma a-bi-sa-mar#-[ma]',
                                     '4. sa-li-ma-am e-pu-[usz]',
                                     '5. asz-szum mu-sze-zi-ba-am# '
                                     '[la i-szu]',
                                     '6. [sa]-li#-ma-am sza e-[pu-szu]',
                                     '7. [u2-ul] e-pu-usz sa#-[li-mu-um]',
                                     '8. [u2-ul] sa-[li-mu-um-ma]',
                                     '$ rest broken',
                                     '@reverse',
                                     '$ beginning broken',
                                     "1'. isz#-tu mu#-[sze-zi-ba-am "
                                     "la i-szu]",
                                     "2'. a-la-nu-ia sza la is,-s,a-ab#-[tu]",
                                     "3'. i-na-an-na is,-s,a-ab-[tu]",
                                     "4'. i-na ne2-kur-ti _lu2_ "
                                     "ha-szi-[im{ki}]",
                                     "5'. ur-si-im{ki} _lu2_ "
                                     "ka-ar-ka#-[mi-is{ki}]",
                                     "6'. u3 ia-am-ha-ad[{ki}]",
                                     "7'. a-la-nu an-nu-tum u2-ul ih-li-qu2#",
                                     "8'. i-na ne2-kur-ti "
                                     "{disz}sa-am-si-{d}iszkur#-ma",
                                     "9'. ih-ta-al-qu2",
                                     "10'. u3 a-la-nu sza ki-ma "
                                     "u2-hu-ru u2-sze-zi-ib#",
                                     "11'. u3 na-pa-asz2-ti u2-ba-li-it,",
                                     "12'. pi2-qa-at ha-s,e-ra#-at",
                                     "13'. asz-szum a-la-nu-ka",
                                     "14'. u3 ma-ru-ka sza-al#-[mu]",
                                     "15'. [a-na na-pa]-asz2#-ti-ia "
                                     "i-tu-ur"]},
                {'cdli number': ['&P254203'],
                 'metadata': ['Primary publication: ARM 01, 002',
                              'Author(s): Dossin, Georges',
                              'Publication date: 1946',
                              'Secondary publication(s): Durand, '
                              'Jean-Marie, LAPO 16, 0306',
                              'Collection: National Museum of '
                              'Syria, Damascus, Syria',
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
                              'CDLI no.: P254203'],
                 'text edition': ['ARM 01, 002'],
                 'transliteration': ['&P254203 = ARM 01, 002',
                                     '#atf: lang akk',
                                     '@tablet',
                                     '@obverse',
                                     '1. a-na ia-ah-du-[li-im]',
                                     '2. qi2-bi2-[ma]',
                                     '3. um-ma a-bi-sa-mar-[ma]',
                                     '4. asz-szum sza a-qa-bi-kum '
                                     'la ta-ha-asz2#',
                                     '5. a-na ma-ni-im lu-ud-bu-ub',
                                     '6. szum-ma a-na?-<ku> a-na '
                                     'a-bi-ia la ad#-[bu-ub]',
                                     '7. szum-ma a-bi-sa-mar te-zi-ir#',
                                     '8. u3 a-la#-ni#-ka te-zi-ir-ma#',
                                     '9. i-na an-ni-a-tim sza a-da-bu-[bu]',
                                     '10. a-na-ku mi-im-ma u2-ul e-le#-[i]',
                                     '11. sza sza-ru-ti-ka u3 sza '
                                     'ra-pa#-[szi-ka e-pu-usz]',
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
                                     "11'. pi2-qa-at ta-qa-ab#-[bi "
                                     "um-ma at-ta-a-ma]",
                                     '@left',
                                     '1. {disz}a-bi-sa-mar u2-ul ma-ri '
                                     'u3 bi-ti a-na la '
                                     'bi-tu#-[tu-ur2-ma]',
                                     '2. bi-tum bi-it-ka u3 '
                                     '{disz}a-bi#-[sa]-mar# '
                                     'ma-ru-ka-[ma]']}]
        self.assertEqual(cdli.texts, goal)

    def test_table_of_contents(self):
        """
        Tests table_of_contents.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        cdli.ingest_text_file(text_file)
        output = cdli.table_of_contents()
        goal = ["edition: ['ARM 01, 001']; cdli number: ['&P254202']",
                "edition: ['ARM 01, 002']; cdli number: ['&P254203']"]
        self.assertEqual(output, goal)

    def test_print_text(self):
        """
        Tests print_text.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        cdli.ingest_text_file(text_file)
        output = cdli.call_text('&P254202')
        goal = ['&P254202 = ARM 01, 001',
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
        self.assertEqual(output, goal)

    def test_print_metadata(self):
        """
        Tests print_metadata.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        cdli.ingest_text_file(text_file)
        output = cdli.call_metadata('&P254202')
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
                'CDLI no.: P254202']
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
        text_file = os.path.join('..', 'Akkadian_test_texts', 'Akkadian.txt')
        output = TOKENIZER.line_tokenizer(text_file)
        goal = ['24. _{gesz}ma2_ dan-na-tam',
                '25. a-na be-el _{gesz}ma2_',
                '26. i-na-ad-di-in',
                '@law 236',
                '27. szum-ma a-wi-lum',
                '28. _{gesz}ma2_-szu',
                '29. a-na _ma2-lah5_',
                '30. a-na ig-ri-im',
                '31. id-di-in-ma',
                '32. _ma2-lah5_ i-gi-ma',
                '33. _{gesz}ma2_ ut,-t,e4-bi',
                '34. u3 lu uh2-ta-al-li-iq']
        self.assertEqual(output[3042:3054], goal)

    def test_markdown_single_text(self):
        """
        Tests markdown_single_text.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        cdli.ingest_text_file(text_file)
        p_p = PrettyPrint()
        p_p.markdown_single_text(cdli.texts, 'P254203')
        output = p_p.markdown_text
        goal = """ARM 01, 002
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
    &P254203 = ARM 01, 002
 	#atf: lang akk
 	@tablet
 	@obverse
 	1. a-na ia-ah-du-[li-im]
 	2. qi2-bi2-[ma]
 	3. um-ma a-bi-sa-mar-[ma]
 	4. asz-szum sza a-qa-bi-kum la ta-ha-asz2#
 	5. a-na ma-ni-im lu-ud-bu-ub
 	6. szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]
 	7. szum-ma a-bi-sa-mar te-zi-ir#
 	8. u3 a-la#-ni#-ka te-zi-ir-ma#
 	9. i-na an-ni-a-tim sza a-da-bu-[bu]
 	10. a-na-ku mi-im-ma u2-ul e-le#-[i]
 	11. sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]
 	12. u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]
 	13. u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]
 	14. u3 lu ma-at ia-ma-ha-ad#{ki}
 	15. u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]
 	$ rest broken
 	@reverse
 	$ beginning broken
 	1'. um#-[...]
 	2'. lu#-[...]
 	3'. a-[...]
 	4'. szum#-[...]
 	5'. a-na# [...]
 	6'. ma-li# [...]
 	7'. u3 u2-hu-ur# [...]
 	8'. a-su2-ur-ri [...]
 	9'. szu-zi-ba-an#-[ni ...]
 	10'. a-na [...]
 	11'. pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]
 	@left
 	1. {disz}a-bi-sa-mar u2-ul ma-ri u3 bi-ti a-na la bi-tu#-[tu-ur2-ma]
 	2. bi-tum bi-it-ka u3 {disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]  
"""
        self.assertEqual(output, goal)

    def test_html_print_file(self):
        """
        Tests html_print_file.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        cdli.ingest_text_file(text_file)
        destination = os.path.join('..', 'Akkadian_test_texts',
                                   'html_file.html')
        p_p = PrettyPrint()
        p_p.html_print_file(cdli.texts, destination)
        f_o = FileImport(destination)
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
<h2>ARM 01, 001</h2>
</th><th>
<h3>metadata</h3>
</th><th>
<h3>transliteration</h3>
</th></tr><tr><td></td><td>
<font size='2'>
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
CDLI no.: P254202
</font></td><td>
<p>&P254202 = ARM 01, 001<br>
#atf: lang akk<br>
@tablet<br>
@obverse<br>
1. a-na ia-ah-du-li-[im]<br>
2. qi2-bi2-[ma]<br>
3. um-ma a-bi-sa-mar#-[ma]<br>
4. sa-li-ma-am e-pu-[usz]<br>
5. asz-szum mu-sze-zi-ba-am# [la i-szu]<br>
6. [sa]-li#-ma-am sza e-[pu-szu]<br>
7. [u2-ul] e-pu-usz sa#-[li-mu-um]<br>
8. [u2-ul] sa-[li-mu-um-ma]<br>
$ rest broken<br>
@reverse<br>
$ beginning broken<br>
1'. isz#-tu mu#-[sze-zi-ba-am la i-szu]<br>
2'. a-la-nu-ia sza la is,-s,a-ab#-[tu]<br>
3'. i-na-an-na is,-s,a-ab-[tu]<br>
4'. i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]<br>
5'. ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]<br>
6'. u3 ia-am-ha-ad[{ki}]<br>
7'. a-la-nu an-nu-tum u2-ul ih-li-qu2#<br>
8'. i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma<br>
9'. ih-ta-al-qu2<br>
10'. u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#<br>
11'. u3 na-pa-asz2-ti u2-ba-li-it,<br>
12'. pi2-qa-at ha-s,e-ra#-at<br>
13'. asz-szum a-la-nu-ka<br>
14'. u3 ma-ru-ka sza-al#-[mu]<br>
15'. [a-na na-pa]-asz2#-ti-ia i-tu-ur
</td></tr></table>
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
<h2>ARM 01, 002</h2>
</th><th>
<h3>metadata</h3>
</th><th>
<h3>transliteration</h3>
</th></tr><tr><td></td><td>
<font size='2'>
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
CDLI no.: P254203
</font></td><td>
<p>&P254203 = ARM 01, 002<br>
#atf: lang akk<br>
@tablet<br>
@obverse<br>
1. a-na ia-ah-du-[li-im]<br>
2. qi2-bi2-[ma]<br>
3. um-ma a-bi-sa-mar-[ma]<br>
4. asz-szum sza a-qa-bi-kum la ta-ha-asz2#<br>
5. a-na ma-ni-im lu-ud-bu-ub<br>
6. szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]<br>
7. szum-ma a-bi-sa-mar te-zi-ir#<br>
8. u3 a-la#-ni#-ka te-zi-ir-ma#<br>
9. i-na an-ni-a-tim sza a-da-bu-[bu]<br>
10. a-na-ku mi-im-ma u2-ul e-le#-[i]<br>
11. sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]<br>
12. u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]<br>
13. u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]<br>
14. u3 lu ma-at ia-ma-ha-ad#{ki}<br>
15. u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]<br>
$ rest broken<br>
@reverse<br>
$ beginning broken<br>
1'. um#-[...]<br>
2'. lu#-[...]<br>
3'. a-[...]<br>
4'. szum#-[...]<br>
5'. a-na# [...]<br>
6'. ma-li# [...]<br>
7'. u3 u2-hu-ur# [...]<br>
8'. a-su2-ur-ri [...]<br>
9'. szu-zi-ba-an#-[ni ...]<br>
10'. a-na [...]<br>
11'. pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]<br>
@left<br>
1. {disz}a-bi-sa-mar u2-ul ma-ri u3 bi-ti a-na la bi-tu#-[tu-ur2-ma]<br>
2. bi-tum bi-it-ka u3 {disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]
</td></tr></table>
<br>
</body>
</html>"""
        self.maxDiff=None
        self.assertEqual(output, goal)

    def test_html_print_single_text(self):
        """
        Tests html_print_single_text.
        """
        path = os.path.join('..', 'Akkadian_test_texts', 'two_text.txt')
        destination = os.path.join('..', 'Akkadian_test_texts',
                                   'html_single_text.html')
        f_i = FileImport(path)
        f_i.read_file()
        text_file = f_i.file_lines
        cdli = CDLICorpus()
        cdli.ingest_text_file(text_file)
        p_p = PrettyPrint()
        p_p.html_print_single_text(cdli.texts, '&P254203', destination)
        f_o = FileImport(destination)
        f_o.read_file()
        output = f_o.raw_file
        goal = \
            """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ARM 01, 002</title>
</head>
<body><table cellpadding="10"; border="1">
<tr><th>
<h2>ARM 01, 002</h2>
</th><th>
<h3>metadata</h3>
</th><th>
<h3>transliteration</h3>
</th></tr><tr><td></td><td>
<font size='2'>
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
CDLI no.: P254203
</font></td><td>
<p>&P254203 = ARM 01, 002<br>
#atf: lang akk<br>
@tablet<br>
@obverse<br>
1. a-na ia-ah-du-[li-im]<br>
2. qi2-bi2-[ma]<br>
3. um-ma a-bi-sa-mar-[ma]<br>
4. asz-szum sza a-qa-bi-kum la ta-ha-asz2#<br>
5. a-na ma-ni-im lu-ud-bu-ub<br>
6. szum-ma a-na?-<ku> a-na a-bi-ia la ad#-[bu-ub]<br>
7. szum-ma a-bi-sa-mar te-zi-ir#<br>
8. u3 a-la#-ni#-ka te-zi-ir-ma#<br>
9. i-na an-ni-a-tim sza a-da-bu-[bu]<br>
10. a-na-ku mi-im-ma u2-ul e-le#-[i]<br>
11. sza sza-ru-ti-ka u3 sza ra-pa#-[szi-ka e-pu-usz]<br>
12. u3 lu-u2 sza sza-ru-ut-ka u2-ul te-le#-[i]<br>
13. u3 lu-u2 sza ra-pa-szi-ka [te-ep-pe2-esz]<br>
14. u3 lu ma-at ia-ma-ha-ad#{ki}<br>
15. u3# lu# _u4 8(disz)-kam_ isz-tu [i-na-an-na]<br>
$ rest broken<br>
@reverse<br>
$ beginning broken<br>
1'. um#-[...]<br>
2'. lu#-[...]<br>
3'. a-[...]<br>
4'. szum#-[...]<br>
5'. a-na# [...]<br>
6'. ma-li# [...]<br>
7'. u3 u2-hu-ur# [...]<br>
8'. a-su2-ur-ri [...]<br>
9'. szu-zi-ba-an#-[ni ...]<br>
10'. a-na [...]<br>
11'. pi2-qa-at ta-qa-ab#-[bi um-ma at-ta-a-ma]<br>
@left<br>
1. {disz}a-bi-sa-mar u2-ul ma-ri u3 bi-ti a-na la bi-tu#-[tu-ur2-ma]<br>
2. bi-tum bi-it-ka u3 {disz}a-bi#-[sa]-mar# ma-ru-ka-[ma]
</td></tr></table>
<br>
</body>
</html>"""
        self.assertEqual(output, goal)


if __name__ == '__main__':
    unittest.main()
