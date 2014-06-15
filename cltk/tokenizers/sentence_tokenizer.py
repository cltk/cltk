"""Build a sentence tokenizer for a language. Latin below.
Some guidance available here: http://wiki.apertium.org/wiki/Sentence_segmenting
"""

from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize.punkt import PunktTrainer
import os
import pickle

cltk_data_dir = '~/cltk_data'
cltk_data = os.path.expanduser(cltk_data_dir)

def train_latin_from_file():
    """Open a training set file and write a Latin pickle trainer"""
    training_file = 'training_sentences.txt'
    training_path = os.path.join(cltk_data, 'compiled', 'sentence_tokens_latin/', training_file)
    with open(training_path, 'r') as f:
        train_data = f.read()
    language_vars = PunktLanguageVars
    language_vars.sent_end_chars=('.', '?', ';', ':')
    language_vars.internal_punctuation = ','
    trainer = PunktTrainer(train_data, language_vars)

    with open('latin.pickle', 'wb') as f:
        pickle.dump(trainer, f)

def tokenize_sents_latin(sentences_string):
    """Tokenize a Latin string into sentences"""
    pickle_name = 'latin.pickle'
    pickle_path = os.path.join(cltk_data, 'compiled', 'sentence_tokens_latin/', pickle_name)
    with open(pickle_path, 'rb') as f:
        train_data = pickle.load(f)
    train_data.INCLUDE_ALL_COLLOCS = True
    train_data.INCLUDE_ABBREV_COLLOCS = True
    params = train_data.get_params()
    sbd = PunktSentenceTokenizer(params)
    tokenenized_sentences = []
    for sentence in sbd.sentences_from_text(sentences_string, realign_boundaries=True):
        tokenenized_sentences.append(sentence)
    print(tokenenized_sentences)
    return tokenenized_sentences

def train_and_tokenize_latin(sentences_string_input):
    train_latin_from_file()
    tokenize_sents_latin(sentences_string_input)
