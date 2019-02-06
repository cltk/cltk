"""Test for Old Norse"""

import os
import unittest

from cltk.corpus.swadesh import Swadesh
import cltk.phonology.old_norse.transcription as ont
from cltk.stop.old_norse.stops import STOPS_LIST as OLD_NORSE_STOPS
from nltk.tokenize.punkt import PunktLanguageVars
from cltk.phonology import utils as ut
from cltk.tokenize.word import WordTokenizer
from cltk.phonology.syllabify import Syllabifier
from cltk.tag.pos import POSTag
from cltk.corpus.utils.importer import CorpusImporter
from cltk.tokenize.word import tokenize_old_norse_words
from cltk.corpus.old_norse.syllabifier import invalid_onsets
from cltk.inflection.old_norse import pronouns, nouns
import cltk.inflection.utils as decl_utils
from cltk.prosody.old_norse.verse import Fornyrdhislag, Ljoodhhaattr, MetreManager, UnspecifiedStanza


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
        transcribed_sentence = tr.text_to_phonetic_representation(example_sentence)
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
        s.set_invalid_onsets(invalid_onsets)
        syllabified_words = [s.syllabify_ssp(word.lower())
                             for word in words if word not in ",."]

        target = [['gef', 'jun'], ['dró'], ['frá'], ['gyl', 'fa'], ['glöð'], ['djúp', 'rö', 'ðul'], ['óðl', 'a'],
                  ['svá'], ['at'], ['af'], ['ren', 'ni', 'rauk', 'num'], ['rauk'], ['dan', 'mar', 'kar'], ['auk', 'a'],
                  ['bár', 'u'], ['öxn'], ['ok'], ['át', 'ta'], ['en', 'ni', 'tungl'], ['þars'], ['geng', 'u'],
                  ['fy', 'rir'], ['vi', 'ney', 'jar'], ['víðr', 'i'], ['val', 'rauf'], ['fjö', 'gur'], ['hö', 'fuð']]
        self.assertListEqual(syllabified_words, target)

    def test_declension_pronouns(self):
        thessi_declension = [
            [["þessi", "þenna", "þessum", "þessa"], ["þessir", "þessa", "þessum", "þessa"]],
            [["þessi", "þessa", "þessi", "þessar"], ["þessar", "þessar", "þessum", "þessa"]],
            [["þetta", "þetta", "þessu", "þessa"], ["þessi", "þessi", "þessum", "þessa"]]
        ]
        self.assertListEqual(pronouns.pro_demonstrative_pronouns_this.declension, thessi_declension)

    def test_declension_nouns(self):
        noun_sumar = decl_utils.DeclinableOneGender("sumar", decl_utils.Gender.neuter)
        noun_sumar.set_declension(nouns.sumar)
        self.assertEqual(noun_sumar.get_declined(decl_utils.Case.nominative, decl_utils.Number.plural), "sumur")

    def test_prosody_fornyrdhislag(self):
        poem = "Hljóðs bið ek allar\nhelgar kindir,\nmeiri ok minni\nmögu Heimdallar;\nviltu at ek, Valföðr,\n" \
               "vel fyr telja\nforn spjöll fira,\nþau er fremst of man."
        fo = Fornyrdhislag()
        fo.from_short_lines_text(poem)
        fo.to_phonetics()
        res_alliterations, res_n_alliterations_lines = fo.find_alliteration()
        self.assertEqual(res_alliterations, [[('hljóðs', 'helgar')], [('meiri', 'mögu'), ('minni', 'mögu')], [],
                                             [('forn', 'fremst'), ('fira', 'fremst')]])

    def test_prosody_ljoodhhaattr(self):
        poem = "Deyr fé,\ndeyja frændr,\ndeyr sjalfr it sama,\nek veit einn,\nat aldrei deyr:\n" \
               "dómr um dauðan hvern."
        lj = Ljoodhhaattr()
        lj.from_short_lines_text(poem)
        lj.to_phonetics()
        verse_alliterations, n_alliterations_lines = lj.find_alliteration()
        self.assertEqual(verse_alliterations,
                         [[('deyr', 'deyja'), ('fé', 'frændr')], [('sjalfr', 'sjalfr')], [('einn', 'aldrei')],
                          [('dómr', 'um')]])

    def test_poem(self):
        fake_poetic_text = ["Hljóðs bið ek allar\nhelgar kindir,\nmeiri ok minni\nmögu Heimdallar;\n"
                            "viltu at ek, Valföðr,\nvel fyr telja\nforn spjöll fira,\nþau er fremst of man.",
                            "Deyr fé,\ndeyja frændr,\ndeyr sjalfr it sama,\nek veit einn,\nat aldrei deyr:\n"
                            "dómr um dauðan hvern.",
                            "Ein sat hon úti,\nþá er inn aldni kom\nyggjungr ása\nok í augu leit.\n"
                            "Hvers fregnið mik?\nHví freistið mín?\nAllt veit ek, Óðinn,\nhvar þú auga falt,\n"
                            "í inum mæra\nMímisbrunni.\nDrekkr mjöð Mímir\nmorgun hverjan\naf veði Valföðrs.\n"
                            "Vituð ér enn - eða hvat?"]
        fake_poem = MetreManager.load_poem_from_paragraphs(fake_poetic_text)
        self.assertIsInstance(fake_poem[0], Fornyrdhislag)
        self.assertIsInstance(fake_poem[1], Ljoodhhaattr)
        self.assertIsInstance(fake_poem[2], UnspecifiedStanza)

    def test_syllable_length_1(self):
        syllabifier = Syllabifier(language="old_norse_ipa")
        word = [ont.a, ont.s, ont.g, ont.a, ont.r, ont.dh, ont.r]  # asgarðr (normally it is ásgarðr)
        syllabified_word = syllabifier.syllabify_phonemes(word)
        lengths = []
        for syllable in syllabified_word:
            lengths.append(ont.measure_old_norse_syllable(syllable))
        self.assertListEqual(lengths, [ut.Length.short, ut.Length.long])

    def test_syllable_length_2(self):
        ont.o.length = ont.Length.long
        word = [ont.n, ont.o, ont.t.lengthen()]  # nótt
        syllabified_word = [word]
        lengths = []
        for syllable in syllabified_word:
            lengths.append(ont.measure_old_norse_syllable(syllable))
        self.assertListEqual(lengths, [ut.Length.overlong])

    def test_syllable_length_3(self):
        word = [ont.t, ont.t]  # tt
        lengths = []
        for syllable in [word]:
            lengths.append(ont.measure_old_norse_syllable(syllable))
        self.assertListEqual(lengths, [None])


if __name__ == '__main__':
    unittest.main()
