""" Code for sentences tokenization: Latin

>>> from cltk.sentence.lat import LatinPunktSentenceTokenizer
>>> from cltk.languages.example_texts import get_example_text
>>> splitter = LatinPunktSentenceTokenizer()
>>> sentences = splitter.tokenize(get_example_text("lat"))
>>> sentences[2]
'Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit.'
>>> len(sentences)
8
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License."

import os

from nltk.tokenize.punkt import PunktLanguageVars

from cltk.sentence.sentence import PunktSentenceTokenizer
from cltk.utils import CLTK_DATA_DIR
from cltk.utils.file_operations import open_pickle


class LatinLanguageVars(PunktLanguageVars):
    _re_non_word_chars = PunktLanguageVars()._re_non_word_chars.replace("'", "")


PUNCTUATION = (".", "?", "!")
STRICT_PUNCTUATION = PUNCTUATION + ("-", ":", ";")


class LatinPunktSentenceTokenizer(PunktSentenceTokenizer):
    """Sentence tokenizer for Latin. Inherits from NLTK's ``PunktSentenceTokenizer``."""

    def __init__(self: object, strict: bool = False):
        """Constructor for ``LatinPunktSentenceTokenizer``.

        :param strict : allow for stricter punctuation for sentences tokenization
        :type strict: bool
        """
        self.lang_vars = LatinLanguageVars()
        self.strict = strict
        super().__init__(language="lat", lang_vars=self.lang_vars)

        fp_sentence_tok_model_dir = "lat/model/lat_models_cltk/tokenizers/sentence/"
        models_path = os.path.join(CLTK_DATA_DIR, fp_sentence_tok_model_dir)
        self.models_path = os.path.join(models_path, "latin_punkt.pickle")

        try:
            self.model = open_pickle(self.models_path)
        except FileNotFoundError as err:
            msg = f"``LatinPunktSentenceTokenizer`` could not find required file ``{self.models_path}``. Download the corpus ``lat_models_cltk``."
            raise FileNotFoundError(msg)

        if self.strict:
            PunktLanguageVars.sent_end_chars = STRICT_PUNCTUATION
        else:
            PunktLanguageVars.sent_end_chars = PUNCTUATION
