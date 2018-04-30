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

from cltk.lemmatize.backoff import DefaultLemmatizer, IdentityLemmatizer, UnigramLemmatizer, RegexpLemmatizer
from cltk.lemmatize.latin.latin import latin_sub_patterns, latin_verb_patterns, latin_pps, rn_patterns
from cltk.utils.file_operations import open_pickle


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

                
    def lemmatize(self, tokens):
        return self.tag(tokens)
    
    
class RomanNumeralLemmatizer(RegexpLemmatizer):
    """"""
    def __init__(self, regexps=rn_patterns, default=None, backoff=None):
        """RomanNumeralLemmatizer"""
        RegexpLemmatizer.__init__(self, regexps, backoff)
        self._regexs = [(re.compile(regexp), pattern,) for regexp, pattern in regexps]
        self.default = default
        
        
    def choose_tag(self, tokens, index, history):
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

                
class BackoffLemmatizer(object):
    """Suggested backoff chain; includes at least on of each
    type of major sequential backoff class from backoff.py

    ### Putting it all together
    ### BETA Version of the Backoff Lemmatizer
    """
    
    
    def __init__(self, train=None):
        self.rel_path = os.path.join('~/cltk_data/latin/model/latin_models_cltk/lemmata/backoff')
        self.path = os.path.expanduser(self.rel_path)

        if train:
            self.pos_train_sents = train
        else:
            self.pos_train_sents = self._get_training_data()
        self.train_sents = [[(item[0], item[1]) for item in sent] for sent in self.pos_train_sents]
        #self.seed = seed        

        # Check for presence of LATIN_OLD_MODEL
        file = 'latin_lemmata_cltk.pickle'      

        old_model_path = os.path.join(self.path, file)
        if os.path.isfile(old_model_path):
            self.LATIN_OLD_MODEL = open_pickle(old_model_path)
        else:
            self.LATIN_OLD_MODEL = {}
            print('The file %s is not available in cltk_data' % file)  
        
        # Check for presence of LATIN_MODEL
        file = 'latin_model.pickle'      

        model_path = os.path.join(self.path, file)
        if os.path.isfile(model_path):
            self.LATIN_MODEL = open_pickle(model_path)
        else:
            self.LATIN_MODEL = {}
            print('The file %s is not available in cltk_data' % file)  
        
        self.latin_sub_patterns = latin_sub_patterns
        self.latin_verb_patterns = latin_verb_patterns
        self.latin_pps = latin_pps

        self._define_lemmatizer()

    
    def _get_training_data(self):
        # Set up training sentences
        path = os.path.expanduser(self.rel_path)

        # Check for presence of latin_pos_lemmatized_sents
        file = 'latin_pos_lemmatized_sents.pickle'      
        latin_pos_lemmatized_sents_path = os.path.join(path, file)
        if os.path.isfile(latin_pos_lemmatized_sents_path):
            latin_pos_lemmatized_sents = open_pickle(latin_pos_lemmatized_sents_path)
        else:
            latin_pos_lemmatized_sents = []
            print('The file %s is not available in cltk_data' % file)
        return latin_pos_lemmatized_sents
        
        
    def _define_lemmatizer(self):
        
        # Suggested backoff chain--should be tested for optimal order
        backoff0 = None
        backoff1 = IdentityLemmatizer()
        backoff2 = UnigramLemmatizer(model=self.LATIN_OLD_MODEL, backoff=backoff1)
        backoff3 = PPLemmatizer(regexps=self.latin_verb_patterns, pps=self.latin_pps, backoff=backoff2)                 
        backoff4 = RegexpLemmatizer(self.latin_sub_patterns, backoff=backoff3)
        backoff5 = UnigramLemmatizer(self.train_sents, backoff=backoff4)
        backoff6 = UnigramLemmatizer(model=self.LATIN_MODEL, backoff=backoff5)
        self.lemmatizer = backoff6


    def lemmatize(self, tokens):
        lemmas = self.lemmatizer.lemmatize(tokens)
        return lemmas

#    def evaluate(self):
#        #lemmatizer = self._define_lemmatizer()
#        return lemmatizer.evaluate(self.test_sents)

########
### EXPERIMENTAL - NOT IN USE
########
#
#class ContextPOSLemmatizer(ContextLemmatizer):
#    """Lemmatizer that combines context with POS-tagging based on
#        training data. Subclasses define context.
#        
#        The code for _train closely follows ContextTagger in
#        https://github.com/nltk/nltk/blob/develop/nltk/tag/sequential.py
#        
#        This lemmatizer is included here as proof of concept that 
#        lemma disambiguation can be made based on the pattern:
#        LEMMA & POS of following word.
#        
#        Should be rewritten to give more flexibility to the kinds
#        of context that a free word order language demand. I.e. to
#        study patterns such as:
#        POS of preceding word & LEMMA
#        LEMMA & POS of following two words
#        LEMMA & POS of n-skipgrams
#        etc.            
#        """
#
#    def __init__(self, context_to_lemmatize, include=None, backoff=None):
#        """Setup ContextPOSLemmatizer().
#
#        :param context_to_lemmatize: List of tuples of the form (TOKEN, LEMMA);
#        this should be 'gold standard' data that can be used to train on a 
#        given context, e.g. unigrams, bigrams, etc.
#        :param include: List of tokens to include, all other tokens return None
#        from choose_lemma--runs VERY SLOW if no list is given as a parameter
#        since every token gets POS-tagged. Only tested so far on 'cum'
#        --also, test data only distinguishes 'cum1'/'cum2'. Further 
#        testing should be done with ambiguous lemmas using Morpheus numbers.
#        :param backoff: Next lemmatizer in backoff chain.
#        :param include: List of tokens to consider        
#        """
#        # SequentialBackoffLemmatizer.__init__(self, backoff)
#        ContextLemmatizer.__init__(self, context_to_lemmatize, backoff)
#        self.include = include
#        self._context_to_tag = (context_to_lemmatize if context_to_lemmatize else {})
#
#    def _get_pos_tags(self, tokens):
#        """Iterate through list of tokens and use POS tagger to build
#        a corresponding list of tags.
#
#        :param tokens: List of tokens to be POS-tagged
#        :return: List with POS-tag for each token
#        """
#        # Import (and define tagger) with other imports?    
#        from cltk.tag.pos import POSTag
#        tagger = POSTag('latin')
#        tokens = " ".join(tokens)
#        tags = tagger.tag_ngram_123_backoff(tokens)
#        tags = [tag[1][0].lower() if tag[1] else tag[1] for tag in tags]
#        return tags
#
#    def choose_lemma(self, tokens, index, history):
#        """Choose lemma based on POS-tag defined by context.
#
#        :param tokens: List of tokens to be lemmatized
#        :param index: Int with current token
#        :param history: List with POS-tags of tokens that have already
#        been lemmatized.
#        :return: String with suggested lemma
#        """        
#        if self.include:
#            if tokens[index] not in self.include:
#                return None
#        history = self._get_pos_tags(tokens)
#        context = self.context(tokens, index, history)
#        suggested_lemma = self._context_to_tag.get(context)
#        return suggested_lemma
#
#    def _train(self, lemma_pos_corpus, cutoff=0):
#        """Override method for _train from ContextTagger in
#        nltk.tag.sequential. Original _train method expects
#        tagged corpus of form (TOKEN, LEMMA); this expects in
#        addition POS-tagging information.
#
#        :param lemma_pos_corpus: List of tuples of form (TOKEN, LEMMA, POSTAG)
#        :param cutoff: Int with minimum number of matches to choose lemma
#        """
#        token_count = hit_count = 0
#
#        # A context is considered 'useful' if it's not already lemmatized
#        # perfectly by the backoff lemmatizer.
#        useful_contexts = set()
#
#        # Count how many times each tag occurs in each context.
#        fd = ConditionalFreqDist()
#        for sentence in lemma_pos_corpus:
#            tokens, lemmas, poss = zip(*sentence)
#            for index, (token, lemma, pos) in enumerate(sentence):
#                # Record the event.
#                token_count += 1
#
#                context = self.context(tokens, index, poss)
#                if context is None: continue
#                fd[context][lemma] += 1
#
#                # If the backoff got it wrong, this context is useful:
#                if (self.backoff is None or lemma != self.backoff.tag_one(tokens, index, lemmas[:index])):  # pylint: disable=line-too-long
#                    useful_contexts.add(context)
#
#        # Build the context_to_lemmatize table -- for each context, figure
#        # out what the most likely lemma is. Only include contexts that
#        # we've seen at least `cutoff` times.
#        for context in useful_contexts:
#            best_lemma = fd[context].max()
#            hits = fd[context][best_lemma]
#            if hits > cutoff:
#                self._context_to_tag[context] = best_lemma
#                hit_count += hits
#
#
#class NgramPOSLemmatizer(ContextPOSLemmatizer):
#    """"""
#    def __init__(self, n, train=None, model=None, include=None,
#                 backoff=None, cutoff=0):
#        """Setup for NgramPOSLemmatizer
#
#        :param n: Int with length of 'n'-gram
#        :param train: List of tuples of the form (TOKEN, LEMMA, POS)
#        :param model: Dict; DEPRECATED
#        :param include: List of tokens to consider
#        :param backoff: Next lemmatizer in backoff chain.
#        :param cutoff: Int with minimum number of matches to choose lemma
#        """
#        self._n = n
#        self._check_params(train, model)
#        ContextPOSLemmatizer.__init__(self, model, include, backoff)
#
#        if train:
#            self._train(train, cutoff)
#
#    def context(self, tokens, index, history):
#        """Redefines context with look-ahead of length n (not look behind
#        as in original method).
#
#        :param tokens: List of tokens to be lemmatized
#        :param index: Int with current token
#        :param history: List with tokens that have already been
#        tagged/lemmatized
#        :return: Tuple of the form (TOKEN, (CONTEXT)); CONTEXT will
#        depend on ngram value, e.g. for bigram ('cum', ('n',)) but
#        for trigram ('cum', ('n', 'n', ))
#        """
#        lemma_context = tuple(history[index + 1: index + self._n])
#        return tokens[index], lemma_context
#
#
#class BigramPOSLemmatizer(NgramPOSLemmatizer):
#    """"""
#    def __init__(self, train=None, model=None, include=None,
#                 backoff=None, cutoff=0):
#        """Setup for BigramPOSLemmatizer()"""
#        NgramPOSLemmatizer.__init__(self, 2, train, model,
#                                    include, backoff, cutoff)
#
#
##class TrigramPOSLemmatizer(NgramPOSLemmatizer):
##    """"""
##    def __init__(self, train=None, model=None, include=None,
##                 backoff=None, cutoff=0):
##        """Setup for TrigramPOSLemmatizer()"""
##        NgramPOSLemmatizer.__init__(self, 3, train, model, include,
##                                    backoff, cutoff)
    
if __name__ == "__main__":
    l = BackoffLemmatizer()    
    test = "arma virum que cano aviatrices habuit xxii".split()
    print(l.lemmatize(test))