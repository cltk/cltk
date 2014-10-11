# encoding: utf-8
"""Perseus Latin texts class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus_api import RemoteCorpus, TEIDoc

class PerseusLatin(RemoteCorpus):
    def __init__(self):
        self.name = 'perseus_latin'
        self.tar_url = ('https://raw.githubusercontent.com/kylepjohnson/'
                        'corpus_perseus_latin/master/perseus_latin.tar.gz')
        RemoteCorpus.__init__(self, self.name, self.tar_url)

    def retrieve(self):
        self.get_tar()


class PerseusLatinDoc(TEIDoc):
    def __init__(self, path):
        self.path = path
        TEIDoc.__init__(self, self.path)
