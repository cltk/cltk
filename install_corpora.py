import os.path
from cltk.corpus.utils.importer import CorpusImporter

print(f'Travis directory for cltk_data is {os.path.expanduser("~/cltk_data/")}')

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
        corpus_importer.import_corpus(corpus)
        print(f'Installing {corpus}.')
