"""A quick sanity check for the main ``NLP()`` object. Intended to
run under 5 mins on the build server (assuming models already downloaded).
"""

import time
import unittest

import numpy as np
from stanza.models.common.doc import Document

from cltk import NLP
from cltk.core.data_types import Doc, Language, Word
from cltk.languages.example_texts import get_example_text
from cltk.languages.pipelines import LatinPipeline
from cltk.morphology.morphosyntax import MorphosyntacticFeatureBundle
from cltk.morphology.universal_dependencies_features import POS


class TestNLPLatin(unittest.TestCase):
    """Test all Latin models in default pipeline."""

    def test_nlp_latin(self):
        time_0 = time.time()
        print("Starting complete `NLP()` test for 'lat' ...")

        lang: str = "lat"

        self.assertIsInstance(LatinPipeline.description, str)
        self.assertIsInstance(LatinPipeline.language, Language)
        self.assertIsInstance(LatinPipeline.language.family_id, str)
        self.assertIsInstance(LatinPipeline.language.glottolog_id, str)
        self.assertIsInstance(LatinPipeline.language.iso_639_3_code, str)
        self.assertIsInstance(LatinPipeline.language.latitude, float)
        self.assertIsInstance(LatinPipeline.language.level, str)
        self.assertIsInstance(LatinPipeline.language.longitude, float)
        self.assertIsInstance(LatinPipeline.language.parent_id, str)
        self.assertIsInstance(LatinPipeline.language.type, str)

        text = get_example_text(iso_code=lang)
        self.assertIsInstance(text, str)

        cltk_nlp: NLP = NLP(language=lang)
        self.assertIsInstance(cltk_nlp, NLP)

        cltk_doc = cltk_nlp.analyze(text=text)
        self.assertIsInstance(cltk_doc, Doc)
        self.assertIsInstance(cltk_doc.raw, str)
        self.assertEqual(cltk_doc.language, lang)
        self.assertIsInstance(cltk_doc.stanza_doc, Document)

        self.assertTrue(len(cltk_doc.words) > 0)
        all_words_pres = all([isinstance(word, Word) for word in cltk_doc.words])
        self.assertTrue(all_words_pres)
        word = cltk_doc.words[0]
        self.assertIsInstance(word.category, MorphosyntacticFeatureBundle)
        self.assertIsInstance(word.dependency_relation, str)
        self.assertIsInstance(word.embedding, np.ndarray)
        self.assertIsInstance(word.governor, int)
        self.assertIsInstance(word.index_token, int)
        self.assertIsInstance(word.lemma, str)
        # self.assertIsInstance(word.named_entity, str)
        self.assertIsInstance(word.pos, POS)
        self.assertIsInstance(word.stanza_features, str)
        self.assertIsInstance(word.stop, bool)
        self.assertIsInstance(word.string, str)
        self.assertIsInstance(word.upos, str)
        self.assertIsInstance(word.xpos, str)

        print(f"Finished complete test of `NLP()` in {time.time() - time_0} secs.")


if __name__ == "__main__":
    unittest.main()
