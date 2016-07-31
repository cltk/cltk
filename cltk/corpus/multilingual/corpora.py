"""Multilingual language corpora and software available for download or loading locally.
All remote corpora hosted by github on the cltk organization account, eg:
'http://github.com/cltk' + name
"""

MULTILINGUAL_CORPORA = [
    {'encoding': 'utf-8',
     'markup': ['conll', 'xml'],
     'location': 'remote',
     'type': 'treebank',
     'name': 'multilingual_treebank_proiel'},
    {'name': 'lapos',
     'location': 'remote',
     'type': 'software'},
]
