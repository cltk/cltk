"""Ensemble Lemmatizer module, includes several classes for different
lemmatizing approaches--based on training data, regex pattern matching, etc.
These can be chained together using the backoff parameter. Unlike backoff
lemmatizer, ensemble lemmatizer uses tag information from every lemmatizer in
the backoff chain and returns available lemmas. Selection and scoring
mechanisms for use with the Ensemble Lemmatizer are under development.

Ensemble Lemmatizer classes are subclasses of the NLTK SequentialBackoffTagger
with modifications made for lemmatization and for better integration with CLTK.
NLTK SequentialBackoffTagger available for modification and distribution under
the Apache License 2.0 (https://github.com/nltk/nltk/blob/develop/LICENSE.txt).
The original code is (C) 2001-2020 NLTK Project.
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

import os
import re
from collections import defaultdict, Counter

from typing import List, Dict, Tuple, Set, Any, Generator
import reprlib

from nltk.probability import ConditionalFreqDist
from nltk.tag.api import TaggerI
from nltk.tag.sequential import SequentialBackoffTagger, ContextTagger, DefaultTagger, NgramTagger, UnigramTagger, RegexpTagger

from cltk.utils.file_operations import open_pickle

from pprint import pprint

class SequentialEnsembleLemmatizer(SequentialBackoffTagger):
    """
    Abstract base class for lemmatizers created as a subclass of
    NLTK's SequentialBackoffTagger. Lemmatizers in this class "[tag]
    words sequentially, left to right. Tagging of individual words is
    performed by the ``choose_tag()`` method, which should be defined
    by subclasses. Unlike the actual backoff tagger, every tagger
    supplied either returns a scored result or None. There scores can
    be used to choose a single lemma or a list of possible lemmas.

    :type _taggers: list
    :ivar _taggers: A list of all the taggers in the backoff chain,
        inc. self.
    :type _repr: Repr object
    :ivar _repr: An instance of Repr() from reprlib to handle list
        and dict length in subclass __repr__'s
    """
    def __init__(self: object, backoff: object, verbose: bool = False):
        """
        Setup for SequentialBackoffLemmatizer

        :param backoff: Next lemmatizer in backoff chain
        :param verbose: Flag to include which lemmatizer assigned in a given tag in the return tuple
        """
        SequentialBackoffTagger.__init__(self, backoff=None)
        # Setup backoff chain
        if backoff is None:
            self._taggers = [self]
        else:
            self._taggers = [self] + backoff._taggers

        self.VERBOSE = verbose
        self.repr = reprlib.Repr()
        self.repr.maxlist = 1
        self.repr.maxdict = 1

    def lemmatize(self: object, tokens: List[str], lemmas_only: bool = False):
        """
        Transform tag method into custom method for lemmatizing tasks. Cf. ``tag`` method above.

        :param tokens: List of tokens to tag
        """

        def extract_lemma_scores(ensemble_lemmas):
            lemma_scores = []
            for token, lemma in ensemble_lemmas:
                lemma_scores_ = []
                for lemma_ in lemma:
                    for value in lemma_.values():
                        for value_ in value:
                            lemma_scores_.append(value_)
                lemma_scores.append(lemma_scores_)
            return lemma_scores

        def get_all_matches(lemma):
            # https://stackoverflow.com/a/35344958/1816347
            return sorted(set([lemma_[0] for lemma_ in lemma]))

        if lemmas_only:
            lemma_scores = extract_lemma_scores(self.tag(tokens))
            lemmas = []
            for lemma_score in lemma_scores:
                lemmas.append(get_all_matches(lemma_score))
            return lemmas
        else:
            return self.tag(tokens)

    def tag(self: object, tokens: List[str]):
        """ (Mostly) inherited from TaggerI; cf.
        https://www.nltk.org/_modules/nltk/tag/api.html#TaggerI.tag

        :rtype list
        :param tokens: List of tokens to tag
        """
        tags = []
        for i in range(len(tokens)):
            tag = self.tag_one(tokens, i, tags)
            tags.append(tag)

        output = []
        for i, token in enumerate(tokens):
            lemmas = []
            for tag in tags[i]:
                if tag:
                    lemmas.append(tag)
            output.append((token, lemmas))
        return output

    def tag_one(self: object, tokens: List[str], index: int, history: List[str]):
        """
        Determine an appropriate tag for the specified token, and
        return that tag.  If this tagger is unable to determine a tag
        for the specified token, then its backoff tagger is consulted.

        :rtype: tuple
        :param tokens: The list of words that are being tagged.
        :param index: The index of the word whose tag should be
            returned.
        :param history: A list of the tags for all words before index.
        """
        lemma = None
        lemmas = []
        for tagger in self._taggers:
            lemma = tagger.choose_tag(tokens, index, history)
            if isinstance(lemma, str):
                lemmas.append({str(tagger): [(lemma, 100)]})
            elif isinstance(lemma, list):
                lemmas.append({str(tagger): lemma})
            else:
                lemmas.append(None)

        return lemmas


class EnsembleDictLemmatizer(SequentialEnsembleLemmatizer):
    """
    Lexicon-based lemmatizer.
    """
    def __init__(self: object, lemmas: dict, backoff: object = None, source: str = None, verbose: bool = False):
        """
        Setup for EnsembleDictLemmatizer().

        :param lemmas: Dictionary with form {TOKEN: LEMMA} to be used for 'lookup'-style lemmatization
        :param backoff: Next lemmatizer in backoff chain
        :param source: String for labelling lemmatizer in repr; used by verbose mode
        :param verbose: Flag to include which lemmatizer assigned in a given tag in the return tuple
        """
        SequentialEnsembleLemmatizer.__init__(self, backoff, verbose=verbose)
        self.lemmas = lemmas
        self.source = source

    def choose_tag(self: object, tokens: List[str], index: int, history: List[str]):
        """
        Looks up token in ``lemmas`` dict and returns the corresponding value as lemma.

        :rtype: str
        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized; NOT USED
        """
        keys = self.lemmas.keys()
        if tokens[index] in keys:
            return self.lemmas[tokens[index]]

    def __repr__(self: object):
        if self.source:
            return f'<{type(self).__name__}: {self.source}>'
        else:
            return f'<{type(self).__name__}>'


class EnsembleUnigramLemmatizer(SequentialEnsembleLemmatizer, UnigramTagger):
    """
    Frequency-distribution-based lemmatization based on training data
    """
    def __init__(self: object, train=None, model=None, backoff: object = None, source: str = None, cutoff=0, verbose: bool = False):
        """
        Setup for EnsembleUnigramLemmatizer()

        :param train: List of sentences, tokenized as tuples of (TOKEN, LEMMA)
        :param model: Not used; vestige of NLTK backoff and should be removed in future refactoring
        :param backoff: Next lemmatizer in backoff chain
        :param source: String for labelling lemmatizer in repr; used by verbose mode
        :param cutoff: Minimum frequency in frequency distribution to return a lemma
        :param verbose: Flag to include which lemmatizer assigned in a given tag in the return tuple
        """
        SequentialEnsembleLemmatizer.__init__(self, backoff=None, verbose=verbose)
        UnigramTagger.__init__(self, train, model, backoff, cutoff)
        self.train = train
        self.source = source


    def _train(self, tagged_corpus: list, cutoff: int = 0, verbose: bool = False):
        """
        Initialize this ContextTagger's ``_context_to_tag`` table
        based on the given training data.  In particular, for each
        context ``c`` in the training data, set
        ``_context_to_tag[c]`` to the most frequent tag for that
        context.  However, exclude any contexts that are already
        tagged perfectly by the backoff tagger(s).

        The old value of ``self._context_to_tag`` (if any) is discarded.

        :param tagged_corpus: A tagged corpus.  Each item should be
            a list of (word, tag) tuples.
        :param cutoff: If the most likely tag for a context occurs
            fewer than cutoff times, then exclude it from the
            context-to-tag table for the new tagger.
        :param verbose: Not used
        """

        token_count = hit_count = 0

        # A context is considered 'useful' if it's not already tagged
        # perfectly by the backoff tagger.
        useful_contexts = set()

        # Count how many times each tag occurs in each context.
        fd = ConditionalFreqDist()
        for sentence in tagged_corpus:
            tokens, tags = zip(*sentence)
            for index, (token, tag) in enumerate(sentence):
                # Record the event.
                token_count += 1
                context = self.context(tokens, index, tags[:index])
                if context is None:
                    continue
                fd[context][tag] += 1
                # If the backoff got it wrong, this context is useful:
                if self.backoff is None or tag != self.backoff.tag_one(
                    tokens, index, tags[:index]
                ):
                    useful_contexts.add(context)

        # Build the context_to_tag table -- for each context, figure
        # out what the most likely tag is.  Only include contexts that
        # we've seen at least `cutoff` times.
        for context in useful_contexts:
            best_tag = fd[context].max() # Remove
            weighted_tags = [(k, v/sum(fd[context].values())) for k, v in fd[context].items()]
            hits = fd[context][best_tag] #INT
            if hits > cutoff:
                self._context_to_tag[context] = weighted_tags
                hit_count += hits


    def choose_tag(self: object, tokens: List[str], index: int, history: List[str]):
        """
        Looks up token in ``lemmas`` dict and returns the corresponding value as lemma.

        :rtype: str
        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized; NOT USED
        """
        keys = self._context_to_tag.keys()
        if tokens[index] in keys:
            return self._context_to_tag[tokens[index]]

    def __repr__(self: object):
        if self.source:
            return f'<{type(self).__name__}: {self.source}>'
        else:
            return f'<{type(self).__name__}: {self.repr.repr(self.train)}>'


class EnsembleRegexpLemmatizer(SequentialEnsembleLemmatizer, RegexpTagger):
    """
    Regex-based lemmatizer
    """
    def __init__(self: object, regexps=None, backoff=None, source: str = None, verbose: bool = False):
        """Setup for RegexpLemmatizer()
        :param regexps: List of tuples of form (PATTERN, REPLACEMENT)
        :param backoff: Next lemmatizer in backoff chain
        :param source: String for labelling lemmatizer in repr; used by verbose mode
        :param verbose: Flag to include which lemmatizer assigned in a given tag in the return tuple
        """
        SequentialEnsembleLemmatizer.__init__(self, backoff=None, verbose=verbose)
        RegexpTagger.__init__(self, regexps, backoff)
        self._regexs = regexps
        self.source = source

    def choose_tag(self: object, tokens: List[str], index: int, history: List[str]):
        """Use regular expressions for rules-based lemmatizing based on word endings;
        tokens are matched for patterns with the base kept as a group; an word ending
        replacement is added to the (base) group.
        :rtype: str
        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized; NOT USED
        """
        hits = []

        for pattern, replace in self._regexs:
            if re.search(pattern, tokens[index]):
                hits.append(re.sub(pattern, replace, tokens[index]))
        hits = list(set(hits))
        hits = [(hit, 1/len(hits)) for hit in hits]
        return hits if hits else None

    def __repr__(self: object):
        if self.source:
            return f'<{type(self).__name__}: {self.source}>'
        else:
            return f'<{type(self).__name__}: {self.repr.repr(self._regexs)}>'


if __name__ == '__main__':
    test = "arma virumque cano qui".split()
    patterns = [
    (r'\b(.+)(o|is|it|imus|itis|unt)\b', r'\1o'),
    (r'\b(.+)(o|as|at|amus|atis|ant)\b', r'\1o'),
]
    EDL = EnsembleDictLemmatizer(lemmas = {'cano': 'cano'}, source='EDL', verbose=True)
    EUL = EnsembleUnigramLemmatizer(train=[
            [('arma', 'arma'), ('virumque', 'vir'), ('cano', 'cano')],
            [('arma', 'arma'), ('virumque', 'virus'), ('cano', 'canus')],
            [('arma', 'arma'), ('virumque', 'vir'), ('cano', 'canis')],
            [('arma', 'arma'), ('virumque', 'vir'), ('cano', 'cano')],
            ], verbose=True, backoff=EDL)
    ERL = EnsembleRegexpLemmatizer(regexps=patterns, source='Latin Regex Patterns', verbose=True, backoff=EUL)
    ensemble_lemmas = ERL.lemmatize(test, lemmas_only=False)
    print(ensemble_lemmas)
