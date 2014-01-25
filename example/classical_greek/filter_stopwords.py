import nltk.tokenize

from cltk.stop.classical_greek.stops_unicode import STOPS_LIST

SENTENCE = """
Ἅρπαγος δὲ καταστρεψάμενος Ἰωνίην ἐποιέετο στρατηίην ἐπὶ Κᾶρας καὶ Καυνίους καὶ Λυκίους, ἅμα ἀγόμενος καὶ Ἴωνας καὶ Αἰολέας.
"""

lowered = SENTENCE.lower()

tokens = nltk.word_tokenize(lowered)

filtered = [w for w in tokens if not w in STOPS_LIST]

print(SENTENCE)
print(filtered)
