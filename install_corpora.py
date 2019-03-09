import os.path
from cltk.corpus.utils.importer import CorpusImporter

corpora = [
    ('latin', 'model', 'latin_models_cltk'),
    ('latin', 'text', 'latin_text_latin_library'),
    ('greek', 'model', 'greek_models_cltk'),
]

for lang, type, corpus in corpora:
    if os.path.isdir(os.path.expanduser(f'~/cltk_data/{lang}/{type}/{corpus}/')):
        print(f'{corpus} is already installed.')
    else:
        corpus_importer = CorpusImporter(lang)
        print(f'Installing {corpus}.')
