from cltk.tokenize.word import WordTokenizer
from cltk.lemmatize.french.entries import entries
from cltk.lemmatize.french.forms_and_lemmas import forms_and_lemmas
from cltk.lemmatize.french.french import regex
import os
import importlib

__author__ = ['Natasha Voake <natashavoake@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


rel_path = os.path.join('~','cltk_data',
                                    'french',
                                    'model','greek_models_cltk',
                                    'lemmata','greek_lemmata_cltk.py')
            path = os.path.expanduser(rel_path)
            #logger.info('Loading lemmata. This may take a minute.')
            loader = importlib.machinery.SourceFileLoader('french_data_cltk', path)
        module = loader.load_module()


def lemmatize(tokens):
    """define list of lemmas"""
    lemma_list = [x[0] for x in entries]
    """Provide a lemma for each token"""
    lemmatized = []
    for token in tokens:
        """check for a match between token and list of lemmas"""
        if token in lemma_list:
            lemmed = (token, token)
            lemmatized.append(lemmed)
        else:
            """if no match check for a match between token and list of lemma forms"""
            lemma = [k for k, v in forms_and_lemmas.items() if token in v]
            if lemma != []:
                lemmed = (token, lemma)
                lemmatized.append(lemmed)
            elif lemma==[]:
                """if no match apply regular expressions and check for a match against the list of lemmas again"""
                regexed = regex(token)
                if regexed in lemma_list:
                    lemmed = (token, regexed)
                    lemmatized.append(lemmed)
                else:
                    lemmed = (token, "None")
                    lemmatized.append(lemmed)
    return lemmatized
