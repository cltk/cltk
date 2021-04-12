"""Test ``cltk.corpora``."""

import os
import unittest
from unicodedata import normalize
from unittest.mock import patch

from cltk.corpora.grc.tlg.tlgu import TLGU
from cltk.utils.file_operations import make_cltk_path

# import nltk
#
# from cltk.corpus.greek.alphabet import expand_iota_subscript
# from cltk.corpus.greek.alphabet import filter_non_greek
# from cltk.corpus.greek.beta_to_unicode import Replacer
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_female_authors
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_epithet_index
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_epithets
# from cltk.corpus.greek.tlg.parse_tlg_indices import select_authors_by_epithet
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_epithet_of_author
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_geo_index
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_geographies
# from cltk.corpus.greek.tlg.parse_tlg_indices import select_authors_by_geo
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_geo_of_author
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_lists
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_id_author
# from cltk.corpus.greek.tlg.parse_tlg_indices import select_id_by_name
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_works_by_id
# from cltk.corpus.greek.tlg.parse_tlg_indices import check_id
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_date_author
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_dates
# from cltk.corpus.greek.tlg.parse_tlg_indices import get_date_of_author
# from cltk.corpus.greek.tlg.parse_tlg_indices import _get_epoch
# from cltk.corpus.greek.tlg.parse_tlg_indices import _check_number
# from cltk.corpus.greek.tlg.parse_tlg_indices import _handle_splits
# from cltk.corpus.middle_english.alphabet import normalize_middle_english
# from cltk.corpus.old_norse import runes
# from cltk.corpus.utils.formatter import assemble_phi5_author_filepaths
# from cltk.corpus.utils.formatter import assemble_phi5_works_filepaths
# from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths
# from cltk.corpus.utils.formatter import assemble_tlg_works_filepaths
# from cltk.corpus.utils.formatter import phi5_plaintext_cleanup
# from cltk.corpus.utils.formatter import remove_non_ascii
# from cltk.corpus.utils.formatter import remove_non_latin
# from cltk.corpus.utils.formatter import tonos_oxia_converter
# from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
# from cltk.corpus.utils.formatter import cltk_normalize
# from cltk.corpus.utils.importer import CorpusImporter
# from cltk.corpus.utils.importer import CorpusImportError
# from cltk.corpus.sanskrit.itrans.itrans_transliterator import *
# from cltk.corpus.sanskrit.itrans.unicode_transliterate import *
# from cltk.corpus.sanskrit.itrans.langinfo import *
# from cltk.corpus.sanskrit.itrans.sinhala_transliterator import (
#     SinhalaDevanagariTransliterator as sdt,
# )
# from cltk.corpus.punjabi.numerifier import punToEnglish_number
# from cltk.corpus.punjabi.numerifier import englishToPun_number
# from cltk.corpus.egyptian.transliterate_mdc import mdc_unicode
# from cltk.corpus.aramaic.transliterate import square_to_imperial
# from cltk.corpus.utils.formatter import normalize_fr
# from cltk.corpus.swadesh import Swadesh
# from cltk.corpus.latin.latin_library_corpus_types import (
#     corpus_texts_by_type,
#     corpus_directories_by_type,
# )
# from cltk.utils.matrix_corpus_fun import distinct_words

__license__ = "MIT License. See LICENSE."

# DISTRIBUTED_CORPUS_PATH_REL = get_cltk_data_dir() + "/test_distributed_corpora.yaml"
# DISTRIBUTED_CORPUS_PATH = os.path.expanduser(DISTRIBUTED_CORPUS_PATH_REL)


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    @classmethod
    def setUpClass(self):
        pass
        # try:
        #     corpus_importer = CorpusImporter("latin")
        #     corpus_importer.import_corpus("latin_text_latin_library")
        #     corpus_importer.import_corpus("latin_text_perseus")
        #     corpus_importer = CorpusImporter("greek")
        #     corpus_importer.import_corpus("greek_text_perseus")
        #     corpus_importer.import_corpus("greek_text_tesserae")
        #     nltk.download("punkt")
        #     nltk.download("averaged_perceptron_tagger")
        # except:
        #     raise Exception("Failure to download test corpus")

    #
    # def test_greek_betacode_to_unicode(self):
    #     """Test converting Beta Code to Unicode.
    #     Note: assertEqual appears to not be correctly comparing certain
    #     characters (``ά`` and ``ί``, at least).
    #     """
    #     replacer = Replacer()
    #     # Generic test
    #     beta_1 = r"""O(/PWS OU)=N MH\ TAU)TO\ """
    #     unicode_1 = replacer.beta_code(beta_1)
    #     target_1 = "ὅπως οὖν μὴ ταὐτὸ "
    #     # Test for iota and diaeresis
    #     self.assertEqual(unicode_1, target_1)
    #     beta_2 = r"""*XALDAI+KH\N"""
    #     unicode_2 = replacer.beta_code(beta_2)
    #     target_2 = "Χαλδαϊκὴν"
    #     self.assertEqual(unicode_2, target_2)
    #     # Test for upsilon and diaeresis
    #     beta_3 = r"""PROU+POTETAGME/NWN"""
    #     unicode_3 = replacer.beta_code(beta_3)
    #     target_3 = "προϋποτεταγμένων"
    #     self.assertEqual(unicode_3, target_3)
    #     # Test for lowercase
    #     beta_4 = r"""proi+sxome/nwn"""
    #     unicode_4 = replacer.beta_code(beta_4)
    #     target_4 = "προϊσχομένων"
    #     self.assertEqual(unicode_4, target_4)

    def test_tlgu_init(self):
        """Test constructors of TLGU module for check, import, and install."""
        TLGU(interactive=False)
        header_file = make_cltk_path("grc/software/grc_software_tlgu/README.md")
        self.assertTrue(os.path.isfile(header_file))


#     def test_import_greek_software_tlgu(self):
#         """Test instantiating TLGU(). This will download and install
#         the software, if necessary.
#         """
#         corpus_importer = CorpusImporter("greek")
#         corpus_importer.import_corpus("greek_software_tlgu")
#         file_rel = os.path.join(
#             get_cltk_data_dir() + "/greek/software/greek_software_tlgu/README.md"
#         )
#         _file = os.path.expanduser(file_rel)
#         file_exists = os.path.isfile(_file)
#         self.assertTrue(file_exists)
#
#     def test_tlgu_convert(self):
#         """Test TLGU convert. This reads the file
#         ``tlgu_test_text_beta_code.txt``, which mimics a TLG file, and
#         converts it.
#         Note: assertEqual fails on some accented characters ('ή', 'ί').
#         """
#         in_test = os.path.abspath("cltk/tests/test_nlp/tlgu_test_text_beta_code.txt")
#         out_test = os.path.normpath(get_cltk_data_dir() + "/tlgu_test_text_unicode.txt")
#         tlgu = TLGU(testing=True)
#         tlgu.convert(in_test, out_test)
#         with open(out_test) as out_file:
#             new_text = out_file.read()
#         os.remove(out_test)
#         target = """
# βλλον δ' ἀλλλους χαλκρεσιν ἐγχεῃσιν.
# """
#         self.assertEqual(new_text, target)
#
#     def test_tlgu_convert_fail(self):
#         """Test the TLGU to fail when importing a corpus that doesn't exist."""
#         tlgu = TLGU(testing=True)
#         with self.assertRaises(AssertionError):
#             tlgu.convert(
#                 "~/Downloads/corpora/TLG_E/bad_path.txt", "~/Documents/thucydides.txt"
#             )
#
#     def test_tlgu_convert_corpus_fail(self):
#         """Test the TLGU to fail when trying to convert an unsupported corpus."""
#         tlgu = TLGU(testing=True)
#         with self.assertRaises(AssertionError):
#             tlgu.convert_corpus(corpus="bad_corpus")
#
#     def test_tlg_plaintext_cleanup(self):
#         """Test post-TLGU cleanup of text of Greek TLG text."""
#         dirty = """{ΑΘΗΝΑΙΟΥ ΝΑΥΚΡΑΤΙΤΟΥ ΔΕΙΠΝΟΣΟΦΙΣΤΩΝ} LATIN Ἀθήναιος (μὲν) ὁ τῆς 999 βίβλου 〈πατήρ〉: ποιεῖται δὲ τὸν λόγον πρὸς Τιμοκράτην."""  # pylint: disable=line-too-long
#         clean = tlg_plaintext_cleanup(dirty, rm_punctuation=True, rm_periods=False)
#         target = " Ἀθήναιος μὲν ὁ τῆς βίβλου πατήρ ποιεῖται δὲ τὸν λόγον πρὸς Τιμοκράτην."
#         self.assertEqual(clean, target)
#
#     def test_tlg_plaintext_cleanup_rm_periods(self):
#         """Test post-TLGU cleanup of text of Greek TLG text."""
#         dirty = """{ΑΘΗΝΑΙΟΥ ΝΑΥΚΡΑΤΙΤΟΥ ΔΕΙΠΝΟΣΟΦΙΣΤΩΝ} LATIN Ἀθήναιος (μὲν) ὁ τῆς 999 βίβλου 〈πατήρ〉: ποιεῖται δὲ τὸν λόγον πρὸς Τιμοκράτην."""  # pylint: disable=line-too-long
#         clean = tlg_plaintext_cleanup(dirty, rm_punctuation=True, rm_periods=True)
#         target = " Ἀθήναιος μὲν ὁ τῆς βίβλου πατήρ ποιεῖται δὲ τὸν λόγον πρὸς Τιμοκράτην"
#         self.assertEqual(clean, target)
#
#     def test_phi5_plaintext_cleanup(self):
#         """Test post-TLGU cleanup of text of Latin PHI5 text."""
#         dirty = """        {ODYSSIA}
#         {Liber I}
# Virum áge 999 mihi, Camena, (insece) versutum.
# Pater noster, Saturni filie . . .
# Mea puera, quid verbi ex tuo ore supera fugit?
# argenteo polubro, aureo eclutro. """
#         clean = phi5_plaintext_cleanup(dirty, rm_punctuation=True, rm_periods=False)
#         target = " Virum áge mihi Camena versutum. Pater noster Saturni filie . . . Mea puera quid verbi ex tuo ore supera fugit argenteo polubro aureo eclutro. "  # pylint: disable=line-too-long
#         self.assertEqual(clean, target)
#
#     def test_phi5_plaintext_cleanup_rm_periods(self):
#         """Test post-TLGU cleanup of text of Latin PHI5 text."""
#         dirty = """        {ODYSSIA}
#         {Liber I}
# Virum áge 999 mihi, Camena, (insece) versutum.
# Pater noster, Saturni filie . . .
# Mea puera, quid verbi ex tuo ore supera fugit?
# argenteo polubro, aureo eclutro. """
#         clean = phi5_plaintext_cleanup(dirty, rm_punctuation=True, rm_periods=True)
#         target = " Virum áge mihi Camena versutum Pater noster Saturni filie Mea puera quid verbi ex tuo ore supera fugit argenteo polubro aureo eclutro "  # pylint: disable=line-too-long
#         self.assertEqual(clean, target)
#
#     def test_phi5_plaintext_cleanup_rm_periods_bytes(self):
#         """Test post-TLGU cleanup of text of Latin PHI5 text."""
#         dirty = "\xcc\x81 Virum áge 999 mihi."
#         clean = phi5_plaintext_cleanup(dirty, rm_punctuation=True, rm_periods=True)
#         target = "Ì Virum áge mihi"
#         self.assertEqual(clean, target)
#
#     def test_cltk_normalize_compatible(self):
#         """Test Normalizing Text with compatibility True"""
#         s1 = "café"
#         s2 = "cafe\u0301"
#         normalized_text = cltk_normalize(s1, compatibility=True)
#         target = normalize("NFKC", s2)
#         self.assertEqual(normalized_text, target)
#
#     def test_cltk_normalize_noncompatible(self):
#         """Test Normalizing Text with compatibility False"""
#         s1 = "café"
#         s2 = "cafe\u0301"
#         normalized_text = cltk_normalize(s1, compatibility=False)
#         target = normalize("NFC", s2)
#         self.assertEqual(normalized_text, target)
#
#     def test_assemble_tlg_author(self):
#         """Test building absolute filepaths from TLG index."""
#         paths = assemble_tlg_author_filepaths()
#         self.assertEqual(len(paths), 1823)
#
#     def test_assemble_phi5_author(self):
#         """Test building absolute filepaths from TLG index."""
#         paths = assemble_phi5_author_filepaths()
#         self.assertEqual(len(paths), 362)
#
#     def test_assemble_tlg_works(self):
#         """"Test building absolute filepaths from TLG works index."""
#         paths = assemble_tlg_works_filepaths()
#         self.assertEqual(len(paths), 6625)
#
#     def test_assemble_phi5_works(self):
#         """"Test building absolute filepaths from PHI5 works index."""
#         paths = assemble_phi5_works_filepaths()
#         self.assertEqual(len(paths), 836)
#
#     def test_corpora_import_list_greek(self):
#         """Test listing of available corpora."""
#         corpus_importer = CorpusImporter("greek")
#         available_corpora = corpus_importer.list_corpora
#         self.assertTrue(available_corpora)
#
#     def test_corpora_import_list_latin(self):
#         """Test listing of available corpora."""
#         corpus_importer = CorpusImporter("latin")
#         available_corpora = corpus_importer.list_corpora
#         self.assertTrue(available_corpora)
#
#     def test_tonos_oxia_converter(self):
#         """Test function converting tonos to oxia accent."""
#         char_tonos = "ά"  # with tonos, for Modern Greek
#         char_oxia = "ά"  # with oxia, for Ancient Greek
#         corrected = tonos_oxia_converter(char_tonos)
#         self.assertEqual(char_oxia, corrected)
#
#     def test_tonos_oxia_converter_reverse(self):
#         """Test function converting tonos to oxia accent."""
#         char_tonos = "ά"  # with tonos, for Modern Greek
#         char_oxia = "ά"  # with oxia, for Ancient Greek
#         corrected = tonos_oxia_converter(char_oxia, reverse=True)
#         self.assertEqual(char_tonos, corrected)
#
#     def test_remove_non_ascii(self):
#         """Test removing all non-ascii characters from a string."""
#         non_ascii_str = "Ascii and some non-ascii: θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν"  # pylint: disable=line-too-long
#         ascii_str = remove_non_ascii(non_ascii_str)
#         valid = "Ascii and some non-ascii:     "
#         self.assertEqual(ascii_str, valid)
#
#     def test_remove_non_latin(self):
#         """Test removing all non-Latin characters from a string."""
#         latin_str = "(1) Dices ἐστιν ἐμός pulchrum esse inimicos ulcisci."  # pylint: disable=line-too-long
#         non_latin_str = remove_non_latin(latin_str)
#         valid = " Dices   pulchrum esse inimicos ulcisci"
#         self.assertEqual(non_latin_str, valid)
#
#     def test_remove_non_latin_opt(self):
#         """Test removing all non-Latin characters from a string, with
#         `also_keep` parameter.
#         """
#         latin_str = "(1) Dices ἐστιν ἐμός pulchrum esse inimicos ulcisci."  # pylint: disable=line-too-long
#         non_latin_str = remove_non_latin(latin_str, also_keep=[".", ","])
#         valid = " Dices   pulchrum esse inimicos ulcisci."
#         self.assertEqual(non_latin_str, valid)

#     def test_import_lat_text_lat_lib(self):
#         """Test cloning the Latin Library text corpus."""
#         corpus_importer = CorpusImporter("latin")
#         corpus_importer.import_corpus("latin_text_latin_library")
#         file_rel = os.path.join(
#             get_cltk_data_dir() + "/latin/text/latin_text_latin_library/README.md"
#         )
#         _file = os.path.expanduser(file_rel)
#         file_exists = os.path.isfile(_file)
#         self.assertTrue(file_exists)
#
#     def test_import_latin_models_cltk(self):
#         """Test cloning the CLTK Latin models."""
#         corpus_importer = CorpusImporter("latin")
#         corpus_importer.import_corpus("latin_models_cltk")
#         file_rel = os.path.join(
#             get_cltk_data_dir() + "/latin/model/latin_models_cltk/README.md"
#         )
#         _file = os.path.expanduser(file_rel)
#         file_exists = os.path.isfile(_file)
#         self.assertTrue(file_exists)
#
#     def test_import_greek_models_cltk(self):
#         """Test pull (not clone) the CLTK Greek models. Import was run in
#         ``setUp()``.
#         """
#         corpus_importer = CorpusImporter("greek")
#         corpus_importer.import_corpus("greek_models_cltk")
#         file_rel = os.path.join(
#             get_cltk_data_dir() + "/greek/model/greek_models_cltk/README.md"
#         )
#         _file = os.path.expanduser(file_rel)
#         file_exists = os.path.isfile(_file)
#         self.assertTrue(file_exists)
#
#     def test_show_corpora_bad_lang(self):
#         """Test failure of importer upon selecting unsupported language."""
#         with self.assertRaises(CorpusImportError):
#             CorpusImporter("bad_lang")
#
#     def test_import_nonexistant_corpus(self):
#         """Test that creating a CorpusImporter for a non existent lang
#            fails smoothly
#         """
#         with self.assertRaises(CorpusImportError):
#             corpus_importer = CorpusImporter("greek")
#             corpus_importer.import_corpus("euclids_book_of_recipes")
#
#     def test_import_latin_text_antique_digiliblt(self):
#         """Test cloning the Antique Latin from digilibLT."""
#         corpus_importer = CorpusImporter("latin")
#         corpus_importer.import_corpus("latin_text_antique_digiliblt")
#         file_rel = os.path.join(
#             get_cltk_data_dir() + "/latin/text/latin_text_antique_digiliblt/README.md"
#         )
#         _file = os.path.expanduser(file_rel)
#         file_exists = os.path.isfile(_file)
#         self.assertTrue(file_exists)
#
#     def test_get_female_authors(self):
#         """Test function to parse TLG female authors list."""
#         authors = get_female_authors()
#         authors = sorted(authors)[:3]
#         self.assertEqual(authors, ["0009", "0051", "0054"])
#
#     def test_get_epithet_index(self):
#         """Test get_epithet_index()."""
#         ind = get_epithet_index()
#         self.assertEqual(type(ind), dict)
#
#     def test_get_epithets(self):
#         """Test get_epithets()."""
#         epithets = get_epithets()
#         self.assertEqual(epithets[:2], ["Alchemistae", "Apologetici"])
#
#     def test_select_authors_by_epithet(self):
#         """Test select_authors_by_epithet()."""
#         authors = select_authors_by_epithet("Apologetici")
#         self.assertEqual(len(authors), 9)
#
#     def test_get_epithet_of_author(self):
#         """Test get_epithet_of_author()."""
#         epithet = get_epithet_of_author("0016")
#         self.assertEqual(epithet, "Historici/-ae")
#
#     def test_get_geo_index(self):
#         """Test get_geo_index()."""
#         index = get_geo_index()
#         self.assertEqual(type(index), dict)
#
#     def test_get_geographies(self):
#         """Test get_geographies()."""
#         geos = get_geographies()
#         self.assertEqual(type(geos), list)
#
#     def test_select_authors_by_geo(self):
#         """Test select_authors_by_geo()."""
#         authors = select_authors_by_geo("Athenae")
#         self.assertEqual(len(authors), 113)
#
#     def test_get_geo_of_author(self):
#         """Test get_geo_of_author()."""
#         geo = get_geo_of_author("0008")
#         self.assertEqual(geo, "Naucratis")
#
#     def test_get_lists(self):
#         """Test get_lists()."""
#         index = get_lists()
#         self.assertEqual(type(index), dict)
#
#     def test_get_id_author(self):
#         """Test get_id_author()."""
#         self.assertEqual(type(get_id_author()), dict)
#
#     def test_select_id_by_name(self):
#         """Test select_id_by_name()."""
#         matches = select_id_by_name("hom")
#         self.assertEqual(len(matches), 11)
#
#     def test_get_works_by_id(self):
#         """Test get_works_by_id()."""
#         works = get_works_by_id("0007")
#         self.assertEqual(len(works), 147)
#
#     def test_check_id(self):
#         """Test check_id"""
#         author = check_id("0557")
#         valid = "Epictetus Phil."
#         self.assertEqual(author, valid)
#
#     # #! Figure out why this test stopped working (actual function runs fine)
#     # def test_get_date_author(self):
#     #     """Test get_date_author()."""
#     #     dates = get_date_author()
#     #     self.assertEqual(type(dates), dict)
#
#     # #! Figure out why this test stopped working (actual function runs fine)
#     # def test_get_dates(self):
#     #     """Test get_dates()."""
#     #     dates = get_dates()
#     #     self.assertEqual(type(dates), list)
#     #     self.assertEqual(len(dates), 183)
#
#     # #! Figure out why this test stopped working (actual function runs fine)
#     # def test_get_date_of_author(self):
#     #     """Test get_date_of_author()."""
#     #     self.assertEqual(get_date_of_author('1747'), '1 B.C./A.D. 1')
#     #     self.assertEqual(get_date_of_author('1143'), '2-1 B.C.')
#     #     self.assertEqual(get_date_of_author('0295'), 'Varia')
#     #     self.assertEqual(get_date_of_author('4304'), 'a. A.D. 10')
#     #     self.assertIsNone(get_date_of_author('123456'))
#
#     def test_get_epoch(self):
#         """Test _get_epoch()."""
#         self.assertEqual(_get_epoch("A.D. 9-10"), "ad")
#         self.assertEqual(_get_epoch("p. A.D. 2"), "ad")
#         self.assertIsNone(_get_epoch("a. A.D. 2"))
#         self.assertEqual(_get_epoch("3 B.C."), "bc")
#         self.assertIsNone(_get_epoch("p. 7 B.C."))
#         self.assertEqual(_get_epoch("a. 1 B.C."), "bc")
#         self.assertEqual(_get_epoch("a. 1 B.C.?"), "bc")
#
#     def test_check_number(self):
#         """Test _check_number()."""
#         self.assertTrue(_check_number("5"))
#         self.assertTrue(_check_number("5?"))
#         self.assertFalse(_check_number("A.D. 5"))
#         self.assertFalse(_check_number("A.D. 5?"))
#         self.assertFalse(_check_number("p. 4 B.C."))
#
#     def test_handle_splits(self):
#         """Test _handle_splits()."""
#         _dict = {
#             "start_raw": "A.D. 9",
#             "start_epoch": "ad",
#             "stop_epoch": "ad",
#             "stop_raw": "A.D. 10",
#         }
#         self.assertEqual(_handle_splits("A.D. 9-10"), _dict)
#         _dict = {
#             "start_raw": "A.D. 1?",
#             "start_epoch": "ad",
#             "stop_epoch": "ad",
#             "stop_raw": "A.D. 6",
#         }
#         self.assertEqual(_handle_splits("A.D. 1?-6"), _dict)
#         _dict = {
#             "stop_raw": "p. A.D. 2",
#             "start_raw": "a. 4 B.C.",
#             "stop_epoch": "ad",
#             "start_epoch": "bc",
#         }
#         self.assertEqual(_handle_splits("a. 4 B.C.-p. A.D. 2"), _dict)
#         _dict = {
#             "stop_raw": "A.D. 2?",
#             "start_raw": "A.D. 2?",
#             "stop_epoch": "ad",
#             "start_epoch": "ad",
#         }
#         self.assertEqual(_handle_splits("A.D. 2?"), _dict)
#         _dict = {
#             "stop_raw": "1 B.C.?",
#             "start_raw": "2 B.C.?",
#             "stop_epoch": "bc",
#             "start_epoch": "bc",
#         }
#         self.assertEqual(_handle_splits("2/1 B.C.?"), _dict)
#
#     def test_punjabi_to_english_number_conversion(self):
#         str_test = "੧੨੩੪੫੬੭੮੯੦"
#         self.assertEqual(1234567890, punToEnglish_number(str_test))
#
#     def test_englishToPun_number(self):
#         str_test = "੧੨੩੪੫੬੭੮੯੦"
#         self.assertEqual(str_test, englishToPun_number(1234567890))
#
#     def test_english_to_punjabi_number_conversion(self):
#         """Test English to Punjabi number conversion."""
#         str_test = "੧੨੩੪੫੬੭੮੯੦"
#         self.assertEqual(str_test, englishToPun_number(1234567890))
#
#     def make_distributed_corpora_testing_file(self):
#         """Setup for some cloning tests, make file at
#         get_cltk_data_dir() + '/test_distributed_corpora.yaml'.
#         """
#         # ! Don't format this literal string, must be YAML-ish
#         yaml_str_to_write = """example_distributed_latin_corpus:
#         git_remote: git@github.com:kylepjohnson/latin_corpus_newton_example.git
#         language: latin
#         type: text
#
# example_distributed_fake_language_corpus:
#         origin: git@github.com:kylepjohnson/doesntexistyet.git
#         language: fake_language
#         type: treebank
#     """
#         cltk_data_dir = get_cltk_data_dir()
#         if not os.path.isdir(cltk_data_dir):
#             os.mkdir(cltk_data_dir)
#         with open(DISTRIBUTED_CORPUS_PATH, "w") as file_open:
#             file_open.write(yaml_str_to_write)
#
#     def remove_distributed_corpora_testing_file(self):
#         """Remove ~/cltk_data/test_distributed_corpora.yaml."""
#         os.remove(DISTRIBUTED_CORPUS_PATH)
#
#     def test_corpus_importer_variables_no_user_but_in_core(self):
#         """Test function which checks for presence of
#         ~/cltk_data/distributed_corpora.yaml. Look for a language
#         not in core repos but not in user-defined.
#         """
#         self.make_distributed_corpora_testing_file()
#         corpus_importer = CorpusImporter("sanskrit", testing=True)
#         self.assertIn("sanskrit_models_cltk", corpus_importer.list_corpora)
#         self.remove_distributed_corpora_testing_file()
#
#     def test_corpus_importer_variables_user_but_not_core(self):
#         """Test function which checks for presence of
#         `~/cltk_data/distributed_corpora.yaml`. Look for a language
#         not in the core but in the user's custom file.
#         """
#         self.make_distributed_corpora_testing_file()
#         corpus_importer = CorpusImporter("fake_language", testing=True)
#         corpus_name = corpus_importer.list_corpora
#         target_name = "example_distributed_fake_language_corpus"
#         self.assertEqual(corpus_name[0], target_name)
#         self.remove_distributed_corpora_testing_file()
#
#     def test_corpus_importer_variables_no_user_but_yes_core(self):
#         """Test function which checks for presence of
#         `~/cltk_data/distributed_corpora.yaml`. Look for a language
#         in the core but not in the user's custom file.
#         """
#         self.make_distributed_corpora_testing_file()
#         corpus_importer = CorpusImporter("pali", testing=True)
#         corpora = corpus_importer.list_corpora
#         self.assertIn("pali_text_ptr_tipitaka", corpora)
#         self.remove_distributed_corpora_testing_file()
#
#     def test_corpus_importer_variables_no_user_no_core(self):
#         """Test function which checks for presence of
#         `~/cltk_data/distributed_corpora.yaml`. Look for a language
#         neither in the core or in the user's custom file.
#         """
#         self.make_distributed_corpora_testing_file()
#         with self.assertRaises(CorpusImportError):
#             CorpusImporter("fake_language_nowhere")
#         self.remove_distributed_corpora_testing_file()
#
#     #
#     # def test_import_punjabi_punjabi_text_gurban(self):
#     #     pun_import = CorpusImporter('punjabi')
#     #     corpora_list = pun_import.list_corpora
#     #     self.assertTrue('punjabi_text_gurban' in corpora_list)
#     #     pun_import.import_corpus('punjabi_text_gurban')
#     #     file_path = os.path.join(get_cltk_data_dir() + '/punjabi/text/punjabi_text_gurban/README.md')
#     #     _file = os.path.expanduser(file_path)
#     #     self.assertTrue(os.path.isfile(_file))
#     #
#     # Ancient Egyptian Stuff -----------------------------
#
#     def test_egyptian_transliterate_mdc_to_unicode_q_kopf_True(self):
#         """
#         test to transliterate mdc to unicode
#         for ancient egyptian texts.
#         q_kopf option True
#         """
#         #
#         mdc_string = """ink Smsw Sms nb=f bAk n ipt nswt
#         irt pat wrt <Hswt> Hmt [nswt] snwsrt m Xnm-swt
#         sAt nswt imn-m-HAt m
#         qA-nfrw nfrw nbt imAx"""
#         #
#         test_result_string = mdc_unicode(mdc_string)
#         #
#         comparison_string = """i҆nk šmsw šms nb⸗f bꜣk n i҆pt nswt
#         i҆rt pꜥt wrt 〈ḥswt〉 ḥmt [nswt] snwsrt m ẖnm-swt
#         sꜣt nswt i҆mn-m-ḥꜣt m
#         qꜣ-nfrw nfrw nbt i҆mꜣḫ"""
#         #
#         self.assertEqual(test_result_string, comparison_string)
#
#     def test_egyptian_transliterate_mdc_to_unicode_q_kopf_False(self):
#         """
#         test to transliterate mdc to unicode
#         for ancient egyptian texts.
#         q_kopf option False
#         """
#         #
#         mdc_string = """ink Smsw Sms nb=f bAk n ipt nswt
#         irt pat wrt <Hswt> Hmt [nswt] snwsrt m Xnm-swt
#         sAt nswt imn-m-HAt m
#         qA-nfrw nfrw nbt imAx"""
#         #
#         test_result_string = mdc_unicode(mdc_string, q_kopf=False)
#         #
#         comparison_string = """i҆nk šmsw šms nb⸗f bꜣk n i҆pt nswt
#         i҆rt pꜥt wrt 〈ḥswt〉 ḥmt [nswt] snwsrt m ẖnm-swt
#         sꜣt nswt i҆mn-m-ḥꜣt m
#         ḳꜣ-nfrw nfrw nbt i҆mꜣḫ"""
#         #
#         self.assertEqual(test_result_string, comparison_string)
#
#     def test_square_to_imperial_(self):
#         "test square_to_imperial function"
#         square_script = "פדי בר דג[נ]מלך לאחא בר חפיו נתנת לך"
#         imperial_version = "𐡐𐡃𐡉 𐡁𐡓 𐡃𐡂[𐡍]𐡌𐡋𐡊 𐡋𐡀𐡇𐡀 𐡁𐡓 𐡇𐡐𐡉𐡅 𐡍𐡕𐡍𐡕 𐡋𐡊"
#         result = square_to_imperial(square_script)
#         self.assertEqual(imperial_version, result)
#
#     def test_expand_iota_subscript(self):
#         """Test subscript expander."""
#         unexpanded = "εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ"
#         expanded = expand_iota_subscript(unexpanded)
#         target = "εἰ δὲ καὶ τῶΙ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῶΙ"
#         self.assertEqual(expanded, target)
#
#     def test_expand_iota_subscript_lower(self):
#         """Test subscript expander."""
#         unexpanded = "εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ"
#         expanded = expand_iota_subscript(unexpanded, lowercase=True)
#         target = "εἰ δὲ καὶ τῶι ἡγεμόνι πιστεύσομεν ὃν ἂν κῦρος διδῶι"
#         self.assertEqual(expanded, target)
#
#     #
#     def test_filter_non_greek(self):
#         """
#         Test filter non greek characters in a mixed string.
#         """
#         test_input_string = (
#             "[Ἑκα]τόμανδ[ρος Αἰσχ]ρίωνος ⋮ Ἀρ[ιστείδη..c5..]"  # PH247029, line 2
#         )
#         comparison_string = "Ἑκατμανδρος Αἰσχρωνος  Ἀριστεδη"
#         test_result_string = filter_non_greek(test_input_string)
#         #
#         self.assertEqual(test_result_string, comparison_string)
#
#     def test_normalize(self):
#         """
#         Test french normalizer
#         """
#         text = "viw"
#         normalized = normalize_fr(text)
#         target = ["vieux"]
#         self.assertEqual(normalized, target)
#
#     def test_normalize_middle_english(self):
#         """Tests ME normalizer"""
#         in_test = "'Madame,' quod he, 'reule me As ȝ,e ly:k?eþ best.'"
#         target = "'madame' quod he 'reule me as ye lyketh best'"
#         test = normalize_middle_english(in_test)
#         self.assertEqual(target, test)
#
#
# class TestUnicode(unittest.TestCase):
#     "Test py23char"
#
#     def test_py23char(self):
#         self.assertEqual(py23char(0x92D), "भ")
#         self.assertFalse(py23char(0x93D) == "भ")
#
#
# class TestTransliteration(unittest.TestCase):
#     "Test the transliteration in corpus.sanskrit"
#
#     def test_Indicization(
#         self,
#     ):  # Test ItransTransliterator - Convert from Itrans to Devanagari
#         x = ItransTransliterator.from_itrans("pitL^In", "hi")
#         y = ItransTransliterator.from_itrans("yogazcittavRttinirodhaH", "hi")
#         z = ItransTransliterator.from_itrans("yogazcittavRttinirodhaH", "badVar")
#         self.assertEqual(x, "पितॣन्")
#         self.assertEqual(y, "योगश्चित्तव्ऱ्त्तिनिरोधः")
#         self.assertEqual(z, "yogazcittavRttinirodhaH")
#
#     def test_ScriptConversion(
#         self,
#     ):  # Test UnicodeIndicTransliterator - Convert between various scripts
#         x = UnicodeIndicTransliterator.transliterate("राजस्थान", "hi", "pa")
#         self.assertEqual(x, "ਰਾਜਸ੍ਥਾਨ")
#         y = UnicodeIndicTransliterator.transliterate("සිංහල අක්ෂර මාලාව", "si", "hi")
#         self.assertEqual(y, "सिंहल अक्षर मालाव")
#         z = UnicodeIndicTransliterator.transliterate("सिंहल अक्षर मालाव", "hi", "si")
#         self.assertEqual(z, "සිංහල අක්ෂර මාලාව")
#         t = UnicodeIndicTransliterator.transliterate("தமிழ் அரிச்சுவடி", "ta", "hi")
#         self.assertEqual(t, "तमिऴ् अरिच्चुवटि")
#         h = UnicodeIndicTransliterator.transliterate("तमिऴ् अरिच्चुवटि", "hi", "ta")
#         self.assertEqual(h, "தமிழ் அரிச்சுவடி")
#
#     def test_Romanization(self):
#         x = ItransTransliterator.to_itrans("राजस्थान", "hi")
#         self.assertTrue(x == "rAjasthAna" or x == "raajasthaana")
#         x = ItransTransliterator.to_itrans("राजस्थान", "asdasd")
#         self.assertEqual(x, "राजस्थान")
#         ml = ItransTransliterator.to_itrans("മല", "ml")
#         self.assertEqual(ml, "mala")
#
#     def test_SinhalaDevanagariTransliterator(self):
#         sin = sdt.devanagari_to_sinhala("राजस्थान")
#         self.assertEqual(sin, "රාජස්ථාන")
#         dev = sdt.sinhala_to_devanagari("රාජස්ථාන")
#         self.assertEqual(dev, "राजस्थान")
#
#
# class TestScriptInformation(unittest.TestCase):
#     def test_IsVowel(self):
#         self.assertFalse(is_vowel("क", "hi"))
#         self.assertTrue(is_vowel("अ", "hi"))
#
#     def test_IsConsonant(self):
#         self.assertTrue(is_consonant("क", "hi"))
#         self.assertFalse(is_consonant("अ", "hi"))
#
#     def test_IsVelar(self):
#         self.assertTrue(is_velar("क", "hi"))
#         self.assertFalse(is_velar("अ", "hi"))
#
#     def test_IsPalatal(self):
#         self.assertTrue(is_palatal("च", "hi"))
#         self.assertFalse(is_palatal("त", "hi"))
#
#     def test_IsAspirated(self):
#         self.assertTrue(is_aspirated("छ", "hi"))
#         self.assertFalse(is_aspirated("क", "hi"))
#
#     def test_IsUnvoiced(self):
#         self.assertTrue(is_unvoiced("ट", "hi"))
#         self.assertFalse(is_unvoiced("ग", "hi"))
#
#     def test_IsNasal(self):
#         self.assertTrue(is_nasal("ण", "hi"))
#         self.assertFalse(is_nasal("ड", "hi"))
#
#     def test_IsVowelSign(self):
#         self.assertTrue(is_vowel_sign("ा", "hi"))
#
#     def test_IsNukta(self):
#         self.assertTrue(is_nukta("़", "hi"))
#
#     def test_IsAum(self):
#         self.assertTrue(is_aum("ॐ", "hi"))
#
#     def test_IsHalanta(self):
#         self.assertTrue(is_halanta("्", "hi"))
#
#     def test_IsRetroflex(self):
#         self.assertTrue(is_retroflex("ट", "hi"))
#
#     def test_IsDental(self):
#         self.assertTrue(is_dental("त", "hi"))
#
#     def test_IsLabial(self):
#         self.assertTrue(is_labial("प", "hi"))
#
#     def test_IsVoiced(self):
#         self.assertTrue(is_voiced("ग", "hi"))
#
#     def test_IsUnAspirated(self):
#         self.assertTrue(is_unaspirated("ज", "hi"))
#
#     def test_IsFricative(self):
#         self.assertTrue(is_fricative("श", "hi"))
#
#     def test_IsApproximant(self):
#         self.assertTrue(is_approximant("य", "hi"))
#
#     def test_IsNumber(self):
#         self.assertTrue(is_number("२", "hi"))
#
#     def test_offset_to_char(self):
#         self.assertEqual(offset_to_char(0x021, "hi"), "ड")
#
#     def test_in_coordinated_range(self):
#         self.assertTrue(in_coordinated_range(0x6E))
#
#     def test_is_indiclang_char(self):
#         self.assertTrue(is_indiclang_char("क", "hi"))
#
#     def test_swadesh_greek(self):
#         swadesh = Swadesh("gr")
#         first_word = "ἐγώ"
#         match = swadesh.words()[0]
#         self.assertEqual(first_word, match)
#
#     def test_swadesh_latin(self):
#         swadesh = Swadesh("la")
#         first_word = "ego"
#         match = swadesh.words()[0]
#         self.assertEqual(first_word, match)
#
#     def test_swadesh_tocharianB(self):
#         swadesh = Swadesh("txb")
#         first_word = "ñäś"
#         match = swadesh.words()[0]
#         self.assertEqual(first_word, match)
#
#     def test_swadesh_old_portuguese(self):
#         swadesh = Swadesh("pt_old")
#         first_word = "eu"
#         match = swadesh.words()[0]
#         self.assertEqual(first_word, match)
#
#     def test_swadesh_sanskrit(self):
#         swadesh = Swadesh("sa")
#         first_word = "अहम्"
#         match = swadesh.words()[0]
#         self.assertEqual(first_word, match)
#
#     def test_swadesh_hindi(self):
#         swadesh = Swadesh("hi")
#         first_word = "मैं"
#         match = swadesh.words()[0]
#         self.assertEqual(first_word, match)
#
#     def test_swadesh_old_english(self):
#         swadesh = Swadesh("eng_old")
#         first_word = "ic, iċċ, ih"
#         match = swadesh.words()[0]
#         self.assertEqual(first_word, match)
#
#     def test_swadesh_old_norse(self):
#         swadesh = Swadesh("old_norse")
#         first_word = "ek"
#         match = swadesh.words()[0]
#         self.assertEqual(first_word, match)
#
#     def test_swadesh_arabic(self):
#         swadesh = Swadesh("ar")
#         first_word = "أنا"
#         match = swadesh.words()[0]
#         self.assertEqual(first_word, match)
#
#
# class TestRunes(unittest.TestCase):
#     def test_rune_alphabet_name(self):
#         self.assertEqual(runes.RunicAlphabetName.elder_futhark.value, "elder_futhark")
#
#     def test_rune_definition(self):
#         haglaz = runes.Rune(
#             runes.RunicAlphabetName.elder_futhark, "\u16BA", "h", "h", "haglaz"
#         )
#         self.assertEqual(haglaz.form, "ᚺ")
#
#     def test_runic_transcription_definition(self):
#         inscription = "ᚦᛁᛅᚴᚾ᛫ᛅᚢᚴ᛫ᚴᚢᚾᛅᚱ᛫ᚱᛅᛁᛋᛏᚢ᛫ᛋᛏᛅᛁᚾᛅ ᛅᚠᛏᛁᛦ᛫ᚢᛅᚱ᛫ᛒᚱᚢᚦᚢᚱ᛫ᛋᛁᚾ"
#         transcription = runes.Transcriber.transcribe(inscription, runes.YOUNGER_FUTHARK)
#         self.assertEqual(
#             transcription, "þiakn᛫auk᛫kunar᛫raistu᛫staina᛫aftiR᛫uar᛫bruþur᛫sin"
#         )


if __name__ == "__main__":
    unittest.main()
