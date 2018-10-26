"""Test cltk.stop."""

__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.utils.importer import CorpusImporter
from cltk.stop.stop import Stoplist, BaseCorpusStoplist
from cltk.stop.greek.stops import STOPS_LIST as GREEK_STOPS
from cltk.stop.latin import STOPS_LIST as LATIN_STOPS
from cltk.stop.french.stops import STOPS_LIST as FRENCH_STOPS
from cltk.stop.middle_high_german.stops import STOPS_LIST as MHG_STOPS
from cltk.stop.classical_hindi.stops import STOPS_LIST as HINDI_STOPS
from cltk.stop.arabic.stopword_filter import stopwords_filter as arabic_stop_filter
from cltk.stop.old_norse.stops import STOPS_LIST as OLD_NORSE_STOPS
from cltk.stop.classical_chinese import CorpusStoplist as ClassicalChineseCorpusStoplist
from cltk.stop.latin import CorpusStoplist as LatinCorpusStoplist
from cltk.stop.akkadian.stops import STOP_LIST as AKKADIAN_STOPS
from cltk.tokenize.sentence import TokenizeSentence
from nltk.tokenize.punkt import PunktLanguageVars
from cltk.tokenize.word import WordTokenizer
import os
import sys
import unittest


class TestSequenceFunctions(unittest.TestCase):
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

    def test_greek_stopwords(self):
        """Test filtering Greek stopwords."""
        sentence = 'Ἅρπαγος δὲ καταστρεψάμενος Ἰωνίην ἐποιέετο στρατηίην \
        ἐπὶ Κᾶρας καὶ Καυνίους καὶ Λυκίους, ἅμα ἀγόμενος καὶ Ἴωνας καὶ \
        Αἰολέας.'
        lowered = sentence.lower()
        punkt = PunktLanguageVars()
        tokens = punkt.word_tokenize(lowered)
        no_stops = [w for w in tokens if w not in GREEK_STOPS]
        target_list = ['ἅρπαγος', 'καταστρεψάμενος', 'ἰωνίην', 'ἐποιέετο',
                       'στρατηίην', 'κᾶρας', 'καυνίους', 'λυκίους', ',',
                       'ἅμα', 'ἀγόμενος', 'ἴωνας', 'αἰολέας.']
        self.assertEqual(no_stops, target_list)

    def test_latin_stopwords(self):
        """Test filtering Latin stopwords."""
        sentence = 'Quo usque tandem abutere, Catilina, patientia nostra?'
        lowered = sentence.lower()
        punkt = PunktLanguageVars()
        tokens = punkt.word_tokenize(lowered)
        no_stops = [w for w in tokens if w not in LATIN_STOPS]
        target_list = ['usque', 'tandem', 'abutere', ',', 'catilina', ',',
                       'patientia', 'nostra', '?']
        self.assertEqual(no_stops, target_list)

    def test_arabic_stopwords(self):
        """Test filtering arabic stopwords."""
        sentence = 'سُئِل بعض الكُتَّاب عن الخَط، متى يَسْتحِقُ أن يُوصَف بِالجَودةِ؟'
        no_stops = arabic_stop_filter(sentence)
        target_list = ['سئل', 'الكتاب', 'الخط', '،', 'يستحق', 'يوصف', 'بالجودة', '؟']
        self.assertEqual(no_stops, target_list)

    def test_french_stopwords(self):
        ##test filtering French stopwords
        sentence = "En pensé ai e en talant que d ’ Yonec vus die avant dunt il fu nez, e de sun pere cum il vint primes a sa mere ."
        lowered = sentence.lower()
        punkt = PunktLanguageVars()
        tokens = punkt.word_tokenize(lowered)
        no_stops = [w for w in tokens if w not in FRENCH_STOPS]
        target_list = ['pensé', 'talant', 'd', '’', 'yonec', 'die', 'avant', 'dunt', 'nez', ',', 'pere', 'cum', 'primes',
                       'mere','.']
        self.assertEqual(no_stops, target_list)

    def test_old_norse_stopwords(self):
        """
        Test filtering Old Norse stopwords
        Sentence extracted from Eiríks saga rauða (http://www.heimskringla.no/wiki/Eir%C3%ADks_saga_rau%C3%B0a)
        """
        sentence = 'Þat var einn morgin, er þeir Karlsefni sá fyrir ofan rjóðrit flekk nökkurn, sem glitraði við þeim'
        lowered = sentence.lower()
        punkt = PunktLanguageVars()
        tokens = punkt.word_tokenize(lowered)
        no_stops = [w for w in tokens if w not in OLD_NORSE_STOPS]
        target_list = ['var', 'einn', 'morgin', ',', 'karlsefni', 'rjóðrit', 'flekk', 'nökkurn', ',', 'glitraði']
        self.assertEqual(no_stops, target_list)

    def test_akkadian_stopwords(self):
        """
        Test filtering Akkadian stopwrods
        Sentence extracted from the law code of Hammurabi, law 3 (Martha Roth 2nd Edition 1997, Law Collections from
        Mesopotamia and Asia Minor).
        """
        sentence = "šumma awīlum ina dīnim ana šībūt sarrātim ūṣiamma awat iqbû la uktīn šumma dīnum šû dīn napištim awīlum šû iddâk"
        lowered = sentence.lower()
        punkt = PunktLanguageVars()
        tokens = punkt.word_tokenize(lowered)
        no_stops = [w for w in tokens if w not in AKKADIAN_STOPS]
        target_list = ['awīlum', 'dīnim', 'šībūt', 'sarrātim', 'ūṣiamma', 'awat', 'iqbû', 'uktīn', 'dīnum',
                       'dīn', 'napištim', 'awīlum', 'iddâk']
        self.assertEqual(no_stops, target_list)

class TestStop_General(unittest.TestCase):
    """
    Class for unittests related specifically to stop.py
    """

    @classmethod
    def setUpClass(self):
        """
        Set up sample texts/corpus for testing stop.py
        """
        self.test_1 = """cogitanti mihi saepe numero et memoria vetera repetenti perbeati fuisse, quinte frater, illi videri solent, qui in optima re publica, cum et honoribus et rerum gestarum gloria florerent, eum vitae cursum tenere potuerunt, ut vel in negotio sine periculo vel in otio cum dignitate esse possent; ac fuit cum mihi quoque initium requiescendi atque animum ad utriusque nostrum praeclara studia referendi fore iustum et prope ab omnibus concessum arbitrarer, si infinitus forensium rerum labor et ambitionis occupatio decursu honorum, etiam aetatis flexu constitisset. quam spem cogitationum et consiliorum meorum cum graves communium temporum tum varii nostri casus fefellerunt; nam qui locus quietis et tranquillitatis plenissimus fore videbatur, in eo maximae moles molestiarum et turbulentissimae tempestates exstiterunt; neque vero nobis cupientibus atque exoptantibus fructus oti datus est ad eas artis, quibus a pueris dediti fuimus, celebrandas inter nosque recolendas. nam prima aetate incidimus in ipsam perturbationem disciplinae veteris, et consulatu devenimus in medium rerum omnium certamen atque discrimen, et hoc tempus omne post consulatum obiecimus eis fluctibus, qui per nos a communi peste depulsi in nosmet ipsos redundarent. sed tamen in his vel asperitatibus rerum vel angustiis temporis obsequar studiis nostris et quantum mihi vel fraus inimicorum vel causae amicorum vel res publica tribuet oti, ad scribendum potissimum conferam; tibi vero, frater, neque hortanti deero neque roganti, nam neque auctoritate quisquam apud me plus valere te potest neque voluntate."""

        self.test_2 = """ac mihi repetenda est veteris cuiusdam memoriae non sane satis explicata recordatio, sed, ut arbitror, apta ad id, quod requiris, ut cognoscas quae viri omnium eloquentissimi clarissimique senserint de omni ratione dicendi. vis enim, ut mihi saepe dixisti, quoniam, quae pueris aut adulescentulis nobis ex commentariolis nostris incohata ac rudia exciderunt, vix sunt hac aetate digna et hoc usu, quem ex causis, quas diximus, tot tantisque consecuti sumus, aliquid eisdem de rebus politius a nobis perfectiusque proferri; solesque non numquam hac de re a me in disputationibus nostris dissentire, quod ego eruditissimorum hominum artibus eloquentiam contineri statuam, tu autem illam ab elegantia doctrinae segregandam putes et in quodam ingeni atque exercitationis genere ponendam. ac mihi quidem saepe numero in summos homines ac summis ingeniis praeditos intuenti quaerendum esse visum est quid esset cur plures in omnibus rebus quam in dicendo admirabiles exstitissent; nam quocumque te animo et cogitatione converteris, permultos excellentis in quoque genere videbis non mediocrium artium, sed prope maximarum. quis enim est qui, si clarorum hominum scientiam rerum gestarum vel utilitate vel magnitudine metiri velit, non anteponat oratori imperatorem? quis autem dubitet quin belli duces ex hac una civitate praestantissimos paene innumerabilis, in dicendo autem excellentis vix paucos proferre possimus? iam vero consilio ac sapientia qui regere ac gubernare rem publicam possint, multi nostra, plures patrum memoria atque etiam maiorum exstiterunt, cum boni perdiu nulli, vix autem singulis aetatibus singuli tolerabiles oratores invenirentur. ac ne qui forte cum aliis studiis, quae reconditis in artibus atque in quadam varietate litterarum versentur, magis hanc dicendi rationem, quam cum imperatoris laude aut cum boni senatoris prudentia comparandam putet, convertat animum ad ea ipsa artium genera circumspiciatque, qui in eis floruerint quamque multi sint; sic facillime, quanta oratorum sit et semper fuerit paucitas, iudicabit."""

        self.test_corpus = [self.test_1, self.test_2]

    def test_corpus_stop_list_freq(self):
        """Test production of stoplists from a corpus, using basis: frequency"""
        target_list = ['ac', 'ad', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'vel']

        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10,
                    basis='frequency', inc_values=False)
        self.assertEqual(stoplist, target_list)

    def test_corpus_stop_list_freq_inc_values(self):
        """Test production of stoplists from a corpus with values,
        using basis: frequency"""
        target_list = [('ac', 8), ('ad', 5), ('atque', 6), ('cum', 8),
                        ('et', 15), ('in', 18), ('mihi', 6), ('neque', 5),
                        ('qui', 7), ('vel', 9)]
        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10,
                    basis='frequency', inc_values=True)
        self.assertEqual(stoplist, target_list)

    def test_corpus_stop_list_tfidf(self):
        """Test production of stoplists from a corpus, using basis: frequency"""
        target_list = ['ac', 'atque', 'autem', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'vel']

        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10,
                    basis='tfidf', inc_values=False)
        self.assertEqual(stoplist, target_list)

    def test_corpus_stop_list_freq_exclude(self):
        """Test production of stoplists from a corpus, using basis: frequency"""
        target_list = ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'vel']

        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10,
                    basis='frequency', inc_values=False, exclude=['ad'])
        self.assertEqual(stoplist, target_list)

    def test_corpus_stop_list_freq_include(self):
        """Test production of stoplists from a corpus, using basis: frequency"""
        target_list = ['ac', 'ad', 'atque', 'cum', 'est', 'et', 'in', 'mihi', 'neque', 'qui', 'vel']
        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10, basis='frequency', include=['est'])
        self.assertEqual(stoplist, target_list)

    def test_corpus_stop_list_freq_sort_words(self):
        """Test production of stoplists from a corpus, using basis: frequency"""
        target_list = ['in', 'et', 'vel', 'ac', 'cum', 'qui', 'atque', 'mihi', 'ad', 'neque']

        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10,
                    basis='frequency', inc_values=False, sort_words=False)
        self.assertEqual(stoplist, target_list)

    def test_corpus_stop_list_mean(self):
        """Test production of stoplists from a corpus, using basis: mean"""
        target_list = ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'rerum', 'vel']

        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10,
                    basis='mean', inc_values=False)
        self.assertEqual(stoplist, target_list)

    def test_corpus_stop_list_variance(self):
        """Test production of stoplists from a corpus, using basis: variance"""
        target_list = ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'rerum', 'vel']
        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10,
                    basis='variance', inc_values=False)
        self.assertEqual(stoplist, target_list)

    def test_corpus_stop_list_variance(self):
        """Test production of stoplists from a corpus, using basis: variance"""
        target_list = ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'rerum', 'vel']
        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10,basis='variance')
        self.assertEqual(stoplist, target_list)

    def test_corpus_stop_list_entropy(self):
        """Test production of stoplists from a corpus, using basis: entropy"""
        target_list = ['ac', 'ad', 'atque', 'cum', 'et', 'in', 'mihi', 'qui', 'rerum', 'vel']
        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10,
                    basis='entropy', inc_values=False)
        self.assertEqual(stoplist, target_list)

    def test_corpus_stop_list_zou(self):
        """Test production of stoplists from a corpus, using basis: zou"""
        target_list = ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque',
                        'qui', 'rerum', 'vel']
        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.test_corpus, size=10,
                    basis='zou', inc_values=False)
        self.assertEqual(stoplist, target_list)


class TestStop_LanguageSpecific(unittest.TestCase):
    """
    Class for language-specific unittests
    """

    @classmethod
    def setUpClass(self):
        """
        Set up sample texts/corpus for testing stop.py
        """
        self.test_1 = """cogitanti mihi saepe numero et memoria vetera repetenti perbeati fuisse, quinte frater, illi videri solent, qui in optima re publica, cum et honoribus et rerum gestarum gloria florerent, eum vitae cursum tenere potuerunt, ut vel in negotio sine periculo vel in otio cum dignitate esse possent; ac fuit cum mihi quoque initium requiescendi atque animum ad utriusque nostrum praeclara studia referendi fore iustum et prope ab omnibus concessum arbitrarer, si infinitus forensium rerum labor et ambitionis occupatio decursu honorum, etiam aetatis flexu constitisset. quam spem cogitationum et consiliorum meorum cum graves communium temporum tum varii nostri casus fefellerunt; nam qui locus quietis et tranquillitatis plenissimus fore videbatur, in eo maximae moles molestiarum et turbulentissimae tempestates exstiterunt; neque vero nobis cupientibus atque exoptantibus fructus oti datus est ad eas artis, quibus a pueris dediti fuimus, celebrandas inter nosque recolendas. nam prima aetate incidimus in ipsam perturbationem disciplinae veteris, et consulatu devenimus in medium rerum omnium certamen atque discrimen, et hoc tempus omne post consulatum obiecimus eis fluctibus, qui per nos a communi peste depulsi in nosmet ipsos redundarent. sed tamen in his vel asperitatibus rerum vel angustiis temporis obsequar studiis nostris et quantum mihi vel fraus inimicorum vel causae amicorum vel res publica tribuet oti, ad scribendum potissimum conferam; tibi vero, frater, neque hortanti deero neque roganti, nam neque auctoritate quisquam apud me plus valere te potest neque voluntate."""

        self.test_2 = """ac mihi repetenda est veteris cuiusdam memoriae non sane satis explicata recordatio, sed, ut arbitror, apta ad id, quod requiris, ut cognoscas quae viri omnium eloquentissimi clarissimique senserint de omni ratione dicendi. vis enim, ut mihi saepe dixisti, quoniam, quae pueris aut adulescentulis nobis ex commentariolis nostris incohata ac rudia exciderunt, vix sunt hac aetate digna et hoc usu, quem ex causis, quas diximus, tot tantisque consecuti sumus, aliquid eisdem de rebus politius a nobis perfectiusque proferri; solesque non numquam hac de re a me in disputationibus nostris dissentire, quod ego eruditissimorum hominum artibus eloquentiam contineri statuam, tu autem illam ab elegantia doctrinae segregandam putes et in quodam ingeni atque exercitationis genere ponendam. ac mihi quidem saepe numero in summos homines ac summis ingeniis praeditos intuenti quaerendum esse visum est quid esset cur plures in omnibus rebus quam in dicendo admirabiles exstitissent; nam quocumque te animo et cogitatione converteris, permultos excellentis in quoque genere videbis non mediocrium artium, sed prope maximarum. quis enim est qui, si clarorum hominum scientiam rerum gestarum vel utilitate vel magnitudine metiri velit, non anteponat oratori imperatorem? quis autem dubitet quin belli duces ex hac una civitate praestantissimos paene innumerabilis, in dicendo autem excellentis vix paucos proferre possimus? iam vero consilio ac sapientia qui regere ac gubernare rem publicam possint, multi nostra, plures patrum memoria atque etiam maiorum exstiterunt, cum boni perdiu nulli, vix autem singulis aetatibus singuli tolerabiles oratores invenirentur. ac ne qui forte cum aliis studiis, quae reconditis in artibus atque in quadam varietate litterarum versentur, magis hanc dicendi rationem, quam cum imperatoris laude aut cum boni senatoris prudentia comparandam putet, convertat animum ad ea ipsa artium genera circumspiciatque, qui in eis floruerint quamque multi sint; sic facillime, quanta oratorum sit et semper fuerit paucitas, iudicabit."""

        self.latin_test_corpus = [self.test_1, self.test_2]

    def test_corpus_latin(self):
        """Test production of Latin stoplists from a corpus"""
        target_list = ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque',
                        'qui', 'rerum', 'vel']
        S = LatinCorpusStoplist()
        stoplist = S.build_stoplist(self.latin_test_corpus, size=10,
                    basis='zou', inc_values=False)

        self.assertEqual(stoplist, target_list)


class TestPackageImports(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.S = Stoplist()
        self.S.numpy_installed = False
        self.S.sklearn_installed = False

    def test_numpy_installed(self):
        self.assertFalse(self.S.numpy_installed)

    def test_sklearn_installed(self):
        self.assertFalse(self.S.sklearn_installed)

    def test_middle_high_german_stopwords(self):
        """Test filtering  Middle High German stopwords."""

        sentence = "Swer was ze Bêârosche komn, doch hete Gâwân dâ genomn den prîs ze bêder sît al ein wan daz dervor ein ritter schein, bî rôtem wâpen unrekant, des prîs man in die hœhe bant."
        lowered = sentence.lower()
        tokenizer = WordTokenizer('middle_high_german')
        tokens = tokenizer.tokenize(lowered)
        no_stops = [w for w in tokens if w not in MHG_STOPS]
        target_list = ['swer', 'bêârosche', 'komn', ',', 'gâwân', 'genomn', 'prîs', 'bêder', 'sît', 'dervor', 'ritter', 'schein', ',', 'rôtem', 'wâpen', 'unrekant', ',', 'prîs', 'hœhe', 'bant', '.']
        self.assertEqual(no_stops,target_list)

    def test_classical_hindi_stops(self):
        """
        Test filtering classical hindi stopwords
        Sentence extracted from (https://github.com/cltk/hindi_text_ltrc/blob/master/miscellaneous/gandhi/main.txt)
        """
        sentence = " वह काबुली फिर वहां आकर खडा हो गया है  "
        tokenizer = TokenizeSentence('hindi')
        tokens = tokenizer.tokenize(sentence)
        no_stops = [word for word in tokens if word not in HINDI_STOPS]
        target_list = ['काबुली', 'फिर', 'वहां', 'आकर', 'खडा', 'गया']
        self.assertEqual(no_stops, target_list)


if __name__ == '__main__':
    unittest.main()
