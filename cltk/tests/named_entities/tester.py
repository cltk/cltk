#encoding: utf8

#from cltk.corpus.utils.importer import CorpusImporter
#from nltk.tokenize.punkt import PunktLanguageVars
#from cltk.tokenize.word import WordTokenizer
#import os



entities = [("Abel", "REL"),
    ("Abilant", "LOC"),
    ("Abirun", "CHI"),
    ("Abisme", "CHI"),
    ("Abraham", "REL"),
    ("Absalon", "REL"),
    ("Acelin", "CHI"),
    ("Acenssion", "FEST"),
    ("Achilles", "CLAS"),
    ("Acre", "LOC")]

d = dict(entities)
print(d["Acre"])
#for entity in entities:
 #   (name, type) = entity

text = "Abel alla à Abirun et Abisme et Acre pour la fête de l' Acenssion"

named_entities = ([x[0] for x in entities])
#ne_type = ([x[1] for x in entities])

tokenized_text = str.split(text)

for word in tokenized_text:
   # for name in entities:
        if word== name in named_entities:
            print([(word, "entity", type)])
        if word in entities:
            print(entities)



#if type(input_text) == str:
#    punkt = PunktLanguageVars()
#    tokens = punkt.word_tokenize(input_text)
#    new_tokens = []
#    for word in tokens:
#        if word.endswith('.'):
#            new_tokens.append(word[:-1])
#            new_tokens.append('.')
#        else:
#            new_tokens.append(word)
#    input_text = new_tokens

#ner_tuple_list = []

#for count, word_token in enumerate(input_text):
#    match = False
#    for tuple in entities:
#        if word_token==[x[0] for x in entities]:
#            ner_tuple = (word_token, [x[1] for x in entities])
 #           ner_tuple_list.append(ner_tuple)
  #          match = True
   #         break
    #    if not match:
     #       ner_tuple_list.append((word_token,))

#print(ner_tuple_list)


