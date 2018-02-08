"""
CLTK Latin corpus readers
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'


import os.path
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

from cltk.corpus.utils.importer import CorpusImporter
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from cltk.utils.cltk_logger import logger


def get_latin_library_reader():
    # Would like to have this search through a CLTK_DATA environment variable
    # Better to use something like make_cltk_path in cltk.utils.file_operations?
    home = os.path.expanduser('~')
    cltk_path = os.path.join(home, 'cltk_data')
    #if not os.path.isdir(cltk_path):
    #    os.makedirs(cltk_path)

    word_tokenizer = WordTokenizer('latin')

    if os.path.exists(cltk_path + 'latin/model/latin_models_cltk/tokenizers/sentence'):
        sent_tokenizer = TokenizeSentence('latin')
    else:
        punkt_param = PunktParameters()
        abbreviations = ['c', 'l', 'm', 'p', 'q', 't', 'ti', 'sex', 'a', 'd', 'cn', 'sp', "m'", 'ser', 'ap', 'n', 'v', 'k', 'mam', 'post', 'f', 'oct', 'opet', 'paul', 'pro', 'sert', 'st', 'sta', 'v', 'vol', 'vop']
        punkt_param.abbrev_types = set(abbreviations)
        sent_tokenizer = PunktSentenceTokenizer(punkt_param)

    # Latin Library
    try:
        latinlibrary = PlaintextCorpusReader(cltk_path + '/latin/text/latin_text_latin_library',
                                             '.*\.txt',
                                             word_tokenizer=word_tokenizer,
                                             sent_tokenizer=sent_tokenizer,
                                             encoding='utf-8')
        logger.debug("Loaded the NLTK's PlaintextCorpusReader.")
    except IOError as io_err:
        logger.error("Couldn't find Latin Library. Please import.")
        install = input('Latin Library not found. Import? [Y/n] ')
        install = install.lower()
        if install == 'y':
            corpus_importer = CorpusImporter('latin')
            corpus_importer.import_corpus('latin_text_latin_library')
            # now try again
            latinlibrary = PlaintextCorpusReader(cltk_path + '/latin/text/latin_text_latin_library',
                                                 '.*\.txt',
                                                 word_tokenizer=word_tokenizer,
                                                 sent_tokenizer=sent_tokenizer,
                                                 encoding='utf-8')
        else:
            logger.error(io_err)
            raise
    return latinlibrary

   # try:
   #     # Necessary for Travis tests to pass?
   #     ll_path_rel = os.path.join('~/cltk_data/latin/text/latin_text_latin_library')
   #     ll_path = os.path.expanduser(ll_path_rel)
   #     latinlibrary = PlaintextCorpusReader(ll_path,
   # '.*\.txt',
   # word_tokenizer=word_tokenizer,
   # sent_tokenizer=sent_tokenizer,
   # encoding='utf-8')
   # except IOError as e:
   #     pass
       # print("Corpus not found. Please check that the Latin Library is installed in CLTK_DATA.")


if __name__ == '__main__':
    latinlibrary = get_latin_library_reader()
    print(latinlibrary.fileids()[:3])