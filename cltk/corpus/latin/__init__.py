# CLTK: Latin Corpus Readers

__author__ = 'Patrick J. Burns <patrick@diyclassics.org>'
__license__ = 'MIT License. See LICENSE.'

"""
CLTK Latin corpus readers
"""
import os.path
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

# Would like to have this search through a CLTK_DATA environment variable
# Better to use something like make_cltk_path in cltk.utils.file_operations?
home = os.path.expanduser('~')
cltk_path = os.path.join(home, 'CLTK_DATA')

# Latin Library
try:
    latinlibrary = PlaintextCorpusReader(cltk_path + '/latin/text/latin_text_latin_library', '.*\.txt', encoding='utf-8')
    pass
except IOError as e:
    print("Corpus not found. Please check that the Latin Library is installed in CLTK_DATA.")
