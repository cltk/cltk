"""Search CLTK corpora with Whoosh, a Python-language index."""

import os
import time

from whoosh.fields import ID
from whoosh.fields import Schema
from whoosh.fields import TEXT
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from cltk.corpus.greek.tlg.id_author import ID_AUTHOR as TLG_AUTHOR_MAP
from cltk.corpus.latin.phi5_index import PHI5_INDEX as PHI5_AUTHOR_MAP
from cltk.utils.cltk_logger import logger


__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>']
__license__ = 'MIT License. See LICENSE.'


class CLTKIndex:
    """Functions sharing the state of an index to be made or already created."""
    def __init__(self, lang, corpus, chunk='author'):
        self.lang = lang
        self.corpus = corpus
        self.chunk = chunk
        chunks = ['author', 'work']
        assert self.chunk in chunks, 'Chunk must be one of the following: {}.'.format(chunks)

        self.index_dir_base = os.path.expanduser('~/cltk_data')
        self.index_dir_base = os.path.join(self.index_dir_base, lang, 'index')
        self.index_path = os.path.join(self.index_dir_base, corpus, chunk)

    def index_corpus(self):
        """Make a Whoosh index out of a pre-processed corpus, ie TLG, PHI5,
        or PHI7.

        TLG takes almost 13 min; PHI5 1.5 min.
        To setup index parameters
        >>> # cltk_index = CLTKIndex('latin', 'phi5')  # 1.5 min, 363 docs
        >>> # cltk_index = CLTKIndex('latin', 'phi5', chunk='work')  # 2 min, 837 docs
        >>> # cltk_index = CLTKIndex('greek', 'tlg')  # 13 min, 1823 docs
        >>> # cltk_index = CLTKIndex('greek', 'tlg', chunk='work')  #15.5 min, 6625 docs

        # And to start indexing:
        >>> # cltk_index.index_corpus()

        TODO: Prevent overwriting. Ask user to rm old dir before re-indexing.
        TODO: Add option for lemmatizing.
        TODO: Add for figure out lower() options.
        TODO: Process TLG through forthcoming normalize().
        TODO: Add name to each index.
        TODO: Turn off any language-specific mods (eg, stemming, case) that
        Whoosh might be doing by default.
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
            corpus_index = TLG_AUTHOR_MAP
        elif self.lang == 'latin' and self.corpus == 'phi5':
            files = [f[:-4] for f in files if f.startswith('LAT')]
            corpus_index = PHI5_AUTHOR_MAP

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
                    logger.error(key_error)
                    raise

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

    def corpus_query(self, query, save_file=None, window_size=300, surround_size=50):
        """Send query to a corpus's index. `save_file` is a filename.
        :type save_file: str

        >>> # cltk_index = CLTKIndex('latin', 'latin_text_latin_library')
        >>> # results = cltk_index.corpus_query('amicitia')

        """
        _index = open_dir(self.index_path)

        output_str = ''

        with _index.searcher() as searcher:
            _query = QueryParser("content", _index.schema).parse(query)
            results = searcher.search(_query, limit=None)
            results.fragmenter.charlimit = None

            # Allow larger fragments
            results.fragmenter.maxchars = window_size
            # Show more context before and after
            results.fragmenter.surround = surround_size

            docs_number = searcher.doc_count_all()

            output_str += 'Docs containing hits: {}.'.format(docs_number) + '</br></br>'

            for hit in results:
                author = hit['author']
                filepath = hit['path']
                output_str += author + '</br>'
                output_str += filepath + '</br>'

                with open(filepath) as file_open:
                    file_contents = file_open.read()

                highlights = hit.highlights("content", text=file_contents, top=10000000)
                lines = highlights.split('\n')
                #lines_numbers = [l for l in lines]
                lines_br = '</br>'.join(lines)
                lines_number_approx = len(lines)
                output_str += 'Approximate hits: {}.'.format(lines_number_approx) + '</br>'

                output_str += lines_br + '</br></br>'

        if save_file:
            user_dir = os.path.expanduser('~/cltk_data/user_data/search')
            output_path = os.path.join(user_dir, save_file + '.html')

            try:
                with open(output_path, 'w') as file_open:
                    file_open.write(output_str)
            except FileNotFoundError:
                os.mkdir(user_dir)
                with open(output_path, 'w') as file_open:
                    file_open.write(output_str)
        else:
            return output_str

if __name__ == '__main__':
    #cltk_index = CLTKIndex('latin', 'phi5')
    #cltk_index = CLTKIndex('latin', 'phi5', chunk='work')
    #cltk_index = CLTKIndex('greek', 'tlg')
    #cltk_index = CLTKIndex('greek', 'tlg', chunk='work')
    #cltk_index.index_corpus()

    #_results = cltk_index.corpus_query('amicitia')
    #_results = cltk_index.corpus_query('ἀνὴρ')
    #print(_results)

    user_dir = os.path.expanduser('~/cltk_data/user_data/search')
    output_file = 'amicitia.html'
    output_path = os.path.join(user_dir, output_file)

    _index = open_dir('/Users/kyle/cltk_data/latin/index/phi5/work/')
    query = 'amicitia'

    output_str = ''
    with _index.searcher() as searcher:
        _query = QueryParser("content", _index.schema).parse(query)
        results = searcher.search(_query, limit=None)
        results.fragmenter.charlimit = None

        # Allow larger fragments
        results.fragmenter.maxchars = 300
        # Show more context before and after
        results.fragmenter.surround = 50

        docs_number = searcher.doc_count_all()

        output_str += 'Docs containing hits: {}.'.format(docs_number) + '</br></br>'


        for hit in results:
            author = hit['author']
            filepath = hit['path']
            output_str += author + '</br>'
            output_str += filepath + '</br>'

            with open(filepath) as file_open:
                file_contents = file_open.read()

            highlights = hit.highlights("content", text=file_contents, top=10000000)
            lines = highlights.split('\n')
            lines_numbers = [l for l in lines]
            lines_br = '</br>'.join(lines)
            lines_number_approx = len(lines)
            output_str += 'Approximate hits: {}.'.format(lines_number_approx) + '</br>'

            output_str += lines_br + '</br></br>'

    try:
        with open(output_path, 'w') as file_open:
            file_open.write(output_str)
    except FileNotFoundError:
        os.mkdir(user_dir)
        with open(output_path, 'w') as file_open:
            file_open.write(output_str)


