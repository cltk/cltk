from cltk.utils.philology import ConcordanceIndex
from cltk.utils.philology import Philology
from nltk.tokenize.punkt import PunktLanguageVars

path = '/Users/kyle/Desktop/bg.txt'
paths = ['~/Desktop/PlinyNH.xml', '/Users/kyle/Desktop/bg.txt']

'''
with open('/Users/kyle/Desktop/bg.txt') as f:
    r = f.read()
p = PunktLanguageVars()
orig_tokens = p.word_tokenize(r)
c = ConcordanceIndex(orig_tokens)
tokens = set(orig_tokens)

#! rm dupes after index, before loop
tokens = [x for x in tokens if x not in [',', '.', ';', ':', '"', "'", '[', ']']]

all_tokens = c.return_concordance_all(tokens)

for words in all_tokens:
    for line in words:
        print(line)
'''

p = Philology()
p.write_concordance(paths, 'bellum_gallicum')