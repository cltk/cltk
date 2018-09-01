# -*-coding:utf-8-*-
"""Test cltk.tokenize.

"""

from cltk.corpus.utils.importer import CorpusImporter
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import nltk_tokenize_words
from cltk.tokenize.word import WordTokenizer
from cltk.tokenize.line import LineTokenizer

import os
import unittest

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
#        corpus_importer.import_corpus('latin_models_cltk')
        file_rel = os.path.join('~/cltk_data/latin/model/latin_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        if file_exists:
            self.assertTrue(file_exists)
        else:
            corpus_importer.import_corpus('latin_models_cltk')
        self.assertTrue(file_exists)

    def test_sentence_tokenizer_latin(self):
        """Test tokenizing Latin sentences."""
        text = "O di inmortales! ubinam gentium sumus? in qua urbe vivimus? quam rem publicam habemus? Hic, hic sunt in nostro numero, patres conscripti, in hoc orbis terrae sanctissimo gravissimoque consilio, qui de nostro omnium interitu, qui de huius urbis atque adeo de orbis terrarum exitio cogitent! Hos ego video consul et de re publica sententiam rogo et, quos ferro trucidari oportebat, eos nondum voce volnero! Fuisti igitur apud Laecam illa nocte, Catilina, distribuisti partes Italiae, statuisti, quo quemque proficisci placeret, delegisti, quos Romae relinqueres, quos tecum educeres, discripsisti urbis partes ad incendia, confirmasti te ipsum iam esse exiturum, dixisti paulum tibi esse etiam nunc morae, quod ego viverem."  # pylint: disable=line-too-long
        target = ['O di inmortales!', 'ubinam gentium sumus?', 'in qua urbe vivimus?', 'quam rem publicam habemus?', 'Hic, hic sunt in nostro numero, patres conscripti, in hoc orbis terrae sanctissimo gravissimoque consilio, qui de nostro omnium interitu, qui de huius urbis atque adeo de orbis terrarum exitio cogitent!', 'Hos ego video consul et de re publica sententiam rogo et, quos ferro trucidari oportebat, eos nondum voce volnero!', 'Fuisti igitur apud Laecam illa nocte, Catilina, distribuisti partes Italiae, statuisti, quo quemque proficisci placeret, delegisti, quos Romae relinqueres, quos tecum educeres, discripsisti urbis partes ad incendia, confirmasti te ipsum iam esse exiturum, dixisti paulum tibi esse etiam nunc morae, quod ego viverem.']  # pylint: disable=line-too-long
        tokenizer = TokenizeSentence('latin')
        tokenized_sentences = tokenizer.tokenize_sentences(text)
        self.assertEqual(tokenized_sentences, target)


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


    def test_greek_word_tokenizer(self):
        """Test Latin-specific word tokenizer."""
        word_tokenizer = WordTokenizer('greek')
        
        # Test sources:
        # - Thuc. 1.1.1       
        
        test = "Θουκυδίδης Ἀθηναῖος ξυνέγραψε τὸν πόλεμον τῶν Πελοποννησίων καὶ Ἀθηναίων, ὡς ἐπολέμησαν πρὸς ἀλλήλους, ἀρξάμενος εὐθὺς καθισταμένου καὶ ἐλπίσας μέγαν τε ἔσεσθαι καὶ ἀξιολογώτατον τῶν προγεγενημένων, τεκμαιρόμενος ὅτι ἀκμάζοντές τε ᾖσαν ἐς αὐτὸν ἀμφότεροι παρασκευῇ τῇ πάσῃ καὶ τὸ ἄλλο Ἑλληνικὸν ὁρῶν ξυνιστάμενον πρὸς ἑκατέρους, τὸ μὲν εὐθύς, τὸ δὲ καὶ διανοούμενον."

        target = ['Θουκυδίδης', 'Ἀθηναῖος', 'ξυνέγραψε', 'τὸν', 'πόλεμον', 'τῶν', 'Πελοποννησίων', 'καὶ', 'Ἀθηναίων', ',', 'ὡς', 'ἐπολέμησαν', 'πρὸς', 'ἀλλήλους', ',', 'ἀρξάμενος', 'εὐθὺς', 'καθισταμένου', 'καὶ', 'ἐλπίσας', 'μέγαν', 'τε', 'ἔσεσθαι', 'καὶ', 'ἀξιολογώτατον', 'τῶν', 'προγεγενημένων', ',', 'τεκμαιρόμενος', 'ὅτι', 'ἀκμάζοντές', 'τε', 'ᾖσαν', 'ἐς', 'αὐτὸν', 'ἀμφότεροι', 'παρασκευῇ', 'τῇ', 'πάσῃ', 'καὶ', 'τὸ', 'ἄλλο', 'Ἑλληνικὸν', 'ὁρῶν', 'ξυνιστάμενον', 'πρὸς', 'ἑκατέρους', ',', 'τὸ', 'μὲν', 'εὐθύς', ',', 'τὸ', 'δὲ', 'καὶ', 'διανοούμενον', '.']

        result = word_tokenizer.tokenize(test)

        self.assertEqual(result, target)

        
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
        # - Plaut. Bacch. 837-38
        # - Plaut. Amph. 823
        # - Caes. Bel. 6.29.2

        tests = ['Arma virumque cano, Troiae qui primus ab oris.',
                    'Hoc verumst, tota te ferri, Cynthia, Roma, et non ignota vivere nequitia?',
                    'Nec te decipiant veteres circum atria cerae. Tolle tuos tecum, pauper amator, avos!',
                    'Neque enim, quod quisque potest, id ei licet, nec, si non obstatur, propterea etiam permittitur.',
                    'Quid opust verbis? lingua nullast qua negem quidquid roges.',
                    'Textile post ferrumst, quia ferro tela paratur, nec ratione alia possunt tam levia gigni insilia ac fusi, radii, scapique sonantes.',  # pylint: disable=line-too-long
                    'Dic sodes mihi, bellan videtur specie mulier?',
                    'Cenavin ego heri in navi in portu Persico?',
                    'quae ripas Ubiorum contingebat in longitudinem pedum ducentorum rescindit']

        results = []

        for test in tests:
            result = word_tokenizer.tokenize(test)
            results.append(result)

        target = [['Arma', 'virum', '-que', 'cano', ',', 'Troiae', 'qui', 'primus', 'ab', 'oris', '.'],
                  ['Hoc', 'verum', 'est', ',', 'tota', 'te', 'ferri', ',', 'Cynthia', ',', 'Roma', ',', 'et', 'non', 'ignota', 'vivere', 'nequitia', '?'],  # pylint: disable=line-too-long
                  ['Nec', 'te', 'decipiant', 'veteres', 'circum', 'atria', 'cerae', '.', 'Tolle', 'tuos', 'cum', 'te', ',', 'pauper', 'amator', ',', 'avos', '!'],  # pylint: disable=line-too-long
                  ['Neque', 'enim', ',', 'quod', 'quisque', 'potest', ',', 'id', 'ei', 'licet', ',', 'nec', ',', 'si', 'non', 'obstatur', ',', 'propterea', 'etiam', 'permittitur', '.'],  # pylint: disable=line-too-long
                  ['Quid', 'opus', 'est', 'verbis', '?', 'lingua', 'nulla', 'est', 'qua', 'negem', 'quidquid', 'roges', '.'],  # pylint: disable=line-too-long
                  ['Textile', 'post', 'ferrum', 'est', ',', 'quia', 'ferro', 'tela', 'paratur', ',', 'nec', 'ratione', 'alia', 'possunt', 'tam', 'levia', 'gigni', 'insilia', 'ac', 'fusi', ',', 'radii', ',', 'scapi', '-que', 'sonantes', '.'],  # pylint: disable=line-too-long
                  ['Dic', 'si', 'audes', 'mihi', ',', 'bella', '-ne', 'videtur', 'specie', 'mulier', '?'],
                  ['Cenavi', '-ne', 'ego', 'heri', 'in', 'navi', 'in', 'portu', 'Persico', '?'],
                  ['quae', "ripas", "Ubiorum", "contingebat", "in", "longitudinem", "pedum", "ducentorum", "rescindit"]
                  ]

        self.assertEqual(results, target)

    def test_tokenize_arabic_words(self):
        word_tokenizer = WordTokenizer('arabic')
        tests = ['اللُّغَةُ الْعَرَبِيَّةُ جَمِيلَةٌ.',
                 'انما الْمُؤْمِنُونَ اخوه فاصلحوا بَيْنَ اخويكم',
                 'الْعَجُزُ عَنِ الْإِدْرَاكِ إِدْرَاكٌ، وَالْبَحْثَ فِي ذاتِ اللَّه اشراك.',
                 'اللَّهُمُّ اُسْتُرْ عُيُوبَنَا وَأَحْسَنَ خَوَاتِيمَنَا الْكَاتِبِ: نَبِيلُ جلهوم',
                 'الرَّأْي قَبْلَ شَجَاعَة الشّجعَانِ',
                 'فَأَنْزَلْنَا مِنْ السَّمَاء مَاء فَأَسْقَيْنَاكُمُوهُ',
                 'سُئِلَ بَعْضُ الْكُتَّابِ عَنِ الْخَطّ، مَتَى يَسْتَحِقُّ أَنْ يُوصَفَ بِالْجَوْدَةِ ؟'
                ]

        results = []
        for test in tests:
            result = word_tokenizer.tokenize(test)
            results.append(result)

        target = [['اللُّغَةُ', 'الْعَرَبِيَّةُ', 'جَمِيلَةٌ', '.'],
                  ['انما', 'الْمُؤْمِنُونَ', 'اخوه', 'فاصلحوا', 'بَيْنَ', 'اخويكم'],
                  ['الْعَجُزُ', 'عَنِ', 'الْإِدْرَاكِ', 'إِدْرَاكٌ', '،', 'وَالْبَحْثَ', 'فِي', 'ذاتِ', 'اللَّه', 'اشراك', '.'],  # pylint: disable=line-too-long
                  ['اللَّهُمُّ', 'اُسْتُرْ', 'عُيُوبَنَا', 'وَأَحْسَنَ', 'خَوَاتِيمَنَا', 'الْكَاتِبِ', ':', 'نَبِيلُ', 'جلهوم'],  # pylint: disable=line-too-long
                  ['الرَّأْي', 'قَبْلَ', 'شَجَاعَة', 'الشّجعَانِ'],
                  ['فَأَنْزَلْنَا', 'مِنْ', 'السَّمَاء', 'مَاء', 'فَأَسْقَيْنَاكُمُوهُ'],
                  ['سُئِلَ', 'بَعْضُ', 'الْكُتَّابِ', 'عَنِ', 'الْخَطّ', '،', 'مَتَى', 'يَسْتَحِقُّ', 'أَنْ', 'يُوصَفَ', 'بِالْجَوْدَةِ', '؟']  # pylint: disable=line-too-long
                 ]
        self.assertEqual(results, target)

    def test_word_tokenizer_french(self):
        word_tokenizer = WordTokenizer('french')

        tests = ["S'a table te veulz maintenir, Honnestement te dois tenir Et garder les enseignemens Dont cilz vers sont commancemens."]  # pylint: disable=line-too-long

        results = []

        for test in tests:
            result = word_tokenizer.tokenize(test)
            results.append(result)

        target = [["S'", 'a', 'table', 'te', 'veulz', 'maintenir', ',', 'Honnestement', 'te', 'dois', 'tenir', 'Et', 'garder', 'les', 'enseignemens', 'Dont', 'cilz', 'vers', 'sont', 'commancemens', '.']]  # pylint: disable=line-too-long

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

    def test_sanskrit_nltk_tokenize_words(self):
        """Test wrapper for NLTK's PunktLanguageVars()"""
        tokens = nltk_tokenize_words("कृपया।", attached_period=False, language='sanskrit')
        target = ['कृपया', '।']
        self.assertEqual(tokens, target)

    def test_sanskrit_nltk_tokenize_words_attached(self):
        """Test wrapper for NLTK's PunktLanguageVars(), returning unaltered output."""
        tokens = nltk_tokenize_words("कृपया।", attached_period=True, language='sanskrit')
        target = ['कृपया।']
        self.assertEqual(tokens, target)

    def test_nltk_tokenize_words_assert(self):
        """Test assert error for CLTK's word tokenizer."""
        with self.assertRaises(AssertionError):
            nltk_tokenize_words(['Sentence', '1.'])

    def test_line_tokenizer(self):
        """Test LineTokenizer"""
        text = """49. Miraris verbis nudis me scribere versus?\nHoc brevitas fecit, sensus coniungere binos."""
        target = ['49. Miraris verbis nudis me scribere versus?','Hoc brevitas fecit, sensus coniungere binos.']
        tokenizer = LineTokenizer('latin')
        tokenized_lines = tokenizer.tokenize(text)
        self.assertTrue(tokenized_lines == target)

    def test_line_tokenizer_include_blanks(self):
        """Test LineTokenizer"""
        text = """48. Cum tibi contigerit studio cognoscere multa,\nFac discas multa, vita nil discere velle.\n\n49. Miraris verbis nudis me scribere versus?\nHoc brevitas fecit, sensus coniungere binos."""  # pylint: disable=line-too-long
        target = ['48. Cum tibi contigerit studio cognoscere multa,','Fac discas multa, vita nil discere velle.','','49. Miraris verbis nudis me scribere versus?','Hoc brevitas fecit, sensus coniungere binos.']  # pylint: disable=line-too-long
        tokenizer = LineTokenizer('latin')
        tokenized_lines = tokenizer.tokenize(text, include_blanks=True)
        self.assertTrue(tokenized_lines == target)

    def test_french_line_tokenizer(self):
        """Test LineTokenizer"""
        text = """Ki de bone matire traite,\nmult li peise, se bien n’est faite.\nOëz, seignur, que dit Marie,\nki en sun tens pas ne s’oblie. """  # pylint: disable=line-too-long
        target = ['Ki de bone matire traite,', 'mult li peise, se bien n’est faite.','Oëz, seignur, que dit Marie,', 'ki en sun tens pas ne s’oblie. ']  # pylint: disable=line-too-long
        tokenizer = LineTokenizer('french')
        tokenized_lines = tokenizer.tokenize(text)
        self.assertTrue(tokenized_lines == target)

    def test_french_line_tokenizer_include_blanks(self):
        """Test LineTokenizer"""
        text = """Ki de bone matire traite,\nmult li peise, se bien n’est faite.\nOëz, seignur, que dit Marie,\nki en sun tens pas ne s’oblie.\n\nLes contes que jo sai verais,\ndunt li Bretun unt fait les lais,\nvos conterai assez briefment."""  # pylint: disable=line-too-long
        target = ['Ki de bone matire traite,', 'mult li peise, se bien n’est faite.', 'Oëz, seignur, que dit Marie,', 'ki en sun tens pas ne s’oblie.','','Les contes que jo sai verais,','dunt li Bretun unt fait les lais,','vos conterai assez briefment.']  # pylint: disable=line-too-long
        tokenizer = LineTokenizer('french')
        tokenized_lines = tokenizer.tokenize(text, include_blanks=True)
        self.assertTrue(tokenized_lines == target)

    def test_old_norse_word_tokenizer(self):
        text = "Gylfi konungr var maðr vitr ok fjölkunnigr. " \
               "Hann undraðist þat mjök, er ásafólk var svá kunnigt, at allir hlutir gengu at vilja þeira."
        target = ['Gylfi', 'konungr', 'var', 'maðr', 'vitr', 'ok', 'fjölkunnigr', '.', 'Hann', 'undraðist', 'þat',
                  'mjök', ',', 'er', 'ásafólk', 'var', 'svá', 'kunnigt', ',', 'at', 'allir', 'hlutir', 'gengu', 'at',
                  'vilja', 'þeira', '.']
        word_tokenizer = WordTokenizer('old_norse')
        result = word_tokenizer.tokenize(text)
        self.assertTrue(result == target)
        
    def test_middle_english_tokenizer(self):
        text = "    Fers am I ferd of oure fare;\n Fle we ful fast þer-fore. \n Can Y no cownsel bot care.\n\n"
        target = ['Fers', 'am', 'I', 'ferd', 'of', 'oure', 'fare', ';', 'Fle', 'we', 'ful', 'fast', 'þer', '-', 'fore', '.',
                  'Can', 'Y', 'no', 'cownsel', 'bot', 'care', '.']
        tokenizer = WordTokenizer('middle_english')
        tokenized = tokenizer.tokenize(text)
        self.assertTrue(tokenized == target)
    
    def test_middle_high_german_tokenizer(self):
        text = "Gâwân het êre unde heil,\nieweders volleclîchen teil:\nnu nâht och sînes kampfes zît."
        target = ['Gâwân', 'het', 'êre', 'unde', 'heil', ',', 'ieweders', 'volleclîchen', 'teil', ':', 'nu', 'nâht', 'och', 'sînes', 'kampfes', 'zît', '.']
        tokenizer = WordTokenizer('middle_high_german')
        tokenized_lines = tokenizer.tokenize(text)
        self.assertTrue(tokenized_lines == target)

    def test_sentence_tokenizer_bengali(self):
        """Test tokenizing bengali sentences."""
        text = "দুর্ব্বাসার শাপে রাজা শকুন্তলাকে একেবারে ভুলে বেশ সুখে আছেন।"
        target = ['দুর্ব্বাসার', 'শাপে', 'রাজা', 'শকুন্তলাকে', 'একেবারে', 'ভুলে', 'বেশ', 'সুখে', 'আছেন', '।']
        tokenizer = TokenizeSentence('bengali')
        tokenized_sentences = tokenizer.tokenize(text)
        self.assertEqual(tokenized_sentences, target)

    def test_sentence_tokenizer_classical_hindi(self):
        """Test tokenizing classical_hindi sentences."""
        text = "जलर्  चिकित्सा से उन्हें कोई लाभ नहीं हुआ।"
        target = ['जलर्', 'चिकित्सा', 'से', 'उन्हें', 'कोई', 'लाभ', 'नहीं', 'हुआ', '।']
        tokenizer = TokenizeSentence('hindi')
        tokenized_sentences = tokenizer.tokenize(text)
        self.assertEqual(tokenized_sentences, target)

    def test_sentence_tokenizer_marathi(self):
        """Test tokenizing marathi sentences."""
        text = "अर्जुन उवाच । एवं सतत युक्ता ये भक्तास्त्वां पर्युपासते । ये चाप्यक्षरमव्यक्तं तेषां के योगवित्तमाः ॥"
        target = ['अर्जुन', 'उवाच', '।', 'एवं', 'सतत', 'युक्ता', 'ये', 'भक्तास्त्वां', 'पर्युपासते', '।', 'ये', 'चाप्यक्षरमव्यक्तं', 'तेषां', 'के', 'योगवित्तमाः', '॥']
        tokenizer = TokenizeSentence('marathi')
        tokenized_sentences = tokenizer.tokenize(text)
        self.assertEqual(tokenized_sentences, target)

    def test_sentence_tokenizer_sanskrit(self):
        """Test tokenizing sanskrit sentences."""
        text = "श्री भगवानुवाच पश्य मे पार्थ रूपाणि शतशोऽथ सहस्रशः। नानाविधानि दिव्यानि नानावर्णाकृतीनि च।।"
        target = ['श्री', 'भगवानुवाच', 'पश्य', 'मे', 'पार्थ', 'रूपाणि', 'शतशोऽथ', 'सहस्रशः', '।', 'नानाविधानि', 'दिव्यानि', 'नानावर्णाकृतीनि', 'च', '।', '।']
        tokenizer = TokenizeSentence('sanskrit')
        tokenized_sentences = tokenizer.tokenize(text)
        self.assertEqual(tokenized_sentences, target)

    def test_sentence_tokenizer_telugu(self):
        """Test tokenizing telugu sentences."""
        text = "తా. ఎక్కడెక్కడ బుట్టిన నదులును రత్నాకరుడను నాశతో సముద్రుని చేరువిధముగా నెన్నియిక్కట్టులకైన నోర్చి ప్రజలు దమంతట దామె ప్రియముం జూపుచు ధనికుని యింటికేతెంచుచుందురు."
        target = ['తా', '.', 'ఎక్కడెక్కడ', 'బుట్టిన', 'నదులును', 'రత్నాకరుడను', 'నాశతో', 'సముద్రుని', 'చేరువిధముగా', 'నెన్నియిక్కట్టులకైన', 'నోర్చి', 'ప్రజలు', 'దమంతట', 'దామె', 'ప్రియముం', 'జూపుచు', 'ధనికుని', 'యింటికేతెంచుచుందురు', '.']
        tokenizer = TokenizeSentence('telugu')
        tokenized_sentences = tokenizer.tokenize(text)
        self.assertEqual(tokenized_sentences, target)
    def test_akkadian_word_tokenizer(self):
        """
        Tests word_tokenizer.
        """
        tokenizer = WordTokenizer('akkadian')
        line = 'u2-wa-a-ru at-ta e2-kal2-la-ka _e2_-ka wu-e-er'
        output = tokenizer.tokenize(line)
        goal = [('u2-wa-a-ru', 'akkadian'), ('at-ta', 'akkadian'),
                ('e2-kal2-la-ka', 'akkadian'),
                ('_e2_-ka', 'sumerian'), ('wu-e-er', 'akkadian')]
        self.assertEqual(output, goal)

    def test_akkadian_sign_tokenizer(self):
        """
        Tests sign_tokenizer.
        """
        tokenizer = WordTokenizer('akkadian')
        word = ("{gisz}isz-pur-ram", "akkadian")
        output = tokenizer.tokenize_sign(word)
        goal = [("gisz", "determinative"), ("isz", "akkadian"),
                ("pur", "akkadian"), ("ram", "akkadian")]
        self.assertEqual(output, goal)


if __name__ == '__main__':
    unittest.main()
