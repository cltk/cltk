"""Pali language corpora available for download or loading locally.
All remote corpora hosted by github on the cltk organization account, eg:
'http://github.com/cltk' + name
"""

PALI_CORPORA = [
    {'encoding': 'ascii',
     'markup': 'xml',
     'location': 'remote',
     'type': 'text',
     'origin': 'https://github.com/cltk/pali_text_ptr_tipitaka.git',
     'name': 'pali_text_ptr_tipitaka'},
     {'name':'pali_texts_gretil',
      'type':'text',
      'location':'remote',
      'origin':'https://github.com/cltk/pali_texts_gretil'}
]
