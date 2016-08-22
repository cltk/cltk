"""Primary module for lemmatizing Latin.

TODO: Get rid of the wildcard "*" import
"""

# from pprint import pprint

# from nltk.tag.api import TaggerI
from nltk.tag.sequential import *

from cltk.lemmatize.latin.model import LATIN_MODEL
from cltk.lemmatize.latin.old_model import LATIN_OLD_MODEL
from cltk.lemmatize.latin.regexp_patterns import latin_pps
from cltk.lemmatize.latin.regexp_patterns import latin_verb_patterns
from cltk.lemmatize.latin.regexp_patterns import latin_misc_patterns
from cltk.lemmatize.latin.regexp_patterns import rn_patterns
from cltk.lemmatize.latin.lemmatized_sentences import latin_pos_lemmatized_sents

__author__ = 'Patrick J. Burns <patrick@diyclassics.org>'
__license__ = 'MIT License. See LICENSE.'


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


class IdentityLemmatizer(SequentialBackoffLemmatizer):
    """"""
    def __init__(self, backoff=None):
        """Setup for IdentityLemmatizer()."""
        SequentialBackoffLemmatizer.__init__(self, backoff)

    def lemmatize(self, tokens):
        """
        Custom lemmatize method for working with identity. No need to
        call tagger because token is return as lemma.
        :param tokens: List of tokens to be lemmatized
        :return: Tuple of the form (TOKEN, LEMMA)

        Note: "enumerate" may be better way of handling this loop in general;
        compare "range(len(tokens))" in nltk.tag.sequential.
        """
        lemmas = []
        for i in enumerate(tokens):
            lemmas.append(i[1])
        return list(zip(tokens, lemmas))

    def choose_lemma(self, tokens, index, history):
        """Returns the given token as the lemma.

        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized
        :return: String, spec. the token found at the current index.
        """
        _lemma = tokens[index]
        return _lemma


class ModelLemmatizer(SequentialBackoffLemmatizer):
    """Standalone version of 'model' function found in UnigramTagger; by
    defining as its own class, it is clearer that this lemmatizer is
    based on dictionary lookup and does not use training data."""

    def __init__(self, model, backoff=None):
        """Setup for ModelLemmatizer().

        :param model: Dictionary with form {TOKEN: LEMMA}
        :param backoff: Next lemmatizer in backoff chain.
        """
        SequentialBackoffLemmatizer.__init__(self, backoff)
        self.model = model


    def choose_lemma(self, tokens, index, history):
        """Returns the given token as the lemma.

        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized; NOT USED
        :return: String, spec. the dictionary value found with token as key.
        """
        keys = self.model.keys()
        if tokens[index] in keys:
            return self.model[tokens[index]]


class ContextLemmatizer(SequentialBackoffLemmatizer, ContextTagger):
    """"""
    def __init__(self, context_to_lemmatize, backoff=None):
        """Setup for ContextLemmatizer().

        :param context_to_lemmatize: List of tuples of the form (TOKEN, LEMMA);
        this should be 'gold standard' data that can be used to train on a 
        given context, e.g. unigrams, bigrams, etc.
        :param backoff: Next lemmatizer in backoff chain.
        """
        SequentialBackoffLemmatizer.__init__(self, backoff)
        self._context_to_lemmatize = (context_to_lemmatize if context_to_lemmatize else {})
        ContextTagger.__init__(self, self._context_to_lemmatize, backoff)

    def choose_lemma(self, tokens, index, history):
        return ContextTagger.choose_tag(self, tokens, index, history)


class NgramLemmatizer(ContextLemmatizer, NgramTagger):
    """"""
    def __init__(self, n, train=None, model=None, backoff=None, cutoff=0):
        """Setup for NgramLemmatizer()

        :param n: Int with length of 'n'-gram
        :param train: List of tuples of the form (TOKEN, LEMMA)
        :param model: Dict; DEPRECATED, use ModelLemmatizer
        :param backoff: Next lemmatizer in backoff chain.
        :param cutoff: Int with minimum number of matches to choose lemma
        """
        self._n = n
        self._check_params(train, model)
        ContextLemmatizer.__init__(self, model, backoff)
        NgramTagger.__init__(self, self._n, train, model, backoff, cutoff)

        if train:
            # Refactor to remove model? Always train?
            self._train(train, cutoff)

    def context(self, tokens, index, history):
        """"""
        return NgramTagger.context(self, tokens, index, history)


class UnigramLemmatizer(NgramLemmatizer, UnigramTagger):
    """Setup for UnigramLemmatizer()"""
    def __init__(self, train=None, model=None, backoff=None, cutoff=0):
        """"""
        NgramLemmatizer.__init__(self, 1, train, model, backoff, cutoff) # Note 1 for unigram
        UnigramTagger.__init__(self, train, model, backoff, cutoff)


class RegexpLemmatizer(SequentialBackoffLemmatizer, RegexpTagger):
    """"""
    def __init__(self, regexps, backoff=None):
        """Setup for RegexpLemmatizer()

        :param regexps: List of tuples of form (PATTERN, REPLACEMENT)
        :param backoff: Next lemmatizer in backoff chain.
        """
        SequentialBackoffLemmatizer.__init__(self, backoff)
        RegexpTagger.__init__(self, regexps, backoff)

    def choose_lemma(self, tokens, index, history):
        """Use regular expressions for rules-based lemmatizing based on word endings;
        tokens are matched for patterns with the base kept as a group; an word ending
        replacement is added to the (base) group.
        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized
        :return: Str with concatenated lemma
        """
        for regexp, pattern in self._regexs:
            m = re.match(regexp, tokens[index])
            if m:
                return (m.group(1)) + pattern


class PPLemmatizer(RegexpLemmatizer):
    """Customization of the RegexpLemmatizer for Latin. The RegexpLemmatizer is
        used as a stemmer; the stem is then applied to a dictionary lookup of
        principal parts."""
    def __init__(self, regexps=latin_verb_patterns, backoff=None):
        """Setup PPLemmatizer().

        :param regexps: List of tuples of form (PATTERN, INT) where INT is
        the principal part number needed to lookup the correct stem.
        :param backoff: Next lemmatizer in backoff chain.
        """
        RegexpLemmatizer.__init__(self, regexps, backoff)
        # Note different compile to make use of principal parts dictionary structure; also, note
        # that the PP dictionary has been set up so that principal parts match their traditional
        # numbering, i.e. present stem is indexed as 1. The 0 index is used for the lemma.
        self._regexs = [(re.compile(regexp), num) for regexp, num in
                        regexps]

    def choose_lemma(self, tokens, index, history):
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
                match = [lemma for (lemma, pp) in latin_pps.items() if root == pp[regexp[1]]]
                if not match:
                    pass
                else:
                    return match[0] # Lemma is indexed at zero in PP dictionary


class RomanNumeralLemmatizer(RegexpLemmatizer):
    """"""
    def __init__(self, regexps=rn_patterns, backoff=None):
        """RomanNumeralLemmatizer"""
        RegexpLemmatizer.__init__(self, regexps, backoff)

    def choose_lemma(self, tokens, index, history):
        """Test case for customized rules-based improvements to lemmatizer using regex; differs
        from base RegexpLemmatizer in that it returns the given pattern without stemming,
        concatenating, etc.
        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized
        :return: Str with replacement from pattern
        """
        for regexp, pattern in self._regexs:
            m = re.match(regexp, tokens[index])
            if m:
                return pattern
        return None


class ContextPOSLemmatizer(ContextLemmatizer):
    """Lemmatizer that combines context with POS-tagging based on
        training data. Subclasses define context."""

    def __init__(self, context_to_lemmatize, include=None, backoff=None):
        """Setup ContextPOSLemmatizer().

        :param context_to_lemmatize: List of tuples of the form (TOKEN, LEMMA);
        this should be 'gold standard' data that can be used to train on a 
        given context, e.g. unigrams, bigrams, etc.
        :param include: List of tokens to include, all other tokens return None
        from choose_lemma--runs VERY SLOW if no list is given as a parameter
        since every token gets POS-tagged. Only tested so far on 'cum'
        --also, test data only distinguishes 'cum1'/'cum2'. Further 
        testing should be done with ambiguous lemmas using Morpheus numbers.
        :param backoff: Next lemmatizer in backoff chain.
        :param include: List of tokens to consider        
        """
        # SequentialBackoffLemmatizer.__init__(self, backoff)
        ContextLemmatizer.__init__(self, context_to_lemmatize, backoff)
        self.include = include
        self._context_to_tag = (context_to_lemmatize if context_to_lemmatize else {})

    def _get_pos_tags(self, tokens):
        """Iterate through list of tokens and use POS tagger to build
        a corresponding list of tags.

        :param tokens: List of tokens to be POS-tagged
        :return: List with POS-tag for each token
        """
        # Import (and define tagger) with other imports?    
        from cltk.tag.pos import POSTag
        tagger = POSTag('latin')
        tokens = " ".join(tokens)
        tags = tagger.tag_ngram_123_backoff(tokens)
        tags = [tag[1][0].lower() if tag[1] else tag[1] for tag in tags]
        return tags

    def choose_lemma(self, tokens, index, history):
        """Choose lemma based on POS-tag defined by context.

        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with POS-tags of tokens that have already
        been lemmatized.
        :return: String with suggested lemma
        """        
        if self.include:
            if tokens[index] not in self.include:
                return None
        history = self._get_pos_tags(tokens)
        context = self.context(tokens, index, history)
        suggested_lemma = self._context_to_tag.get(context)
        return suggested_lemma

    def _train(self, lemma_pos_corpus, cutoff=0):
        """Override method for _train from ContextTagger in
        nltk.tag.sequential. Original _train method expects
        tagged corpus of form (TOKEN, LEMMA); this expects in
        addition POS-tagging information.

        :param lemma_pos_corpus: List of tuples of form (TOKEN, LEMMA, POSTAG)
        :param cutoff: Int with minimum number of matches to choose lemma
        """
        token_count = hit_count = 0

        # A context is considered 'useful' if it's not already lemmatized
        # perfectly by the backoff lemmatizer.
        useful_contexts = set()

        # Count how many times each tag occurs in each context.
        fd = ConditionalFreqDist()
        for sentence in lemma_pos_corpus:
            tokens, lemmas, poss = zip(*sentence)
            for index, (token, lemma, pos) in enumerate(sentence):
                # Record the event.
                token_count += 1

                context = self.context(tokens, index, poss)
                if context is None: continue
                fd[context][lemma] += 1

                # If the backoff got it wrong, this context is useful:
                if (self.backoff is None or lemma != self.backoff.tag_one(tokens, index, lemmas[:index])):  # pylint: disable=line-too-long
                    useful_contexts.add(context)

        # Build the context_to_lemmatize table -- for each context, figure
        # out what the most likely lemma is. Only include contexts that
        # we've seen at least `cutoff` times.
        for context in useful_contexts:
            best_lemma = fd[context].max()
            hits = fd[context][best_lemma]
            if hits > cutoff:
                self._context_to_tag[context] = best_lemma
                hit_count += hits


class NgramPOSLemmatizer(ContextPOSLemmatizer):
    """"""
    def __init__(self, n, train=None, model=None, include=None,
                 backoff=None, cutoff=0):
        """Setup for NgramPOSLemmatizer

        :param n: Int with length of 'n'-gram
        :param train: List of tuples of the form (TOKEN, LEMMA, POS)
        :param model: Dict; DEPRECATED
        :param include: List of tokens to consider
        :param backoff: Next lemmatizer in backoff chain.
        :param cutoff: Int with minimum number of matches to choose lemma
        """
        self._n = n
        self._check_params(train, model)
        ContextPOSLemmatizer.__init__(self, model, include, backoff)

        if train:
            self._train(train, cutoff)

    def context(self, tokens, index, history):
        """Redefines context with look-ahead of length n (not look behind
        as in original method).

        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been
        tagged/lemmatized
        :return: Tuple of the form (TOKEN, (CONTEXT)); CONTEXT will
        depend on ngram value, e.g. for bigram ('cum', ('n',)) but
        for trigram ('cum', ('n', 'n', ))
        """
        lemma_context = tuple(history[index + 1: index + self._n])
        return tokens[index], lemma_context


class BigramPOSLemmatizer(NgramPOSLemmatizer):
    """"""
    def __init__(self, train=None, model=None, include=None,
                 backoff=None, cutoff=0):
        """Setup for BigramPOSLemmatizer()"""
        NgramPOSLemmatizer.__init__(self, 2, train, model,
                                    include, backoff, cutoff)


class TrigramPOSLemmatizer(NgramPOSLemmatizer):
    """"""
    def __init__(self, train=None, model=None, include=None,
                 backoff=None, cutoff=0):
        """Setup for TrigramPOSLemmatizer()"""
        NgramPOSLemmatizer.__init__(self, 3, train, model, include,
                                    backoff, cutoff)


class LazyLatinLemmatizer(object):
    """Suggested backoff chain; includes at least on of each
    type of major sequential backoff class from backoff.py

    ### Putting it all together
    ### BETA Version of the Backoff Lemmatizer AKA LazyLatinLemmatizer
    ### For comparison, there is also a ModelLemmatizer that replicates the
    ###    original Latin lemmatizer from cltk.stem
    """
    def __init__(self, train):
        self.train = train

        def _randomize_data(train):
            import random
            random.shuffle(train)
            pos_train_sents = train[:4000]
            lem_train_sents = [[(item[0], item[1]) for item in sent] for sent in train]
            train_sents = lem_train_sents[:4000]
            test_sents = lem_train_sents[4000:5000]

            return pos_train_sents, train_sents, test_sents

        self.pos_train_sents, self.train_sents, self.test_sents = _randomize_data(self.train)

    def _define_lemmatizer(self):
        backoff0 = None
        backoff1 = IdentityLemmatizer()
        backoff2 = ModelLemmatizer(model=LATIN_OLD_MODEL, backoff=backoff1)
        backoff3 = PPLemmatizer(backoff=backoff2)                 
        backoff4 = UnigramLemmatizer(self.train_sents, backoff=backoff3)
        backoff5 = RegexpLemmatizer(latin_misc_patterns, backoff=backoff4)
        backoff6 = ModelLemmatizer(model=LATIN_MODEL, backoff=backoff5)
        backoff7 = BigramPOSLemmatizer(self.pos_train_sents, include=['cum'], backoff=backoff6)
        lemmatizer = backoff7
        return lemmatizer

    def lemmatize(self, tokens):
        lemmatizer = self._define_lemmatizer()
        lemmas = lemmatizer.lemmatize(tokens)
        return lemmas

    def evaluate(self):
        lemmatizer = self._define_lemmatizer()
        #lemmatizer = ModelLemmatizer(model=self.model)
        return lemmatizer.evaluate(self.test_sents)


class OriginalLatinLemmatizer(object):
    """Dictionary matching on the old LEMMATA model."""
    def __init__(self, train):
        """Setup for OriginalLatinLemmatizer()"""
        self.model = LATIN_OLD_MODEL
        self.train = train

        def _randomize_data(train):
            import random
            random.shuffle(train)
            pos_train_sents = train[:4000]
            lem_train_sents = [[(item[0], item[1]) for item in sent] for sent in train]
            train_sents = lem_train_sents[:4000]
            test_sents = lem_train_sents[4000:5000]

            return pos_train_sents, train_sents, test_sents

        self.pos_train_sents, self.train_sents, self.test_sents = _randomize_data(self.train)

    def _define_lemmatizer(self):
        lemmatizer = ModelLemmatizer(model=self.model)
        return lemmatizer

    def lemmatize(self, tokens):
        lemmatizer = self._define_lemmatizer()
        lemmas = lemmatizer.lemmatize(tokens)
        return lemmas

    def evaluate(self):
        lemmatizer = self._define_lemmatizer()
        #lemmatizer = ModelLemmatizer(model=self.model)
        return lemmatizer.evaluate(self.test_sents)


if __name__ == "__main__":
    RUN = 10
    ACCURACIES = []

    for I in range(RUN):
        LEMMATIZER = LazyLatinLemmatizer(latin_pos_lemmatized_sents)
        # lemmatizer = OriginalLatinLemmatizer(latin_pos_lemmatized_sents)
        ACC = LEMMATIZER.evaluate()
        ACCURACIES.append(ACC)
        print('{:.2%}'.format(ACC))

    print('\nTOTAL (Run %d) times' % RUN)
    print('{:.2%}'.format(sum(ACCURACIES) / RUN))
