"""Test Middle High German"""

import os
import unittest
import unicodedata
import os

from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.middle_high_german.alphabet import normalize_middle_high_german
from cltk.lemmatize.middle_high_german.backoff import BackoffMHGLemmatizer
from cltk.stem.middle_high_german.stem import stemmer_middle_high_german as middle_high_german_stemmer
from cltk.stop.middle_high_german.stops import STOPS_LIST as MIDDLE_HIGH_GERMAN_STOPS
from cltk.phonology.middle_high_german import transcription as mhg
from cltk.phonology.syllabify import Syllabifier
from cltk.tag.pos import POSTag
from cltk.tokenize.word import WordTokenizer

__author__ = ['Eleftheria Chatziargyriou <ele.hatzy@gmail.com>', 'Clément Besnier <clemsciences@aol.com>']
__license__ = 'MIT License. See LICENSE.'


class TestMiddleHighGerman(unittest.TestCase):
    """ Middle High German unit tests"""

    def setUp(self):
        corpus_importer = CorpusImporter("middle_high_german")
        corpus_importer.import_corpus("middle_high_german_models_cltk")
        file_rel = os.path.join(get_cltk_data_dir() +
                                '/middle_high_german/model/middle_high_german_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_middle_high_german_tokenize(self):
        """
        Test tokenizing Middle High German
        """
        word_tokenizer = WordTokenizer('middle_high_german')
        text = "Mīn ougen   wurden liebes alsō vol, \n\n\ndō ich die minneclīchen ērst gesach,\ndaȥ eȥ mir hiute und   iemer mē tuot wol."

        tokenized = word_tokenizer.tokenize(text)
        target = ['Mīn', 'ougen', 'wurden', 'liebes', 'alsō', 'vol', ',', 'dō', 'ich', 'die', 'minneclīchen', 'ērst',
                  'gesach', ',', 'daȥ', 'eȥ', 'mir', 'hiute', 'und', 'iemer', 'mē', 'tuot', 'wol', '.']

        self.assertEqual(tokenized, target)

    def test_middle_high_german_stopwords(self):
        """
        Test filtering  Middle High German stopwords.
        """

        sentence = "Swer was ze Bêârosche komn, doch hete Gâwân dâ genomn den prîs ze bêder sît al ein wan daz dervor ein ritter schein, bî rôtem wâpen unrekant, des prîs man in die hœhe bant."
        lowered = sentence.lower()
        tokenizer = WordTokenizer('middle_high_german')
        tokens = tokenizer.tokenize(lowered)
        no_stops = [w for w in tokens if w not in MIDDLE_HIGH_GERMAN_STOPS]
        target_list = ['swer', 'bêârosche', 'komn', ',', 'gâwân', 'genomn', 'prîs', 'bêder', 'sît', 'dervor', 'ritter',
                       'schein', ',', 'rôtem', 'wâpen', 'unrekant', ',', 'prîs', 'hœhe', 'bant', '.']

        self.assertEqual(no_stops, target_list)

    def test_middle_high_german_transcriber(self):
        """
        Test Middle High German IPA transcriber
        """
        inputs = "Slâfest du friedel ziere?"
        transcriber = mhg.Transcriber().transcribe
        transcription = [unicodedata.normalize('NFC', x) for x in transcriber(inputs)]
        target = [unicodedata.normalize('NFC', x) for x in '[Slɑːfest d̥ʊ frɪ͡əd̥el t͡sɪ͡əre?]']

        self.assertEqual(target, transcription)

    def test_middle_high_german_ascii_encoding(self):
        """
        Test Middle High German ASCII encoder
        """
        s1 = mhg.Word("vogellîn").ASCII_encoding()
        s2 = mhg.Word("vogellīn").ASCII_encoding()
        target = ['vogellin', 'vogellin']

        self.assertEqual([s1, s2], target)

    def test_middle_high_german_normalizer(self):
        """
        Test Middle High German normalizer
        """
        normalized = normalize_middle_high_german("Dô erbiten si der nahte und fuoren über Rîn")
        target = 'dô erbiten si der nahte und fuoren über rîn'

        self.assertEqual(normalized, target)

    def test_middle_high_german_normalizer_spelling(self):
        """
        Test Middle High German spelling normalizer
        """
        normalized = normalize_middle_high_german("Mit ūf erbürten schilden in was ze strīte nōt", alpha_conv=True)
        target = 'mit ûf erbürten schilden in was ze strîte nôt'

        self.assertEqual(normalized, target)

    def test_middle_high_german_normalizer(self):
        """
        Test Middle High German punctuation normalizer
        """
        normalized = normalize_middle_high_german("Si sprach: ‘herre Sigemunt, ir sult iȥ lāȥen stān", punct=True)
        target = 'si sprach herre sigemunt ir sult iȥ lâȥen stân'

        self.assertEqual(normalized, target)

    def test_middle_high_german_stemmer(self):
        """
        Test stemming Middle High German words
        """
        stemmed = middle_high_german_stemmer("Man lūte dā zem münster nāch gewoneheit")
        target = ['man', 'lut', 'dâ', 'zem', 'munst', 'nâch', 'gewoneheit']

        self.assertEqual(stemmed, target)

    def test_middle_high_german_stemmer_strip_umlaut(self):
        """
        Test Middle High German stemmer's strip umlaut function
        """
        stemmed = middle_high_german_stemmer("Man lūte dā zem münster nāch gewoneheit", rem_umlauts=False)
        target = ['man', 'lût', 'dâ', 'zem', 'münst', 'nâch', 'gewoneheit']

        self.assertEqual(stemmed, target)

    def test_middle_high_german_stemmer_dictionary(self):
        """
        Test Middle High German stemmer's user-defined dictionary function
        """
        exception_dic = {"biuget": "biegen"}
        stemmed = middle_high_german_stemmer("swaȥ kriuchet unde fliuget und bein zer erden biuget", rem_umlauts=False,
                                             exceptions=exception_dic)
        target = ['swaȥ', 'kriuchet', 'unde', 'fliuget', 'und', 'bein', 'zer', 'erden', 'biegen']

        self.assertEqual(stemmed, target)

    def test_middle_high_german_syllabification(self):
        """
        Test Middle High German syllabification
        """
        mhg_syllabifier = Syllabifier(language='middle_high_german')
        syllabified = mhg_syllabifier.syllabify('lobebæren')
        target = ['lo', 'be', 'bæ', 'ren']

        self.assertEqual(syllabified, target)

    def test_lemmatizer(self):
        mhg_lemmatizer = BackoffMHGLemmatizer()
        lemmatized_sentence = mhg_lemmatizer.lemmatize("uns ist in alten mæren".split(" "))
        res = [lemmata[1] for lemmata in lemmatized_sentence]
        target = ["wir", "sîn", "in", "alt", "mære"]
        for lemma_target, lemma_estimated in zip(target, res):
            self.assertIn(lemma_target, lemma_estimated)

    def test_middle_high_german_tnt_pos_tagger(self):
        target = [('uns', 'PPER'), ('ist', 'VAFIN'), ('in', 'APPR'), ('alten', 'ADJA'), ('mæren', 'ADJA'),
                  ('wunders', 'NA'), ('vil', 'AVD'), ('geseit', 'VVPP')]
        mhg_pos_tagger = POSTag("middle_high_german")
        res = mhg_pos_tagger.tag_tnt("uns ist in alten mæren wunders vil geseit")
        self.assertEqual(target, res)

    def test_middle_high_german_unigram_pos_tagger(self):
        target = [('uns', 'PPER'), ('ist', 'VAFIN'), ('in', 'APPR'), ('alten', 'ADJA'), ('mæren', 'ADJA'),
                  ('wunders', 'NA'), ('vil', 'ADJA'), ('geseit', 'VVPP')]
        mhg_pos_tagger = POSTag("middle_high_german")
        res = mhg_pos_tagger.tag_unigram("uns ist in alten mæren wunders vil geseit")
        self.assertEqual(target, res)

    def test_middle_high_german_bigram_pos_tagger(self):
        target = [('uns', 'PPER'), ('ist', 'VAFIN'), ('in', 'APPR'), ('alten', 'ADJA'), ('mæren', 'NA'),
                  ('wunders', 'NA'), ('vil', None), ('geseit', None)]
        mhg_pos_tagger = POSTag("middle_high_german")
        res = mhg_pos_tagger.tag_bigram("uns ist in alten mæren wunders vil geseit")
        self.assertEqual(target, res)

    def test_middle_high_german_trigram_pos_tagger(self):
        target = [('uns', 'PPER'), ('ist', 'VAFIN'), ('in', 'APPR'), ('alten', 'ADJA'), ('mæren', 'NA'),
                  ('wunders', 'NA'), ('vil', None), ('geseit', None)]
        mhg_pos_tagger = POSTag("middle_high_german")
        res = mhg_pos_tagger.tag_trigram("uns ist in alten mæren wunders vil geseit")
        self.assertEqual(target, res)


if __name__ == '__main__':
    unittest.main()
