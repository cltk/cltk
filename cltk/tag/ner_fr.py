#encoding: utf8

from cltk.corpus.utils.importer import CorpusImporter
from nltk.tokenize.punkt import PunktLanguageVars
from cltk.tokenize.word import WordTokenizer
from cltk.tag.named_entities_fr import entities

#tags named entities in a string and outputs a list of tuples in the following format:
# (name, "entity", kind_of_entity)
def tag_ner_fr(input_text, output_type=list):

    for entity in entities:
        (name, kind) = entity

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
    return ner_tuple_list



