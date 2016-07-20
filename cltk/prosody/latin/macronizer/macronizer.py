"""
Macronizes Latin word by matching its POS tag to its entry in the Morpehus database.

All unfound and ambiguous entries are logged in cltk_log.

Example:
In  [1]: text = "Gallia est omnis divisa in partes tres"
In  [2]: Macronizer().macronize_text(text)
Out    : [('n-s---fb-', 'Gallia', 'Galliā')
          ('v3spia---', 'sum', 'est')
          ('a-s---mn-', 'omnis', 'omnis')
          ('divisa', 't-prppnn-', None)
          ('n-p---fa-', 'pars', 'partēs')
          ('tres', 'm--------', None)]
"""
# TODO Figure out what to do with ambiguous lemmata (e.g. est -> edo or sum)
# TODO Determine how to regularize tags
# TODO Fix CRF tagger option
# TODO Fix import error with full import statement

from cltk.tag.pos import POSTag
from cltk.utils.cltk_logger import logger
import macrons
import random
import re

AVAILABLE_TAGGERS = ['tag_ngram_123_backoff', 'tag_tnt', 'tag_crf']


class Macronizer(object):
    """
    Macronize Latin words.

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
            return [(tag[0], tag[1]) for tag in tags]
        elif self.tagger == 'tag_tnt':
            tags = POSTag('latin').tag_tnt(text.lower())
            return [(tag[0], tag[1]) for tag in tags]
        elif self.tagger == 'tag_crf':
            tags = POSTag('latin').tag_crf(text.lower())
            return [(tag[0], tag[1]) for tag in tags]

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
            if tag[1] is not None:
                pos_tag = tag[1].lower()
            else:
                continue
            entry = macrons.vowel_len_map.get(tag[0])
            if entry is not None:
                matching_entries = [entries for entries in entry if pos_tag in entries]
            else:
                logger.info('Entry {} not found in Morpheus.'.format(tag[0]))
                continue
            if len(entry) == 0 or len(matching_entries) == 0:
                entries.append([tag + (tag[0],)])
                logger.info('No entry found for "{}".'.format(tag))
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
                logger.info('Multiple entries found for "{}".'.format(entry))
                macronized.append(random.choice(entry))
        return macronized


if __name__ == "__main__":
    def clean_text(text):
        return re.sub('[^a-zA-Z\s]+', '', text)
    test = "/Users/Tyler1/cltk_data/latin/text/latin_text_latin_library/caesar/gall1.txt"
    with open(test) as file:
        caesar = file.read()
    print(Macronizer('tag_ngram_123_backoff').macronize(clean_text(caesar))[990:1000])
    # test = "[1] gallia est divisa omnis tres partes."
    # print(Macronizer("tag_ngram_123_backoff").retrieve_morpheus_entry(test))
