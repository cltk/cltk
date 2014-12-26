"""Greek language corpora available for download or loading locally."""

GREEK_CORPORA = [
    {'encoding': None,  #?
     'homepage': 'https://github.com/cltk/tlgu',
     'markup': None,
     'name': 'tlgu',
     'location': 'remote',
     'type': 'software',
     'path': 'https://github.com/cltk/tlgu/blob/master/tlgu.tar.gz?raw=true'},  # pylint: disable=C0301
    {'encoding': 'utf-8',
     'homepage': 'https://github.com/cltk/greek_corpus_perseus',
     'markup': 'tei_xml',
     'name': 'greek_text_perseus',
     'location': 'remote',
     'type': 'text',
     'path': 'https://raw.githubusercontent.com/cltk/greek_corpus_perseus/master/greek_corpus_perseus_new.tar.gz'},  # pylint: disable=C0301
    {'encoding': 'latin-1',
     'homepage': 'http://epigraphy.packhum.org/inscriptions/',
     'markup': 'beta_code',
     'name': 'phi7',
     'location': 'local',
     'type': 'text',
     'path': ''},
    {'encoding': 'latin-1',
     'homepage': '',
     'markup': 'beta_code',
     'name': 'tlg',
     'location': 'local',
     'type': 'text',
     'path': ''},
    {'encoding': 'utf-8',
     'homepage': 'https://github.com/cltk/greek_proper_names',
     'markup': 'plaintext',
     'name': 'greek_proper_names',
     'location': 'remote',
     'type': 'dictionary',
     'path': 'https://raw.githubusercontent.com/cltk/greek_proper_names/master/greek_proper_names.tar.gz'},  # pylint: disable=C0301
    {'encoding': 'utf-8',
     'homepage': 'https://github.com/cltk/cltk_greek_linguistic_data',
     'markup': 'pickle',
     'name': 'cltk_linguistic_data',
     'location': 'remote',
     'type': 'trained_model',
     'path': 'https://raw.githubusercontent.com/cltk/cltk_greek_linguistic_data/master/greek.tar.gz'},  # pylint: disable=C0301
    {'encoding': 'utf-8',
     'homepage': 'https://github.com/cltk/greek_treebank_perseus',
     'markup': 'xml',
     'name': 'greek_treebank_perseus',
     'location': 'remote',
     'type': 'treebank',
     'path': 'https://raw.githubusercontent.com/cltk/greek_treebank_perseus/master/greek_treebank_perseus.tar.gz'},  # pylint: disable=C0301
]



