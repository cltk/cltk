# encoding: utf-8
"""Perseus Latin texts class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus import Corpus, TEIDoc


class PerseusLatin(Corpus):
    def __init__(self):
        self.name = 'perseus_latin'
        Corpus.__init__(self, self.name)
        self.tar_url = ('https://raw.githubusercontent.com/kylepjohnson/'
                        'corpus_perseus_latin/master/perseus_latin.tar.gz')

    def retrieve(self):
        self.retrieve(url=self.tar_url)


class PerseusLatinDoc(TEIDoc):
    def __init__(self, path):
        self.path = path
        TEIDoc.__init__(self, self.path)
