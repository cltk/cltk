from from cltk.corpus.latin import *

try:
    latinlibrary = PlaintextCorpusReader(cltk_path + '/latin/text/latin_text_latin_library', 
    '.*\.txt',
    word_tokenizer=word_tokenizer, 
    sent_tokenizer=sent_tokenizer, 
    encoding='utf-8')    
    pass
except IOError as e:
    pass
    # print("Corpus not found. Please check that the Latin Library is installed in CLTK_DATA.")