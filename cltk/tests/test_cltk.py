"""Unit tests for CLTK"""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import unittest

from cltk.corpus.common.compiler import Compile
from cltk.corpus.greek.beta_to_unicode import Replacer
from cltk.stem.latin.j_and_v_converter import JVReplacer
from cltk.tag.pos.pos_tagger import POSTag
from cltk.tokenize.sentence.tokenize_sentences import TokenizeSentence
from nltk.tokenize.punkt import PunktWordTokenizer
import os


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        c = Compile()
        c.import_corpus('cltk_latin_linguistic_data')

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

    '''
    def test_import_cltk_linguistic_data_greek(self):
        """Import CLTK linguistic data to ~/cltk_data/greek/"""
        c = Compile()
        c.import_corpus('cltk_greek_linguistic_data')
        rel_path = '~/cltk_data/greek/cltk_linguistic_data/'
        abs_path = os.path.expanduser(rel_path)
        self.assertTrue(abs_path)

    def test_import_cltk_linguistic_data_latin(self):
        """Import CLTK linguistic data to ~/cltk_data/latin/"""
        c = Compile()
        c.import_corpus('cltk_latin_linguistic_data')
        rel_path = '~/cltk_data/latin/cltk_linguistic_data/'
        abs_path = os.path.expanduser(rel_path)
        self.assertTrue(abs_path)

    def test_sentence_tokenizer_greek(self):
        """Tokenizes Greek sentences."""
        t = TokenizeSentence()
        sentences = 'εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν; ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.'  # pylint: disable=C0301
        good_tokenized_sentences = ['εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν;', 'ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.']  # pylint: disable=C0301
        tokenized_sentences = t.sentence_tokenizer(sentences, 'greek')
        self.assertEqual(tokenized_sentences, good_tokenized_sentences)
    '''

    def test_sentence_tokenizer_latin(self):
        """Tokenizes Greek sentences."""
        t = TokenizeSentence()
        sentences = "Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti. Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum."  # pylint: disable=C0301
        good_tokenized_sentences = ['Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti.', 'Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum.']  # pylint: disable=C0301
        tokenized_sentences = t.sentence_tokenizer(sentences, 'latin')
        self.assertEqual(tokenized_sentences, good_tokenized_sentences)

    '''
    def test_pos_unigram_greek(self):
        """POS unigram tag Greek words."""
        p = POSTag()
        tagged = p.unigram_tagger('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος', 'greek')
        self.assertTrue(tagged)

    def test_pos_bigram_greek(self):
        """POS bigram tag Greek words."""
        p = POSTag()
        tagged = p.bigram_tagger('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος', 'greek')
        self.assertTrue(tagged)

    def test_pos_trigram_greek(self):
        """POS trigram tag Greek words."""
        p = POSTag()
        tagged = p.trigram_tagger('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος', 'greek')
        self.assertTrue(tagged)

    def test_pos_unigram_latin(self):
        """POS unigram tag Latin words."""
        p = POSTag()
        tagged = p.unigram_tagger('Gallia est omnis divisa in partes tres', 'latin')
        self.assertTrue(tagged)

    def test_pos_bigram_latin(self):
        """POS bigram tag Latin words."""
        p = POSTag()
        tagged = p.bigram_tagger('Gallia est omnis divisa in partes tres', 'latin')
        self.assertTrue(tagged)

    def test_pos_trigram_latin(self):
        """POS trigram tag Latin words."""
        p = POSTag()
        tagged = p.trigram_tagger('Gallia est omnis divisa in partes tres', 'latin')
        self.assertTrue(tagged)
    '''

if __name__ == '__main__':
    unittest.main()
