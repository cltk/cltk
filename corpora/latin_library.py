# encoding: utf-8
"""Latin Library texts class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus import Corpus


class LatinLibrary(Corpus):
    def __init__(self):
        self.name = 'latin_library'
        Corpus.__init__(self, self.name)
        self.tar_url = ('https://raw.githubusercontent.com/kylepjohnson/'
                        'corpus_latin_library/master/latin_library.tar.gz')

    def retrieve(self):
        self.retrieve(url=self.tar_url)


class LatinLibraryDoc(object):
    def __init__(self, path):
        self.path = path

