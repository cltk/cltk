"""Test the CLTK.
TODO: Write test for copy_dir_contents
"""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import os
import unittest

from cltk.corpus.greek.beta_to_unicode import Replacer

from cltk.corpus.greek.tlgu import TLGU
from cltk.utils.file_operations import open_pickle
from cltk.utils.build_contribs_index import build_contribs_file
from cltk.corpus.utils.formatter import remove_non_ascii
from cltk.corpus.utils.formatter import assemble_phi5_author_filepaths
from cltk.corpus.utils.formatter import assemble_phi5_works_filepaths
from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths
from cltk.corpus.utils.formatter import assemble_tlg_works_filepaths
from cltk.corpus.utils.formatter import phi5_plaintext_cleanup
from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
from cltk.corpus.utils.importer import CorpusImporter
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.stem import Stemmer
from cltk.stop.greek.stops import STOPS_LIST as greek_stops
from cltk.stem.latin.syllabifier import Syllabifier
from cltk.stop.latin.stops import STOPS_LIST as latin_stops
from cltk.tag.pos import POSTag
from cltk.tokenize.sentence import TokenizeSentence
from nltk.tokenize.punkt import PunktLanguageVars
import stat


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        pass

    def test_import_perseus_latin_text(self):
        """Test downloading the Perseus Latin text corpus."""
        c = CorpusImporter('latin')
        c.import_corpus('latin_text_perseus')
        dir_rel = os.path.join('~/cltk_data/latin/text/latin_text_perseus/latin_corpus_perseus/Ammianus')
        dir = os.path.expanduser(dir_rel)
        dir_exists = os.path.isfile(dir)
        self.assertTrue(dir_exists)

    # below imports are good
    '''
    # good
    def test_import_proper_names_latin(self):
        """Test downloading the Latin proper names corpus."""
        c = CorpusImporter('latin')
        c.import_corpus('latin_proper_names')
        file_rel = os.path.join('~/cltk_data/latin/dictionary/latin_proper_names/proper_names.txt')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    # good
    def test_import_tlgu(self):
        """Test downloading TLGU."""
        c = CorpusImporter('greek')
        c.import_corpus('greek_proper_names')
        file_rel = os.path.join('~/cltk_data/greek/software/tlgu/tlgu.h')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)


    # good
    def test_import_proper_names_greek(self):
        """Test downloading the Greek proper names corpus."""
        c = CorpusImporter('greek')
        c.import_corpus('greek_proper_names')
        file_rel = os.path.join('~/cltk_data/greek/dictionary/greek_proper_names/proper_names.txt')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)


    # good
    def test_import_greek_trbnk_perseus(self):
        """Test downloading the Perseus greek treebank corpus."""
        c = CorpusImporter('greek')
        c.import_corpus('greek_treebank_perseus')
        file_rel = os.path.join('~/cltk_data/greek/treebank/greek_treebank_perseus/unigram.pickle')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)


    # good
    def test_import_latin_trbnk_perseus(self):
        """Test downloading the Perseus Latin treebank corpus."""
        c = CorpusImporter('latin')
        c.import_corpus('latin_treebank_perseus')
        file_rel = os.path.join('~/cltk_data/latin/treebank/latin_treebank_perseus/unigram.pickle')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)


    # good
    def test_import_lacus_curtius(self):
        """Test downloading the Lacus_Curtius Latin text corpus."""
        c = CorpusImporter('latin')
        c.import_corpus('latin_text_lacus_curtius')
        dir_rel = os.path.join('~/cltk_data/latin/text/latin_text_lacus_curtius/lacus_curtius/Aelian')
        dir = os.path.expanduser(dir_rel)
        dir_exists = os.path.isdir(dir)
        self.assertTrue(dir_exists)

    # good
    def test_import_perseus_greek_text(self):
        """Test downloading the Perseus Greek text corpus."""
        c = CorpusImporter('greek')
        c.import_corpus('greek_text_perseus')
        dir_rel = os.path.join('~/cltk_data/greek/text/greek_text_perseus/greek_corpus_perseus/Aeschines')
        dir = os.path.expanduser(dir_rel)
        dir_exists = os.path.isdir(dir)
        self.assertTrue(dir_exists)



    # good
    def test_import_latin_library(self):
        """Test downloading the Latin Library text corpus."""
        c = CorpusImporter('latin')
        c.import_corpus('latin_text_latin_library')
        dir_rel = os.path.join('~/cltk_data/latin/text/latin_text_latin_library/latin_library/abelard')
        dir = os.path.expanduser(dir_rel)
        dir_exists = os.path.isdir(dir)
        self.assertTrue(dir_exists)

    def test_latin_ling_import(self):
        # good
        c = CorpusImporter('latin')
        c.import_corpus('cltk_linguistic_data')
        dir_rel = os.path.join('~/cltk_data/latin/trained_model/cltk_linguistic_data')
        dir = os.path.expanduser(dir_rel)
        dir_exists = os.path.isdir(dir)
        self.assertTrue(dir_exists)


    def test_greek_ling_import(self):
        # good
        c = CorpusImporter('greek')
        c.import_corpus('cltk_linguistic_data')
        dir_rel = os.path.join('~/cltk_data/greek/trained_model/cltk_linguistic_data')
        dir = os.path.expanduser(dir_rel)
        dir_exists = os.path.isdir(dir)
        self.assertTrue(dir_exists)

    def test_git_import(self):
        # good
        c = CorpusImporter('latin')
        c.import_corpus('latin_proper_names')
        dir_rel = os.path.join('~/cltk_data/latin/dictionary/latin_proper_names')
        dir = os.path.expanduser(dir_rel)
        dir_exists = os.path.isdir(dir)
        self.assertTrue(dir_exists)
    '''

    '''
    def test_build_contribs_file(self):
        str = build_contribs_file(test=True)
        self.assertTrue(str)

    def test_remove_non_ascii(self):
        """Test removing all non-ascii characters from a string."""
        non_ascii_str = 'Ascii and some non-ascii: θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν'  # pylint: disable=C0301
        ascii_str = remove_non_ascii(non_ascii_str)
        valid = 'Ascii and some non-ascii:     '
        self.assertEqual(ascii_str, valid)

    def test_tlg_plaintext_cleanup(self):
        """Test post-TLGU cleanup of text of Greek TLG text."""
        dirty = """{ΑΘΗΝΑΙΟΥ ΝΑΥΚΡΑΤΙΤΟΥ ΔΕΙΠΝΟΣΟΦΙΣΤΩΝ} LATIN Ἀθήναιος (μὲν) ὁ τῆς 999 βίβλου πατήρ: ποιεῖται δὲ τὸν λόγον πρὸς Τιμοκράτην."""
        clean = tlg_plaintext_cleanup(dirty)
        target = """  Ἀθήναιος  ὁ τῆς  βίβλου πατήρ: ποιεῖται δὲ τὸν λόγον πρὸς Τιμοκράτην."""
        self.assertEqual(clean, target)

    def test_phi5_plaintext_cleanup(self):
        """Test post-TLGU cleanup of text of Latin PHI5 text."""
        dirty = """        {ODYSSIA}
        {Liber I}
Virum 999 mihi, Camena, insece versutum.
Pater noster, Saturni filie . . .
Mea puera, quid verbi ex tuo ore supera fugit?
argenteo polubro, aureo eclutro. """
        clean = phi5_plaintext_cleanup(dirty)
        target = """                  Virum  mihi, Camena, insece versutum. Pater noster, Saturni filie . . . Mea puera, quid verbi ex tuo ore supera fugit? argenteo polubro, aureo eclutro. """
        self.assertEqual(clean, target)

    def test_assemble_tlg_author_filepaths(self):
        """Test building absolute filepaths from TLG index."""
        paths = assemble_tlg_author_filepaths()
        self.assertEqual(len(paths), 1823)

    def test_assemble_phi5_author_filepaths(self):
        """Test building absolute filepaths from TLG index."""
        paths = assemble_phi5_author_filepaths()
        self.assertEqual(len(paths), 362)

    def test_assemble_tlg_works_filepaths(self):
        """"Test building absolute filepaths from TLG works index."""
        paths = assemble_tlg_works_filepaths()
        self.assertEqual(len(paths), 6625)

    def test_assemble_phi5_works_filepaths(self):
        """"Test building absolute filepaths from PHI5 works index.
        TODO: finish this once the PHI5 works index is finished.
        """
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

    def test_open_pickle(self):
        """Test opening function pickle."""
        pickle_path_rel = '~/cltk_data/greek/trained_model/cltk_linguistic_data/tokenizers/sentence/greek.pickle'  # pylint: disable=C0301
        pickle_path = os.path.expanduser(pickle_path_rel)
        a_pickle = open_pickle(pickle_path)
        self.assertTrue(a_pickle)

    def test_open_pickle_fail_doesnt_exist(self):
        """Test failure to unpickle a file that doesn't exist"""
        bad_file = 'cltk/tests/doesnt_exist.pickle'
        with self.assertRaises(SystemExit):
            open_pickle(bad_file)

    def test_open_pickle_fail_corrupt(self):
        bad_file = 'cltk/tests/bad_pickle.pickle'
        with self.assertRaises(SystemExit):
            open_pickle(bad_file)

    def test_show_corpora_unsupported_lang(self):
        """Test failure of importer upon selecting unsupported language."""
        with self.assertRaises(AssertionError):
            CorpusImporter('bad_lang')

    def test_lemmatizer_latin(self):
        """Test the Latin lemmatizer."""
        replacer = LemmaReplacer('latin')
        sentence = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(sentence)
        target = 'homo divus voluptas'
        self.assertEqual(lemmatized, target)

    def test_latin_i_u_transform(self):
        """Test converting ``j`` to ``i`` and ``v`` to ``u``."""
        j = JVReplacer()
        trans = j.replace('vem jam VEL JAM')
        self.assertEqual(trans, 'uem iam UEL IAM')

    def test_latin_stopwords(self):
        """Test filtering Latin stopwords."""
        sentence = 'Quo usque tandem abutere, Catilina, patientia nostra?'
        lowered = sentence.lower()
        #tokens = PunktWordTokenizer().tokenize(lowered)
        p = PunktLanguageVars()
        tokens = p.word_tokenize(lowered)
        no_stops = [w for w in tokens if w not in latin_stops]
        target_list = ['usque', 'tandem', 'abutere', ',', 'catilina', ',',
                       'patientia', 'nostra', '?']
        self.assertEqual(no_stops, target_list)

    def test_greek_stopwords(self):
        """Test filtering Greek stopwords."""
        sentence = 'Ἅρπαγος δὲ καταστρεψάμενος Ἰωνίην ἐποιέετο στρατηίην \
        ἐπὶ Κᾶρας καὶ Καυνίους καὶ Λυκίους, ἅμα ἀγόμενος καὶ Ἴωνας καὶ \
        Αἰολέας.'
        lowered = sentence.lower()
        #tokens = PunktWordTokenizer().tokenize(lowered)
        p = PunktLanguageVars()
        tokens = p.word_tokenize(lowered)
        no_stops = [w for w in tokens if w not in greek_stops]
        target_list = ['ἅρπαγος', 'καταστρεψάμενος', 'ἰωνίην', 'ἐποιέετο',
                       'στρατηίην', 'κᾶρας', 'καυνίους', 'λυκίους', ',',
                       'ἅμα', 'ἀγόμενος', 'ἴωνας', 'αἰολέας.']
        self.assertEqual(no_stops, target_list)

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

    def test_latin_stemmer(self):
        """Test Latin stemmer."""
        sentence = 'Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum.'  # pylint: disable=C0301
        stemmer = Stemmer()
        stemmed_text = stemmer.stem(sentence.lower())
        target = 'est interd praestar mercatur r quaerere, nisi tam periculos sit, et it foenerari, si tam honestum. '  # pylint: disable=C0301
        self.assertEqual(stemmed_text, target)

    def test_latin_syllabifier(self):
        """Test Latin syllabifier."""
        word = 'sidere'  # pylint: disable=C0301
        syllabifier = Syllabifier()
        syllables = syllabifier.syllabify(word)
        target = ['si', 'de', 're']  # pylint: disable=C0301
        self.assertEqual(syllables, target)

    def test_import_ling_data_greek(self):
        """Test whether CLTK Greek linguistic data was imported during
        ``setUp()``."""
        rel_path = '~/cltk_data/greek/trained_model/cltk_linguistic_data/'
        abs_path = os.path.expanduser(rel_path)
        self.assertTrue(abs_path)

    def test_import_ling_data_latin(self):
        """Test whether CLTK Latin linguistic data was imported during
        ``setUp()``."""
        rel_path = '~/cltk_data/latin/trained_model/cltk_linguistic_data/'
        abs_path = os.path.expanduser(rel_path)
        self.assertTrue(abs_path)

    def test_sentence_tokenizer_greek(self):
        """Test tokenizing Greek sentences."""
        sentences = 'εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν; ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.'  # pylint: disable=C0301
        good_tokenized_sentences = ['εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν;', 'ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.']  # pylint: disable=C0301
        tokenizer = TokenizeSentence('greek')
        tokenized_sentences = tokenizer.tokenize_sentences(sentences)
        self.assertEqual(tokenized_sentences, good_tokenized_sentences)

    def test_sentence_tokenizer_latin(self):
        """Test tokenizing Latin sentences."""
        sentences = "Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti. Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum."  # pylint: disable=C0301
        good_tokenized_sentences = ['Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti.', 'Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum.']  # pylint: disable=C0301
        tokenizer = TokenizeSentence('latin')
        tokenized_sentences = tokenizer.tokenize_sentences(sentences)
        self.assertEqual(tokenized_sentences, good_tokenized_sentences)

    def test_pos_unigram_greek(self):
        """Test tagging Greek POS with unigram tagger."""
        tagger = POSTag('greek')
        tagged = tagger.tag_unigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')  # pylint: disable=C0301
        self.assertTrue(tagged)

    def test_pos_bigram_greek(self):
        """Test tagging Greek POS with bigram tagger."""
        tagger = POSTag('greek')
        tagged = tagger.tag_bigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')  # pylint: disable=C0301
        self.assertTrue(tagged)

    def test_pos_trigram_greek(self):
        """Test tagging Greek POS with trigram tagger."""
        tagger = POSTag('greek')
        tagged = tagger.tag_trigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')  # pylint: disable=C0301
        self.assertTrue(tagged)

    def test_pos_ngram123_tagger_greek(self):
        """Test tagging Greek POS with a 1-, 2-, and 3-gram backoff tagger."""
        tagger = POSTag('greek')
        tagged = tagger.tag_ngram_123_backoff('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')  # pylint: disable=C0301
        self.assertTrue(tagged)

    def test_pos_tnt_tagger_greek(self):
        """Test tagging Greek POS with TnT tagger."""
        tagger = POSTag('greek')
        tagged = tagger.tag_tnt('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')  # pylint: disable=C0301
        self.assertTrue(tagged)

    def test_pos_unigram_latin(self):
        """Test tagging Latin POS with unigram tagger."""
        tagger = POSTag('latin')
        tagged = tagger.tag_unigram('Gallia est omnis divisa in partes tres')
        self.assertTrue(tagged)

    def test_pos_bigram_latin(self):
        """Test tagging Latin POS with bigram tagger."""
        tagger = POSTag('latin')
        tagged = tagger.tag_bigram('Gallia est omnis divisa in partes tres')
        self.assertTrue(tagged)

    def test_pos_trigram_latin(self):
        """Test tagging Latin POS with trigram tagger."""
        tagger = POSTag('latin')
        tagged = tagger.tag_trigram('Gallia est omnis divisa in partes tres')
        self.assertTrue(tagged)

    def test_pos_ngram123_tagger_latin(self):
        """Test tagging Latin POS with a 1-, 2-, and 3-gram backoff tagger."""
        tagger = POSTag('latin')
        tagged = tagger.tag_ngram_123_backoff('Gallia est omnis divisa in partes tres')  # pylint: disable=C0301
        self.assertTrue(tagged)

    def test_pos_tnt_tagger_latin(self):
        """Test tagging Latin POS with TnT tagger."""
        tagger = POSTag('latin')
        tagged = tagger.tag_tnt('Gallia est omnis divisa in partes tres')
        self.assertTrue(tagged)

    def test_logger(self):
        """Test the CLTK logger."""
        home_dir = os.path.expanduser('~/cltk_data')
        log_path = os.path.join(home_dir, 'cltk.log')
        self.assertTrue(log_path)

    def test_tlgu_init(self):
        """Test constructors of TLGU module for check, import, and install."""
        tlgu = TLGU()
        self.assertTrue(tlgu)

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

    def test_tlgu_convert_fail(self):
        """Test the TLGU to fail when importing a corpus that doesn't exist."""
        tlgu = TLGU()
        with self.assertRaises(SystemExit):
            tlgu.convert('~/Downloads/corpora/TLG_E/bad_path.txt',
                         '~/Documents/thucydides.txt')

    def test_tlgu_convert_unsupported_corpus_fail(self):
        """Test the TLGU to fail when trying to convert an unsupported corpus."""
        tlgu = TLGU()
        with self.assertRaises(SystemExit):
            tlgu.convert_corpus(corpus='bad_corpus')
    '''

if __name__ == '__main__':
    unittest.main()
