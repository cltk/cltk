import os.path
from cltk.corpus.utils.importer import CorpusImporter

print('This is the Travis directory for cltk_data:')
print(os.path.expanduser(f'~/cltk_data/'))

corpora = [
    # ('latin', 'model', 'latin_models_cltk'),
    ('latin', 'text', 'latin_text_latin_library'),
    # ('greek', 'model', 'greek_models_cltk'),
]

for lang, type, corpus in corpora:
    print(os.path.expanduser(f'~/cltk_data/{lang}/{type}/{corpus}/'))
    print(os.path.isdir(os.path.expanduser(f'~/cltk_data/{lang}/{type}/{corpus}/')))
    if os.path.isdir(os.path.expanduser(f'~/cltk_data/{lang}/{type}/{corpus}/')):
        print(f'{corpus} is already installed.')
    else:
        corpus_importer = CorpusImporter(lang)
        corpus_importer.import_corpus(corpus)
        print(f'Installing {corpus}.')
    if os.path.isdir(os.path.expanduser(f'~/cltk_data/{lang}/{type}/{corpus}/')):
        print(f'{corpus} is now installed.')
    else:
        print('No corpus installed!')
