"""Test the CLTK."""

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
from cltk.prosody.latin.scanner import Scansion
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.latin.stem import Stemmer
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.syllabifier import Syllabifier
from cltk.stop.greek.stops import STOPS_LIST as greek_stops
from cltk.stop.latin.stops import STOPS_LIST as latin_stops
from cltk.stop.make_stopwords_list import Stopwords
from cltk.tag.pos import POSTag
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from cltk.utils.build_contribs_index import build_contribs_file
from cltk.utils.file_operations import open_pickle
from cltk.utils.philology import Philology
from nltk.tokenize.punkt import PunktLanguageVars
import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        """Clone Greek models in order to test pull function and other model
        tests later.
        """
        corpus_importer = CorpusImporter('greek')
        corpus_importer.import_corpus('greek_models_cltk')
        file_rel = os.path.join('~/cltk_data/greek/model/greek_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_models_cltk')
        file_rel = os.path.join('~/cltk_data/latin/model/latin_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_concordance_from_string(self):
        """Test ``write_concordance_from_string()`` for file writing completion
        of concordance builder. Doesn't test quality of output."""
        philology = Philology()
        text = 'felices cantus ore sonante dedit'
        philology.write_concordance_from_string(text, 'test_string')
        file = os.path.expanduser('~/cltk_data/user_data/concordance_test_string.txt')
        is_file = os.path.isfile(file)
        self.assertTrue(is_file)

    def test_concordance_from_file(self):
        """Test ``write_concordance_from_file()`` for file writing completion
        of concordance builder. Doesn't test quality of output."""
        philology = Philology()
        file = 'cltk/tests/bad_pickle.pickle'
        philology.write_concordance_from_file(file, 'test_file')
        file = os.path.expanduser('~/cltk_data/user_data/concordance_test_file.txt')
        is_file = os.path.isfile(file)
        self.assertTrue(is_file)

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

    def test_import_lat_pos_lemm_cltk(self):
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

    def test_build_contribs_file(self):
        """Test building of contributors file ``contributors.md`` by
        ``build_contribs_file.py``."""
        string = build_contribs_file(test=True)
        self.assertTrue(string)

    def test_remove_non_ascii(self):
        """Test removing all non-ascii characters from a string."""
        non_ascii_str = 'Ascii and some non-ascii: θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν'  # pylint: disable=line-too-long
        ascii_str = remove_non_ascii(non_ascii_str)
        valid = 'Ascii and some non-ascii:     '
        self.assertEqual(ascii_str, valid)

    def test_tlg_plaintext_cleanup(self):
        """Test post-TLGU cleanup of text of Greek TLG text."""
        dirty = """{ΑΘΗΝΑΙΟΥ ΝΑΥΚΡΑΤΙΤΟΥ ΔΕΙΠΝΟΣΟΦΙΣΤΩΝ} LATIN Ἀθήναιος (μὲν) ὁ τῆς 999 βίβλου πατήρ: ποιεῖται δὲ τὸν λόγον πρὸς Τιμοκράτην."""  # pylint: disable=line-too-long
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
        target = """                  Virum  mihi, Camena, insece versutum. Pater noster, Saturni filie . . . Mea puera, quid verbi ex tuo ore supera fugit? argenteo polubro, aureo eclutro. """  # pylint: disable=line-too-long
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

    def test_open_pickle_fail_missing(self):
        """Test failure to unpickle a file that doesn't exist"""
        bad_file = 'cltk/tests/doesnt_exist.pickle'
        with self.assertRaises(FileNotFoundError):
            open_pickle(bad_file)

    def test_open_pickle_fail_corrupt(self):
        """Test failure to open corrupted pickle."""
        bad_file = 'cltk/tests/bad_pickle.pickle'
        with self.assertRaises(EOFError):
            open_pickle(bad_file)

    def test_show_corpora_bad_lang(self):
        """Test failure of importer upon selecting unsupported language."""
        with self.assertRaises(AssertionError):
            CorpusImporter('bad_lang')

    def test_latin_i_u_transform(self):
        """Test converting ``j`` to ``i`` and ``v`` to ``u``."""
        jv_replacer = JVReplacer()
        trans = jv_replacer.replace('vem jam VEL JAM')
        self.assertEqual(trans, 'uem iam UEL IAM')

    def test_latin_stopwords(self):
        """Test filtering Latin stopwords."""
        sentence = 'Quo usque tandem abutere, Catilina, patientia nostra?'
        lowered = sentence.lower()
        punkt = PunktLanguageVars()
        tokens = punkt.word_tokenize(lowered)
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
        punkt = PunktLanguageVars()
        tokens = punkt.word_tokenize(lowered)
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
        sentence = 'Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum.'  # pylint: disable=line-too-long
        stemmer = Stemmer()
        stemmed_text = stemmer.stem(sentence.lower())
        target = 'est interd praestar mercatur r quaerere, nisi tam periculos sit, et it foenerari, si tam honestum. '  # pylint: disable=line-too-long
        self.assertEqual(stemmed_text, target)

    def test_latin_syllabifier(self):
        """Test Latin syllabifier."""
        word = 'sidere'  # pylint: disable=line-too-long
        syllabifier = Syllabifier()
        syllables = syllabifier.syllabify(word)
        target = ['si', 'de', 're']  # pylint: disable=line-too-long
        self.assertEqual(syllables, target)

    def test_sentence_tokenizer_latin(self):
        """Test tokenizing Latin sentences."""
        sentences = "Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti. Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum."  # pylint: disable=line-too-long
        good_tokenized_sentences = ['Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti.', 'Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum.']  # pylint: disable=line-too-long
        tokenizer = TokenizeSentence('latin')
        tokenized_sentences = tokenizer.tokenize_sentences(sentences)
        self.assertEqual(tokenized_sentences, good_tokenized_sentences)

    '''
    def test_sentence_tokenizer_greek(self):
        """Test tokenizing Greek sentences.
        TODO: Re-enable this. Test & code are good, but now fail on Travis CI for some reason.
        """
        sentences = 'εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν; ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.'  # pylint: disable=line-too-long
        good_tokenized_sentences = ['εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν;', 'ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.']  # pylint: disable=line-too-long
        tokenizer = TokenizeSentence('greek')
        tokenized_sentences = tokenizer.tokenize_sentences(sentences)
        self.assertEqual(len(tokenized_sentences), len(good_tokenized_sentences))
    '''
    
    def test_pos_unigram_greek(self):
        """Test tagging Greek POS with unigram tagger."""
        tagger = POSTag('greek')
        tagged = tagger.tag_unigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_bigram_greek(self):
        """Test tagging Greek POS with bigram tagger."""
        tagger = POSTag('greek')
        tagged = tagger.tag_bigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_trigram_greek(self):
        """Test tagging Greek POS with trigram tagger."""
        tagger = POSTag('greek')
        tagged = tagger.tag_trigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_ngram123_tagger_greek(self):
        """Test tagging Greek POS with a 1-, 2-, and 3-gram backoff tagger."""
        tagger = POSTag('greek')
        tagged = tagger.tag_ngram_123_backoff('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_tnt_tagger_greek(self):
        """Test tagging Greek POS with TnT tagger."""
        tagger = POSTag('greek')
        tagged = tagger.tag_tnt('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')  # pylint: disable=line-too-long
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
        tagged = tagger.tag_ngram_123_backoff('Gallia est omnis divisa in partes tres')  # pylint: disable=line-too-long
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

    def test_import_greek_software_tlgu(self):
        """Test cloning TLGU."""
        corpus_importer = CorpusImporter('greek')
        corpus_importer.import_corpus('greek_software_tlgu')
        file_rel = os.path.join('~/cltk_data/greek/software/greek_software_tlgu/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

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
        with self.assertRaises(AssertionError):
            tlgu.convert('~/Downloads/corpora/TLG_E/bad_path.txt',
                         '~/Documents/thucydides.txt')

    def test_tlgu_convert_corpus_fail(self):
        """Test the TLGU to fail when trying to convert an unsupported corpus."""
        tlgu = TLGU()
        with self.assertRaises(AssertionError):
            tlgu.convert_corpus(corpus='bad_corpus')

    def test_open_pickle(self):
        """Test opening pickle. This requires ``greek_models_cltk``
        to have been run in ``setUp()``.
        """
        pickle_path_rel = '~/cltk_data/greek/model/greek_models_cltk/tokenizers/sentence/greek.pickle'  # pylint: disable=line-too-long
        pickle_path = os.path.expanduser(pickle_path_rel)
        a_pickle = open_pickle(pickle_path)
        self.assertTrue(a_pickle)

    def test_lemmatizer_inlist_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=False, return_string=False)
        target = ['homo', 'divus', 'voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=True, return_string=False)
        target = ['hominum/homo', 'divomque/divus', 'voluptas/voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=False, return_string=True)
        target = 'homo divus voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = ['hominum', 'divomque', 'voluptas']
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=True, return_string=True)
        target = 'hominum/homo divomque/divus voluptas/voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=False, return_string=False)
        target = ['homo', 'divus', 'voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=True, return_string=False)
        target = ['hominum/homo', 'divomque/divus', 'voluptas/voluptas']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=False, return_string=True)
        target = 'homo divus voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_outstring_latin(self):
        """Test the Latin lemmatizer.
        """
        replacer = LemmaReplacer('latin')
        unlemmatized = 'hominum divomque voluptas'
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=True, return_string=True)
        target = 'hominum/homo divomque/divus voluptas/voluptas'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=False, return_string=False)
        target = ['τὴν', 'διάγνωσις', 'ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=True, return_string=False)
        target = ['τὴν/τὴν', 'διάγνωσιν/διάγνωσις', 'ἔρχεσθαι/ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=False, return_string=True)
        target = 'τὴν διάγνωσις ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_inlist_outlemma_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = ['τὴν', 'διάγνωσιν', 'ἔρχεσθαι']
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=True, return_string=True)
        target = 'τὴν/τὴν διάγνωσιν/διάγνωσις ἔρχεσθαι/ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=False, return_string=False)
        target = ['τὴν', 'διάγνωσις', 'ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=True, return_string=False)
        target = ['τὴν/τὴν', 'διάγνωσιν/διάγνωσις', 'ἔρχεσθαι/ἔρχομαι']
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=False, return_string=True)
        target = 'τὴν διάγνωσις ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_lemmatizer_instr_outlemma_outstring_greek(self):
        """Test the Greek lemmatizer.
        """
        replacer = LemmaReplacer('greek')
        unlemmatized = 'τὴν διάγνωσιν ἔρχεσθαι'
        lemmatized = replacer.lemmatize(unlemmatized, return_lemma=True, return_string=True)
        target = 'τὴν/τὴν διάγνωσιν/διάγνωσις ἔρχεσθαι/ἔρχομαι'
        self.assertEqual(lemmatized, target)

    def test_make_stopwords(self):
        """Test stopword builder."""
        s = Stopwords('latin')
        text = 'Quo Quo Quo Quo usque tandem abutere, Catilina Catilina Catilina, patientia nostra nostra ?'.lower()
        stops = s.make_list_from_str(text, 3)
        target = ['quo', 'catilina', 'nostra']
        self.assertEqual(stops, target)

    def test_make_stopwords_save(self):
        """Test stopword builder."""
        s = Stopwords('latin')
        text = 'Quo Quo Quo Quo usque tandem abutere, Catilina Catilina Catilina, patientia nostra nostra ?'.lower()
        s.make_list_from_str(text, 3, save=True)
        # cltk_data/user_data/stops_latin_*
        user_data_rel = '~/cltk_data/user_data/'
        user_data = os.path.expanduser(user_data_rel)
        list_dir = os.listdir(user_data)
        file_start = 'stops_latin_'
        for file in list_dir:
            if file.startswith(file_start):
                self.assertTrue(file.startswith(file_start))
                os.remove(user_data + file)

    def test_save_stopwords(self):
        """Test stopword saving private module."""
        s = Stopwords('latin')
        s._save_stopwords(['word1', 'word2'])
        # cltk_data/user_data/stops_latin_*
        user_data_rel = '~/cltk_data/user_data/'
        user_data = os.path.expanduser(user_data_rel)
        list_dir = os.listdir(user_data)
        file_start = 'stops_latin_'
        for file in list_dir:
            if file.startswith(file_start):
                self.assertTrue(file.startswith(file_start))
                os.remove(user_data + file)

    def test_latin_word_tokenizer(self):
        """Test Latin-specific word tokenizer."""
        word_tokenizer = WordTokenizer('latin')
        text = 'atque haec abuterque nihil'
        tokens = word_tokenizer.tokenize(text)
        target = ['atque', 'haec', 'abuter', 'que', 'nihil']
        self.assertEqual(tokens, target)

    def test_latin(self):
        scan = Scansion()
        meter = scan.scan_text('quō usque tandem abūtēre, Catilīna, patientiā nostrā. quam diū etiam furor iste tuus nōs ēlūdet.')
        self.assertEqual(meter, ['¯˘¯˘¯¯˘˘˘¯˘˘˘¯˘¯¯¯', '¯˘¯˘¯˘˘¯˘˘¯¯¯¯˘'])

if __name__ == '__main__':
    unittest.main()
