"""Tibetan language corpora available for download or loading locally.
All remote corpora hosted by github on the cltk organization account, eg:
'http://github.com/cltk' + name
"""

TIBETAN_CORPORA = [
    {'encoding': 'utf-8',
     'markup': 'xml',
     'location': 'remote',
     'type': 'pos',
     'origin': 'https://github.com/cltk/tibetan_pos_tdc.git',
     'name': 'tibetan_pos_tdc'},
    {'encoding': 'utf-8',
     'markup': 'xml',
     'location': 'remote',
     'type': 'lexicon',
     'origin': 'https://github.com/cltk/tibetan_lexica_tdc.git',
     'name': 'tibetan_lexica_tdc'}
]
