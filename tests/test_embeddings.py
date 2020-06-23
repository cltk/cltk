"""The full unit test suite, testing every available model for every language."""

import unittest

from cltkv1.embeddings.embeddings import FastTextEmbeddings, Word2VecEmbeddings


class TestStringMethods(unittest.TestCase):

    def test_embeddings_fasttext(self):
        embeddings_obj = FastTextEmbeddings(iso_code="ang", interactive=False, overwrite=False, silent=True)
        most_similar_word = embeddings_obj.get_sims(word="mōnaþ")[0][0]
        self.assertEqual(most_similar_word, "hāliȝmōnaþ")

        embeddings_obj = FastTextEmbeddings(iso_code="arb", interactive=False, overwrite=False, silent=True)
        most_similar_word = embeddings_obj.get_sims(word="بعدها")[0][0]
        self.assertEqual(most_similar_word, "وبعدها")

        embeddings_obj = FastTextEmbeddings(iso_code="arc", interactive=False, overwrite=False, silent=True)
        most_similar_word = embeddings_obj.get_sims(word="ܒܠܚܘܕ")[0][0]
        self.assertEqual(most_similar_word, "ܠܒܪ")

        embeddings_obj = FastTextEmbeddings(iso_code="got", interactive=False, overwrite=False, silent=True)
        most_similar_word = embeddings_obj.get_sims(word="𐍅𐌰𐌹𐌷𐍄𐌹𐌽𐍃")[0][0]
        self.assertEqual(most_similar_word, "𐍅𐌰𐌹𐌷𐍄𐍃")

        embeddings_obj = FastTextEmbeddings(iso_code="lat", interactive=False, overwrite=False, silent=True)
        most_similar_word = embeddings_obj.get_sims(word="amicitia")[0][0]
        self.assertEqual(most_similar_word, "amicitiam")

        embeddings_obj = FastTextEmbeddings(iso_code="pli", interactive=False, overwrite=False, silent=True)
        most_similar_word = embeddings_obj.get_sims(word="anattamanā")[0][0]
        self.assertEqual(most_similar_word, "kupitā")

        embeddings_obj = FastTextEmbeddings(iso_code="san", interactive=False, overwrite=False, silent=True)
        most_similar_word = embeddings_obj.get_sims(word="निर्माणम्")[0][0]
        self.assertEqual(most_similar_word, "निर्माणमपि")

    def test_embeddings_word2vec(self):
        # TODO: Add Arabic test; fails with `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xce in position 97: invalid continuation byte`
        # embeddings_obj = Word2VecEmbeddings(iso_code="arb", interactive=False, overwrite=False, silent=True)
        # most_similar_word = embeddings_obj.get_sims(word="ἦλθον")[0][0]
        # self.assertEqual(most_similar_word, "ἀφικόμην")

        embeddings_obj = Word2VecEmbeddings(iso_code="chu", interactive=False, overwrite=False, silent=True)
        most_similar_word = embeddings_obj.get_sims(word="обꙑчаѥмь")[0][0]
        self.assertEqual(most_similar_word, "дрьжавꙑ")

        embeddings_obj = Word2VecEmbeddings(iso_code="grc", interactive=False, overwrite=False, silent=True)
        most_similar_word = embeddings_obj.get_sims(word="ἦλθον")[0][0]
        self.assertEqual(most_similar_word, "ἀφικόμην")

        embeddings_obj = Word2VecEmbeddings(iso_code="lat", interactive=False, overwrite=False, silent=True)
        most_similar_word = embeddings_obj.get_sims(word="amicitia")[0][0]
        self.assertEqual(most_similar_word, "amicitiam")


if __name__ == "__main__":
    unittest.main()
