

from cltk.tokenize.word import WordTokenizer
from cltk.lemmatize.french.tobler import entries
from cltk.lemmatize.french.forms_and_lemmas import forms_and_lemmas
from cltk.stem.french.lemmas_alone import lemmas
from fuzzywuzzy import process


def forms_lemmatizer(tokens):
    lemma_list = [x[0] for x in entries]
    lemmatized = []
    for token in tokens:
        if token in lemma_list:
            lemurs = (token, token)
            lemmatized.append(lemurs)
        else:
            lemurs = (token, "no lemma")
            lemmatized.append(lemurs)
    return lemmatized


text = "Puis que ma dame de Chanpaigne Vialt que romans a feire anpraigne, Je l’anprendrai mout volentiers, Come cil qui est suens antiers De quanqu’il puet el monde feire, Sanz rien de losange avant treire."

text = str.lower(text)
tokenizer = WordTokenizer('french')
tokens = tokenizer.tokenize(text)
#print(forms_lemmatizer(tokens))



#lemmars = [x[0] for x in forms_and_lemmas]
#forms = [x[1] for x in forms_and_lemmas]


for token in tokens:
    lemma = [k for k,v in forms_and_lemmas.items() if token in v]
return((token, lemma))




