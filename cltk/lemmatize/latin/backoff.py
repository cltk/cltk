"""Module for lemmatizing Latin—includes several classes for different
lemmatizing approaches--based on training data, regex pattern matching,
etc. These can be chained together using the backoff parameter. Also,
includes a pre-built chain that uses models in latin_models_cltk repo
called BackoffLatinLemmatizer.

The logic behind the backoff lemmatizer is based on backoff POS-tagging in
NLTK and repurposes several of the tagging classes for lemmatization
tasks. See here for more info on sequential backoff tagging in NLTK:
http://www.nltk.org/_modules/nltk/tag/sequential.html
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

import os
import re

import reprlib

from nltk.probability import ConditionalFreqDist
from nltk.tag.api import TaggerI
from nltk.tag.sequential import SequentialBackoffTagger, ContextTagger, DefaultTagger, NgramTagger, UnigramTagger, RegexpTagger

from cltk.utils.file_operations import open_pickle
from cltk.lemmatize.latin.latin import latin_sub_patterns, latin_verb_patterns, latin_pps, rn_patterns

# Unused for now
#def backoff_lemmatizer(train_sents, lemmatizer_classes, backoff=None):
#    """From Python Text Processing with NLTK Cookbook."""
#    for cls in lemmatizer_classes:
#        backoff = cls(train_sents, backoff=backoff)
#    return backoff

class SequentialBackoffLemmatizer(SequentialBackoffTagger):
    """
    Abstract base class for lemmatizers created as a subclass of
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

    def __init__(self, backoff, verbose=False):
        """
        Setup for SequentialBackoffLemmatizer
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


    def tag(self, tokens):
        """ Docs (mostly) inherited from TaggerI; cf.
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


    def tag_one(self, tokens, index, history):
        """
        Determine an appropriate tag for the specified token, and
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
            if lemma is not None:
                break
        return lemma, tagger


    def lemmatize(self, tokens):
        """
        Transform tag method into custom method for lemmatizing
        tasks. Cf. ``tag`` method above.
        """
        return self.tag(tokens)


class DefaultLemmatizer(SequentialBackoffLemmatizer):
    """
    Lemmatizer that assigns the same lemma to every token. Useful as the final
    tagger in chain, e.g. to assign 'UNK' to all remaining unlemmatized tokens.
    :type lemma: str
    :param lemma: Lemma to assign to each token

        >>> from cltk.lemmatize.latin.backoff import DefaultLemmatizer
        >>> default_lemmatizer = DefaultLemmatizer('UNK')
        >>> list(default_lemmatizer.lemmatize('arma virumque cano'.split()))
        [('arma', 'UNK'), ('virumque', 'UNK'), ('cano', 'UNK')]

    """
    def __init__(self, lemma=None, backoff=None, verbose=False):
        self.lemma = lemma
        SequentialBackoffLemmatizer.__init__(self, backoff=None, verbose=verbose)

    def choose_tag(self, tokens, index, history):
        return self.lemma

    def __repr__(self):
        return f'<{type(self).__name__}: lemma={self.lemma}>'


class IdentityLemmatizer(SequentialBackoffLemmatizer):
    """
    Lemmatizer that returns a given token as its lemma. Like DefaultLemmatizer,
    useful as the final tagger in a chain, e.g. to assign a possible form to
    all remaining unlemmatized tokens, increasing the chance of a successful
    match.

        >>> from cltk.lemmatize.latin.backoff import IdentityLemmatizer
        >>> identity_lemmatizer = IdentityLemmatizer()
        >>> list(identity_lemmatizer.lemmatize('arma virumque cano'.split()))
        [('arma', 'arma'), ('virumque', 'virumque'), ('cano', 'cano')]

    """
    def __init__(self, backoff=None, verbose=False):
        SequentialBackoffLemmatizer.__init__(self, backoff=None, verbose=verbose)

    def choose_tag(self, tokens, index, history):
        return tokens[index]

    def __repr__(self):
        return f'<{type(self).__name__}>'


class DictLemmatizer(SequentialBackoffLemmatizer):
    """Standalone version of 'model' function found in UnigramTagger; by
    defining as its own class, it is clearer that this lemmatizer is
    based on dictionary lookup and does not use training data."""

    def __init__(self, lemmas, backoff=None, source=None, verbose=False):
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


    def choose_tag(self, tokens, index, history):
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


    def __repr__(self):
        if self.source:
            return f'<{type(self).__name__}: {self.source}>'
        else:
            return f'<{type(self).__name__}: {self.repr.repr(self.lemmas)}>'


class UnigramLemmatizer(SequentialBackoffLemmatizer, UnigramTagger):
    """
    Standalone version of 'train' function found in UnigramTagger; by
    defining as its own class, it is clearer that this lemmatizer is
    based on training data and not on dictionary.
    """

    def __init__(self, train=None, model=None, backoff=None, source=None, cutoff=0, verbose=False):
        """
        Setup for UnigramLemmatizer()
        """
        SequentialBackoffLemmatizer.__init__(self, backoff=None, verbose=verbose)
        UnigramTagger.__init__(self, train, model, backoff, cutoff)
        self.train = train
        self.source = source


    def __repr__(self):
        if self.source:
            return f'<{type(self).__name__}: {self.source}>'
        else:
            return f'<{type(self).__name__}: {self.repr.repr(self.train)}>'


class RegexpLemmatizer(SequentialBackoffLemmatizer, RegexpTagger):
    """"""

    def __init__(self, regexps=None, source=None, backoff=None, verbose=False):
        """Setup for RegexpLemmatizer()
        :type regexps: list
        :param regexps: List of tuples of form (PATTERN, REPLACEMENT)
        :param backoff: Next lemmatizer in backoff chain.
        """
        SequentialBackoffLemmatizer.__init__(self, backoff=None, verbose=verbose)
        RegexpTagger.__init__(self, regexps, backoff)
        self._regexs = regexps
        self.source = source


    def choose_tag(self, tokens, index, history):
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


    def __repr__(self):
        if self.source:
            return f'<{type(self).__name__}: {self.source}>'
        else:
            return f'<{type(self).__name__}: {self.repr.repr(self._regexs)}>'


class RomanNumeralLemmatizer(RegexpLemmatizer):
    """

    """
    def __init__(self, default=None, backoff=None):
        """
        RomanNumeralLemmatizer
        :type default: str
        :param default: Default replacement for lemma; 'NUM' in given pattern
        """
        regexps = [
            (r'(?=^[MDCLXVUI]+$)(?=^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|IU|V?I{0,3}|U?I{0,3})$)', 'NUM'),
            (r'(?=^[mdclxvui]+$)(?=^m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|iu|v?i{0,3}|u?i{0,3})$)', 'NUM')
            ]
        RegexpLemmatizer.__init__(self, regexps, backoff)
        self._regexs = [(re.compile(regexp), pattern,) for regexp, pattern in regexps]
        self.default = default

    def choose_tag(self, tokens, index, history):
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
                if self.default:
                    return self.default
                else:
                    return replace

    def __repr__(self):
        return f'<{type(self).__name__}: CLTK Roman Numeral Patterns>'

class BackoffLatinLemmatizer(object):
    """Suggested backoff chain; includes at least on of each
    type of major sequential backoff class from backoff.py

    ### Putting it all together
    ### BETA Version of the Backoff Lemmatizer AKA BackoffLatinLemmatizer
    ### For comparison, there is also a TrainLemmatizer that replicates the
    ###    original Latin lemmatizer from cltk.stem
    """

    models_path = os.path.expanduser('~/cltk_data/latin/model/latin_models_cltk/lemmata/backoff')

    def __init__(self, train=None, seed=3, verbose=False):
        self.models_path = BackoffLatinLemmatizer.models_path

        missing_models_message = "BackoffLatinLemmatizer requires the ```latin_models_cltk``` to be in cltk_data. Please load this corpus."

        try:
            self.train =  open_pickle(os.path.join(self.models_path, 'latin_pos_lemmatized_sents.pickle'))
            self.LATIN_OLD_MODEL =  open_pickle(os.path.join(self.models_path, 'latin_lemmata_cltk.pickle'))
            self.LATIN_MODEL =  open_pickle(os.path.join(self.models_path, 'latin_model.pickle'))
        except FileNotFoundError as err:
            raise type(err)(missing_models_message)

        self.latin_sub_patterns = latin_sub_patterns # Move to latin_models_cltk
        self.latin_verb_patterns = latin_verb_patterns # Move to latin_models_cltk
        # self.latin_pps = latin_pps # Move to latin_models_cltk

        self.seed = seed
        self.VERBOSE=verbose

        def _randomize_data(train, seed):
            import random
            random.seed(seed)
            random.shuffle(train)
            pos_train_sents = train[:4000]
            lem_train_sents = [[(item[0], item[1]) for item in sent] for sent in train]
            train_sents = lem_train_sents[:4000]
            test_sents = lem_train_sents[4000:5000]

            return pos_train_sents, train_sents, test_sents

        self.pos_train_sents, self.train_sents, self.test_sents = _randomize_data(self.train, self.seed)
        self._define_lemmatizer()


    def _define_lemmatizer(self):
        # Suggested backoff chain--should be tested for optimal order
        self.backoff0 = None
        self.backoff1 = IdentityLemmatizer(verbose=self.VERBOSE)
        self.backoff2 = DictLemmatizer(lemmas=self.LATIN_OLD_MODEL, source='Morpheus Lemmas', backoff=self.backoff1, verbose=self.VERBOSE)
        self.backoff3 = RegexpLemmatizer(self.latin_sub_patterns, source='CLTK Latin Regex Patterns', backoff=self.backoff2, verbose=self.VERBOSE)
        self.backoff4 = UnigramLemmatizer(self.train_sents, source='CLTK Sentence Training Data', backoff=self.backoff3, verbose=self.VERBOSE)
        self.backoff5 = DictLemmatizer(lemmas=self.LATIN_MODEL, source='Latin Model', backoff=self.backoff4, verbose=self.VERBOSE)
        self.lemmatizer = self.backoff5

    def lemmatize(self, tokens):
        lemmas = self.lemmatizer.lemmatize(tokens)
        return lemmas

    def evaluate(self):

        if self.VERBOSE:
            raise AssertionError("evaluate() method only works when verbose=False")
        return self.lemmatizer.evaluate(self.test_sents)

    def __repr__(self):
        return f'<BackoffLatinLemmatizer v0.2>'


if __name__ == '__main__':

    from pprint import pprint
    l1 = DefaultLemmatizer('UNK', verbose=True)
    l2 = DictLemmatizer(lemmas={'arma': 'arma', 'uirum': 'uir'}, backoff=l1, verbose=True)
    l3 = UnigramLemmatizer(train=[[('cano', 'cano'), ('.', 'punc')],], backoff=l2, verbose=True)
    l4 = RegexpLemmatizer(regexps=[('(.)tat(is|i|em|e|es|um|ibus)$', r'\1tas'),], backoff=l3, verbose=True)
    lemmas = l4.lemmatize('arma uirum -que cano nobilitatis .'.split())
    pprint(lemmas)

    # [('arma', 'arma', <UnigramLemmatizer: [[('res', 'res'), ...], ...]>),
    # ('uirum', 'uir', <UnigramLemmatizer: [[('res', 'res'), ...], ...]>),
    # ('-que', '-que', <DictLemmatizer: {'!': 'punc', ...}>),
    # ('cano', 'cano', <DictLemmatizer: {'-nam': 'nam', ...}>),
    # ('nobilitatis',
    # 'nobilitas',
    # <RegexpLemmatizer: [('(bil)(is|i|e...es|ium|ibus)$', '\\1is'), ...]>),
    # ('.', 'punc', <DictLemmatizer: {'!': 'punc', ...}>)]

    print('\n')

    bll = BackoffLatinLemmatizer(seed=5, verbose=False)
    lemmas = bll.lemmatize('arma uirum -que cano nobilitatis .'.split())
    pprint(lemmas)

    # [('arma', 'arma', <UnigramLemmatizer: CLTK Sentence Training Data>),
    # ('uirum', 'uir', <UnigramLemmatizer: CLTK Sentence Training Data>),
    # ('-que', '-que', <DictLemmatizer: Latin Model>),
    # ('cano', 'cano', <DictLemmatizer: Morpheus Lemmas>),
    # ('nobilitatis', 'nobilitas', <RegexpLemmatizer: CLTK Latin Regex Patterns>),
    # ('.', 'punc', <DictLemmatizer: Latin Model>)]

    rn = RomanNumeralLemmatizer()
    print(rn.lemmatize(['MMCI']))
