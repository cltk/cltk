"""`reader.py` - Corpus reader utility objects."""
import json
import os
import re
import codecs
import time

import logging
from typing import List, Dict, Tuple, Set, Any, Generator

from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader import PlaintextCorpusReader
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize  # Replace with CLTK
from nltk import pos_tag  # Replace with CLTK

from cltk.prosody.latin.string_utils import flatten
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

# TODO add your corpus here:
SUPPORTED_CORPORA = {
    'latin': ['latin_text_latin_library',
              'latin_text_perseus',
              'latin_text_tesserae',
              ],
    'greek': ['greek_text_perseus',
              'greek_text_tesserae',
              ]
}  # type: Dict[str, List[str]]


def get_corpus_reader(corpus_name: str = None, language: str = None) -> CorpusReader:
    """
    Corpus reader factory method
    :param corpus_name: the name of the supported corpus, available as: [package].SUPPORTED_CORPORA
    :param langugage: the language for search in
    :return: NLTK compatible corpus reader
    """
    BASE = get_cltk_data_dir() + '/{}/text'.format(language)
    root = os.path.join(os.path.expanduser(BASE), corpus_name)

    if not os.path.exists(root) or corpus_name not in SUPPORTED_CORPORA.get(language):
        raise ValueError(
            'Specified corpus data not found, please install {} for language: {}'.format(
                corpus_name, language))

    sentence_tokenizer = TokenizeSentence(language)
    the_word_tokenizer = WordTokenizer(language)
    doc_pattern = r'.*\.txt'  #: Generic file ending, override below in your own CorpusReader implementation

    if language == 'latin':
        if corpus_name == 'latin_text_latin_library':
            skip_keywords = ['Latin', 'Library']
            return FilteredPlaintextCorpusReader(root=root, fileids=doc_pattern,
                                                 sent_tokenizer=sentence_tokenizer,
                                                 word_tokenizer=the_word_tokenizer,
                                                 skip_keywords=skip_keywords)
        if corpus_name == 'latin_text_perseus':
            valid_json_root = os.path.join(root, 'cltk_json')  #: we only support this subsection
            return JsonfileCorpusReader(root=valid_json_root,
                                        sent_tokenizer=sentence_tokenizer,
                                        word_tokenizer=the_word_tokenizer,
                                        target_language='latin')  # perseus also contains English

        if corpus_name == 'latin_text_tesserae':
            return TesseraeCorpusReader(root=root, fileids=r'.*\.tess',
                                        sent_tokenizer=sentence_tokenizer,
                                        word_tokenizer=the_word_tokenizer,
                                        )

    if language == 'greek':
        if corpus_name == 'greek_text_perseus':
            valid_json_root = os.path.join(root, 'cltk_json')  #: we only support this subsection
            return JsonfileCorpusReader(root=valid_json_root,
                                        sent_tokenizer=sentence_tokenizer,
                                        word_tokenizer=the_word_tokenizer,
                                        target_language='grc')  #: this abbreviation is required

        if corpus_name == 'greek_text_tesserae':
            # tokenizers/taggers need to be replaced with CLTK version
            # most obv. for POS tagging!
            return TesseraeCorpusReader(root=root, fileids=r'.*\.tess',
                                        sent_tokenizer=sent_tokenize,
                                        word_tokenizer=word_tokenize,
                                        pos_tagger=pos_tag,
                                        target_language='grc')  #: this abbreviation is required

    # TODO add other languages and write tests for each corpus


def assemble_corpus(corpus_reader: CorpusReader,
                    types_requested: List[str],
                    type_dirs: Dict[str, List[str]] = None,
                    type_files: Dict[str, List[str]] = None) -> CorpusReader:
    """
    Create a filtered corpus.
    :param corpus_reader: This get mutated
    :param types_requested: a list of string types, which are to be found in the type_dirs and
    type_files mappings
    :param type_dirs: a dict of corpus types to directories
    :param type_files: a dict of corpus types to files
    :return: a CorpusReader object containing only the mappings desired
    """
    fileid_names = []  # type: List[str]
    try:
        all_file_ids = list(corpus_reader.fileids())
        clean_ids_types = []  # type: List[Tuple[str, str]]
        if type_files:
            for key, valuelist in type_files.items():
                if key in types_requested:
                    for value in valuelist:
                        if value in all_file_ids:
                            if key:
                                clean_ids_types.append((value, key))
        if type_dirs:
            for key, valuelist in type_dirs.items():
                if key in types_requested:
                    for value in valuelist:
                        corrected_dir = value.replace('./', '')
                        corrected_dir = '{}/'.format(corrected_dir)
                        for name in all_file_ids:
                            if name and name.startswith(corrected_dir):
                                clean_ids_types.append((name, key))
        clean_ids_types.sort(key=lambda x: x[0])
        fileid_names, categories = zip(*clean_ids_types)  # type: ignore
        corpus_reader._fileids = fileid_names
        return corpus_reader
    except Exception:
        LOG.exception('failure in corpus building')


class FilteredPlaintextCorpusReader(PlaintextCorpusReader, CorpusReader):
    """
    A corpus reader for plain text documents with simple filtration for streamlined pipeline use.
    A list keywords may be provided, and if any of these keywords are found in a document's
    paragraph, that whole paragraph will be skipped, same for sentences and words.
    """

    def __init__(self, root, fileids=None, encoding='utf8', skip_keywords=None,
                 **kwargs):
        """
        :param root: The file root of the corpus directory
        :param fileids: the list of file ids to consider, or wildcard expression
        :param skip_keywords: a list of words which indicate whole paragraphs that should
        be skipped by the paras and words methods()
        :param encoding: utf8
        :param kwargs: Any values to be passed to NLTK super classes, such as sent_tokenizer,
        word_tokenizer.
        """
        if not fileids:
            fileids = r'.*\.txt'

        # Initialize the NLTK corpus reader objects
        PlaintextCorpusReader.__init__(self, root, fileids, encoding)
        CorpusReader.__init__(self, root, fileids, encoding)
        if 'sent_tokenizer' in kwargs:
            self._sent_tokenizer = kwargs['sent_tokenizer']
        if 'word_tokenizer' in kwargs:
            self._word_tokenizer = kwargs['word_tokenizer']
        self.skip_keywords = skip_keywords

    def words(self, fileids=None) -> Generator[str, str, None]:
        """
        Provide the words of the corpus; skipping any paragraphs flagged by keywords to the main
        class constructor
        :param fileids:
        :return: words, including punctuation, one by one
        """
        if not fileids:
            fileids = self.fileids()
        for para in self.paras(fileids):
            flat_para = flatten(para)
            skip = False
            if self.skip_keywords:
                for keyword in self.skip_keywords:
                    if keyword in flat_para:
                        skip = True
            if not skip:
                for word in flat_para:
                    yield word

    def paras(self, fileids=None) -> Generator[str, str, None]:
        """
        Provide paragraphs, if possible
        :param fileids:
        :return: a generator of paragraphs
        """
        if not fileids:
            fileids = self.fileids()
        for para in super().paras(fileids):
            flat_para = flatten(para)
            skip = False
            if self.skip_keywords:
                for keyword in self.skip_keywords:
                    if keyword in flat_para:
                        skip = True
            if not skip:
                yield para

    def sents(self, fileids=None) -> Generator[str, str, None]:
        """
        A generator for sentences in a text, or texts
        :param fileids:
        :return: a generator of sentences
        """
        if not fileids:
            fileids = self.fileids()
        for sent in super().sents(fileids):
            skip = False
            if self.skip_keywords:
                for keyword in self.skip_keywords:
                    if keyword in sent:
                        skip = True
            if not skip:
                yield sent

    def docs(self, fileids=None) -> Generator[str, str, None]:
        """
        Returns the complete text of an Text document, closing the document
        after we are done reading it and yielding it in a memory safe fashion.
        """
        if not fileids:
            fileids = self.fileids()
        # Create a generator, loading one document into memory at a time.
        for path, encoding in self.abspaths(fileids, include_encoding=True):
            with codecs.open(path, 'r', encoding=encoding) as reader:
                if self.skip_keywords:
                    tmp_data = []
                    for line in reader:
                        skip = False
                        for keyword in self.skip_keywords:
                            if keyword in line:
                                skip = True
                        if not skip:
                            tmp_data.append(line)
                    yield ''.join(tmp_data)
                else:
                    yield reader.read()

    def sizes(self, fileids=None) -> Generator[int, int, None]:
        """
        Returns a list of tuples, the fileid and size on disk of the file.
        This function is used to detect oddly large files in the corpus.
        """
        if not fileids:
            fileids = self.fileids()
        # Create a generator, getting every path and computing filesize
        for path in self.abspaths(fileids):
            yield os.path.getsize(path)

    def __iter__(self):
        """convenience iterator for Word2Vec training."""
        for sent in self.sents():
            yield sent


class JsonfileCorpusReader(CorpusReader):
    """
    A corpus reader for Json documents where contents are stored in a dictionary.
    Supports any documents stored under a text key.
    A document may have any number of subsections as nested dictionaries, as long as their keys
    are sortable; they will be traversed and only strings datatypes will be collected as the text.
    E.g.:

    doc['text']['1'] = "some text"
    doc['text']['2'] = "more text"
    Or with one level of subsections:
    doc['text']['1']['1'] = "some text"
    doc['text']['1']['2'] = "more text"
    """

    def __init__(self, root, fileids=None, encoding='utf8', skip_keywords=None,
                 target_language=None, paragraph_separator='\n\n', **kwargs):
        """
        :param root: The file root of the corpus directory
        :param fileids: the list of file ids to consider, or wildcard expression
        :param skip_keywords: a list of words which indicate whole paragraphs that should
        be skipped by the paras and words methods()
        :param target_language: which files to select; sometimes a corpus contains English
         translations, we expect these files to be named ...english.json -- if not, pass in fileids
        :param paragraph_separator: character sequence demarcating paragraph separation
        :param encoding: utf8
        :param kwargs: Any values to be passed to NLTK super classes, such as sent_tokenizer,
        word_tokenizer.
        """

        if not target_language:
            target_language = ''
        if not fileids:
            fileids = r'.*{}\.json'.format(target_language)

        # Initialize the NLTK corpus reader objects
        CorpusReader.__init__(self, root, fileids, encoding)
        if 'sent_tokenizer' in kwargs:
            self._sent_tokenizer = kwargs['sent_tokenizer']
        if 'word_tokenizer' in kwargs:
            self._word_tokenizer = kwargs['word_tokenizer']
        self.skip_keywords = skip_keywords
        self.paragraph_separator = paragraph_separator

    def words(self, fileids=None) -> Generator[str, str, None]:
        """
        Provide the words of the corpus; skipping any paragraphs flagged by keywords to the main
        class constructor
        :param fileids:
        :return: words, including punctuation, one by one
        """
        for sentence in self.sents(fileids):
            words = self._word_tokenizer.tokenize(sentence)
            for word in words:
                yield word

    def sents(self, fileids=None) -> Generator[str, str, None]:
        """
        :param fileids:
        :return: A generator of sentences
        """
        for para in self.paras(fileids):
            sentences = self._sent_tokenizer.tokenize(para)
            for sentence in sentences:
                yield sentence

    def paras(self, fileids=None) -> Generator[str, str, None]:
        """
        Yield paragraphs of the text, as demarcated by double new lines.
        :param fileids: single document file or files of proper JSON objects with a text key,
        and section subkey
        :return: a generator of paragraphs
        """

        def _recurse_to_strings(my_dict: Dict[str, Any]) -> List[str]:
            """Internal accumulator method."""
            vals = []  # type: List[str]
            m_keys = sorted(list(my_dict.keys()))
            for mkey in m_keys:
                if isinstance(my_dict[mkey], dict):
                    vals += _recurse_to_strings(my_dict[mkey])
                else:
                    vals += [my_dict[mkey]]
            return vals

        for doc in self.docs(fileids):
            text_data = _recurse_to_strings(doc['text'])  # type: List[str]
            text_sections = []  # type: List[str]
            for text_part in text_data:
                skip = False
                if self.skip_keywords:
                    for keyword in self.skip_keywords:
                        if keyword in text_part:
                            skip = True
                if not skip:
                    text_sections.append(text_part)
            for para in text_sections:
                yield para.strip()

    def docs(self, fileids=None) -> Generator[Dict[str, Any], Dict[str, Any], None]:
        """
        Returns the complete text of an Text document, closing the document
        after we are done reading it and yielding it in a memory safe fashion.
        :return : Python Dictionary of strings or Nested Dictionaries. The top level dictionary
        also contains the filename from which it spawned.
        """
        # Create a generator, loading one document into memory at a time.
        for path, encoding in self.abspaths(fileids, include_encoding=True):
            with codecs.open(path, 'r', encoding=encoding) as reader:
                the_doc = json.loads(reader.read())
                if 'filename' not in the_doc:
                    the_doc['filename'] = path
                yield the_doc

    def sizes(self, fileids=None) -> Generator[int, int, None]:
        """
        Returns a list of tuples, the fileid and size on disk of the file.
        This function is used to detect oddly large files in the corpus.
        """
        if not fileids:
            fileids = self.fileids()
        # Create a generator, getting every path and computing filesize
        for path in self.abspaths(fileids):
            yield os.path.getsize(path)

    def __iter__(self) -> Generator[str, str, None]:
        """convenience iterator for Word2Vec training."""
        for sent in self.sents():
            yield sent


# WRITE DOCSTRING
class TesseraeCorpusReader(PlaintextCorpusReader):
    """
    """

    def __init__(self, root, fileids=None, encoding='utf8', skip_keywords=None,
                 **kwargs):
        """
        :param root: The file root of the corpus directory
        :param fileids: the list of file ids to consider, or wildcard expression
        :param skip_keywords: a list of words which indicate whole paragraphs that should
        be skipped by the paras and words methods()
        :param encoding: utf8
        :param kwargs: Any values to be passed to NLTK super classes, such as sent_tokenizer,
        word_tokenizer.
        """
        # Initialize the NLTK corpus reader objects
        PlaintextCorpusReader.__init__(self, root, fileids, encoding)
        # CorpusReader.__init__(self, root, fileids, encoding)
        if 'sent_tokenizer' in kwargs:
            self._sent_tokenizer = kwargs['sent_tokenizer']
        if 'word_tokenizer' in kwargs:
            self._word_tokenizer = kwargs['word_tokenizer']
        if 'pos_tagger' in kwargs:
            self.pos_tagger = kwargs['pos_tagger']

    def docs(self: object, fileids: str):
        """
        Returns the complete text of a .tess file, closing the document after
        we are done reading it and yielding it in a memory-safe fashion.
        """

        for path, encoding in self.abspaths(fileids, include_encoding=True):
            with codecs.open(path, 'r', encoding=encoding) as f:
                yield f.read()

    def texts(self: object, fileids: str, plaintext: bool = True):
        """
        Returns the text content of a .tess file, i.e. removing the bracketed
        citation info (e.g. "<Ach. Tat.  1.1.0>")
        """

        for doc in self.docs(fileids):
            if plaintext == True:
                doc = re.sub(r'<.+?>\s', '', doc)  # Remove citation info
            doc = doc.rstrip()  # Clean up final line breaks
            yield doc

    def paras(self: object, fileids: str):
        """
        Returns paragraphs in a .tess file, as defined by two \n characters.
        NB: Most .tess files do not have this feature; only the Homeric poems
        from what I have noticed so far. Perhaps a feature worth looking into.
        """

        for text in self.texts(fileids):
            for para in text.split('\n\n'):
                yield para

    def lines(self: object, fileids: str, plaintext: bool = True):
        """
        Tokenizes documents in the corpus by line
        """

        for text in self.texts(fileids, plaintext):
            text = re.sub(r'\n\s*\n', '\n', text, re.MULTILINE)  # Remove blank lines
            for line in text.split('\n'):
                yield line

    def sents(self: object, fileids: str):
        """
        Tokenizes documents in the corpus by sentence
        """

        for para in self.paras(fileids):
            for sent in sent_tokenize(para):
                yield sent

    def words(self: object, fileids: str):
        """
        Tokenizes documents in the corpus by word
        """
        for sent in self.sents(fileids):
            for token in word_tokenize(sent):
                yield token

    def pos_tokenize(self: object, fileids: str):
        """
        Segments, tokenizes, and POS tag a document in the corpus.
        """
        for para in self.paras(fileids):
            yield [
                self.pos_tagger(word_tokenize(sent))
                for sent in sent_tokenize(para)
            ]

    def describe(self: object, fileids: str = None):
        """
        Performs a single pass of the corpus and returns a dictionary with a
        variety of metrics concerning the state of the corpus.

        based on (Bengfort et al, 2018: 46)
        """
        started = time.time()

        # Structures to perform counting
        counts = FreqDist()
        tokens = FreqDist()

        # Perform a single pass over paragraphs, tokenize, and counts
        for para in self.paras(fileids):
            counts['paras'] += 1

            for sent in para:
                counts['sents'] += 1

                # Include POS at some point
                for word in sent:
                    counts['words'] += 1
                    tokens[word] += 1

        # Compute the number of files in the corpus
        n_fileids = len(self.fileids())

        # Return data structure with information
        return {
            'files': n_fileids,
            'paras': counts['paras'],
            'sents': counts['sents'],
            'words': counts['words'],
            'vocab': len(tokens),
            'lexdiv': round((counts['words'] / len(tokens)), 3),
            'ppdoc': round((counts['paras'] / n_fileids), 3),
            'sppar': round((counts['sents'] / counts['paras']), 3),
            'secs': round((time.time() - started), 3),
        }
