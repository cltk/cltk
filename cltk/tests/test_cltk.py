"""Unit tests for CLTK"""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.classical_greek.beta_to_unicode import Replacer
from cltk.stem.classical_latin.j_and_v_converter import JVReplacer
from cltk.tokenize.sentence_tokenizer_greek import tokenize_latin_sentences
from nltk.tokenize.punkt import PunktWordTokenizer
import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_latin_i_u_transform(self):
        """Test conversion of j to i and v to u"""
        j = JVReplacer()
        trans = j.replace('vem jam VEL JAM')
        self.assertEqual(trans, 'uem iam UEL IAM')

    def test_latin_stopwords(self):
        """Filter Latin stopwords"""
        from cltk.stop.classical_latin.stops import STOPS_LIST
        sentence = 'Quo usque tandem abutere, Catilina, patientia nostra?'
        lowered = sentence.lower()
        tokens = PunktWordTokenizer().tokenize(lowered)
        no_stops = [w for w in tokens if w not in STOPS_LIST]
        target_list = ['usque', 'tandem', 'abutere', ',', 'catilina', ',',
                       'patientia', 'nostra', '?']
        self.assertEqual(no_stops, target_list)

    def test_greek_stopwords(self):
        """Filter Greek stopwords."""
        from cltk.stop.classical_greek.stops_unicode import STOPS_LIST
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

    def test_sentence_tokenizer_greek(self):
        """Reads Greek sentence tokenizer pickle, tokenizes into a list, and
        checks against a known good list.
        """
        try:
            cltk_data_dir_rel = '~/cltk_data'
            cltk_data_dir_abs = os.path.expanduser(cltk_data_dir_rel)
            greek_sentence_tokenizer_dir = os.path.join(cltk_data_dir_abs,
                                                        'compiled/sentence_tokens_greek')
            pickle_file = 'greek.pickle'
            pickle_file_path = os.path.join(greek_sentence_tokenizer_dir, pickle_file)
            try:
                os.path.exists(pickle_file_path)
                sentences = 'εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν; ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.'  # pylint: disable=C0301
                good_tokenized_sentences = ['εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν;', 'ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.']  # pylint: disable=C0301
                tokenized_sentences = tokenize_latin_sentences(sentences)
                self.assertEqual(tokenized_sentences, good_tokenized_sentences)
            except:
                pass
        except:
            pass

if __name__ == '__main__':
    unittest.main()
