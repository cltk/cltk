"""
CLTK: Latin Corpus Readers
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>', 'Todd Cook <todd.g.cook@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import os
import os.path
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.corpus.reader import PlaintextCorpusReader
from cltk.corpus.readers import FilteredPlaintextCorpusReader

from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer

# Would like to have this search through a CLTK_DATA environment variable
# Better to use something like make_cltk_path in cltk.utils.file_operations?
home = os.path.expanduser('~')
cltk_path = os.path.join(home, 'cltk_data')
if not os.path.isdir(cltk_path):
    os.makedirs(cltk_path)

word_tokenizer = WordTokenizer('latin')

if os.path.exists(cltk_path + 'latin/model/latin_models_cltk/tokenizers/sentence'):
    sent_tokenizer = TokenizeSentence('latin')
else:
    punkt_param = PunktParameters()
    abbreviations = ['c', 'l', 'm', 'p', 'q', 't', 'ti', 'sex', 'a', 'd', 'cn', 'sp', "m'", 'ser',
                     'ap', 'n', 'v', 'k', 'mam', 'post', 'f', 'oct', 'opet', 'paul', 'pro', 'sert',
                     'st', 'sta', 'v', 'vol', 'vop']
    punkt_param.abbrev_types = set(abbreviations)
    sent_tokenizer = PunktSentenceTokenizer(punkt_param)

# Latin Library
try:
    latinlibrary = PlaintextCorpusReader(cltk_path + '/latin/text/latin_text_latin_library',
                                         '.*\.txt',
                                         word_tokenizer=word_tokenizer,
                                         sent_tokenizer=sent_tokenizer,
                                         encoding='utf-8')
    pass
except IOError as e:
    pass
    # print("Corpus not found. Please check that the Latin Library is installed in CLTK_DATA.")

SUPPORTED_CORPORA = frozenset(['latin_text_latin_library'])

# TODO support 'latin_text_perseus'
# stretch goal: support:
# >>> corpus_importer.list_corpora
# ['latin_text_perseus', 'latin_treebank_perseus', 'latin_text_latin_library', 'phi5', 'phi7', 'latin_proper_names_cltk', 'latin_models_cltk', 'latin_pos_lemmata_cltk', 'latin_treebank_index_thomisticus', 'latin_lexica_perseus', 'latin_training_set_sentence_cltk', 'latin_word2vec_cltk', 'latin_text_antique_digiliblt', 'latin_text_corpus_grammaticorum_latinorum', 'latin_text_poeti_ditalia']


def get_corpus_reader(corpus_name: str):
    """
    Corpus reader factory method
    :param corpus_name: the name of the supported corpus, available as: [package].SUPPORTED_CORPORA
    :return: NLTK compatible corpus reader
    """
    if corpus_name not in SUPPORTED_CORPORA:
        raise ValueError('Requested corpus: %s not supported.' % corpus_name)

    DOC_PATTERN = r'.*\.txt'
    BASE = '~/cltk_data/latin/text'
    sentence_tokenizer = TokenizeSentence('latin')
    the_word_tokenizer = WordTokenizer('latin')
    root = os.path.join(os.path.expanduser(BASE), corpus_name)

    if not os.path.exists(root):
        raise ValueError('Specified corpus %s data not found, please install' % corpus_name)

    if corpus_name == 'latin_text_latin_library':
        skip_keywords = ['Latin', 'Library']
        return FilteredPlaintextCorpusReader(root=root, fileids=DOC_PATTERN,
                                             sent_tokenizer=sentence_tokenizer,
                                             word_tokenizer=the_word_tokenizer,
                                             skip_keywords=skip_keywords)

    if corpus_name == 'latin_text_perseus':
        pass
