#encoding: utf8

from cltk.corpus.utils.importer import CorpusImporter
from nltk.tokenize.punkt import PunktLanguageVars
from cltk.tokenize.word import WordTokenizer

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

def tag_ner_fr(input_text, output_type=list):

    NER_DICT = {'french': 'named_entities.txt'}
    entities = NER_DICT

    word_tokenizer = WordTokenizer('french')
    tokenized_text = word_tokenizer.tokenize(input_text)
    ner_tuple_list = []

    match = False
    for word in tokenized_text:
        for name, kind in entities:
            if word == name:
                named_things = ([(name, 'entity', kind)])
                ner_tuple_list.append(named_things)
                match = True
                break
        else:
            ner_tuple_list.append((word,))
    return(ner_tuple_list)