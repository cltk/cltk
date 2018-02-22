"""Test cltk.stop."""

__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.utils.importer import CorpusImporter
from cltk.stop.stop import Stoplist, StringStoplist, CorpusStoplist
from cltk.stop.greek.stops import STOPS_LIST as GREEK_STOPS
from cltk.stop.latin.stops import STOPS_LIST as LATIN_STOPS
from cltk.stop.french.stops import STOPS_LIST as FRENCH_STOPS
from cltk.stop.middle_high_german.stops import STOPS_LIST as MHG_STOPS
from cltk.stop.classical_hindi.stops import STOPS_LIST as HINDI_STOPS
from cltk.stop.arabic.stopword_filter import stopwords_filter as arabic_stop_filter
from cltk.stop.old_norse.stops import STOPS_LIST as OLD_NORSE_STOPS
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

    def test_string_stop_list(self):
        """Test production of stoplists from a given string"""
        text = """
        Cogitanti mihi saepe numero et memoria vetera repetenti perbeati fuisse, Quinte frater, illi videri solent, qui in optima re publica, cum et honoribus et rerum gestarum gloria florerent, eum vitae cursum tenere potuerunt, ut vel in negotio sine periculo vel in otio cum dignitate esse possent; ac fuit cum mihi quoque initium requiescendi atque animum ad utriusque nostrum praeclara studia referendi fore iustum et prope ab omnibus concessum arbitrarer, si infinitus forensium rerum labor et ambitionis occupatio decursu honorum, etiam aetatis flexu constitisset. [2] Quam spem cogitationum et consiliorum meorum cum graves communium temporum tum varii nostri casus fefellerunt; nam qui locus quietis et tranquillitatis plenissimus fore videbatur, in eo maximae moles molestiarum et turbulentissimae tempestates exstiterunt; neque vero nobis cupientibus atque exoptantibus fructus oti datus est ad eas artis, quibus a pueris dediti fuimus, celebrandas inter nosque recolendas. [3] Nam prima aetate incidimus in ipsam perturbationem disciplinae veteris, et consulatu devenimus in medium rerum omnium certamen atque discrimen, et hoc tempus omne post consulatum obiecimus eis fluctibus, qui per nos a communi peste depulsi in nosmet ipsos redundarent. Sed tamen in his vel asperitatibus rerum vel angustiis temporis obsequar studiis nostris et quantum mihi vel fraus inimicorum vel causae amicorum vel res publica tribuet oti, ad scribendum potissimum conferam; [4] tibi vero, frater, neque hortanti deero neque roganti, nam neque auctoritate quisquam apud me plus valere te potest neque voluntate.
        """
        target_list = ['a', 'ab', 'ac', 'ad', 'aetatis', 'ambitionis', 'animum', 'arbitrarer', 'atque', 'casus', 'cogitanti', 'cogitationum', 'communium', 'concessum', 'consiliorum', 'constitisset', 'cum', 'cursum', 'decursu', 'dignitate', 'eo', 'esse', 'et', 'etiam', 'eum', 'fefellerunt', 'flexu', 'florerent', 'fore', 'forensium', 'frater', 'fuisse', 'fuit', 'gestarum', 'gloria', 'graves', 'honoribus', 'honorum', 'illi', 'in', 'infinitus', 'initium', 'iustum', 'labor', 'locus', 'maximae', 'memoria', 'meorum', 'mihi', 'moles', 'molestiarum', 'nam', 'negotio', 'neque', 'nostri', 'nostrum', 'numero', 'occupatio', 'omnibus', 'optima', 'oti', 'otio', 'perbeati', 'periculo', 'plenissimus', 'possent', 'potuerunt', 'praeclara', 'prope', 'publica', 'quam', 'qui', 'quietis', 'quinte', 'quoque', 're', 'referendi', 'repetenti', 'requiescendi', 'rerum', 'saepe', 'si', 'sine', 'solent', 'spem', 'studia', 'temporum', 'tenere', 'tranquillitatis', 'tum', 'turbulentissimae', 'ut', 'utriusque', 'varii', 'vel', 'vero', 'vetera', 'videbatur', 'videri', 'vitae']
        stoplist = StringStoplist('latin').build_stoplist(text)
        self.assertEqual(stoplist, target_list)

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
        
         
    def test_string_stop_list(self):
        """Test production of stoplists from a given string"""
        target_list = ['a', 'ab', 'ac', 'ad', 'aetatis', 'ambitionis', 'animum', 'arbitrarer', 'atque', 'casus', 'cogitanti', 'cogitationum', 'communium', 'concessum', 'consiliorum', 'constitisset', 'cum', 'cursum', 'decursu', 'dignitate', 'eo', 'esse', 'et', 'etiam', 'eum', 'fefellerunt', 'flexu', 'florerent', 'fore', 'forensium', 'frater', 'fuisse', 'fuit', 'gestarum', 'gloria', 'graves', 'honoribus', 'honorum', 'illi', 'in', 'infinitus', 'initium', 'iustum', 'labor', 'locus', 'maximae', 'memoria', 'meorum', 'mihi', 'moles', 'molestiarum', 'nam', 'negotio', 'neque', 'nostri', 'nostrum', 'numero', 'occupatio', 'omnibus', 'optima', 'oti', 'otio', 'perbeati', 'periculo', 'plenissimus', 'possent', 'potuerunt', 'praeclara', 'prope', 'publica', 'quam', 'qui', 'quietis', 'quinte', 'quoque', 're', 'referendi', 'repetenti', 'requiescendi', 'rerum', 'saepe', 'si', 'sine', 'solent', 'spem', 'studia', 'temporum', 'tenere', 'tranquillitatis', 'tum', 'turbulentissimae', 'ut', 'utriusque', 'varii', 'vel', 'vero', 'vetera', 'videbatur', 'videri', 'vitae'] 
        stoplist = StringStoplist('latin').build_stoplist(self.test_1)
        self.assertEqual(stoplist, target_list)
    

    def test_string_stop_list_inc_counts(self):
        """Test production of stoplists from a given string"""
        target_list = [('a', 2), ('ab', 1), ('ac', 1), ('ad', 3), ('aetatis', 1), ('ambitionis', 1), ('animum', 1), ('arbitrarer', 1), ('atque', 3), ('casus', 1), ('cogitanti', 1), ('cogitationum', 1), ('communium', 1), ('concessum', 1), ('consiliorum', 1), ('constitisset', 1), ('cum', 4), ('cursum', 1), ('decursu', 1), ('dignitate', 1), ('eo', 1), ('esse', 1), ('et', 11), ('etiam', 1), ('eum', 1), ('fefellerunt', 1), ('flexu', 1), ('florerent', 1), ('fore', 2), ('forensium', 1), ('frater', 2), ('fuisse', 1), ('fuit', 1), ('gestarum', 1), ('gloria', 1), ('graves', 1), ('honoribus', 1), ('honorum', 1), ('illi', 1), ('in', 8), ('infinitus', 1), ('initium', 1), ('iustum', 1), ('labor', 1), ('locus', 1), ('maximae', 1), ('memoria', 1), ('meorum', 1), ('mihi', 3), ('moles', 1), ('molestiarum', 1), ('nam', 3), ('negotio', 1), ('neque', 5), ('nostri', 1), ('nostrum', 1), ('numero', 1), ('occupatio', 1), ('omnibus', 1), ('optima', 1), ('oti', 2), ('otio', 1), ('perbeati', 1), ('periculo', 1), ('plenissimus', 1), ('possent', 1), ('potuerunt', 1), ('praeclara', 1), ('prope', 1), ('publica', 2), ('quam', 1), ('qui', 3), ('quietis', 1), ('quinte', 1), ('quoque', 1), ('re', 1), ('referendi', 1), ('repetenti', 1), ('requiescendi', 1), ('rerum', 4), ('saepe', 1), ('si', 1), ('sine', 1), ('solent', 1), ('spem', 1), ('studia', 1), ('temporum', 1), ('tenere', 1), ('tranquillitatis', 1), ('tum', 1), ('turbulentissimae', 1), ('ut', 1), ('utriusque', 1), ('varii', 1), ('vel', 7), ('vero', 2), ('vetera', 1), ('videbatur', 1), ('videri', 1), ('vitae', 1)]
        stoplist = StringStoplist('latin').build_stoplist(self.test_1, inc_counts=True)
        self.assertEqual(stoplist, target_list)        

      
    def test_corpus_stop_list_freq(self):
        """Test production of stoplists from a corpus, using basis: frequency"""
        target_list = ['ac', 'ad', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'vel']
        S = CorpusStoplist('latin')
        stoplist = S.build_stoplist(self.test_corpus, size=10, basis='frequency')       
        self.assertEqual(stoplist, target_list)
        
    
    def test_corpus_stop_list_tfidf(self):
        """Test production of stoplists from a corpus, using basis: frequency"""
        target_list = ['ac', 'atque', 'autem', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'vel']
        S = CorpusStoplist('latin')
        stoplist = S.build_stoplist(self.test_corpus, size=10, basis='tfidf')       
        self.assertEqual(stoplist, target_list)   


    def test_corpus_stop_list_freq_exclude(self):
        """Test production of stoplists from a corpus, using basis: frequency"""
        target_list = ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'vel']
        S = CorpusStoplist('latin')
        stoplist = S.build_stoplist(self.test_corpus, size=10, basis='frequency', exclude=['ad'])       
        self.assertEqual(stoplist, target_list)   
        
     
    def test_corpus_stop_list_freq_include(self):
        """Test production of stoplists from a corpus, using basis: frequency"""
        target_list = ['ac', 'ad', 'atque', 'cum', 'est', 'et', 'in', 'mihi', 'neque', 'qui', 'vel']
        S = CorpusStoplist('latin')
        stoplist = S.build_stoplist(self.test_corpus, size=10, basis='frequency', include=['est'])       
        self.assertEqual(stoplist, target_list)            


    def test_corpus_stop_list_freq_sort_words(self):
        """Test production of stoplists from a corpus, using basis: frequency"""
        target_list = ['in', 'et', 'vel', 'ac', 'cum', 'qui', 'atque', 'mihi', 'ad', 'neque']
        S = CorpusStoplist('latin')
        stoplist = S.build_stoplist(self.test_corpus, size=10, basis='frequency', sort_words=False)
        self.assertEqual(stoplist, target_list)        

      
    def test_corpus_stop_list_mean(self):
        """Test production of stoplists from a corpus, using basis: mean"""
        target_list = ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'rerum', 'vel']
        S = CorpusStoplist('latin')
        stoplist = S.build_stoplist(self.test_corpus, size=10,basis='mean')       
        self.assertEqual(stoplist, target_list)
        
 
    def test_corpus_stop_list_variance(self):
        """Test production of stoplists from a corpus, using basis: variance"""
        target_list = ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'rerum', 'vel']
        S = CorpusStoplist('latin')
        stoplist = S.build_stoplist(self.test_corpus, size=10,basis='variance')    
        self.assertEqual(stoplist, target_list)        
    
  
    def test_corpus_stop_list_entropy(self):
        """Test production of stoplists from a corpus, using basis: entropy"""
        target_list = ['ac', 'ad', 'atque', 'cum', 'et', 'in', 'mihi', 'qui', 'rerum', 'vel']
        S = CorpusStoplist('latin')
        stoplist = S.build_stoplist(self.test_corpus, size=10,basis='entropy')
        self.assertEqual(stoplist, target_list)

                
    def test_corpus_stop_list_zou(self):
        """Test production of stoplists from a corpus, using basis: zou"""
        target_list = ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'rerum', 'vel']
        S = CorpusStoplist('latin')
        stoplist = S.build_stoplist(self.test_corpus, size=10,basis='zou')
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
