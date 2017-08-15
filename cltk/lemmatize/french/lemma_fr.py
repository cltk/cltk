from cltk.tokenize.word import WordTokenizer
from cltk.lemmatize.french.tobler import entries
from cltk.lemmatize.french.forms_and_lemmas import forms_and_lemmas
from cltk.stem.french.lemmas_alone import lemmas
from fuzzywuzzy import process


def lemmatize(tokens):
    lemma_list = [x[0] for x in entries]
    lemmatized = []
    for token in tokens:
        if token in lemma_list:
            lemurs = (token, token)
            lemmatized.append(lemurs)
        else:
            for token in tokens:
                lemma = [k for k, v in forms_and_lemmas.items() if token in v]
                thingy = (token, lemma)
                lemmatized.append(thingy)
    return lemmatized


