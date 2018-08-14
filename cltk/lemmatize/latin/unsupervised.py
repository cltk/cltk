'''Scan the entire Tesserae corpus of Latin and build frequency data
for each possible lemma in the corpus. This results in a simple, unsupervised language model
of frequency data. Use the unsupervised language model created by lemma_frequency.py in order to lemmatize
Latin words. Picking the most common lemma, as in this module tests out at > 90% accurate.
Contributors: James Gawley, Jeff Kinnison.
'''

from os import listdir, chdir
from os.path import isfile, join, expanduser
from cltk.tokenize.word import WordTokenizer
from cltk.stem.latin.j_v import JVReplacer
from cltk.semantics.latin.lookup import Lemmata
from cltk.utils.file_operations import open_pickle
import pickle

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
relativepath = join('~', 'cltk_data',
                    'latin', 'text',
                    'latin_text_tesserae_collection')
path = expanduser(relativepath)
onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and 'augustine' not in f and 'ambrose' not in f and 'jerome' not in f and 'tertullian' not in f and 'eugippius' not in f and 'hilary' not in f]
onlyfiles = [join(path, f) for f in onlyfiles]
for filename in onlyfiles:
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

class TessFile(object):
    """Buffered/non-buffered reader for .tess file I/O.

    Parameters
    ----------
    path : str
        Path to the .tess file.
    mode : str
        File open mode ('r', 'w', 'a', etc.)
    buffer : bool
        If True, load file contents into memory on-the-fly. Otherwise, load in
        contents on initialization.

    Attributes
    ----------
    path : str
        Path to the .tess file.
    mode : str
        File open mode ('r', 'w', 'a', etc.)
    buffer : bool
        If True, load file contents into memory on-the-fly. Otherwise, load in
        contents on initialization.
    hash : str
        MD5 hash of the file.


    """
    def __init__(self, path, mode='r', buffer=True, validate=False):
        self.path = path
        self.mode = mode
        self.buffer = buffer
        self.fname = os.path.basename(path)

        if buffer:
            self.file = open(path, 'r')
        else:
            self.file = []
            with open(path, 'r') as f:
                for line in f.readlines():
                    self.file.append(line)

        self.__hash = None
        self.__len = None

        if validate:
            self.validate()

    def __getitem__(self, index):
        if index < 0 or index >= len(self):
            raise IndexError()

        if self.buffer:
            self.file.seek(0)
            for _ in range(index + 1):
                line = self.file.readline()
            return line
        else:
            return self.file[index]

    def __len__(self):
        if self.__len is None:
            self.__len = sum([1 for _ in self.readlines()])
        return self.__len

    @property
    def hash(self):
        """The MD5 hash of the .tess file"""
        if self.__hash is None:
            hashinator = hashlib.md5()
            for line in self.readlines():
                hashinator.update(line.encode('utf-8'))
            self.__hash = hashinator.hexdigest()
        return self.__hash

    def readlines(self):
        """Iterate over the lines of the .tess file in order.

        Yields
        ------
        line : str
            One line of the .tess file.
        """
        if self.buffer:
            self.file.seek(0)
            for line in self.file.readlines():
                yield line
        else:
            for line in self.file:
                yield line

    def read_tokens(self, include_tag=False):
        """Iterate over the tokens of a .tess file in order.

        Parameters
        ----------
        include_tag : bool
            If True, include the starting tag with each line of the .tess file.
            Otherwise, only return the raw tokens.

        Yields
        ------
        token : str
            One token of the .tess file.
        """
        for line in self.readlines():
            start = line.find('>') + 1 if not include_tag else 0
            line = line[start:].strip(string.whitespace)
            tokens = line.split()
            for token in tokens:
                yield token

    def validate(self):
        """Determine if this file is a valid .tess file.

        Raises
        ------
        MalformedTessFileError
            If a tag in the file does not contain the proper information.
        """
        name, ext = os.path.splitext(self.fname)

        # Ensure that the file has the .tess extension
        if ext != '.tess':
            msg = 'Bad filename {}. tess files must end in .tess'.format(
                                                                    self.fname)
            warnings.warn(msg, warning.UserWarning)

        # Get the author and title from the filename
        parts = name.split('.')
        author, title = parts[:2]

        if len(parts) > 2:
            major = int(parts[-1])
        else:
            major = 1

        minor = 1

        for i, line in enumerate(self.readlines()):
            line = line.strip(string.whitespace)
            if len(line) > 5:
                # Ensure that a line tage exists
                i += 1
                tag_end = line.find('>')
                if tag_end < 0:
                    msg = '{} may be malformed on line {}'.format(
                                                            self.fname, line)
                    warnings.warn(msg, UserWarning)

                tag = line[:tag_end + 1]
                parts = tag.split()
                tag_author, tag_title = parts[0][1:-1], parts[1][:-1]
                maj_min = parts[-1][:-1].split('.')
                if len(maj_min) == 1:
                    tag_maj = int(maj_min[0])
                    tag_min = 1
                else:
                    tag_maj = int(maj_min[0])
                    tag_min = int(maj_min[1])

                # Ensure the tag author and title match the filename
                if author.find(tag_author) < 0 or title.find(tag_title) < 0:
                    msg = '{} may be malformed on line {}'.format(
                                                            self.fname, line)
                    warnings.warn(msg, UserWarning)

                # Ensure that the major part number is incrementing correctly
                if int(tag_maj) not in [major, major + 1]:
                    msg = '{} may be malformed on line {}'.format(
                                                            self.fname, line)
                    warnings.warn(msg, UserWarning)

                # Ensure that the minor part number is incrementing corectly
                if tag_maj == major and tag_min != minor:
                    msg = '{} may be malformed on line {}'.format(
                                                            self.fname, line)
                    warnings.warn(msg, UserWarning)
                elif tag_maj == major + 1 and tag_min != 1:
                    msg = '{} may be malformed on line {}'.format(
                                                            self.fname, line)
                    warnings.warn(msg, UserWarning)

                if tag_maj == major:
                    minor += 1
                else:
                    major += 1
                    minor = 2

punctuation_list = ['!', ';', ':', '?', '-', '–', '&', '*', '(', ')', '[', ']', ',', '"', '\'']

def frequency_lemmatize(target):
    '''Use the unsupervised count of lemma frequencies generated by read_files_count()
    to assign probabilities in the case of an ambiguous lemmatization.
    parameters
    ----------
    target: a token to be lemmatized
    results
    -------
    a list of tuples of the form [(lemma, probability)]
    '''
    if target in punctuation_list:
        lemmalist = [('punc', 1)]
        return lemmalist
    if target == 'ne':
        lemmalist = [('ne', 1)]
        return lemmalist
    lemmalist = lemmatizer.lookup([target])
    lemmas = lemmatizer.isolate(lemmalist)
    if len(lemmas) > 1:
        all_lemmas_total = sum([COUNT_LIBRARY[l] for l in lemmas])
        try:
            lemmalist = [(l, (COUNT_LIBRARY[l] / all_lemmas_total)) for l in lemmas]
        except ZeroDivisionError:
            print([(COUNT_LIBRARY[l], l) for l in lemmas])
        return lemmalist
    else:
        lemmalist = []
        lemmaobj = (lemmas[0], 1)
        lemmalist.append(lemmaobj)
        return lemmalist


def test_count_library(token_list, lemma_list):
    '''Test the ability of frequency_lemmatize(), (which uses the COUNT_LIBRARY dictionary,
    to predict the most likely lemmatization in ambiguous cases. Punctuation is 
    automatically counted as correct, because the 'punc' lemmatization usage is inconsistent
    in the test corpus.
    dependencies
    ------------
    itemgetter class from operator package
    parameters
    ----------
    token_list: a list of tokens
    lemma_list: a list of corresponding 'correct' lemmatizaitons
    results
    -------
    prints four numbers: the number of correctly assigned lemmas in ambiguous cases;
    the number of ambiguous cases in total; the number of tokens analyzed; and a
    decimal between 0 and 1 representing the proportion of correct lemmatizations.
    return
    ------
    a list object containing all incorrect lemmatizations for analysis. Format:
    [(token, answer_given, correct_answer), (token...)]

    NOTE: Initial tests show roughly 91% accuracy, identification of punctuation included.
    '''
    trials = 0
    correct = 0
    errors = []
    for position in range(0, (len(token_list)-1)):
        lemmalist = frequency_lemmatize(token_list[position])
        lemma = max(lemmalist,key=itemgetter(1))
        if len(lemmalist) > 1:
            trials = trials + 1
            if lemma[0] == lemma_list[position] or lemma[0] == 'punc':
                correct = correct + 1
            else:
                errors.append((token_list[position], lemma[0], lemma_list[position]))
    print(correct)
    print(trials)
    print(len(lemma_list))
    rate = (len(lemma_list) - trials + correct) / len(lemma_list)
    print(rate)
    return errors