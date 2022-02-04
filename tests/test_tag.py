"""Test cltk.tag."""

import os
import shutil
import unittest

from cltk.data.fetch import FetchCorpus
from cltk.tag import ner
from cltk.tag.ner import NamedEntityReplacer
from cltk.tag.pos import POSTag
from cltk.text.lat import replace_jv
from cltk.utils import CLTK_DATA_DIR

__license__ = "MIT License. See LICENSE."


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def setUp(self):
        """Clone Greek models in order to test pull function and other model
        tests later.
        """
        corpus_importer = FetchCorpus("grc")
        corpus_importer.import_corpus("grc_models_cltk")
        file_rel = os.path.join(CLTK_DATA_DIR, "grc/model/grc_models_cltk/README.md")
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

        corpus_importer = FetchCorpus("lat")
        corpus_importer.import_corpus("lat_models_cltk")
        file_rel = os.path.join(CLTK_DATA_DIR, "lat/model/lat_models_cltk/README.md")
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

        corpus_importer = FetchCorpus("fro")
        corpus_importer.import_corpus("fro_models_cltk")
        file_rel = os.path.join(CLTK_DATA_DIR, "fro/text/fro_models_cltk/README.md")
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

        corpus_importer = FetchCorpus("non")
        corpus_importer.import_corpus("non_models_cltk")
        file_rel = os.path.join(CLTK_DATA_DIR, "non/model/non_models_cltk/README.md")
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

        corpus_importer = FetchCorpus("gml")
        corpus_importer.import_corpus("gml_models_cltk")
        file_rel = os.path.join(CLTK_DATA_DIR, "gml/model/gml_models_cltk/README.md")
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

        corpus_importer = FetchCorpus("ang")
        corpus_importer.import_corpus("ang_models_cltk")
        file_rel = os.path.join(CLTK_DATA_DIR, "ang/model/ang_models_cltk/README.md")
        file = os.path.expanduser(file_rel)
        file_exists = os.path.isfile(file)
        self.assertTrue(file_exists)

        corpus_importer = FetchCorpus("gmh")
        corpus_importer.import_corpus("gmh_models_cltk")
        file_rel = os.path.join(CLTK_DATA_DIR, "gmh/model/gmh_models_cltk/README.md")
        file = os.path.expanduser(file_rel)
        file_exists = os.path.exists(file)
        self.assertTrue(file_exists)

    def test_pos_unigram_greek(self):
        """Test tagging Greek POS with unigram tagger."""
        tagger = POSTag("grc")
        tagged = tagger.tag_unigram(
            "θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος"
        )  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_bigram_greek(self):
        """Test tagging Greek POS with bigram tagger."""
        tagger = POSTag("grc")
        tagged = tagger.tag_bigram(
            "θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος"
        )  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_trigram_greek(self):
        """Test tagging Greek POS with trigram tagger."""
        tagger = POSTag("grc")
        tagged = tagger.tag_trigram(
            "θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος"
        )  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_ngram123_tagger_greek(self):
        """Test tagging Greek POS with a 1-, 2-, and 3-gram backoff tagger."""
        tagger = POSTag("grc")
        tagged = tagger.tag_ngram_123_backoff(
            "θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος"
        )  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_tnt_tagger_greek(self):
        """Test tagging Greek POS with TnT tagger."""
        tagger = POSTag("grc")
        tagged = tagger.tag_tnt(
            "θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος"
        )  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_unigram_latin(self):
        """Test tagging Latin POS with unigram tagger."""
        tagger = POSTag("lat")
        tagged = tagger.tag_unigram("Gallia est omnis divisa in partes tres")
        self.assertTrue(tagged)

    def test_pos_bigram_latin(self):
        """Test tagging Latin POS with bigram tagger."""
        tagger = POSTag("lat")
        tagged = tagger.tag_bigram("Gallia est omnis divisa in partes tres")
        self.assertTrue(tagged)

    def test_pos_trigram_latin(self):
        """Test tagging Latin POS with trigram tagger."""
        tagger = POSTag("lat")
        tagged = tagger.tag_trigram("Gallia est omnis divisa in partes tres")
        self.assertTrue(tagged)

    def test_pos_ngram123_tagger_latin(self):
        """Test tagging Latin POS with a 1-, 2-, and 3-gram backoff tagger."""
        tagger = POSTag("lat")
        tagged = tagger.tag_ngram_123_backoff(
            "Gallia est omnis divisa in partes tres"
        )  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    def test_pos_tnt_tagger_latin(self):
        """Test tagging Latin POS with TnT tagger."""
        tagger = POSTag("lat")
        tagged = tagger.tag_tnt("Gallia est omnis divisa in partes tres")
        self.assertTrue(tagged)

    # TODO: Re-enable this. Something breaking on build server but works for KJ locally
    # see also ``test_pos_crf_tagger_old_english`` below
    # https://travis-ci.org/github/cltk/cltk/jobs/721808293#L639
    # def test_pos_crf_tagger_latin(self):
    #     """Test tagging Latin POS with CRF tagger."""
    #     tagger = POSTag("lat")
    #     tagged = tagger.tag_crf("Gallia est omnis divisa in partes tres")
    #     self.assertTrue(tagged)

    def test_check_latest_latin(self):
        """Test _check_latest_data()"""
        ner._check_latest_data("lat")
        names_path = os.path.normpath(
            CLTK_DATA_DIR, "lat/model/latin_models_cltk/ner/proper_names.txt"
        )
        self.assertTrue(os.path.isfile(names_path))

    def test_check_latest_latin(self):
        """Test _check_latest_data()"""
        path = os.path.join(CLTK_DATA_DIR, "lat/model/lat_models_cltk")
        names_dir = os.path.expanduser(path)
        shutil.rmtree(names_dir, ignore_errors=True)
        ner._check_latest_data("lat")
        names_path = os.path.join(names_dir, "ner", "proper_names.txt")
        self.assertTrue(os.path.isfile(names_path))

    def test_tag_ner_str_list_latin(self):
        """Test make_ner(), str, list."""
        text_str = """ut Venus, ut Sirius, ut Spica, ut aliae quae primae dicuntur esse mangitudinis."""
        text_str_iu = replace_jv(text_str)
        tokens = ner.tag_ner("lat", input_text=text_str_iu, output_type=list)
        target = [
            ("ut",),
            ("Uenus", "Entity"),
            (",",),
            ("ut",),
            ("Sirius", "Entity"),
            (",",),
            ("ut",),
            ("Spica", "Entity"),
            (",",),
            ("ut",),
            ("aliae",),
            ("quae",),
            ("primae",),
            ("dicuntur",),
            ("esse",),
            ("mangitudinis",),
            (".",),
        ]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_list_latin(self):
        """Test make_ner(), list, list."""
        text_list = ["ut", "Venus", "Sirius"]
        text_list_iu = [replace_jv(x) for x in text_list]
        tokens = ner.tag_ner("lat", input_text=text_list_iu, output_type=list)
        target = [("ut",), ("Uenus", "Entity"), ("Sirius", "Entity")]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_str_latin(self):
        """Test make_ner(), list, str."""
        text_list = ["ut", "Venus", "Sirius"]
        text_list_iu = [replace_jv(x) for x in text_list]
        text = ner.tag_ner("lat", input_text=text_list_iu, output_type=str)
        target = " ut Uenus/Entity Sirius/Entity"
        self.assertEqual(text, target)

    def test_tag_ner_str_str_latin(self):
        """Test make_ner(), str, str."""
        text_str = """ut Venus, ut Sirius, ut Spica, ut aliae quae primae dicuntur esse mangitudinis."""
        text_str_iu = replace_jv(text_str)
        text = ner.tag_ner("lat", input_text=text_str_iu, output_type=str)
        target = " ut Uenus/Entity, ut Sirius/Entity, ut Spica/Entity, ut aliae quae primae dicuntur esse mangitudinis."
        self.assertEqual(text, target)

    def test_tag_ner_str_list_greek(self):
        """Test make_ner(), str, list."""
        text_str = "τὰ Σίλαριν Σιννᾶν Κάππαρος Πρωτογενείας Διονυσιάδες τὴν"
        tokens = ner.tag_ner("grc", input_text=text_str, output_type=list)
        target = [
            ("τὰ",),
            ("Σίλαριν", "Entity"),
            ("Σιννᾶν", "Entity"),
            ("Κάππαρος", "Entity"),
            ("Πρωτογενείας", "Entity"),
            ("Διονυσιάδες", "Entity"),
            ("τὴν",),
        ]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_list_greek(self):
        """Test make_ner(), list, list."""
        text_list = ["τὰ", "Σίλαριν", "Σιννᾶν"]
        tokens = ner.tag_ner("grc", input_text=text_list, output_type=list)
        target = [("τὰ",), ("Σίλαριν", "Entity"), ("Σιννᾶν", "Entity")]
        self.assertEqual(tokens, target)

    def test_tag_ner_list_str_greek(self):
        """Test make_ner(), list, str."""
        text_list = ["τὰ", "Σίλαριν", "Σιννᾶν"]
        text = ner.tag_ner("grc", input_text=text_list, output_type=str)
        target = " τὰ Σίλαριν/Entity Σιννᾶν/Entity"
        self.assertEqual(text, target)

    def test_tag_ner_str_str_greek(self):
        """Test make_ner(), str, str."""
        text_str = "τὰ Σίλαριν Σιννᾶν Κάππαρος Πρωτογενείας Διονυσιάδες τὴν"
        text = ner.tag_ner("grc", input_text=text_str, output_type=str)
        target = " τὰ Σίλαριν/Entity Σιννᾶν/Entity Κάππαρος/Entity Πρωτογενείας/Entity Διονυσιάδες/Entity τὴν"
        self.assertEqual(text, target)

    def test_tag_ner_str_list_french(self):
        """Test make_ner(), str, list."""
        text_str = "Berte fu mere Charlemaine, qui pukis tint France et tot le Maine."
        ner_replacer = NamedEntityReplacer()
        tokens = ner_replacer.tag_ner_fr(input_text=text_str, output_type=list)
        target = [
            [("Berte", "entity", "CHI")],
            ("fu",),
            ("mere",),
            [("Charlemaine", "entity", "CHI")],
            (",",),
            ("qui",),
            ("pukis",),
            ("tint",),
            [("France", "entity", "LOC")],
            ("et",),
            ("tot",),
            ("le",),
            [("Maine", "entity", "LOC")],
            (".",),
        ]
        self.assertEqual(tokens, target)

    def test_pos_tnt_tagger_old_norse(self):
        """Test tagging Old Norse POS with TnT tagger."""
        tagger = POSTag("non")
        tagged = tagger.tag_tnt("Hlióðs bið ek allar.")
        self.assertTrue(tagged)

    def test_pos_ngram12_tagger_middle_low_german(self):
        """Test MOG POS 12-backoff tagger"""
        tagger = POSTag("gml")
        tagged = tagger.tag_ngram_12_backoff(
            "Jck Johannes preister verwarer vnde voirs tender des Juncfrouwen kloisters to Mariendale"
        )
        self.assertTrue(tagged)

    def test_pos_unigram_old_english(self):
        """Test tagging Old English POS with unigram tagger."""
        tagger = POSTag("ang")
        tagged = tagger.tag_unigram(
            "Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon."
        )
        self.assertTrue(tagged)

    def test_pos_bigram_old_english(self):
        """Test tagging Old English POS with bigram tagger."""
        tagger = POSTag("ang")
        tagged = tagger.tag_bigram(
            "Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon."
        )
        self.assertTrue(tagged)

    def test_pos_trigram_old_english(self):
        """Test tagging old_english POS with trigram tagger."""
        tagger = POSTag("ang")
        tagged = tagger.tag_trigram(
            "Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon."
        )
        self.assertTrue(tagged)

    def test_pos_ngram123_tagger_old_english(self):
        """Test tagging Old English POS with a 1-, 2-, and 3-gram backoff tagger."""
        tagger = POSTag("ang")
        tagged = tagger.tag_ngram_123_backoff(
            "Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon."
        )  # pylint: disable=line-too-long
        self.assertTrue(tagged)

    # TODO: Re-enable; see ``test_pos_crf_tagger_latin`` above
    # https://travis-ci.org/github/cltk/cltk/jobs/721808293#L732
    # def test_pos_crf_tagger_old_english(self):
    #     """Test tagging Old English POS with CRF tagger."""
    #     tagger = POSTag("ang")
    #     tagged = tagger.tag_crf(
    #         "Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon."
    #     )
    #     self.assertTrue(tagged)

    def test_pos_perceptron_tagger_old_english(self):
        """Test tagging Old English POS with Perceptron tagger."""
        tagger = POSTag("ang")
        tagged = tagger.tag_perceptron(
            "Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon."
        )
        self.assertTrue(tagged)

    def test_pos_unigram_middle_high_german(self):
        """Test tagging Middle High German with unigram tagger"""
        target = [
            ("uns", "PPER"),
            ("ist", "VAFIN"),
            ("in", "APPR"),
            ("alten", "ADJA"),
            ("mæren", "ADJA"),
            ("wunders", "NA"),
            ("vil", "ADJA"),
            ("geseit", "VVPP"),
        ]
        tagger = POSTag("gmh")
        tagged = tagger.tag_unigram("uns ist in alten mæren wunders vil geseit")
        self.assertEqual(target, tagged)

    def test_pos_bigram_middle_high_german(self):
        """Test tagging Middle High German with bigram tagger"""
        target = [
            ("uns", "PPER"),
            ("ist", "VAFIN"),
            ("in", "APPR"),
            ("alten", "ADJA"),
            ("mæren", "NA"),
            ("wunders", "NA"),
            ("vil", None),
            ("geseit", None),
        ]
        tagger = POSTag("gmh")
        tagged = tagger.tag_bigram("uns ist in alten mæren wunders vil geseit")
        self.assertEqual(target, tagged)

    def test_pos_trigram_middle_high_german(self):
        """Test tagging Middle High German with trigram tagger"""
        target = [
            ("uns", "PPER"),
            ("ist", "VAFIN"),
            ("in", "APPR"),
            ("alten", "ADJA"),
            ("mæren", "NA"),
            ("wunders", "NA"),
            ("vil", None),
            ("geseit", None),
        ]
        tagger = POSTag("gmh")
        tagged = tagger.tag_trigram("uns ist in alten mæren wunders vil geseit")
        self.assertEqual(target, tagged)

    def test_pos_tnt_middle_high_german(self):
        """Test tagging Middle High German with TnT tagger"""
        target = [
            ("uns", "PPER"),
            ("ist", "VAFIN"),
            ("in", "APPR"),
            ("alten", "ADJA"),
            ("mæren", "ADJA"),
            ("wunders", "NA"),
            ("vil", "AVD"),
            ("geseit", "VVPP"),
        ]
        tagger = POSTag("gmh")
        tagged = tagger.tag_tnt("uns ist in alten mæren wunders vil geseit")
        self.assertEqual(target, tagged)


if __name__ == "__main__":
    unittest.main()
