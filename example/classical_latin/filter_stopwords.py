import nltk.tokenize

from cltk.stop.classical_latin.stops import STOPS_LIST

SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'

lowered = SENTENCE.lower()

tokens = nltk.word_tokenize(lowered)

filtered = [w for w in tokens if not w in STOPS_LIST]

print(tokens)
print(filtered)
