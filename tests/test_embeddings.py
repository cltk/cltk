"""The full unit test suite, testing every available model for every language."""

import unittest
from typing import List

import numpy

from cltk.core.data_types import Doc, Word
from cltk.core.exceptions import (
    CLTKException,
    UnimplementedAlgorithmError,
    UnknownLanguageError,
)
from cltk.embeddings.embeddings import FastTextEmbeddings, Word2VecEmbeddings
from cltk.embeddings.processes import (
    AramaicEmbeddingsProcess,
    GothicEmbeddingsProcess,
    GreekEmbeddingsProcess,
    LatinEmbeddingsProcess,
    OldEnglishEmbeddingsProcess,
    PaliEmbeddingsProcess,
    SanskritEmbeddingsProcess,
)
from cltk.languages.example_texts import get_example_text


class TestEmbedding(unittest.TestCase):
    def test_embeddings_fasttext(self):
        embeddings_obj = FastTextEmbeddings(
            iso_code="ang", interactive=False, silent=True, overwrite=False
        )
        most_similar_word = embeddings_obj.get_sims(word="mōnaþ")[0][0]
        self.assertEqual(most_similar_word, "hāliȝmōnaþ")

        embeddings_obj = FastTextEmbeddings(
            iso_code="arb", interactive=False, silent=True, overwrite=False
        )
        most_similar_word = embeddings_obj.get_sims(word="بعدها")[0][0]
        self.assertEqual(most_similar_word, "وبعدها")

        embeddings_obj = FastTextEmbeddings(
            iso_code="arc", interactive=False, silent=True, overwrite=False
        )
        most_similar_word = embeddings_obj.get_sims(word="ܒܠܚܘܕ")[0][0]
        self.assertEqual(most_similar_word, "ܠܒܪ")

        embeddings_obj = FastTextEmbeddings(
            iso_code="got", interactive=False, silent=True, overwrite=False
        )
        most_similar_word = embeddings_obj.get_sims(word="𐍅𐌰𐌹𐌷𐍄𐌹𐌽𐍃")[0][0]
        self.assertEqual(most_similar_word, "𐍅𐌰𐌹𐌷𐍄𐍃")

        embeddings_obj = FastTextEmbeddings(
            iso_code="lat", interactive=False, silent=True, overwrite=False
        )
        most_similar_word = embeddings_obj.get_sims(word="amicitia")[0][0]
        self.assertEqual(most_similar_word, "amicitiam")

        embeddings_obj = FastTextEmbeddings(
            iso_code="pli", interactive=False, silent=True, overwrite=False
        )
        most_similar_word = embeddings_obj.get_sims(word="anattamanā")[0][0]
        self.assertEqual(most_similar_word, "kupitā")

        embeddings_obj = FastTextEmbeddings(
            iso_code="san", interactive=False, silent=True, overwrite=False
        )
        most_similar_word = embeddings_obj.get_sims(word="निर्माणम्")[0][0]
        self.assertEqual(most_similar_word, "निर्माणमपि")

        self.assertIsInstance(embeddings_obj, FastTextEmbeddings)

        with self.assertRaises(
            UnimplementedAlgorithmError
        ) as exception_context_manager:
            FastTextEmbeddings(
                iso_code="ave", interactive=False, silent=True, overwrite=False
            )
        exception = exception_context_manager.exception
        self.assertEqual(
            exception.args,
            (
                "No embedding available for language 'ave'. FastTextEmbeddings available for: 'ang', 'arb', 'arc', 'got', 'lat', 'pli', 'san'.",
            ),
        )

        with self.assertRaises(UnknownLanguageError) as exception_context_manager:
            FastTextEmbeddings(
                iso_code="xxx", interactive=False, silent=True, overwrite=False
            ),
        exception = exception_context_manager.exception
        self.assertEqual(exception.args, ("Unknown ISO language code 'xxx'.",))

        with self.assertRaises(CLTKException) as exception_context_manager:
            FastTextEmbeddings(
                iso_code="got",
                training_set="common_crawl",
                interactive=False,
                silent=True,
                overwrite=False,
            ),
        exception = exception_context_manager.exception
        self.assertEqual(
            exception.args,
            (
                "Training set 'common_crawl' not available for language 'got'. Languages available for this training set: 'arb', 'lat', 'san'.",
            ),
        )

    def test_embeddings_word2vec(self):
        # TODO: Add Arabic test; fails with `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xce in position 97: invalid continuation byte`
        # embeddings_obj = Word2VecEmbeddings(iso_code="arb", interactive=False, overwrite=False, silent=True)
        # most_similar_word = embeddings_obj.get_sims(word="ἦλθον")[0][0]
        # self.assertEqual(most_similar_word, "ἀφικόμην")

        embeddings_obj = Word2VecEmbeddings(
            iso_code="chu", interactive=False, silent=True, overwrite=False
        )
        most_similar_word = embeddings_obj.get_sims(word="обꙑчаѥмь")[1][0]
        self.assertEqual(most_similar_word, "послѣди")

        embeddings_obj = Word2VecEmbeddings(
            iso_code="grc", interactive=False, silent=True, overwrite=False
        )
        most_similar_word = embeddings_obj.get_sims(word="ἦλθον")[0][0]
        self.assertEqual(most_similar_word, "ἀφικόμην")

        embeddings_obj = Word2VecEmbeddings(
            iso_code="lat", interactive=False, silent=True, overwrite=False
        )
        most_similar_word = embeddings_obj.get_sims(word="amicitia")[0][0]
        self.assertEqual(most_similar_word, "amicitiam")

        self.assertIsInstance(embeddings_obj, Word2VecEmbeddings)

    def test_embeddings_processes(self):

        language = "ang"  # type: str
        example_text = get_example_text(language)  # type: str
        word_objs = [
            Word(string=word_obj) for word_obj in example_text.split(" ")
        ]  # type: List[Word]
        a_process = OldEnglishEmbeddingsProcess()  # type: OldEnglishEmbeddingsProcess
        a_doc = a_process.run(
            input_doc=Doc(raw=get_example_text(language), words=word_objs)
        )  # type: Doc
        isinstance(a_doc.words[1].embedding, numpy.ndarray)

        language = "arc"  # type: str
        example_text = get_example_text(language)  # type: str
        word_objs = [
            Word(string=word_obj) for word_obj in example_text.split(" ")
        ]  # type: List[Word]
        a_process = AramaicEmbeddingsProcess()  # type: AramaicEmbeddingsProcess
        a_doc = a_process.run(
            input_doc=Doc(raw=get_example_text(language), words=word_objs)
        )  # type: Doc
        isinstance(a_doc.words[1].embedding, numpy.ndarray)

        language = "got"  # type: str
        example_text = get_example_text(language)  # str
        word_objs = [
            Word(string=word_obj) for word_obj in example_text.split(" ")
        ]  # type: List[Word]
        a_process = GothicEmbeddingsProcess()  # type: GothicEmbeddingsProcess
        a_doc = a_process.run(
            input_doc=Doc(raw=get_example_text(language), words=word_objs)
        )  # type: Doc
        isinstance(a_doc.words[1].embedding, numpy.ndarray)

        language = "grc"  # type: str
        example_text = get_example_text(language)  # type: str
        word_objs = [
            Word(string=word_obj) for word_obj in example_text.split(" ")
        ]  # type: List[Word]
        a_process = GreekEmbeddingsProcess()  # type: GreekEmbeddingsProcess
        a_doc = a_process.run(
            input_doc=Doc(raw=get_example_text(language), words=word_objs)
        )  # type: Doc
        isinstance(a_doc.words[1].embedding, numpy.ndarray)

        language = "lat"  # type: str
        example_text = get_example_text(language)  # type: str
        word_objs = [
            Word(string=word_obj) for word_obj in example_text.split(" ")
        ]  # type: List[Word]
        a_process = LatinEmbeddingsProcess()  # type: LatinEmbeddingsProcess
        a_doc = a_process.run(
            input_doc=Doc(raw=get_example_text(language), words=word_objs)
        )  # type: Doc
        isinstance(a_doc.words[1].embedding, numpy.ndarray)

        language = "pli"  # type: str
        example_text = get_example_text(language)  # type: str
        word_objs = [
            Word(string=word_obj) for word_obj in example_text.split(" ")
        ]  # type: List[Word]
        a_process = PaliEmbeddingsProcess()  # type: PaliEmbeddingsProcess
        a_doc = a_process.run(
            input_doc=Doc(raw=get_example_text(language), words=word_objs)
        )
        isinstance(a_doc.words[1].embedding, numpy.ndarray)

        language = "san"  # type: str
        example_text = get_example_text(language)  # type: str
        word_objs = [
            Word(string=word_obj) for word_obj in example_text.split(" ")
        ]  # type: List[Word]
        a_process = SanskritEmbeddingsProcess()  # type: SanskritEmbeddingsProcess
        a_doc = a_process.run(
            input_doc=Doc(raw=get_example_text(language), words=word_objs)
        )  # type: Doc
        isinstance(a_doc.words[1].embedding, numpy.ndarray)


if __name__ == "__main__":
    unittest.main()
