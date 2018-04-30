"""Module for lemmatizing historical languages
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

import re

from nltk.tag.sequential import SequentialBackoffTagger, DefaultTagger, UnigramTagger, RegexpTagger

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
                