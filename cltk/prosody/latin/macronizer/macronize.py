#!/usr/bin/env python
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
import macrons

class Macronizer():
    def __init__(self, tagger: str):
        self.tagger = tagger

    def get_tags(self, text):
        tagger = POSTag('latin')
        return tagger.tag_ngram_123_backoff(text)[0][1].lower()

    def get_macronized(self, text):
        tag = Macronizer('test').get_tags(text)
        entry = macrons.vowel_len_map.get(text)
        if len(entry) == 1:
            print(entry)
            return entry[0][2]
        for entries in entry:
            print(entries)
            if entries[0] == tag:
                return entries[2]
            else:
                print("Not found")
        print(tag)

if __name__ == "__main__":
    test = "divisa"
    print(Macronizer('test').get_macronized(test))
