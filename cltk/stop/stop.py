""" Code for building and working with stoplists
"""

## Goal: to build a stop list of from top 100 count using Counter

from collections import Counter

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'GPL License.'


class Stoplist():
    """ Create stoplists
    """

    def __init__(self, language=None):
        """ Initialize stoplist builder with option for language specific parameters
        :type language: str
        :param language : text from which to build the stoplist
        """
        self.language = language.lower()
        Stoplist.__init__(self, language)        
        self.numpy_installed = True ## Write utility for common import traps?
        self.sklearn_installed = True
        
        try:
            import numpy as np
        except ImportError:
            self.numpy_installed = False        
        
        try:
            from sklearn.feature_extraction.text import CountVectorizer
        except ImportError:
            self.sklearn_installed = False
            
    def build_stoplist(text, size=100):
        """
        :type language: int
        :param language : size of the output list
        :type language: str
        :param language : language in case of language-specific considerations
        """
        
        if self.language = 'latin':
            pass
            # set preprocessing
        else:
            pass
        
        text = text.split() # Load real tokenizer
        c = Counter(text)
        return c.most_common(size)

## Write subclass designed to make a stoplist from a single string.
class StringStoplist(Stoplist):
    
    def __init__(self, language=None):
        Stoplist.__init__(self, language)      
        
        
    def build_stoplist(text, size=100):
        """
        :type language: int
        :param language : size of the output list
        :type language: str
        :param language : language in case of language-specific considerations
        """
        
        if self.language = 'latin':
            pass
            # set preprocessing
        else:
            pass
        
        text = text.split() # Load real tokenizer
        c = Counter(text)
        return c.most_common(size)

## Write subclass designed to make stoplist from a list of strings
class CorpusStoplist(Stoplist):

    def __init__(self, language=None):
        Stoplist.__init__(self, language)
        if not self.numpy_installed and not self.sklearn_installed:
            logger.error('The Corpus-based Stoplist method requires numpy and scikit-learn for calculations. Try installing with `pip install numpy sklearn scipy`.')
            raise ImportError
        
    
    def _make_dtm(texts):
        vectorizer = CountVectorizer(input='content') # Set df?
        dtm = vectorizer.fit_transform(texts)
        dtm = dtm.toarray()
        return dtm
    
    
    def _make_vocabulary(dtm)
        vectorizer = CountVectorizer(input='content') # Set df? Make DRY with previous function?
        dtm = vectorizer.fit_transform(texts)
        vocab = vectorizer.get_feature_names()
        vocab = np.array(vocab)
        return vocab
    
    def _get_raw_lengths(texts):
        return [len(tokens.split()) for tokens in texts] # Use tokenizer rather than split?
    
    def _get_length_array(raw_lengths):
        length_array = np.array(raw_lengths)
        length_array = length_array.reshape(len(lengths),1)
        return length_array
    
    
    def _get_probabilities(dtm, length_array):
        return dtm / length_array

    
    def _get_mean_probabilities(P, N):
        # Call N something different?
        probability_sum = np.ravel(P.sum(axis=0))
        return probability_sum / N
    
    
    def _get_variance_probabilities(bP, P, N):
        variance = (P-bP) ** 2
        variance_sum = np.ravel(variance.sum(axis=0))
        return variance_sum / N

    
    def _get_entropies(P):
        with np.errstate(divide='ignore', invalid='ignore'):
            log_probabilties = np.where(P != 0, np.log10(1/P), 0)
        return P / log_probabilities

    def _combine_vocabulary(vocab, measure):
        temp = list(zip(vocab, measure))
        temp.sort(key=lambda x: x[1], reverse=True)
        temp = [item[0] for item in temp]
        return temp        
    
    
    def _borda_sort(lists):
        ### From http://stackoverflow.com/a/30259368/1816347 ###
        scores = {}
        for l in lists:
            for idx, elem in enumerate(reversed(l)):
                if not elem in scores:
                    scores[elem] = 0
                scores[elem] += idx
        return sorted(scores.keys(), key=lambda elem: scores[elem], reverse=True)    
    
    def build_stoplist(texts, size=100):
        """
        :type language: int
        :param language : size of the output list
        :type language: str
        :param language : language in case of language-specific considerations
        """
        
        if self.language = 'latin':
            pass
            # set preprocessing
        else:
            pass
        
        dtm = _make_dtm(texts)
        vocab = _make_vocabulary(d)       
        
        M = len(vocab)
        N = len(texts)

        # Calculate probabilities
        raw_lengths = _get_raw_lengths(texts)
        l = _get_length_array(raw_lengths)
        P = dtm / l
        
        # Calculate mean probabilities
        MP = _get_mean_probabilities(P, N)
        
        # Calculate variance probabilities
        bP = dtm / sum(raw_lengths)        
        VP = _get_variance_probabilities(bP, VP, N)
        
        # Calculate entropies
        ent = _get_entropies(P)
        
        # Zip vocabulary
        mp_list = _combine_vocabulary(vocab, MP)[:size]
        vp_list = combine_vocabulary(vocab, VP)[:size]
        ent_list = combine_vocabulary(vocab, ent)[:size]
        
        lists = [mp, vp, ent]
        return borda_sort(lists) 
