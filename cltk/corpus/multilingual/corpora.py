"""Multilingual language corpora and software available for download or loading locally.
All remote corpora hosted by github on the cltk organization account, eg:
'http://github.com/cltk' + name
"""

MULTILINGUAL_CORPORA = [
    {'encoding': 'utf-8',
     'markup': ['conll', 'xml'],
     'location': 'remote',
     'type': 'treebank',
     'origin': 'https://github.com/cltk/multilingual_treebank_proiel.git',
     'name': 'multilingual_treebank_proiel'},
    {'encoding': 'utf-8',
     'markup': ['conll', 'xml'],
     'location': 'remote',
     'type': 'treebank',
     'origin': 'https://github.com/cltk/iswoc-treebank.git',
     'name': 'multilingual_treebank_iswoc'},
    {'encoding': 'utf-8',
     'markup': ['conll', 'xml'],
     'location': 'remote',
     'type': 'treebank',
     'origin': 'https://github.com/cltk/treebank-releases.git',
     'name': 'multilingual_treebank_torot'},
]
