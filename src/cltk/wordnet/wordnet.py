"""A CLTK interface for Sanskrit, Greek and Latin WordNets, built on the NLTK WordNet API
The Sanskrit, Greek and Latin WordNets are lexico-semantic databases for the classical languages inspired by the Princeton WordNet for English. Most directly, these WordNets build on the framework of the Fondazione Bruno Kessler's MultiWordNet Project.
The CLTK WordNet API provides a nearly complete interface to the RESTful API provided by these services and thus provides access to the rich lexical and, especially, semantic information they contain. The WordNets share a common set of semantic descriptors
(synsets) for defining the senses of words, as well as language-specific ones.

The WordNetCorpusReader class is the main entry point for getting information about lemmas, synsets,
and various lexical and semantic (conceptual) relationships such as hypernymy, hyponymy,
synonymy, antonymy etc. It is also possible to compute semantic similarities using several different algorithms.

>>> from cltk.wordnet.wordnet import WordNetCorpusReader
>>> LWN = WordNetCorpusReader(iso_code="lat")
>>> uirtus = LWN.lemma('uirtus')

>>> list(uirtus[0].synsets())
[Synset(pos='n', offset='05595229', gloss='feeling no fear'), Synset(pos='n', offset='04504076', gloss='a characteristic property that defines the apparent individual nature of something'), Synset(pos='n', offset='04349777', gloss='possession of the qualities (especially mental qualities) required to do something or get something done; "danger heightened his powers of discrimination"'), Synset(pos='n', offset='04549901', gloss='an ideal of personal excellence toward which a person strives'), Synset(pos='n', offset='03800378', gloss='moral excellence or admirableness'), Synset(pos='n', offset='03800842', gloss='morality with respect to sexual relations'), Synset(pos='n', offset='03805961', gloss='a quality of spirit that enables you to face danger of pain without showing fear'), Synset(pos='n', offset='03929156', gloss='strength of mind that enables one to endure adversity with courage'), Synset(pos='n', offset='03678310', gloss='the trait of being manly; having the characteristics of an adult male'), Synset(pos='n', offset='03806773', gloss='resolute courageousness'), Synset(pos='n', offset='04505328', gloss='something in which something or some one excels'), Synset(pos='n', offset='03806965', gloss='the trait of having a courageous spirit'), Synset(pos='n', offset='03655289', gloss='courageous high-spiritedness'), Synset(pos='n', offset='03808136', gloss='the trait of showing courage and determination in spite of possible loss or injury'), Synset(pos='n', offset='04003047', gloss='the quality that renders something desirable or valuable or useful'), Synset(pos='n', offset='03717355', gloss='a degree or grade of excellence or worth'), Synset(pos='n', offset='04003707', gloss='any admirable quality or attribute'), Synset(pos='n', offset='03798920', gloss='the quality of doing what is right and avoiding what is wrong'), Synset(pos='n', offset='03799068', gloss='a particular moral excellence')]

>>> LWN.synset('n#03457380')
Synset(pos='n', offset='03457380', gloss='a cutting or thrusting weapon with a long blade')

>>> from cltk.wordnet.wordnet import Synset
>>> s1 = Synset(LWN, 'lat', pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
>>> s2 = Synset(LWN, 'lat', pos='n', offset='03457380', gloss='a cutting or thrusting weapon with a long blade')
>>> s1.lowest_common_hypernyms(s2)
[Synset(pos='n', offset='03601056', gloss='weaponry used in fighting or hunting')]
>>> s1.shortest_path_distance(s2)
3
>>> s1.wup_similarity(s2)
0.8
"""

from __future__ import print_function, unicode_literals

import codecs
import logging
import math
import os
import re
import string
from collections import defaultdict, deque
from functools import total_ordering
from itertools import chain
from operator import itemgetter

import requests
from nltk.corpus.reader import CorpusReader
from nltk.probability import FreqDist

from cltk.utils import get_cltk_data_dir

logger = logging.getLogger(__name__)

nesteddict = lambda: defaultdict(nesteddict)
punctuation = str.maketrans("", "", string.punctuation)

######################################################################
# Table of Contents
######################################################################
# - Constants
# - Data Classes
#   - WordNetError
#   - Lemma
#   - Synset
# - WordNet Corpus Reader
# - WordNet Information Content Corpus Reader
# - Similarity Metrics
# - Demo

######################################################################
# Constants
######################################################################

#: Positive infinity (for similarity functions)
_INF = 1e300

# { Part-of-speech constants
ADJ, ADV, NOUN, VERB, PREP = "a", "r", "n", "v", "p"
# }

POS_LIST = [NOUN, VERB, ADJ, ADV, PREP]

SENSENUM_RE = re.compile(r"^([nvarp])#(\w+)$")


######################################################################
# Data Classes
######################################################################


class WordNetError(Exception):
    """An exception class for WordNet-related errors."""


class _WordNetObject(object):
    """A common base class for lemmas and synsets.

    >>> LWN = WordNetCorpusReader(iso_code="lat")
    >>> sub = Lemma(LWN, lemma='sub', pos='r', morpho='rp--------', uri='37096')
    >>> 'super' in [lemma.lemma() for lemma in sub.antonyms()]
    True

    >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
    >>> s1.hypernyms()
    [Synset(pos='n', offset='02893681', gloss='a weapon with a handle and blade with a sharp point')]

    >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
    >>> s1.hyponyms()
    [Synset(pos='n', offset='02575932', gloss='(Scottish) a long straight-bladed dagger'), Synset(pos='n', offset='03155758', gloss='a dagger with a slender blade'), Synset(pos='n', offset='03413564', gloss='a small dagger with a tapered blade')]

    >>> s1 = LWN.synset_from_pos_and_offset('n', '00510771')
    >>> s1.member_meronyms()
    [Synset(pos='n', offset='07260585', gloss='a supporter of feminism')]

    >>> s1 = LWN.synset_from_pos_and_offset('n', '02335723')
    >>> s1.substance_meronyms()
    [Synset(pos='n', offset='10626993', gloss='soil that is plastic when moist but hard when fired')]

    >>> s1 = LWN.synset_from_pos_and_offset('n', '00541686')
    >>> s1.attributes()
    [Synset(pos='a', offset='01151057', gloss='sexually attracted to members of the opposite sex'), Synset(pos='a', offset='01151299', gloss='sexually attracted to members of your own sex')]

    >>> s1 = LWN.synset_from_pos_and_offset('n', '00077986')
    >>> s1.part_meronyms()
    [Synset(pos='n', offset='00078772', gloss='preparation for the delivery of shellfire on a target')]

    >>> s1 = LWN.synset_from_pos_and_offset('v', '00107243')
    >>> s1.also_sees()
    [Synset(pos='v', offset='00293275', gloss='become looser or slack')]

    >>> s1 = LWN.synset_from_pos_and_offset('v', '00001740')
    >>> s1.entailments()
    [Synset(pos='v', offset='00003142', gloss='expel air'), Synset(pos='v', offset='00003763', gloss='draw in air')]

    >>> s1 = LWN.synset_from_pos_and_offset('v', '00014590')
    >>> s1.causes()
    [Synset(pos='v', offset='00009805', gloss='be asleep')]


    >>> s1 = LWN.synset_from_pos_and_offset('v', '00051515')
    >>> s1.verb_groups()
    [Synset(pos='v', offset='00050470', gloss='eliminate urine')]

    >>> s1 = LWN.synset_from_pos_and_offset('n', 'L9083855')
    >>> s1.nearest()
    [Synset(pos='n', offset='03543592', gloss='ship for transporting troops')]
    """

    def antonyms(self):
        """"""
        return self.related("!")

    def hypernyms(self):
        """"""
        return self.related("@")

    def _hypernyms(self):
        return self.related("@")

    def hyponyms(self):
        """"""
        return self.related("~")

    def member_holonyms(self):  # pragma: no cover
        return self.related("#m")

    def substance_holonyms(self):  # pragma: no cover
        return self.related("#s")

    def part_holonyms(self):  # pragma: no cover
        return self.related("#p")

    def member_meronyms(self):
        """"""
        return self.related("%m")

    def substance_meronyms(self):
        """"""
        return self.related("%s")

    def part_meronyms(self):
        """"""
        return self.related("%p")

    def attributes(self):
        """"""
        return self.related("=")

    def entailments(self):
        """"""
        return self.related("*")

    def causes(self):
        """"""
        return self.related(">")

    def also_sees(self):
        """"""
        return self.related("^")

    def verb_groups(self):
        """"""
        return self.related("$")

    def similar_tos(self):
        return self.related("&")

    def nearest(self):
        """"""
        return self.related("|")


@total_ordering
class Lemma(_WordNetObject):
    """The lexical entry for a single morphological form of a
    sense-disambiguated word.
    Create a Lemma from lemma, pos, and morpho, or uri parameters where:
    <lemma> is the morphological form identifying the lemma
    <pos> is one of the module attributes 'n', 'v', 'a' or 'r'
    <morpho> is the morphological descriptor
    <uri> is the URI

    >>> LWN = WordNetCorpusReader(iso_code="lat")
    >>> animus = Lemma(LWN, lemma='animus', pos='n', morpho='n-s---mn2-', uri='a2046')
    >>> print(animus)
    Lemma(lemma='animus', pos='n', morpho='n-s---mn2-', uri='a2046')
    >>> virtus = Lemma(LWN, lemma='uirtus', pos='n', morpho='n-s---fn3-', uri='u0800')
    >>> print(virtus)
    Lemma(lemma='uirtus', pos='n', morpho='n-s---fn3-', uri='u0800')

    Lemma attributes, accessible via methods with the same name:
    - lemma: The canonical form of this lemma
    - synsets: The synsets that this lemma belongs to
    - literal: The synsets that this lemma belongs to in virtue of its literal senses
    - metonymic: The synsets that this lemma belongs to in virtue of its metonymic senses
    - metaphoric: The synsets that this lemma belongs to in virtue of its metaphoric senses
    - count: The frequency of this lemma in the WordNet, i.e., the number of synsets
    (literal, metonymic, or metaphoric) to which it belongs
    Lemma methods:
    Lemmas have the following methods for retrieving related Lemmas. They
    correspond to the names for the pointer symbols defined here:
    https://wordnet.princeton.edu/documentation/wninput5wn
    These methods all return lists of Lemmas:
    - antonyms
    - hypernyms
    - hyponyms
    - member_holonyms, substance_holonyms, part_holonyms
    - member_meronyms, substance_meronyms, part_meronyms
    - attributes
    - derivationally_related_forms
    - entailments
    - causes
    - also_sees
    - verb_groups
    - similar_tos
    - pertainyms
    """

    __slots__ = [
        "_wordnet_corpus_reader",
        "_lemma",
        "_pos",
        "_morpho",
        "__synsets",
        "__related",
        "_literal",
        "_metonymic",
        "_metaphoric",
        "_uri",
        "_lang",
    ]

    def __init__(self, wordnet_corpus_reader, lemma, pos, morpho, uri, **kwargs):
        self._wordnet_corpus_reader = wordnet_corpus_reader
        self._lemma = lemma
        self._pos = pos
        self._morpho = morpho
        self._uri = uri
        self.__synsets = None
        self.__related = None

    def uri(self):
        """URI.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> metus = Lemma(LWN, lemma='metus', pos='n', morpho='n-s---mn4-', uri='m0918')
        >>> metus.uri()
        'm0918'
        """
        return self._uri

    def lemma(self):
        """Lemma.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> metus = Lemma(LWN, lemma='metus', pos='n', morpho='n-s---mn4-', uri='m0918')
        >>> metus.lemma()
        'metus'
        """
        return self._lemma

    def pos(self):
        """POS.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> metus = Lemma(LWN, lemma='metus', pos='n', morpho='n-s---mn4-', uri='m0918')
        >>> metus.pos()
        'n'
        """
        return self._pos

    def morpho(self):
        """Morpho.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> metus = Lemma(LWN, lemma='metus', pos='n', morpho='n-s---mn4-', uri='m0918')
        >>> metus.morpho()
        'n-s---mn4-'
        """
        return self._morpho

    @property
    def _related(self):
        if self.__related is None:
            if not (self.lemma() and self.pos() and self.morpho()):
                results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/uri/{self.uri()}/relations/?format=json",
                    timeout=(30.0, 90.0),
                ).json()["results"]
            else:
                results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/lemmas/{self.lemma()}/{self.pos() if self.pos() else '*'}"
                    f"/{self.morpho() if self.morpho() else '*'}/relations/?format=json",
                    timeout=(30.0, 90.0),
                ).json()["results"]
            if len(results) > 1:
                if not self._wordnet_corpus_reader._ignore_errors:
                    ambiguous = [
                        f"{result['lemma']['lemma']} ({result['lemma']['morpho']})"
                        for result in results
                    ]
                    raise WordNetError(f"can't disambiguate {', '.join(ambiguous)}")
            else:
                self.__related = results[0]["relations"]
        return self.__related

    @property
    def _synsets(self):
        if self.__synsets is None:
            if not (self.lemma() and self.pos() and self.morpho()):
                results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/uri/{self.uri()}/synsets/?format=json",
                    timeout=(30.0, 90.0),
                ).json()
            else:
                results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/lemmas/{self.lemma()}/"
                    f"{self.pos() if self.pos() else '*'}/{self.morpho() if self.morpho() else '*'}/synsets/?format=json",
                    timeout=(30.0, 90.0),
                )
            if results:
                data = results.json()["results"]
                if len(data) > 1:
                    if not self._wordnet_corpus_reader._ignore_errors:
                        ambiguous = [
                            f"{result['lemma']} ({result['morpho']})" for result in data
                        ]
                        raise WordNetError(f"can't disambiguate {', '.join(ambiguous)}")
                else:
                    self.__synsets = data[0]["synsets"]
        return self.__synsets

    def synsets(self):
        """Retrieve all synsets for the lemma.

        :return: A generator of Synset objects.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> virtus = LWN.lemmas_from_uri('u0800')[0]
        >>> synset = list(virtus.synsets())[0]
        >>> print(synset.gloss())
        feeling no fear

        """
        return chain(self.literal(), self.metonymic(), self.metaphoric())

    def literal(self):
        """Retrieve all literal senses of the lemma.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> virtus = LWN.lemmas_from_uri('u0800')[0]
        >>> list(virtus.literal())
        [Synset(pos='n', offset='05595229', gloss='feeling no fear'), Synset(pos='n', offset='04504076', gloss='a characteristic property that defines the apparent individual nature of something'), Synset(pos='n', offset='04349777', gloss='possession of the qualities (especially mental qualities) required to do something or get something done; "danger heightened his powers of discrimination"'), Synset(pos='n', offset='04549901', gloss='an ideal of personal excellence toward which a person strives'), Synset(pos='n', offset='03800378', gloss='moral excellence or admirableness'), Synset(pos='n', offset='03800842', gloss='morality with respect to sexual relations'), Synset(pos='n', offset='03805961', gloss='a quality of spirit that enables you to face danger of pain without showing fear'), Synset(pos='n', offset='03929156', gloss='strength of mind that enables one to endure adversity with courage'), Synset(pos='n', offset='03678310', gloss='the trait of being manly; having the characteristics of an adult male'), Synset(pos='n', offset='03806773', gloss='resolute courageousness'), Synset(pos='n', offset='04505328', gloss='something in which something or some one excels'), Synset(pos='n', offset='03806965', gloss='the trait of having a courageous spirit'), Synset(pos='n', offset='03655289', gloss='courageous high-spiritedness'), Synset(pos='n', offset='03808136', gloss='the trait of showing courage and determination in spite of possible loss or injury'), Synset(pos='n', offset='04003047', gloss='the quality that renders something desirable or valuable or useful'), Synset(pos='n', offset='03717355', gloss='a degree or grade of excellence or worth'), Synset(pos='n', offset='04003707', gloss='any admirable quality or attribute'), Synset(pos='n', offset='03798920', gloss='the quality of doing what is right and avoiding what is wrong'), Synset(pos='n', offset='03799068', gloss='a particular moral excellence')]

        """
        return (
            Synset(
                self._wordnet_corpus_reader,
                synset["language"],
                synset["pos"],
                synset["offset"],
                synset["gloss"],
            )
            for synset in self._synsets["literal"]
        )

    def metonymic(self):
        """Retrieve all metonymic senses of the lemma.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> baculum = LWN.lemma('baculum', 'n', 'n-s---nn2-')
        >>> list(baculum[0].metonymic())
        [Synset(pos='n', offset='02327416', gloss='a support that steadies or strengthens something else'), Synset(pos='n', offset='02531456', gloss='used as a weapon'), Synset(pos='n', offset='03444976', gloss='any device that bears the weight of another thing')]

        """
        return (
            Synset(
                self._wordnet_corpus_reader,
                synset["language"],
                synset["pos"],
                synset["offset"],
                synset["gloss"],
            )
            for synset in self._synsets["metonymic"]
        )

    def metaphoric(self):
        """Retrieve all metaphoric senses of the lemma.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> baculum = LWN.lemma('baculum', 'n', 'n-s---nn2-')
        >>> list(baculum[0].metaphoric())
        [Synset(pos='n', offset='04399253', gloss='something providing immaterial support or assistance to a person or cause or interest')]

        """
        return (
            Synset(
                self._wordnet_corpus_reader,
                synset["language"],
                synset["pos"],
                synset["offset"],
                synset["gloss"],
            )
            for synset in self._synsets["metaphoric"]
        )

    def related(self, relation_symbol=None):
        """Retrieve lemmas having the given relation type to this lemma.

        :param relation_symbol: Symbol for the lexical or semantic relation
        :return: A list of Lemma objects

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> baculum = LWN.lemma('baculum', 'n', 'n-s---nn2-')
        >>> list(baculum.related('/'))  # doctest: +SKIP
        [Lemma(lemma='bacillum', pos='n', morpho='n-s---nn2-', uri='b0028'), Lemma(lemma='imbecillus', pos='a', morpho='aps---mn1-', uri='i0301')]
        """
        if relation_symbol and relation_symbol in self._related:
            return (
                Lemma(
                    self._wordnet_corpus_reader,
                    lemma["lemma"],
                    lemma["pos"],
                    lemma["morpho"],
                    lemma["uri"],
                )
                for lemma in self._related[relation_symbol]
            )
        else:
            return (
                Lemma(
                    self._wordnet_corpus_reader,
                    lemma["lemma"],
                    lemma["pos"],
                    lemma["morpho"],
                    lemma["uri"],
                )
                for relation_symbol in self.__related
                for lemma in self._related[relation_symbol]
            )

    def derivationally_related_forms(self):
        """derivationally_related_forms.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> abalienatio = LWN.lemma('abalienatio', 'n', 'n-s---fn3-')
        >>> abalienatio
        [Lemma(lemma='abalienatio', pos='n', morpho='n-s---fn3-', uri='a0014')]

        >>> sorted(abalienatio[0].derivationally_related_forms())
        [Lemma(lemma='abalienatus', pos='a', morpho='aps---mn1-', uri='53399'), Lemma(lemma='abalieno', pos='v', morpho='v1spia--1-', uri='a0015')]
        """
        return self.related("/")

    def pertainyms(self):
        """Pertainyms.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> abalienatio = LWN.lemma('abalienatio', 'n', 'n-s---fn3-')
        >>> abalienatio
        [Lemma(lemma='abalienatio', pos='n', morpho='n-s---fn3-', uri='a0014')]

        >>> list(abalienatio[0].pertainyms())
        [Lemma(lemma='abalieno', pos='v', morpho='v1spia--1-', uri='a0015'), Lemma(lemma='ab', pos='p', morpho='p---------', uri='a0001')]
        """
        return self.related("\\")

    def participle(self):
        return self.related("<")

    def composed_of(self):
        """Composed of.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> evoco = LWN.lemma('euoco', 'v', 'v1spia--1-')
        >>> list(evoco[0].composed_of())
        [Lemma(lemma='uoco', pos='v', morpho='v1spia--1-', uri='u1152'), Lemma(lemma='ex', pos='p', morpho='p---------', uri='e1167')]
        """
        return self.related("+c")

    def composes(self):
        """Composes.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> voco = LWN.lemma('uoco', 'v', 'v1spia--1-')
        >>> list(voco[0].composes())
        [Lemma(lemma='euoco', pos='v', morpho='v1spia--1-', uri='e1117'), Lemma(lemma='conuoco', pos='v', morpho='v1spia--1-', uri='c3931'), Lemma(lemma='prouoco', pos='v', morpho='v1spia--1-', uri='p4232'), Lemma(lemma='inuoco', pos='v', morpho='v1spia--1-', uri='i2733'), Lemma(lemma='reuoco', pos='v', morpho='v1spia--1-', uri='r1447')]
        """
        return self.related("-c")

    def __repr__(self):
        return "Lemma(lemma='{}', pos='{}', morpho='{}', uri='{}')".format(
            self.lemma(), self.pos(), self.morpho(), self.uri()
        )

    def __hash__(self):
        return hash(self._lemma)

    def __eq__(self, other):
        return (
            self._lemma == other._lemma
            and self._pos == other._pos
            and self._morpho == other._morpho
            and self._uri == other._uri
        )

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self._lemma < other._lemma


class Semfield:
    """
    Create a Semfield from code and english parameters where:
    <code> is the semfield's DDCS code
    <english> is the semfield's DDCS descriptor
    A semfield (semantic field) defines a broad conceptual domain that includes
    many synsets. The Latin WordNet uses the Dewey Decimal Classification System
    as a topic index and hierarchy.

    >>> LWN = WordNetCorpusReader(iso_code="lat")
    >>> anatomy = Semfield(LWN, '611', "Human Anatomy, Cytology & Histology")

    """

    __slots__ = [
        "_wordnet_corpus_reader",
        "_code",
        "_english",
        "_synsets",
        "_lemmas",
        "_hypers",
        "_hypons",
    ]

    def __init__(self, wordnet_corpus_reader, code, english=None):
        self._wordnet_corpus_reader = wordnet_corpus_reader

        self._code = code
        self._english = english
        self._synsets = None
        self._lemmas = None
        self._hypers = None
        self._hypons = None

    def code(self):
        return self._code

    def english(self):
        if self._english is None:  # pragma: no cover
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/semfields/{self.code()}/?format=json",
                timeout=(30.0, 90.0),
            )
            if results:
                if len(results.json()) > 1:
                    if self._wordnet_corpus_reader._ignore_errors:
                        ambiguous = [f"'{semfield['english']}'" for semfield in results]
                        raise WordNetError(f"can't disambiguate {', '.join(ambiguous)}")
                else:
                    self._english = results.json()[0]["english"]
        return self._english

    def synsets(self):
        """Retrieve all synsets of the semfield.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> anatomy = Semfield(LWN, '611', "Human anatomy, cytology & histology")
        >>> fat = LWN.synset('n#04089143')
        >>> print(fat in list(anatomy.synsets()))
        True

        """
        if self._synsets is None:
            english = re.sub(" ", "_", self.english())
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/semfields/{self.code()}/{english}/synsets/?format=json",
                timeout=(30.0, 90.0),
            )
            if results:
                data = results.json()["results"]
                self._synsets = (
                    Synset(
                        self._wordnet_corpus_reader,
                        synset["language"],
                        synset["pos"],
                        synset["offset"],
                        synset["gloss"],
                    )
                    for synset in data[0]["synsets"]
                )
            else:
                self._synsets = []
        return self._synsets

    def lemmas(self):
        """Retrieve all lemmas for all synsets of the semfield.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> anatomy = Semfield(LWN, '611', "Human anatomy, cytology & histology")
        >>> list(anatomy.lemmas())[0]
        Lemma(lemma='autopsia', pos='n', morpho='n-s---fn1-', uri='50882')

        """
        if self._lemmas is None:
            english = re.sub(" ", "_", self.english())
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/semfields/{self.code()}/{english}/lemmas/?format=json",
                timeout=(30.0, 90.0),
            )
            if results:
                self._lemmas = list(
                    Lemma(
                        self._wordnet_corpus_reader,
                        lemma["lemma"],
                        lemma["pos"],
                        lemma["morpho"],
                        lemma["uri"],
                    )
                    for lemma in results.json()["results"][0]["lemmas"]
                )
            else:
                self._lemmas = []
        return self._lemmas

    def hypers(self):
        """Retrieve all superordinate semfields of the semfield.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> anatomy = Semfield(LWN, '611', "Human anatomy, cytology & histology")
        >>> print(list(anatomy.hypers()))
        [Semfield(code='610', english='Medicine & Health')]

        """
        if self._hypers is None:
            english = re.sub(" ", "_", self.english())
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/semfields/{self.code()}/{english}/?format=json",
                timeout=(30.0, 90.0),
            )
            if results:
                self._hypers = (
                    Semfield(
                        self._wordnet_corpus_reader,
                        semfield["code"],
                        semfield["english"],
                    )
                    for semfield in results.json()["results"][0]["hypers"]
                )
            else:
                self._hypers = []
        return self._hypers

    def hypons(self):
        """Retrieve all subordinate semfields of the semfield.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> medicine = Semfield(LWN, '610', "Medicine & Health")
        >>> print(list(medicine.hypons()))
        [Semfield(code='610', english='Medicine & health'), Semfield(code='611', english='Human anatomy, cytology & histology'), Semfield(code='612', english='Human Physiology'), Semfield(code='613', english='Personal Health & Safety'), Semfield(code='614', english='Incidence & prevention of disease'), Semfield(code='615', english='Pharmacology & therapeutics'), Semfield(code='616', english='Diseases'), Semfield(code='617', english='Surgery & Related Medical Specialties'), Semfield(code='618', english='Gynecology, Obstetrics, Pediatrics & Geriatrics')]

        """
        if self._hypons is None:
            english = re.sub(" ", "_", self.english())
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/semfields/{self.code()}/{english}/?format=json",
                timeout=(30.0, 90.0),
            )
            if results:
                self._hypons = sorted(
                    [
                        Semfield(
                            self._wordnet_corpus_reader,
                            semfield["code"],
                            semfield["english"],
                        )
                        for semfield in results.json()["results"][0]["hypons"]
                    ],
                    key=lambda x: x.code(),
                )
            else:
                self._hypons = []
        return self._hypons

    def __repr__(self):
        return "Semfield(code='{}', english='{}')".format(self.code(), self.english())


@total_ordering
class Synset(_WordNetObject):
    """Create a Synset from pos, offset and gloss parameters where:

    <pos> is the synset's part of speech
    <offset> is the offset ID of the synset
    <gloss> is the synset's gloss

    >>> LWN = WordNetCorpusReader(iso_code="lat")
    >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
    >>> print(s1.id())
    n#02542418

    Synset attributes, accessible via methods with the same name:
    - pos: The synset's part of speech, 'n', 'v', 'a', or 'r'
    - offset: The unique offset ID of the synset
    - lemmas: A list of the Lemma objects for this synset
    - gloss: The gloss for this synset
    Synset methods:
    Synsets have the following methods for retrieving related Synsets.
    They correspond to the names for the pointer symbols defined here:
    https://wordnet.princeton.edu/documentation/wninput5wn
    These methods all return lists of Synsets.
    - hypernyms
    - hyponyms
    - member_holonyms, substance_holonyms, part_holonyms
    - member_meronyms, substance_meronyms, part_meronyms
    - attributes
    - entailments
    - causes
    - also_sees
    - verb_groups
    - similar_tos
    - nearest
    Additionally, Synsets support the following methods specific to the
    hypernym relation:
    - root_hypernyms
    - common_hypernyms
    - lowest_common_hypernyms
    Note that Synsets do not support the following relations because
    these are defined by WordNet as lexical relations:
    - derivationally_related_forms
    - pertainyms
    - composed_of
    - composes
    - participle

    """

    __slots__ = [
        "_pos",
        "_offset",
        "_lemmas",
        "_gloss",
        "_semfields",
        "_sentiment",
        "__related",
        "_max_depth",
        "_min_depth",
        "_all_hypernyms",
    ]

    def __init__(
        self, wordnet_corpus_reader, language, pos, offset, gloss, semfield=None
    ):
        self._wordnet_corpus_reader = wordnet_corpus_reader

        self._language = language
        self._pos = pos
        self._offset = offset
        self._gloss = gloss.split(":")[0]
        self._examples = None
        self._lemmas = None
        self.__related = None
        self._semfields = None
        self._sentiment = None
        self._all_hypernyms = None

    def id(self):
        return "{}#{}".format(self.pos(), self.offset())

    def semfields(self):
        """Retrieve the synset's semfields.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset('n', 'L6992236')
        >>> list(s1.semfields())
        [Semfield(code='150', english='Psychology')]

        """
        if self._semfields is None:
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/synsets/{self.pos()}/{self.offset()}/?format=json",
                timeout=(30.0, 90.0),
            )
            if results:
                self._semfields = results.json()["results"][0]["semfield"]
            else:
                self._semfields = []
        return (
            Semfield(self._wordnet_corpus_reader, semfield["code"], semfield["english"])
            for semfield in self._semfields
        )

    def sentiment(self):
        """Retrieve sentiment scores for the synset.

        :return: A dict including the synset's positivity, negativity, and objectivity scores (-1 to 1).

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset('v', '01215448')
        >>> s1.sentiment()
        {'positivity': 0.0, 'negativity': 0.625, 'objectivity': 0.375}

        """
        if self._sentiment is None:
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/synsets/{self.pos()}/{self.offset()}/sentiment/?format=json",
                timeout=(30.0, 90.0),
            )
            if results:
                data = results.json()["results"]
                self._sentiment = data[0]["sentiment"]
        return self._sentiment

    def positivity(self):
        """Positivity.

        :return: An integer value representing the synset's positivity score.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset('v', '01215448')
        >>> s1.positivity()
        0.0

        """
        if self._sentiment is None:
            self.sentiment()
        return self._sentiment["positivity"]

    def negativity(self):
        """Negativity.

        :return: An integer value representing the synset's negativity score.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset('v', '01215448')
        >>> s1.negativity()
        0.625

        """
        if self._sentiment is None:
            self.sentiment()
        return self._sentiment["negativity"]

    def objectivity(self):
        """Objectivity.

        :return: An integer value representing the synset's objectivity score.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset('v', '01215448')
        >>> s1.objectivity()
        0.375

        """
        if self._sentiment is None:
            self.sentiment()
        return self._sentiment["objectivity"]

    def language(self):
        return self._language

    def pos(self):
        return self._pos

    def offset(self):
        return self._offset

    def gloss(self):
        return self._gloss

    def examples(self):
        """Retrieve examples of any lemma instantiating this synset.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset('n', '04399253')
        >>> print(s1.examples()[0])
        {'lemma': {'lemma': 'baculum', 'pos': 'n', 'morpho': 'n-s---nn2-', 'uri': 'b0034', 'prosody': 'baculum'}, 'author_abbr': 'Vulg', 'work_abbr': 'Tob', 'reference': '10.4', 'text': 'baculum senectutis nostrae'}

        """
        if self._examples is None:
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/synsets/{self.pos()}/{self.offset()}/examples/?format=json",
                timeout=(30.0, 90.0),
            )
            if results:
                data = results.json()["results"]
                self._examples = data[0]["examples"]
        return self._examples

    def _needs_root(self):
        return self._pos == "n" or self._pos == "v"

    def lemmas(self):
        """Return all the Lemma objects associated with the synset.

        :return: A generator of Lemma objects.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> for lemma in sorted(set(s1.lemmas())):
        ...     print(lemma.lemma())
        clunaculum
        gladiolus
        parazonium
        pugio
        pugiunculus
        sica
        sicula

        """
        if self._lemmas is None:
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/synsets/{self.pos()}/{self.offset()}/lemmas/?format=json",
                timeout=(30.0, 90.0),
            )
            if results:
                data = results.json()["results"]
                self._lemmas = data[0]["lemmas"]
            else:
                self._lemmas = []
        return (
            Lemma(
                self._wordnet_corpus_reader,
                lemma["lemma"],
                lemma["pos"],
                lemma["morpho"],
                lemma["uri"],
            )
            for sense_type in self._lemmas
            for lemma in self._lemmas[sense_type]
        )

    def root_hypernyms(self):
        """et the topmost hypernyms of this synset in WordNet.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> s1.root_hypernyms()
        [Synset(pos='n', offset='00001740', gloss='anything having existence (living or nonliving)')]

        """
        result = []
        seen = set()
        todo = [self]
        while todo:
            next_synset = todo.pop()
            if next_synset not in seen:
                seen.add(next_synset)
                next_hypernyms = next_synset.hypernyms()
                if not next_hypernyms:
                    result.append(next_synset)
                else:
                    todo.extend(next_hypernyms)
        return result

    def max_depth(self):
        """Get the length of the longest hypernym path from this synset to the root.

        :return: An integer value representing the maximum path length to the root.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> s1.max_depth()
        7

        """
        if "_max_depth" not in self.__dict__:
            hypernyms = self.hypernyms()
            if not hypernyms:
                self._max_depth = 0
            else:
                self._max_depth = 1 + max(h.max_depth() for h in hypernyms)
        return self._max_depth

    def min_depth(self):
        """Get min depth.
        :return: The length of the shortest hypernym path from this
        synset to the root.
        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> s1.min_depth()
        7
        """
        if "_min_depth" not in self.__dict__:
            hypernyms = self.hypernyms()
            if not hypernyms:
                self._min_depth = 0
            else:
                self._min_depth = 1 + min(h.min_depth() for h in hypernyms)
        return self._min_depth

    def closure(self, rel, depth=-1):
        """Return the transitive closure of the synset under the rel
        relationship, breadth-first.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> hypers = lambda s: s.hypernyms()
        >>> list(s1.closure(hypers))
        [Synset(pos='n', offset='02893681', gloss='a weapon with a handle and blade with a sharp point'), Synset(pos='n', offset='03601056', gloss='weaponry used in fighting or hunting'), Synset(pos='n', offset='03601456', gloss='weapons considered collectively'), Synset(pos='n', offset='02859872', gloss='an artifact (or system of artifacts) that is instrumental in accomplishing some end'), Synset(pos='n', offset='00011937', gloss='a man-made object'), Synset(pos='n', offset='00009457', gloss='a physical (tangible and visible) entity'), Synset(pos='n', offset='00001740', gloss='anything having existence (living or nonliving)')]

        """
        from nltk.util import breadth_first

        synset_ids = []
        for synset in breadth_first(self, rel, depth):
            if synset.id() != self.id():
                if synset.id() not in synset_ids:
                    synset_ids.append(synset.id())
                    yield synset

    def hypernym_paths(self):
        """Get the path(s) from this synset to the root, where each path is a
        list of the synset nodes traversed on the way to the root.
        :return: A list of lists, where each list gives the node sequence
        connecting the initial ``Synset`` node and a root node.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> s1.hypernym_paths()
        [[Synset(pos='n', offset='00001740', gloss='anything having existence (living or nonliving)'), Synset(pos='n', offset='00009457', gloss='a physical (tangible and visible) entity'), Synset(pos='n', offset='00011937', gloss='a man-made object'), Synset(pos='n', offset='02859872', gloss='an artifact (or system of artifacts) that is instrumental in accomplishing some end'), Synset(pos='n', offset='03601456', gloss='weapons considered collectively'), Synset(pos='n', offset='03601056', gloss='weaponry used in fighting or hunting'), Synset(pos='n', offset='02893681', gloss='a weapon with a handle and blade with a sharp point'), Synset(pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')]]
        """
        paths = []

        hypernyms = self.hypernyms()
        if len(hypernyms) == 0:
            paths = [[self]]

        for hypernym in hypernyms:
            for ancestor_list in hypernym.hypernym_paths():
                ancestor_list.append(self)
                paths.append(ancestor_list)
        return paths

    def common_hypernyms(self, other):
        """Find all synsets that are hypernyms of this synset and the
        other synset.
        :type other: Synset
        :param other: other input synset.
        :return: The synsets that are hypernyms of both synsets.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> s2 = Synset(LWN, None, pos='n', offset='03457380', gloss='a cutting or thrusting weapon with a long blade')
        >>> sorted(s1.common_hypernyms(s2))
        [Synset(pos='n', offset='00001740', gloss='anything having existence (living or nonliving)'), Synset(pos='n', offset='00009457', gloss='a physical (tangible and visible) entity'), Synset(pos='n', offset='00011937', gloss='a man-made object'), Synset(pos='n', offset='02859872', gloss='an artifact (or system of artifacts) that is instrumental in accomplishing some end'), Synset(pos='n', offset='03601056', gloss='weaponry used in fighting or hunting'), Synset(pos='n', offset='03601456', gloss='weapons considered collectively')]

        """
        if not self._all_hypernyms:
            self._all_hypernyms = set(
                self_synset
                for self_synsets in self._iter_hypernym_lists()
                for self_synset in self_synsets
            )
        if not other._all_hypernyms:
            other._all_hypernyms = set(
                other_synset
                for other_synsets in other._iter_hypernym_lists()
                for other_synset in other_synsets
            )
        return list(self._all_hypernyms.intersection(other._all_hypernyms))

    def lowest_common_hypernyms(self, other, simulate_root=False, use_min_depth=False):
        """Get a list of lowest synset(s) that both synsets have as a hypernym.
        When `use_min_depth == False` this means that the synset which appears
        as a hypernym of both `self` and `other` with the lowest maximum depth
        is returned or if there are multiple such synsets at the same depth
        they are all returned
        However, if `use_min_depth == True` then the synset(s) which has/have
        the lowest minimum depth and appear(s) in both paths is/are returned.
        :type other: Synset
        :param other: other input synset
        :type simulate_root: bool
        :param simulate_root: The various verb taxonomies do not
        share a single root which disallows this metric from working for
        synsets that are not connected. This flag (False by default)
        creates a fake root that connects all the taxonomies. Set it
        to True to enable this behavior. For the noun taxonomy,
        there is usually a default root except for WordNet version 1.6.
        If you are using wordnet 1.6, a fake root will need to be added
        for nouns as well.
        :type use_min_depth: bool
        :param use_min_depth: This setting mimics older (v2) behavior of NLTK
        wordnet If True, will use the min_depth function to calculate the
        lowest common hypernyms. This is known to give strange results for
        some synset pairs (eg: 'chef.n.01', 'fireman.n.01') but is retained
        for backwards compatibility
        :return: The synsets that are the lowest common hypernyms of both
        synsets

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> s2 = Synset(LWN, None, pos='n', offset='03457380', gloss='a cutting or thrusting weapon with a long blade')
        >>> s1.lowest_common_hypernyms(s2)
        [Synset(pos='n', offset='03601056', gloss='weaponry used in fighting or hunting')]

        """
        synsets = self.common_hypernyms(other)
        if simulate_root:
            root = Synset(self._wordnet_corpus_reader, None, self.pos(), "00000000", "")
            synsets.append(root)

        try:
            if use_min_depth:
                max_depth = max(s.min_depth() for s in synsets)
                unsorted_lch = [s for s in synsets if s.min_depth() == max_depth]
            else:
                max_depth = max(s.max_depth() for s in synsets)
                unsorted_lch = [s for s in synsets if s.max_depth() == max_depth]
            return sorted(unsorted_lch)
        except ValueError:
            return []

    def hypernym_distances(self, distance=0, simulate_root=False):
        """Get the path(s) from this synset to the root, counting the distance
        of each node from the initial node on the way. A set of
        (synset, distance) tuples is returned.
        :type distance: int
        :param distance: the distance (number of edges) from this hypernym to
        the original hypernym ``Synset`` on which this method was called.
        :return: A set of ``(Synset, int)`` tuples where each ``Synset`` is
        a hypernym of the first ``Synset``.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> sorted(s1.hypernym_distances())
        [(Synset(pos='n', offset='00001740', gloss='anything having existence (living or nonliving)'), 7), (Synset(pos='n', offset='00009457', gloss='a physical (tangible and visible) entity'), 6), (Synset(pos='n', offset='00011937', gloss='a man-made object'), 5), (Synset(pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade'), 0), (Synset(pos='n', offset='02859872', gloss='an artifact (or system of artifacts) that is instrumental in accomplishing some end'), 4), (Synset(pos='n', offset='02893681', gloss='a weapon with a handle and blade with a sharp point'), 1), (Synset(pos='n', offset='03601056', gloss='weaponry used in fighting or hunting'), 2), (Synset(pos='n', offset='03601456', gloss='weapons considered collectively'), 3)]

        """
        distances = set([(self, distance)])
        for hypernym in self._hypernyms():
            distances |= set(
                hypernym.hypernym_distances(distance + 1, simulate_root=False)
            )
        if simulate_root:
            root = Synset(self._wordnet_corpus_reader, self.pos(), "00000000")
            root_distance = max(distances, key=itemgetter(1))[1]
            distances.add((root, root_distance + 1))
        return list(distances)

    def _shortest_hypernym_paths(self, simulate_root):
        if self.offset == "00000000":
            return {self: 0}

        queue = deque([(self, 0)])
        path = {}

        while queue:
            s, depth = queue.popleft()
            if s in path:
                continue
            path[s] = depth

            depth += 1
            queue.extend((hyp, depth) for hyp in s._hypernyms())

        if simulate_root:
            root = Synset(self._wordnet_corpus_reader, None, self.pos(), "00000000", "")
            path[root] = max(path.values()) + 1

        return path

    def shortest_path_distance(self, other, simulate_root=False):
        """Returns the distance of the shortest path linking the two synsets (if
        one exists). For each synset, all the ancestor nodes and their
        distances are recorded and compared. The ancestor node common to both
        synsets that can be reached with the minimum number of traversals is
        used. If no ancestor nodes are common, None is returned. If a node is
        compared with itself 0 is returned.
        :type other: Synset
        :param other: The Synset to which the shortest path will be found.
        :return: The number of edges in the shortest path connecting the two
        nodes, or None if no path exists.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> s2 = Synset(LWN, None, pos='n', offset='03457380', gloss='a cutting or thrusting weapon with a long blade')
        >>> s1.shortest_path_distance(s2)
        3

        """
        if self == other:
            return 0

        dist_dict1 = self._shortest_hypernym_paths(simulate_root)
        dist_dict2 = other._shortest_hypernym_paths(simulate_root)

        # For each ancestor synset common to both subject synsets, find the
        # connecting path length. Return the shortest of these.

        inf = float("inf")
        path_distance = inf
        for synset, d1 in dist_dict1.items():
            d2 = dist_dict2.get(synset, inf)
            path_distance = min(path_distance, d1 + d2)

        return None if math.isinf(path_distance) else path_distance

    def tree(self, rel, depth=-1, cut_mark=None):
        """Generate a tree-like list structure for rel relationship of this synset.
        :param rel: A function returning the relations of a certain kind of this synset.
        :param depth:
        :param cut_mark: An object used to indicate where a branch has been truncated.
        :return: A list of lists.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset(pos='n', offset='01595188')
        >>> hypers = lambda s: s.hypernyms()
        >>> s1.tree(hypers)
        [Synset(pos='n', offset='01595188', gloss='a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; occurs in many breeds; "the dog barked all night"'), [Synset(pos='n', offset='01594481', gloss='any of various fissiped mammals with nonretractile claws and typically long muzzles'), [Synset(pos='n', offset='01586585', gloss='terrestrial or aquatic flesh-eating mammal; terrestrial carnivores have four or five clawed digits on each limb'), [Synset(pos='n', offset='01402712', gloss='mammals having a placenta; all mammals except monotremes and marsupials'), [Synset(pos='n', offset='01378363', gloss='any warm-blooded vertebrate having the skin more or less covered with hair; young are born alive except for the small subclass of monotremes and nourished with milk'), [Synset(pos='n', offset='00995974', gloss='animals having a bony or cartilaginous skeleton with a segmented spinal column and a large brain enclosed in a skull or cranium'), [Synset(pos='n', offset='00990770', gloss='any animal of the phylum Chordata having a notochord or spinal column'), [Synset(pos='n', offset='00008019', gloss='a living organism characterized by voluntary movement'), [Synset(pos='n', offset='00002086', gloss='any living entity'), [Synset(pos='n', offset='00001740', gloss='anything having existence (living or nonliving)')]]]]]]]]]]

        """
        tree = [self]
        if depth != 0:
            tree += [x.tree(rel, depth - 1, cut_mark) for x in rel(self)]
        elif cut_mark:
            tree += [cut_mark]
        return tree

    # Similarity methods
    def path_similarity(self, other, verbose=False, simulate_root=True):
        """Path Distance Similarity:
        Return a score denoting how similar two word senses are, based on the
        shortest path that connects the senses in the is-a (hypernym/hypnoym)
        taxonomy. The score is in the range 0 to 1, except in those cases where
        a path cannot be found (will only be true for verbs as there are many
        distinct verb taxonomies), in which case None is returned. A score of
        1 represents identity i.e. comparing a sense with itself will return 1.
        :type other: Synset
        :param other: The ``Synset`` that this ``Synset`` is being compared to.
        :type simulate_root: bool
        :param simulate_root: The various verb taxonomies do not
        synsets that are not connected. This flag (True by default)
        creates a fake root that connects all the taxonomies. Set it
        to false to disable this behavior. For the noun taxonomy,
        there is usually a default root except for WordNet version 1.6.
        If you are using wordnet 1.6, a fake root will be added for nouns
        as well.
        :return: A score denoting the similarity of the two ``Synset`` objects,
        normally between 0 and 1. None is returned if no connecting path
        could be found. 1 is returned if a ``Synset`` is compared with
        itself.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> s2 = Synset(LWN, None, pos='n', offset='03457380', gloss='a cutting or thrusting weapon with a long blade')
        >>> s1.path_similarity(s2)
        0.25

        """
        distance = self.shortest_path_distance(
            other, simulate_root=simulate_root and self._needs_root()
        )
        if distance is None or distance < 0:
            return None
        return 1.0 / (distance + 1)

    def _lcs_ic(self, other, icreader, verbose=False):  # pragma: no cover
        """Get the information content of the least common subsumer that has
        the highest information content value.  If two nodes have no
        explicit common subsumer, assume that they share an artificial
        root node that is the hypernym of all explicit roots.
        :type synset1: Synset
        :param synset1: First input synset.
        :type synset2: Synset
        :param synset2: Second input synset.  Must be the same part of
        speech as the first synset.
        :type  ic: WordNetICCorpusReader
        :param ic: an information content reader object
        :return: The information content of the two synsets and their most
        informative subsumer
        """
        if self._pos != other._pos:
            raise WordNetError(
                "Computing the least common subsumer requires "
                "%s and %s to have the same part of speech." % (self, other)
            )

        ic1 = icreader.information_content(self)
        ic2 = icreader.information_content(other)
        subsumers = self.common_hypernyms(other)
        if len(subsumers) == 0:
            subsumer_ic = 0
        else:
            subsumer_ic = max(icreader.information_content(s) for s in subsumers)

        if verbose:
            print("> LCS Subsumer by content:", subsumer_ic)

        return ic1, ic2, subsumer_ic

    def lch_similarity(
        self, other, verbose=False, simulate_root=True
    ):  # pragma: no cover
        """Leacock Chodorow Similarity:
        Return a score denoting how similar two word senses are, based on the
        shortest path that connects the senses (as above) and the maximum depth
        of the taxonomy in which the senses occur. The relationship is given as
        -log(p/2d) where p is the shortest path length and d is the taxonomy
        depth. Because this metric must compute the max depth of the entire synset
        taxonomy, it can be very slow!
        :type  other: Synset
        :param other: The ``Synset`` that this ``Synset`` is being compared to.
        :type simulate_root: bool
        :param simulate_root: The various verb taxonomies do not
        share a single root which disallows this metric from working for
        synsets that are not connected. This flag (True by default)
        creates a fake root that connects all the taxonomies. Set it
        to false to disable this behavior.
        :return: A score denoting the similarity of the two ``Synset`` objects,
        normally greater than 0. None is returned if no connecting path
        could be found. If a ``Synset`` is compared with itself, the
        maximum score is returned, which varies depending on the taxonomy
        depth.

        """
        if self._pos != other._pos:
            raise WordNetError(
                "Computing the lch similarity requires "
                "%s and %s to have the same part of speech." % (self, other)
            )

        need_root = self._needs_root()

        if self._pos not in self._wordnet_corpus_reader._max_depth:
            self._wordnet_corpus_reader._compute_max_depth(self._pos, need_root)

        depth = self._wordnet_corpus_reader._max_depth[self._pos]

        distance = self.shortest_path_distance(
            other, simulate_root=simulate_root and need_root
        )

        if distance is None or distance < 0 or depth == 0:
            return None
        return -math.log((distance + 1) / (2.0 * depth))

    def wup_similarity(self, other, verbose=False, simulate_root=True):
        """Wu-Palmer Similarity:
        Return a score denoting how similar two word senses are, based on the
        depth of the two senses in the taxonomy and that of their Least Common
        Subsumer (most specific ancestor node). Previously, the scores computed
        by this implementation did _not_ always agree with those given by
        Pedersen's Perl implementation of WordNet Similarity. However, with
        the addition of the simulate_root flag (see below), the score for
        verbs now almost always agree but not always for nouns.
        The LCS does not necessarily feature in the shortest path connecting
        the two senses, as it is by gloss the common ancestor deepest in
        the taxonomy, not closest to the two senses. Typically, however, it
        will so feature. Where multiple candidates for the LCS exist, that
        whose shortest path to the root node is the longest will be selected.
        Where the LCS has multiple paths to the root, the longer path is used
        for the purposes of the calculation.
        :type  other: Synset
        :param other: The ``Synset`` that this ``Synset`` is being compared to.
        :type simulate_root: bool
        :param simulate_root: The various verb taxonomies do not
        share a single root which disallows this metric from working for
        synsets that are not connected. This flag (True by default)
        creates a fake root that connects all the taxonomies. Set it
        to false to disable this behavior.
        :return: A float score denoting the similarity of the two ``Synset``
        objects, normally greater than zero. If no connecting path between
        the two senses can be found, None is returned.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = Synset(LWN, None, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
        >>> s2 = Synset(LWN, None, pos='n', offset='03457380', gloss='a cutting or thrusting weapon with a long blade')
        >>> s1.wup_similarity(s2)
        0.8

        """
        need_root = self._needs_root()
        # Note that to preserve behavior from NLTK2 we set use_min_depth=True
        # It is possible that more accurate results could be obtained by
        # removing this setting and it should be tested later on
        subsumers = self.lowest_common_hypernyms(
            other, simulate_root=simulate_root and need_root, use_min_depth=True
        )

        # If no LCS was found return None
        if len(subsumers) == 0:
            return None

        subsumer = self if self in subsumers else subsumers[0]

        # Get the longest path from the LCS to the root,
        # including a correction:
        # - add one because the calculations include both the start and end
        #   nodes
        depth = subsumer.max_depth() + 1

        # Note: No need for an additional add-one correction for non-nouns
        # to account for an imaginary root node because that is now
        # automatically handled by simulate_root
        # if subsumer._pos != NOUN:
        #     depth += 1

        # Get the shortest path from the LCS to each of the synsets it is
        # subsuming.  Add this to the LCS path length to get the path
        # length from each synset to the root.
        len1 = self.shortest_path_distance(
            subsumer, simulate_root=simulate_root and need_root
        )
        len2 = other.shortest_path_distance(
            subsumer, simulate_root=simulate_root and need_root
        )
        if len1 is None or len2 is None:
            return None
        len1 += depth
        len2 += depth
        return (2.0 * depth) / (len1 + len2)

    def res_similarity(self, other, icreader, verbose=False):
        """Resnik Similarity:
        Return a score denoting how similar two word senses are, based on the
        Information Content (IC) of the Least Common Subsumer (most specific
        ancestor node).
        :type  other: Synset
        :param other: The ``Synset`` that this ``Synset`` is being compared to.
        :type ic: WordNetICCorpusReader
        :param ic: an information content reader
        :return: A float score denoting the similarity of the two ``Synset``
        objects. Synsets whose LCS is the root node of the taxonomy will
        have a score of 0 (e.g. N['dog'][0] and N['table'][0]).

        >>> from cltk.wordnet.wordnet import WordNetCorpusReader, WordNetICCorpusReader
        >>> LASLA_IC = WordNetICCorpusReader(iso_code="lat", fileids=['ic-lasla.dat'])
        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset('n', '02542418')
        >>> s2 = LWN.synset_from_pos_and_offset('n', '03457380')
        >>> s1.res_similarity(s2, LASLA_IC)
        6.056495670686355
        """
        ic1, ic2, lcs_ic = self._lcs_ic(other, icreader)
        return lcs_ic

    def jcn_similarity(self, other, icreader, verbose=False):
        """Jiang-Conrath Similarity:
        Return a score denoting how similar two word senses are, based on the
        Information Content (IC) of the Least Common Subsumer (most specific
        ancestor node) and that of the two input Synsets. The relationship is
        given by the equation 1 / (IC(s1) + IC(s2) - 2 * IC(lcs)).
        :type  other: Synset
        :param other: The ``Synset`` that this ``Synset`` is being compared to.
        :type  ic: WordNetICCorpusReader
        :param ic: an information content reader
        :return: A float score denoting the similarity of the two ``Synset``
        objects.

        >>> from cltk.wordnet.wordnet import WordNetCorpusReader, WordNetICCorpusReader
        >>> LASLA_IC = WordNetICCorpusReader(iso_code='lat', fileids=['ic-lasla.dat'])
        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset('n', '02542418')
        >>> s2 = LWN.synset_from_pos_and_offset('n', '03457380')
        >>> s1.jcn_similarity(s2, LASLA_IC)
        0.23789011550933925
        """
        if self == other:
            return _INF

        ic1, ic2, lcs_ic = self._lcs_ic(other, icreader)

        # If either of the input synsets are the root synset, or have a
        # frequency of 0 (sparse data problem), return 0.
        if ic1 == 0 or ic2 == 0:
            return 0

        ic_difference = ic1 + ic2 - 2 * lcs_ic

        if ic_difference == 0:
            return _INF

        return 1 / ic_difference

    def lin_similarity(self, other, icreader, verbose=False):
        """Lin Similarity.
        Return a score denoting how similar two word senses are, based on the
        Information Content (IC) of the Least Common Subsumer (most specific
        ancestor node) and that of the two input Synsets. The relationship is
        given by the equation 2 * IC(lcs) / (IC(s1) + IC(s2)).
        :type other: Synset
        :param other: The ``Synset`` that this ``Synset`` is being compared to.
        :type ic: WordNetICCorpusReader
        :param ic: an information content reader
        :return: A float score denoting the similarity of the two ``Synset``
        objects, in the range 0 to 1.

        >>> from cltk.wordnet.wordnet import WordNetCorpusReader, WordNetICCorpusReader
        >>> LASLA_IC = WordNetICCorpusReader(iso_code="lat", fileids=['ic-lasla.dat'])
        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset('n', '02542418')
        >>> s2 = LWN.synset_from_pos_and_offset('n', '03457380')
        >>> s1.lin_similarity(s2, LASLA_IC)
        0.7423716841366877
        """
        ic1, ic2, lcs_ic = self._lcs_ic(other, icreader)
        return (2.0 * lcs_ic) / (ic1 + ic2)

    def _iter_hypernym_lists(self):
        """Get hypernyms.
        :return: An iterator over ``Synset`` objects that are either proper
        hypernyms or instance of hypernyms of the synset.
        """
        todo = [self]
        seen = set()
        while todo:
            for synset in todo:
                seen.add(synset)
            yield todo
            todo = [
                hypernym
                for synset in todo
                for hypernym in synset.hypernyms()
                if hypernym not in seen
            ]

    def __repr__(self):
        return "Synset(pos='{}', offset='{}', gloss='{}')".format(
            self.pos(), self.offset(), self.gloss()
        )

    def related(self, relation_symbol=None, sort=True):
        """Get related.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> s1 = LWN.synset_from_pos_and_offset('v', '01215448')
        >>> s1.related('~')
        [Synset(pos='v', offset='01217265', gloss='feel panic')]

        """
        get_synset = self._wordnet_corpus_reader.synset_from_pos_and_offset
        if relation_symbol and relation_symbol in self._related:
            r = [
                get_synset(synset["pos"], synset["offset"])
                for synset in self._related[relation_symbol]
            ]
            if sort:
                r.sort()
        else:
            r = []
        return r

    @property
    def _related(self):
        if self.__related is None:
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/synsets/{self.pos()}/{self.offset()}/relations/?format=json",
                timeout=(30.0, 90.0),
            )

            if results and len(results.json()["results"]) != 0:
                self.__related = results.json()["results"][0]["relations"]
            else:
                self.__related = []
        return self.__related

    def __eq__(self, other):
        return self._pos == other._pos and self._offset == other._offset

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self._pos != other._pos:
            raise WordNetError(
                "operation undefined for '{}' and '{}'".format(self._pos, other._pos)
            )
        return self._offset < other._offset

    def __hash__(self):
        return hash(f"{self.pos()}#{self.offset()}")


######################################################################
# WordNet Corpus Reader
######################################################################
class WordNetCorpusReader(CorpusReader):
    """A corpus reader used to access a WordNet.
    :param iso_code: The ISO code for one of the languages providing a WordNet API

    >>> LWN = WordNetCorpusReader(iso_code="lat")
    >>> animus = LWN.lemma('animus', 'n', 'n-s---mn2-')
    >>> print(animus)
    [Lemma(lemma='animus', pos='n', morpho='n-s---mn2-', uri='a2046')]
    >>> dico = LWN.lemmas('dico', 'v')
    >>> print(sorted(list(dico), key=lambda x: x.uri()))
    [Lemma(lemma='dico', pos='v', morpho='v1spia--1-', uri='d1349'), Lemma(lemma='dico', pos='v', morpho='v1spia--3-', uri='d1350')]
    >>> virtus = LWN.lemmas_from_uri('u0800')
    >>> print(virtus)
    [Lemma(lemma='uirtus', pos='n', morpho='n-s---fn3-', uri='u0800')]
    >>> courage = LWN.synset('n#03805961')
    >>> print(courage)
    Synset(pos='n', offset='03805961', gloss='a quality of spirit that enables you to face danger of pain without showing fear')
    >>> adverbs = LWN.synsets('r')
    >>> print(len(list(adverbs)) > 3600)
    True
    """

    _DEFAULT_HOSTS = {
        "san": "https://sanskritwordnet.unipv.it",
        "grc": "https://greekwordnet.chs.harvard.edu",
        "lat": "https://latinwordnet.exeter.ac.uk",
    }
    _ENCODING = "utf8"

    # { Part of speech constants
    _pos_numbers = {NOUN: 1, VERB: 2, ADJ: 3, ADV: 4, PREP: 5}
    _pos_names = dict(tup[::-1] for tup in _pos_numbers.items())
    # }

    def __init__(self, iso_code, ignore_errors=False):
        """Construct a new WordNet corpus reader"""
        super(WordNetCorpusReader, self).__init__(
            encoding=self._ENCODING, root="", fileids=None
        )
        self._iso_code = iso_code
        self._host = self._DEFAULT_HOSTS[self._iso_code]
        self._ignore_errors = ignore_errors

        # A cache so we don't have to reconstuct synsets
        # Map from pos -> offset -> Synset
        self._synset_cache = nesteddict()

        # A cache so we don't have to reconstuct synsets
        # Map from lemma -> pos -> morpho -> Lemma
        self._lemma_cache = nesteddict()

        # A lookup for the maximum depth of each part of speech.  Useful for
        # the lch similarity metric.
        self._max_depth = defaultdict(dict)

    def host(self):
        return self._host

    def _compute_max_depth(self, pos, simulate_root):  # pragma: no cover
        """Compute the max depth for the given part of speech.  This is
        used by the lch similarity metric.
        """
        depth = 0
        for ii in self.synsets(pos=pos):
            try:
                depth = max(depth, ii.max_depth())
            except RuntimeError:
                print(ii)
        if simulate_root:
            depth += 1
        self._max_depth[pos] = depth

    def get_status(self):  # pragma: no cover
        results = requests.get(
            f"{self.host()}/api/status/?format=json", timeout=(30.0, 90.0)
        )
        return results

    #############################################################
    # Loading Lemmas
    #############################################################
    def lemma(self, lemma, pos="", morpho="", return_ambiguous=True):
        """Takes ``lemma`` and finds matching headword.

        If ``pos`` or ``morph`` is provided, the results found through
        ``lemma`` alone are filtered. ``pos`` tags are in the form
        ``n`` for noun, ``v`` for verb, ``a`` for adjective, ``r`` for adverb.

        If ``return_ambiguous`` is ``False``, only the first matching lemma
        is returned as a single-element list. If ``True``, (default) all the
        matching lemmas will be returned.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> LWN.lemma('baculum')
        [Lemma(lemma='baculum', pos='n', morpho='n-s---nn2-', uri='b0034')]

        """
        resolved = []
        if lemma in self._lemma_cache:
            logger.debug(f"lemma found in cache: {lemma}")
            if pos and pos in self._lemma_cache[lemma]:  # pragma: no cover
                logger.debug(f"pos found in cache: {pos}")
                if morpho and morpho in self._lemma_cache[lemma][pos]:
                    logger.debug(f"morpho found in cache: {morpho}")
                    resolved.extend(self._lemma_cache[lemma][pos][morpho])
                else:
                    resolved.extend(
                        [
                            self._lemma_cache[lemma][pos][morpho][uri]
                            for morpho in self._lemma_cache[lemma][pos]
                            for uri in self._lemma_cache[lemma][pos][morpho]
                        ]
                    )
            else:
                resolved.extend(
                    [
                        self._lemma_cache[lemma][pos][morpho][uri]
                        for pos in self._lemma_cache[lemma]
                        for morpho in self._lemma_cache[lemma][pos]
                        for uri in self._lemma_cache[lemma][pos][morpho]
                        if morpho in self._lemma_cache[lemma][pos]
                    ]
                )

        if not resolved:
            logger.debug(f"REQUEST: {lemma}, (pos={pos}, morpho={morpho})")
            results = self.json = requests.get(
                f"{self.host()}/api/lemmas/{lemma if lemma else '*'}/{pos if pos else '*'}"
                f"/{morpho if morpho else '*'}?format=json",
                timeout=(30.0, 90.0),
            )
            if results:
                data = results.json()["results"]
                for item in data:
                    l = Lemma(self, **(item))
                    resolved.append(l)
                    self._lemma_cache[lemma][item["pos"]][item["morpho"]][
                        item["uri"]
                    ] = l

        if return_ambiguous:
            return resolved
        else:
            return resolved[:1]

    def lemma_from_uri(self, uri):
        """Get lemma from URI.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> LWN.lemma_from_uri('b0034')
        Lemma(lemma='baculum', pos='n', morpho='n-s---nn2-', uri='b0034')
        """
        results = self.json = requests.get(
            f"{self.host()}/api/uri/{uri}?format=json", timeout=(30.0, 90.0)
        )
        if results:
            data = results.json()["results"]
            if len(data) > 1:
                ambiguous = [
                    f"{result['lemma']} ({result['morpho']})" for result in results
                ]
                raise WordNetError(f"can't disambiguate {', '.join(ambiguous)}")
            l = Lemma(self, **data[0])
            self._lemma_cache[data[0]["lemma"]][data[0]["pos"]][data[0]["morpho"]][
                data[0]["uri"]
            ] = l
            return l

    def semfield(self, code, english):
        """Semfield.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> LWN.semfield('910', 'Geography & travel')
        Semfield(code='910', english='Geography & travel')
        """
        english = re.sub(" ", "_", english)

        # load semfield information
        results = self.json = requests.get(
            f"{self.host()}/api/semfields/{code}/{english}/?format=json",
            timeout=(30.0, 90.0),
        )
        if results:
            data = results.json()["results"]
        if len(data) == 0:
            raise WordNetError(f"semfield {code} '{english}' not found")

        # Return the semfield object.
        return Semfield(self, data[0]["code"], data[0]["english"])

    #############################################################
    # Loading Synsets
    #############################################################
    def synset(self, id):
        """Get synset.

        :param id: Synset id, consisting of POS and offset separated by '#'
        :return: Synset object

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> LWN.synset('r#L2556264')
        Synset(pos='r', offset='L2556264', gloss='in the manner of a woman')

        """
        pos, offset = SENSENUM_RE.search(id).groups()

        # load synset information
        synset = self.synset_from_pos_and_offset(pos, offset)

        if synset is None:
            raise WordNetError(f"synset {id} not found")

        # Return the synset object.
        return synset

    def synset_from_pos_and_offset(self, pos, offset):
        """Get synset from pos.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> LWN.synset_from_pos_and_offset('r', 'L2556264')
        Synset(pos='r', offset='L2556264', gloss='in the manner of a woman')

        """
        # Check to see if the synset is in the cache
        if offset in self._synset_cache[pos]:
            return self._synset_cache[pos][offset]

        results = requests.get(
            f"{self.host()}/api/synsets/{pos}/{offset}?format=json",
            timeout=(30.0, 90.0),
        )
        if results:
            data = results.json()["results"][0]
            synset = Synset(self, **data)
            self._synset_cache[pos][offset] = synset
            return synset

    #############################################################
    # Retrieve synsets and lemmas.
    #############################################################
    def lemmas(self, lemma=None, pos=None, morpho=None):
        """Return all Lemma objects with a name matching the specified lemma
        name, part of speech tag or morphological descriptor.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> sorted(list(LWN.lemmas('dico', 'v')), key=lambda x: x.uri())
        [Lemma(lemma='dico', pos='v', morpho='v1spia--1-', uri='d1349'), Lemma(lemma='dico', pos='v', morpho='v1spia--3-', uri='d1350')]

        """

        results = requests.get(
            f"{self.host()}/api/lemmas/{lemma if lemma else '*'}/{pos if pos else '*'}/"
            f"{morpho if morpho else '*'}?format=json",
            timeout=(30.0, 90.0),
        ).json()
        if results:
            return (
                Lemma(self, lemma["lemma"], lemma["pos"], lemma["morpho"], lemma["uri"])
                for lemma in results["results"]
            )

    def lemmas_from_uri(self, uri):
        """Get lemmas from URI.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> list(sorted(LWN.lemmas_from_uri('f1052')))
        [Lemma(lemma='frumentaria', pos='n', morpho='n-s---fn1-', uri='f1052'), Lemma(lemma='frumentarius', pos='n', morpho='n-s---mn2-', uri='f1052'), Lemma(lemma='frumentarius', pos='a', morpho='aps---mn1-', uri='f1052')]

        """
        results = self.json = requests.get(
            f"{self.host()}/api/uri/{uri}?format=json", timeout=(30.0, 90.0)
        )
        if results:
            data = results.json()["results"]
            lemmas_list = []
            for result in data:
                l = Lemma(self, **result)
                self._lemma_cache[result["lemma"]][result["pos"]][result["morpho"]][
                    result["uri"]
                ] = l
                lemmas_list.append(l)
            return lemmas_list

    def synsets(self, pos=None):
        """Load all synsets for a given part of speech, if specified.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> len(list(LWN.synsets('r'))) > 3000
        True

        """
        synsets_list = []

        results = requests.get(
            f"{self.host()}/api/synsets/{pos if pos else '*'}/?format=json",
            timeout=(30.0, 90.0),
        )
        if results:
            data = results.json()
            synsets_list.extend(data["results"])

            while data["next"]:
                data = requests.get(data["next"], timeout=(30.0, 90.0)).json()
                synsets_list.extend(data["results"])

        return (
            Synset(
                self,
                synset["language"],
                synset["pos"],
                synset["offset"],
                synset["gloss"],
            )
            for synset in synsets_list
        )

    def semfields(self, code=None):
        """Load all semfields for a given code, if specified.

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> list(LWN.semfields('300'))
        [Semfield(code='300', english='Social Sciences'), Semfield(code='300', english='Social Sciences, Sociology & Anthropology'), Semfield(code='300', english='Social sciences')]

        """
        semfields_list = []
        if code is None:  # pragma: no cover
            results = requests.get(
                f"{self.host()}/api/semfields/?format=json", timeout=(30.0, 90.0)
            ).json()
            semfields_list.extend(results["results"])

            while results["next"]:
                results = requests.get(results["next"], timeout=(30.0, 90.0)).json()
                semfields_list.extend(results["results"])
        else:
            results = requests.get(
                f"{self.host()}/api/semfields/{code}/?format=json", timeout=(30.0, 90.0)
            )
            if results:
                data = results.json()["results"]
            semfields_list.extend(data)
        return sorted(
            [
                Semfield(self, semfield["code"], semfield["english"])
                for semfield in semfields_list
            ],
            key=lambda x: (x.code(), x.english()),
        )

    #############################################################
    # Lemmatizer
    #############################################################
    def lemmatize(self, form: str, morpho: str = None):
        """Lemmatizes a word form.
        :param form: The form to lemmatize, as a string
        :param morpho: Optional 10-place morphological descriptor, used as a filter
        :return: A list of matching Lemma objects

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> print(list(LWN.lemmatize('pumice')))
        [Lemma(lemma='pumex', pos='n', morpho='n-s---cn3-', uri='p4512')]

        """
        if self._iso_code in ("skt", "grk"):
            raise ValueError(
                f"Lemmatization not currently available for '{self._iso_code}'"
            )

        form = form.translate(punctuation)
        if form:
            results = requests.get(
                f"{self.host()}/lemmatize/{form}/{morpho if morpho else ''}?format=json",
                timeout=(30.0, 90.0),
            )
            if results and results.json():
                return (
                    Lemma(
                        self,
                        result["lemma"]["lemma"],
                        result["lemma"]["morpho"][0],
                        result["lemma"]["morpho"],
                        result["lemma"]["uri"],
                    )
                    for result in results.json()
                )
        return []

    #############################################################
    # Translater
    #############################################################
    def translate(self, language: str, form: str, pos: str = "*"):
        """Translates an English, French, Spanish, or Italian word into Latin.
        :param language: 'en', 'fr', 'es', 'it' indicating the source language
        :param form: The word to translate
        :param pos: Optionally, a part-of-speech ('n', 'v', 'a', 'r') indicator
        used as a filter
        :return: A list of Lemma objects

        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> offspring_translations = list(LWN.translate('en', 'offspring'))
        >>> print('pusio' in [lemma.lemma() for lemma in offspring_translations])
        True

        """
        pos = f"{pos}/" if pos else ""
        results = requests.get(
            f"{self.host()}/translate/{language}/{form}/{pos}?format=json",
            timeout=(30.0, 90.0),
        )
        if results:
            data = results.json()["results"]
        return (
            Lemma(self, lemma["lemma"], lemma["pos"], lemma["morpho"], lemma["uri"])
            for lemma in data
        )


######################################################################
# WordNet Information Content Corpus Reader
######################################################################
class WordNetICCorpusReader(CorpusReader):
    """A corpus reader for the WordNet information content corpus.
    :param root: The root directory where the information content file is stored.
    :param fileids: A list of file names, relative to the root directory, in this
    case a single file containing information content for a corpus.

    >>> from cltk.wordnet.wordnet import WordNetICCorpusReader
    >>> LWNIC = WordNetICCorpusReader(iso_code='lat', fileids=['ic-lasla.dat'])
    """

    def __init__(self, iso_code, root=None, fileids=None):
        if not root:

            root = os.path.join(
                get_cltk_data_dir(),
                f"{iso_code}/model/{iso_code}_models_cltk/semantics/wordnet/",
            )
        CorpusReader.__init__(self, root, fileids, encoding="utf8")
        if fileids is not None:
            self.load_ic(fileids[0])
        else:
            self._ic = None

    def ic(self):  # pragma: no cover
        return self._ic

    #############################################################
    # Create information content from corpus
    #############################################################
    def create_ic(
        self, iso_code, corpus, weight_senses_equally=False, smoothing=1.0
    ):  # pragma: no cover
        """Creates an information content lookup dictionary from a corpus.
        :type corpus: CorpusReader
        :param corpus: The corpus from which we create an information
        content dictionary.
        :type weight_senses_equally: bool
        :param weight_senses_equally: If this is True, gives all
        possible senses equal weight rather than dividing by the
        number of possible senses.  (If a word has 3 synses, each
        sense gets 0.3333 per appearance when this is False, 1.0 when
        it is true.)
        :param smoothing: How much do we smooth synset counts (default is 1.0)
        :type smoothing: float
        :return: An information content dictionary
        """

        WN = WordNetCorpusReader(iso_code=iso_code)

        counts = FreqDist()
        for ww in corpus.words():
            results = WN.lemmatize(ww)
            for lemma in results:
                counts[lemma] += 1

        ic = {}
        for pp in POS_LIST:
            ic[pp] = defaultdict(float)

        # Initialize the counts with the smoothing value
        if smoothing > 0.0:
            for ss in WN.synsets():
                pos = ss._pos
                ic[pos][ss._offset] = smoothing

        for ww in counts:
            possible_synsets = list(ww.synsets())
            if len(possible_synsets) == 0:
                continue

            # Distribute weight among possible synsets
            weight = float(counts[ww])
            if not weight_senses_equally:
                weight /= float(len(possible_synsets))

            for ss in possible_synsets:
                pos = ss._pos
                for level in ss._iter_hypernym_lists():
                    for hh in level:
                        ic[pos][hh._offset] += weight
                # Add the weight to the root
                ic[pos][0] += weight
        self._ic = ic

    def write_ic(self, corpus_name):  # pragma: no cover
        if self._ic is None:
            raise WordNetError("No information content available")

        get_synset = self.synset_from_pos_and_offset

        path = os.path.join(self._root, "ic-{}.dat".format(corpus_name))
        with codecs.open(path, "w", "utf8") as fp:
            fp.write("lwnver:{}\n".format(self.get_status()["last_modified"]))
            for pp in POS_LIST:
                for offset in self._ic[pp]:
                    ss = get_synset(pp, offset)
                    if len(ss.hypernyms()) == 0:
                        fp.write("{} {} ROOT\n".format(ss.id(), self._ic[pp][offset]))
                    else:
                        fp.write("{} {}\n".format(ss.id(), self._ic[pp][offset]))
        self._fileids = ["ic-{}.dat".format(corpus_name)]

    def load_ic(self, icfile=None):  # pragma: no cover
        """Load an information content file and return a dictionary
        whose keys are POS types and whose values are dictionaries
        that map from synsets to information content values.
        :type icfile: str
        :param icfile: The name of the wordnet_ic file (e.g. "ic-latin_library.dat")
        :return: An information content dictionary

        >>> from cltk.wordnet.wordnet import WordNetICCorpusReader
        >>> LWNIC = WordNetICCorpusReader(iso_code="lat")
        >>> LWNIC.load_ic('ic-lasla.dat')

        """
        if not icfile:
            if self._fileids:
                icfile = self._fileids[0]
            else:
                raise WordNetError("No information content file specified")

        ic = {}
        for pos in POS_LIST:
            ic[pos] = defaultdict(float)

        for num, line in enumerate(self.open(icfile)):
            if num == 0:  # skip the header
                continue
            fields = line.split()
            pos, offset = fields[0].split("#")
            value = float(fields[1])
            if len(fields) == 3 and fields[2] == "ROOT":
                # Store root count.
                ic[pos][0] += value
            if value != 0:
                ic[pos][offset] = value
        self._fileids = [icfile]
        self._ic = ic

    def information_content(self, synset):  # pragma: no cover
        """Retrieve the information content score for a synset.

        >>> from cltk.wordnet.wordnet import WordNetCorpusReader, WordNetICCorpusReader
        >>> LWN = WordNetCorpusReader(iso_code="lat")
        >>> LWNIC = WordNetICCorpusReader(iso_code="lat", fileids=['ic-lasla.dat'])
        >>> s = LWN.synset_from_pos_and_offset('n', '02542418')
        >>> LWNIC.information_content(s)
        9.256474058450094

        """
        if not self._ic:
            raise WordNetError("No information content file has been loaded")
        try:
            icpos = self._ic[synset._pos]
        except KeyError:
            msg = "Information content file has no entries for part-of-speech: %s"
            raise WordNetError(msg % synset._pos)

        counts = icpos[synset._offset]
        if counts == 0:
            return _INF
        else:
            return -math.log(counts / icpos[0])


relation_types = {
    "!": "antonyms",
    "@": "hypernyms",
    "~": "hyponyms",
    "#m": "member-of",
    "#s": "substance-of",
    "#p": "part-of",
    "%m": "has-member",
    "%s": "has-substance",
    "%p": "has-part",
    "=": "attribute-of",
    "|": "nearest",
    "+r": "has-role",
    "-r": "is-role-of",
    "*": "entails",
    ">": "causes",
    "^": "also-see",
    "$": "verb-group",
    "&": "similar-to",
    "<": "participle",
    "+c": "composed-of",
    "-c": "composes",
    "\\": "derived-from",
    "/": "related-to",
}


# Example usage
if __name__ == "__main__":
    LWN = WordNetCorpusReader(iso_code="lat")

    lemmas = list(LWN.lemmatize("virtutem"))
    print("Lemmatized 'virtutem':", lemmas)
    virtus = LWN.lemma_from_uri("u0800")
    print("Fetched lemma by URI:", virtus)
    print("...with synsets:")
    for synset in virtus.synsets():
        print("-", synset.gloss())
    animus = LWN.lemma("animus", return_ambiguous=False)
    print("Fetched lemma", animus)
    print("'Virtus' and 'animus' share the following synsets:")
    for synset in set(virtus.synsets()).intersection(set(animus.synsets())):
        print("-", synset.id(), "in semfields:", list(synset.semfields()))
        print(
            "...with synonyms:", ", ".join([lemma.lemma() for lemma in synset.lemmas()])
        )
        print(
            "...and antonyms:",
            ", ".join(
                [
                    lemma.lemma()
                    for antonym in synset.antonyms()
                    for lemma in antonym.lemmas()
                ]
            ),
        )
    courage = list(LWN.translate("en", "courage", "n"))
    print("Translating 'courage':", courage)

    s1 = LWN.synset("n#02542418")
    print("Fetched synset:", s1.id(), "=", s1.gloss())
    s2 = LWN.synset("n#03457380")
    print("Fetched synset:", s2.id(), "=", s2.gloss())

    print("Common hypernyms:")
    for hypernym in sorted(s1.common_hypernyms(s2), key=lambda x: x.offset()):
        print("-", hypernym.gloss())
