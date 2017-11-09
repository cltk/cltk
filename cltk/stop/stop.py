""" Code for building and working with stoplists
"""

## Goal: to build a stop list of from top 100 count using Counter

from abc import abstractmethod
from collections import Counter

from cltk.utils.cltk_logger import logger

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
        self.numpy_installed = True ## Write utility for common import traps?
        self.sklearn_installed = True
        
        try:
            import numpy as np
            self.np = np
        except ImportError:
            self.numpy_installed = False        
        
        try:
            from sklearn.feature_extraction.text import CountVectorizer
            self.vectorizer = CountVectorizer(input='content') # Set df?
        except ImportError:
            self.sklearn_installed = False
            
            
    @abstractmethod        
    def build_stoplist(self, text, size=100):
        """
        Build a stoplist based on string or list of strings. This method 
        should be overridden by subclasses of Stoplist.
        """
        
        
## Write subclass designed to make a stoplist from a single string.
class StringStoplist(Stoplist):
    """ Creates a stoplist based on the input of a single string of text.
    """
    
    
    def __init__(self, language=None):
        Stoplist.__init__(self, language)      
        self.language = language
        
    def build_stoplist(self, text, size=100, inc_counts=False, lower=True, sort_words=True, remove_punctuation = True, remove_numbers=True):
        """
        :type language: int
        :param language : size of the output list
        :type language: str
        :param language : language in case of language-specific considerations
        """
        
        # Move all of this preprocessing code outside 'build_stoplist'
        if self.language == 'latin':
            pass
            # set preprocessing
        else:
            pass
        
        if lower:
            text = text.lower()
        
        if remove_punctuation:
            punctuation = "\"#$%&\'()*+,-/:;<=>@[\]^_`{|}~.?!«»"
            translator = str.maketrans({key: " " for key in punctuation})
            text = text.translate(translator)

        if remove_numbers:            
            translator = str.maketrans({key: " " for key in '0123456789'})
            text = text.translate(translator)
        
        text = text.split() # Load real tokenizer
        c = Counter(text)
        
        stoplist = c.most_common(size)
        
        if sort_words:
            stoplist.sort()
        
        if inc_counts:
            return stoplist
        
        return [item[0] for item in stoplist]

### Write subclass designed to make stoplist from a list of strings
#class CorpusStoplist(Stoplist):
#
#    def __init__(self, language=None):
#        Stoplist.__init__(self, language)
#        if not self.numpy_installed or not self.sklearn_installed:
#            print('\n\nThe Corpus-based Stoplist method requires numpy and scikit-learn for calculations. Try installing with `pip install numpy sklearn scipy`.\n\n')
#            raise ImportError
#        else:
#            from sklearn.feature_extraction.text import CountVectorizer
#        
#    
#    def _make_dtm_vocab(self, texts):
#        dtm = self.vectorizer.fit_transform(texts)
#        dtm = dtm.toarray()
#        vocab = self.vectorizer.get_feature_names()
#        vocab = self.np.array(vocab)
#        return dtm, vocab
#            
#    
#    def _get_raw_lengths(self, texts):
#        return [len(tokens.split()) for tokens in texts] # Use tokenizer rather than split?
#    
#    def _get_length_array(self, raw_lengths):
#        length_array = self.np.array(raw_lengths)
#        length_array = length_array.reshape(len(length_array),1)
#        return length_array
#    
#    
#    def _get_probabilities(self, dtm, length_array):
#        return dtm / length_array
#
#    
#    def _get_mean_probabilities(self, P, N):
#        # Call N something different?
#        probability_sum = self.np.ravel(P.sum(axis=0))
#        return probability_sum / N
#    
#    
#    def _get_variance_probabilities(self, bP, P, N):
#        variance = (P-bP) ** 2
#        variance_sum = self.np.ravel(variance.sum(axis=0))
#        return variance_sum / N
#
#    
#    #def _get_entropies(self, P):
#    #    with self.np.errstate(divide='ignore', invalid='ignore'):
#    #        log_probabilities = self.np.where(P != 0, self.np.log10(1/P), 0)
#    #    return P / log_probabilities
#
#    def _combine_vocabulary(self, vocab, measure):
#        temp = list(zip(vocab, measure))
#        temp = sorted(temp, key=lambda x: x[1], reverse=True)
#        temp = [item[0] for item in temp]
#        return temp        
#    
#    
#    def _borda_sort(self, lists):
#        ### From http://stackoverflow.com/a/30259368/1816347 ###
#        scores = {}
#        for l in lists:
#            for idx, elem in enumerate(reversed(l)):
#                if not elem in scores:
#                    scores[elem] = 0
#                scores[elem] += idx
#        return sorted(scores.keys(), key=lambda elem: scores[elem], reverse=True)    
#    
#    def build_stoplist(self, texts, size=100, inc_counts=False, lower=True, sort_words=True, remove_punctuation = True, remove_numbers=True):
#        """
#        :type language: int
#        :param language : size of the output list
#        :type language: str
#        :param language : language in case of language-specific considerations
#        """
#        
#        if self.language == 'latin':
#            pass
#            # set preprocessing
#        else:
#            pass
#        
#        if lower:
#            texts = [text.lower() for text in texts]
#        
#        if remove_punctuation:
#            punctuation = "\"#$%&\'()*+,-/:;<=>@[\]^_`{|}~.?!«»"
#            translator = str.maketrans({key: " " for key in punctuation})
#            texts = [text.translate(translator) for text in texts]
#
#        if remove_numbers:            
#            translator = str.maketrans({key: " " for key in '0123456789'})
#            texts = [text.translate(translator) for text in texts]    
#        
#        
#        dtm, vocab = self._make_dtm_vocab(texts)  
#        
#        M = len(vocab)
#        N = len(texts)
#
#        # Calculate probabilities
#        raw_lengths = self._get_raw_lengths(texts)
#        l = self._get_length_array(raw_lengths)
#        P = dtm / l
#        
#        # Calculate mean probabilities
#        MP = self._get_mean_probabilities(P, N)
#        
#        # Calculate variance probabilities
#        bP = dtm / sum(raw_lengths)        
#        VP = self._get_variance_probabilities(bP, P, N)
#        
#        # Calculate entropies
#        #ent = self._get_entropies(P)
#        
#        # Zip vocabulary
#        mp_list = self._combine_vocabulary(vocab, MP)[:size]
#        vp_list = self._combine_vocabulary(vocab, VP)[:size]
#        #ent_list = self._combine_vocabulary(vocab, ent)[:size]
#
#        lists = [mp_list, vp_list]        
#        #lists = [mp_list, vp_list, ent_list]
#        return self._borda_sort(lists)
