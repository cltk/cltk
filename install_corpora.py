import os.path
from cltk.corpus.utils.importer import CorpusImporter

print(f'Travis directory for cltk_data is {os.path.expanduser("~/cltk_data/")}')

corpora = [
    ('latin', 'model', 'latin_models_cltk'),
    ('latin', 'text', 'latin_text_latin_library'),
    ('latin', 'text', 'latin_text_perseus'),
    ('greek', 'model', 'greek_models_cltk'),
    ('greek', 'text', 'greek_text_perseus'),
    ('french', 'text', 'french_data_cltk'), # Fix this naming
    ('old_norse', 'model', 'old_norse_models_cltk'),
    ('middle_low_german', 'model', 'middle_low_german_models_cltk'),
    ('old_english', 'model', 'old_english_models_cltk'),
]

for lang, type, corpus in corpora:
    if os.path.isdir(os.path.expanduser(f'~/cltk_data/{lang}/{type}/{corpus}/')):
        print(f'{corpus} is already installed.') # Should work if I can get caching on this folder!
    else:
        corpus_importer = CorpusImporter(lang)
        corpus_importer.import_corpus(corpus)
        print(f'Installing {corpus}.')
