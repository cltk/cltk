# encoding: utf-8
"""PHI5 Greek texts class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import os
from cltk.corpus_api.tlgu import TLGU
from cltk.corpus_api import LocalCorpus


class PHI5(LocalCorpus):
    def __init__(self, path):
        self.name = 'phi5'
        self.path = path
        LocalCorpus.__init__(self, self.name, self.path)
        self.tlgu = TLGU()

    def retrieve(self):
        return self.copy_contents()

    def compile(self):
        """Reads original Beta Code files and converts to Unicode files

        """
        self.logger.info('Starting PHI5 corpus compilation into files.')
        for file_name, abbrev in self.authors.items():
            orig_file = file_name + '.TXT'
            orig_path = os.path.join(self.original_texts, orig_file)
            try:
                compiled_file = file_name + '.txt'
                compiled_path = os.path.join(self.compiled_texts,
                                             compiled_file)
                # Use `tlgu` utility to compile to Unicode text
                self.tlgu.run(orig_path, compiled_path,
                              opts=['-r', '-X', '-b'])
                msg = 'Compiled {} to : {}'.format(file_name, compiled_path)
                self.logger.info(msg)
            except IOError:
                msg = 'Failed to compile {}'.format(file_name)
                self.logger.error(msg)

    @property
    def authors(self):
        return self._property('authors_index.json', self.index_authors)

    def index_authors(self, path):
        """Reads PHI5's `AUTHTAB.DIR` and writes a JSON dict
        to `author_index.json` in the CLTK's corpus directory.

        """
        splitter = lambda x: x.split('ÿ')[1:-21]

        def to_dict(item):
            item_repl = item.replace('\x83l', '') \
                            .replace('Â€', '; ').replace('&1', '') \
                            .replace('&', '').replace('\x80', '; ')
            item_split = item_repl.split(' ', 1)
            return item_split[0], item_split[1]

        return self._indexer('AUTHTAB.DIR', path, splitter, to_dict)

print(PHI5('~/').compile())
#print(TLGU().exe)
