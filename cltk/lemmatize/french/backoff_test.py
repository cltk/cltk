#encoding :utf-8

import os
import re

from nltk.probability import ConditionalFreqDist
from nltk.tag.api import TaggerI
from nltk.tag.sequential import SequentialBackoffTagger, ContextTagger, DefaultTagger, NgramTagger, UnigramTagger, RegexpTagger
from cltk.tokenize.word import WordTokenizer
from cltk.utils.file_operations import open_pickle
##from cltk.lemmatize.french.lex import entries
from cltk.lemmatize.french.french import estre_replace, avoir_replace, first_conj_rules, i_type_rules, u_type_rules, regime_rules, plural_rules, misc_rules, masc_to_fem_rules, determiner_rules, reduction_rules


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

    def __init__(self, model, backoff=None):
        """Setup for TrainLemmatizer().

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
        for lemma, entry in entries:
            if tokens == lemma:
                return (tokens, lemma)

class RegexpLemmatizer(SequentialBackoffLemmatizer, RegexpTagger):
    """"""

    def __init__(self, regexps=None, backoff=None):
        """Setup for RegexpLemmatizer()

        :param regexps: List of tuples of form (PATTERN, REPLACEMENT)
        :param backoff: Next lemmatizer in backoff chain.
        """
        SequentialBackoffLemmatizer.__init__(self, backoff)
        RegexpTagger.__init__(self, regexps, backoff)
        self._regexs = regexps

    def choose_lemma(self, tokens, index, history):
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
            break
                # pragma: no cover

class PPLemmatizer(RegexpLemmatizer):
   

    def __init__(self, regexps=None, pps=None, backoff=None):
        """Setup PPLemmatizer().

        :param regexps: List of tuples of form (PATTERN, INT) where INT is
        the principal part number needed to lookup the correct stem.
        :param backoff: Next lemmatizer in backoff chain.
        """
        RegexpLemmatizer.__init__(self, regexps, backoff)
        self._regexs = [estre_replace, avoir_replace, first_conj_rules, i_type_rules, u_type_rules, regime_rules, plural_rules, misc_rules, masc_to_fem_rules, determiner_rules, reduction_rules]

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
                match = [lemma for (lemma, pp) in self.pps.items() if root == pp[regexp[1]]]
                if not match:
                    pass
                else:
                    return match[0]  # Lemma is indexed at zero in PP dictionary



