# encoding: utf-8
"""Latin Library texts class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus import RemoteCorpus


class LatinLibrary(RemoteCorpus):
    def __init__(self):
        self.name = 'latin_library'
        self.tar_url = ('https://raw.githubusercontent.com/kylepjohnson/'
                        'corpus_latin_library/master/latin_library.tar.gz')
        RemoteCorpus.__init__(self, self.name, self.tar_url)

    def retrieve(self):
        self.get_tar()


class LatinLibraryDoc(object):
    def __init__(self, path):
        self.path = path
