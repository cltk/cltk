import math
import os
import re
from abc import ABC, abstractmethod
from typing import List, Tuple, Union

from numpy import argmax

from cltk.utils import CLTK_DATA_DIR


def _build_match_and_apply_functions(pattern, replace):
    def matches_rule(word):
        return re.search(pattern, word)

    def apply_rule(word):
        return re.sub(pattern, replace, word)

    return (matches_rule, apply_rule)


class DictionaryRegexLemmatizer(ABC):
    """Implementation of a lemmatizer based on a
    dictionary of lemmas and forms, backing off to regex rules.
    Since a given form may map to multiple lemmas,
    a corpus-based frequency disambiguator is employed.

    Subclasses must provide methods to load dictionary and corpora,
    and to specify regular expressions.
    """

    def __init__(self):
        self.inverted_index = self._load_forms_and_lemmas()
        self.unigram_counts = self._load_unigram_counts()

        self.regex_rules = [
            _build_match_and_apply_functions(pattern, replace)
            for (pattern, replace) in self._specify_regex_rules()
        ]

        super().__init__()

    @abstractmethod
    def _load_forms_and_lemmas(self):
        pass

    @abstractmethod
    def _load_unigram_counts(self):
        pass

    @abstractmethod
    def _specify_regex_rules(self):
        pass

    def _relative_frequency(self, word: str) -> float:
        """Computes the log relative frequency for a word form"""

        count = self.unigram_counts.get(word, 0)
        return math.log(count / len(self.unigram_counts)) if count > 0 else 0

    def _apply_regex(self, token):
        """Looks for a match in the regex rules with the token.
        If found, applies the replacement part of the rule to the token and returns the result.
        Else just returns the token unchanged.
        """
        for matches_rule, apply_rule in self.regex_rules:
            if matches_rule(token):
                return apply_rule(token)
        return token

    def lemmatize_token(
        self, token: str, best_guess: bool = True, return_frequencies: bool = False
    ) -> Union[str, List[Union[str, Tuple[str, float]]]]:
        """Lemmatize a single token.  If best_guess is true, then take the most
        frequent lemma when a form has multiple possible lemmatizations.
        If the form is not found, just return it.
        If best_guess is false, then
        always return the full set of possible lemmas, or the empty list if none found.
        If return_frequencies is true ,then also return the relative frequency of the lemma in a corpus.

        >>> from cltk.lemmatize.ang import OldEnglishDictionaryLemmatizer
        >>> lemmatizer = OldEnglishDictionaryLemmatizer()
        >>> lemmatizer.lemmatize_token('fōrestepeþ')
        'foresteppan'
        >>> lemmatizer.lemmatize_token('Caesar', return_frequencies=True, best_guess=True)
        ('Caesar', 0)
        """

        lemmas = self.inverted_index.get(token.lower(), None)
        if not lemmas:
            mod_token = self._apply_regex(token.lower())
            lemmas = self.inverted_index.get(mod_token, None)

        if best_guess:
            if not lemmas:
                lemma = token
            elif len(lemmas) > 1:
                counts = [self.unigram_counts.get(word, 0) for word in lemmas]
                lemma = lemmas[argmax(counts)]
            else:
                lemma = lemmas[0]

            if return_frequencies:
                lemma = (lemma, self._relative_frequency(lemma))
        else:
            lemma = [] if not lemmas else lemmas
            if return_frequencies:
                lemma = [(word, self._relative_frequency(word)) for word in lemma]

        return lemma

    def lemmatize(
        self,
        tokens: List[str],
        best_guess: bool = True,
        return_frequencies: bool = False,
    ) -> Union[str, List[Union[str, Tuple[str, float]]]]:
        """
        Lemmatize tokens in a list of strings.

        >>> from cltk.lemmatize.ang import OldEnglishDictionaryLemmatizer
        >>> lemmatizer = OldEnglishDictionaryLemmatizer()
        >>> lemmatizer.lemmatize(['eotenas','ond','ylfe','ond','orcneas'], return_frequencies=True, best_guess=True)
        [('eoten', -9.227295812625597), ('and', -2.8869365088978443), ('ylfe', -9.227295812625597), ('and', -2.8869365088978443), ('orcneas', -9.227295812625597)]
        """

        return [
            self.lemmatize_token(token, best_guess, return_frequencies)
            for token in tokens
        ]

    def __call__(self, token: str) -> str:
        return self.lemmatize_token(token)
