"""Latin language corpora available for download or loading locally."""

CORPORA = [
    {'encoding': 'utf-8',
     'homepage': 'https://github.com/cltk/latin_corpus_perseus',
     'markup': 'tei_xml',
     'name': 'latin_corpus_perseus',
     'location ': 'remote',
     'type': 'text',
     'path': 'https://raw.githubusercontent.com/cltk/latin_corpus_perseus/master/latin_corpus_perseus.tar.gz'},  # pylint: disable=C0301
    {'encoding': 'utf-8',
     'homepage': 'https://github.com/cltk/latin_treebank_perseus',
     'markup': 'xml',
     'name': 'latin_treebank_perseus',
     'location ': 'remote',
     'type': 'treebank',
     'path': 'https://raw.githubusercontent.com/cltk/latin_treebank_perseus/master/latin_treebank_perseus.tar.gz'},  # pylint: disable=C0301
    {'encoding': 'utf-8',
     'homepage': 'https://github.com/cltk/latin_corpus_lacus_curtius',
     'markup': 'plaintext',
     'name': 'latin_corpus_lacus_curtius',
     'location ': 'remote',
     'type': 'text',
     'path': 'https://raw.githubusercontent.com/cltk/latin_corpus_lacus_curtius/master/lacus_curtius.tar.gz'},  # pylint: disable=C0301
    {'encoding': 'utf-8',
     'homepage': 'https://github.com/cltk/latin_corpus_latin_library',
     'markup': 'plaintext',
     'name': 'latin_corpus_latin_library',
     'location ': 'remote',
     'type': 'text',
     'path': 'https://raw.githubusercontent.com/cltk/latin_corpus_latin_library/master/latin_library.tar.gz'},  # pylint: disable=C0301
    {'encoding': 'latin-1',
     'homepage': 'http://latin.packhum.org/',
     'markup': 'beta_code',
     'name': 'phi5',
     'location ': 'local',
     'type': 'text',
     'path': ''},
    {'encoding': 'latin-1',
     'homepage': 'http://epigraphy.packhum.org/inscriptions/',
     'markup': 'beta_code',
     'name': 'phi7',
     'location ': 'local',
     'type': 'text',
     'path': ''},
    {'encoding': 'utf-8',
     'homepage': 'https://github.com/cltk/latin_proper_names',
     'markup': 'plaintext',
     'name': 'latin_proper_names',
     'location ': 'remote',
     'type': 'dictionary',
     'path': 'https://raw.githubusercontent.com/cltk/latin_proper_names/master/proper_names.tar.gz'},  # pylint: disable=C0301
    {'encoding': 'utf-8',
     'homepage': 'https://github.com/cltk/cltk_greek_linguistic_data',
     'markup': 'pickle',
     'name': 'cltk_greek_linguistic_data',
     'location': 'remote',
     'type': 'trained_model',
     'path': 'https://raw.githubusercontent.com/cltk/cltk_latin_linguistic_data/master/latin.tar.gz'},  # pylint: disable=C0301
]



