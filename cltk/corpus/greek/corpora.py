"""Greek language corpora available for download or loading locally.
All remote corpora hosted by github on the cltk organization account, eg:
'http://github.com/cltk' + name
"""

GREEK_CORPORA = [
    {'name': 'greek_software_tlgu',
     'location': 'remote',
     'type': 'software'},
    {'encoding': 'utf-8',
     'markup': 'tei_xml',
     'name': 'greek_text_perseus',
     'location': 'remote',
     'type': 'text'},
    {'encoding': 'latin-1',
     'markup': 'beta_code',
     'name': 'phi7',
     'location': 'local',
     'type': 'text'},
    {'encoding': 'latin-1',
     'markup': 'beta_code',
     'name': 'tlg',
     'location': 'local',
     'type': 'text'},
    {'encoding': 'utf-8',
     'markup': 'plaintext',
     'name': 'greek_cltk_proper_names',
     'location': 'remote',
     'type': 'dictionary'},
    {'name': 'greek_cltk_linguistic_data',
     'location': 'remote',
     'type': 'model'},
    {'encoding': 'utf-8',
     'markup': 'xml',
     'name': 'greek_treebank_perseus',
     'location': 'remote',
     'type': 'treebank'},
]



