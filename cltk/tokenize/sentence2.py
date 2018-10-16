""" Code for sentence tokenization
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'


from abc import abstractmethod

#from nltk.metrics.scores import accuracy, precision, recall, f-score

#from cltk.utils.cltk_logger import logger

class BaseSentenceTokenizer():
    """ Base class for sentence tokenization
    """

    def __init__(self, language=None):
        """ Initialize stoplist builder with option for language specific parameters
        :param language : language for sentence tokenization
        :type language: str
        """
        if language:
            self.language = language.lower()            
        
        
    @abstractmethod        
    def tokenize(self, text):
        """
        Method for tokenizing sentences. This method 
        should be overridden by subclasses of SentenceTokenizer.
        """
        
## Think more about how this will work
#    def evaluate(self, gold):
#        """
#        following http://www.nltk.org/_modules/nltk/tag/api.html#TaggerI.evaluate
#        Score the accuracy of the tokenizer against the gold standard.
#        Strip the tags from the gold standard text, retokenize it using
#        the tokenizer, then compute the accuracy, precision, recall, and f-score.
#
#        :type gold: list(list(tuple(str, str)))
#        :param gold: The list of tagged sentences to score the tagger on.
#        :rtype: float
#        """
#
#        tokenized_sents = self.tag_sents(untag(sent) for sent in gold)
#        gold_tokens = list(chain(*gold))
#        test_tokens = list(chain(*tagged_sents))
#        return accuracy(gold_tokens, test_tokens)        