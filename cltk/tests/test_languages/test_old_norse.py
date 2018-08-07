"""Test for Old Norse"""

import os
import unittest

from cltk.corpus.swadesh import Swadesh
from cltk.phonology.old_norse import transcription as ont
from cltk.stop.old_norse.stops import STOPS_LIST as OLD_NORSE_STOPS
from nltk.tokenize.punkt import PunktLanguageVars
from cltk.phonology import utils as ut
from cltk.tokenize.word import WordTokenizer
from cltk.phonology.syllabify import Syllabifier
from cltk.tag.pos import POSTag
from cltk.corpus.utils.importer import CorpusImporter
from cltk.tokenize.word import tokenize_old_norse_words
from cltk.corpus.old_norse.syllabifier import invalid_onsets
from cltk.declension.old_norse import utils as decl_utils


__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


class TestOldNorse(unittest.TestCase):
    """Class for unittest"""
    def setUp(self):
        corpus_importer = CorpusImporter("old_norse")
        corpus_importer.import_corpus("old_norse_models_cltk")
        file_rel = os.path.join('~/cltk_data/old_norse/model/old_norse_models_cltk/README.md')
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

    def test_swadesh_old_norse(self):
        """Swadesh list"""
        swadesh = Swadesh('old_norse')
        first_word = 'ek'
        match = swadesh.words()[0]
        self.assertEqual(first_word, match)

    def test_old_norse_transcriber(self):
        """phonetic transcription"""
        example_sentence = "Almáttigr guð skapaði í upphafi himin ok jörð ok alla þá hluti, er þeim fylgja, og " \
                           "síðast menn tvá, er ættir eru frá komnar, Adam ok Evu, ok fjölgaðist þeira kynslóð ok " \
                           "dreifðist um heim allan."

        tr = ut.Transcriber(ont.DIPHTHONGS_IPA, ont.DIPHTHONGS_IPA_class, ont.IPA_class, ont.old_norse_rules)
        transcribed_sentence = tr.main(example_sentence)
        print(transcribed_sentence)
        target = "[almaːtːiɣr guð skapaði iː upːhavi himin ɔk jœrð ɔk alːa θaː hluti ɛr θɛim fylɣja ɔɣ siːðast mɛnː " \
                 "tvaː ɛr ɛːtːir ɛru fraː kɔmnar adam ɔk ɛvu ɔk fjœlɣaðist θɛira kynsloːð ɔk drɛivðist um hɛim alːan]"
        self.assertEqual(target, transcribed_sentence)

    def test_old_norse_stopwords(self):
        """
        Stop words
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

    def test_pos_tnt_tagger_old_norse(self):
        """Test tagging Old Norse POS with TnT tagger."""
        tagger = POSTag('old_norse')
        tagged = tagger.tag_tnt('Hlióðs bið ek allar.')
        print(tagged)
        self.assertTrue(tagged)

    def test_old_norse_word_tokenizer(self):
        """Word tokenization"""
        text = "Gylfi konungr var maðr vitr ok fjölkunnigr. " \
               "Hann undraðist þat mjök, er ásafólk var svá kunnigt, at allir hlutir gengu at vilja þeira."
        target = ['Gylfi', 'konungr', 'var', 'maðr', 'vitr', 'ok', 'fjölkunnigr', '.', 'Hann', 'undraðist', 'þat',
                  'mjök', ',', 'er', 'ásafólk', 'var', 'svá', 'kunnigt', ',', 'at', 'allir', 'hlutir', 'gengu', 'at',
                  'vilja', 'þeira', '.']
        word_tokenizer = WordTokenizer('old_norse')
        result = word_tokenizer.tokenize(text)
        # print(result)
        self.assertTrue(result == target)

    def test_syllabification_old_norse(self):
        """Syllabification"""
        s = Syllabifier(language="old_norse", break_geminants=True)
        text = "Gefjun dró frá Gylfa glöð djúpröðul óðla, svá at af rennirauknum rauk, Danmarkar auka. Báru öxn ok " \
               "átta ennitungl, þars gengu fyrir vineyjar víðri valrauf, fjögur höfuð."
        words = tokenize_old_norse_words(text)
        syllabified_words = [s.legal_onsets(s.syllabify_SSP(word.lower()), invalid_onsets)
                             for word in words if word not in ",."]

        target = [['gef', 'jun'], ['dró'], ['frá'], ['gyl', 'fa'], ['glöð'], ['djúp', 'rö', 'ðul'], ['óðl', 'a'],
                  ['svá'], ['at'], ['af'], ['ren', 'ni', 'rauk', 'num'], ['rauk'], ['dan', 'mar', 'kar'], ['auk', 'a'],
                  ['bár', 'u'], ['öxn'], ['ok'], ['át', 'ta'], ['en', 'ni', 'tungl'], ['þars'], ['geng', 'u'],
                  ['fy', 'rir'], ['vi', 'ney', 'jar'], ['víðr', 'i'], ['val', 'rauf'], ['fjö', 'gur'], ['hö', 'fuð']]
        self.assertListEqual(syllabified_words, target)

    def test_declensions(self):
        thessi_declension = [
            [["þessi", "þenna", "þessum", "þessa"], ["þessir", "þessa", "þessum", "þessa"]],
            [["þessi", "þessa", "þessi", "þessar"], ["þessar", "þessar", "þessum", "þessa"]],
            [["þetta", "þetta", "þessu", "þessa"], ["þessi", "þessi", "þessum", "þessa"]]
        ]
        self.assertListEqual(decl_utils.pro_demonstrative_pronouns_this.declension, thessi_declension)


if __name__ == '__main__':
    unittest.main()
