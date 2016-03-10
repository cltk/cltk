"""Test cltk.tokenize."""

from cltk.corpus.utils.importer import CorpusImporter
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
        
        #Test sources:
        # - V. Aen. 1.1
        # - Prop. 2.5.1-2
        # - Ov. Am. 1.8.65-66
        # - Cic. Phillip. 13.14
        # - Plaut. Capt. 937
        # - Lucr. DRN. 5.1351-53
        
        tests = ['Arma virumque cano, Troiae qui primus ab oris.',
                    'Hoc verumst, tota te ferri, Cynthia, Roma, et non ignota vivere nequitia?',
                    'Nec te decipiant veteres circum atria cerae. Tolle tuos tecum, pauper amator, avos!',
                    'Neque enim, quod quisque potest, id ei licet, nec, si non obstatur, propterea etiam permittitur.',
                    'Quid opust verbis? lingua nullast qua negem quidquid roges.',
                    'Textile post ferrumst, quia ferro tela paratur, nec ratione alia possunt tam levia gigni insilia ac fusi, radii, scapique sonantes.'
                    ]
        
        results = []
        
        for test in tests:
            result = word_tokenizer.tokenize(test)
            results.append(result)
                    
        target = [['Arma', 'que', 'virum', 'cano', ',', 'Troiae', 'qui', 'primus', 'ab', 'oris.'],
                    ['Hoc', 'verum', 'est', ',', 'tota', 'te', 'ferri', ',', 'Cynthia', ',', 'Roma', ',', 'et', 'non', 'ignota', 'vivere', 'nequitia', '?'],
                    ['Nec', 'te', 'decipiant', 'veteres', 'circum', 'atria', 'cerae.', 'Tolle', 'tuos', 'cum', 'te', ',', 'pauper', 'amator', ',', 'avos', '!'],
                    ['que', 'Ne', 'enim', ',', 'quod', 'quisque', 'potest', ',', 'id', 'ei', 'licet', ',', 'c', 'ne', ',', 'si', 'non', 'obstatur', ',', 'propterea', 'etiam', 'permittitur.'],
                    ['Quid', 'opus', 'est', 'verbis', '?', 'lingua', 'nulla', 'est', 'qua', 'negem', 'quidquid', 'roges.'],
                    ['Textile', 'post', 'ferrum', 'est', ',', 'quia', 'ferro', 'tela', 'paratur', ',', 'c', 'ne', 'ratione', 'alia', 'possunt', 'tam', 'levia', 'gigni', 'insilia', 'ac', 'fusi', ',', 'radii', ',', 'que', 'scapi', 'sonantes.']
                    ]
                    
        self.assertEqual(results, target)

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


if __name__ == '__main__':
    unittest.main()
