"""
Macronizes Latin word by matching its POS tag to its entry in the Morpehus database.

Example:
In  [1]: text = "Gallia est omnis divisa in partes tres"
In  [2]: Macronizer().macronize_text(text)
Out    : [('gallia', 'galliā'),
          ('est', 'est'),
          ('omnis', 'omnīs'),
          ('divisa', 'dīvīsā'),
          ('partes', 'partēs'),
          ('tres', 'tres')]
"""

from cltk.tag.pos import POSTag
from ..macronizer import macron_temp

class Macronizer():
    def __init__(self, tagger: str):
        self.tagger = tagger

    def get_tags(self, text):
        tagger = POSTag('latin')
        return tagger.tag_ngram_123_backoff(text)

    def get_macronized(self, text):
        tag = Macronizer('test').get_tags(text)[0][1]
        entry = macronizer.macrons.vowel_len_map.get(text)
        return entry

if __name__ == "__main__":
    test = "divisa"
    print(sys.path)
    #print(Macronizer('test').get_macronized(test))
