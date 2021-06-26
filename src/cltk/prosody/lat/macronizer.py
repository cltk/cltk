"""Delineate length of lat vowels.

The Macronizer class places a macron over naturally long Latin vowels. To discern whether a vowel is long, a word is
first matched with its Morpheus entry by way of its POS tag. The Morpheus entry includes the macronized form of the
matched word.

Since the accuracy of the macronizer largely derives from the accuracy of the POS tagger used to match words to their
Morpheus entry, the Macronizer class allows for multiple POS to be used.

.. todo::
   Determine how to disambiguate tags (see logger)

"""

import importlib.machinery
import os
from typing import List, Tuple

from cltk.core.cltk_logger import logger
from cltk.tag.pos import POSTag
from cltk.utils import CLTK_DATA_DIR

__author__ = ["Tyler Kirby <tyler.kirby9398@gmail.com>"]
__license__ = "MIT License. See LICENSE."


AVAILABLE_TAGGERS = ["tag_ngram_123_backoff", "tag_tnt", "tag_crf"]


class Macronizer:
    """Macronize Latin words.

    Macronize text by using the POS tag to find the macronized form within the
    Morpheus database.
    """

    def __init__(self, tagger):
        """Initialize class with chosen tagger."""
        self.macron_data = self._setup_macrons_data()
        self.tagger = tagger.lower()
        assert (
            self.tagger in AVAILABLE_TAGGERS
        ), "Macronizer not available for '{0}' tagger.".format(self.tagger)

    def _setup_macrons_data(self):
        rel_path = os.path.join(
            CLTK_DATA_DIR, "lat/model/lat_models_cltk/taggers/macrons/macrons.py"
        )
        path = os.path.expanduser(rel_path)
        loader = importlib.machinery.SourceFileLoader("macrons", path)
        module = loader.load_module()
        macrons = module.vowel_len_map
        return macrons

    def _retrieve_tag(self, text: str) -> List[Tuple[str, str]]:
        """Tag text with chosen tagger and clean tags.

        Tag format: ``[('word', 'tag')]``

        :param text: string

        :return: list of tuples, with each tuple containing the word and its pos tag

        """
        if (
            self.tagger == "tag_ngram_123_backoff"
        ):  # Data format: Perseus Style (see https://github.com/cltk/latin_treebank_perseus)
            tags = POSTag("lat").tag_ngram_123_backoff(text.lower())
            return [(tag[0], tag[1]) for tag in tags]
        elif self.tagger == "tag_tnt":
            tags = POSTag("lat").tag_tnt(text.lower())
            return [(tag[0], tag[1]) for tag in tags]
        elif self.tagger == "tag_crf":
            tags = POSTag("lat").tag_crf(text.lower())
            return [(tag[0], tag[1]) for tag in tags]

    def _retrieve_morpheus_entry(self, word: str) -> Tuple[str, str, str]:
        """Return Morpheus entry for word

        Entry format: ``[(head word, tag, macronized form)]``

        :param word: unmacronized, lowercased word
        :ptype word: string

        :return: Morpheus entry in tuples

        """
        entry = self.macron_data.get(word)
        if entry is None:
            logger.info("No Morpheus entry found for {}.".format(word))
            return None
        elif len(entry) == 0:
            logger.info("No Morpheus entry found for {}.".format(word))
        return entry

    def _macronize_word(self, word: Tuple[str, str]) -> Tuple[str, str, str]:
        """Return macronized word.

        :param word: (word, tag)

        :return: (word, tag, macronized_form)
        """
        head_word = word[0]
        tag = word[1]
        if tag is None:
            logger.info("Tagger {} could not tag {}.".format(self.tagger, head_word))
            return head_word, tag, head_word
        elif tag == "U--------":
            return (head_word, tag.lower(), head_word)
        else:
            entries = self._retrieve_morpheus_entry(head_word)
            if entries is None:
                return head_word, tag.lower(), head_word
            matched_entry = [entry for entry in entries if entry[0] == tag.lower()]
            if len(matched_entry) == 0:
                logger.info(
                    "No matching Morpheus entry found for {}.".format(head_word)
                )
                return head_word, tag.lower(), entries[0][2]
            elif len(matched_entry) == 1:
                return head_word, tag.lower(), matched_entry[0][2].lower()
            else:
                logger.info("Multiple matching entries found for {}.".format(head_word))
                return head_word, tag.lower(), matched_entry[1][2].lower()

    def macronize_tags(self, text: str) -> List[Tuple[str, str, str]]:
        """Return macronized form along with POS tags.

        E.g. "Gallia est omnis divisa in partes tres," ->
        [('gallia', 'n-s---fb-', 'galliā'), ('est', 'v3spia---', 'est'), ('omnis', 'a-s---mn-', 'omnis'),
        ('divisa', 't-prppnn-', 'dīvīsa'), ('in', 'r--------', 'in'), ('partes', 'n-p---fa-', 'partēs'),
        ('tres', 'm--------', 'trēs')]

        :param text: raw text

        :return: tuples of head word, tag, macronized form
        """
        return [self._macronize_word(word) for word in self._retrieve_tag(text)]

    def macronize_text(self, text: str) -> str:
        """Return macronized form of text.

        E.g. "Gallia est omnis divisa in partes tres," ->
        "galliā est omnis dīvīsa in partēs trēs ,"

        :param text: raw text

        :return: macronized text

        """
        macronized_words = [entry[2] for entry in self.macronize_tags(text)]
        return " ".join(macronized_words)


if __name__ == "__main__":
    not_macronized = (
        "Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum "
        "lingua Celtae, nostra Galli appellantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos "
        "ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. Horum omnium fortissimi sunt Belgae, "
        "propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe "
        "commeant atque ea quae ad effeminandos animos pertinent important, proximique sunt Germanis, qui trans "
        "Rhenum incolunt, quibuscum continenter bellum gerunt. Qua de causa Helvetii quoque reliquos Gallos virtute "
        "praecedunt, quod fere cotidianis proeliis cum Germanis contendunt, cum aut suis finibus eos prohibent aut "
        "ipsi in eorum finibus bellum gerunt. Eorum una pars, quam Gallos obtinere dictum est, initium capit a "
        "flumine Rhodano, continetur Garumna flumine, Oceano, finibus Belgarum, attingit etiam ab Sequanis et "
        "Helvetiis flumen Rhenum, vergit ad septentriones. Belgae ab extremis Galliae finibus oriuntur, pertinent "
        "ad inferiorem partem fluminis Rheni, spectant in septentrionem et orientem solem. Aquitania a Garumna "
        "flumine ad Pyrenaeos montes et eam partem Oceani quae est ad Hispaniam pertinet; spectat inter occasum "
        "solis et septentriones. M. Caelio est malus."
    )
    test = Macronizer("tag_ngram_123_backoff")
    print(test.macronize_text(not_macronized))
