# -*- coding: utf-8 -*-


"""
A CLTK interface for Latin WordNet, built on the NLTK WordNet API

Latin WordNet is a lexico-semantic database of Latin.
Using synsets, helps find conceptual relationships between words
such as hypernyms, hyponyms, synonyms, antonyms etc.

"""

from __future__ import print_function, unicode_literals

import codecs
import math
import re
import string
from collections import defaultdict, deque
from functools import total_ordering
from itertools import chain
from operator import itemgetter

import requests
from nltk.compat import python_2_unicode_compatible
from nltk.corpus.reader import CorpusReader
from nltk.probability import FreqDist
from nltk.util import binary_search_file as _binary_search_file
from six import iteritems


nesteddict = lambda: defaultdict(nesteddict)
punctuation = str.maketrans('', '', string.punctuation)

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
ADJ, ADV, NOUN, VERB, PREP = 'a', 'r', 'n', 'v', 'p'
# }

POS_LIST = [NOUN, VERB, ADJ, ADV, PREP]

SENSENUM_RE = re.compile(r'^([nvarp])#(\d+)$')


######################################################################
# Data Classes
######################################################################


class WordNetError(Exception):
    """An exception class for wordnet-related errors."""


class _WordNetObject(object):
    """A common base class for lemmas and synsets."""

    def antonyms(self):
        return self.related('!')

    def hypernyms(self):
        return self.related('@')

    def _hypernyms(self):
        return self.related('@')

    def hyponyms(self):
        return self.related('~')

    def member_holonyms(self):
        return self.related('#m')

    def substance_holonyms(self):
        return self.related('#s')

    def part_holonyms(self):
        return self.related('#p')

    def member_meronyms(self):
        return self.related('%m')

    def substance_meronyms(self):
        return self.related('%s')

    def part_meronyms(self):
        return self.related('%p')

    def attributes(self):
        return self.related('=')

    def entailments(self):
        return self.related('*')

    def causes(self):
        return self.related('>')

    def also_sees(self):
        return self.related('^')

    def verb_groups(self):
        return self.related('$')

    def similar_tos(self):
        return self.related('&')

    def nearest(self):
        return self.related('|')

@total_ordering
@python_2_unicode_compatible
class Lemma(_WordNetObject):
    """
    The lexical entry for a single morphological form of a
    sense-disambiguated word.

    Create a Lemma from lemma, pos, and morpho, or uri parameters where:
    <lemma> is the morphological form identifying the lemma
    <pos> is one of the module attributes 'n', 'v', 'a' or 'r'
    <morpho> is the morphological descriptor
    <uri> is the URI

    >>> LWN = WordNetCorpusReader()
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

    >>> synset = list(virtus.synsets())[0]
    >>> print(synset.definition())
    feeling no fear

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

    >>> metus = Lemma(LWN, lemma='metus', pos='n', morpho='n-s---mn4-', uri='m0918')
    >>> print(metus in list(virtus.antonyms()))
    True

    """

    __slots__ = [
        '_wordnet_corpus_reader',
        '_lemma',
        '_pos',
        '_morpho',
        '__synsets',
        '__related',
        '_literal',
        '_metonymic',
        '_metaphoric',
        '_uri',
        '_lang',
    ]

    def __init__(
        self,
        wordnet_corpus_reader,
        lemma,
        pos,
        morpho,
        uri,
        **kwargs
    ):
        self._wordnet_corpus_reader = wordnet_corpus_reader
        self._lemma = lemma
        self._pos = pos
        self._morpho = morpho
        self._uri = uri
        self.__synsets = None
        self.__related = None

    def uri(self):
        return self._uri

    def lemma(self):
        return self._lemma

    def pos(self):
        return self._pos

    def morpho(self):
        return self._morpho

    @property
    def _related(self):
        if self.__related is None:
            if not (self.lemma() and self.pos() and self.morpho()):
                results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/uri/{self.uri()}/relations/?format=json",
                    timeout=(30.0, 90.0)
                ).json()
                synsets_results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/uri/{self.uri()}/synsets/relations/?format=json",
                    timeout=(30.0, 90.0)
                ).json()
            else:
                results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/lemmas/{self.lemma()}/{self.pos() if self.pos() else '*'}"
                    f"/{self.morpho() if self.morpho() else '*'}/relations/?format=json",
                    timeout=(30.0, 90.0)
                ).json()
                synsets_results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/lemmas/{self.lemma()}/{self.pos() if self.pos() else '*'}"
                    f"/{self.morpho() if self.morpho() else '*'}/synsets/relations/?format=json",
                    timeout=(30.0, 90.0)
                ).json()
            if len(results) > 1:
                if not self._wordnet_corpus_reader._ignore_errors:
                    ambiguous = [f"{result['lemma']['lemma']} ({result['lemma']['morpho']})"
                                 for result in results]
                    raise WordNetError(f"can't disambiguate {', '.join(ambiguous)}")
            else:
                self.__related = results[0]['relations']
                self.__related.update(synsets_results[0]['relations'])
        return self.__related

    @property
    def _synsets(self):
        if self.__synsets is None:
            if not (self.lemma() and self.pos() and self.morpho()):
                results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/uri/{self.uri()}/synsets/?format=json",
                    timeout=(30.0, 90.0)
                ).json()
            else:
                results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/lemmas/{self.lemma()}/"
                    f"{self.pos() if self.pos() else '*'}/{self.morpho() if self.morpho() else '*'}/synsets/?format=json",
                    timeout=(30.0, 90.0)
                ).json()
            if len(results) > 1:
                if not self._wordnet_corpus_reader._ignore_errors:
                    ambiguous = [f"{result['lemma']} ({result['morpho']})"
                                 for result in results]
                    raise WordNetError(f"can't disambiguate {', '.join(ambiguous)}")
            else:
                self.__synsets = results[0]['synsets']
        return self.__synsets

    def synsets(self):
        return chain(self.literal(), self.metonymic(), self.metaphoric())

    def literal(self):
        return (
            Synset(self._wordnet_corpus_reader, synset['pos'], synset['offset'], synset['gloss'])
            for synset in self._synsets['literal']
        )

    def metonymic(self):
        return (
            Synset(self._wordnet_corpus_reader, synset['pos'], synset['offset'], synset['gloss'])
            for synset in self._synsets['metonymic']
        )

    def metaphoric(self):
        return (
            Synset(self._wordnet_corpus_reader, synset['pos'], synset['offset'], synset['gloss'])
            for synset in self._synsets['metaphoric']
        )

    def __repr__(self):
        return "Lemma(lemma='{}', pos='{}', morpho='{}', uri='{}')".format(self.lemma(), self.pos(), self.morpho(), self.uri())

    def related(self, relation_symbol=None):
        if relation_symbol and relation_types[relation_symbol] in self._related:
            return (
                Lemma(self._wordnet_corpus_reader,
                      lemma['lemma'], lemma['pos'], lemma['morpho'], lemma['uri'])
                for lemma in self._related[relation_types[relation_symbol]]
            )
        else:
            return (
                Lemma(self._wordnet_corpus_reader,
                      lemma['lemma'], lemma['pos'], lemma['morpho'], lemma['uri'])
                for relation_symbol in self.__related
                for lemma in self._related[relation_symbol]
            )

    def count(self):
        """Return the frequency count for this Lemma"""
        return self._wordnet_corpus_reader.lemma_count(self)


    def derivationally_related_forms(self):
        return self.related('\\')

    def pertainyms(self):
        return self.related('/')

    def participle(self):
        return self.related('<')

    def composed_of(self):
        return self.related('+c')

    def composes(self):
        return self.related('-c')

    def __hash__(self):
        return hash(self._lemma)

    def __eq__(self, other):
        return self._lemma == other._lemma and \
                self._pos == other._pos and \
                self._morpho == other._morpho and \
                self._uri == other._uri

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self._lemma < other._lemma


@python_2_unicode_compatible
class Semfield:
    """Create a Semfield from code and english parameters where:
    <code> is the semfield's DDCS code
    <english> is the semfield's DDCS descriptor

    >>> LWN = WordNetCorpusReader()
    >>> anatomy = Semfield(LWN, '611', "Human Anatomy, Cytology & Histology")
    >>> fat = LWN.synset('n#04089143')
    >>> print(fat in list(anatomy.synsets()))
    True

    """
    __slots__ = [
        '_wordnet_corpus_reader',
        '_code',
        '_english',
        '_synsets',
        '_lemmas',
        '_hypers',
        '_hypons',
    ]

    def __init__(self, wordnet_corpus_reader, code, english=None):
        self._wordnet_corpus_reader = wordnet_corpus_reader

        self._code = code
        self._english = english
        self._synsets = None
        self._lemmas = None

    def code(self):
        return self._code

    def english(self):
        if self._english is None:
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/semfields/{self.code()}/?format=json",
                timeout=(30.0, 90.0)
            )
            if results:
                if len(results.json()) > 1:
                    if self._wordnet_corpus_reader._ignore_errors:
                        ambiguous = [f"'{semfield['english']}'" for semfield in results]
                        raise WordNetError(f"can't disambiguate {', '.join(ambiguous)}")
                else:
                    self._english = results.json()[0]['english']
        return self._english

    def synsets(self):
        if self._synsets is None:
            english = re.sub(' ', '_', self.english())
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/semfields/{self.code()}/{english}/synsets/?format=json",
                timeout=(30.0, 90.0)
            )
            if results:
                self._synsets = (
                    Synset(self._wordnet_corpus_reader, synset['pos'], synset['offset'], synset['gloss'])
                    for synset in results.json()[0]['synsets']
            )
            else:
                self._synsets = []
        return self._synsets

    def lemmas(self):
        if self._lemmas is None:
            english = re.sub(' ', '_', self.english())
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/semfields/{self.code()}/{english}/lemmas/?format=json",
                timeout=(30.0, 90.0)
            )
            if results:
                self._lemmas = (
                    Lemma(self._wordnet_corpus_reader, lemma['lemma'], lemma['pos'], lemma['morpho'], lemma['uri'])
                    for lemma in results.json()[0]['lemmas']
                )
            else:
                self._lemmas = []
        return self._lemmas

    def __repr__(self):
        return "Semfield(code='{}', english='{}')".format(self.code(), self.english())


@total_ordering
@python_2_unicode_compatible
class Synset(_WordNetObject):
    """Create a Synset from pos and offset parameters where:
    <pos> is the synset's part of speech
    <offset> is the offset ID of the synset.

    >>> LWN = WordNetCorpusReader()
    >>> s1 = Synset(LWN, pos='n', offset='02542418', gloss='a short stabbing weapon with a pointed blade')
    >>> print(list(s1.semfields()))
    [Semfield(code='739.7', english='Arms And Armour')]

    Synset attributes, accessible via methods with the same name:

    - pos: The synset's part of speech, 'n', 'v', 'a', or 'r'
    - offset: The unique offset ID of the synset
    - lemmas: A list of the Lemma objects for this synset
    - definition: The definition for this synset

    >>> for lemma in s1.lemmas():
    ...     print(lemma.lemma())
    sica
    clunaculum
    gladiolus
    parazonium
    pugio
    sicula
    sicula
    pugiunculus

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

    >>> s2 = Synset(LWN, pos='n', offset='03457380', gloss='a cutting or thrusting weapon with a long blade')
    >>> hyponym = list(s2.hyponyms())[0]
    >>> print(hyponym.id(), hyponym.definition())
    n#02235272 broad blade; used for cutting rather than stabbing

    Additionally, Synsets support the following methods specific to the
    hypernym relation:

    - root_hypernyms
    - common_hypernyms
    - lowest_common_hypernyms

    >>> print(s1.root_hypernyms())
    [Synset(pos='n', offset='00001740', definition='anything having existence (living or nonliving)')]
    >>> print(s1.lowest_common_hypernyms(s2))
    [Synset(pos='n', offset='03601056', definition='weaponry used in fighting or hunting')]
    >>> print(s1.shortest_path_distance(s2))
    3

    Note that Synsets do not support the following relations because
    these are defined by WordNet as lexical relations:

    - derivationally_related_forms
    - pertainyms
    - composed_of
    - composes
    - participle
    """

    __slots__ = [
        '_pos',
        '_offset',
        '_lemmas',
        '_definition',
        '_semfields',
        '_sentiment',
        '__related',
        '_max_depth',
        '_min_depth',
        '_all_hypernyms'
    ]

    def __init__(self, wordnet_corpus_reader, pos, offset, gloss, semfield=None):
        self._wordnet_corpus_reader = wordnet_corpus_reader

        self._pos = pos
        self._offset = offset
        self._definition = gloss.split(':')[0]
        self._examples = None
        self._lemmas = None
        self.__related = None
        self._semfields = None
        self._sentiment = None
        self._all_hypernyms = None

    def id(self):
        return "{}#{}".format(self.pos(), self.offset())

    def semfields(self):
        if self._semfields is None:
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/synsets/{self.pos()}/{self.offset()}/?format=json",
                timeout=(30.0, 90.0)
            )
            if results:
                self._semfields = results.json()['semfield']
            else:
                self._semfields = []
        return (
            Semfield(self._wordnet_corpus_reader, semfield['code'], semfield['english'])
            for semfield in self._semfields
        )

    def sentiment(self):
        if self._sentiment is None:
            results = requests.get(
                    f"{self._wordnet_corpus_reader.host()}/api/synsets/{self.pos()}/{self.offset()}/sentiment/?format=json",
                    timeout=(30.0, 90.0)
                )
            if results:
                self._sentiment = results.json()['sentiment']
        return self._sentiment

    def positivity(self):
        return self._sentiment['positivity']

    def negativity(self):
        return self._sentiment['negativity']

    def objectivity(self):
        return self._sentiment['objectivity']

    def pos(self):
        return self._pos

    def offset(self):
        return self._offset

    def definition(self):
        return self._definition

    def examples(self):
        if self._examples is None:
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/synsets/{self.pos()}/{self.offset()}/examples/?format=json",
                timeout=(30.0, 90.0)
            )
            if results:
                self._examples = results.json()['examples']
        return self._examples

    def _needs_root(self):
        return self._pos == 'n' or self._pos == 'v'

    def lemmas(self):
        '''Return all the lemma objects associated with the synset'''
        if self._lemmas is None:
            results = requests.get(
                f"{self._wordnet_corpus_reader.host()}/api/synsets/{self.pos()}/{self.offset()}/lemmas/?format=json",
                timeout=(30.0, 90.0)
            )
            if results:
                self._lemmas = results.json()['lemmas']
            else:
                self._lemmas = []
        return (
            Lemma(self._wordnet_corpus_reader, lemma['lemma'], lemma['pos'], lemma['morpho'], lemma['uri'])
            for lemma in self._lemmas
        )

    def root_hypernyms(self):
        """Get the topmost hypernyms of this synset in WordNet."""

        result = []
        seen = set()
        todo = [self]
        while todo:
            next_synset = todo.pop()
            if next_synset not in seen:
                seen.add(next_synset)
                next_hypernyms = (
                    next_synset.hypernyms()
                )
                if not next_hypernyms:
                    result.append(next_synset)
                else:
                    todo.extend(next_hypernyms)
        return result

    def max_depth(self):
        """
        :return: The length of the longest hypernym path from this
        synset to the root.
        """

        if "_max_depth" not in self.__dict__:
            hypernyms = self.hypernyms()
            if not hypernyms:
                self._max_depth = 0
            else:
                self._max_depth = 1 + max(h.max_depth() for h in hypernyms)
        return self._max_depth

    def min_depth(self):
        """
        :return: The length of the shortest hypernym path from this
        synset to the root.
        """

        if "_min_depth" not in self.__dict__:
            hypernyms = self.hypernyms()
            if not hypernyms:
                self._min_depth = 0
            else:
                self._min_depth = 1 + min(h.min_depth() for h in hypernyms)
        return self._min_depth

    def closure(self, rel, depth=-1):
        """Return the transitive closure of source under the rel
        relationship, breadth-first
        """
        from nltk.util import breadth_first

        synset_ids = []
        for synset in breadth_first(self, rel, depth):
            if synset.id() != self.id():
                if synset.id() not in synset_ids:
                    synset_ids.append(synset.id())
                    yield synset

    def hypernym_paths(self):
        """
        Get the path(s) from this synset to the root, where each path is a
        list of the synset nodes traversed on the way to the root.

        :return: A list of lists, where each list gives the node sequence
           connecting the initial ``Synset`` node and a root node.
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
        """
        Find all synsets that are hypernyms of this synset and the
        other synset.

        :type other: Synset
        :param other: other input synset.
        :return: The synsets that are hypernyms of both synsets.
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
        """
        Get a list of lowest synset(s) that both synsets have as a hypernym.
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
        """
        synsets = self.common_hypernyms(other)
        if simulate_root:
            root = Synset(self._wordnet_corpus_reader, self.pos(), '00000000', '')
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
        """
        Get the path(s) from this synset to the root, counting the distance
        of each node from the initial node on the way. A set of
        (synset, distance) tuples is returned.

        :type distance: int
        :param distance: the distance (number of edges) from this hypernym to
            the original hypernym ``Synset`` on which this method was called.
        :return: A set of ``(Synset, int)`` tuples where each ``Synset`` is
           a hypernym of the first ``Synset``.
        """
        distances = set([(self, distance)])
        for hypernym in self._hypernyms():
            distances |= hypernym.hypernym_distances(distance + 1, simulate_root=False)
        if simulate_root:
            root = Synset(self._wordnet_corpus_reader, self.pos(), '00000000')
            root_distance = max(distances, key=itemgetter(1))[1]
            distances.add((root, root_distance + 1))
        return distances

    def _shortest_hypernym_paths(self, simulate_root):
        if self.offset == '00000000':
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
            root = Synset(self._wordnet_corpus_reader, self.pos(), '00000000', "")
            path[root] = max(path.values()) + 1

        return path

    def shortest_path_distance(self, other, simulate_root=False):
        """
        Returns the distance of the shortest path linking the two synsets (if
        one exists). For each synset, all the ancestor nodes and their
        distances are recorded and compared. The ancestor node common to both
        synsets that can be reached with the minimum number of traversals is
        used. If no ancestor nodes are common, None is returned. If a node is
        compared with itself 0 is returned.

        :type other: Synset
        :param other: The Synset to which the shortest path will be found.
        :return: The number of edges in the shortest path connecting the two
            nodes, or None if no path exists.
        """

        if self == other:
            return 0

        dist_dict1 = self._shortest_hypernym_paths(simulate_root)
        dist_dict2 = other._shortest_hypernym_paths(simulate_root)

        # For each ancestor synset common to both subject synsets, find the
        # connecting path length. Return the shortest of these.

        inf = float('inf')
        path_distance = inf
        for synset, d1 in iteritems(dist_dict1):
            d2 = dist_dict2.get(synset, inf)
            path_distance = min(path_distance, d1 + d2)

        return None if math.isinf(path_distance) else path_distance

    def tree(self, rel, depth=-1, cut_mark=None):
        """
        :param rel:
        :param depth:
        :param cut_mark:
        :return:
        """

        tree = [self]
        if depth != 0:
            tree += [x.tree(rel, depth - 1, cut_mark) for x in self.related(rel, sort=True)]
        elif cut_mark:
            tree += [cut_mark]
        return tree

    # interface to similarity methods
    def path_similarity(self, other, verbose=False, simulate_root=True):
        """
        Path Distance Similarity:
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
            share a single root which disallows this metric from working for
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
        """

        distance = self.shortest_path_distance(
            other, simulate_root=simulate_root and self._needs_root()
        )
        if distance is None or distance < 0:
            return None
        return 1.0 / (distance + 1)

    def lch_similarity(self, other, verbose=False, simulate_root=True):
        """
        Leacock Chodorow Similarity:
        Return a score denoting how similar two word senses are, based on the
        shortest path that connects the senses (as above) and the maximum depth
        of the taxonomy in which the senses occur. The relationship is given as
        -log(p/2d) where p is the shortest path length and d is the taxonomy
        depth.

        :type  other: Synset
        :param other: The ``Synset`` that this ``Synset`` is being compared to.
        :type simulate_root: bool
        :param simulate_root: The various verb taxonomies do not
            share a single root which disallows this metric from working for
            synsets that are not connected. This flag (True by default)
            creates a fake root that connects all the taxonomies. Set it
            to false to disable this behavior. For the noun taxonomy,
            there is usually a default root except for WordNet version 1.6.
            If you are using wordnet 1.6, a fake root will be added for nouns
            as well.
        :return: A score denoting the similarity of the two ``Synset`` objects,
            normally greater than 0. None is returned if no connecting path
            could be found. If a ``Synset`` is compared with itself, the
            maximum score is returned, which varies depending on the taxonomy
            depth.
        """

        if self._pos != other._pos:
            raise WordNetError(
                'Computing the lch similarity requires '
                '%s and %s to have the same part of speech.' % (self, other)
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
        """
        Wu-Palmer Similarity:
        Return a score denoting how similar two word senses are, based on the
        depth of the two senses in the taxonomy and that of their Least Common
        Subsumer (most specific ancestor node). Previously, the scores computed
        by this implementation did _not_ always agree with those given by
        Pedersen's Perl implementation of WordNet Similarity. However, with
        the addition of the simulate_root flag (see below), the score for
        verbs now almost always agree but not always for nouns.

        The LCS does not necessarily feature in the shortest path connecting
        the two senses, as it is by definition the common ancestor deepest in
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
            to false to disable this behavior. For the noun taxonomy,
            there is usually a default root except for WordNet version 1.6.
            If you are using wordnet 1.6, a fake root will be added for nouns
            as well.
        :return: A float score denoting the similarity of the two ``Synset``
            objects, normally greater than zero. If no connecting path between
            the two senses can be found, None is returned.

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

    def res_similarity(self, other, ic, verbose=False):
        """
        Resnik Similarity:
        Return a score denoting how similar two word senses are, based on the
        Information Content (IC) of the Least Common Subsumer (most specific
        ancestor node).

        :type  other: Synset
        :param other: The ``Synset`` that this ``Synset`` is being compared to.
        :type ic: dict
        :param ic: an information content object (as returned by
            ``nltk.corpus.wordnet_ic.ic()``).
        :return: A float score denoting the similarity of the two ``Synset``
            objects. Synsets whose LCS is the root node of the taxonomy will
            have a score of 0 (e.g. N['dog'][0] and N['table'][0]).
        """

        ic1, ic2, lcs_ic = _lcs_ic(self, other, ic)
        return lcs_ic

    def jcn_similarity(self, other, ic, verbose=False):
        """
        Jiang-Conrath Similarity:
        Return a score denoting how similar two word senses are, based on the
        Information Content (IC) of the Least Common Subsumer (most specific
        ancestor node) and that of the two input Synsets. The relationship is
        given by the equation 1 / (IC(s1) + IC(s2) - 2 * IC(lcs)).

        :type  other: Synset
        :param other: The ``Synset`` that this ``Synset`` is being compared to.
        :type  ic: dict
        :param ic: an information content object (as returned by
            ``nltk.corpus.wordnet_ic.ic()``).
        :return: A float score denoting the similarity of the two ``Synset``
            objects.
        """

        if self == other:
            return _INF

        ic1, ic2, lcs_ic = _lcs_ic(self, other, ic)

        # If either of the input synsets are the root synset, or have a
        # frequency of 0 (sparse data problem), return 0.
        if ic1 == 0 or ic2 == 0:
            return 0

        ic_difference = ic1 + ic2 - 2 * lcs_ic

        if ic_difference == 0:
            return _INF

        return 1 / ic_difference

    def lin_similarity(self, other, ic, verbose=False):
        """
        Lin Similarity:
        Return a score denoting how similar two word senses are, based on the
        Information Content (IC) of the Least Common Subsumer (most specific
        ancestor node) and that of the two input Synsets. The relationship is
        given by the equation 2 * IC(lcs) / (IC(s1) + IC(s2)).

        :type other: Synset
        :param other: The ``Synset`` that this ``Synset`` is being compared to.
        :type ic: dict
        :param ic: an information content object (as returned by
            ``nltk.corpus.wordnet_ic.ic()``).
        :return: A float score denoting the similarity of the two ``Synset``
            objects, in the range 0 to 1.
        """

        ic1, ic2, lcs_ic = _lcs_ic(self, other, ic)
        return (2.0 * lcs_ic) / (ic1 + ic2)

    def _iter_hypernym_lists(self):
        """
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
        return "Synset(pos='{}', offset='{}', definition='{}')".format(self.pos(), self.offset(), self.definition())

    def related(self, relation_symbol=None, sort=True):
        get_synset = self._wordnet_corpus_reader.synset_from_pos_and_offset
        if relation_symbol and relation_types[relation_symbol] in self._related:
            r = [get_synset(synset['pos'], synset['offset']) for synset in self._related[relation_types[relation_symbol]]]
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
                timeout=(30.0, 90.0)
            )
            if results:
                self.__related = results.json()['relations']
            else:
                self.__related = []
        return self.__related

    def __eq__(self, other):
        return self._pos == other._pos and \
                self._offset == other._offset

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self._pos != other._pos:
            raise WordNetError("operation undefined for '{}' and '{}'".format(self._pos, other._pos))
        return self._offset < other._offset

    def __hash__(self):
        return hash(f"{self.pos()}#{self.offset()}")


######################################################################
# WordNet Corpus Reader
######################################################################
class WordNetCorpusReader(CorpusReader):
    """
    A corpus reader used to access the Latin WordNet.

    :param host: The Latin WordNet host address.

    >>> LWN = WordNetCorpusReader()
    >>> animus = LWN.lemma('animus', 'n', 'n-s---mn2-')
    >>> print(animus)
    Lemma(lemma='animus', pos='n', morpho='n-s---mn2-', uri='a2046')
    >>> dico = LWN.lemmas('dico', 'v')
    >>> print(list(dico))
    [Lemma(lemma='dico', pos='v', morpho='v1spia--3-', uri='d1350'), Lemma(lemma='dico', pos='v', morpho='v1spia--1-', uri='d1349')]
    >>> virtus = LWN.lemmas_from_uri('u0800')
    >>> print(virtus)
    [Lemma(lemma='uirtus', pos='n', morpho='n-s---fn3-', uri='u0800')]
    >>> courage = LWN.synset('n#03805961')
    >>> print(courage)
    Synset(pos='n', offset='03805961', definition='a quality of spirit that enables you to face danger of pain without showing fear')
    >>> adverbs = LWN.synsets('r')
    >>> print(len(list(adverbs)) > 3600)
    True

    """

    _ENCODING = 'utf8'

    # { Part-of-speech constants
    ADJ, ADV, NOUN, VERB = 'a', 'r', 'n', 'v'
    # }

    # { Part of speech constants
    _pos_numbers = {NOUN: 1, VERB: 2, ADJ: 3, ADV: 4, }
    _pos_names = dict(tup[::-1] for tup in _pos_numbers.items())
    # }

    def __init__(self, host="http://latinwordnet.exeter.ac.uk", ignore_errors=False):
        """
        Construct a new WordNet corpus reader, using the host address
        """
        super(WordNetCorpusReader, self).__init__(
            encoding=self._ENCODING, root='', fileids=None
        )
        self._host = host
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

    def _compute_max_depth(self, pos, simulate_root):
        """
        Compute the max depth for the given part of speech.  This is
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

    def get_status(self):
        results = requests.get(
            f"{self.host()}/api/status/?format=json",
            timeout=(30.0, 90.0)
        )
        return results


    #############################################################
    # Loading Lemmas
    #############################################################
    def lemma(self, lemma, pos, morpho):
        '''Return lemma object that matches the lemma, pos, morpho'''
        if pos in self._lemma_cache[lemma]:
            if morpho in self._lemma_cache[lemma][pos]:
                if len(self._lemma_cache[lemma][pos][morpho]) > 1:
                    ambiguous = " or ".join([f"lemma_by_uri({uri})"
                                             for uri in self._lemma_cache[lemma][pos][morpho]
                                             ])
                    if self._ignore_errors:
                        print(f"can't disambiguate {lemma} ({morpho}): try {ambiguous}")
                    else:
                        raise WordNetError(f"can't disambiguate {lemma} ({morpho}): try {ambiguous}")
                else:
                    return self._lemma_cache[lemma][pos][morpho].values()

        results = self.json = requests.get(
                f"{self.host()}/api/lemmas/{lemma if lemma else '*'}/{pos if pos else '*'}"
                f"/{morpho if morpho else '*'}?format=json",
                timeout=(30.0, 90.0)
            ).json()
        if len(results) > 1:
            ambiguous = [f"{result['lemma']} ({result['morpho']})"
                         for result in results]
            raise WordNetError(f"can't disambiguate {', '.join(ambiguous)}")
        elif len(results) == 0:
            raise WordNetError(f"'{lemma}'' ({pos}) not found")
        l = Lemma(self, **results[0])
        self._lemma_cache[lemma][pos][morpho][results[0]['uri']] = l
        return l

    def lemma_from_uri(self, uri):
        results = self.json = requests.get(
            f"{self.host()}/api/uri/{uri}?format=json",
            timeout=(30.0, 90.0)
        ).json()
        if len(results) > 1:
            ambiguous = [f"{result['lemma']} ({result['morpho']})"
                         for result in results]
            raise WordNetError(f"can't disambiguate {', '.join(ambiguous)}")
        l = Lemma(self, **results[0])
        self._lemma_cache[results[0]['lemma']][results[0]['pos']][results[0]['morpho']][results[0]['uri']] = l
        return l

    def semfield(self, code, english):
        english = re.sub(' ', '_', english)

        # load semfield information
        results = self.json = requests.get(
            f"{self.host()}/api/semfields/{code}/{english}/?format=json",
            timeout=(30.0, 90.0)
        ).json()

        if len(results) == 0:
            raise WordNetError(f"semfield {code} '{english}' not found")

        # Return the semfield object.
        return Semfield(self, results[0]['code'], results[0]['english'])

    #############################################################
    # Loading Synsets
    #############################################################
    def synset(self, id):
        pos, offset = SENSENUM_RE.search(id).groups()

        # load synset information
        synset = self.synset_from_pos_and_offset(pos, offset)

        if synset is None:
            raise WordNetError(f"synset {id} not found")

        # Return the synset object.
        return synset

    def synset_from_pos_and_offset(self, pos, offset):
        # Check to see if the synset is in the cache
        if offset in self._synset_cache[pos]:
            return self._synset_cache[pos][offset]

        results = requests.get(
                f"{self.host()}/api/synsets/{pos}/{offset}?format=json",
                timeout=(30.0, 90.0)
            ).json()
        if len(results) != 0:
            synset = Synset(self, **results)
            self._synset_cache[pos][offset] = synset
            return synset

    #############################################################
    # Retrieve synsets and lemmas.
    #############################################################
    def lemmas(self, lemma=None, pos=None, morpho=None):
        """Return all Lemma objects with a name matching the specified lemma
        name, part of speech tag or morphological descriptor."""

        results = requests.get(
                    f"{self.host()}/api/lemmas/{lemma if lemma else '*'}/{pos if pos else '*'}/"
                    f"{morpho if morpho else '*'}?format=json",
                    timeout=(30.0, 90.0)
                ).json()
        return (
            Lemma(self, lemma['lemma'], lemma['pos'], lemma['morpho'], lemma['uri'])
            for lemma in results
        )

    def lemmas_from_uri(self, uri):
        results = self.json = requests.get(
            f"{self.host()}/api/uri/{uri}?format=json",
            timeout=(30.0, 90.0)
        ).json()
        lemmas_list = []
        for result in results:
            l = Lemma(self, **result)
            self._lemma_cache[result['lemma']][result['pos']][result['morpho']][result['uri']] = l
            lemmas_list.append(l)
        return lemmas_list


    def synsets(self, pos=None):
        """Load all synsets for a given part of speech, if specified.

        """
        synsets_list = []

        results = requests.get(
            f"{self.host()}/api/synsets/{pos if pos else '*'}/?format=json",
            timeout=(30.0, 90.0)
        ).json()
        synsets_list.extend(results['results'])

        while results["next"]:
            results = requests.get(results["next"], timeout=(30.0, 90.0)).json()
            synsets_list.extend(results['results'])

        return (
            Synset(self, synset['pos'], synset['offset'], synset['gloss']) for synset in
            synsets_list
        )

    def semfields(self, code=None):
        """Load all semfields for a given code, if specified.

        """
        semfields_list = []
        if code is None:
            results = requests.get(
                f"{self.host()}/api/semfields/?format=json",
                timeout=(30.0, 90.0)
            ).json()
            semfields_list.extend(results['results'])

            while results["next"]:
                results = requests.get(results["next"], timeout=(30.0, 90.0)).json()
                semfields_list.extend(results['results'])
        else:
            results = requests.get(
                f"{self.host()}/api/semfields/{code}/?format=json",
                timeout=(30.0, 90.0)
            ).json()
            semfields_list.extend(results)
        return (
            Semfield(self, semfield['code'], semfield['english']) for semfield in
            semfields_list
        )

    #############################################################
    # Similarity
    #############################################################
    def path_similarity(self, synset1, synset2, verbose=False, simulate_root=True):
        return synset1.path_similarity(synset2, verbose, simulate_root)

    path_similarity.__doc__ = Synset.path_similarity.__doc__

    def lch_similarity(self, synset1, synset2, verbose=False, simulate_root=True):
        return synset1.lch_similarity(synset2, verbose, simulate_root)

    lch_similarity.__doc__ = Synset.lch_similarity.__doc__

    def wup_similarity(self, synset1, synset2, verbose=False, simulate_root=True):
        return synset1.wup_similarity(synset2, verbose, simulate_root)

    wup_similarity.__doc__ = Synset.wup_similarity.__doc__

    def res_similarity(self, synset1, synset2, ic, verbose=False):
        return synset1.res_similarity(synset2, ic, verbose)

    res_similarity.__doc__ = Synset.res_similarity.__doc__

    def jcn_similarity(self, synset1, synset2, ic, verbose=False):
        return synset1.jcn_similarity(synset2, ic, verbose)

    jcn_similarity.__doc__ = Synset.jcn_similarity.__doc__

    def lin_similarity(self, synset1, synset2, ic, verbose=False):
        return synset1.lin_similarity(synset2, ic, verbose)

    lin_similarity.__doc__ = Synset.lin_similarity.__doc__

    #############################################################
    # Lemmatizer
    #############################################################
    def lemmatize(self, form: str, morpho: str = None):
        """
        Lemmatizes a Latin form.

        :param form: The form to lemmatize, as a string
        :param morpho: Optional 10-place morphological descriptor, used as a filter
        :return: A list of matching Lemma objects

        >>> LWN = WordNetCorpusReader()
        >>> print(list(LWN.lemmatize('pumice')))
        [Lemma(lemma='pumex', pos='n', morpho='n-s---cn3-', uri='p4512')]

        """

        form = form.translate(punctuation)
        if form:
            results = requests.get(
                f"{self.host()}/lemmatize/{form}/{morpho if morpho else ''}?format=json",
                timeout=(30.0, 90.0)
            )
            if results and results.json():
                return (
                    Lemma(self, result['lemma']['lemma'], result['lemma']['morpho'][0], result['lemma']['morpho'],
                              result['lemma']['uri'])
                        for result in results.json()
                )
        return []

    #############################################################
    # Translater
    #############################################################
    def translate(self, language: str, form: str, pos: str = "*"):
        """
        Translates an English, French, Spanish, or Italian word into Latin.

        :param language: 'en', 'fr', 'es', 'it' indicating the source language
        :param form: The word to translate
        :param pos: Optionally, a part-of-speech ('n', 'v', 'a', 'r') indicator
        used as a filter
        :return: A list of Lemma objects

        >>> LWN = WordNetCorpusReader()
        >>> offspring_translations = list(LWN.translate('en', 'offspring'))
        >>> print('pusio' in [lemma.lemma() for lemma in offspring_translations])
        True

        """
        pos = f"{pos}/" if pos else ""
        results = requests.get(
            f"{self.host()}/translate/{language}/{form}/{pos}?format=json",
            timeout=(30.0, 90.0)
        ).json()
        return (
            Lemma(self, lemma['lemma'], lemma['pos'], lemma['morpho'], lemma['uri'])
            for lemma in results
        )


    #############################################################
    # Create information content from corpus
    #############################################################
    def ic(self, corpus, weight_senses_equally=False, smoothing=1.0):
        """
        Creates an information content lookup dictionary from a corpus.

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
        counts = FreqDist()
        for ww in corpus.words():
            results = self.lemmatize(ww)
            for lemma in results:
                counts[lemma] += 1

        ic = {}
        for pp in POS_LIST:
            ic[pp] = defaultdict(float)

        # Initialize the counts with the smoothing value
        if smoothing > 0.0:
            for ss in self.synsets():
                pos = ss._pos
                ic[pos][ss._offset] = smoothing

        for ww in counts:
            possible_synsets = ww.synsets()
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
        return ic

    def write_ic(self, corpus_name, ic):
        get_synset = self.synset_from_pos_and_offset

        with codecs.open('ic-latin-{}.dat'.format(corpus_name), 'w', 'utf8') as fp:
            fp.write('lwnver:{}\n'.format(self.get_status()['last_modified']))
            for pp in POS_LIST:
                for offset in ic[pp]:
                    ss = get_synset(pp, offset)
                    if len(ss.hypernyms()) == 0:
                        fp.write('{} {} ROOT\n'.format(ss.id(), ic[pp][offset]))
                    else:
                        fp.write('{} {}\n'.format(ss.id(), ic[pp][offset]))


######################################################################
# WordNet Information Content Corpus Reader
######################################################################
class WordNetICCorpusReader(CorpusReader):
    """
    A corpus reader for the WordNet information content corpus.
    """

    def __init__(self, root='', fileids=None):
        CorpusReader.__init__(self, root, fileids, encoding='utf8')

    # this load function would be more efficient if the data was pickled
    # Note that we can't use NLTK's frequency distributions because
    # synsets are overlapping (each instance of a synset also counts
    # as an instance of its hypernyms)
    def ic(self, icfile):
        """
        Load an information content file from the wordnet_ic corpus
        and return a dictionary.  This dictionary has just two keys,
        NOUN and VERB, whose values are dictionaries that map from
        synsets to information content values.

        :type icfile: str
        :param icfile: The name of the wordnet_ic file (e.g. "ic-latin-library.dat")
        :return: An information content dictionary
        """
        ic = {}
        ic[NOUN] = defaultdict(float)
        ic[VERB] = defaultdict(float)
        for num, line in enumerate(self.open(icfile)):
            if num == 0:  # skip the header
                continue
            fields = line.split()
            offset = int(fields[0][:-1])
            value = float(fields[1])
            pos = _get_pos(fields[0])
            if len(fields) == 3 and fields[2] == "ROOT":
                # Store root count.
                ic[pos][0] += value
            if value != 0:
                ic[pos][offset] = value
        return ic


######################################################################
# Similarity metrics
######################################################################
def path_similarity(synset1, synset2, verbose=False, simulate_root=True):
    return synset1.path_similarity(synset2, verbose, simulate_root)


def lch_similarity(synset1, synset2, verbose=False, simulate_root=True):
    return synset1.lch_similarity(synset2, verbose, simulate_root)


def wup_similarity(synset1, synset2, verbose=False, simulate_root=True):
    return synset1.wup_similarity(synset2, verbose, simulate_root)


def res_similarity(synset1, synset2, ic, verbose=False):
    return synset1.res_similarity(synset2, ic, verbose)


def jcn_similarity(synset1, synset2, ic, verbose=False):
    return synset1.jcn_similarity(synset2, ic, verbose)


def lin_similarity(synset1, synset2, ic, verbose=False):
    return synset1.lin_similarity(synset2, ic, verbose)


path_similarity.__doc__ = Synset.path_similarity.__doc__
lch_similarity.__doc__ = Synset.lch_similarity.__doc__
wup_similarity.__doc__ = Synset.wup_similarity.__doc__
res_similarity.__doc__ = Synset.res_similarity.__doc__
jcn_similarity.__doc__ = Synset.jcn_similarity.__doc__
lin_similarity.__doc__ = Synset.lin_similarity.__doc__


def _lcs_ic(synset1, synset2, ic, verbose=False):
    """
    Get the information content of the least common subsumer that has
    the highest information content value.  If two nodes have no
    explicit common subsumer, assume that they share an artificial
    root node that is the hypernym of all explicit roots.

    :type synset1: Synset
    :param synset1: First input synset.
    :type synset2: Synset
    :param synset2: Second input synset.  Must be the same part of
    speech as the first synset.
    :type  ic: dict
    :param ic: an information content object (as returned by ``load_ic()``).
    :return: The information content of the two synsets and their most
    informative subsumer
    """
    if synset1._pos != synset2._pos:
        raise WordNetError(
            'Computing the least common subsumer requires '
            '%s and %s to have the same part of speech.' % (synset1, synset2)
        )

    ic1 = information_content(synset1, ic)
    ic2 = information_content(synset2, ic)
    subsumers = synset1.common_hypernyms(synset2)
    if len(subsumers) == 0:
        subsumer_ic = 0
    else:
        subsumer_ic = max(information_content(s, ic) for s in subsumers)

    if verbose:
        print("> LCS Subsumer by content:", subsumer_ic)

    return ic1, ic2, subsumer_ic


# Utility functions
def information_content(synset, ic):
    try:
        icpos = ic[synset._pos]
    except KeyError:
        msg = 'Information content file has no entries for part-of-speech: %s'
        raise WordNetError(msg % synset._pos)

    counts = icpos[synset._offset]
    if counts == 0:
        return _INF
    else:
        return -math.log(counts / icpos[0])


# get the part of speech (NOUN or VERB) from the information content record
# (each identifier has a 'n' or 'v' suffix)
def _get_pos(field):
    if field[-1] == 'n':
        return NOUN
    elif field[-1] == 'v':
        return VERB
    else:
        msg = (
            "Unidentified part of speech in WordNet Information Content file "
            "for field %s" % field
        )
        raise ValueError(msg)


# unload corpus after tests
def teardown_module(module=None):
    from nltk.corpus import wordnet

    wordnet._unload()


relation_types = {
    '!': 'antonyms',
    '@': 'hypernyms',
    '~': 'hyponyms',
    '#m': 'member-of',
    '#s': 'substance-of',
    '#p': 'part-of',
    '%m': 'has-member',
    '%s': 'has-substance',
    '%p': 'has-part',
    '=': 'attribute-of',
    '|': 'nearest',
    '+r': 'has-role',
    '-r': 'is-role-of',
    '*': 'entails',
    '>': 'causes',
    '^': 'also-see',
    '$': 'verb-group',
    '&': 'similar-to',
    '<': 'participle',
    '+c': 'composed-of',
    '-c': 'composes',
    '\\': 'derived-from',
    '/': 'related-to',
    }

# Example usage
if __name__ == "__main__":
    LWN = WordNetCorpusReader()

    lemmas = list(LWN.lemmatize('virtutem'))
    print(lemmas)
    virtus = LWN.lemma_from_uri('u0800')
    print(virtus)
    print(list(virtus.antonyms()))
    print(list(virtus.hypernyms()))
    animus = LWN.lemma('animus', 'n', 'n-s---mn2-')
    print(animus)
    for synset in set(virtus.synsets()).intersection(set(animus.synsets())):
        print(list(synset.semfields()), '>>', list(synset.lemmas()))

    courage = list(LWN.translate('en', 'courage', 'n'))
    for lemma in courage:
        print(lemma)

    s1 = LWN.synset('n#02542418')
    print(s1.id(), '=', s1.definition())
    s2 = LWN.synset('n#03457380')
    print(s2.id(), '=', s2.definition())

    print('Common hypernyms:', list(s1.common_hypernyms(s2)))
    print('Lowest common hypernyms:', list(s1.lowest_common_hypernyms(s2)))
    print('Shortest path distance:', s1.shortest_path_distance(s2))
