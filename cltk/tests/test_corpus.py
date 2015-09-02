"""Test cltk.corpus."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.greek.beta_to_unicode import Replacer
from cltk.corpus.greek.tlgu import TLGU
from cltk.corpus.utils.formatter import assemble_phi5_author_filepaths
from cltk.corpus.utils.formatter import assemble_phi5_works_filepaths
from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths
from cltk.corpus.utils.formatter import assemble_tlg_works_filepaths
from cltk.corpus.utils.formatter import phi5_plaintext_cleanup
from cltk.corpus.utils.formatter import remove_non_ascii
from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
from cltk.corpus.utils.importer import CorpusImporter
import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        #tlgu = TLGU(testing=True)
        #print('Existing tlgu?', tlgu)
        pass

    def test_greek_betacode_to_unicode(self):
        """Test converting Beta Code to Unicode.
        Note: assertEqual appears to not be correctly comparing certain
        characters (``ά`` and ``ί``, at least).
        """
        beta_example = r"""O(/PWS OU)=N MH\ TAU)TO\ """
        replacer = Replacer()
        unicode = replacer.beta_code(beta_example)
        target_unicode = 'ὅπως οὖν μὴ ταὐτὸ '
        self.assertEqual(unicode, target_unicode)

    def test_tlgu_init(self):
        """Test constructors of TLGU module for check, import, and install."""
        tlgu = TLGU()
        self.assertTrue(tlgu)

    def test_import_greek_software_tlgu(self):
        """Test cloning TLGU."""
        corpus_importer = CorpusImporter('greek')
        corpus_importer.import_corpus('greek_software_tlgu')
        file_rel = os.path.join('~/cltk_data/greek/software/greek_software_tlgu/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    '''
    def test_tlgu_convert(self):
        """Test TLGU convert. This reads the file
        ``tlgu_test_text_beta_code.txt``, which mimics a TLG file, and
        converts it.
        Note: assertEquals fails on some accented characters ('ή', 'ί').
        """
        in_test = os.path.abspath('cltk/tests/tlgu_test_text_beta_code.txt')
        out_test = os.path.expanduser('~/cltk_data/tlgu_test_text_unicode.txt')
        tlgu = TLGU()
        tlgu.convert(in_test, out_test)
        with open(out_test) as out_file:
            new_text = out_file.read()
        os.remove(out_test)
        target = """
βλλον δ' ἀλλλους χαλκρεσιν ἐγχεῃσιν.
"""
        self.assertEqual(new_text, target)
    '''

    '''
    def test_tlgu_convert_fail(self):
        """Test the TLGU to fail when importing a corpus that doesn't exist."""
        tlgu = TLGU()
        with self.assertRaises(AssertionError):
            tlgu.convert('~/Downloads/corpora/TLG_E/bad_path.txt',
                         '~/Documents/thucydides.txt')
    '''

    '''
    def test_tlgu_convert_corpus_fail(self):
        """Test the TLGU to fail when trying to convert an unsupported corpus."""
        tlgu = TLGU()
        with self.assertRaises(AssertionError):
            tlgu.convert_corpus(corpus='bad_corpus')
    '''

    def test_tlg_plaintext_cleanup(self):
        """Test post-TLGU cleanup of text of Greek TLG text."""
        dirty = """{ΑΘΗΝΑΙΟΥ ΝΑΥΚΡΑΤΙΤΟΥ ΔΕΙΠΝΟΣΟΦΙΣΤΩΝ} LATIN Ἀθήναιος (μὲν) ὁ τῆς 999 βίβλου πατήρ: ποιεῖται δὲ τὸν λόγον πρὸς Τιμοκράτην."""  # pylint: disable=line-too-long
        clean = tlg_plaintext_cleanup(dirty, rm_punctuation=True, rm_periods=False)
        target = ' Ἀθήναιος ὁ τῆς βίβλου πατήρ ποιεῖται δὲ τὸν λόγον πρὸς Τιμοκράτην.'
        self.assertEqual(clean, target)

    def test_phi5_plaintext_cleanup(self):
        """Test post-TLGU cleanup of text of Latin PHI5 text."""
        dirty = """        {ODYSSIA}
        {Liber I}
Virum áge 999 mihi, Camena, (insece) versutum.
Pater noster, Saturni filie . . .
Mea puera, quid verbi ex tuo ore supera fugit?
argenteo polubro, aureo eclutro. """
        clean = phi5_plaintext_cleanup(dirty, rm_punctuation=True, rm_periods=False)
        target = ' Virum áge mihi Camena versutum. Pater noster Saturni filie . . . Mea puera quid verbi ex tuo ore supera fugit argenteo polubro aureo eclutro. '  # pylint: disable=line-too-long
        self.assertEqual(clean, target)

    def test_assemble_tlg_author(self):
        """Test building absolute filepaths from TLG index."""
        paths = assemble_tlg_author_filepaths()
        self.assertEqual(len(paths), 1823)

    def test_assemble_phi5_author(self):
        """Test building absolute filepaths from TLG index."""
        paths = assemble_phi5_author_filepaths()
        self.assertEqual(len(paths), 362)

    def test_assemble_tlg_works(self):
        """"Test building absolute filepaths from TLG works index."""
        paths = assemble_tlg_works_filepaths()
        self.assertEqual(len(paths), 6625)

    def test_assemble_phi5_works(self):
        """"Test building absolute filepaths from PHI5 works index."""
        paths = assemble_phi5_works_filepaths()
        self.assertEqual(len(paths), 836)

    def test_corpora_import_list_greek(self):
        """Test listing of available corpora."""
        corpus_importer = CorpusImporter('greek')
        available_corpora = corpus_importer.list_corpora
        self.assertTrue(available_corpora)

    def test_corpora_import_list_latin(self):
        """Test listing of available corpora."""
        corpus_importer = CorpusImporter('latin')
        available_corpora = corpus_importer.list_corpora
        self.assertTrue(available_corpora)

    def test_remove_non_ascii(self):
        """Test removing all non-ascii characters from a string."""
        non_ascii_str = 'Ascii and some non-ascii: θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν'  # pylint: disable=line-too-long
        ascii_str = remove_non_ascii(non_ascii_str)
        valid = 'Ascii and some non-ascii:     '
        self.assertEqual(ascii_str, valid)

    def test_import_latin_text_perseus(self):
        """Test cloning the Perseus Latin text corpus."""
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_text_perseus')
        file_rel = os.path.join('~/cltk_data/latin/text/latin_text_perseus/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_import_greek_text_perseus(self):
        """Test cloning the Perseus Greek text corpus."""
        corpus_importer = CorpusImporter('greek')
        corpus_importer.import_corpus('greek_text_perseus')
        file_rel = os.path.join('~/cltk_data/greek/text/greek_text_perseus/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_import_proper_names_latin(self):
        """Test cloning the Latin proper names corpus."""
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_proper_names_cltk')
        file_rel = os.path.join('~/cltk_data/latin/lexicon/latin_proper_names_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_import_proper_names_greek(self):
        """Test cloning the Greek proper names corpus."""
        corpus_importer = CorpusImporter('greek')
        corpus_importer.import_corpus('greek_proper_names_cltk')
        file_rel = os.path.join('~/cltk_data/greek/lexicon/greek_proper_names_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_import_grk_treebank_pers(self):
        """Test cloning the Perseus Greek treebank corpus."""
        corpus_importer = CorpusImporter('greek')
        corpus_importer.import_corpus('greek_treebank_perseus')
        file_rel = os.path.join('~/cltk_data/greek/treebank/greek_treebank_perseus/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_import_la_treebank_pers(self):
        """Test cloning the Perseus Latin treebank corpus."""
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_treebank_perseus')
        file_rel = os.path.join('~/cltk_data/latin/treebank/latin_treebank_perseus/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_import_la_text_lac_curt(self):
        """Test cloning the Lacus Curtius Latin text corpus."""
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_text_lacus_curtius')
        file_rel = os.path.join('~/cltk_data/latin/text/latin_text_lacus_curtius/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_import_lat_text_lat_lib(self):
        """Test cloning the Latin Library text corpus."""
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_text_latin_library')
        file_rel = os.path.join('~/cltk_data/latin/text/latin_text_latin_library/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_import_latin_models_cltk(self):
        """Test cloning the CLTK Latin models."""
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_models_cltk')
        file_rel = os.path.join('~/cltk_data/latin/model/latin_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_import_lat_pos_lemma_cltk(self):
        """Test cloning the CLTK POS lemmata dict."""
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_pos_lemmata_cltk')
        file_rel = os.path.join('~/cltk_data/latin/lemma/latin_pos_lemmata_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_import_greek_models_cltk(self):
        """Test pull (not clone) the CLTK Greek models. Import was run in
        ``setUp()``.
        """
        corpus_importer = CorpusImporter('greek')
        corpus_importer.import_corpus('greek_models_cltk')
        file_rel = os.path.join('~/cltk_data/greek/model/greek_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_git_import_copt_script(self):
        """Test import of Coptic Scriptorium."""
        corpus_importer = CorpusImporter('coptic')
        corpus_importer.import_corpus('coptic_text_scriptorium')
        file_rel = os.path.join('~/cltk_data/coptic/text/coptic_text_scriptorium/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_git_import_tib_pos_tdc(self):
        """Test import Tibetan POS files."""
        corpus_importer = CorpusImporter('tibetan')
        corpus_importer.import_corpus('tibetan_pos_tdc')
        file_rel = os.path.join('~/cltk_data/tibetan/pos/tibetan_pos_tdc/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_git_import_tib_lexica_tdc(self):
        """Test import of Tibetan dictionary."""
        corpus_importer = CorpusImporter('tibetan')
        corpus_importer.import_corpus('tibetan_lexica_tdc')
        file_rel = os.path.join('~/cltk_data/tibetan/lexicon/tibetan_lexica_tdc/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_show_corpora_bad_lang(self):
        """Test failure of importer upon selecting unsupported language."""
        with self.assertRaises(AssertionError):
            CorpusImporter('bad_lang')

if __name__ == '__main__':
    unittest.main()
