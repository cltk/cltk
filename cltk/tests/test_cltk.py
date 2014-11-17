"""Unit tests for CLTK
TODO: Add test for list_corpora (now w/ return type of list)
"""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'


from cltk.corpus import CLTK_DATA_DIR
#from cltk.corpus.cltk_logging import logger
from cltk.corpus.formatter import cleanup_tlg_txt
from cltk.corpus.formatter import remove_non_ascii
from cltk.corpus.greek.beta_to_unicode import Replacer
from cltk.corpus.importer import import_corpora, list_corpora
from cltk.stem.latin.j_and_v_converter import JVReplacer
from cltk.stem.latin.stemmer import Stemmer
#from cltk.tag.pos.pos_tagger import POSTag
from cltk.tag.pos import tag_unigram, tag_bigram, tag_trigram, tag_ngram_123_backoff, tag_tnt
#from cltk.tokenize.sentence.tokenize_sentences import TokenizeSentence
from cltk.tokenize.sentence import tokenize_sentences
import unittest
from nltk.tokenize.punkt import PunktWordTokenizer
import os


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        """Download CLTK linguistic data for tests."""
        greek_path_rel = '~/cltk_data/greek/trained_model/cltk_linguistic_data/'
        greek_path = os.path.expanduser(greek_path_rel)
        if not os.path.isdir(greek_path):
            import_corpora('greek', 'cltk_linguistic_data')
        latin_path_rel = '~/cltk_data/latin/trained_model/cltk_linguistic_data/'
        latin_path = os.path.expanduser(latin_path_rel)
        if not os.path.isdir(latin_path):
            import_corpora('latin', 'cltk_linguistic_data')

    def test_formatter_strip_ascii(self):
        """Test removing all non-ascii characters from a string."""
        non_ascii_str = 'Ascii and some non-ascii: θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν'
        ascii_str = remove_non_ascii(non_ascii_str)
        valid = 'Ascii and some non-ascii:     '
        self.assertEqual(ascii_str, valid)

    def test_formatter_cleanup_tlg(self):
        """Test removing misc TLG formatting."""
        unclean_str = 'πολλὰ ἔτι πάνυ παραλείπω· τὸ δὲ μέγιστον εἴρηται πλὴν αἱ τάξεισ τοῦ φόρου· τοῦτο δὲ γίγνεται ὡσ τὰ πολλὰ δῐ ἔτουσ πέμπτου. φέρε δὴ τοίνυν, ταῦτα οὐκ οἴεσθαι [2χρὴ]2 χρῆναι διαδικάζειν ἅπαντα; εἰπάτω γάρ τισ ὅ τι οὐ χρῆν αὐτόθι διαδικάζεσθαι. εἰ δ’ αὖ ὁμολογεῖν δεῖ ἅπαντα χρῆναι διαδικάζειν, ἀνάγκη δῐ ἐνιαυτοῦ· ὡσ οὐδὲ νῦν δῐ ἐνιαυτοῦ δικάζοντεσ ὑπάρχουσιν ὥστε παύειν τοὺσ ἀδικοῦντασ ὑπὸ τοῦ πλήθουσ τῶν ἀνθρώπων.'  # pylint: disable=C0301
        clean_str = cleanup_tlg_txt(unclean_str)
        valid = 'πολλὰ ἔτι πάνυ παραλείπω· τὸ δὲ μέγιστον εἴρηται πλὴν αἱ τάξεισ τοῦ φόρου· τοῦτο δὲ γίγνεται ὡσ τὰ πολλὰ δῐ ἔτουσ πέμπτου. φέρε δὴ τοίνυν, ταῦτα οὐκ οἴεσθαι  χρῆναι διαδικάζειν ἅπαντα; εἰπάτω γάρ τισ ὅ τι οὐ χρῆν αὐτόθι διαδικάζεσθαι. εἰ δ’ αὖ ὁμολογεῖν δεῖ ἅπαντα χρῆναι διαδικάζειν, ἀνάγκη δῐ ἐνιαυτοῦ· ὡσ οὐδὲ νῦν δῐ ἐνιαυτοῦ δικάζοντεσ ὑπάρχουσιν ὥστε παύειν τοὺσ ἀδικοῦντασ ὑπὸ τοῦ πλήθουσ τῶν ἀνθρώπων.'  # pylint: disable=C0301
        self.assertEqual(clean_str, valid)

    def test_latin_i_u_transform(self):
        """Test conversion of j to i and v to u"""
        j = JVReplacer()
        trans = j.replace('vem jam VEL JAM')
        self.assertEqual(trans, 'uem iam UEL IAM')

    def test_latin_stopwords(self):
        """Filter Latin stopwords"""
        from cltk.stop.latin.stops import STOPS_LIST
        sentence = 'Quo usque tandem abutere, Catilina, patientia nostra?'
        lowered = sentence.lower()
        tokens = PunktWordTokenizer().tokenize(lowered)
        no_stops = [w for w in tokens if w not in STOPS_LIST]
        target_list = ['usque', 'tandem', 'abutere', ',', 'catilina', ',',
                       'patientia', 'nostra', '?']
        self.assertEqual(no_stops, target_list)

    def test_greek_stopwords(self):
        """Filter Greek stopwords."""
        from cltk.stop.greek.stops_unicode import STOPS_LIST
        sentence = 'Ἅρπαγος δὲ καταστρεψάμενος Ἰωνίην ἐποιέετο στρατηίην \
        ἐπὶ Κᾶρας καὶ Καυνίους καὶ Λυκίους, ἅμα ἀγόμενος καὶ Ἴωνας καὶ \
        Αἰολέας.'
        lowered = sentence.lower()
        tokens = PunktWordTokenizer().tokenize(lowered)
        no_stops = [w for w in tokens if w not in STOPS_LIST]
        target_list = ['ἅρπαγος', 'καταστρεψάμενος', 'ἰωνίην', 'ἐποιέετο',
                       'στρατηίην', 'κᾶρας', 'καυνίους', 'λυκίους', ',',
                       'ἅμα', 'ἀγόμενος', 'ἴωνας', 'αἰολέας.']
        self.assertEqual(no_stops, target_list)

    def test_greek_betacode_to_unicode(self):
        """Test conversion of Beta Code to Unicode.
        Note: assertEqual appears to not be correctly comparing certain
        characters (ά and ί, at least).
        """
        beta_example = r"""O(/PWS OU)=N MH\ TAU)TO\ """
        replacer = Replacer()
        unicode = replacer.beta_code(beta_example)
        target_unicode = 'ὅπως οὖν μὴ ταὐτὸ '
        self.assertEqual(unicode, target_unicode)

    def test_latin_stemmer(self):
        """Test Latin stemmer."""
        cato = 'Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit.'
        j = JVReplacer()
        iu_cato = j.replace(cato.lower())
        s = Stemmer()
        stemmed_text = s.stem(iu_cato)
        target = 'est interd praestar mercatur r quaerere, nisi tam periculos sit. '
        self.assertEqual(stemmed_text, target)

    def test_import_cltk_linguistic_data_greek(self):
        """Check whether Greek linguistic data was imported during setUp()."""
        rel_path = '~/cltk_data/greek/trained_model/cltk_linguistic_data/'
        abs_path = os.path.expanduser(rel_path)
        self.assertTrue(abs_path)

    def test_import_cltk_linguistic_data_latin(self):
        """Check whether Latin linguistic data was imported during setUp()."""
        rel_path = '~/cltk_data/latin/trained_model/cltk_linguistic_data/'
        abs_path = os.path.expanduser(rel_path)
        self.assertTrue(abs_path)

    '''
    def test_logging(self):
        """Test CLTK logger."""
        logger.info('Testing CLTK logging module.')
        home_rel = CLTK_DATA_DIR
        home = os.path.expanduser(home_rel)
        logfile_path = os.path.join(home, 'cltk.log')
        with open(logfile_path, 'r') as f:
            r = f.read()
        eof = r.splitlines()[-1]
        log_message = eof.endswith('Testing CLTK logging module.')
        self.assertTrue(log_message)
    '''

    def test_sentence_tokenizer_greek(self):
        """Tokenizes Greek sentences."""
        sentences = 'εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν; ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.'  # pylint: disable=C0301
        good_tokenized_sentences = ['εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν;', 'ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.']  # pylint: disable=C0301
        tokenized_sentences = tokenize_sentences(sentences, 'greek')
        self.assertEqual(tokenized_sentences, good_tokenized_sentences)

    def test_sentence_tokenizer_latin(self):
        """Tokenizes Greek sentences."""
        sentences = "Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti. Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum."  # pylint: disable=C0301
        good_tokenized_sentences = ['Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti.', 'Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum.']  # pylint: disable=C0301
        tokenized_sentences = tokenize_sentences(sentences, 'latin')
        self.assertEqual(tokenized_sentences, good_tokenized_sentences)

    def test_pos_unigram_greek(self):
        """POS unigram tag Greek words."""
        tagged = tag_unigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος', 'greek')
        self.assertTrue(tagged)

    def test_pos_bigram_greek(self):
        """POS bigram tag Greek words."""
        tagged = tag_bigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος', 'greek')
        self.assertTrue(tagged)

    def test_pos_trigram_greek(self):
        """POS trigram tag Greek words."""
        tagged = tag_trigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος', 'greek')
        self.assertTrue(tagged)

    def test_pos_ngram_123_backoff_tagger_greek(self):
        """POS 123 ngram backoff tagger Greek words."""
        tagged = tag_ngram_123_backoff('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος', 'greek')
        self.assertTrue(tagged)

    def test_pos_tnt_tagger_greek(self):
        """POS 123 ngram backoff tagger Greek words."""
        tagged = tag_tnt('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος', 'greek')
        self.assertTrue(tagged)

    def test_pos_unigram_latin(self):
        """POS unigram tag Latin words."""
        tagged = tag_unigram('Gallia est omnis divisa in partes tres', 'latin')
        self.assertTrue(tagged)

    def test_pos_bigram_latin(self):
        """POS bigram tag Latin words."""
        tagged = tag_bigram('Gallia est omnis divisa in partes tres', 'latin')
        self.assertTrue(tagged)

    def test_pos_trigram_latin(self):
        """POS trigram tag Latin words."""
        tagged = tag_trigram('Gallia est omnis divisa in partes tres', 'latin')
        self.assertTrue(tagged)

    def test_pos_ngram_123_backoff_tagger_latin(self):
        """POS 123 ngram backoff tagger Latin words."""
        tagged = tag_ngram_123_backoff('Gallia est omnis divisa in partes tres', 'latin')
        self.assertTrue(tagged)

    def test_pos_tnt_tagger_latin(self):
        """POS TNT tagger Latin words."""
        tagged = tag_tnt('Gallia est omnis divisa in partes tres', 'latin')
        self.assertTrue(tagged)


if __name__ == '__main__':
    unittest.main()
