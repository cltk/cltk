"""Build a sentence tokenizer for a language. Latin below.
Some guidance available here: http://wiki.apertium.org/wiki/Sentence_segmenting
"""

import nltk
import os
import pickle

def train_from_file(training_file):
    #PunktLanguageVars
    language_punkt_vars = nltk.tokenize.punkt.PunktLanguageVars
    language_punkt_vars.sent_end_chars=('.', '?', ';', ':')
    #PunktTrainer
    language_punkt_vars.internal_punctuation = ','
    with open(training_file) as f:
        train_data = f.read()
    #build trainer
    trainer = nltk.tokenize.punkt.PunktTrainer(train_data, language_punkt_vars)
    with open('latin.pickle', 'wb') as f:
        pickle.dump(trainer, f)

def tokenize_sentences(input_file, output_file=None):
    default_cltk_data = '~/cltk_data'
    cltk_data = os.path.expanduser(default_cltk_data)
    compile_cltk_lat_sent_data = os.path.join(cltk_data, 'compiled', 'sentence_tokens_latin/')
    pickle_name = 'latin.pickle'
    pickle_path = compile_cltk_lat_sent_data + pickle_name
    #open pickle file, which is actually a class of trained rule class
    with open(pickle_path, 'rb') as f:
        train_data = pickle.load(f)
    train_data.INCLUDE_ALL_COLLOCS = True
    train_data.INCLUDE_ABBREV_COLLOCS = True
    params = train_data.get_params()
    sbd = nltk.tokenize.punkt.PunktSentenceTokenizer(params)
    with open(input_file) as f:
        to_be_tokenized = f.read()
    tokenenized_sentences = []
    for sentence in sbd.sentences_from_text(to_be_tokenized, realign_boundaries=True):
        tokenenized_sentences.append(sentence)
    if output_file:
        with open(output_file, 'w') as f:
            f.write(str(tokenenized_sentences))
    else:
        return tokenenized_sentences

def tokenize_sentences_from_str(to_be_tokenized, output_file=None):
    default_cltk_data = '~/cltk_data'
    cltk_data = os.path.expanduser(default_cltk_data)
    compile_cltk_lat_sent_data = os.path.join(cltk_data, 'compiled', 'sentence_tokens_latin/')
    pickle_name = 'latin.pickle'
    pickle_path = compile_cltk_lat_sent_data + pickle_name
    #open pickle file, which is actually a class of trained rule class
    with open(pickle_path, 'rb') as f:
        train_data = pickle.load(f)
    train_data.INCLUDE_ALL_COLLOCS = True
    train_data.INCLUDE_ABBREV_COLLOCS = True
    params = train_data.get_params()
    sbd = nltk.tokenize.punkt.PunktSentenceTokenizer(params)
    '''
    with open(input_file) as f:
        to_be_tokenized = f.read()
    '''
    tokenenized_sentences = []
    for sentence in sbd.sentences_from_text(to_be_tokenized, realign_boundaries=True):
        tokenenized_sentences.append(sentence)
    if output_file:
        with open(output_file, 'w') as f:
            f.write(str(tokenenized_sentences))
    else:
        return tokenenized_sentences

#temporary for debugging
def main():
    input_file = 'transform/cat1.txt'
    tokenize_sentences(input_file)

if __name__ == '__main__':
    main()