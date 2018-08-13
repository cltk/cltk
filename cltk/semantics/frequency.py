'''Scan the entire Tesserae corpus of Latin and build frequency data
for each possible lemma in the corpus. This results in a simple, unsupervised language model
of frequency data. The model is useful for lemmatization (see frequency.py),
as well as generating probability values for synonyms and translations. The module does not 
require training data, and lemma counting proceeds in an unsupervised manner.
Contributors: James Gawley.
'''

from os import listdir, chdir
from os.path import isfile, join, expanduser
from cltk.tokenize.word import WordTokenizer
from cltk.stem.latin.j_v import JVReplacer
from tesserae.utils import TessFile
from cltk.semantics.latin.lookup import Lemmata
from cltk.utils.file_operations import open_pickle
import pickle

#This filepath needs to be customized. The git repo is located at https://github.com/jeffkinnison/tesserae-v5.git
rel_path = join('~/tesserae-v5')
path = expanduser(rel_path)
chdir(path)
from tesserae.utils import TessFile
from tesserae.utils import TessFile



#Global objects
lemmatizer = Lemmata(dictionary = 'lemmata', language = 'latin')
jv = JVReplacer()
word_tokenizer = WordTokenizer('latin')
COUNT_LIBRARY = dict()

def read_files_count(filepath):
    '''Reads the corpus and builds the COUNT_LIBRARY dictionary object by calling
    the countgram() method on individual tokens. 
    Dependencies
    ------------
    TessFile class from tesserae.utils
    Lemmata class from cltk.semantics.latin.lookup
    JVReplacer class from cltk.stem.latin.j_v
    WordTokenizer class from cltk.tokenize.word
    Parameters
    ----------
    filepath: a file in .tess format
    Results
    -------
    Updates COUNT_LIBRARY
    Returns
    -------
    none'''
    tessobj = TessFile(filepath)
    tokengenerator = iter(tessobj.read_tokens())
    stop = 0
    while stop != 1:
        try:
            rawtoken = next(tokengenerator)
            cleantoken_list = token_cleanup(rawtoken) 
            token = cleantoken_list[0]
            countgram(token)
        except StopIteration:
            stop = 1

def token_cleanup(rawtoken):
    '''Standardize tokens by replaceing j with i and v with u, and
    split into multiple tokens as needed with tokenize() method of word_tokenizer class
    parameters
    ----------
    rawtoken: the token as drawn from the text
    return
    ------
    tokenlist: a list of possible word or punctuation tokens
    '''
    rawtoken = jv.replace(rawtoken)
    rawtoken = rawtoken.lower()
    tokenlist = word_tokenizer.tokenize(rawtoken)
    #sometimes words are split into enclitics and punctuation.
    return tokenlist



#open all the tesserae files
relativepath = join('~/cleantess/tesserae/texts/la')
path = expanduser(relativepath)
onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and 'augustine' not in f and 'ambrose' not in f and 'jerome' not in f and 'tertullian' not in f and 'eugippius' not in f and 'hilary' not in f]
onlyfiles = [join(path, f) for f in onlyfiles]
for filename in onlyfiles:
    print(filename)
    if '.tess' in filename:
        read_files(filename)

def save_pickle(filename):
    '''Saves the COUNT_LIBRARY object for later reuse.
    dependencies
    ------------
    os package
    parameters
    ----------
    filename: name for the pickle file'''
    relativepath = join('~/latin_lemma_disambiguation_models')
    os.path = expanduser(relativepath)
    pickle_file = join(path, filename)
    pickle.dump( COUNT_LIBRARY, open( pickle_file, "wb" ) )