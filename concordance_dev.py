from cltk.utils.philology import ConcordanceIndex
from nltk.tokenize.punkt import PunktLanguageVars

with open('/Users/kyle/Desktop/bg.txt') as f:
    r = f.read()
p = PunktLanguageVars()
tokens = p.word_tokenize(r)

c = ConcordanceIndex(tokens)

tokens = set(tokens)  #! rm dupes after index, before loop
tokens = [x for x in tokens if x not in [',', '.', ';', ':', '"', "'", '[', ']']]

'''
concordance_list = []
for token in tokens:
    x = None
    x = c.return_concordance(token)
    print(x)
    #input()
    concordance_list.append(x)

print(concordance_list)
'''

x = c.return_concordance_all(tokens)
print(x)