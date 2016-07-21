from cltk.tag.pos import POSTag
from cltk.utils.cltk_logger import logger
import macrons

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
        if self.tagger == 'tag_ngram_123_backoff':  # Data format: Perseus Style (see https://github.com/cltk/latin_treebank_perseus)
            tags = POSTag('latin').tag_ngram_123_backoff(text.lower())
            return [(tag[0], tag[1]) for tag in tags]
        elif self.tagger == 'tag_tnt':
            tags = POSTag('latin').tag_tnt(text.lower())
            return [(tag[0], tag[1]) for tag in tags]
        elif self.tagger == 'tag_crf':
            tags = POSTag('latin').tag_crf(text.lower())
            return [(tag[0], tag[1]) for tag in tags]

    @staticmethod
    def retrieve_morpheus_entry(word):
        """
        Return Morpheus entry for word

        :param word: unmacronized, lowercased word
        :ptype word: string
        :return: Morpheus entry with tuples containing the tag, head word, and macronized form
        :rtype : list
        """
        entry = macrons.vowel_len_map.get(word)
        if len(entry) == 0:
            logger.info('No Morpheus entry found for {}.'.format(word))
        return entry

    def macronize_word(self, word):
        """
        Return macronized word.

        :param word: (word, tag)
        :ptype word: tuple
        :return: (word, tag, macronized_form)
        :rtype : tuple
        """
        head_word = word[0]
        tag = word[1]
        if tag is None:
            logger.info('Tagger {} could not tag {}.'.format(self.tagger, head_word))
            return (head_word, tag, head_word)
        elif tag == 'U--------':
            return (head_word, tag.lower(), head_word)
        else:
            entries = self.retrieve_morpheus_entry(head_word)
            matched_entry = [entry for entry in entries if entry[0] == tag.lower()]
            if len(matched_entry) == 0:
                logger.info('No matching Morpheus entry found for {}.'.format(head_word))
                return (head_word, tag.lower(), head_word)
            elif len(matched_entry) == 1:
                return (head_word, tag.lower(), matched_entry[0][2].lower())
            else:
                logger.info('Multiple matching entries found for {}.'.format(head_word))
                return (head_word, tag.lower(), matched_entry[1][2].lower())




if __name__ == "__main__":
    not_macronized = "Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum " \
                     "lingua Celtae, nostra Galli appellantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos " \
                     "ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. Horum omnium fortissimi sunt Belgae, " \
                     "propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe " \
                     "commeant atque ea quae ad effeminandos animos pertinent important, proximique sunt Germanis, qui trans " \
                     "Rhenum incolunt, quibuscum continenter bellum gerunt. Qua de causa Helvetii quoque reliquos Gallos virtute " \
                     "praecedunt, quod fere cotidianis proeliis cum Germanis contendunt, cum aut suis finibus eos prohibent aut " \
                     "ipsi in eorum finibus bellum gerunt. Eorum una pars, quam Gallos obtinere dictum est, initium capit a " \
                     "flumine Rhodano, continetur Garumna flumine, Oceano, finibus Belgarum, attingit etiam ab Sequanis et " \
                     "Helvetiis flumen Rhenum, vergit ad septentriones. Belgae ab extremis Galliae finibus oriuntur, pertinent " \
                     "ad inferiorem partem fluminis Rheni, spectant in septentrionem et orientem solem. Aquitania a Garumna " \
                     "flumine ad Pyrenaeos montes et eam partem Oceani quae est ad Hispaniam pertinet; spectat inter occasum " \
                     "solis et septentriones."
    test = Macronizer("tag_ngram_123_backoff")
    tags = (test.retrieve_tag(not_macronized))
    for tag in tags:
        print(test.macronize_word(tag))