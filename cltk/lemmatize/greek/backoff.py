"""Module for lemmatizing Greek—NOT READY
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

import os

import re

from cltk.lemmatize.backoff import DefaultLemmatizer, IdentityLemmatizer, UnigramLemmatizer, RegexpLemmatizer
from cltk.lemmatize.greek.greek import greek_sub_patterns, greek_pps
from cltk.utils.file_operations import open_pickle


#class PPLemmatizer(RegexpLemmatizer):
#    """Customization of the RegexpLemmatizer for Latin. The RegexpLemmatizer is
#        used as a stemmer; the stem is then applied to a dictionary lookup of
#        principal parts."""
#    def __init__(self, regexps=None, pps=None, backoff=None):
#        """Setup PPLemmatizer().
#
#        :param regexps: List of tuples of form (PATTERN, INT) where INT is
#        the principal part number needed to lookup the correct stem.
#        :param backoff: Next lemmatizer in backoff chain.
#        """
#        RegexpLemmatizer.__init__(self, regexps, backoff)
#        # Note different compile to make use of principal parts dictionary structure; also, note
#        # that the PP dictionary has been set up so that principal parts match their traditional
#        # numbering, i.e. present stem is indexed as 1. The 0 index is used for the lemma.
#        self._regexs = latin_verb_patterns
#        self.pps = latin_pps
#        
#
#    def choose_tag(self, tokens, index, history):
#        """Use regular expressions for rules-based lemmatizing based on
#        principal parts stems. Tokens are matched for patterns with 
#        the ending kept as a group; the stem is looked up in a dictionary 
#        by PP number (see above) and ending is discarded.
#
#        :param tokens: List of tokens to be lemmatized
#        :param index: Int with current token
#        :param history: List with tokens that have already been lemmatized
#        :return: Str with index[0] from the dictionary value, see above about '0 index'
#        """
#        for regexp in self._regexs:
#            m = re.match(regexp[0], tokens[index])
#            if m:
#                root = m.group(1)
#                match = [lemma for (lemma, pp) in self.pps.items() if root == pp[regexp[1]]]
#                if not match:
#                    pass
#                else:
#                    return match[0] # Lemma is indexed at zero in PP dictionary
#
#                
#    def lemmatize(self, tokens):
#        return self.tag(tokens)
#
#                
class BackoffLemmatizer(object):
    """Suggested backoff chain; includes at least on of each
    type of major sequential backoff class from backoff.py

    ### Putting it all together
    ### BETA Version of the Backoff Lemmatizer
    """
    pass
    
    
    def __init__(self, train=None):
        self.rel_path = os.path.join('~/cltk_data/greek/model/greek_models_cltk/lemmata/backoff')
        self.path = os.path.expanduser(self.rel_path)
#
#        if train:
#            self.pos_train_sents = train
#        else:
#            self.pos_train_sents = self._get_training_data()
#        self.train_sents = [[(item[0], item[1]) for item in sent] for sent in self.pos_train_sents]     

        # Check for presence of LATIN_OLD_MODEL
        file = 'greek_lemmata_cltk.pickle'      

        old_model_path = os.path.join(self.path, file)
        if os.path.isfile(old_model_path):
            self.GREEK_OLD_MODEL = open_pickle(old_model_path)
        else:
            self.GREEK_OLD_MODEL = {}
            print('The file %s is not available in cltk_data' % file)  
        
#        # Check for presence of LATIN_MODEL
#        file = 'latin_model.pickle'      
#
#        model_path = os.path.join(self.path, file)
#        if os.path.isfile(model_path):
#            self.LATIN_MODEL = open_pickle(model_path)
#        else:
#            self.LATIN_MODEL = {}
#            print('The file %s is not available in cltk_data' % file)  
        
#        self.latin_sub_patterns = latin_sub_patterns
#        self.latin_verb_patterns = latin_verb_patterns
#        self.latin_pps = latin_pps

        self._define_lemmatizer()

    
#    def _get_training_data(self):
#        # Set up training sentences
#        path = os.path.expanduser(self.rel_path)
#
#        # Check for presence of latin_pos_lemmatized_sents
#        file = 'latin_pos_lemmatized_sents.pickle'      
#        latin_pos_lemmatized_sents_path = os.path.join(path, file)
#        if os.path.isfile(latin_pos_lemmatized_sents_path):
#            latin_pos_lemmatized_sents = open_pickle(latin_pos_lemmatized_sents_path)
#        else:
#            latin_pos_lemmatized_sents = []
#            print('The file %s is not available in cltk_data' % file)
#        return latin_pos_lemmatized_sents
        
        
    def _define_lemmatizer(self):
        #Suggested backoff chain--should be tested for optimal order
        backoff0 = None
        backoff1 = IdentityLemmatizer()
        backoff2 = UnigramLemmatizer(model=self.GREEK_OLD_MODEL, backoff=backoff1)
#        backoff3 = PPLemmatizer(regexps=self.latin_verb_patterns, pps=self.latin_pps, backoff=backoff2)                 
#        backoff4 = RegexpLemmatizer(self.latin_sub_patterns, backoff=backoff3)
#        backoff5 = UnigramLemmatizer(self.train_sents, backoff=backoff4)
#        backoff6 = UnigramLemmatizer(model=self.LATIN_MODEL, backoff=backoff5)
        self.lemmatizer = backoff2


    def lemmatize(self, tokens):
        lemmas = self.lemmatizer.lemmatize(tokens)
        return lemmas

    
#if __name__ == "__main__":
#    l = BackoffLemmatizer()    
#    test = "arma virum que cano aviatrices habuit xxii".split()
#    print(l.lemmatize(test))