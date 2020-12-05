"""Stem Latin words with an implementation of the Schinke Latin stemming
algorithm (Schinke R, Greengrass M, Robertson AM and Willett P. (1996). 'A
stemming algorithm for Latin text databases'. Journal of Documentation, 52:
172-187).

.. todo::
   Make this stemmer like lemma, with import from ``stem`` dir.

"""

__author__ = ["Luke Hollis <lukehollis@gmail.com>"]
__license__ = "MIT License. See LICENSE."

import re

from cltk.stops.lat import STOPS


def _checkremove_que(word):
    """If word ends in -que and if word is not in pass list, strip -que"""

    in_que_pass_list = False

    que_pass_list = [
        "atque",
        "quoque",
        "neque",
        "itaque",
        "absque",
        "apsque",
        "abusque",
        "adaeque",
        "adusque",
        "denique",
        "deque",
        "susque",
        "oblique",
        "peraeque",
        "plenisque",
        "quandoque",
        "quisque",
        "quaeque",
        "cuiusque",
        "cuique",
        "quemque",
        "quamque",
        "quaque",
        "quique",
        "quorumque",
        "quarumque",
        "quibusque",
        "quosque",
        "quasque",
        "quotusquisque",
        "quousque",
        "ubique",
        "undique",
        "usque",
        "uterque",
        "utique",
        "utroque",
        "utribique",
        "torque",
        "coque",
        "concoque",
        "contorque",
        "detorque",
        "decoque",
        "excoque",
        "extorque",
        "obtorque",
        "optorque",
        "retorque",
        "recoque",
        "attorque",
        "incoque",
        "intorque",
        "praetorque",
    ]

    if word not in que_pass_list:
        word = re.sub(r"que$", "", word)
    else:
        in_que_pass_list = True

    return word, in_que_pass_list


def _matchremove_simple_endings(word):
    """Remove the noun, adjective, adverb word endings"""

    was_stemmed = False

    # noun, adjective, and adverb word endings sorted by charlen, then alph
    simple_endings = [
        "ibus",
        "ius",
        "ae",
        "am",
        "as",
        "em",
        "es",
        "ia",
        "is",
        "nt",
        "os",
        "ud",
        "um",
        "us",
        "a",
        "e",
        "i",
        "o",
        "u",
    ]

    for ending in simple_endings:
        if word.endswith(ending):
            word = re.sub(r"{0}$".format(ending), "", word)
            was_stemmed = True
            break

    return word, was_stemmed


def _matchremove_verb_endings(word):
    """Remove the verb endings"""

    i_verb_endings = ["iuntur", "erunt", "untur", "iunt", "unt"]

    bi_verb_endings = ["beris", "bor", "bo"]

    eri_verb_endings = ["ero"]

    verb_endings = [
        "mini",
        "ntur",
        "stis",
        "mur",
        "mus",
        "ris",
        "sti",
        "tis",
        "tur",
        "ns",
        "nt",
        "ri",
        "m",
        "r",
        "s",
        "t",
    ]

    # replace i verb endings with i
    for ending in i_verb_endings:
        if word.endswith(ending):
            word = re.sub(r"{0}$".format(ending), "i", word)
            return word

    # replace bi verb endings with bi
    for ending in bi_verb_endings:
        if word.endswith(ending):
            word = re.sub(r"{0}$".format(ending), "bi", word)
            return word

    # replace eri verb endings with eri
    for ending in eri_verb_endings:
        if word.endswith(ending):
            word = re.sub(r"{0}$".format(ending), "eri", word)
            return word

    # otherwise, remove general verb endings
    for ending in verb_endings:
        if word.endswith(ending):
            word = re.sub(r"{0}$".format(ending), "", word)
            break

    return word


def stem(word: str) -> str:
    """
    Stem each word of the Latin text.

    >>> stem('interdum')
    'interd'
    >>> stem('mercaturis')
    'mercatur'
    """

    if word not in STOPS:
        # remove '-que' suffix
        word, in_que_pass_list = _checkremove_que(word)

        if not in_que_pass_list:
            # remove the simple endings from the target word
            word, was_stemmed = _matchremove_simple_endings(word)

            # if word didn't match the simple endings, try verb endings
            if not was_stemmed:
                word = _matchremove_verb_endings(word)

    return word
