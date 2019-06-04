"""This module is designed around looking up synonyms for Latin and Greek words.
The synonym and translation dictionaries used by this module were originally 
developed by Chris Forstall and James Gawley of the Tesserae Project (http://github.com/tesserae).
In addition to looking up alternate words, this module is designed to assign probabilities to each possible synonym.
As of June 11, 2018, probability distributions are simply split evenly between possibilities. This will be changed soon.
"""

import importlib.machinery
import os
import types

from cltk.utils.cltk_logger import logger


class Lemmata:
    """Parent class for all semantic 'lemmatizers'. Initialize with the
    dictionary type (lemmata, synonym, translation) and the source language).
    """

    def __init__(self, dictionary, language):
        self.dictionary = dictionary
        self.language = language
        self.lemmata = self.load_replacement_patterns()

    def load_replacement_patterns(self):
        """Check for availability of the specified dictionary."""
        filename = self.dictionary + '.py'
        models = self.language + '_models_cltk'
        rel_path = os.path.join(get_cltk_data_dir(),
                                self.language,
                                'model',
                                models,
                                'semantics',
                                filename)
        path = os.path.expanduser(rel_path)
        logger.info('Loading lemmata or synonyms. This may take a minute.')
        loader = importlib.machinery.SourceFileLoader(filename, path)
        module = types.ModuleType(loader.name)
        loader.exec_module(module)
        return module.DICTIONARY

    def lookup(self, tokens):
        """Return a list of possible lemmata and their probabilities for each token"""
        lemmatized_tokens = []
        if type(tokens) == list:
            for token in tokens:
                # look for token in lemma dict keys
                if token.lower() in self.lemmata.keys():
                    # `lemmas` is a list of possible lemmata. Probability values must be assigned.
                    # `lemmalist` is a list of the form [(LEMMA, PROBABILITY), (LEMMA, PROBABILITY)]
                    # `lemmaobj` is a tuple with the form (LEMMA, LIST)
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
        if type(tokens) == str:
            if tokens.lower() in self.lemmata.keys():
                # `lemmas` is a list of possible lemmata. Probability values must be assigned.
                # `lemmalist` is a list of the form [(LEMMA, PROBABILITY), (LEMMA, PROBABILITY)]
                # `lemmaobj` is a tuple with the form (LEMMA, LIST)
                lemmas = self.lemmata[tokens.lower()]
                lemmalist = []
                for lemma in lemmas:
                    lemmalist.append((lemma, 1/len(lemmas)))
                lemmaobj = (tokens, lemmalist)
            else:
            # if token not found in lemma-headword list, return the token itself
                lemmalist = []
                lemmalist.append((tokens, 1))
                lemmaobj = (tokens, lemmalist)
            lemmatized_tokens.append(lemmaobj)
        return lemmatized_tokens

    @staticmethod
    def isolate(obj):
        """Feed a standard semantic object in and receive a simple list of
        lemmata
        """
        answers = []
        for token in obj:
            lemmata = token[1]
            for pair in lemmata:
                answers.append(pair[0])
        return answers

class Synonyms(Lemmata):
    """This sub-class is used to lookup syonyms or translations for a list of lemmata. 
    Because the synonym and translation dictionaries are keyed by lemma, not inflected word-form,
    it is necessary to lemmatize first. This class takes a dictionary variable (translation, synonym) 
    and a language variable (latin, greek). 
    """

    def __init__(self, *args, **kwargs):
        """Setup class."""
        super().__init__(*args, **kwargs)
        self.synonyms = self.load_replacement_patterns()

    def lookup_synonyms(self, lems):
        """Requires a list of lemmata, not tokens. Feed tokens through a
        Lemmata object's lookup() and isolate() methods first.
        """
        final_synonyms = []
        if type(lems) == list:
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
        if type(lems) == str:
            if lems.lower() in self.synonyms.keys():
                syns = self.synonyms[lems.lower()]
                synlist = []
                for syn in syns:
                    synlist.append((syn, 1/len(syns)))
                synobj = (lems, synlist)
                final_synonyms.append(synobj)
            else:
                pass
        return final_synonyms
