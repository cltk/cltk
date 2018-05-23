from cltk.utils.cltk_logger import logger
import importlib.machinery
import os

class Lemmatize:
    """Example class for all semantic 'lemmatizers'"""
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.lemmatized_tokens = []
    def load_replacement_patterns(self):
        """Check for availability of the specified dictionary."""
        filename = self.dictionary + '.py'
        rel_path = os.path.join('~','cltk_data','latin','model','latin_models_cltk','semantics',filename)
        path = os.path.expanduser(rel_path)
        #logger.info('Loading lemmata. This may take a minute.')
        loader = importlib.machinery.SourceFileLoader(filename, path)
        module = loader.load_module()
        self.lemmata = module.LEMMATA    
    def lemmatize(self, tokens):
        """Return a list of possible lemmata and their probabilities for each token"""
        for token in tokens:
            # look for token in lemma dict keys
            if token.lower() in self.lemmata.keys():
                """lemmas is a list of possible lemmata. Probability values must be assigned."""
                """lemmalist is a list of the form [(LEMMA, PROBABILITY), (LEMMA, PROBABILITY)]"""
                """lemmaobj is a tuple with the form (LEMMA, LIST)"""
                lemmas = self.lemmata[token.lower()]
                lemmalist = []
                for lemma in lemmas:
                    lemmalist.append(tuple(lemma, 1/len(lemmas)))
                lemmaobj = tuple(token, lemmalist)                
            else:
            # if token not found in lemma-headword list, return the token itself
                lemmalist = []
                lemmalist.append(tuple(token, 1))
                lemmaobj = tuple(token, lemmalist)
            lemmatized_tokens.append(lemmalist)                        
        return lemmatized_tokens
