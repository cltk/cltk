"""Search CLTK corpora with Whoosh, a Python-language index."""

import os

from whoosh.fields import *
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


class CLTKIndex:

    def __init__(self, lang, corpus, chunk='author'):
        self.lang = lang
        self.corpus = corpus
        chunks = ['author', 'work']
        assert chunk in chunks, 'Chunk must be one of the following: {}.'.format(chunks)

        self.index_dir_base = os.path.expanduser('~/cltk_data/indices')
        self.index_path = os.path.join(self.index_dir_base, lang, corpus, chunk)

    def make_index(self):
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

    def query_index(self, query):
        """Send query to pre-made index, get response."""
        _index = open_dir(self.index_path)
        with _index.searcher() as searcher:
            _query = QueryParser("content", _index.schema).parse(query)
            results = searcher.search(_query)
            return results


if __name__ == '__main__':
    cltk_index = CLTKIndex('latin', 'phi5')
    cltk_index.make_index()
    results = cltk_index.query_index('none')
    print(results)
