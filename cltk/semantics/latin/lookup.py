from cltk.utils.cltk_logger import logger
import importlib.machinery
import os

class Lookup:
    """Example class for all semantic 'lemmatizers'"""
    def __init__(self, dictionary, language):
        self.dictionary = dictionary
        self.language = language
    def load_replacement_patterns(self):
        """Check for availability of the specified dictionary."""
        filename = self.dictionary + '.py'
        models = self.language + '_models_cltk'
        rel_path = os.path.join('~','cltk_data', self.language,'model', models,'semantics',filename)
        path = os.path.expanduser(rel_path)
        #logger.info('Loading lemmata. This may take a minute.')
        loader = importlib.machinery.SourceFileLoader(filename, path)
        module = loader.load_module()
        self.lemmata = module.DICTIONARY    
    def lookup(self, tokens):
        """Return a list of possible lemmata and their probabilities for each token"""
        lemmatized_tokens = []
        for token in tokens:
            # look for token in lemma dict keys
            if token.lower() in self.lemmata.keys():
                """lemmas is a list of possible lemmata. Probability values must be assigned."""
                """lemmalist is a list of the form [(LEMMA, PROBABILITY), (LEMMA, PROBABILITY)]"""
                """lemmaobj is a tuple with the form (LEMMA, LIST)"""
                lemmas = self.lemmata[token.lower()]
                lemmalist = []
                for lemma in lemmas:
                    lemmalist.append((lemma, 1/len(lemmas)))
                lemmaobj = (token, lemmalist)                
            else:
            # if token not found in lemma-headword list, return the token itself
                lemmalist = []
                lemmalist.append((token, 1))
                lemmaobj = (token, lemmalist)
            lemmatized_tokens.append(lemmaobj)                        
        return lemmatized_tokens
