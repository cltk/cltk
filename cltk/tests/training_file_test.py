from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktTrainer
import pickle


def train_from_file(training_file):
    """Make a ruleset from a file."""
    language_punkt_vars = PunktLanguageVars
    language_punkt_vars.sent_end_chars = ('.', '?', '!')
    language_punkt_vars.internal_punctuation = (',', ';')
    with open(training_file) as opened_training_file:
        train_data = opened_training_file.read()
    trainer = PunktTrainer(train_data, language_punkt_vars)
    with open('french.pickle', 'wb') as open_pickle_file:
        pickle.dump(trainer, open_pickle_file)

def main():
    """For debugging."""
    training_file = 'training_sentences.txt'
    train_from_file(training_file)

if __name__ == '__main__':
    main()