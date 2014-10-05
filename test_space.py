# encoding: utf-8
"""TLG Greek texts class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import os
import re
from cltk.corpus import Corpus

#c = Corpus('tlg')

with open('/Users/smargh/Code/cltk/cltk_data/compiled/tlg/TLG0001.txt', 'r', encoding='utf-8') as file:
    data = file.read()

