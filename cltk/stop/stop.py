""" Code for building and working with stoplists
"""

## Goal: to build a stop list of from top 100 count using Counter

from abc import abstractmethod
from collections import Counter

from cltk.utils.cltk_logger import logger

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'


class Stoplist():
    """ Create stoplists
    """

    def __init__(self, language=None):
        """ Initialize stoplist builder with option for language specific parameters
        :type language: str
        :param language : text from which to build the stoplist
        """
        if language:
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

## Write subclass designed to make stoplist from a list of strings
class CorpusStoplist(Stoplist):

    def __init__(self, language=None):
        Stoplist.__init__(self, language)
        if not self.numpy_installed or not self.sklearn_installed:
            print('\n\nThe Corpus-based Stoplist method requires numpy and scikit-learn for calculations. Try installing with `pip install numpy sklearn scipy`.\n\n')
            raise ImportError
        else:
            from sklearn.feature_extraction.text import CountVectorizer

    
    def _make_dtm_vocab(self, texts):
        dtm = self.vectorizer.fit_transform(texts)
        dtm = dtm.toarray()
        vocab = self.vectorizer.get_feature_names()
        vocab = self.np.array(vocab)
        return dtm, vocab
            
    
    def _get_raw_lengths(self, texts):
        return [len(tokens.split()) for tokens in texts] # Use tokenizer rather than split?
    
    def _get_length_array(self, raw_lengths):
        length_array = self.np.array(raw_lengths)
        length_array = length_array.reshape(len(length_array),1)
        return length_array
    
    
    def _get_probabilities(self, dtm, length_array):
        return dtm / length_array

    
    def _get_mean_probabilities(self, P, N):
        # Call N something different?
        probability_sum = self.np.ravel(P.sum(axis=0))
        return probability_sum / N
    
    
    def _get_variance_probabilities(self, bP, P, N):
        variance = (P-bP) ** 2
        variance_sum = self.np.ravel(variance.sum(axis=0))
        return variance_sum / N

    
    def _get_entropies(self, P):
        with self.np.errstate(divide='ignore', invalid='ignore'):
            logprobs = self.np.where(P != 0, self.np.log10(1/P), 0)
            ent = P * logprobs
            return self.np.ravel(ent.sum(axis=0))

    
    def _combine_vocabulary(self, vocab, measure):
        temp = list(zip(vocab, measure))
        temp = sorted(temp, key=lambda x: x[1], reverse=True)
        temp = [item[0] for item in temp]
        return temp        
    
    
    def _borda_sort(self, lists):
        ### From http://stackoverflow.com/a/30259368/1816347 ###
        scores = {}
        for l in lists:
            for idx, elem in enumerate(reversed(l)):
                if not elem in scores:
                    scores[elem] = 0
                scores[elem] += idx
        return sorted(scores.keys(), key=lambda elem: scores[elem], reverse=True)    
    
    
    def build_stoplist(self, texts, basis='zou', size=100, inc_counts=False, lower=True, sort_words=True, remove_punctuation = True, remove_numbers=True, include =[], exclude=[]):
        """
        :param texts: list of strings used as document collection for extracting stopwords
        :param basis: Define the basis for extracting stopwords from the corpus. Available methods are:
                      - 'frequency', word counts
                      - 'mean', mean probabilities
                      - 'variance', variance probabilities
                      - 'entropy', entropy
                      - 'zou', composite measure as defined in the following paper
                        Zou, F., Wang, F.L., Deng, X., Han, S., and Wang, L.S. 2006. “Automatic Construction of Chinese Stop Word List.” In Proceedings of the 5th WSEAS International Conference on Applied Computer Science, 1010–1015. https://pdfs.semanticscholar.org/c543/8e216071f6180c228cc557fb1d3c77edb3a3.pdf.
        :param size: Set the size of the output list
        :param inc_counts: Include basis value; e.g. word counts for 'frequency', mean probabilities for 'mean'
        :param lower: Lowercase corpus or no?
        :param sort_words: Sort output list alphabetically? (Otherwise return is descending by basis value)
        :param remove_punctuation: Remove punctuation from corpus or no?
        :param remove_numbers: Remove numbers from corpus or no?
        :param include: List of words in addition to stopwords that are extracted from the document collection
                        to be added to the final list  
        :param exclude: List of words in addition to stopwords that are extracted from the document collection
                        to be removed from the final list 
        :type texts: list
        :type basis: str
        :type size: int
        :type inc_counts: bool
        :type lower: bool
        :type sort_words: bool
        :type remove_punctuation: bool
        :type remove_numbers: bool
        :type include: list
        :type exclude: list
        :return: a list of stopwords extracted from the corpus
        :rtype: list
        """
        
        
        # Preprocessing
        if self.language == 'latin':
            pass
            # set preprocessing
        else:
            pass
        
        if lower:
            texts = [text.lower() for text in texts]
        
        if remove_punctuation:
            punctuation = "\"#$%&\'()*+,-/:;<=>@[\]^_`{|}~.?!«»"
            translator = str.maketrans({key: " " for key in punctuation})
            texts = [text.translate(translator) for text in texts]

        if remove_numbers:            
            translator = str.maketrans({key: " " for key in '0123456789'})
            texts = [text.translate(translator) for text in texts]    


        # Get DTM and basic descriptive info
        dtm, vocab = self._make_dtm_vocab(texts)  
        
        M = len(vocab)
        N = len(texts)
        
        # Calculate probabilities
        raw_lengths = self._get_raw_lengths(texts)
        l = self._get_length_array(raw_lengths)
        P = self._get_probabilities(dtm, l)
        
        if basis == 'frequency':
            # Calculate plain frequencies
            freq = self.np.ravel(dtm.sum(axis=0))
            freq_list = self._combine_vocabulary(vocab, freq)[:size]
            stops = freq_list
        elif basis == 'mean':
            # Calculate mean probabilities
            MP = self._get_mean_probabilities(P, N)
            mp_list = self._combine_vocabulary(vocab, MP)[:size]
            stops = mp_list
        elif basis == 'variance':
            bP = dtm / sum(raw_lengths)        
            VP = self._get_variance_probabilities(bP, P, N)
            vp_list = self._combine_vocabulary(vocab, VP)[:size]
            stops = vp_list
        elif basis == 'entropy':
            ent = self._get_entropies(P)
            ent_list = self._combine_vocabulary(vocab, ent)[:size]
            stops = set(ent_list)
        elif basis == 'zou':
            MP = self._get_mean_probabilities(P, N)
            mp_list = self._combine_vocabulary(vocab, MP)[:size]
            
            bP = dtm / sum(raw_lengths)        
            VP = self._get_variance_probabilities(bP, P, N)
            vp_list = self._combine_vocabulary(vocab, VP)[:size]

            ent = self._get_entropies(P)
            ent_list = self._combine_vocabulary(vocab, ent)[:size]
            
            lists = [mp_list, vp_list, ent_list]
            stops = self._borda_sort(lists)
        else:
            raise ValueError("Basis '{}' not supported.".format(basis))
        
        if exclude:
            stops = [item for item in stops if item not in exclude]
            
        if include:
            stops.extend(item for item in include if item not in stops)
            
        if sort_words:
            return sorted(stops)
        else:
            return stops
