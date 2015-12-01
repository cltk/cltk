"""Search CLTK corpora with Whoosh, a Python-language index."""

import os
import time

from cltk.corpus.greek.tlg.id_author import ID_AUTHOR as tlg_author_map
from cltk.corpus.latin.phi5_index import PHI5_INDEX as phi5_author_map
from cltk.utils.cltk_logger import logger
from whoosh.fields import ID
from whoosh.fields import Schema
from whoosh.fields import TEXT
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


class CLTKIndex:
    """Functions sharing the state of an index to be made or already created."""
    def __init__(self, lang, corpus, chunk='author'):
        self.lang = lang
        self.corpus = corpus
        self.chunk = chunk
        chunks = ['author', 'work']
        assert self.chunk in chunks, 'Chunk must be one of the following: {}.'.format(chunks)

        self.index_dir_base = os.path.expanduser('~/cltk_data/index')
        self.index_path = os.path.join(self.index_dir_base, lang, corpus, chunk)

    def make_index_example(self):
        """Make a Whoosh index."""
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
        try:
            _index = create_in(self.index_path, schema)
        except FileNotFoundError:
            os.makedirs(self.index_path)
            _index = create_in(self.index_path, schema)
        writer = _index.writer()

        writer.add_document(title=u"First document",
                            path=u"/a",
                            content=u"This is the first document we've added!")
        writer.add_document(title=u"Second document",
                            path=u"/b",
                            content=u"The second one is even more interesting!")
        writer.commit()

    def index_corpus(self):
        """Make a Whoosh index out of a pre-processed corpus, ie TLG, PHI5,
        or PHI7.

        TLG takes almost 13 min; PHI5 1.5 min.
        To setup index parameters
        >>> cltk_index = CLTKIndex('latin', 'phi5')  # 1.5 min, 363 docs
        >>> cltk_index = CLTKIndex('latin', 'phi5', chunk='work')  # 2 min, 837 docs
        >>> cltk_index = CLTKIndex('greek', 'tlg')  # 13 min, 1823 docs
        >>> cltk_index = CLTKIndex('greek', 'tlg', chunk='work')  #15.5 min, 6625 docs

        # And to start indexing:
        >>> cltk_index.index_corpus()

        TODO: Prevent overwriting. Ask user to rm old dir before re-indexing.
        """

        # Setup index dir
        schema = Schema(path=ID(stored=True),
                        author=TEXT(stored=True),
                        content=TEXT)
        try:
            _index = create_in(self.index_path, schema)
        except FileNotFoundError:
            os.makedirs(self.index_path)
            _index = create_in(self.index_path, schema)
        writer = _index.writer()

        # Setup corpus to be indexed
        if self.lang == 'greek' and self.corpus == 'tlg':
            corpus_path = os.path.expanduser('~/cltk_data/greek/text/tlg/plaintext/')
            if self.chunk == 'work':
                corpus_path = os.path.expanduser('~/cltk_data/greek/text/tlg/individual_works/')
        elif self.lang == 'latin' and self.corpus == 'phi5':
            corpus_path = os.path.expanduser('~/cltk_data/latin/text/phi5/plaintext/')
            if self.chunk == 'work':
                corpus_path = os.path.expanduser('~/cltk_data/latin/text/phi5/individual_works/')
        assert os.path.isdir(corpus_path), 'Corpus does not exist in the following location: "%s". Use CLTK Corpus Importer and TLGU to create transformed corpus.' % corpus_path  # pylint: disable=line-too-long

        files = os.listdir(corpus_path)
        if self.lang == 'greek' and self.corpus == 'tlg':
            files = [f[:-4] for f in files if f.startswith('TLG')]
            corpus_index = tlg_author_map
        elif self.lang == 'latin' and self.corpus == 'phi5':
            files = [f[:-4] for f in files if f.startswith('LAT')]
            corpus_index = phi5_author_map

        time_0 = time.time()
        logger.info("Commencing indexing of %s documents of '%s' corpus." % (len(files), self.corpus))  # pylint: disable=line-too-long
        logger.info('Index will be written to: "%s".' % self.index_path)
        if self.chunk == 'author':
            for count, file in enumerate(files, 1):

                try:
                    if self.lang == 'greek' and self.corpus == 'tlg':
                        file = file[3:]
                        author = corpus_index[file]
                        path = os.path.join(corpus_path, 'TLG' + file + '.TXT')
                    if self.lang == 'latin' and self.corpus == 'phi5':
                        author = corpus_index[file]
                        path = os.path.join(corpus_path, file + '.TXT')
                except KeyError as key_error:
                    if file.startswith('LAT9999'):
                        continue
                    raise
                    logger.error(key_error)

                with open(path) as file_open:
                    content = file_open.read()
                writer.add_document(path=path,
                                    author=author,
                                    content=content)

                if count % 100 == 0:
                    logger.info('Indexed doc %s.' % count)

        if self.chunk == 'work':
            for count, file in enumerate(files, 1):
                try:
                    if self.lang == 'greek' and self.corpus == 'tlg':
                        path = os.path.join(corpus_path, file + '.TXT')
                        author = corpus_index[file[3:-8]]
                    if self.lang == 'latin' and self.corpus == 'phi5':
                        path = os.path.join(corpus_path, file + '.TXT')
                        author = corpus_index[file[:-8]]
                except KeyError as key_error:
                    if file.startswith('LAT9999'):
                        continue
                    logger.error(key_error)
                    raise

                with open(path) as file_open:
                    content = file_open.read()
                writer.add_document(path=path,
                                    author=author,
                                    content=content)
                if count % 100 == 0:
                    logger.info('Indexed doc %s.' % count)
        logger.info('Commencing to commit changes.')
        writer.commit()

        time_1 = time.time()
        elapsed = time_1 - time_0
        logger.info('Finished indexing all documents in %s seconds (averaging %s docs per sec.)' % (elapsed, (len(files) / elapsed)))  # pylint: disable=line-too-long

    def query_index_example(self, query):
        """Send query to pre-made index, get response.

        >>> results = cltk_index.query_index_example('first')
        """
        _index = open_dir(self.index_path)
        with _index.searcher() as searcher:
            _query = QueryParser("content", _index.schema).parse(query)
            results = searcher.search(_query)
            return results


if __name__ == '__main__':
    cltk_index = CLTKIndex('latin', 'phi5')
    #cltk_index = CLTKIndex('latin', 'phi5', chunk='work')
    #cltk_index = CLTKIndex('greek', 'tlg')
    #cltk_index = CLTKIndex('greek', 'tlg', chunk='work')
    cltk_index.index_corpus()
