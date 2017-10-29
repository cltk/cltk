"""Test cltk.stop."""

__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.utils.importer import CorpusImporter
from cltk.stop.greek.stops import STOPS_LIST as GREEK_STOPS
from cltk.stop.latin.stops import STOPS_LIST as LATIN_STOPS
from cltk.stop.french.stops import STOPS_LIST as FRENCH_STOPS
from cltk.stop.arabic.stopword_filter import stopwords_filter as arabic_stop_filter
from nltk.tokenize.punkt import PunktLanguageVars
import os
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

if __name__ == '__main__':
    unittest.main()
