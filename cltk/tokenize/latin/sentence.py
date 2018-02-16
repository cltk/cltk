""" Code for sentence tokenization: Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
from cltk.tokenize.sentence2 import BaseSentenceTokenizer
from cltk.utils.file_operations import open_pickle

#from nltk.metrics.scores import accuracy, precision, recall, f-score

#from cltk.utils.cltk_logger import logger

class SentenceTokenizer(BaseSentenceTokenizer):
    """ Base class for sentence tokenization
    """

    def __init__(self):
        """ 
        :param language : language for sentence tokenization
        :type language: str
        """
        BaseSentenceTokenizer.__init__(self, 'latin')
        self.model = self._get_model()
    
        
             
    def tokenize(self, text, model=None):
        """
        Method for tokenizing sentences. This method 
        should be overridden by subclasses of SentenceTokenizer.
        """
        if not self.model:
            model = self.model
        
        tokenizer = open_pickle(self.model)
        
        #return type(tokenizer), dir(tokenizer)
        #return tokenizer.sentences_from_text(text, realign_boundaries=True)
    
    
    def _get_model(self):
        model_file = '{}.pickle'.format(self.language)
        model_path = os.path.join('~/cltk_data',
                                self.language,
                                'model/' + self.language + '_models_cltk/tokenizers/sentence')  # pylint: disable=C0301
        model_path = os.path.expanduser(model_path)
        model_path = os.path.join(model_path, model_file)
        assert os.path.isfile(model_path), \
            'Please download sentence tokenization model for {}.'.format(self.language)
        return model_path
            
        
if __name__ == "__main__":
    text = "arma. virumque. cano."
    T = SentenceTokenizer()
    sents = T.tokenize(text)
    print(sents)
    print(T.model)
    
    import nltk.data
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    tokenizer.tokenize(text)
    print(type(tokenizer), dir(tokenizer))
