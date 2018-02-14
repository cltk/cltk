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
        :type language: int
        :param language : size of the output list
        :type language: str
        :param language : language in case of language-specific considerations
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
        
        if exclude:
            stops = [item for item in stops if item not in exclude]
            
        if include:
            stops.extend(item for item in include if item not in stops)
            
        if sort_words:
            return sorted(stops)
        else:
            return stops
        


if __name__ == "__main__":
    test_1 = """cogitanti mihi saepe numero et memoria vetera repetenti perbeati fuisse, quinte frater, illi videri solent, qui in optima re publica, cum et honoribus et rerum gestarum gloria florerent, eum vitae cursum tenere potuerunt, ut vel in negotio sine periculo vel in otio cum dignitate esse possent; ac fuit cum mihi quoque initium requiescendi atque animum ad utriusque nostrum praeclara studia referendi fore iustum et prope ab omnibus concessum arbitrarer, si infinitus forensium rerum labor et ambitionis occupatio decursu honorum, etiam aetatis flexu constitisset. quam spem cogitationum et consiliorum meorum cum graves communium temporum tum varii nostri casus fefellerunt; nam qui locus quietis et tranquillitatis plenissimus fore videbatur, in eo maximae moles molestiarum et turbulentissimae tempestates exstiterunt; neque vero nobis cupientibus atque exoptantibus fructus oti datus est ad eas artis, quibus a pueris dediti fuimus, celebrandas inter nosque recolendas. nam prima aetate incidimus in ipsam perturbationem disciplinae veteris, et consulatu devenimus in medium rerum omnium certamen atque discrimen, et hoc tempus omne post consulatum obiecimus eis fluctibus, qui per nos a communi peste depulsi in nosmet ipsos redundarent. sed tamen in his vel asperitatibus rerum vel angustiis temporis obsequar studiis nostris et quantum mihi vel fraus inimicorum vel causae amicorum vel res publica tribuet oti, ad scribendum potissimum conferam; tibi vero, frater, neque hortanti deero neque roganti, nam neque auctoritate quisquam apud me plus valere te potest neque voluntate."""
    
    test_2 = """ac mihi repetenda est veteris cuiusdam memoriae non sane satis explicata recordatio, sed, ut arbitror, apta ad id, quod requiris, ut cognoscas quae viri omnium eloquentissimi clarissimique senserint de omni ratione dicendi. vis enim, ut mihi saepe dixisti, quoniam, quae pueris aut adulescentulis nobis ex commentariolis nostris incohata ac rudia exciderunt, vix sunt hac aetate digna et hoc usu, quem ex causis, quas diximus, tot tantisque consecuti sumus, aliquid eisdem de rebus politius a nobis perfectiusque proferri; solesque non numquam hac de re a me in disputationibus nostris dissentire, quod ego eruditissimorum hominum artibus eloquentiam contineri statuam, tu autem illam ab elegantia doctrinae segregandam putes et in quodam ingeni atque exercitationis genere ponendam. ac mihi quidem saepe numero in summos homines ac summis ingeniis praeditos intuenti quaerendum esse visum est quid esset cur plures in omnibus rebus quam in dicendo admirabiles exstitissent; nam quocumque te animo et cogitatione converteris, permultos excellentis in quoque genere videbis non mediocrium artium, sed prope maximarum. quis enim est qui, si clarorum hominum scientiam rerum gestarum vel utilitate vel magnitudine metiri velit, non anteponat oratori imperatorem? quis autem dubitet quin belli duces ex hac una civitate praestantissimos paene innumerabilis, in dicendo autem excellentis vix paucos proferre possimus? iam vero consilio ac sapientia qui regere ac gubernare rem publicam possint, multi nostra, plures patrum memoria atque etiam maiorum exstiterunt, cum boni perdiu nulli, vix autem singulis aetatibus singuli tolerabiles oratores invenirentur. ac ne qui forte cum aliis studiis, quae reconditis in artibus atque in quadam varietate litterarum versentur, magis hanc dicendi rationem, quam cum imperatoris laude aut cum boni senatoris prudentia comparandam putet, convertat animum ad ea ipsa artium genera circumspiciatque, qui in eis floruerint quamque multi sint; sic facillime, quanta oratorum sit et semper fuerit paucitas, iudicabit."""
    
    test_corpus = [test_1, test_2]
    
    #from cltk.corpus.latin.readers import latinlibrary
    #test_corpus = [latinlibrary.raw(file) for file in latinlibrary.fileids() if 'cicero/' in file]
    
    #remove = ['Cicero', "The Latin Library", "The Classics Page"]
    #for word in remove:
    #    test_corpus = [text.replace(word,' ') for text in test_corpus]
    
    S = CorpusStoplist('latin')
    print(S.build_stoplist(test_corpus, size=10,basis='zou'))