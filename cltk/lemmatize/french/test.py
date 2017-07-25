#encoding: utf-8

text = "En Bretaigne jadis maneient " \
       "dui chevalier ; veisin esteient. " \
       "Riche hume furent e manant, " \
       "e chevalier pru e vaillant. " \
       "Prochein furent, d’une cuntree. " \
       "Chescuns femme aveit espusee. " \
       "L’une des dames enceinta. " \
       "Al terme qu’ele delivra, " \
       "a cele feiz ot dous enfanz. " \
       "Sis sire en est liez e joianz. " \
       "Pur la joie que il en a, " \
       "a sun bon veisin le manda, " \
       "que sa femme a dous fiz eüz, " \
       "de tanz enfanz esteit creüz ; " \
       "l’un li trametra a lever, " \
       "de sun nun le face nomer. "

lemmas = "en Bretaigne jadis manoir" \
         "deus chevalier ; veisin estre." \
         "Riche hume estre e manant" \
         "e chevalier PRU e vaillant" \
         "prochain estre de un contree(OOD)." \
         "Chascun (OOD) femme avoir espuser" \
         "le un de le dame enceinter ." \
         "a le terme que el delivrer ," \
         "a celui faire avoir deus enfant." \
         "son sire en estre lié e joiant ." \
         "Por le joie que il en avoir" \
         "a son bon voisin le mander ," \
         "que son femme avoir deus fil avoir ," \
         "de tant enfant estre creuz ;" \
         "le un li trametre a lever , " \
         "de son nom le faire nomer"


from cltk.lemmatize.french.backoff_test import DefaultLemmatizer
from cltk.lemmatize.french.backoff_test import DictLemmatizer
from cltk.tokenize.word import WordTokenizer

text = text.lower()

lemmatizer = DefaultLemmatizer()

tokenizer = WordTokenizer('french')
tokens = tokenizer.tokenize(text)

a = lemmatizer.lemmatize(tokens)

print(a)


from cltk.lemmatize.french.lex import entries

lemmatized_tokens = []

for token in tokens:
    for lemma, entry in entries:
        if token == lemma:
            lemmatized = (token, lemma)
            lemmatized_tokens.append(lemmatized)
            break
      #  if token != lemma:
       #     lemmatized = (token, 'None')
        #    lemmatized_tokens.append(lemmatized)
        #    break
print(lemmatized_tokens)



