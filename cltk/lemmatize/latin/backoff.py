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

    def __init__(self, backoff, VERBOSE=False):
        """
        Setup for SequentialBackoffLemmatizer
        :param backoff: Next lemmatizer in backoff chain
        :type VERBOSE: bool
        :param VERBOSE: Flag to include which lemmatizer assigned in
            a given tag in the return tuple
        """
        SequentialBackoffTagger.__init__(self, backoff=None)

        # Setup backoff chain
        if backoff is None:
            self._taggers = [self]
        else:
            self._taggers = [self] + backoff._taggers

        self.VERBOSE = VERBOSE
        self.repr = reprlib.Repr()
        self.repr.maxlist = 1
        self.repr.maxdict = 1


    def tag(self, tokens):
        # Docs (mostly) inherited from TaggerI
        # Cf. https://www.nltk.org/_modules/nltk/tag/api.html#TaggerI.tag
        #
        # Two tweaks:
        # 1. Properly handle 'verbose' listing of current tagger in
        # the case of None (i.e. ``if tag: etc.``)
        # 2. Keep track of taggers and change return depending on
        # 'verbose' flag
        tags = []
        taggers = []
        for i in range(len(tokens)):
            tag, tagger = self.tag_one(tokens, i, tags)
            tags.append(tag)
            if tag:
                taggers.append(tagger)
            else:
                taggers.append(None)

        if self.VERBOSE:
            return(list(zip(tokens, tags, taggers)))
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
    Lemmatizer that assigns the same lemma to every token.

        >>> from cltk.lemmatize.latin.backoff import DefaultLemmatizer
        >>> default_lemmatizer = DefaultLemmatizer('UNK')
        >>> list(default_lemmatizer.lemmatize('arma virumque cano'.split()))
        [('arma', 'UNK'), ('virumque', 'UNK'), ('cano', 'UNK')]

    Useful as the final tagger in a chain, e.g. to assign 'UNK' to all
    remaining unlemmatized tokens.

    :type lemma: str
    :param lemma: Lemma to assign to each token
    """
    def __init__(self, lemma=None, backoff=None, VERBOSE=False):
        self.lemma = lemma
        SequentialBackoffLemmatizer.__init__(self, backoff=None, VERBOSE=VERBOSE)


    def choose_tag(self, tokens, index, history):
        return self.lemma


    def __repr__(self):
        return f'<DefaultLemmatizer: lemma={self.lemma}>'


class IdentityLemmatizer(SequentialBackoffLemmatizer):
    """
    Lemmatizer that returns a given token as its lemma.

        >>> from cltk.lemmatize.latin.backoff import IdentityLemmatizer
        >>> identity_lemmatizer = IdentityLemmatizer()
        >>> list(identity_lemmatizer.lemmatize('arma virumque cano'.split()))
        [('arma', 'arma'), ('virumque', 'virumque'), ('cano', 'cano')]

    Like DefaultLemmatizer, useful as the final tagger in a chain,
    e.g. to assign a possible form to all remaining unlemmatized
    tokens, increasing the chance of a successful match.
    """

    def __init__(self, backoff=None, VERBOSE=False):
        SequentialBackoffLemmatizer.__init__(self, backoff=None, VERBOSE=VERBOSE)


    def choose_tag(self, tokens, index, history):
        return tokens[index]


    def __repr__(self):
        return f'<IdentityLemmatizer>'

# REFACTORED AS DictLemmatizer below
# class TrainLemmatizer(SequentialBackoffLemmatizer):
#     """Standalone version of 'model' function found in UnigramTagger; by
#     defining as its own class, it is clearer that this lemmatizer is
#     based on dictionary lookup and does not use training data."""
#
#     def __init__(self, model, backoff=None):
#         """Setup for TrainLemmatizer().
#
#         :param model: Dictionary with form {TOKEN: LEMMA}
#         :param backoff: Next lemmatizer in backoff chain.
#         """
#         SequentialBackoffLemmatizer.__init__(self, backoff)
#         self.model = model
#
#
#     def choose_lemma(self, tokens, index, history):
#         """Returns the given token as the lemma.
#
#         :param tokens: List of tokens to be lemmatized
#         :param index: Int with current token
#         :param history: List with tokens that have already been lemmatized; NOT USED
#         :return: String, spec. the dictionary value found with token as key.
#         """
#         keys = self.model.keys()
#         if tokens[index] in keys:
#             return self.model[tokens[index]]


class DictLemmatizer(SequentialBackoffLemmatizer):
    """Standalone version of 'model' function found in UnigramTagger; by
    defining as its own class, it is clearer that this lemmatizer is
    based on dictionary lookup and does not use training data."""

    def __init__(self, lemmas, backoff=None, VERBOSE=False):
        """
        Setup for DictLemmatizer().
        :type lemmas: dict
        :param lemmas: Dictionary with form {TOKEN: LEMMA} to be used
            as foor 'lookup'-style lemmatization
        :param backoff: Next lemmatizer in backoff chain.
        """
        SequentialBackoffLemmatizer.__init__(self, backoff, VERBOSE=VERBOSE)
        self.lemmas = lemmas


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
        return f'<DictLemmatizer: {self.repr.repr(self.lemmas)}>'


class UnigramLemmatizer(SequentialBackoffLemmatizer, UnigramTagger):
    """
    Standalone version of 'train' function found in UnigramTagger; by
    defining as its own class, it is clearer that this lemmatizer is
    based on training data and not on dictionary.
    """

    def __init__(self, train=None, model=None, backoff=None, cutoff=0, VERBOSE=False):
        """
        Setup for UnigramLemmatizer()
        """
        SequentialBackoffLemmatizer.__init__(self, backoff=None, VERBOSE=VERBOSE)
        UnigramTagger.__init__(self, train, model, backoff, cutoff)
        self.train = train


    def __repr__(self):
        return f'<UnigramLemmatizer: {self.repr.repr(self.train)}>'


class RegexpLemmatizer(SequentialBackoffLemmatizer):
    """"""

    def __init__(self, regexps=None, backoff=None, VERBOSE=False):
        """Setup for RegexpLemmatizer()
        :type regexps: list
        :param regexps: List of tuples of form (PATTERN, REPLACEMENT)
        :param backoff: Next lemmatizer in backoff chain.
        """
        SequentialBackoffLemmatizer.__init__(self, backoff, VERBOSE=VERBOSE)
        self._regexs = regexps


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
        return f'<RegexpLemmatizer: {self.repr.repr(self._regexs)}>'


class PPLemmatizer(RegexpLemmatizer):
    """Customization of the RegexpLemmatizer for Latin. The RegexpLemmatizer is
        used as a stemmer; the stem is then applied to a dictionary lookup of
        principal parts."""
    def __init__(self, regexps=None, pps=None, backoff=None):
        """Setup PPLemmatizer().

        :param regexps: List of tuples of form (PATTERN, INT) where INT is
        the principal part number needed to lookup the correct stem.
        :param backoff: Next lemmatizer in backoff chain.
        """
        RegexpLemmatizer.__init__(self, regexps, backoff)
        # Note different compile to make use of principal parts dictionary structure; also, note
        # that the PP dictionary has been set up so that principal parts match their traditional
        # numbering, i.e. present stem is indexed as 1. The 0 index is used for the lemma.
        self._regexs = latin_verb_patterns
        self.pps = latin_pps


    def choose_tag(self, tokens, index, history):
        """Use regular expressions for rules-based lemmatizing based on
        principal parts stems. Tokens are matched for patterns with
        the ending kept as a group; the stem is looked up in a dictionary
        by PP number (see above) and ending is discarded.

        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized
        :return: Str with index[0] from the dictionary value, see above about '0 index'
        """
        for regexp in self._regexs:
            m = re.match(regexp[0], tokens[index])
            if m:
                root = m.group(1)
                match = [lemma for (lemma, pp) in self.pps.items() if root == pp[regexp[1]]]
                if not match:
                    pass
                else:
                    return match[0] # Lemma is indexed at zero in PP dictionary


class RomanNumeralLemmatizer(RegexpLemmatizer):
    """"""
    def __init__(self, regexps=rn_patterns, default=None, backoff=None):
        """RomanNumeralLemmatizer"""
        RegexpLemmatizer.__init__(self, regexps, backoff)
        self._regexs = [(re.compile(regexp), pattern,) for regexp, pattern in regexps]
        self.default = default

    def choose_lemma(self, tokens, index, history):
        """Test case for customized rules-based improvements to lemmatizer using regex; differs
        from base RegexpLemmatizer in that it returns the given pattern without stemming,
        concatenating, etc.
        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized
        :return: Str with replacement from pattern
        """
        for pattern, replace in self._regexs:
            if re.search(pattern, tokens[index]):
                if self.default:
                    return self.default
                else:
                    return replace
                break # pragma: no cover

# EXPERIMENTAL—NEEDS REVIEW
# class ContextPOSLemmatizer(ContextLemmatizer):
#     """Lemmatizer that combines context with POS-tagging based on
#         training data. Subclasses define context.
#
#         The code for _train closely follows ContextTagger in
#         https://github.com/nltk/nltk/blob/develop/nltk/tag/sequential.py
#
#         This lemmatizer is included here as proof of concept that
#         lemma disambiguation can be made based on the pattern:
#         LEMMA & POS of following word.
#
#         Should be rewritten to give more flexibility to the kinds
#         of context that a free word order language demand. I.e. to
#         study patterns such as:
#         POS of preceding word & LEMMA
#         LEMMA & POS of following two words
#         LEMMA & POS of n-skipgrams
#         etc.
#         """
#
#     def __init__(self, context_to_lemmatize, include=None, backoff=None):
#         """Setup ContextPOSLemmatizer().
#
#         :param context_to_lemmatize: List of tuples of the form (TOKEN, LEMMA);
#         this should be 'gold standard' data that can be used to train on a
#         given context, e.g. unigrams, bigrams, etc.
#         :param include: List of tokens to include, all other tokens return None
#         from choose_lemma--runs VERY SLOW if no list is given as a parameter
#         since every token gets POS-tagged. Only tested so far on 'cum'
#         --also, test data only distinguishes 'cum1'/'cum2'. Further
#         testing should be done with ambiguous lemmas using Morpheus numbers.
#         :param backoff: Next lemmatizer in backoff chain.
#         :param include: List of tokens to consider
#         """
#         # SequentialBackoffLemmatizer.__init__(self, backoff)
#         ContextLemmatizer.__init__(self, context_to_lemmatize, backoff)
#         self.include = include
#         self._context_to_tag = (context_to_lemmatize if context_to_lemmatize else {})
#
#     def _get_pos_tags(self, tokens):
#         """Iterate through list of tokens and use POS tagger to build
#         a corresponding list of tags.
#
#         :param tokens: List of tokens to be POS-tagged
#         :return: List with POS-tag for each token
#         """
#         # Import (and define tagger) with other imports?
#         from cltk.tag.pos import POSTag
#         tagger = POSTag('latin')
#         tokens = " ".join(tokens)
#         tags = tagger.tag_ngram_123_backoff(tokens)
#         tags = [tag[1][0].lower() if tag[1] else tag[1] for tag in tags]
#         return tags
#
#     def choose_lemma(self, tokens, index, history):
#         """Choose lemma based on POS-tag defined by context.
#
#         :param tokens: List of tokens to be lemmatized
#         :param index: Int with current token
#         :param history: List with POS-tags of tokens that have already
#         been lemmatized.
#         :return: String with suggested lemma
#         """
#         if self.include:
#             if tokens[index] not in self.include:
#                 return None
#         history = self._get_pos_tags(tokens)
#         context = self.context(tokens, index, history)
#         suggested_lemma = self._context_to_tag.get(context)
#         return suggested_lemma
#
#     def _train(self, lemma_pos_corpus, cutoff=0):
#         """Override method for _train from ContextTagger in
#         nltk.tag.sequential. Original _train method expects
#         tagged corpus of form (TOKEN, LEMMA); this expects in
#         addition POS-tagging information.
#
#         :param lemma_pos_corpus: List of tuples of form (TOKEN, LEMMA, POSTAG)
#         :param cutoff: Int with minimum number of matches to choose lemma
#         """
#         token_count = hit_count = 0
#
#         # A context is considered 'useful' if it's not already lemmatized
#         # perfectly by the backoff lemmatizer.
#         useful_contexts = set()
#
#         # Count how many times each tag occurs in each context.
#         fd = ConditionalFreqDist()
#         for sentence in lemma_pos_corpus:
#             tokens, lemmas, poss = zip(*sentence)
#             for index, (token, lemma, pos) in enumerate(sentence):
#                 # Record the event.
#                 token_count += 1
#
#                 context = self.context(tokens, index, poss)
#                 if context is None: continue
#                 fd[context][lemma] += 1
#
#                 # If the backoff got it wrong, this context is useful:
#                 if (self.backoff is None or lemma != self.backoff.tag_one(tokens, index, lemmas[:index])):  # pylint: disable=line-too-long
#                     useful_contexts.add(context)
#
#         # Build the context_to_lemmatize table -- for each context, figure
#         # out what the most likely lemma is. Only include contexts that
#         # we've seen at least `cutoff` times.
#         for context in useful_contexts:
#             best_lemma = fd[context].max()
#             hits = fd[context][best_lemma]
#             if hits > cutoff:
#                 self._context_to_tag[context] = best_lemma
#                 hit_count += hits
#
#
# class NgramPOSLemmatizer(ContextPOSLemmatizer):
#     """"""
#     def __init__(self, n, train=None, model=None, include=None,
#                  backoff=None, cutoff=0):
#         """Setup for NgramPOSLemmatizer
#
#         :param n: Int with length of 'n'-gram
#         :param train: List of tuples of the form (TOKEN, LEMMA, POS)
#         :param model: Dict; DEPRECATED
#         :param include: List of tokens to consider
#         :param backoff: Next lemmatizer in backoff chain.
#         :param cutoff: Int with minimum number of matches to choose lemma
#         """
#         self._n = n
#         self._check_params(train, model)
#         ContextPOSLemmatizer.__init__(self, model, include, backoff)
#
#         if train:
#             self._train(train, cutoff)
#
#     def context(self, tokens, index, history):
#         """Redefines context with look-ahead of length n (not look behind
#         as in original method).
#
#         :param tokens: List of tokens to be lemmatized
#         :param index: Int with current token
#         :param history: List with tokens that have already been
#         tagged/lemmatized
#         :return: Tuple of the form (TOKEN, (CONTEXT)); CONTEXT will
#         depend on ngram value, e.g. for bigram ('cum', ('n',)) but
#         for trigram ('cum', ('n', 'n', ))
#         """
#         lemma_context = tuple(history[index + 1: index + self._n])
#         return tokens[index], lemma_context
#
#
# class BigramPOSLemmatizer(NgramPOSLemmatizer):
#     """"""
#     def __init__(self, train=None, model=None, include=None,
#                  backoff=None, cutoff=0):
#         """Setup for BigramPOSLemmatizer()"""
#         NgramPOSLemmatizer.__init__(self, 2, train, model,
#                                     include, backoff, cutoff)


class BackoffLatinLemmatizer(object):
    """Suggested backoff chain; includes at least on of each
    type of major sequential backoff class from backoff.py

    ### Putting it all together
    ### BETA Version of the Backoff Lemmatizer AKA BackoffLatinLemmatizer
    ### For comparison, there is also a TrainLemmatizer that replicates the
    ###    original Latin lemmatizer from cltk.stem
    """
    def __init__(self, train, seed=3):
        self.train = train
        self.seed = seed

        rel_path = os.path.join('~/cltk_data/latin/model/latin_models_cltk/lemmata/backoff')
        path = os.path.expanduser(rel_path)

        # Check for presence of LATIN_OLD_MODEL
        file = 'latin_lemmata_cltk.pickle'

        old_model_path = os.path.join(path, file)
        if os.path.isfile(old_model_path):
            self.LATIN_OLD_MODEL = open_pickle(old_model_path)
        else:
            self.LATIN_OLD_MODEL = {}
            print('The file %s is not available in cltk_data' % file)

        # Check for presence of LATIN_MODEL
        file = 'latin_model.pickle'

        model_path = os.path.join(path, file)
        if os.path.isfile(model_path):
            self.LATIN_MODEL = open_pickle(model_path)
        else:
            self.LATIN_MODEL = {}
            print('The file %s is not available in cltk_data' % file)

        # Check for presence of misc_patterns
        self.latin_sub_patterns = latin_sub_patterns

        # Check for presence of verb_patterns
        self.latin_verb_patterns = latin_verb_patterns

        # Check for presence of latin_pps
        self.latin_pps = latin_pps

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
        self.backoff1 = IdentityLemmatizer()
        self.backoff2 = DictLemmatizer(lemmas=self.LATIN_OLD_MODEL, backoff=self.backoff1)
        self.backoff3 = PPLemmatizer(regexps=self.latin_verb_patterns, pps=self.latin_pps, backoff=self.backoff2)
        self.backoff4 = RegexpLemmatizer(self.latin_sub_patterns, backoff=self.backoff2)
        self.backoff5 = UnigramLemmatizer(self.train_sents, backoff=self.backoff3)
        self.backoff6 = DictLemmatizer(lemmas=self.LATIN_MODEL, backoff=self.backoff5)
        self.lemmatizer = self.backoff6

    def lemmatize(self, tokens):
        lemmas = self.lemmatizer.lemmatize(tokens)
        return lemmas

    def evaluate(self):
        return lemmatizer.evaluate(self.test_sents)

    def __repr__(self):
        return f'<BackoffLatinLemmatizer>'

if __name__ == '__main__':
    pass
    # # Set up training sentences
    # rel_path = os.path.join('~/cltk_data/latin/model/latin_models_cltk/lemmata/backoff')
    # path = os.path.expanduser(rel_path)
    #
    # # Check for presence of latin_pos_lemmatized_sents
    # file = 'latin_pos_lemmatized_sents.pickle'
    #
    # latin_pos_lemmatized_sents_path = os.path.join(path, file)
    # if os.path.isfile(latin_pos_lemmatized_sents_path):
    #    latin_pos_lemmatized_sents = open_pickle(latin_pos_lemmatized_sents_path)
    # else:
    #    latin_pos_lemmatized_sents = []
    #    print('The file %s is not available in cltk_data' % file)
    #
    # l = BackoffLatinLemmatizer(latin_pos_lemmatized_sents)
    #
    # import pickle
    # pickle.dump(l, open( "backofflatinlemmatizer.p", "wb" ) )
