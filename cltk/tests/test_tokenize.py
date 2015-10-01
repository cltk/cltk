"""Test cltk.tokenize."""

from cltk.corpus.utils.importer import CorpusImporter
from cltk.stem.latin.j_v import JVReplacer
from cltk.tag import ner
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import nltk_tokenize_words
from cltk.tokenize.word import WordTokenizer
import os
import unittest

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'


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

    def test_latin_word_tokenizer(self):
        """Test Latin-specific word tokenizer."""
        word_tokenizer = WordTokenizer('latin')
        text = 'atque haec abuterque nihil'
        tokens = word_tokenizer.tokenize(text)
        target = ['atque', 'haec', 'abuter', '-que', 'nihil']
        self.assertEqual(tokens, target)

    def test_nltk_tokenize_words(self):
        """Test wrapper for NLTK's PunktLanguageVars()"""
        tokens = nltk_tokenize_words("Sentence 1. Sentence 2.", attached_period=False)
        target = ['Sentence', '1', '.', 'Sentence', '2', '.']
        self.assertEqual(tokens, target)

    def test_nltk_tokenize_words_attached(self):
        """Test wrapper for NLTK's PunktLanguageVars(), returning unaltered output."""
        tokens = nltk_tokenize_words("Sentence 1. Sentence 2.", attached_period=True)
        target = ['Sentence', '1.', 'Sentence', '2.']
        self.assertEqual(tokens, target)

    def test_nltk_tokenize_words_assert(self):
        """Test assert error for CLTK's word tokenizer."""
        with self.assertRaises(AssertionError):
            nltk_tokenize_words(['Sentence', '1.'])

    def test_check_latest_latin(self):
        """Test _check_latest_data()"""
        ner._check_latest_data('latin')
        names_path = os.path.expanduser('~/cltk_data/latin/model/latin_models_cltk/ner/proper_names.txt')
        self.assertTrue(os.path.isfile(names_path))

    def test_tag_ner_str_list_latin(self):
        """Test make_ner(), str, list."""
        text_str = """ut Venus, ut Sirius, ut Spica, ut aliae quae primae dicuntur esse mangitudinis."""
        jv_replacer = JVReplacer()
        text_str_iu = jv_replacer.replace(text_str)
        tokens = ner.tag_ner('latin', input_text=text_str_iu, output_type=list)
        target = [('ut',), ('Uenus', 'Entity'), (',',), ('ut',), ('Sirius', 'Entity'), (',',), ('ut',), ('Spica', 'Entity'), (',',), ('ut',), ('aliae',), ('quae',), ('primae',), ('dicuntur',), ('esse',), ('mangitudinis',), ('.',)]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_list_latin(self):
        """Test make_ner(), list, list."""
        text_list = ['ut', 'Venus', 'Sirius']
        jv_replacer = JVReplacer()
        text_list_iu = [jv_replacer.replace(x) for x in text_list]
        tokens = ner.tag_ner('latin', input_text=text_list_iu, output_type=list)
        target = [('ut',), ('Uenus', 'Entity'), ('Sirius', 'Entity')]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_str_latin(self):
        """Test make_ner(), list, str."""
        text_list = ['ut', 'Venus', 'Sirius']
        jv_replacer = JVReplacer()
        text_list_iu = [jv_replacer.replace(x) for x in text_list]
        text = ner.tag_ner('latin', input_text=text_list_iu, output_type=str)
        target = ' ut Uenus/Entity Sirius/Entity'
        self.assertEqual(text, target)

    def test_tag_ner_str_str_latin(self):
        """Test make_ner(), str, str."""
        jv_replacer = JVReplacer()
        text_str = """ut Venus, ut Sirius, ut Spica, ut aliae quae primae dicuntur esse mangitudinis."""
        jv_replacer = JVReplacer()
        text_str_iu = jv_replacer.replace(text_str)
        text = ner.tag_ner('latin', input_text=text_str_iu, output_type=str)
        target = ' ut Uenus/Entity, ut Sirius/Entity, ut Spica/Entity, ut aliae quae primae dicuntur esse mangitudinis.'
        self.assertEqual(text, target)

    def test_tag_ner_str_list_greek(self):
        """Test make_ner(), str, list."""
        text_str = 'τὰ Σίλαριν Σιννᾶν Κάππαρος Πρωτογενείας Διονυσιάδες τὴν'
        tokens = ner.tag_ner('greek', input_text=text_str, output_type=list)
        target = [('τὰ',), ('Σίλαριν', 'Entity'), ('Σιννᾶν', 'Entity'), ('Κάππαρος', 'Entity'), ('Πρωτογενείας', 'Entity'), ('Διονυσιάδες', 'Entity'), ('τὴν',)]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_list_greek(self):
        """Test make_ner(), list, list."""
        text_list = ['τὰ', 'Σίλαριν', 'Σιννᾶν']
        tokens = ner.tag_ner('greek', input_text=text_list, output_type=list)
        target = [('τὰ',), ('Σίλαριν', 'Entity'), ('Σιννᾶν', 'Entity')]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_str_greek(self):
        """Test make_ner(), list, str."""
        text_list = ['τὰ', 'Σίλαριν', 'Σιννᾶν']
        text = ner.tag_ner('greek', input_text=text_list, output_type=str)
        target = ' τὰ Σίλαριν/Entity Σιννᾶν/Entity'
        self.assertEqual(text, target)

    def test_tag_ner_str_str_greek(self):
        """Test make_ner(), str, str."""
        text_str = 'τὰ Σίλαριν Σιννᾶν Κάππαρος Πρωτογενείας Διονυσιάδες τὴν'
        text = ner.tag_ner('greek', input_text=text_str, output_type=str)
        target = ' τὰ Σίλαριν/Entity Σιννᾶν/Entity Κάππαρος/Entity Πρωτογενείας/Entity Διονυσιάδες/Entity τὴν'
        self.assertEqual(text, target)


if __name__ == '__main__':
    unittest.main()
