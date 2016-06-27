"""
Macronizes Latin word by matching its POS tag to its entry in the Morpehus database.

Example:
In  [1]: text = "Gallia est omnis divisa in partes tres"
In  [2]: Macronizer().macronize_text(text)
Out    : [('gallia', 'n-s---fb-', 'galliā'),
          ('est', 'v3spia---', 'est'),
          ('omnis', 'omnīs'),
          ('divisa', 'dīvīsā'),
          ('partes', 'partēs'),
          ('tres', 'tres')]
"""

from cltk.tag.pos import POSTag
import macrons
import random

AVAILABLE_TAGGERS = ['tag_ngram_123_backoff']

class Macronizer(object):
    """
    Macronize text by using the POS tag to find the macronized form within the
    morpheus database.
    """
    def __init__(self, tagger):
        """Initialize class with chosen tagger."""
        self.tagger = tagger.lower()
        assert self.tagger in AVAILABLE_TAGGERS, \
            "Macronizer not available for '{0}' tagger.".format(self.tagger)

    def retrieve_tag(self, text):
        """
        Tag text with chosen tagger and clean tags.
        Tag format: [('word', 'tag')]

        :param text: string
        :return: list of tuples, with each tuple containing the word and its pos tag
        :rtype : list
        """
        if self.tagger == 'tag_ngram_123_backoff': # Data format: Perseus Style (see https://github.com/cltk/latin_treebank_perseus)
                tags = POSTag('latin').tag_ngram_123_backoff(text.lower())
                return [(tag[0], tag[1].lower()) for tag in tags]

    def retrieve_morpheus_entry(self, text):
        """
        Return morpheus entry.
        :param text: string
        :return: list of list of tuples from morpheus db
        :rtype : list
        """
        tags = Macronizer(self.tagger).retrieve_tag(text)
        entries = []
        for tag in tags:
            pos_tag = tag[1]
            entry = macrons.vowel_len_map.get(tag[0])
            matching_entries = [entries for entries in entry if pos_tag in entries]
            if len(entry) == 0 or len(matching_entries) == 0:
                entries.append([tag + (None,)])
            else:
                entries.append(matching_entries)
        return entries



    def macronize(self, text):
        """
        Return list of tuples containing the POS tag, token, and macronized token.
        :param text: string
        :return: tuples with POS tag, token, and macornized token
        :rtype : list
        """
        entries = Macronizer(self.tagger).retrieve_morpheus_entry(text)
        macronized = []
        for entry in entries:
            if len(entry) == 1:
                macronized.append(entry[0])
            else:
                macronized.append(random.choice(entry))
        return macronized


if __name__ == "__main__":
    test = "gallia est omnis divisa partes tres"
    print(Macronizer('tag_ngram_123_backoff').macronize(test))