"""Module for lemmatizing historical languages
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

import re

from nltk.tag.sequential import SequentialBackoffTagger, DefaultTagger, UnigramTagger, RegexpTagger
from nltk.probability import ConditionalFreqDist

from cltk.lemmatize.latin.latin import latin_sub_patterns, latin_verb_patterns, latin_pps, rn_patterns


class DefaultLemmatizer(DefaultTagger):
    """"""
    def __init__(self, lemma=None):
        """Setup for DefaultLemmatizer().

        :param lemma: String with default lemma to be assigned for all tokens;
        set to None if no parameter is assigned.
        """
        self._lemma = lemma
        DefaultTagger.__init__(self, self._lemma)


    def lemmatize(self, tokens):
        return self.tag(tokens)


class IdentityLemmatizer(SequentialBackoffTagger):
    """"""
    def __init__(self, backoff=None):
        """Setup for IdentityLemmatizer()."""
        SequentialBackoffTagger.__init__(self, backoff)


    def choose_tag(self, tokens, index, history):
        """Returns the given token as the lemma.

        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized
        :return: String, spec. the token found at the current index.
        """
        return tokens[index]


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


class UnigramLemmatizer(UnigramTagger):
    """Setup for UnigramLemmatizer()"""
    def __init__(self, train=None, model=None, backoff=None, cutoff=0):
        """"""
        UnigramTagger.__init__(self, train, model, backoff, cutoff)

    # May be a problem with the _train function; see below, overridden in
    # TrainLemmatizer

    def lemmatize(self, tokens):
        return self.tag(tokens)


class DictionaryLemmatizer(UnigramTagger):
    """Setup for UnigramLemmatizer()"""
    def __init__(self, train=None, model=None, backoff=None, cutoff=0):
        """"""
        UnigramTagger.__init__(self, train=None, model=model, backoff=backoff, cutoff=cutoff)

    def lemmatize(self, tokens):
        return self.tag(tokens)


class TrainLemmatizer(UnigramTagger):
    """Setup for UnigramLemmatizer()"""
    def __init__(self, train=None, model=None, backoff=None, cutoff=0):
        """"""
        UnigramTagger.__init__(self, train=train, model=None, backoff=backoff, cutoff=cutoff)

    # Had to include the _train method because of some unusual behavior in
    # ```token``` variable as it went through the backoff chain; specifically
    # it seems around the ```useful_contexts``` part of the method. Below
    # is a slightly modified version of the NLTK code
    def _train(self, tagged_corpus, cutoff=0, verbose=False):
        """
        Initialize this ContextTagger's ``_context_to_tag`` table
        based on the given training data.  In particular, for each
        context ``c`` in the training data, set
        ``_context_to_tag[c]`` to the most frequent tag for that
        context.  However, exclude any contexts that are already
        tagged perfectly by the backoff tagger(s).

        The old value of ``self._context_to_tag`` (if any) is discarded.

        :param tagged_corpus: A tagged corpus.  Each item should be
            a list of (word, tag tuples.
        :param cutoff: If the most likely tag for a context occurs
            fewer than cutoff times, then exclude it from the
            context-to-tag table for the new tagger.
        """
        token_count = hit_count = 0

        # A context is considered 'useful' if it's not already tagged
        # perfectly by the backoff tagger.
        useful_contexts = set()
        # Count how many times each tag occurs in each context.
        fd = ConditionalFreqDist()
        for sentence in tagged_corpus:
            tokens_, tags = zip(*sentence)
            for index, (token, tag) in enumerate(sentence):
                # Record the event.
                token_count += 1
                context = self.context(tokens_, index, tags[:index])
                if context is None:
                    continue
                fd[context][tag] += 1

                # THE IF STATEMENT HERE HAD TO BE REMOVED—OVERLOADING TOKENS VARIABLE???!!!
                # STILL NOT EXACTLY SURE WHY???
                useful_contexts.add(context)

        # Build the context_to_tag table -- for each context, figure
        # out what the most likely tag is.  Only include contexts that
        # we've seen at least `cutoff` times.
        for context in useful_contexts:
            best_tag = fd[context].max()

            hits = fd[context][best_tag]
            if hits > cutoff:
                self._context_to_tag[context] = best_tag
                hit_count += hits

    def lemmatize(self, tokens):
        return self.tag(tokens)


class RegexpLemmatizer(RegexpTagger):
    """"""

    def __init__(self, regexps=None, backoff=None):
        """Setup for RegexpLemmatizer()

        :param regexps: List of tuples of form (PATTERN, REPLACEMENT)
        :param backoff: Next lemmatizer in backoff chain.
        """
        RegexpTagger.__init__(self, regexps, backoff)
        self._regexs = regexps


    def choose_tag(self, tokens, index, history):
        """Use regular expressions for rules-based lemmatizing based on word endings;
        tokens are matched for patterns with the base kept as a group; an word ending
        replacement is added to the (base) group.
        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized
        :return: Str with concatenated lemma
        """
        for pattern, replace in self._regexs:
            if re.search(pattern, tokens[index]):
                return re.sub(pattern, replace, tokens[index])
                break # pragma: no cover


    def lemmatize(self, tokens):
        return self.tag(tokens)
