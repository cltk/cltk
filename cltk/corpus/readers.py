"""`reader.py` - Corpus reader utility objects."""
import os
import codecs
import logging
from typing import List, Dict, Tuple

from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader import PlaintextCorpusReader
from cltk.prosody.latin.string_utils import flatten

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


def assemble_corpus(corpus_reader: CorpusReader,
                    types_requested: List[str],
                    type_dirs: Dict[str, List[str]] = None,
                    type_files: Dict[str, List[str]] = None) -> Tuple[CorpusReader, List[str], List[str]]:
    """
    Create a filtered corpus.
    :param corpus_reader: This get mutated
    :param types_requested: a list of string types, which are to be found in the type_dirs and
    type_files mappings
    :param type_dirs: a dict of corpus types to directories
    :param type_files: a dict of corpus types to files
    :return: a corpusreader object containing only the mappings desired
    """
    fileid_names = []  # type: List[str]
    categories = []  # type: List[str]
    try:
        ALL_FILE_IDS = list(corpus_reader.fileids())
        CLEAN_IDS_TYPES = [] # type: List[Tuple[str, str]]
        if type_files:
            for key, valuelist in type_files.items():
                if key in types_requested:
                    for value in valuelist:
                        if value in ALL_FILE_IDS:
                            if key:
                                CLEAN_IDS_TYPES.append((value, key))
        if type_dirs:
            for key, valuelist in type_dirs.items():
                if key in types_requested:
                    for value in valuelist:
                        corrected_dir = value.replace('./', '')
                        corrected_dir = '{}/'.format(corrected_dir)
                        for name in ALL_FILE_IDS:
                            if name and name.startswith(corrected_dir):
                                CLEAN_IDS_TYPES.append((name, key))
        CLEAN_IDS_TYPES.sort(key=lambda x: x[0])
        fileid_names, categories = zip(*CLEAN_IDS_TYPES)
        corpus_reader._fileids = fileid_names
    except Exception:
        LOG.exception('failure in corpus building')

    return corpus_reader, fileid_names, categories


class FilteredPlaintextCorpusReader(PlaintextCorpusReader, CorpusReader):
    """
    A corpus reader for plain text documents with simple filtration for streamlined pipeline use.
    A list keywords may be provided, and if any of these keywords are found in a document's
    paragraph, that whole paragraph will be skipped.
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

    def words(self, fileids=None):
        """
        Provide the words of the corpus; skipping any paragraphs flagged by keywords to the main
        class constructor
        :param fileids:
        :return: words, including punctuation, one by one
        """
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

    def paras(self, fileids=None):
        for para in super().paras(fileids):
            flat_para = flatten(para)
            skip = False
            if self.skip_keywords:
                for keyword in self.skip_keywords:
                    if keyword in flat_para:
                        skip = True
            if not skip:
                yield para

    def sents(self, fileids=None):
        for sent in super().sents(fileids):
            skip = False
            if self.skip_keywords:
                for keyword in self.skip_keywords:
                    if keyword in sent:
                        skip = True
            if not skip:
                yield sent

    def docs(self, fileids=None):
        """
        Returns the complete text of an Text document, closing the document
        after we are done reading it and yielding it in a memory safe fashion.
        """

        # Create a generator, loading one document into memory at a time.
        for path, encoding in self.abspaths(fileids, include_encoding=True):
            with codecs.open(path, 'r', encoding=encoding) as f:
                if self.skip_keywords:
                    tmp_data = []
                    skip = False
                    for line in f:
                        for keyword in self.skip_keywords:
                            if keyword in line:
                                skip = True
                        if not skip:
                            tmp_data.append(line)
                    yield ''.join(tmp_data)
                else:
                    yield f.read()

    def sizes(self, fileids=None):
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
