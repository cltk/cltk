#encoding :utf-8

import os
import re

from nltk.probability import ConditionalFreqDist
from nltk.tag.api import TaggerI
from nltk.tag.sequential import SequentialBackoffTagger, ContextTagger, DefaultTagger, NgramTagger, UnigramTagger, RegexpTagger
from cltk.tokenize.word import WordTokenizer
from cltk.utils.file_operations import open_pickle
from cltk.lemmatize.french.lex import entries


def backoff_lemmatizer(train_sents, lemmatizer_classes, backoff=None):
    """From Python Text Processing with NLTK Cookbook."""
    for cls in lemmatizer_classes:
        backoff = cls(train_sents, backoff=backoff)
    return backoff


class LemmatizerI(TaggerI):
    """Inherit base tagging class for Latin lemmatizer."""
   # def __init__(self):
   #     TaggerI.__init__(self)
    pass


class SequentialBackoffLemmatizer(LemmatizerI, SequentialBackoffTagger):
    """"""
    def __init__(self, backoff=None):
        """Setup for SequentialBackoffLemmatizer()

        :param backoff: Next lemmatizer in backoff chain.
        """
        LemmatizerI.__init__(self)
        SequentialBackoffTagger.__init__(self, backoff)

    def lemmatize(self, tokens):
        """Transform tag method into custom method for lemmatizing tasks. Can
        be overwritten by specific instances where list of tokens should
        be handled in a different manner. (Cf. IdentityLemmatizer)

        :param tokens: List of tokens to be lemmatized
        :return: Tuple of the form (TOKEN, LEMMA)
        """
        return SequentialBackoffLemmatizer.tag(self, tokens)

    def choose_tag(self, tokens, index, history):
        """Override choose_tag with lemmatizer-specific method for various
        methods that expect a method with this name.

        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized
        :return: String with lemma, if found; otherwise NONE
        """
        return self.choose_lemma(tokens, index, history)


class DefaultLemmatizer(SequentialBackoffLemmatizer, DefaultTagger):
    """"""
    def __init__(self, lemma=None):
        """Setup for DefaultLemmatizer().

        :param lemma: String with default lemma to be assigned for all tokens;
        set to None if no parameter is assigned.
        """
        self._lemma = lemma
        SequentialBackoffLemmatizer.__init__(self, None)
        DefaultTagger.__init__(self, self._lemma)

    def choose_lemma(self, tokens, index, history):
        return DefaultTagger.choose_tag(self, tokens, index, history)



class DictLemmatizer(SequentialBackoffLemmatizer):
    """Standalone version of 'model' function found in UnigramTagger; by
    defining as its own class, it is clearer that this lemmatizer is
    based on dictionary lookup and does not use training data."""

    def choose_lemma(self, tokens, index, history):
        """Returns the given token as the lemma.

        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized; NOT USED
        :return: String, spec. the dictionary value found with token as key.
        """
        for lemma, entry in entries:
            if tokens == lemma:
                return (tokens, lemma)



