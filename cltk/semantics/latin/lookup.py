from cltk.utils.cltk_logger import logger
import importlib.machinery
import os

class Lemmata:
    """Parent class for all semantic 'lemmatizers'. Initialize with the dictionary type (lemmata, synonym, translation) and the source language)."""
    def __init__(self, dictionary, language):
        self.dictionary = dictionary
        self.language = language
        self.load_replacement_patterns()
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
                #lemmas is a list of possible lemmata. Probability values must be assigned.
                #lemmalist is a list of the form [(LEMMA, PROBABILITY), (LEMMA, PROBABILITY)]
                #lemmaobj is a tuple with the form (LEMMA, LIST)
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
    def isolate(self, obj):
        """Feed a standard semantic object in and receive a simple list of lemmata"""
        answers = []
        for token in obj:
            lemmata = token[1]
            for pair in lemmata:
                answers.append(pair[0])
        return answers

class Synonyms(Lemmata):
    def __init__(self, dictionary, language):
        self.dictionary = dictionary
        self.language = language
        self.load_replacement_patterns()
    def load_replacement_patterns(self):
        """Check for availability of the specified dictionary."""
        filename = self.dictionary + '.py'
        models = self.language + '_models_cltk'
        rel_path = os.path.join('~','cltk_data', self.language,'model', models,'semantics',filename)
        path = os.path.expanduser(rel_path)
        #logger.info('Loading synonyms. This may take a minute.')
        loader = importlib.machinery.SourceFileLoader(filename, path)
        module = loader.load_module()
        self.synonyms = module.DICTIONARY
    def lookup(self, lems):
        """Requires a list of lemmata, not tokens. Feed tokens through a Lemmata object's lookup() and isolate() methods first."""
        final_synonyms = []
        for lemma in lems:
            if lemma.lower() in self.synonyms.keys():
                syns = self.synonyms[lemma.lower()]
                synlist = []
                for syn in syns:
                    synlist.append((syn, 1/len(syns)))
                synobj = (lemma, synlist)
                final_synonyms.append(synobj)
            else:
                pass
        return final_synonyms









































