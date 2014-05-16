"""Build a sentence tokenizer for a language. Latin below.
Some guidance available here: http://wiki.apertium.org/wiki/Sentence_segmenting
"""

import nltk
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

def tokenize_sentences(input_file):
    with open('latin.pickle', 'rb') as f:
        train_data = pickle.load(f)
    '''
    language_punkt_vars = nltk.tokenize.punkt.PunktLanguageVars
    trainer = nltk.tokenize.punkt.PunktTrainer(train_data, language_punkt_vars)
    params = trainer.get_params()
    '''
    #trainer = nltk.tokenize.punkt.PunktTrainer(train_data)
    train_data.INCLUDE_ALL_COLLOCS = True
    train_data.INCLUDE_ABBREV_COLLOCS = True
    params = train_data.get_params()
    sbd = nltk.tokenize.punkt.PunktSentenceTokenizer(params)
    #print(sbd)
    with open(input_file) as f:
        to_be_tokenized = f.read()
    tokenenized_sentences = []
    for sentence in sbd.sentences_from_text(to_be_tokenized, realign_boundaries=True):
        tokenenized_sentences.append(sentence)
    file_output_name = 'sentences_tokenized_' + input_file
    with open('tokenized_output.txt', 'w') as f:
        f.write(str(tokenenized_sentences))
    print(tokenenized_sentences)

#temporary for debugging
def main():
    input_file = 'transform/cat1.txt'
    tokenize_sentences(input_file)

if __name__ == '__main__':
    main()