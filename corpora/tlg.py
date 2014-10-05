# encoding: utf-8
"""TLG Greek texts class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus import Corpus, TEIDoc


class TLG(Corpus):
    def __init__(self, path):
        self.name = 'tlg'
        Corpus.__init__(self, self.name)
        self.tlg_path = path

    def retrieve(self):
        self.retrieve(location=self.tlg_path)


class TLGDoc(TEIDoc):
    def __init__(self, path):
        self.path = path
        TEIDoc.__init__(self, self.path)
