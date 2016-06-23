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

AVAILABLE_TAGGERS = ['tag_ngram_123_backoff']

class Macronizer(object):
    """
    Macronize text by using the POS tag to find the macronized form within the
    morpheus database.
    """
    def __init__(self, tagger):
        self.tagger = tagger.lower()
        assert self.tagger in AVAILABLE_TAGGERS, \
            "Macronizer not available for '{0}' tagger.".format(self.tagger)

    def retrieve_tag(self, text):
        if self.tagger == 'tag_ngram_123_backoff':
                tags = POSTag('latin').tag_ngram_123_backoff(text.lower())
                return [(tag[0], tag[1].lower()) for tag in tags]

    def macronize(self, text):
        tags = Macronizer(self.tagger).retrieve_tag(text)
        print(tags)
        macronized = []
        for tag in tags:
            if tag[1] != None:
                pos_tag = tag[1].lower()
                entry = macrons.vowel_len_map.get(tag[0])
                if len(entry) == 1:
                    macronized_form = tag + (entry[0][2],)
                    macronized.append(macronized_form)
                else:
                    for entries in entry:
                        if entries[0] == pos_tag:
                            macronized_form = tag + (entries[2],)
                            macronized.append(macronized_form)
            else:
                macronized.append(tag)
        return macronized



if __name__ == "__main__":
    test = "gallia est divisa partes tres"
    print(Macronizer('tag_ngram_123_backoff').macronize(test))