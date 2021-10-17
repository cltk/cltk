"""Lemmatization module—includes several classes for different
lemmatizing approaches--based on training data, regex pattern matching,
etc. These can be chained together using the backoff parameter. Also,
includes a pre-built chain that uses models in cltk_data.

The logic behind the backoff lemmatizer is based on backoff POS-tagging in
NLTK and repurposes several of the tagging classes for lemmatization
tasks. See here for more info on sequential backoff tagging in NLTK:
http://www.nltk.org/_modules/nltk/tag/sequential.html

PJB: The Latin lemmatizer modules were completed as part of Google Summer of Code
2016. I have written up a detailed report of the summer work here:
https://gist.github.com/diyclassics/fc80024d65cc237f185a9a061c5d4824.
"""

import re
import reprlib
from typing import List

from nltk.tag.sequential import RegexpTagger, SequentialBackoffTagger, UnigramTagger


class SequentialBackoffLemmatizer(SequentialBackoffTagger):
    """Abstract base class for lemmatizers created as a subclass of
    NLTK's SequentialBackoffTagger. Lemmatizers in this class "[tag]
    words sequentially, left to right. Tagging of individual words is
    performed by the ``choose_tag()`` method, which should be defined
    by subclasses.  If a tagger is unable to determine a tag for the
    specified token, then its backoff tagger is consulted."

    See: https://www.nltk.org/_modules/nltk/tag/sequential.html#SequentialBackoffTagger

    :type _taggers: list
    :ivar _taggers: A list of all the taggers in the backoff chain,
        inc. self.
    :type _repr: Repr object
    :ivar _repr: An instance of Repr() from reprlib to handle list
        and dict length in subclass __repr__'s
    """

    def __init__(self: object, backoff: object, verbose: bool = False):
        """Setup for SequentialBackoffLemmatizer
        :param backoff: Next lemmatizer in backoff chain
        :type verbose: bool
        :param verbose: Flag to include which lemmatizer assigned in
            a given tag in the return tuple
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

    def tag(self: object, tokens: List[str]):
        """Docs (mostly) inherited from TaggerI; cf.
        https://www.nltk.org/_modules/nltk/tag/api.html#TaggerI.tag

        Two tweaks:
        1. Properly handle 'verbose' listing of current tagger in
        the case of None (i.e. ``if tag: etc.``)
        2. Keep track of taggers and change return depending on
        'verbose' flag

        :rtype list
        :type tokens: list
        :param tokens: List of tokens to tag
        """
        tags = []
        taggers = []
        for i in range(len(tokens)):
            tag, tagger = self.tag_one(tokens, i, tags)
            tags.append(tag)
            taggers.append(str(tagger)) if tag else taggers.append(None)

        if self.VERBOSE:
            return list(zip(tokens, tags, taggers))
        else:
            return list(zip(tokens, tags))

    def tag_one(self: object, tokens: List[str], index: int, history: List[str]):
        """Determine an appropriate tag for the specified token, and
        return that tag.  If this tagger is unable to determine a tag
        for the specified token, then its backoff tagger is consulted.

        :rtype: tuple
        :type tokens: list
        :param tokens: The list of words that are being tagged.
        :type index: int
        :param index: The index of the word whose tag should be
            returned.
        :type history: list(str)
        :param history: A list of the tags for all words before index.
        """
        lemma = None
        for tagger in self._taggers:
            lemma = tagger.choose_tag(tokens, index, history)
            if lemma is not None and lemma != "":
                break
        return lemma, tagger

    def lemmatize(self: object, tokens: List[str]):
        """
        Transform tag method into custom method for lemmatizing
        tasks. Cf. ``tag`` method above.
        """
        return self.tag(tokens)


class DefaultLemmatizer(SequentialBackoffLemmatizer):
    """Lemmatizer that assigns the same lemma to every token. Useful as the final
    tagger in chain, e.g. to assign 'UNK' to all remaining unlemmatized tokens.
    :type lemma: str
    :param lemma: Lemma to assign to each token

    >>> default_lemmatizer = DefaultLemmatizer('UNK')
    >>> list(default_lemmatizer.lemmatize('arma virumque cano'.split()))
    [('arma', 'UNK'), ('virumque', 'UNK'), ('cano', 'UNK')]

    """

    def __init__(
        self: object, lemma: str = None, backoff: object = None, verbose: bool = False
    ):
        self.lemma = lemma
        SequentialBackoffLemmatizer.__init__(self, backoff=None, verbose=verbose)

    def choose_tag(self: object, tokens: List[str], index: int, history: List[str]):
        return self.lemma

    def __repr__(self: object):
        return f"<{type(self).__name__}: lemma={self.lemma}>"


class IdentityLemmatizer(SequentialBackoffLemmatizer):
    """Lemmatizer that returns a given token as its lemma. Like DefaultLemmatizer,
    useful as the final tagger in a chain, e.g. to assign a possible form to
    all remaining unlemmatized tokens, increasing the chance of a successful
    match.

    >>> identity_lemmatizer = IdentityLemmatizer()
    >>> list(identity_lemmatizer.lemmatize('arma virumque cano'.split()))
    [('arma', 'arma'), ('virumque', 'virumque'), ('cano', 'cano')]
    """

    def __init__(self: object, backoff: object = None, verbose: bool = False):
        SequentialBackoffLemmatizer.__init__(self, backoff=None, verbose=verbose)

    def choose_tag(self: object, tokens: List[str], index: int, history: List[str]):
        return tokens[index]

    def __repr__(self: object):
        return f"<{type(self).__name__}>"


class DictLemmatizer(SequentialBackoffLemmatizer):
    """Standalone version of 'model' function found in UnigramTagger; by
    defining as its own class, it is clearer that this lemmatizer is
    based on dictionary lookup and does not use training data."""

    def __init__(
        self: object,
        lemmas: List[str],
        backoff: object = None,
        source: str = None,
        verbose: bool = False,
    ):
        """
        Setup for DictLemmatizer().
        :type lemmas: dict
        :param lemmas: Dictionary with form {TOKEN: LEMMA} to be used
            as foor 'lookup'-style lemmatization
        :param backoff: Next lemmatizer in backoff chain.
        """
        SequentialBackoffLemmatizer.__init__(self, backoff, verbose=verbose)
        self.lemmas = lemmas
        self.source = source

    def choose_tag(self: object, tokens: List[str], index: int, history: List[str]):
        """
        Looks up token in ``lemmas`` dict and returns the corresponding
        value as lemma.
        :rtype: str
        :type tokens: list
        :param tokens: List of tokens to be lemmatized
        :type index: int
        :param index: Int with current token
        :type history: list
        :param history: List with tokens that have already been lemmatized; NOT USED
        """
        keys = self.lemmas.keys()
        if tokens[index] in keys:
            return self.lemmas[tokens[index]]

    def __repr__(self: object):
        if self.source:
            return f"<{type(self).__name__}: {self.source}>"
        else:
            return f"<{type(self).__name__}: {self.repr.repr(self.lemmas)}>"


class UnigramLemmatizer(SequentialBackoffLemmatizer, UnigramTagger):
    """Standalone version of 'train' function found in UnigramTagger; by
    defining as its own class, it is clearer that this lemmatizer is
    based on training data and not on dictionary.
    """

    def __init__(
        self: object,
        train=None,
        model=None,
        backoff: object = None,
        source: str = None,
        cutoff=0,
        verbose: bool = False,
    ):
        """
        Setup for UnigramLemmatizer()
        """
        SequentialBackoffLemmatizer.__init__(self, backoff=None, verbose=verbose)
        UnigramTagger.__init__(self, train, model, backoff, cutoff)
        self.train = train
        self.source = source

    def __repr__(self: object):
        if self.source:
            return f"<{type(self).__name__}: {self.source}>"
        else:
            return f"<{type(self).__name__}: {self.repr.repr(self.train)}>"


class RegexpLemmatizer(SequentialBackoffLemmatizer, RegexpTagger):
    """Regular expression tagger, inheriting from
    ``SequentialBackoffLemmatizer`` and ``RegexpTagger``.
    """

    def __init__(
        self: object, regexps=None, source=None, backoff=None, verbose: bool = False
    ):
        """Setup for RegexpLemmatizer()
        :type regexps: list
        :param regexps: List of tuples of form (PATTERN, REPLACEMENT)
        :param backoff: Next lemmatizer in backoff chain.
        """
        SequentialBackoffLemmatizer.__init__(self, backoff=None, verbose=verbose)
        RegexpTagger.__init__(self, regexps, backoff)
        self._regexs = regexps
        self.source = source

    def choose_tag(self: object, tokens: List[str], index: int, history: List[str]):
        """Use regular expressions for rules-based lemmatizing based on word endings;
        tokens are matched for patterns with the base kept as a group; an word ending
        replacement is added to the (base) group.
        :rtype: str
        :type tokens: list
        :param tokens: List of tokens to be lemmatized
        :type index: int
        :param index: Int with current token
        :type history: list
        :param history: List with tokens that have already been lemmatized; NOT USED
        """
        for pattern, replace in self._regexs:
            if re.search(pattern, tokens[index]):
                return re.sub(pattern, replace, tokens[index])

    def __repr__(self: object):
        if self.source:
            return f"<{type(self).__name__}: {self.source}>"
        else:
            return f"<{type(self).__name__}: {self.repr.repr(self._regexs)}>"
