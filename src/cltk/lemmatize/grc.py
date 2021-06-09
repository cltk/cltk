"""Module for lemmatizing Ancient Greek."""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License. See LICENSE."

import os
from typing import List

from cltk.lemmatize.backoff import (
    DictLemmatizer,
    IdentityLemmatizer,
    RegexpLemmatizer,
    UnigramLemmatizer,
)
from cltk.utils import CLTK_DATA_DIR
from cltk.utils.file_operations import open_pickle

greek_sub_patterns = [("(ων)(ος|ι|να)$", r"ων")]

models_path = os.path.normpath(
    os.path.join(CLTK_DATA_DIR, "grc/model/grc_models_cltk/lemmata/backoff")
)


class GreekBackoffLemmatizer:
    """Suggested backoff chain; includes at least on of each
    type of major sequential backoff class from backoff.py.
    """

    def __init__(
        self: object, train: List[list] = None, seed: int = 3, verbose: bool = False
    ):
        self.models_path = models_path

        missing_models_message = "GreekBackoffLemmatizer requires the ```grc_models_cltk``` to be in cltk_data. Please load this corpus."

        try:
            self.train = open_pickle(
                os.path.join(self.models_path, "greek_lemmatized_sents.pickle")
            )
            self.GREEK_OLD_MODEL = open_pickle(
                os.path.join(self.models_path, "greek_lemmata_cltk.pickle")
            )
            self.GREEK_MODEL = open_pickle(
                os.path.join(self.models_path, "greek_model.pickle")
            )
        except FileNotFoundError as err:
            raise type(err)(missing_models_message)

        self.greek_sub_patterns = greek_sub_patterns

        self.seed = seed
        self.VERBOSE = verbose

        def _randomize_data(train: List[list], seed: int):
            import random

            random.seed(seed)
            random.shuffle(train)
            train_size = int(0.9 * len(train))
            pos_train_sents = train[:train_size]
            lem_train_sents = [[(item[0], item[1]) for item in sent] for sent in train]
            train_sents = lem_train_sents[:train_size]
            test_sents = lem_train_sents[train_size:]

            return pos_train_sents, train_sents, test_sents

        self.pos_train_sents, self.train_sents, self.test_sents = _randomize_data(
            self.train, self.seed
        )
        self._define_lemmatizer()

    def _define_lemmatizer(self: object):
        # Suggested backoff chain--should be tested for optimal order
        self.backoff0 = None
        self.backoff1 = IdentityLemmatizer(verbose=self.VERBOSE)
        self.backoff2 = DictLemmatizer(
            lemmas=self.GREEK_OLD_MODEL,
            source="Morpheus Lemmas",
            backoff=self.backoff1,
            verbose=self.VERBOSE,
        )
        self.backoff3 = RegexpLemmatizer(
            self.greek_sub_patterns,
            source="CLTK Greek Regex Patterns",
            backoff=self.backoff2,
            verbose=self.VERBOSE,
        )
        self.backoff4 = UnigramLemmatizer(
            self.train_sents,
            source="CLTK Sentence Training Data",
            backoff=self.backoff3,
            verbose=self.VERBOSE,
        )
        self.backoff5 = DictLemmatizer(
            lemmas=self.GREEK_MODEL,
            source="Greek Model",
            backoff=self.backoff4,
            verbose=self.VERBOSE,
        )
        self.lemmatizer = self.backoff5

    def lemmatize(self: object, tokens: List[str]):
        """
        Lemmatize a list of words.

        >>> lemmatizer = GreekBackoffLemmatizer()
        >>> from cltk.alphabet.text_normalization import cltk_normalize
        >>> word = cltk_normalize('διοτρεφές')
        >>> lemmatizer.lemmatize([word])
        [('διοτρεφές', 'διοτρεφής')]
        >>> republic = cltk_normalize("κατέβην χθὲς εἰς Πειραιᾶ μετὰ Γλαύκωνος τοῦ Ἀρίστωνος")
        >>> lemmatizer.lemmatize(republic.split())
        [('κατέβην', 'καταβαίνω'), ('χθὲς', 'χθές'), ('εἰς', 'εἰς'), ('Πειραιᾶ', 'Πειραιεύς'), ('μετὰ', 'μετά'), ('Γλαύκωνος', 'Γλαύκων'), ('τοῦ', 'ὁ'), ('Ἀρίστωνος', 'Ἀρίστων')]
        """

        lemmas = self.lemmatizer.lemmatize(tokens)
        return lemmas

    def evaluate(self: object):
        if self.VERBOSE:
            raise AssertionError(
                "evaluate() method only works when verbose: bool = False"
            )
        return self.lemmatizer.evaluate(self.test_sents)

    def __repr__(self: object):
        return f"<BackoffGreekLemmatizer v0.1>"

    def __call__(self, token: str) -> str:
        return self.lemmatize([token])[0][0]
