"""Readers for Latin language corpora"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

import os.path

from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.data import LazyLoader

from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from cltk.utils.cltk_logger import logger
from cltk.corpus.utils.importer import CorpusImporter


# Set up models
home = os.path.expanduser('~')
cltk_path = os.path.join(home, 'cltk_data')
corpus_directory = cltk_path + '/latin/text/latin_text_latin_library'

word_tokenizer = WordTokenizer('latin')

# Prepare sentence tokenizer
# Incorporate way to fall back to NLTK English sentence tokenizer?
def get_latin_sent_tokenizer():
    """
    Function that gets Latin sentence tokenizer
    """
    try:
        latin_sent_tokenizer = TokenizeSentence('latin')
        #logger.debug("Loaded the NLTK's PlaintextCorpusReader.")
    except (IOError, AssertionError) as io_err:
        logger.error("Couldn't find Latin models. Please import.")
        print("Latin model needs to be installed to use this tokenizer. Please import and try again.")
        install = input('Latin model not found. Import? [Y/n] ')
        install = install.lower()
        if install == 'y':
            corpus_importer = CorpusImporter('latin')
            corpus_importer.import_corpus('latin_models_cltk')
            # now try again
            latin_sent_tokenizer = TokenizeSentence('latin')
        else:
            # Incorporate fallback tokenizer?
            logger.error(io_err)
            raise
    return latin_sent_tokenizer    

sent_tokenizer = get_latin_sent_tokenizer() # pragma: no cover


# Load Latin Library corpus
def get_latin_library():
    """
    Function that gets Latin Library
    """
    try:
#        latin_library_reader = PlaintextCorpusReader(corpus_directory, '.*\.txt', word_tokenizer=word_tokenizer, encoding='utf-8')
        latin_library_reader = PlaintextCorpusReader(corpus_directory, '.*\.txt', sent_tokenizer=sent_tokenizer, word_tokenizer=word_tokenizer, encoding='utf-8')
        logger.debug("Loaded the NLTK's PlaintextCorpusReader.")
    except IOError as io_err:
        logger.error("Couldn't find Latin Library. Please import.")
        print("Latin Library corpus needs to be installed to use this reader. Please import and try again.")
        install = input('Latin Library not found. Import? [Y/n] ')
        install = install.lower()
        if install == 'y':
            corpus_importer = CorpusImporter('latin')
            corpus_importer.import_corpus('latin_text_latin_library')
            # now try again
#            latin_library_reader = PlaintextCorpusReader(corpus_directory, '.*\.txt', word_tokenizer=word_tokenizer, encoding='utf-8')
            latin_library_reader = PlaintextCorpusReader(corpus_directory, '.*\.txt', sent_tokenizer=sent_tokenizer, word_tokenizer=word_tokenizer, encoding='utf-8')
        else:
            logger.error(io_err)
            raise
    return latin_library_reader    

latinlibrary = get_latin_library() # pragma: no cover


if __name__ == '__main__':
    print(latinlibrary.fileids()[:3])
    print(latinlibrary.raw()[:1000])
    print(latinlibrary.sents())
    print(latinlibrary.words())
